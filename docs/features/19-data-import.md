# Data import

## Summary

This area lets HR load data from spreadsheets instead of typing it in: new employees, updates to existing employees, assets, asset allocations, assigned leave balances and salary structures. A step-by-step wizard checks the file before anything is saved and reports errors row by row. This is separate from the attendance spreadsheet import, which is described in [Attendance](05-attendance.md).

## Who uses it

- HR and administrators who set up or bulk-change data.

## Features

### The import wizard

- Steps: upload a file, match its columns to the system's fields, check the rows (rows with errors can be corrected on screen), run the import with a progress bar, and see a summary with an error workbook. Past imports are kept in a history. *Not yet verified in the code.*

### What can be imported

- New employees, updates to existing employees, assets, asset allocations, assigned leave balances and salary structures (`master_import/datasets/`).

### Rules when updating existing employees

- Rule: only the matched person is changed, a blank cell never overwrites a value, and a row that matches nobody or more than one person is an error, not a guess (`master_import/datasets/employee_update.py`). Reason: not stated in the code.

### Rules when a name is shared by several companies

- Rule: when a row names, for example, a department that exists in several companies, the import prefers the one that belongs to the active company, then one shared by all companies, and otherwise takes any record with that name (`master_import/datasets/scoping.py`). Reason: not stated in the code.

> Flag (risk): found while checking the code for this report. When the active company has no record with the given name and there is no shared one, the import takes another company's record with that name. Business effect: imported employees can be linked to another company's department or job position without any warning.

> Flag (risk): the import area's 132 automatic tests are not part of the quick test set that runs before changes are merged (`Makefile`). Business effect: a change that breaks imports can be merged without anyone noticing.

## Who can do what

| Action | Who |
|---|---|
| Import new records of a kind | Superusers, and people with the add permission for that kind of record |
| Update existing records by import | Superusers, and people with all the change permissions that kind of import needs |
| See or continue an import | The person who started it, and superusers |

These come from the access checks in the import screens (`master_import/views.py`).

## Recommendations

- Suggestion: when a name exists only in another company, report it as an error instead of using that company's record.
- Suggestion: add the import tests to the quick test set that runs before merging.

## Related documents

- [Attendance](05-attendance.md): the separate attendance spreadsheet import.
- [Horilla HRM feature reference](../Horilla_HRM_FEATURES.md)

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
