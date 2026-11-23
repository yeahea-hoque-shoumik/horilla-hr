# Employees

## Summary

This area holds the employee record: personal details, work information, bank details, notes, company policies, disciplinary actions and bonus points. It also covers the employee's lifecycle in the system: creating, updating, archiving, handing over responsibilities and blocking logins. Almost every other area points to this record, so its rules affect the whole system.

## Who uses it

- HR and admin roles create and maintain employee records, policies and disciplinary actions.
- Reporting managers see their team's records.
- Employees see their own profile and, when allowed, edit it themselves.

## Features

### Employee profile

- Personal data: name, contact details, emergency contact, gender, marital status, number of children, qualification, photo and extra free-form information.
- Rule: an employee's e-mail address must be unique across the whole system. Reason: not stated in the code.

### Work information

- Company, department, job position, job role, shift, work type, employee type, **reporting manager**, tags, location, **time zone**, joining date, contract end date, basic salary and hourly salary.
- A "profile completion" percentage shows how many of 15 work fields are filled in.
- Experience is recalculated every 4 hours as the days since joining divided by 365. Reason: not stated in the code.

> Flag (risk): experience is calculated as a fraction but stored as a whole number, so it is rounded. Business effect: rules and reports that use experience (for example leave eligibility by length of service, or pay items based on experience) see a rounded figure. (`employee/models.py`)

> Flag (gap): an employee can have only one reporting manager, with no levels and no start or end dates. The comparison with Apurba HRM also lists no automatic move from probation to permanent and an optional emergency contact. *Not yet verified in the code.* (Comparison document, section 2.1)

### Bank details

- Each employee can have bank details, used for paying salaries.

### Notes and change history

- HR can keep notes about an employee, with attached files.
- Changes to chosen work-information fields are kept as a history. *Not yet verified in the code.*

### Company policies

- HR publishes policies with attachments, aimed at chosen employees, departments or job positions. The system works out which employees each policy reaches.

### Disciplinary actions

- An action can be a warning, a suspension (for a number of days or hours) or a dismissal.
- For action types where "block login" is switched on, a background job runs every 60 seconds and applies these rules. Reason: not stated in the code.
  - Suspension for days: the login is off from the start date until the start date plus the number of days, then on again.
  - Suspension for hours: on the start date only, the login is off from the start of the employee's shift until the shift start plus the number of hours.
  - Dismissal: the login is off for good from the start date.
  - Warning: no automatic effect.

> Flag (risk): the disciplinary job re-checks every past action every minute and switches the login back on once a suspension has ended. This overrides a later manual block of the same person. Business effect: if HR blocks someone's login by hand after a past suspension has ended, the system can quietly switch that login back on within a minute. (`employee/scheduler.py`)

### Bonus points

- Every new employee automatically gets a bonus point account starting at 0. Reason: not stated in the code.
- Points can be awarded by performance rules (see [Performance](11-performance.md)) and cashed in through payroll (see [Payroll](07-payroll.md)). The account keeps a history of changes.

### Employee lifecycle

- HR can create, update, archive and un-archive, delete and bulk-update employees, reset passwords, send invitation e-mails and block or unblock logins. *Not yet verified in the code.* Archiving and handing over were checked in the code and work as described below.
- **Archive**: the last active **superuser** cannot be archived. An employee who is still named somewhere, for example as someone's reporting manager or as a recruitment manager, cannot be archived until those responsibilities are handed to someone else with "replace". Reason: archiving would otherwise leave teams without an approver.
- Archiving an employee also switches off their login. Reason (from a code comment): logins read the user's active setting, and the mobile app issues sign-in tokens that last 30 days, so a leaver could otherwise keep access.
- **Replace**: hands every reference to one employee over to another.

### Self-service profile edit

- When the "profile edit" feature is granted, employees can edit their own profile. See the feature access rules in [Platform experience](20-platform-experience.md).

### Organisation chart, birthdays and dashboards

- An organisation chart, a birthdays list and employee dashboards are available. *Not yet verified in the code.*

## Who can do what

| Action | Who |
|---|---|
| Create, change, archive or delete employees | People with the employee add, change or delete permission (Admin, HR Manager; Recruiter can add and change) |
| See employee records | People with the employee view permission, and reporting managers for their team (the manager check is the wide one described in [How the system works overall](00-how-the-system-works.md)) |
| See own profile | Every employee |
| Edit own profile | Employees given the "profile edit" feature |
| Create disciplinary actions and policies | People with the disciplinary action or policy permissions |

These come from the permission checks on the employee screens (`employee/views.py`).

## Recommendations

- Suggestion: make the disciplinary job act only on the day a suspension starts and ends, and never undo a manual block.
- Suggestion: store experience with decimals, or in months, so length-of-service rules are exact.
- Suggestion: support more than one approver per employee, with start and end dates, as the Apurba plan describes.
- Suggestion: add a reminder or automatic step when a probation period ends (see [Onboarding](09-onboarding.md)).

## Related documents

- [How the system works overall](00-how-the-system-works.md): the employee record as the centre, archiving, time zones.
- [Offboarding](10-offboarding.md): archiving an employee when they leave.
- [Employee setup guide](../EMPLOYEE_SETUP_GUIDE.md)
- [Apurba HRM v2 compared with Horilla](<../ApurbApurba_HRM-v2_vs_Horilla_HRMS—Feature_Comparison.md>)

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
