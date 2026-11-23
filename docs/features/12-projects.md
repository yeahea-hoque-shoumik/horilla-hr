# Projects

## Summary

This area offers simple project tracking: projects with managers and members, stages shown as a board, tasks with assignees and deadlines, and timesheets recording time spent. It stands on its own and is not connected to payroll or attendance.

## Who uses it

- Project managers create projects, stages and tasks and manage members.
- Project members work on tasks and record time.
- HR or admins with project permissions can see and change all projects.

## Features

### Projects

- A project has managers, members, start and end dates and a document. Status: new, in progress, completed, on hold, cancelled or expired.

### Stages and tasks

- Each project has its own stages, shown as a board. Tasks have assignees and deadlines, and a status: to do, in progress, completed or expired.
- Rule: a task's dates must fall within its project's dates. Reason: not stated in the code.
- Rule: a project or task is marked as expired only when it is edited after its end date has passed. Reason: not stated in the code.

> Flag (gap): projects and tasks are marked expired only when someone edits them; no **background job** does it (`project/models.py`). Business effect: lists and dashboards show overdue projects and tasks as still in progress until someone happens to open and save them.

### Timesheets

- Members record time against a project and a task. A timesheet entry is in progress or completed.
- Timesheets are not linked to payroll or attendance, so time recorded here does not affect pay or worked hours.

## Who can do what

| Action | Who |
|---|---|
| Create and delete projects | People with the project add or delete permission (Admin, Project Manager) |
| Change a project, its stages and tasks | People with the project permissions, and the project's own managers |
| See a project and its tasks | People with the project view permission, and the project's managers and members |
| Record time | Project members, for themselves. *Not yet verified in the code.* |

These come from the permission and project manager-or-member checks on the project screens (`project/views.py`).

## Recommendations

- Suggestion: add a daily job that marks overdue projects and tasks as expired, or show "overdue" based on the date instead of a stored status.
- Suggestion: decide whether timesheets should feed attendance or payroll (for example for hourly workers), and say so on screen if they do not.
- Suggestion: add tests; the area has only two.

## Related documents

- [Attendance](05-attendance.md) and [Payroll](07-payroll.md): not connected to timesheets.
- [Horilla HRM feature reference](../Horilla_HRM_FEATURES.md)

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
