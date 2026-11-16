#!/usr/bin/env python3
"""
Build a foreign-key dependency tree of the tables in the active schema of a PostgreSQL db.

    python3 scripts/db/fk_dependency_tree.py                       # print tree in terminal
    python3 scripts/db/fk_dependency_tree.py --html tree.html      # also write browser view
    python3 scripts/db/fk_dependency_tree.py --json tree.json      # also dump tree object
    python3 scripts/db/fk_dependency_tree.py --direction depends-on
    python3 scripts/db/fk_dependency_tree.py --schema other_schema

Connection comes from POSTGRES_HOST / PORT / USER / PASSWORD / DATABASE in the project .env
(real environment variables win over .env). Schema defaults to the one active on the
connection (`current_schema()`, i.e. first entry of search_path); --schema overrides it.

Only table names are used as nodes; columns are not reported. Only foreign keys between
tables inside the same schema are followed.

Directions
  dependents  (default)  roots = tables that reference nothing; children = tables whose
                         foreign keys point at the parent. Reads like a build/load order.
  depends-on             roots = tables nothing references; children = tables the parent
                         points at through its foreign keys.

A table reachable through several parents is fully expanded only the first time; later
occurrences are leaves marked "see above" (the real edges are all still in the `graph`
object). A back edge to an ancestor is marked "cycle". Tables with no foreign key in or
out are listed separately as isolated.

Dependency object (returned by build_dependency_object, also written by --json):
    {
      "schema": "public",
      "direction": "dependents",
      "graph":  {table: {"depends_on": [...], "dependents": [...],
                         "depth_depends_on": n, "all_depends_on": n, "all_dependents": n}},
      "tree":   {"name": "<schema>", "kind": "root", "children": [node, ...]},
      "isolated": [table, ...]
    }
    node = {"name": str, "kind": "node" | "ref" | "cycle", "children": [node, ...]}
"""
import argparse
import html
import json
import os
import sys
from pathlib import Path

import psycopg2
from dotenv import dotenv_values

PROJECT_ROOT = Path(__file__).resolve().parent

TABLES_SQL = """
    SELECT c.relname
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = %s AND c.relkind IN ('r', 'p') AND NOT c.relispartition
    ORDER BY c.relname
"""

FKS_SQL = """
    SELECT DISTINCT child.relname, parent.relname
    FROM pg_constraint con
    JOIN pg_class child ON child.oid = con.conrelid
    JOIN pg_namespace cn ON cn.oid = child.relnamespace
    JOIN pg_class parent ON parent.oid = con.confrelid
    JOIN pg_namespace pn ON pn.oid = parent.relnamespace
    WHERE con.contype = 'f' AND cn.nspname = %s AND pn.nspname = %s
"""


# --------------------------------------------------------------------------- db
def load_env():
    env = {**dotenv_values(PROJECT_ROOT / ".env"), **os.environ}
    missing = [k for k in ("POSTGRES_HOST", "POSTGRES_USER", "POSTGRES_DATABASE") if not env.get(k)]
    if missing:
        sys.exit(f"missing in .env / environment: {', '.join(missing)}")
    return env


def fetch_edges(env, schema_override=None):
    """Return (schema, tables, edges); edge = (child_table, parent_table)."""
    conn = psycopg2.connect(
        host=env["POSTGRES_HOST"],
        port=env.get("POSTGRES_PORT") or 5432,
        user=env["POSTGRES_USER"],
        password=env.get("POSTGRES_PASSWORD") or None,
        dbname=env["POSTGRES_DATABASE"],
        connect_timeout=10,
    )
    try:
        with conn.cursor() as cur:
            if schema_override:
                schema = schema_override
            else:
                cur.execute("SELECT current_schema()")
                schema = cur.fetchone()[0]
            cur.execute(TABLES_SQL, (schema,))
            tables = [r[0] for r in cur.fetchall()]
            cur.execute(FKS_SQL, (schema, schema))
            edges = [(c, p) for c, p in cur.fetchall()]
    finally:
        conn.close()
    if not tables:
        sys.exit(f"no tables found in schema '{schema}'")
    return schema, tables, edges


# ------------------------------------------------------------------ graph / tree
def build_graph(tables, edges):
    """depends_on[t] = tables t references; dependents[t] = tables referencing t. Self-FKs dropped."""
    depends_on = {t: set() for t in tables}
    dependents = {t: set() for t in tables}
    for child, parent in edges:
        if child == parent or child not in depends_on or parent not in depends_on:
            continue
        depends_on[child].add(parent)
        dependents[parent].add(child)
    return depends_on, dependents


def closure(start, adj):
    """All tables reachable from start (excluding start unless it sits on a cycle)."""
    seen, stack = set(), list(adj[start])
    while stack:
        t = stack.pop()
        if t in seen:
            continue
        seen.add(t)
        stack.extend(adj[t])
    return seen


def depth_map(depends_on):
    """Longest FK chain below each table (0 = references nothing). Cycles are cut."""
    memo, visiting = {}, set()

    def depth(t):
        if t in memo:
            return memo[t]
        if t in visiting:
            return 0
        visiting.add(t)
        d = 1 + max((depth(p) for p in depends_on[t]), default=-1)
        visiting.discard(t)
        memo[t] = d
        return d

    for t in depends_on:
        depth(t)
    return memo


def build_tree(schema, depends_on, dependents, direction):
    child_of = dependents if direction == "dependents" else depends_on
    parent_of = depends_on if direction == "dependents" else dependents

    connected = [t for t in depends_on if depends_on[t] or dependents[t]]
    isolated = sorted(t for t in depends_on if not depends_on[t] and not dependents[t])

    expanded, path = set(), []

    def visit(name):
        if name in path:
            return {"name": name, "kind": "cycle", "children": []}
        if name in expanded:
            return {"name": name, "kind": "ref" if child_of[name] else "node", "children": []}
        expanded.add(name)
        path.append(name)
        kids = [visit(c) for c in sorted(child_of[name])]
        path.pop()
        return {"name": name, "kind": "node", "children": kids}

    roots = sorted(t for t in connected if not parent_of[t])
    children = [visit(r) for r in roots]
    # tables only reachable through a cycle have no natural root: start from the least-dependent
    for t in sorted((t for t in connected if t not in expanded), key=lambda t: (len(parent_of[t]), t)):
        if t not in expanded:
            children.append(visit(t))
    return {"name": schema, "kind": "root", "children": children}, isolated


def build_dependency_object(schema, tables, edges, direction="dependents"):
    depends_on, dependents = build_graph(tables, edges)
    depth = depth_map(depends_on)
    graph = {
        t: {
            "depends_on": sorted(depends_on[t]),
            "dependents": sorted(dependents[t]),
            "depth_depends_on": depth[t],
            "all_depends_on": len(closure(t, depends_on) - {t}),
            "all_dependents": len(closure(t, dependents) - {t}),
        }
        for t in sorted(tables)
    }
    tree, isolated = build_tree(schema, depends_on, dependents, direction)
    return {"schema": schema, "direction": direction, "graph": graph, "tree": tree, "isolated": isolated}


# --------------------------------------------------------------------- terminal
def render_text(obj, color=False):
    def c(code, s):
        return f"\033[{code}m{s}\033[0m" if color else s

    graph = obj["graph"]
    lines = []

    def label(node):
        info = graph[node["name"]]
        n = len(info["dependents"] if obj["direction"] == "dependents" else info["depends_on"])
        name = node["name"]
        if node["kind"] == "ref":
            return f"{c('2', name)} {c('33', '↗ see above')}"
        if node["kind"] == "cycle":
            return f"{name} {c('31', '↻ cycle')}"
        return c("1", name) if not node["children"] else f"{c('1;36', name)} {c('2', f'({n})')}"

    def walk(node, prefix):
        kids = node["children"]
        for i, kid in enumerate(kids):
            last = i == len(kids) - 1
            lines.append(f"{prefix}{'└── ' if last else '├── '}{label(kid)}")
            walk(kid, prefix + ("    " if last else "│   "))

    lines.append(c("1;35", obj["tree"]["name"]))
    walk(obj["tree"], "")
    if obj["isolated"]:
        lines.append("")
        lines.append(c("2", f"isolated (no foreign keys): {', '.join(obj['isolated'])}"))
    return "\n".join(lines)


def summary(obj):
    g = obj["graph"]
    n_edges = sum(len(v["depends_on"]) for v in g.values())
    direction = {
        "dependents": "root = references nothing; child = table that references parent",
        "depends-on": "root = referenced by nothing; child = table the parent references",
    }[obj["direction"]]
    return (
        f"schema '{obj['schema']}': {len(g)} tables, {n_edges} FK edges, "
        f"{len(obj['isolated'])} isolated\n"
        f"direction {obj['direction']}: {direction}\n"
    )


# ------------------------------------------------------------------------- html
HTML_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FK dependency tree - __SCHEMA__</title>
<style>
  :root {
    --bg:#f7f8fa; --panel:#ffffff; --ink:#1f2933; --muted:#6b7785; --line:#b9c2cc; --border:#d9dee4;
    --root:#2f7d5b; --node:#3b7dd8; --leaf:#8a94a0; --hl:#e8a317; --cycle:#d64545;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg:#14181d; --panel:#1c2229; --ink:#e6e9ed; --muted:#8d99a6; --line:#47525e; --border:#2d3640;
      --root:#4fb283; --node:#6aa2ee; --leaf:#7b8794; --hl:#f2b94a; --cycle:#ef6b6b;
    }
  }
  * { box-sizing:border-box; }
  html,body { height:100%; margin:0; }
  body { background:var(--bg); color:var(--ink); font:14px/1.4 system-ui,-apple-system,"Segoe UI",sans-serif;
         display:flex; flex-direction:column; }
  header { display:flex; flex-wrap:wrap; gap:10px 16px; align-items:center; padding:10px 16px;
           background:var(--panel); border-bottom:1px solid var(--border); }
  h1 { font-size:16px; margin:0; font-weight:600; }
  .meta { color:var(--muted); font-size:12px; }
  .controls { display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-left:auto; }
  button,input { font:inherit; color:var(--ink); background:var(--bg); border:1px solid var(--border);
                 border-radius:6px; padding:5px 10px; }
  button { cursor:pointer; } button:hover { border-color:var(--node); }
  button.on { background:var(--node); border-color:var(--node); color:#fff; }
  input { width:180px; }
  #stage { flex:1; position:relative; overflow:hidden; cursor:grab; touch-action:none; }
  #stage.drag { cursor:grabbing; }
  svg { width:100%; height:100%; display:block; }
  .link { fill:none; stroke:var(--line); stroke-width:1.4; }
  .node circle { stroke-width:2; transition:r .12s; }
  .node.root circle { fill:var(--root); stroke:var(--root); }
  .node.node circle { fill:var(--node); stroke:var(--node); }
  .node.leaf circle { fill:var(--panel); stroke:var(--node); }
  .node.ref circle { fill:var(--panel); stroke:var(--leaf); stroke-dasharray:3 2; }
  .node.cycle circle { fill:var(--panel); stroke:var(--cycle); stroke-dasharray:3 2; }
  .node.collapsed circle { stroke-width:4; }
  .node text { fill:var(--ink); font-size:11px; text-anchor:middle; pointer-events:none;
               paint-order:stroke; stroke:var(--bg); stroke-width:3px; stroke-linejoin:round; }
  .node.ref text { fill:var(--muted); }
  .node.match circle { stroke:var(--hl); stroke-width:4; }
  .node.match text { font-weight:700; }
  .node.dim { opacity:.25; }
  .node { cursor:pointer; }
  .node:hover circle { r:11; }
  #tip { position:absolute; pointer-events:none; background:var(--panel); border:1px solid var(--border);
         border-radius:8px; padding:8px 10px; font-size:12px; max-width:320px; display:none;
         box-shadow:0 4px 14px rgba(0,0,0,.18); }
  #tip b { font-size:13px; } #tip .k { color:var(--muted); }
  #legend { position:absolute; left:12px; bottom:12px; background:var(--panel); border:1px solid var(--border);
            border-radius:8px; padding:8px 10px; font-size:12px; color:var(--muted); }
  #legend span { display:inline-flex; align-items:center; gap:5px; margin-right:12px; }
  #legend i { width:12px; height:12px; border-radius:50%; display:inline-block; border:2px solid; }
  #iso { padding:6px 16px; background:var(--panel); border-top:1px solid var(--border); font-size:12px;
         color:var(--muted); max-height:72px; overflow:auto; }
  @media (max-width:640px) { .controls { margin-left:0; } input { width:130px; } }
</style>
</head>
<body>
<header>
  <div>
    <h1>FK dependency tree - <span id="schema"></span></h1>
    <div class="meta" id="meta"></div>
  </div>
  <div class="controls">
    <button id="dir-dependents" title="root = references nothing; child = table that references parent">dependents</button>
    <button id="dir-depends-on" title="root = referenced by nothing; child = table the parent references">depends on</button>
    <input id="q" type="search" placeholder="find table...">
    <button id="expand">expand all</button>
    <button id="collapse">collapse all</button>
    <button id="fit">fit</button>
  </div>
</header>
<div id="stage">
  <svg id="svg"><g id="vp"><g id="links"></g><g id="nodes"></g></g></svg>
  <div id="tip"></div>
  <div id="legend">
    <span><i style="border-color:var(--root);background:var(--root)"></i>top of tree</span>
    <span><i style="border-color:var(--node);background:var(--node)"></i>has children</span>
    <span><i style="border-color:var(--node);background:var(--panel)"></i>leaf</span>
    <span><i style="border-color:var(--leaf);border-style:dashed;background:var(--panel)"></i>shown above</span>
    <span><i style="border-color:var(--cycle);border-style:dashed;background:var(--panel)"></i>cycle</span>
    &middot; click node: fold / unfold &middot; drag: pan &middot; wheel: zoom
  </div>
</div>
<div id="iso"></div>
<script>
const DATA = __DATA__;
const NS = "http://www.w3.org/2000/svg";
const GAP_X = 150, GAP_Y = 90, R = 9, PAD = 60;
let direction = DATA.direction;
let tx = 0, ty = 0, scale = 1;
const collapsed = new Set();           // node ids (path strings)
let query = "";

const $ = id => document.getElementById(id);
const svg = $("svg"), vp = $("vp"), stage = $("stage"), tip = $("tip");

$("schema").textContent = DATA.schema;
const g = DATA.graph;
const edgeCount = Object.values(g).reduce((n, v) => n + v.depends_on.length, 0);
$("meta").textContent = Object.keys(g).length + " tables, " + edgeCount + " foreign keys";
$("iso").textContent = DATA.isolated.length
  ? "Isolated (no foreign keys): " + DATA.isolated.join(", ")
  : "No isolated tables.";
if (!DATA.isolated.length) $("iso").style.display = "none";

function el(name, attrs, parent) {
  const e = document.createElementNS(NS, name);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}

// assign ids by path so folding survives re-render
function annotate(node, id) {
  node.id = id;
  node.children.forEach((c, i) => annotate(c, id + "/" + i));
}
function layout(node, depth, state) {
  node.depth = depth;
  const kids = collapsed.has(node.id) ? [] : node.children;
  node.visible = kids;
  if (!kids.length) { node.x = state.next++ * GAP_X; }
  else {
    kids.forEach(k => layout(k, depth + 1, state));
    node.x = (kids[0].x + kids[kids.length - 1].x) / 2;
  }
  node.y = depth * GAP_Y;
}
function collect(node, out) { out.push(node); node.visible.forEach(k => collect(k, out)); return out; }

function render() {
  const tree = TREES[direction];
  layout(tree, 0, { next: 0 });
  const nodes = collect(tree, []);
  const linksG = $("links"), nodesG = $("nodes");
  linksG.textContent = ""; nodesG.textContent = "";
  const q = query.trim().toLowerCase();

  nodes.forEach(n => n.visible.forEach(k => {
    if (n.kind === "root") return;      // schema node is only an anchor
    const my = (n.y + k.y) / 2;
    el("path", { class: "link", d: `M${n.x},${n.y + R} C${n.x},${my} ${k.x},${my} ${k.x},${k.y - R}` }, linksG);
  }));
  nodes.forEach(n => {
    if (n.kind === "root") return;
    const isLeaf = n.children.length === 0;
    const cls = ["node", n.depth === 1 ? "root" : n.kind === "ref" ? "ref" : n.kind === "cycle" ? "cycle"
                 : isLeaf ? "leaf" : "node"];
    if (collapsed.has(n.id)) cls.push("collapsed");
    if (q) cls.push(n.name.toLowerCase().includes(q) ? "match" : "dim");
    const grp = el("g", { class: cls.join(" "), transform: `translate(${n.x},${n.y})` }, nodesG);
    el("circle", { r: R }, grp);
    const t = el("text", { y: R + 14 }, grp);
    t.textContent = n.name + (collapsed.has(n.id) ? " (+" + countDesc(n) + ")" : "");
    grp.addEventListener("click", () => { if (n.children.length) { toggle(n.id); } });
    grp.addEventListener("mousemove", ev => showTip(ev, n));
    grp.addEventListener("mouseleave", () => tip.style.display = "none");
  });
  apply();
  return nodes;
}
function countDesc(n) { return n.children.reduce((s, c) => s + 1 + countDesc(c), 0); }
function toggle(id) { collapsed.has(id) ? collapsed.delete(id) : collapsed.add(id); render(); }

function showTip(ev, n) {
  const info = g[n.name];
  const list = a => a.length ? a.join(", ") : "none";
  tip.innerHTML = `<b>${n.name}</b><br>
    <span class="k">depends on (${info.depends_on.length}):</span> ${list(info.depends_on)}<br>
    <span class="k">dependents (${info.dependents.length}):</span> ${list(info.dependents)}<br>
    <span class="k">all upstream / downstream:</span> ${info.all_depends_on} / ${info.all_dependents}<br>
    <span class="k">FK depth:</span> ${info.depth_depends_on}`;
  tip.style.display = "block";
  const r = stage.getBoundingClientRect();
  let x = ev.clientX - r.left + 14, y = ev.clientY - r.top + 14;
  if (x + 330 > r.width) x = ev.clientX - r.left - 330;
  if (y + tip.offsetHeight > r.height) y = r.height - tip.offsetHeight - 8;
  tip.style.left = Math.max(4, x) + "px"; tip.style.top = Math.max(4, y) + "px";
}

function apply() { vp.setAttribute("transform", `translate(${tx},${ty}) scale(${scale})`); }
function fit(nodes) {
  nodes = nodes || collect(TREES[direction], []).filter(n => n.kind !== "root");
  if (!nodes.length) return;
  const xs = nodes.map(n => n.x), ys = nodes.map(n => n.y);
  const minX = Math.min(...xs) - PAD, maxX = Math.max(...xs) + PAD;
  const minY = Math.min(...ys) - PAD, maxY = Math.max(...ys) + PAD + 20;
  const w = stage.clientWidth, h = stage.clientHeight;
  scale = Math.min(w / (maxX - minX), h / (maxY - minY), 1.2);
  tx = (w - (maxX - minX) * scale) / 2 - minX * scale;
  ty = (h - (maxY - minY) * scale) / 2 - minY * scale;
  apply();
}

// pan / zoom
let drag = null;
stage.addEventListener("pointerdown", e => {
  if (e.target.closest(".node")) return;
  drag = { x: e.clientX - tx, y: e.clientY - ty }; stage.classList.add("drag"); stage.setPointerCapture(e.pointerId);
});
stage.addEventListener("pointermove", e => { if (drag) { tx = e.clientX - drag.x; ty = e.clientY - drag.y; apply(); } });
stage.addEventListener("pointerup", () => { drag = null; stage.classList.remove("drag"); });
stage.addEventListener("wheel", e => {
  e.preventDefault();
  const r = stage.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top;
  const k = Math.exp(-e.deltaY * 0.0015), ns = Math.min(4, Math.max(0.1, scale * k));
  tx = mx - (mx - tx) * (ns / scale); ty = my - (my - ty) * (ns / scale); scale = ns; apply();
}, { passive: false });

// controls
function setDir(d) {
  direction = d; collapsed.clear();
  $("dir-dependents").classList.toggle("on", d === "dependents");
  $("dir-depends-on").classList.toggle("on", d === "depends-on");
  fit(render());
}
$("dir-dependents").onclick = () => setDir("dependents");
$("dir-depends-on").onclick = () => setDir("depends-on");
$("expand").onclick = () => { collapsed.clear(); fit(render()); };
$("collapse").onclick = () => {
  collapsed.clear();
  TREES[direction].children.forEach(r => { if (r.children.length) collapsed.add(r.id); });
  fit(render());
};
$("fit").onclick = () => fit();
$("q").oninput = e => { query = e.target.value; render(); };
window.addEventListener("resize", () => fit());

const TREES = { "dependents": DATA.trees["dependents"], "depends-on": DATA.trees["depends-on"] };
Object.values(TREES).forEach(t => annotate(t, "r"));
setDir(direction);
</script>
</body>
</html>
"""


def render_html(schema, tables, edges, direction):
    objs = {d: build_dependency_object(schema, tables, edges, d) for d in ("dependents", "depends-on")}
    base = objs[direction]
    payload = {
        "schema": schema,
        "direction": direction,
        "graph": base["graph"],
        "isolated": base["isolated"],
        "trees": {d: o["tree"] for d, o in objs.items()},
    }
    data = json.dumps(payload).replace("</", "<\\/")
    return HTML_TEMPLATE.replace("__SCHEMA__", html.escape(schema)).replace("__DATA__", data)


# ------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--schema", help="schema to inspect (default: active schema of the connection)")
    ap.add_argument("--direction", choices=("dependents", "depends-on"), default="dependents")
    ap.add_argument("--html", metavar="FILE", help="write a self-contained HTML tree view")
    ap.add_argument("--json", metavar="FILE", help="write the dependency object as JSON")
    ap.add_argument("--no-color", action="store_true")
    args = ap.parse_args()

    schema, tables, edges = fetch_edges(load_env(), args.schema)
    obj = build_dependency_object(schema, tables, edges, args.direction)

    print(summary(obj))
    print(render_text(obj, color=sys.stdout.isatty() and not args.no_color))

    if args.json:
        Path(args.json).write_text(json.dumps(obj, indent=2))
        print(f"\njson written: {args.json}")
    if args.html:
        Path(args.html).write_text(render_html(schema, tables, edges, args.direction), encoding="utf-8")
        print(f"\nhtml written: {args.html}")


if __name__ == "__main__":
    main()
