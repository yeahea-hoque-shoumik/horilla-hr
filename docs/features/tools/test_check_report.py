#!/usr/bin/env python3
"""
Unit tests for check_report.py.

Run from the project root:

    python3 docs/features/tools/test_check_report.py

Each test builds a small but complete fake report in a temporary folder, breaks
one thing, and checks that the checker reports exactly that kind of problem.
Uses the Python standard library only; no Django and no application code.
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_report  # noqa: E402

CHANGE_LOG = (
    "## Change log\n\n"
    "| Date | What changed | Who changed it |\n"
    "|---|---|---|\n"
    "| 2026-11-19 | First version. | Test |\n"
)


def area_text(extra=""):
    """A minimal area file with every required section, in order."""
    body = "".join(
        f"## {section}\n\nText.\n\n" for section in check_report.REQUIRED_SECTIONS[:-1]
    )
    return f"# Area\n\n{body}{extra}\n{CHANGE_LOG}"


def minimal_report():
    """File name -> content for a complete report that passes every check."""
    others = [name for name in check_report.EXPECTED_FILES if name != check_report.INDEX_FILE]
    links = "".join(f"- [{name}]({name})\n" for name in others)
    texts = {
        check_report.INDEX_FILE: f"# Index\n\n{links}\n{CHANGE_LOG}",
        check_report.OVERALL_FILE: f"# Overall\n\n## Summary\n\nText.\n\n{CHANGE_LOG}",
        check_report.GLOSSARY_FILE: (
            f"# Glossary\n\n## Terms\n\n- **Grace time**: minutes allowed.\n\n{CHANGE_LOG}"
        ),
    }
    extra = "Uses **grace time**. Reason: not stated in the code.\n"
    for name in check_report.AREA_FILES:
        texts[name] = area_text(extra)
    for _, home, phrase in check_report.FLAGS:
        texts[home] = texts[home].replace("## Change log", f"> Flag: {phrase}.\n\n## Change log", 1)
    return texts


class CheckReportTests(unittest.TestCase):
    """One test per checker rule, plus the passing case."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self._tmp.name)
        self.texts = minimal_report()
        self.write_all()

    def tearDown(self):
        self._tmp.cleanup()

    def write_all(self):
        for name, text in self.texts.items():
            (self.folder / name).write_text(text, encoding="utf-8")

    def rewrite(self, name, text):
        (self.folder / name).write_text(text, encoding="utf-8")

    def problems(self):
        return check_report.check_report(str(self.folder))

    def assert_problem(self, fragment):
        problems = self.problems()
        self.assertTrue(
            any(fragment in problem for problem in problems),
            f"expected a problem containing {fragment!r}, got {problems!r}",
        )

    def test_complete_minimal_report_passes(self):
        self.assertEqual(self.problems(), [])
        self.assertEqual(check_report.main(["check_report.py", str(self.folder)]), 0)

    def test_missing_file_fails(self):
        (self.folder / "07-payroll.md").unlink()
        self.assert_problem("07-payroll.md: expected file is missing")
        self.assertEqual(check_report.main(["check_report.py", str(self.folder)]), 1)

    def test_missing_index_link_fails(self):
        index = self.texts[check_report.INDEX_FILE].replace("- [12-projects.md](12-projects.md)\n", "")
        self.rewrite(check_report.INDEX_FILE, index)
        self.assert_problem("README.md: does not link to 12-projects.md")

    def test_missing_section_fails(self):
        text = self.texts["04-holidays-and-announcements.md"].replace("## Recommendations\n", "")
        self.rewrite("04-holidays-and-announcements.md", text)
        self.assert_problem("04-holidays-and-announcements.md: missing section '## Recommendations'")

    def test_empty_change_log_fails(self):
        text = self.texts["13-assets.md"].replace("| 2026-11-19 | First version. | Test |\n", "")
        self.rewrite("13-assets.md", text)
        self.assert_problem("13-assets.md: change log has no dated entry")

    def test_six_line_code_block_fails(self):
        five = "```\n" + "line\n" * 5 + "```\n\n"
        self.rewrite("16-reports.md", self.texts["16-reports.md"].replace("## Features", five + "## Features"))
        self.assertEqual(self.problems(), [], "a 5-line block is within the limit")
        six = "```\n" + "line\n" * 6 + "```\n\n"
        self.rewrite("16-reports.md", self.texts["16-reports.md"].replace("## Features", six + "## Features"))
        self.assert_problem("code block has 6 lines (limit 5)")

    def test_undefined_bold_term_fails(self):
        text = self.texts["19-data-import.md"].replace("## Features\n\nText.", "## Features\n\nA **payroll run**.")
        self.rewrite("19-data-import.md", text)
        self.assert_problem("bold term 'payroll run' has no glossary entry")

    def test_missing_flag_fails(self):
        home = "03-shifts-and-work-froms.md"
        text = self.texts[home].replace("monthly rotations crash in December", "something else")
        self.rewrite(home, text)
        self.assert_problem("flag #10 is missing")


if __name__ == "__main__":
    unittest.main(verbosity=2)
