# Report checking tool

This folder holds a small tool that checks the product feature report in `docs/features/` after anyone edits it, and the tool's own tests. It needs only Python 3; it does not use Django or any part of the HR application.

## What the checker verifies

`check_report.py` reports a problem when:

1. any of the 25 expected report files is missing (the index, the overall file, the 22 area files and the glossary);
2. the index (`README.md`) does not link to every other report file;
3. an area file lacks one of the required sections, or has them out of order: Summary, Who uses it, Features, Who can do what, Recommendations, Related documents, Change log;
4. a file's change log has no dated entry;
5. a fenced code block is longer than 5 lines, or is never closed;
6. a term written in bold has no entry in `glossary.md` (a plural form matches its singular entry);
7. a "Reason:" line is empty, reads as a guess, or says there is no reason in any wording other than exactly "Reason: not stated in the code";
8. one of the 27 consolidated flags is missing from its home file. The checker holds the list of flags with each one's home file and a key phrase; if a flag's wording is changed on purpose, update its key phrase in `FLAGS` in `check_report.py` in the same change.

The checker does not judge whether the content is correct or complete beyond these rules. A reviewer still has to compare each area file with the code knowledge base (`aidlc/spaces/default/codekb/horilla-hr/business-overview.md`).

## How to run it

From the project root, after editing any report file:

```
python3 docs/features/tools/check_report.py docs/features
```

It prints each problem on its own line and exits with 1, or prints "Report check passed" and exits with 0. It exits with 2 when the folder cannot be found.

To run the checker's own tests:

```
python3 docs/features/tools/test_check_report.py
```

## When you update the report

- Edit only the area file the change belongs to, and add a row to its change log with the date, what changed and who changed it.
- Write any new term in bold on its first use in the file, and add it to `glossary.md`.
- Run the checker and fix every problem it lists.

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
