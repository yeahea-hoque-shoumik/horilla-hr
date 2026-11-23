# Mobile app API

## Summary

The system offers an **API**, a way for other software to talk to it, which the company's mobile app uses. Through it, employees and managers can do most of their everyday self-service from a phone: check in and out with location and face checks, ask for and approve leave, see payslips, and work with most other areas. This file describes what the mobile app can do, not the technical list of addresses.

## Who uses it

- Employees and managers, through the mobile app.
- Other software the company connects, using the same sign-in rules.

## Features

### Signing in and the home screen

- The app signs in and receives tokens as described in [Security and access](21-security-and-access.md). The sign-in reply tells the app the user's role, their permissions and which features are installed, so the app shows only what the user may use.
- One request returns everything the app's home screen needs.
- Times are shown in the user's own **time zone** (added by this fork).

### What the app can do, by area

- Organisation and shifts: companies, departments, job positions, job roles, work from options, shifts and schedules, rotations, and shift and work-from requests with approval and cancellation.
- Employees: employee lists and profiles, work information, bank details, archiving, bulk updates, policies, disciplinary actions, and document requests with approval.
- Attendance: check-in and check-out (the same steps as the web, including the employee's time zone), attendance records, validation, overtime approval, hours balance, late arrival and early departure, today's attendance, who has not checked in, and attendance requests. The location check (**geofence**) and face check are used here; see [Attendance](05-attendance.md).
- Leave: balances, leave types, requests, approval, rejection, cancellation, bulk actions, requests for extra days, holidays and weekly days off.
- Payroll: payslips (list, detail, download and e-mail), loans, reimbursements, tax bands, allowances and deductions.
- Recruitment, onboarding, offboarding, performance, helpdesk, projects, assets and notifications: the main records of each area and their actions.

Source: the API's address list (`horilla_api/urls.py`, `horilla_api/api_urls/`). The full technical list is in the [API documentation](../../aidlc/spaces/default/codekb/horilla-hr/api-documentation.md).

### Technical documentation pages

- The API describes itself on documentation pages. They are open to everyone only when the system runs in debug mode; otherwise only administrators can open them.

### Rules shared with the web, and rules that are not

- Check-in and check-out through the app run the same steps as on the web.
- Rule: whether an app request enforces a business rule depends on the app's own code for that action, because the rules written into the screen forms are not always run (see the forms flag in [How the system works overall](00-how-the-system-works.md)). Reason: not stated in the code.

> Flag (inconsistent), described in [Leave](06-leave.md): some business rules are written again in the app's code instead of shared with the web, so they can differ. Leave approval is the known example: the app uses available days before carried-forward days, the web manager approval does the opposite.

## Who can do what

| Action | Who |
|---|---|
| Use the app | Every employee with an active account |
| Approve, change or delete records through the app | The same people as on the web, checked by the permission, manager and owner checks in the app's code |
| Open the technical documentation pages | Everyone in debug mode; administrators otherwise |

These come from the permission checks in the API code (`horilla_api/api_views/`, `horilla_api/api_decorators/`).

## Recommendations

- Suggestion: move business rules that the app and the web both need into one shared place, starting with leave approval.
- Suggestion: test every app action against the same rules as the matching web screen.

## Related documents

- [API documentation](../../aidlc/spaces/default/codekb/horilla-hr/api-documentation.md): the technical list of the API's addresses.
- [Security and access](21-security-and-access.md): tokens and request limits.
- [Attendance](05-attendance.md): location and face checks.

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
