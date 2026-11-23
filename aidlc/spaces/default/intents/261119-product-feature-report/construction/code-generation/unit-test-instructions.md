# Unit Test Instructions: Product Feature Report

## Test framework setup and configuration

- Runner: Python 3 standard library `unittest` (Python 3.14.0 is installed). No extra package, no project settings, no database.
- The tests live in `docs/features/tools/test_check_report.py` and test the checker `docs/features/tools/check_report.py`.
- The tests do not import Django or any application module; they never touch the HR application.

## How to run this work's tests

Unit tests of the checker (exact, scoped to this work only):

```
python3 docs/features/tools/test_check_report.py
```

Check of the finished report (run separately, after the report is written):

```
python3 docs/features/tools/check_report.py docs/features
```

Both are run from the project root. Each exits 0 on success and non-zero with a list of problems on failure.

## Expected coverage targets

- 8 unit tests, one per checker rule (complete report passes; missing file; missing index link; missing section; empty change log; code block over 5 lines; undefined bold term; missing flag).
- No line-coverage floor applies to this scope (bugfix base: existing suite stays green, which it does because no application code changes).
- The report check must report 0 problems (NFR1, NFR3).

## Mocking and stubbing guidance

- No mocks. Each test builds a small fake report in a temporary folder (`tempfile.TemporaryDirectory`) and runs the checker's functions on it.

## Test data management

- Test data is created per test in the temporary folder and removed automatically. No fixture files are committed.
