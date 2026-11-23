#!/usr/bin/env python3
"""
Check the product feature report in docs/features for completeness and style.

Usage (from the project root):

    python3 docs/features/tools/check_report.py docs/features

Exits 0 when the report passes every check, 1 when it finds problems (each one
is printed on its own line), and 2 when the folder cannot be checked at all.
Uses the Python standard library only.

The checks:
  1. every one of the 25 expected files exists;
  2. the index (README.md) links to every other expected file;
  3. every area file has the required sections, in order;
  4. every file's change log has at least one dated entry;
  5. no fenced code block is longer than 5 lines;
  6. every term written in bold has an entry in glossary.md;
  7. every "Reason:" line gives a stated reason or the exact wording
     "Reason: not stated in the code";
  8. each of the 27 consolidated flags appears in its home file.
"""

import re
import sys
from pathlib import Path

INDEX_FILE = "README.md"
OVERALL_FILE = "00-how-the-system-works.md"
GLOSSARY_FILE = "glossary.md"

AREA_FILES = (
    "01-organisation-and-company-setup.md",
    "02-employees.md",
    "03-shifts-and-work-froms.md",
    "04-holidays-and-announcements.md",
    "05-attendance.md",
    "06-leave.md",
    "07-payroll.md",
    "08-recruitment.md",
    "09-onboarding.md",
    "10-offboarding.md",
    "11-performance.md",
    "12-projects.md",
    "13-assets.md",
    "14-helpdesk.md",
    "15-employee-documents.md",
    "16-reports.md",
    "17-automations-and-notifications.md",
    "18-integrations.md",
    "19-data-import.md",
    "20-platform-experience.md",
    "21-security-and-access.md",
    "22-mobile-app-api.md",
)

EXPECTED_FILES = (INDEX_FILE, OVERALL_FILE) + AREA_FILES + (GLOSSARY_FILE,)

REQUIRED_SECTIONS = (
    "Summary",
    "Who uses it",
    "Features",
    "Who can do what",
    "Recommendations",
    "Related documents",
    "Change log",
)

MAX_CODE_BLOCK_LINES = 5
NOT_STATED = "not stated in the code"

# Words that turn a reason into a guess. A reason is either stated or "not stated".
GUESS_WORDS = ("probably", "likely", "presumably", "perhaps", "maybe", "might", "seems")

# Wordings that mean "no reason" but are not the agreed exact wording.
NO_REASON_WORDINGS = ("unknown", "unclear", "none", "n/a", "not given", "not documented")

# The 27 consolidated flags (business-overview.md section 6): number, home file,
# and a key phrase the home file must contain (matched case-insensitively).
FLAGS = (
    (1, OVERALL_FILE, "background jobs still use the server's clock"),
    (2, "06-leave.md", "which days are used first"),
    (3, "06-leave.md", "the approval order is not enforced"),
    (4, "06-leave.md", "sorted as text"),
    (5, "06-leave.md", "deleting a penalty gives back"),
    (6, "06-leave.md", "leave accrual"),
    (7, "07-payroll.md", "joined in the middle of the period"),
    (8, "07-payroll.md", "no Bangladesh tax pack"),
    (9, "08-recruitment.md", "recruitments past their end date stay open"),
    (10, "03-shifts-and-work-froms.md", "monthly rotations crash in December"),
    (11, "03-shifts-and-work-froms.md", "a roster change is never reverted"),
    (12, "02-employees.md", "overrides a later manual block"),
    (13, "15-employee-documents.md", "never actually saved"),
    (14, "05-attendance.md", "is not deleted when it is rejected"),
    (15, "05-attendance.md", "bulk attendance request with one invalid day"),
    (16, "05-attendance.md", "the Excel import writes the rows straight into the database"),
    (17, "05-attendance.md", "face matching is not done by this system"),
    (18, "05-attendance.md", "extra background pollers"),
    (19, "10-offboarding.md", "approving a resignation letter has no automatic effect"),
    (20, "12-projects.md", "only when someone edits them"),
    (21, "14-helpdesk.md", "no service-level targets"),
    (22, "09-onboarding.md", "the probation end date is recorded but nothing acts on it"),
    (23, "18-integrations.md", "LDAP login and user sync"),
    (24, "21-security-and-access.md", "removed the nginx web server gatekeeper"),
    (25, "21-security-and-access.md", "the access log added by this fork"),
    (26, OVERALL_FILE, "manager access is wider than a manager's own team"),
    (27, "17-automations-and-notifications.md", 'no user named exactly "Horilla Bot" exists'),
)

FENCE_RE = re.compile(r"^ {0,3}(```|~~~)")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
LINK_RE = re.compile(r"\]\(<?([^)>\s]+)>?\)")
GLOSSARY_ENTRY_RE = re.compile(r"^- \*\*(.+?)\*\*:")
REASON_RE = re.compile(r"\bReason(?:\s*\([^)]*\))?:\s*(.*)$")
CHANGE_LOG_ROW_RE = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|(.*)\|\s*$")


class ReportFolderError(Exception):
    """Raised when the report folder itself cannot be checked."""


def read_report(folder):
    """Read every expected file that exists. Returns (texts, problems)."""
    texts, problems = {}, []
    for name in EXPECTED_FILES:
        path = Path(folder) / name
        if not path.is_file():
            problems.append(f"{name}: expected file is missing")
            continue
        try:
            texts[name] = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            problems.append(f"{name}: cannot be read ({error})")
    return texts, problems


def prose_lines(text):
    """Yield (line number, line) for lines outside fenced code blocks."""
    inside = False
    for number, line in enumerate(text.splitlines(), start=1):
        if FENCE_RE.match(line):
            inside = not inside
            continue
        if not inside:
            yield number, line


def h2_headings(text):
    """The level-2 headings of a file, in order, outside code blocks."""
    return [line[3:].strip() for _, line in prose_lines(text) if line.startswith("## ")]


def section_lines(text, heading):
    """The lines under one level-2 heading, up to the next level-2 heading."""
    lines, inside = [], False
    for _, line in prose_lines(text):
        if line.startswith("## "):
            inside = line[3:].strip() == heading
            continue
        if inside:
            lines.append(line)
    return lines


def check_index_links(texts):
    """Rule 2: the index links to every other expected file."""
    if INDEX_FILE not in texts:
        return []
    targets = {target.split("#")[0].removeprefix("./") for target in LINK_RE.findall(texts[INDEX_FILE])}
    return [
        f"{INDEX_FILE}: does not link to {name}"
        for name in EXPECTED_FILES
        if name != INDEX_FILE and name not in targets
    ]


def check_sections(texts):
    """Rule 3: every area file has the required sections, in order."""
    problems = []
    for name in AREA_FILES:
        if name not in texts:
            continue
        headings = h2_headings(texts[name])
        missing = [s for s in REQUIRED_SECTIONS if s not in headings]
        for section in missing:
            problems.append(f"{name}: missing section '## {section}'")
        present = [s for s in REQUIRED_SECTIONS if s in headings]
        order = [headings.index(s) for s in present]
        if order != sorted(order):
            problems.append(f"{name}: sections are not in the required order")
    return problems


def has_change_log_entry(text):
    """True when the change log holds a dated row with a description."""
    for line in section_lines(text, "Change log"):
        match = CHANGE_LOG_ROW_RE.match(line.strip())
        if match and match.group(2).split("|")[0].strip():
            return True
    return False


def check_change_logs(texts):
    """Rule 4: every file's change log has at least one dated entry."""
    problems = []
    for name, text in texts.items():
        if "Change log" not in h2_headings(text):
            problems.append(f"{name}: has no '## Change log' section")
        elif not has_change_log_entry(text):
            problems.append(f"{name}: change log has no dated entry")
    return problems


def check_code_blocks(texts):
    """Rule 5: no fenced code block is longer than the limit, and every block is closed."""
    problems = []
    for name, text in texts.items():
        start, length = None, 0
        for number, line in enumerate(text.splitlines(), start=1):
            if FENCE_RE.match(line):
                if start is None:
                    start, length = number, 0
                    continue
                if length > MAX_CODE_BLOCK_LINES:
                    problems.append(
                        f"{name}:{start}: code block has {length} lines "
                        f"(limit {MAX_CODE_BLOCK_LINES})"
                    )
                start = None
            elif start is not None:
                length += 1
        if start is not None:
            problems.append(f"{name}:{start}: code block is never closed")
    return problems


def normalise_term(term):
    """Lower-case a term and drop surrounding spaces and punctuation."""
    return " ".join(term.lower().split()).strip(".:;,")


def glossary_terms(texts):
    """The normalised terms that have a glossary entry."""
    text = texts.get(GLOSSARY_FILE, "")
    return {normalise_term(m.group(1)) for _, line in prose_lines(text) if (m := GLOSSARY_ENTRY_RE.match(line))}


def is_defined(term, defined):
    """True when the term, or its singular form, has a glossary entry."""
    candidates = {term}
    if term.endswith("es"):
        candidates.add(term[:-2])
    if term.endswith("s"):
        candidates.add(term[:-1])
    return bool(candidates & defined)


def check_bold_terms(texts):
    """Rule 6: every term written in bold has a glossary entry."""
    defined, problems = glossary_terms(texts), []
    for name, text in texts.items():
        for number, line in prose_lines(text):
            for raw in BOLD_RE.findall(INLINE_CODE_RE.sub("", line)):
                term = normalise_term(raw)
                if term and not is_defined(term, defined):
                    problems.append(f"{name}:{number}: bold term '{raw}' has no glossary entry")
    return problems


def reason_problem(reason):
    """What is wrong with the text after 'Reason:', or None when it is acceptable."""
    if not reason:
        return "reason is empty"
    if NOT_STATED in reason.lower() or reason.lower().startswith("not stated"):
        rest = reason[len(NOT_STATED):]
        if reason.startswith(NOT_STATED) and (not rest or rest[0] in ".;,\"'"):
            return None
        return f"use the exact wording 'Reason: {NOT_STATED}'"
    if normalise_term(reason) in NO_REASON_WORDINGS:
        return f"use the exact wording 'Reason: {NOT_STATED}'"
    words = set(re.findall(r"[a-z]+", reason.lower()))
    guesses = sorted(words.intersection(GUESS_WORDS))
    if guesses:
        return f"reason reads as a guess ({', '.join(guesses)})"
    return None


def check_reasons(texts):
    """Rule 7: every 'Reason:' line gives a stated reason or the exact 'not stated' wording."""
    problems = []
    for name, text in texts.items():
        for number, line in prose_lines(text):
            for match in REASON_RE.finditer(line):
                problem = reason_problem(match.group(1).strip())
                if problem:
                    problems.append(f"{name}:{number}: {problem}")
    return problems


def comparable(text):
    """Text reduced for phrase matching: no bold marks, one kind of quote, lower case."""
    text = text.replace("**", "").replace("’", "'").replace("“", '"').replace("”", '"')
    return " ".join(text.lower().split())


def check_flags(texts):
    """Rule 8: each consolidated flag's key phrase appears in its home file."""
    problems = []
    for number, home, phrase in FLAGS:
        if home not in texts:
            continue
        if comparable(phrase) not in comparable(texts[home]):
            problems.append(f"{home}: flag #{number} is missing (key phrase: '{phrase}')")
    return problems


def check_report(folder):
    """Run every check on the report folder and return the list of problems."""
    if not Path(folder).is_dir():
        raise ReportFolderError(f"report folder not found: {folder}")
    texts, problems = read_report(folder)
    for check in (
        check_index_links,
        check_sections,
        check_change_logs,
        check_code_blocks,
        check_bold_terms,
        check_reasons,
        check_flags,
    ):
        problems.extend(check(texts))
    return problems


def main(argv):
    """Command-line entry point. Returns the process exit code."""
    if len(argv) != 2:
        print("usage: python3 docs/features/tools/check_report.py <report folder>", file=sys.stderr)
        return 2
    try:
        problems = check_report(argv[1])
    except ReportFolderError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    for problem in problems:
        print(problem)
    if problems:
        print(f"{len(problems)} problem(s) found.")
        return 1
    print(f"Report check passed: {len(EXPECTED_FILES)} files, 0 problems.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
