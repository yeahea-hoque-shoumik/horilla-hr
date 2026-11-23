# Code Summary: Product Feature Report

## Files created

All new, all under `docs/features/` (no existing file changed; `git status` shows only `docs/features/` and the `aidlc/` record as new):

| File | What it holds |
|------|---------------|
| `docs/features/README.md` | Index: purpose, audience (people with repository access), code version, how to read flags, links to all 24 other files |
| `docs/features/00-how-the-system-works.md` | Ideas shared by every area, code version, fork changes, planned-but-not-built list, home of flags #1 and #26 |
| `docs/features/01-organisation-and-company-setup.md` … `22-mobile-app-api.md` | The 22 area files, each with Summary, Who uses it, Features, Who can do what, Recommendations, Related documents, Change log |
| `docs/features/glossary.md` | 46 entries, one per bold term |
| `docs/features/tools/check_report.py` | Report checker (8 rules, standard library only) |
| `docs/features/tools/test_check_report.py` | 8 unit tests of the checker |
| `docs/features/tools/README.md` | How to run the checker after editing the report |

## Key implementation decisions

- Flags follow the one-home rule from the plan; flag #13 (document expiry) lives in `15-employee-documents.md`, linked from `13-assets.md`, because the affected feature is document expiry.
- Flags are written as blockquotes ("> Flag (type): ..."), keeping bold for glossary terms.
- Payroll, leave and attendance "per doc" claims were checked in the code before being written, including flag #16. The check also found 10 default role groups (the knowledge base listed 9).
- New issues found while verifying were added as flags or notes beyond the original 27: the misspelt "leave encashment" type name that stops rejected encashments from giving days or points back; a whole month paid as unpaid when an attendance conflict stays open; candidate login using e-mail plus phone number; the Audit Activity report not limited to one company; the data import using another company's record when a name exists only there; face-check and geofence setup pages needing a permission that does not exist; employees able to replace their own face image.
- Claims not checked in the code carry "*Not yet verified in the code.*" (mainly in setup wizard, employee lifecycle extras, onboarding portal, reports calculation, platform experience).

## Test coverage summary

- `python3 docs/features/tools/test_check_report.py`: Ran 8 tests, OK (8 passed, 0 failed).
- `python3 docs/features/tools/check_report.py docs/features`: "Report check passed: 25 files, 0 problems."

## Tests written but not executed

- None. Both commands were run.
- Not covered by a dedicated failing test: checker rule 7 (reason wording); the approved plan lists exactly 8 tests, and rule 7 is exercised only by the passing case.
- NFR3 (summaries of at most 5 sentences), link targets and cited source paths were checked once by a read-only script, not by the checker.

## Deviations from the plan

- None. All 30 steps were done as planned and ticked.
