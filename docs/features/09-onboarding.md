# Onboarding

## Summary

This area takes hired candidates from recruitment and guides them to their first day. HR sets up onboarding stages and tasks per job opening, tracks each new joiner's progress, and sends them a personal link to an onboarding portal where they enter their own details. HR then turns the new joiner into an employee.

## Who uses it

- HR and recruiters set up stages and tasks and move new joiners through them.
- The managers named on a stage or task work on what is assigned to them.
- New joiners fill in the onboarding portal.

## Features

### Onboarding stages and tasks

- Each job opening has its own onboarding stages and tasks. A task's status is to do, scheduled, ongoing, stuck or done.

### New joiners in onboarding

- Hired candidates appear in onboarding automatically. HR moves them between stages one at a time or in bulk, on a board.

### Onboarding portal

- HR sends the new joiner a personal link that only works for them. Through it, the new joiner enters personal information, a photo and bank details. HR then creates the login and the employee record ("welcome aboard"). *Not yet verified in the code.*

### Offer, joining and probation details

- HR records the offer letter status, the joining date and the **probation** end date, can reject a new joiner or undo that, and sends e-mails. A task report and a dashboard are available. *Not yet verified in the code.*

> Flag (gap): the probation end date is recorded but nothing acts on it. There is no confirmation step and no reminder, and the onboarding area has no **background job** at all (`onboarding/`). Business effect: probation reviews depend on HR remembering them, and employees can pass their probation end date without anyone being told.

## Who can do what

| Action | Who |
|---|---|
| Set up onboarding stages and tasks | People with the onboarding stage and task permissions (Admin, HR Manager, Recruiter) |
| Move new joiners and update tasks | People with those permissions, and the managers named on the stage or the job opening |
| Fill in the onboarding portal | The new joiner, through their personal link |

These come from the permission checks and the stage-manager and recruitment-manager checks on the onboarding screens (`onboarding/views.py`).

## Recommendations

- Suggestion: add a reminder to the employee's manager and HR before the probation end date, and a confirmation step that records the outcome.
- Suggestion: add tests for onboarding; it currently has a single test, which makes changes risky.

## Related documents

- [Recruitment](08-recruitment.md): where new joiners come from.
- [Employees](02-employees.md): the employee record created at the end of onboarding.
- [How the system works overall](00-how-the-system-works.md): the onboarding quiz is planned but not built.
- [Horilla HRM feature reference](../Horilla_HRM_FEATURES.md)

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
