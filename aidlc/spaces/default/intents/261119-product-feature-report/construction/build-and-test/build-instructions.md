# Build Instructions: Product Feature Report

Upstream: `construction/code-generation/code-generation-plan.md`, `construction/code-generation/unit-test-instructions.md`, `construction/code-generation/code-summary.md`.

## Dependency installation

- None. The deliverable is Markdown under `docs/features/` plus a checker that uses only the Python 3 standard library.
- Requires Python 3 on the path (verified: Python 3.14.0).

## Environment setup

- No environment variables, settings, database or services. The HR application is not started.
- Run every command from the project root.

## Build commands

There is nothing to compile or bundle. The "build" is a syntax check of the two checker scripts:

```
python3 -m py_compile docs/features/tools/check_report.py docs/features/tools/test_check_report.py
```

## Build verification

- The command exits 0 (verified on 2026-11-19).
- `git status --porcelain --untracked-files=no` shows no tracked application file changed; the only new content is `docs/features/` (and the `aidlc/` record).

## Troubleshooting

- `python3: command not found`: install Python 3 or use the interpreter path your system provides.
- A `__pycache__/` folder appears under `docs/features/tools/` after running; it is ignored by git and safe to delete.
- If a Markdown viewer does not open the link to `docs/ApurbApurba_HRM-v2_vs_Horilla_HRMS—Feature_Comparison.md` (its name contains an em dash), open the file directly from the `docs/` folder.
