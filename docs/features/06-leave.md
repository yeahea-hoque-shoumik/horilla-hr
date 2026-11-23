# Leave

## Summary

This area manages time off: the leave types a company offers, each employee's balance, leave requests and their approval, requests for extra days, compensatory leave and periods when leave is not allowed. Balances reset on a schedule and unused days can be carried forward. Approved leave also updates attendance and is used by payroll for paid and unpaid days.

## Who uses it

- Employees ask for leave, ask for extra days, and cancel leave.
- Reporting managers and the managers in an approval chain approve or reject requests.
- HR and leave managers set up leave types, assign balances, set restricted periods and create leave on an employee's behalf.

## Features

### Leave types

- A leave type is paid, unpaid or partly paid (paid at a percentage). It has a number of days, or is unlimited.
- It resets yearly, monthly, weekly or every set number of days, on a chosen month and day.
- Unused days can be carried forward: not at all, up to a maximum, or with an expiry date.
- Switches on a leave type: can be cashed in (encashment, see [Payroll](07-payroll.md)), needs approval, needs an attachment, leaves holidays out of the day count, leaves weekly days off out of the day count, and is compensatory leave.
- A leave type can have **eligibility** conditions: gender, once per employment, marital status, nationality, department, employment type, grade and length of service.

> Flag (half-built): **leave accrual** is defined but does nothing. A plan for earning leave over time, and the fields for "how many days per period", exist and are hidden on the form, but nothing adds leave over time (`leave/models.py`, `leave/forms.py`). There is no monthly accrual, only resets. Business effect: companies that give leave month by month (for example 1.5 days per month) cannot set this up and must assign the full amount at each reset.

### Leave balances

- Each employee has a balance per leave type: available days, carried-forward days, total, the date it was assigned, the next reset date and the expiry date of carried-forward days.
- A running-balance view shows how the balance changed over time, and a forecast shows what the next reset will give.

> Flag (gap): there is no permanent record of each balance change with its reason. The running-balance view is rebuilt from the general change history (`leave/models.py`). Business effect: it is hard to prove to an employee or an auditor exactly why a balance is what it is.

### Leave requests

- A request can be for full days, or start or end on a first half or a second half of a day.
- Status flow: requested, then approved or rejected; an approved request can then be "cancel requested" and then cancelled.
- Rule: the number of days is recalculated on every save from the dates and half days, then holidays and weekly days off are taken out when the leave type says so. Reason: not stated in the code.
- Rule: a request is refused when any of these is true. Reason: not stated in the code.
  - the leave type is not assigned to the employee;
  - the end date is before the start date, or a one-day request has different halves at start and end;
  - an attachment is required and missing;
  - it overlaps another request of the same employee that is not cancelled or rejected (two different halves of the same day are allowed);
  - dates in the past are not allowed for the employee's company (superusers are exempt);
  - no days are left after holidays and days off are taken out;
  - the balance is not enough, counting available days, carried-forward days (up to the type's maximum, or none when the type does not carry forward), and the days the next reset will give if that reset falls on or before the start date;
  - the dates fall in a restricted period for the employee's department or job position (superusers are exempt).
- Rule: when the leave type needs no approval, the request is approved as soon as it is created. This applies also when HR creates the leave on an employee's behalf; HR-created leave for a type that needs approval waits for approval like any other request (`leave/views.py`). Reason: not stated in the code.
- Rule: a request can be deleted only while it is still "requested". Reason: not stated in the code.
- Rule: approved leave, and leave whose cancellation is pending, updates the daily attendance status: full leave days become Absent ("Leave"), half days become Conflict ("Half day: needs validation"). Reason: not stated in the code.

> Flag (risk): when the attendance status update after a leave change fails, the error is only printed to the server's console and otherwise ignored (`leave/signals.py`). Business effect: the leave is saved but the daily attendance status can stay wrong, and nobody is told.

### Approval and balance deduction

- Rule: approving a request takes the days off the balance and records how many came from available days and how many from carried-forward days, so a later rejection or cancellation gives back exactly those days. Reason: not stated in the code.
- Rule: approved leave stays in force (balance taken, attendance marked) until its cancellation is approved; "cancel requested" counts as approved everywhere. Reason (from a code comment): the employee is still off until a manager agrees to the cancellation.
- People who are not **superusers** cannot approve their own leave.

> Flag (inconsistent): which days are used first depends on how the leave is approved. A manager approving on the web uses carried-forward days first; automatic approval and approval through the mobile app use available days first (`leave/views.py`, `horilla_api/api_views/leave/views.py`). Business effect: when carried-forward days expire, an employee can lose more or fewer days depending on which screen approved their leave.

### Multi-level approval

- A **multi-level approval** chain can be set per department and company, chosen by the number of days requested. The chain's managers are copied onto the request in order, and the next approver is told after each stage.
- Rule: if the person asking is one of the approvers, their own stage is approved automatically. Reason: not stated in the code.

> Flag (risk): the approval order is not enforced. The request becomes fully approved when the last approver in the chain approves, even if earlier approvers have not (`leave/views.py`). Business effect: a senior approver can approve before the line manager has looked, and the line manager's decision no longer matters.

> Flag (risk): when a department has several approval conditions, the first match wins, and conditions are sorted as text, so "10" comes before "3" (`leave/models.py`). Business effect: a request can go to the wrong approval chain, for example a 5-day request following the rule meant for 10 days or more.

### Requests for extra days (allocation requests)

- Employees can ask for extra days on a leave type; managers approve or reject.

### Compensatory leave

- When switched on, employees can ask for leave in return for days worked on holidays or weekly days off. The request is linked to those attendance records.

### Restricted leave periods

- HR can block leave in chosen periods, for chosen departments or job positions, and for all leave types, chosen types, or all types except chosen ones.

> Flag (gap): the restricted-period check does not filter by company (`leave/models.py`). Business effect: in an installation with several companies, the check also looks at restricted periods that belong to another company, so leave can be refused because of another company's rules.

### No leave in the past

- Each company can switch on a rule that stops employees asking for leave on past dates.

### Leave clash count

- When reviewing a request, managers see how many colleagues in the same department or job position are off at the same time.

### Resets and carry-forward

- Rule: a reset job runs every 4 hours. On or after the reset date, carried-forward days become the smaller of the current total and the type's maximum, available days become the type's full number of days, and a new reset date is set. On or after the expiry date, carried-forward days expire. Reason (from the code): the check uses "on or after" on purpose, so a missed run still resets.

> Flag (gap), described in [How the system works overall](00-how-the-system-works.md): leave resets use the server's clock, not the company or employee time zone.

### Penalties that cut leave

- Rule: an attendance penalty can cut leave in half-day steps, from available or carried-forward days, never below zero (`base/signals.py`). Reason: not stated in the code.

> Flag (bug): deleting a penalty gives back the full amount it was meant to cut, even when the cut had been stopped at zero (`base/signals.py`). Business effect: deleting a penalty can give an employee more leave than they had before the penalty.

## Who can do what

| Action | Who |
|---|---|
| Ask for leave, extra days or compensatory leave; cancel own leave | Every employee who has the leave type assigned |
| Approve or reject leave | People with the leave change permission, reporting managers, and anyone in any approval chain (see the manager access flag in [How the system works overall](00-how-the-system-works.md)); not their own leave unless they are a superuser |
| Create leave on an employee's behalf | People with the leave add permission, for the employees they may choose |
| Set up leave types, balances, restricted periods and approval conditions | People with the matching leave or approval-condition permissions (Admin, HR Manager, Leave Manager) |

These come from the permission checks on the leave screens (`leave/views.py`).

## Recommendations

- Suggestion: use one rule for which days are used first, on every screen and in the mobile app.
- Suggestion: enforce the approval order in multi-level chains.
- Suggestion: sort approval conditions as numbers.
- Suggestion: build monthly accrual, or remove the hidden accrual fields.
- Suggestion: keep a permanent balance ledger with a reason for each change (this is also in the Apurba plan, see [How the system works overall](00-how-the-system-works.md)).
- Suggestion: when a penalty is deleted, give back only what was actually cut.

## Related documents

- [Attendance](05-attendance.md): penalties, daily status and the monthly summary.
- [Payroll](07-payroll.md): leave encashment and unpaid days.
- [How the system works overall](00-how-the-system-works.md): approvals and planned features.
- [Horilla HRM feature reference](../Horilla_HRM_FEATURES.md)

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
