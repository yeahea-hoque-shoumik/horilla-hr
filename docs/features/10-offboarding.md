# Offboarding

## Summary

This area manages people leaving the company. HR places leavers in an exit pipeline with stages such as notice period, settlement, exit interview and work handover, assigns exit tasks, and records notes and files. Employees can submit a resignation letter, and moving a leaver into the final "archived" stage removes their access.

## Who uses it

- HR and offboarding managers set up exit pipelines, move leavers through stages and manage exit tasks.
- Stage managers and task owners work on the stages and tasks assigned to them.
- Employees submit resignation letters, when the feature is switched on.

## Features

### Exit pipelines and stages

- An exit pipeline is ongoing or completed. Its stages are typed as notice period, full-and-final settlement, exit interview, work handover, other, or archived.
- Rule: moving leavers into a stage of the type "archived" puts the employee in the **archive** and switches off their login; moving them out restores both, and the two changes happen together or not at all. Reason (from a code comment): bulk updates used to leave leavers able to sign in, and the mobile app issues sign-in tokens that last 30 days.

### Leavers and exit tasks

- Each leaver has a notice period start and end date. Exit tasks per stage are to do, in progress, stuck or completed, and leavers can have notes and files.
- Tasks marked as required stop a leaver being moved to the next stage. *Not yet verified in the code.*

### Resignation letters

- An employee submits a resignation letter with a planned leaving date. Status: requested, approved or rejected. The feature can be switched on or off.
- Rule: an employee can have only one open (requested or approved) resignation letter. Reason: not stated in the code.
- Rule: when a resignation is turned into an offboarding entry without an end date, the notice period end is the start date plus the default notice period. Reason: not stated in the code.

> Flag (half-built): approving a resignation letter has no automatic effect; the code for that case is empty, so adding the person to offboarding is a separate manual step (`offboarding/models.py`). The "full-and-final settlement" stage is only a label: there is no final pay calculation linked to payroll. Business effect: HR can approve a resignation and forget to start the exit process, and final settlements must be worked out outside the system.

### Exit reasons and settings

- HR keeps a list of exit reasons and a default notice period.
- The default notice period is stored in the payroll settings (30 days unless changed). Business effect: without the payroll area installed, the default notice period is empty.

## Who can do what

| Action | Who |
|---|---|
| Set up exit pipelines, stages and tasks; add leavers | People with the matching offboarding permissions (Admin, HR Manager), and offboarding managers |
| Work on a stage or exit task | The stage managers and task owners named on it |
| Submit a resignation letter | Every employee, for themselves, when the feature is switched on |
| Approve or reject resignation letters | People with the resignation letter change permission |

These come from the permission checks and the offboarding-manager checks on the offboarding screens (`offboarding/views.py`).

## Recommendations

- Suggestion: when a resignation letter is approved, offer to add the employee to an exit pipeline with the notice period filled in.
- Suggestion: build a full-and-final settlement calculation in payroll (last salary, leave encashment, loan recovery, asset fines).
- Suggestion: keep the default notice period in an offboarding setting so it does not depend on payroll.

## Related documents

- [Employees](02-employees.md): archiving and logins.
- [Payroll](07-payroll.md): where the default notice period lives.
- [Assets](13-assets.md): getting assets back from leavers.
- [Horilla HRM feature reference](../Horilla_HRM_FEATURES.md)

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
