# Integration Test Instructions: Product Feature Report

Upstream: `construction/code-generation/code-generation-plan.md` (Step 29), `construction/code-generation/unit-test-instructions.md`, `construction/code-generation/code-summary.md`.

## What the key boundary is

The one boundary in this work is between the checker (`docs/features/tools/check_report.py`) and the real report folder (`docs/features/`). The unit tests use small fake reports; the integration test runs the checker over the actual 25 report files.

## Test framework setup and configuration

- Python 3 standard library only; no configuration file.

## How to run the tests

```
python3 docs/features/tools/check_report.py docs/features
```

Run from the project root. Exit 0 with "Report check passed: 25 files, 0 problems." means the report meets every checker rule: all 25 files present, every file linked from the index, required sections in order in the 22 area files, a dated change-log entry in every file, no code block over 5 lines, every bold term in the glossary, reason lines worded as allowed, and all 27 consolidated flags present in their home files.

## Expected coverage targets

- 0 problems (NFR1, NFR3, FR2.4, FR2.7, FR5.2).
- The checker proves presence and structure, not that each explanation is correct; accuracy was spot-checked by the reviewer against the code.

## Test data management and environment setup

- The test data is the report itself; nothing is created or deleted. Re-run after any edit to `docs/features/`.
