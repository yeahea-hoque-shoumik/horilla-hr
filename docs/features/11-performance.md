# Performance

## Summary

This area supports performance management: objectives with key results, 360-degree feedback, anonymous feedback, one-to-one meetings and rules that award bonus points. Objectives can be set for the company or per employee and tracked through progress and status. Feedback rounds can repeat automatically.

## Who uses it

- HR and performance managers set up periods, objectives, question templates and bonus point rules.
- Managers set and review their team's objectives, run feedback and hold one-to-one meetings.
- Employees update their own objectives, answer feedback and give anonymous feedback.

## Features

### Objectives and key results

- Work is planned in periods. **Objectives** can be company-wide or per employee, each with **key results**, a progress type and a status: Not Started, On Track, Behind, At Risk or Closed. Objectives have comments and a change history, and can be archived.

### 360-degree feedback

- Feedback is collected from question templates, from the employee's manager, colleagues, people who report to them and others.
- Feedback can repeat every set number of days, months or years.
- Rule: every day at 08:00, a repeating feedback round whose next start date is today is copied into a new round named "… - cyclic <date>", set back to Not Started, and the old round stops repeating (`pms/scheduler.py`). Reason: not stated in the code.

### Anonymous feedback

- Employees can give anonymous feedback about an employee, a department, a job position, or in general.

### One-to-one meetings

- Managers hold one-to-one meetings with question templates and record the answers.

### Bonus point rules

- HR sets rules that award bonus points when an objective or key result reaches a condition, for example when it is completed or closed, judged by completion date, end date, owner, members or managers. Points go to the employee's bonus account (see [Employees](02-employees.md)) and can be cashed in through [Payroll](07-payroll.md).

> Flag (risk): bonus point rules work by attaching listeners to changes while the system runs, and re-attaching them whenever the rules change (`pms/signals.py`). Business effect: whether points are awarded depends on how and when the server started, and it is hard to check afterwards why someone did or did not receive points.

## Who can do what

| Action | Who |
|---|---|
| Set up periods, question templates and bonus point rules | People with the matching performance permissions (Admin, HR Manager, Performance Manager; Project Manager can view, add and change) |
| Create and change employee objectives and key results | People with those permissions, reporting managers (the wide manager check described in [How the system works overall](00-how-the-system-works.md)), and the objective's owner for their own objectives |
| Run feedback and one-to-one meetings | People with the feedback and meeting permissions, reporting managers, and the managers named on a meeting |
| Give anonymous feedback | Every employee. *Not yet verified in the code.* |

These come from the permission, manager and owner checks on the performance screens (`pms/views.py`).

## Recommendations

- Suggestion: award bonus points through a fixed step in the system, with a record of which rule gave which points.
- Suggestion: show HR, for each employee, the history of awarded points and the rule behind each award.

## Related documents

- [Employees](02-employees.md): the bonus point account.
- [Reports](16-reports.md): the objective and key result health report.
- [Horilla HRM feature reference](../Horilla_HRM_FEATURES.md)

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
