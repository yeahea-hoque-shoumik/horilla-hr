# How the system works overall

## Summary

This file explains the ideas that every feature area depends on, so the area files can link here instead of repeating them. It also records which version of the code this report describes, what this fork changed after the original product, and which planned features are not built yet. Two flags that affect the whole system live here: time zones not reaching background jobs, and manager access that is wider than a manager's own team.

## Which code this report describes

- Code version: commit `f2ab49933cfb40d295b3a9e65eba21996df2b0dc`, scanned on 2026-11-19.
- Product: a **fork** of Horilla HRMS 2.2.0, an open-source HR system, owned by ApurbaTech. ApurbaTech also runs its own product, Apurba HRM v2, and plans to move it into this system.
- The production setup runs with the Asia/Dhaka **time zone** and in production mode.

## Who uses the system

| Person | What they do |
|---|---|
| Employee | Checks in and out; asks for leave, shift or work-type changes, attendance corrections, assets and reimbursements; raises helpdesk tickets; resigns; sees their own payslips, objectives and feedback |
| **Reporting manager** | Approves or rejects their team's requests, validates attendance, approves overtime |
| HR and admin roles | Set up the company, policies, leave types, shifts and payroll; run payroll; manage hiring, onboarding and exits |
| Candidate (outside the company) | Applies through a public form, follows their application, fills in the onboarding portal |
| Mobile app user | Does the same self-service through the mobile app, with location and face checks at check-in |

## Ideas that run through every area

### Several companies in one installation

- One installation can hold several companies. A user picks the **active company** at the top of the screen, and company data is filtered to it. Reason: one HR team can run several legal entities without mixing their people or permissions.
- Whether a type of record is filtered by company is decided record type by record type. A system check is said to warn about record types that are not filtered. *Not yet verified in the code.*
- Permission groups can apply per company, so a person can be an HR manager in one company and an ordinary employee in another. This is on by default (`COMPANY_SCOPED_PERMISSIONS`).

### The employee record is the centre

- Each login belongs to one **employee record**, and each employee record has one set of **work information**: company, department, job position, role, shift, work type, reporting manager, employee type, joining date, salary and time zone.
- Almost every other record in the system points to an employee. The reporting manager written on an employee's work information is what makes someone a "manager" for approvals.

### Approvals

- Most requests (leave, attendance, shift, work type, asset, reimbursement, resignation, extra leave days) go from requested to approved or rejected, decided by the reporting manager or by someone with the right **permission**.
- People who are not **superusers** cannot approve their own requests in leave, and cannot validate their own attendance or approve their own overtime (`leave/views.py`, `attendance/views/views.py`). Reason: not stated in the code.
- Only leave requests can go through a **multi-level approval** chain, where several managers approve in turn. The only condition that chooses a chain is the number of days requested.

> Flag (risk): manager access is wider than a manager's own team. The check that lets a person into a manager screen accepts anyone who holds the permission, or who is the reporting manager of anyone at all, or (for leave) who appears in any approval chain (`horilla/decorators.py`). Each screen must then check that the record belongs to that manager's team, and several do not. This was confirmed in the code for validating attendance and approving overtime: any person who manages at least one employee can validate the attendance or approve the overtime of employees outside their team. The fork's attendance notes list more screens with the same problem, including attendance lists, the monthly summary detail and comment files. *Not yet verified in the code.* Business effect: a manager can see or change attendance, overtime and possibly pay-related data of people they do not manage. (Source list: `attendance/MODULE_SUMMARY.md` section 5.)

### Notifications

- People are told about events through an in-app inbox, by e-mail through the company's own mail servers (every e-mail is logged), and optionally by WhatsApp.
- Many automatic messages are sent in the name of a user called "Horilla Bot". What happens when that user is missing is described in [Automations and notifications](17-automations-and-notifications.md).

### Background jobs

- The system runs 25 **background jobs**, such as shift rotations, leave resets, automatic check-out, daily attendance status, contract expiry, automatic payslips, closing job openings and report e-mails.
- They run only inside a separate **scheduler** process. If that process is not running, all of these stop and nothing catches up the missed days. The system's readiness check reports whether the scheduler is running (`/ready/` shows `scheduler: ok` or `missing`).

### Time zones

- Added by this fork: each company can have its own time zone, and each employee can have their own, which wins over the company's. When neither is set, the server's time zone is used.
- Pages and forms show times in the signed-in person's time zone. The mobile app does the same.
- Web and mobile check-in and check-out record the date and time in the employee's own time zone. Reason (from a code comment): the server's own clock followed the container's settings and could put a punch on the wrong day.

> Flag (gap): background jobs still use the server's clock, not the company or employee time zone. This covers automatic check-out, the daily attendance status, leave resets, automatic payslips, contract expiry, disciplinary login blocks and shift rotations, and also the attendance rule "check-out cannot be in the future". Business effect: for a company or employee whose time zone differs from the server's, these jobs can act on the wrong day, so a leave reset, an automatic check-out or a payslip can happen a day early or late. (`attendance/scheduler.py`, `leave/scheduler.py`, `payroll/scheduler.py`, `employee/scheduler.py`, `attendance/models.py`)

### Records are archived, not deleted

- Most records can be moved to the **archive**: hidden from normal use but kept. This keeps history for reporting and audits.
- Changes to configured record types are kept as **audit history**. *Not yet verified in the code.*
- Every save checks text fields for **cross-site scripting** (harmful code typed into a text box).

> Flag (risk): most business checks run only when data comes in through a screen's form. Saving data in other ways, such as some imports and some mobile app paths, skips those checks. Business effect: data that a screen would refuse (for example dates in the wrong order) can still get in through an import or the mobile app. (`horilla/models.py`)

### Roles

Every time the database is set up or updated, the system creates ten default **role groups**: Admin, HR Manager, Payroll Manager, Attendance Manager, Leave Manager, Recruiter, Asset Manager, Helpdesk Agent, Project Manager and Performance Manager (`base/signals.py`). Each group grants permissions over a set of areas. For example, Payroll Manager can fully manage payroll, change employee records and only view attendance and leave. Each area file's "Who can do what" section summarises who can do each main action.

## What this fork changed after Horilla 2.2.0

| Date | Change |
|---|---|
| 2026-11-10 | Documentation added (`docs/`, attendance module notes), a deploy script and production setup changes |
| 2026-11-16 | Database documentation and a tool that draws how the tables depend on each other |
| 2026-11-16 | The web server gatekeeper was removed from production; see [Security and access](21-security-and-access.md) |
| 2026-11-16 | The deploy script rebuilds the application image on every deploy |
| 2026-11-18 | A detailed access log of requests and responses; see [Security and access](21-security-and-access.md) |
| 2026-11-18 | Company and employee time zones, and check-in and check-out in the employee's time zone |
| 2026-11-18 | A fix for a loop when editing one's own profile |
| 2026-11-19 | Configuration for the AI-DLC way of working (not product code) |

## Planned but not built

These items appear in the plan to move Apurba HRM into this system. They do not exist in the code today and must not be read as features:

- a leave balance ledger that records every change as a typed event;
- a monthly quota for attendance corrections, with a cut-off date;
- shift jobs run separately per region;
- approver assignment with start and end dates;
- a work-from-home module;
- a quiz that a new joiner must pass during onboarding.

Source: [Plan to move Apurba HRM into Horilla](../APURBA_TO_HORILLA_INTEGRATION_PLAN.md), sections 3 and 4.

## Related documents

- [Index of this report](README.md)
- [Glossary](glossary.md)
- [Horilla HRM feature reference](../Horilla_HRM_FEATURES.md)
- [Database areas](../horilla_db_domains.md)

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
