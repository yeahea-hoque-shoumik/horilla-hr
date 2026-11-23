# Test Results: Product Feature Report

Run on 2026-11-19 from the project root. Inputs: `construction/code-generation/code-generation-plan.md`, `construction/code-generation/unit-test-instructions.md`, `construction/code-generation/code-summary.md`.

## Build status

- Command: `python3 -m py_compile docs/features/tools/check_report.py docs/features/tools/test_check_report.py`
- Exit code: 0. **Success.**

## Unit tests (stage-level instructions, one distinct command)

- Command: `python3 docs/features/tools/test_check_report.py`
- Exit code: 0. Ran 8 tests in 0.064s, OK.
- Total 8, passed 8, failed 0, skipped 0.
- The lines "07-payroll.md: expected file is missing / 1 problem(s) found." in the output are printed by the checker inside the missing-file test on purpose; they are not a real problem.

| Test | Result |
|------|--------|
| test_complete_minimal_report_passes | ok |
| test_empty_change_log_fails | ok |
| test_missing_file_fails | ok |
| test_missing_flag_fails | ok |
| test_missing_index_link_fails | ok |
| test_missing_section_fails | ok |
| test_six_line_code_block_fails | ok |
| test_undefined_bold_term_fails | ok |

## Integration test

- Command: `python3 docs/features/tools/check_report.py docs/features`
- Exit code: 0. Output: "Report check passed: 25 files, 0 problems."

## Existing application suite

- No application code, settings or tests changed: `git status --porcelain --untracked-files=no` lists no tracked file changes. The existing Django test suite was not re-run because nothing it covers changed.

## Failure details

- None.

## Coverage report

- No line-coverage floor applies (Testing Contract: bugfix scope floor and Standard strategy volume only). The checker's 8 rules each have a test; rule 7 (reason wording) is exercised by the passing case only.

## Target Verification Matrix

| Target ID | Source | Expected | Actual | Evidence | Owning Stage | Verdict |
|---|---|---|---|---|---|---|
| TC-VOL | code-generation-plan.md > Testing Contract > strategy_volume | 5 to 8 tests per component (1 component: the checker) | 8 tests | `python3 docs/features/tools/test_check_report.py`, exit 0 | build-and-test | Met |
| TC-INT | code-generation-plan.md > Testing Contract > strategy_volume | Integration test for the key boundary | Checker run over the real report, 0 problems | `python3 docs/features/tools/check_report.py docs/features`, exit 0 | build-and-test | Met |
| TC-REG | code-generation-plan.md > Testing Contract > scope_floor | Targeted regression for the bug | No bug is fixed in this documentation work; the plan names the checker run as its equivalent | Plan "How the contract applies here"; integration run exit 0 | build-and-test | Met |
| TC-GREEN | code-generation-plan.md > Testing Contract > scope_floor | Existing test suite stays green | No tracked application file changed, so no existing test's code or subject changed | `git status --porcelain --untracked-files=no` empty | build-and-test | Met |
| RQ-NFR1 | requirements.md > NFR1 | 22/22 areas, all 27 flags present | 25 files incl. 22 areas; 27 flags found in home files | Checker rules 1 and 8, exit 0 | build-and-test | Met |
| RQ-NFR3 | requirements.md > NFR3 | Every bold term in glossary; summaries at most 5 sentences | 0 undefined bold terms; summary length checked once by the builder's read-only script | Checker rule 6, exit 0; code-summary.md | build-and-test | Met |
| RQ-FR5.2 | requirements.md > FR5.2 / plan writing rules | No code block over 5 lines | 0 violations | Checker rule 5, exit 0 | build-and-test | Met |
