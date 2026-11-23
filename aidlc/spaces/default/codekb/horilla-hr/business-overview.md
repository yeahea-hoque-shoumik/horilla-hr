# Business Overview: horilla-hr

Commit f2ab49933cfb40d295b3a9e65eba21996df2b0dc, scanned 2026-11-19.

## 1. What this system is

horilla-hr is a fork of **Horilla HRMS 2.2.0** (`horilla/__version__.py:8`), an open-source (LGPL-2.1) human resources management system. It is a single web application for HR teams, managers and employees, plus a REST API for a mobile app. It covers the whole employee lifecycle: hiring, onboarding, the employee record, time and attendance, leave, payroll, performance, offboarding, and supporting services (assets, helpdesk, projects, documents, reports).

The fork belongs to ApurbaTech, which also runs its own "Apurba HRM v2". The fork's `docs/` folder compares the two products and plans a migration from Apurba HRM into Horilla (`docs/APURBA_TO_HORILLA_INTEGRATION_PLAN.md`). The production `.env` runs with `TIME_ZONE=Asia/Dhaka` and `HORILLA_ENV=production`.

**Who uses it**

| Role | What they do in the system |
|---|---|
| Employee | Checks in and out, requests leave, shift/work-type changes, attendance corrections, assets, reimbursements; raises helpdesk tickets; submits resignation; sees own payslips, OKRs, feedback |
| Reporting manager | Approves or rejects the team's requests, validates attendance, approves overtime |
| HR / admin roles | Configure the company, policies, leave types, shifts, payroll; run payroll; manage recruitment, onboarding, offboarding |
| Candidate (external) | Applies through a public form, tracks the application, fills the onboarding portal |
| Mobile app user | Same self-service through `/api/`, with geofence and face check on check-in |

Default role groups created on every migrate: Admin, HR Manager, Payroll Manager, Attendance Manager, Leave Manager, Recruiter, Asset Manager, Helpdesk Agent, Project Manager (`base/signals.py:467-500`, per `docs/Horilla_HRM_FEATURES.md` §3.19).

## 2. How to read this document

- Each domain lists its **features**, the **business rules** behind them (what the system enforces, and why where the code says so), and **flags**.
- Source paths are given so a writer can check a claim. "Verified" means the rule was read in code during this scan. "Per doc" means the rule comes from the in-repo references `docs/Horilla_HRM_FEATURES.md` or `attendance/MODULE_SUMMARY.md` and was not re-read.
- Flag types:
  - **BUG**: the code does something different from what it plainly intends.
  - **GAP**: something a product owner would expect is missing.
  - **HALF-BUILT**: started, partly wired, or defined but unused.
  - **DISABLED**: shipped but switched off or not installed.
  - **INCONSISTENT**: the same rule behaves differently depending on the screen or channel.
  - **RISK**: works, but can produce a wrong or surprising result in realistic conditions.

## 3. Concepts that run through every domain

### 3.1 Companies (multi-company in one install)
- One installation can hold several companies. A user picks the active company in the navbar; company-scoped data is filtered to it (`base/middleware.py:210-422`, `CompanyMiddleware`).
- Scoping is opt-in per model through `HorillaCompanyManager`; a system check warns about unscoped models (per doc §7.3).
- Group permissions apply per company when `COMPANY_SCOPED_PERMISSIONS=True` (default) through `CompanyGroupAssignment` (`horilla/settings/base.py:505`, `base/models.py:200-252`).
- Why: one HR team can run several legal entities without mixing their people or permissions.

### 3.2 The employee record is the hub
- `HorillaUser` (login) 1–1 `Employee` (person) 1–1 `EmployeeWorkInformation` (company, department, job position, role, shift, work type, reporting manager, employee type, joining date, salary, timezone) (`employee/models.py:69-160, 924-1060`).
- Almost every other record points to an `Employee`. The reporting manager on work information is what makes someone a "manager" for approvals.

### 3.3 Approvals
- Most requests (leave, attendance, shift, work type, asset, reimbursement, resignation, allocation) follow **requested → approved / rejected** by the reporting manager or a permission holder.
- Self-approval is blocked for non-superusers in attendance and leave (verified for leave, `leave/views.py:1074-1081`; per doc for attendance).
- Only **leave requests** support multi-level, condition-based approval chains (`base/models.py:2211-2475`): the only condition field offered is "Leave Requested Days" (`FIELD_CHOICE`, `base/models.py:2211-2214`).
- Who counts as a manager: `manager_can_enter` lets in a user who has the permission, **or who is the reporting manager of anyone**, or (for leave) who appears in any approval chain (`horilla/decorators.py:157-190`). The view must then check the specific record. **RISK**: `attendance/MODULE_SUMMARY.md` §5 lists views where this record check is missing, so a manager could act on employees outside their team.

### 3.4 Notifications
- In-app inbox (vendored `django-notifications`), e-mail through company-configured SMTP servers with an e-mail log, and optionally WhatsApp. Many automatic messages are sent as a "Horilla Bot" user; if no user named "Horilla Bot" exists, those notices are silently skipped (`base/scheduler.py:44-53`).

### 3.5 Background jobs
- 25 jobs, run only by the separate `manage.py run_scheduler` process (`horilla/scheduling.py`, `base/management/commands/run_scheduler.py:79`). If that process is not running, rotations, leave resets, auto punch-out, work records, contract expiry, auto payslips, recruitment closing and report e-mails all stop. `/ready/` reports `scheduler: ok|missing` (`horilla/urls.py:58-118`).
- **RISK (fork)**: jobs use the server clock (`date.today()`, `datetime.now()`), not the new per-company or per-employee timezone (see 3.6).

### 3.6 Time zones (fork addition, commits c5ba10744 and 0ad9717b7)
- A company can have its own IANA time zone (`Company.timezone`, `base/models.py:121-153`); an employee can override it on work information (`EmployeeWorkInformation.timezone`, `employee/models.py:991-1003, 1047-1056`). Effective zone = employee's own, else company's, else the server `TIME_ZONE`.
- Pages and forms show times in the signed-in user's zone (`UserTimezoneMiddleware`, `base/middleware.py:539-562`); the API does the same at token check (`horilla_api/authentication.py`).
- Web and API check-in/out date and time are taken in the employee's zone (`attendance/methods/utils.py: employee_localtime`, `attendance/views/clock_in_out.py:272-290, 539-566`). Why (from the code comment): `date.today()` followed the container's OS zone and could put a punch on the wrong day.
- **GAP**: scheduled jobs (auto punch-out, daily work records, leave reset, payslip generation, disciplinary blocking, rotations) and `Attendance.clean()` ("check-out cannot be in the future", `attendance/models.py:1061-1099`) still use server time.

### 3.7 Records are archived, not deleted
- Most domain models carry `is_active`; "archive" hides a record without deleting it (`horilla/models.py`, `HorillaModel`). History is kept with django-simple-history and django-auditlog for configured models (per doc §7.4).
- Every save of a `HorillaModel` runs an XSS check on text fields (`horilla/models.py:147-200`). **RISK**: model `clean()` rules (most business validations) run only through forms, not on every save; direct saves, imports using `bulk_create`, and some API paths skip them.

## 4. Feature domains

### 4.1 Organisation and company setup — app `base`

**Features**
- Companies (name, address, logo, HQ flag, date/time format, time zone) (`base/models.py:103-197`).
- Departments, job positions, job roles, employee types, work types, tags (`base/models.py:255-498, 777-837, 2031-2086`).
- First-run setup wizard protected by `DB_INIT_PASSWORD` (`base/views.py` `initialize_database*`, per doc §3.1).
- System preferences: records per page per user, badge-ID prefix (`EmployeeGeneralSetting.badge_id_prefix`, default "PEP", `employee/models.py:1567-1575`), currency symbol and position (`payroll/models/tax_models.py:21-45`), date/time formats (`horilla/settings/base.py:562-581`), languages per company, announcement expiry.
- Default export permission per company: everyone may export, or export needs the per-model `export_<model>` permission (`base/models.py:3294-3343`, created by signal `base/signals.py:41-58`).
- Mail servers (`DynamicEmailConfiguration`, several per company, one primary) and mail templates (`HorillaMailTemplate`) (`base/models.py:2088-2209`); every outbound mail logged in `EmailLog` (`base/models.py:2676-2727`).
- Setup checklist banner (`SetupChecklistDismissal`, `base/models.py:3264-3292`).

**Business rules**
- A company name + address pair must be unique (`base/models.py:162`).
- A company or employee time zone must be a real IANA name (`base/models.py:134-145`).
- Creating a company automatically creates its announcement-expiry and export-permission settings and its attendance settings row (`base/signals.py:29-58`, `attendance/signals.py`).

**Flags**
- **RISK**: the production gate refuses to start with a default `SECRET_KEY`, `*` hosts or the default `DB_INIT_PASSWORD` (`horilla/settings/security.py`). The shipped `DB_INIT_PASSWORD` default is a known value, so a non-production install that is reachable is open to the setup wizard.

### 4.2 Employees — app `employee`

**Features**
- Employee profile: personal data, contact, emergency contact, gender, marital status, children, qualification, photo, additional JSON info (`employee/models.py:69-150`).
- Work information: company, department, position, role, shift, work type, employee type, reporting manager, tags, location, time zone, joining date, contract end date, basic salary, hourly salary (`employee/models.py:924-1060`); a "profile completion" percentage over 15 work fields (`employee/models.py:1064-1090`).
- Bank details (`EmployeeBankDetails`, `employee/models.py:1139`).
- Notes with files; work-information change history for configured fields (per doc §3.4).
- Company policies with attachments, targeted to employees, departments or job positions (`employee/models.py:1230-1320`; targets expanded to employees by signal `base/signals.py:523-559`).
- Disciplinary actions: warning, suspension (days or hours), dismissal (`employee/models.py:1383-1565`).
- Bonus points per employee, with history; redeemable for payroll encashment (`employee/models.py:1322-1381`).
- Lifecycle: create, update, archive/un-archive, replace (hand references to another employee), delete, bulk actions, password reset, invitation e-mails, login block/unblock (`AccountBlockUnblock` in `horilla_audit`) (per doc §3.4; archive and replace verified `employee/views.py:2569-2700`).
- Self-service profile edit when the "Profile Edit" feature is granted (`ProfileEditFeature`, `employee/models.py:1577-1583`; `accessibility`).
- Org chart, birthdays, dashboards (per doc).

**Business rules**
- Employee e-mail is unique across the system (`employee/models.py:102`).
- Every new employee gets a bonus-point account at 0 (signal inside `BonusPoint`, `employee/models.py:1361-1378`).
- Archiving: the last active superuser cannot be archived; an employee who is still referenced (for example as someone's reporting manager or a recruitment manager) cannot be archived until those references are handed over with "replace" (`employee/views.py:2580-2622`). Why: archiving would otherwise leave teams without an approver.
- Archiving an employee also disables their login (`Employee.sync_login_access`, `employee/models.py:431`). Why (code comment in `offboarding/views.py:531-541`): logins read the user's active flag, and the API issues 30-day refresh tokens.
- Experience is recalculated every 4 h as days since joining ÷ 365 (`employee/models.py:1113-1135`, `employee/scheduler.py:6-17`).
- Disciplinary login block runs every 60 s (`employee/scheduler.py:20-101`), only for action types with "block" enabled:
  - suspension by days: login off from the start date until start + N days, then back on;
  - suspension by hours: on the start date only, login off from today's shift start until shift start + hours;
  - dismissal: login off permanently from the start date;
  - warning: no automatic effect.

**Flags**
- **RISK**: the disciplinary job re-runs for every past action every minute and sets the login back to active after a suspension ends, which overrides any later manual block of the same person (`employee/scheduler.py:51-56, 87-88`).
- **RISK**: experience is stored in an integer field from a fractional calculation (`employee/models.py:1134`), so it rounds.
- **GAP** (from the Apurba comparison, `docs/ApurbApurba_HRM-v2_vs_Horilla_HRMS—Feature_Comparison.md` §2.1): only one reporting manager per employee (no levels or effective dates); no probation-to-permanent automation; emergency contact is optional.

### 4.3 Shifts, work types, rotations, rosters and change requests — app `base`

**Features**
- Shifts with a schedule per weekday: start, end, minimum working hours, night-shift flag, auto check-out time, grace time (`base/models.py:839-1076`).
- Rotating shifts and rotating work types: two or more shifts/work types assigned to an employee, switching **after N days**, **every week on a set day**, or **monthly on a set date or the last day** (`base/models.py:499-776, 1078-1383`; job `base/scheduler.py:96-224`).
- Shift requests and work-type requests (temporary with an end date, or permanent), with comments and files; managers approve, reject or cancel, singly or in bulk (`base/models.py:1493-2029`).
- Roster: one employee, one date, one shift (or "off"), published with a publish log; employees see "My Roster" (`base/models.py:1385-1487`).

**Business rules**
- Rotations and requests cannot start in the past ("Date must be greater than or equal to today"), and only one active rotation per employee (`base/models.py:697-708, 1367-1378`).
- A rotation cannot list the same shift or work type twice in a row (`base/models.py:572-604, 1148-1158`).
- On the requested start date an approved request switches the employee's shift/work type; after the end date it switches back to the previous one (jobs every 4 h, `base/scheduler.py:226-386`). Employees are notified.
- Starting a new rotation deactivates the employee's older rotations (`base/scheduler.py:215-224`).
- A published, non-off roster entry for today overwrites the employee's shift (`base/scheduler.py:415-445`).

**Flags**
- **BUG**: the monthly rotation crashes in December (it adds one to the month number) (`base/scheduler.py:97, 101-103, 203, 207-209`), so monthly rotations stop at year end.
- **RISK**: rotations and requests fire only when the 4-hourly job runs on the exact change date (`switch_date == today`); a day with the scheduler down is never caught up.
- **RISK**: a roster change is never reverted; after the rostered day the employee keeps the rostered shift until something else changes it. The job comment says "daily at 00:05" but it runs every 4 h (`base/scheduler.py:415-419, 464`).
- **GAP**: no shift swap between two employees (comparison doc §2.1).

### 4.4 Holidays, weekly offs, announcements — app `base`

**Features**
- Public holidays (single day or range), for everyone or specific employees/departments/positions, with a recurring flag; import/export (`base/models.py:2876-3036`).
- Company leaves (weekly offs) such as "every Sunday" or "second Saturday" (`base/models.py:3038-3131`).
- Announcements targeted to employees, departments or positions, with attachments, comments, "viewed by", expiry, optional WhatsApp delivery (`base/models.py:2519-2674`; `whatsapp/views.py:420-527`).

**Business rules**
- A recurring holiday is moved to the same dates next year the day after it ends (`base/scheduler.py:389-412`). Why: recurring holidays should not need re-entry each year.
- Holidays and weekly offs set the day's minimum hours to zero in attendance, so any hours worked count as overtime (`attendance/models.py:755-764`), and can be excluded from leave day counts (4.6).

**Flags**
- **RISK**: a recurring holiday whose roll-over would collide with an existing holiday is skipped with only a log warning (`base/scheduler.py:405-412`).

### 4.5 Attendance — apps `attendance`, `biometric`, `geofencing`, `facedetection`

Detailed module reference: `attendance/MODULE_SUMMARY.md` (fork-written, spot-checked in this scan).

**Features**
- Check-in / check-out from the navbar, the mobile API, biometric devices, Excel import, and automatic punch-out. Several in/out pairs per day ("activities"), breaks, a running at-work timer (`attendance/views/clock_in_out.py`).
- Restrictions per company: office IP allow-list, geofence radius (mobile and web), face image per employee, check-in on/off switch (`base/models.py:2803-2837`, `geofencing/models.py`, `facedetection/models.py`, `attendance/models.py:1740-1771`).
- Daily attendance record: shift, work type, first in, last out, worked hours, minimum hours, overtime, validated flag (`attendance/models.py:200-1099`).
- Validation by managers, with auto-validation inside configured hour bounds (`AttendanceValidationCondition`, `attendance/models.py:1500-1597`).
- Overtime: monthly "hours balance" per employee; overtime approval singly or in bulk; cut-off and auto-approve thresholds.
- Grace time per shift or a default, for check-in and optionally check-out (`attendance/models.py:1599-1738`).
- Late arrival / early departure tracking with penalties (fine or leave cut) (`attendance/models.py:1381-1498`, `base/models.py:3133-3238`).
- Attendance requests (create or correct), bulk requests over a date range, batches, comments and files.
- Daily Work Status grid (`WorkRecords`: Present, Half Day, Absent, Holiday/Week-off, Conflict, Draft) (`attendance/models.py:1773-1867`).
- Monthly Summary for payroll: per-day classification, conflict resolution, daily and range hour overrides, month-total overrides, regularisation import (`attendance/views/summary.py`, `attendance/models.py:1869-2094`).
- Biometric devices: ZKTeco/eSSL, Anviz, Matrix COSEC, Dahua, e-Time Office, each as in, out, alternate or system-direction device (`biometric/models.py:53-63`); live capture or polling every N seconds.
- Dashboards (on time, late, early out, on break, pending hours, overtime by department, absentees).

**Business rules (verified)**
- Overtime for a day = worked hours − minimum hours, never negative (`attendance/models.py:766-781`).
- On a holiday or weekly off the minimum is 0, so the whole day is overtime (`attendance/models.py:755-764`).
- Overtime is capped at the condition's cut-off, and auto-approved when the condition allows it and overtime ≥ the minimum to approve (`attendance/models.py:783-800`). The condition used is the shift's own, else the shift-less default (`attendance/models.py:1537-1548`).
- The monthly hours balance counts only **validated** attendances, excludes days covered by approved (or cancel-requested) leave, and caps each day's worked time at that day's minimum (`attendance/models.py:996-1059`). Why: the balance measures whether required hours were met; extra hours are tracked separately as overtime.
- Daily status after each save: not validated → Conflict ("Validate the attendance"); worked ≥ minimum → Present; worked ≥ half the minimum → Half Day; else Absent; no check-out yet → "Currently working" (`attendance/signals.py:19-90`).
- A check-in date cannot be before the attendance date, a check-out cannot be before the check-in or in the future (`attendance/models.py:1061-1099`).
- Night shifts: a punch before 12:00 on a shift that starts after it ends belongs to the previous day (per doc §3.3).
- Late = check-in minus grace after shift start; early = check-out plus grace before shift end; only when late/early tracking is switched on (per doc §3.3).
- A draft daily status row is created every 30 min (and at 00:30) for every employee who has a shift schedule and no row yet (`attendance/scheduler.py:64-117`).
- Auto punch-out every 5 min: for shifts with auto check-out enabled, open activities are closed at the configured time (next day for night shifts) (`attendance/scheduler.py:10-61`).
- Monthly Summary classification (per doc §3.7): worked ≥ minimum − default grace → 1 day, ≥ half → 0.5, else 0; a half-day leave plus attendance makes a full day; attendance on a holiday or week-off counts as holiday/week-off; otherwise leave, holiday, week-off, absent in that order. An HR decision on a day wins. Unresolved attendance-vs-leave conflicts block payroll; a month-total override settles them (`attendance/models.py:1954-2061` docstring).

**Flags**
- **BUG**: rejecting an attendance "create" request does not delete it; it stays as an unvalidated attendance (`attendance/views/requests.py:595-610`).
- **BUG**: a bulk attendance request with one invalid day crashes part-way (`attendance/forms.py:1405`, `logger(form.errors)`).
- **RISK**: Excel attendance import uses `bulk_create`, which skips overtime calculation, hours balance and daily status (per doc §5).
- **RISK**: the IP restriction and lockout need the real client IP; since the fork removed nginx and serves through a tunnel, `AXES_PROXY_COUNT` must be set correctly or all users appear to come from one IP (`horilla/settings/base.py:644-662`, `docker-compose.prod.yml`).
- **RISK**: face detection only stores a reference image per employee on the server; no face matching code is in this repository, so the comparison is done (or trusted) on the mobile client (`facedetection/models.py`, `facedetection/views.py`).
- **RISK**: biometric "schedule" starts an extra in-process poller on top of the central job, so a device can be polled twice (`biometric/views.py:431-504`, `biometric/cbv/biometric.py:288-335`).
- **GAP**: scheduled punch-out and daily status use server time (3.6).
- **GAP** (comparison doc §2.2-2.3): no work-hours-deficit to leave deduction, no claim quota per month, no WFH request type (work-type requests can model it).
- Authorization gaps listed in `attendance/MODULE_SUMMARY.md` §5 (several list and detail views scoped only by login).

### 4.6 Leave — app `leave`

**Features**
- Leave types (`leave/models.py:239-633`): paid, unpaid or custom (paid at a percentage); total days (or unlimited); reset yearly, monthly, weekly or every N days, on a chosen month/day; carry forward none / up to a maximum / with expiry; flags: encashable, requires approval, requires attachment, exclude holidays, exclude weekly offs, compensatory.
- Eligibility conditions on a leave type: gender, once per employment, marital status, nationality, department, employment type, grade, service duration (`leave/models.py:131-140, 190-236`; evaluated in `leave/services.py:11`).
- Assigned leave balances per employee (`AvailableLeave`: available days, carried-forward days, total, assigned date, next reset date, expiry date) with a running-balance "ledger" view built from history (`leave/models.py:635-1102`, `build_ledger` at 815) and a next-reset forecast (1013).
- Leave requests: full day, first half or second half at both start and end; statuses requested → approved / rejected; approved → cancel requested → cancelled (`leave/models.py:151-162, 1153-2116`).
- Multi-level approval chains by requested-days condition, per department and company (3.3).
- Leave allocation requests (ask for extra days) (`leave/models.py:2136-2328`).
- Compensatory leave requests for days worked on holidays/weekly offs, linked to attendance records (`leave/models.py:2440-2630`), switchable (`LeaveGeneralSetting.compensatory_leave`).
- Restricted leave periods by department and/or job position, for all types, specific types or all-but-excluded types (`leave/models.py:2352-2438`).
- "No leave in the past" switch per company (`EmployeePastLeaveRestrict`, `leave/models.py:2660`).
- Leave clash count: how many colleagues in the same department or job position are off at the same time (`leave/models.py:2069-2116`).

**Business rules (verified)**
- Requested days are recalculated on every save from dates and half-day breakdowns, then holidays and/or weekly offs are subtracted when the type excludes them (`leave/models.py:1717-1735, 1947-1980`).
- A request is refused when:
  - the leave type is not assigned to the employee;
  - the end date is before the start date, or a single-day request has different start/end halves;
  - an attachment is required and missing;
  - it overlaps another non-cancelled, non-rejected request of the same employee (two different halves of the same day are allowed);
  - past dates are restricted for the employee's company (superusers exempt);
  - the effective days are zero after exclusions;
  - balance is insufficient: available + carried-forward (capped at the type's maximum, or 0 when the type has no carry-forward) + the next reset's days if the reset falls on or before the start date (forecast);
  - the dates fall in a restricted period for the employee's department or position (superusers exempt) (`leave/models.py:1783-1945`).
- When the leave type needs no approval, the request is approved immediately on creation (`leave/views.py:465-490`).
- Approval deducts the balance and records how many days came from available vs carried-forward, so rejection or cancellation can give exactly those days back (`leave/views.py:1117-1131, 1281-1300`).
- An approved leave stays in force (balance deducted, attendance marked) until its cancellation is approved; "cancel requested" counts as approved everywhere (`leave/models.py:159-162`). Why (code comment): the employee is still off until a manager agrees.
- A request can be deleted only while it is "requested" (`leave/models.py:2054-2067`).
- Multi-level chain: the matching condition's managers are copied to the request in order; if the requester is one of the approvers, their stage is approved automatically (`leave/models.py:1736-1781`, `leave/signals.py:138-148`). The next approver is notified after each stage.
- Approved or cancel-requested leave writes the daily status: full leave days become Absent ("Leave"), half days become Conflict ("Half day: needs validation") (`leave/signals.py:15-83`).
- Reset job every 4 h: on or after the reset date, carry-forward = min(current total, the type's maximum), available days = the type's total days, and a new reset date is set; on or after the expiry date the carry-forward expires. The `<=` comparison is deliberate so a missed run still resets (`leave/scheduler.py:8-60`, `leave/models.py:728-803`).
- Penalties (from attendance) can cut leave in half-day units from available or carried-forward days, never below 0 (`base/signals.py:100-118`).

**Flags**
- **INCONSISTENT**: which days are used first differs by path. Web manager approval uses carried-forward days first (`leave/views.py:1117-1131`); auto-approval and the mobile API use available days first (`leave/views.py:473-490`, `horilla_api/api_views/leave/views.py:738-752`). With expiring carry-forward this changes how many days an employee loses.
- **RISK**: multi-level order is not enforced. The request is fully approved when the **last** approver in the chain approves, even if earlier stages have not (`leave/views.py:1150-1196`, final save at 1181).
- **RISK**: when several conditions exist for a department, the first match wins and conditions are sorted by their value **as text** ("10" before "3") (`leave/models.py:1751`).
- **BUG**: deleting a penalty adds back the full deducted amount even when the deduction had been clamped at 0, inflating the balance (`base/signals.py:172-186`).
- **RISK**: the work-record update in the leave signal swallows errors with `print(e)` (`leave/signals.py:79-80`).
- **HALF-BUILT**: `ACCRUAL_PLAN` and the leave-type fields `count` / `period_in` exist but nothing accrues leave (`leave/models.py:148, 247-248`; hidden in `leave/forms.py:179, 225`). There is no monthly accrual, only resets.
- **GAP**: no append-only balance ledger with event types (the `build_ledger` view is reconstructed from history rows); no leave-on-behalf auto-approve by HR described; restricted periods are not filtered by company in the check (`leave/models.py:1909-1944`).

### 4.7 Payroll — app `payroll`

The largest module (about 48k lines, 850 tests). Internals were skimmed; rules below are verified unless marked.

**Features**
- Contracts: wage type (daily, monthly; hourly when attendance is installed), pay frequency (weekly, monthly, semi-monthly), status draft → active → expired / terminated, filing status for tax, notice period, documents (`payroll/models/models.py:364-1150`).
- Salary structures in Gross-Up or CTC-Down mode with a coherence checker (per doc §3.8, `payroll/methods/structure_rules.py`).
- Allowances and deductions: fixed, percentage of a component, safe formula, conditions, caps with proration, specific or excluded employees, one-time dates, pre/post tax, employer contributions (`payroll/models/models.py:1550-2870`; per doc).
- Component library (India, US, UK, GCC examples) and system components for loans, advances, fines, penalties, reimbursements, encashments, loss of pay (`payroll/component_library.py`, `payroll/system_components.py`).
- Income tax: filing statuses with tax brackets, standard deduction, rebate, cess, optional sandboxed Python formula; tax packs India New and Old Regime FY 2025-26, US Federal Single and Married Filing Jointly 2025, UK PAYE 2025-26, Flat 10% (`payroll/tax_packs.py:41-157`, `payroll/models/tax_models.py`).
- Payslips: single or bulk, status draft → review ongoing → confirmed → paid, PDF, e-mail, per-line "how was this worked out", manual overrides (`payroll/models/models.py:3415-3640`).
- Payroll runs (`PayrollBatch`): scope → review (blocking and non-blocking problems) → generate in slices; status Draft → In review → Approved → Paid, or Cancelled (`payroll/models/payroll_batch.py:138-372`).
- Pay period settings (e.g. 26th to 25th) (`payroll/models/payroll_batch.py:39`).
- Auto payslip generation per company on a set day or the last day (`payroll/models/models.py:4270`, `payroll/scheduler.py:84-138`).
- Loans, salary advances, fines (`LoanAccount`, `payroll/models/models.py:3642-3818`).
- Reimbursements, leave encashment, bonus-point encashment requests with approval (`payroll/models/models.py:3829-4148`).
- Contributions/remittance, employer cost, cost composition, payroll dashboard (per doc).

**Business rules (verified)**
- A run's status can move only along the allowed transitions; **Paid and Cancelled are final**. Why (code comment): "a system that lets a paid run be moved back to draft cannot be relied on to say what was paid" (`payroll/models/payroll_batch.py:140-172, 241-260`).
- Active contracts past their end date become expired every 4 h (`payroll/scheduler.py:22-30`).
- Auto payslips: on the configured day (a day beyond the month's length means the last day), draft payslips are created for the previous month for every employee with an active contract, starting at the later of the period start and the contract start; employees whose tax setup is broken are skipped and logged rather than paid with zero tax (`payroll/scheduler.py:33-138`).
- A loan or advance creates a one-time payout allowance on the provided date and an installment deduction schedule; a fine creates no payout (`payroll/signals.py:75-140`). Why (code comment): the loan's tax and proration follow the standard component, otherwise a mid-month joiner got a fraction of the loan.
- An attendance penalty with an amount becomes a fixed one-time deduction for that employee on the attendance date (`base/signals.py:61-99`).
- Payroll reads the attendance Monthly Summary for paid/unpaid days and overtime; unresolved conflicts block the run (`attendance/MODULE_SUMMARY.md` §6).

**Flags**
- **BUG**: auto payslip recomputes mid-period joiners every 3 h on the generate day and resets their payslip to draft, because it looks the payslip up by the period start but saves it with the contract start (`payroll/scheduler.py:62-79`).
- **GAP**: no Bangladesh tax pack (packs are India, US, UK, flat 10%) for a company running in Asia/Dhaka (`payroll/tax_packs.py`).
- **RISK**: the auto payslip and contract expiry jobs use server dates, not company time zones.
- Encashment, tax and component calculations were not re-verified in this scan (see `payroll/methods/`).

### 4.8 Recruitment — app `recruitment`

**Features**
- Recruitments (job openings): positions, vacancies, dates, managers, skills, survey template, published/closed (`recruitment/models.py:159-441`).
- Pipeline stages typed initial, applied, test, interview, rejected (cancelled), hired, with per-stage managers; kanban drag and drop (`recruitment/models.py:443-622`).
- Candidates: profile, resume, source (application form, inside software, other), referral source (job board, career site, social media, employee referral, recruiter, search engine, college, event, other), offer letter status not sent → sent → accepted / rejected → joined, notes, ratings, reject reasons, history, conversion to employee (`recruitment/models.py:624-1500`).
- Interviews with interviewers and optional Google Meet links (`recruitment/models.py:1822`, `horilla_meet`).
- Surveys / application form: 10 question types (yes/no, choices, multiple choice, text, number, percentage, date, textarea, file, rating) (`recruitment/models.py:1542-1681`); public application form per recruitment.
- Candidate self-tracking portal (feature switch) (`recruitment/auth.py`, per doc).
- Resume screening: bulk upload, NLP extraction of name, e-mail, phone, DOB (spaCy), skill matching and ranking (per doc; `recruitment/views/`).
- Talent pool ("Skill Zone") (`recruitment/models.py:1683-1789`).
- Candidate document requests (`recruitment/models.py:1973-2071`, signal `recruitment/signals.py:64-90`).
- LinkedIn: post and delete job openings (`recruitment/models.py:2073`).

**Business rules (verified)**
- Creating a recruitment creates its initial pipeline stage (`recruitment/signals.py:13-40`).
- Every 5 min, active candidates whose e-mail already belongs to a user are marked "converted" (`recruitment/scheduler.py:31-48`).
- Every hour, recruitments whose end date is today are closed and unpublished (`recruitment/scheduler.py:12-28`).

**Flags**
- **BUG**: `recruitment_close` captures "today" once when the scheduler process starts and needs an exact date match, so in a long-running scheduler recruitments past their end date stay open (`recruitment/scheduler.py:9, 21-28`).
- **RISK**: spaCy and its model are loaded at module import in recruitment views, which ties Python version and image size to resume screening (per `requirements.txt` notes).

### 4.9 Onboarding — app `onboarding`

**Features**
- Onboarding stages and tasks per recruitment; task status todo / scheduled / ongoing / stuck / done (`onboarding/models.py:26-271`).
- Hired candidates appear in onboarding; stage moves, bulk updates, kanban.
- Onboarding portal: a tokenised link where the candidate enters personal info, photo and bank details; HR then creates the user and employee ("welcome aboard") (`onboarding/models.py:273`, per doc §3.10).
- Offer letter status, joining date, probation end date, reject/undo, e-mails, task report, dashboard (per doc).

**Flags**
- **GAP**: probation end date is recorded but nothing acts on it (no confirmation or reminder job) (comparison doc §2.1; no onboarding scheduler exists).

### 4.10 Offboarding — app `offboarding`

**Features**
- Offboarding pipelines (ongoing/completed) with stages typed notice period, FnF settlement, interview, work handover, other, archived (`offboarding/models.py:31-143`).
- Employees placed in a pipeline with notice period start/end; exit tasks per stage (todo, in progress, stuck, completed); notes and files (`offboarding/models.py:153-375, 586-695`).
- Resignation letters: requested / approved / rejected, with planned leaving date; switchable (`offboarding/models.py:377-584`).
- Exit reasons; default notice period setting (`offboarding/models.py:652-704`).

**Business rules (verified)**
- Moving employees into an **archived** stage archives the employee and disables their login; moving them out restores both; done atomically (`offboarding/views.py:522-560, 600-620`). Why (code comment): bulk updates used to leave leavers able to log in, and the API issues 30-day tokens.
- Tasks marked required block a stage move (`offboarding/views.py` "blocked_message", per doc).
- Only one open (requested or approved) resignation letter per employee (`offboarding/models.py:505-516`).
- When a resignation is turned into an offboarding entry without an end date, the notice end = start + the payroll default notice period (`offboarding/models.py:525-584`).

**Flags**
- **HALF-BUILT**: approving a resignation letter has no automatic effect in the model (`offboarding/models.py:519-523`, empty `if self.status == "approved": pass`); adding to offboarding is a separate step.
- **GAP**: "FnF settlement" is only a stage label; there is no full-and-final pay calculation linked to payroll.
- Dependency: the default notice period lives in payroll settings (`PayrollGeneralSetting`), so without payroll it is blank.

### 4.11 Performance management — app `pms`

**Features**
- Periods; objectives (company and per employee) with key results; progress types; statuses Not Started / On Track / Behind / At Risk / Closed; comments and history; archive (`pms/models.py:28-911`).
- 360° feedback from question templates, with manager, colleague, subordinate and other reviewers; cyclic feedback every N days/months/years (`pms/models.py:913-1255, 1384-1431`).
- Anonymous feedback about an employee, department, job position or general (`pms/models.py:1257-1382`).
- 1:1 meetings with question templates and answers (`pms/models.py:1433-1647`).
- Bonus point rules: award points when an objective or key result reaches a condition (completing / closing, by completion date, end date, owner, members, managers) (`pms/models.py:1649-1903`, dynamic signals `pms/signals.py`).

**Business rules (verified)**
- Daily at 08:00, a cyclic feedback whose next start date is today is copied into a new round named "… - cyclic <date>", reset to Not Started, and the old one stops cycling (`pms/scheduler.py:9-47`).

**Flags**
- **RISK**: bonus-point rules work by connecting signal handlers at runtime and reconnecting them when rules change (`pms/signals.py:26-200`); behaviour depends on process start-up and is hard to audit.

### 4.12 Projects — app `project`

**Features**
- Projects with managers, members, dates, document; status new, in progress, completed, on hold, cancelled, expired (`project/models.py:52-265`).
- Stages per project (kanban), tasks (to do, in progress, completed, expired) with assignees and deadlines (`project/models.py:267-658`).
- Timesheets against project and task (status in progress, completed) (`project/models.py:660-799`).

**Business rules (verified)**
- A task's dates must sit within its project's dates (`project/models.py:390-401`).
- A project or task is marked expired only when it is edited and its end date has passed (`project/models.py:228-234, 401-402`).

**Flags**
- **GAP**: no job marks projects or tasks expired automatically; status depends on someone editing the record.
- Timesheets are not linked to payroll or attendance.

### 4.13 Assets — app `asset`

**Features**
- Categories, lots/batches, assets (In use / Available / Not-Available) with quantity and individual items (Available / In use / Damaged / Lost) (`asset/models.py:24-433`).
- Asset requests (Requested / Approved / Rejected) and allocation; return with condition (Healthy / Minor damage / Major damage / Lost), images, reports, documents (`asset/models.py:435-911`).
- Service requests on an allocation (Requested / In Progress / Completed / Rejected / Returned) with notes (`asset/models.py:948-1122`).
- Asset fine on return (form in payroll), import/export, history, dashboard (per doc).

**Business rules (verified)**
- An asset's status is derived from its items; saving an asset creates placeholder items up to its quantity and never removes items (`asset/models.py:306-330, 425-433`).
- Daily: assets past expiry become Not-Available; the owner (or a superuser) is notified on the "notify before" date (`asset/scheduler.py:12-71`).

**Flags**
- **BUG**: the document-expiry job (which lives in the asset scheduler but serves employee documents) marks expired documents inactive in memory only and never saves; its notification links to the asset page (`asset/scheduler.py:74-105`).
- **RISK**: that job runs every 4 h with an exact-day check, so the same expiry notice can be sent several times on the day.

### 4.14 Helpdesk — app `helpdesk`

**Features**
- Tickets: type (suggestion, complaint, service request, meeting request, anonymous complaint, others), priority low/medium/high, status new / in progress / on hold / resolved / canceled, raised against an employee, department or job position, assignees, deadline, tags, comments, attachments (`helpdesk/models.py:22-455`).
- Claim requests: an agent asks to take a ticket; a manager approves (`helpdesk/models.py:457-485`).
- Department managers receive tickets raised against their department or position (`helpdesk/models.py:49-95`).
- FAQ categories and FAQs, suggested while writing a ticket (`helpdesk/models.py:538-586`).

**Flags**
- **GAP**: no SLA, escalation or overdue-deadline job.

### 4.15 Employee documents — app `horilla_documents`

**Features**
- HR raises a document request (e.g. "upload passport", with format) for selected employees; employees upload; HR approves or rejects; expiry date with "notify before" days (`horilla_documents/models.py:46-222`).

**Flags**
- See the expiry job BUG in 4.13.

### 4.16 Reports — app `report`

**Features**
- 34 standard reports (slugs in `report/metrics/definitions.py`): absenteeism-rate, asset-register, attendance-summary, audit-activity, cost-composition, diversity-snapshot, document-expiry-aging, exit-analysis, headcount-bridge, joiners-leavers, labor-cost-summary, leave-liability, leave-utilization, loan-advance-ledger, new-hire-90-day-attrition, offer-acceptance, onboarding-progress, overtime-analysis, payroll-headcount-cost, payroll-readiness, payslip-register, performance-distribution, pipeline-aging, quality-of-hire, recruitment-funnel, reimbursement-register, source-quality, span-of-control, tenure-longevity, time-to-hire, turnover-attrition, unscheduled-absence, visa-contract-expiry, workforce-composition.
- Filters, period comparison, drill-down, KPIs, charts, narrative; Excel/CSV/PDF exports; favourites, saved views, presets; access matrix (view, export, subscribe) per report; scheduled e-mail subscriptions; pivot "Explorer" per module (`report/models.py`, `report/registry.py`; per doc §3.16).

**Business rules (verified)**
- Due subscriptions are checked and sent every hour (`report/scheduler.py:16-39`).
- Users without global permission see only their subordinates (per doc).

### 4.17 Automations, notifications and WhatsApp — apps `horilla_automations`, `notifications`, `whatsapp`

**Features**
- No-code mail automations: pick a model, a trigger (on create, on update, on delete), conditions, recipients through relations, a mail template, delivery by e-mail, in-app notification or both (`horilla_automations/models.py:11-165`).
- In-app notifications with inbox and sound.
- WhatsApp Business (Meta): templates and flows; employees can raise shift, work-type, leave, asset, attendance, bonus-point redemption and reimbursement requests through WhatsApp flows; notifications and announcements go out on WhatsApp; webhook signature check (`whatsapp/utils.py:524-862`, `whatsapp/views.py:116-527`).

**Business rules (verified)**
- WhatsApp requests reuse the same web forms and views through a simulated request, so web validation rules apply (`whatsapp/utils.py:524-590, 657-709`).

**Flags**
- **RISK**: WhatsApp attendance requests call an attendance view that is no longer routed (per `attendance/MODULE_SUMMARY.md` §4.2).

### 4.18 Integrations — apps `horilla_ldap`, `horilla_meet`, `horilla_backup`, `outlook_auth`, settings

| Integration | Status | Source |
|---|---|---|
| Google Meet links for interviews and meetings | Installed | `horilla_meet/` |
| Google Drive backup of DB and media | Installed; runs its own in-process scheduler (**RISK**: lost on restart, may run in several workers) | `horilla_backup/scheduler.py:21` |
| LinkedIn job posting | Installed | `recruitment/models.py:2073` |
| AWS S3 / GCS media storage | Optional by environment | `horilla/settings/addons.py`, `horilla/horilla_backends_gcp.py` |
| Sentry error tracking | Optional by `SENTRY_DSN` | `horilla/observability.py` |
| LDAP login and user sync | **DISABLED / HALF-BUILT**: backend commented out, LDAP libraries not in requirements | `horilla/settings/base.py:630`, `horilla_ldap/` |
| Microsoft 365 / Outlook mail | **DISABLED**: app not in `INSTALLED_APPS` | `outlook_auth/` |
| Runtime custom fields | **DISABLED**: not installed | `dynamic_fields/` |
| Local PostgreSQL dump scheduler | **DISABLED**: not installed | `pg_backup/` |

### 4.19 Data import — app `master_import`

**Features**
- Wizard: upload, map columns, check (row errors editable in place), run with progress, summary and error workbook, history (per doc §3.18).
- Datasets: employees, update existing employees, assets, asset allocations, assigned leave, salary structures (`master_import/datasets/`).

**Business rules (per doc)**
- When updating employees, a blank cell never overwrites a value, and an ambiguous match is an error. Names shared across companies are resolved by company.

**Flags**
- Its 132 tests are not in the CI smoke labels (`Makefile` `SMOKE_LABELS`).

### 4.20 Platform experience — apps `horilla_views`, `horilla_theme`, `horilla_tour`, `horilla_dbtemplate`, `accessibility`, `horilla_audit`, `horilla_crumbs`, `horilla_widgets`

**Features (per doc §6 unless noted)**
- Generic list, card, kanban, pipeline and detail screens with search, filters, saved filters, group-by, column choice and order remembered per user, bulk update/delete/archive, quick export (`horilla_views/models.py`).
- Role-based home dashboard (leadership, HR, manager, employee), employee self-service dashboard, per-user chart layout.
- Colour themes per company, dark mode, white-labelling switch (off by default, `horilla/settings/base.py:455`), 12 UI languages.
- Product tours (driver.js) with per-user progress (`horilla_tour/models.py`).
- Database-stored template overrides with drafts, versions, diff and preview (`horilla_dbtemplate/models.py`).
- Feature access rules ("accessibility"): default employee view, detailed view, profile edit, dashboard charts (gender, department, employees), birthdays (`accessibility/accessibility.py`, `employee/models.py:1586-1589`).
- Audit tags, audit model configuration, history tracking fields, account block/unblock (`horilla_audit/models.py`).

### 4.21 Security and access

- Login: username/password; lockout after 5 failures for 30 min per username + IP (django-axes); optional e-mail OTP two-factor (off by default); forced password change on first login; password reset by e-mail (`horilla/settings/base.py:644-662`, `base/middleware.py:425-505`).
- Sessions: 12 h idle timeout, renewed on every request (`horilla/settings/base.py:689-690`).
- API: 60-min access token, 30-day rotating refresh token, blacklist on logout and rotation, tokens revoked on password change; throttles anon 60/min, user 600/min, login 12/min, bulk 6/min (`horilla/settings/base.py:108-171`).
- Production gate (see 4.1); secure cookies in production; XSS check on every model save; SVG upload middleware; sandboxed payroll formulas.
- **RISK (fork)**: nginx was removed from production (commit fb8ff8eec). The nginx login rate limit (5/min), the `/metrics/` block and the 50 MB upload limit described in `docker/nginx.conf` no longer protect the app; `/metrics/` is still staff-only in code (`horilla/urls.py:121-136`).
- **RISK (fork)**: the new access log records clipped, scrubbed JSON request and response bodies; salary-like keys are scrubbed but `net_pay`, `gross_pay`, `wage`, names and e-mails are not (`horilla/observability.py:181-212`).

### 4.22 Mobile REST API — app `horilla_api`

- About 360 routes under `/api/` for every domain, plus a one-call mobile home and a capabilities payload (role, permissions, installed features) (`horilla_api/urls.py`).
- **INCONSISTENT**: some business rules are re-implemented in the API instead of shared with the web (leave approval order, 4.6).

## 5. Fork-specific changes (after Horilla 2.2.0)

| Commit | Date | Change |
|---|---|---|
| 87b05a3ce | 2026-11-10 | Docs (`docs/`, `attendance/MODULE_SUMMARY.md`), `deploy.sh`, prod compose changes |
| 085bb49ae | 2026-11-16 | DB docs (`docs/horilla_db.dbml`, dependency tree, domains), `fk_dependency_tree.py`, `fk_tree.html` |
| fb8ff8eec | 2026-11-16 | nginx removed from production; web published on host port 1000 |
| 808dea2b0 | 2026-11-16 | `deploy.sh` rebuilds the image every deploy |
| 7d8454d06 | 2026-11-18 | Structured access logging with scrubbed bodies (`horilla/observability.py`, `docker/gunicorn.conf.py`) |
| c5ba10744, 0ad9717b7 | 2026-11-18 | Company and employee time zones; check-in/out in the employee's zone; tests |
| 5c19a3de9 | 2026-11-18 | Edit-profile redirect loop fix |
| f2ab49933 | 2026-11-19 | AI-DLC configuration (not product code) |

Planned but not built (do not report as existing): leave balance ledger with event types, attendance claim quota with cutoff, per-region shift jobs, approver assignment with effective dates, WFH module, onboarding quiz gate (`docs/APURBA_TO_HORILLA_INTEGRATION_PLAN.md` §3-4).

## 6. Consolidated flag list

| # | Flag | Domain | Summary | Source |
|---|---|---|---|---|
| 1 | GAP | Cross-cutting | Scheduled jobs and attendance validation ignore company/employee time zones | `attendance/scheduler.py`, `leave/scheduler.py`, `payroll/scheduler.py`, `employee/scheduler.py`, `attendance/models.py:1061` |
| 2 | INCONSISTENT | Leave | Carry-forward vs available consumed in different order by web approval, auto-approval and API | `leave/views.py:1117`, `leave/views.py:473`, `horilla_api/api_views/leave/views.py:738` |
| 3 | RISK | Leave | Multi-level approval order not enforced; last approver completes the request | `leave/views.py:1150-1196` |
| 4 | RISK | Leave | Approval condition chosen by text sort of its value | `leave/models.py:1751` |
| 5 | BUG | Leave/Attendance | Deleting a clamped penalty over-restores leave | `base/signals.py:172-186` |
| 6 | HALF-BUILT | Leave | Accrual fields defined, no accrual | `leave/models.py:148, 247-248` |
| 7 | BUG | Payroll | Auto payslip re-generates mid-period joiners and resets to draft | `payroll/scheduler.py:62-79` |
| 8 | GAP | Payroll | No Bangladesh tax pack | `payroll/tax_packs.py` |
| 9 | BUG | Recruitment | Recruitment auto-close uses a frozen date and exact match | `recruitment/scheduler.py:9-28` |
| 10 | BUG | Shifts | Monthly rotation crashes in December | `base/scheduler.py:97, 203` |
| 11 | RISK | Shifts | Roster shift never reverted; schedule comment wrong | `base/scheduler.py:415-445` |
| 12 | RISK | Employee | Disciplinary job re-activates logins after suspension every minute | `employee/scheduler.py:51-88` |
| 13 | BUG | Documents | Expired documents never saved inactive; wrong link; repeated notices | `asset/scheduler.py:74-105` |
| 14 | BUG | Attendance | Rejected create-requests are not deleted | `attendance/views/requests.py:595-610` |
| 15 | BUG | Attendance | Bulk request crashes on an invalid day | `attendance/forms.py:1405` |
| 16 | RISK | Attendance | Excel import skips overtime, balance and daily status | `attendance/views/process_attendance_data.py` (per doc) |
| 17 | RISK | Attendance | Face matching not in this codebase | `facedetection/` |
| 18 | RISK | Attendance/Integrations | Extra in-process schedulers (biometric, Drive backup) | `biometric/views.py:431-504`, `horilla_backup/scheduler.py:21` |
| 19 | HALF-BUILT | Offboarding | Resignation approval has no effect; FnF is only a label | `offboarding/models.py:519-523` |
| 20 | GAP | Projects | Expiry only on edit | `project/models.py:228-234, 401-402` |
| 21 | GAP | Helpdesk | No SLA or overdue handling | `helpdesk/` |
| 22 | GAP | Onboarding | Probation end date not acted on | `onboarding/` |
| 23 | DISABLED | Integrations | LDAP, Outlook, dynamic fields, local PG backup | `horilla/settings/base.py:630`, `INSTALLED_APPS` |
| 24 | RISK | Security | nginx protections removed in fork's production | `docker-compose.prod.yml`, commit fb8ff8eec |
| 25 | RISK | Security/Privacy | Access log may record pay amounts and names from API bodies | `horilla/observability.py:181-212` |
| 26 | RISK | Access control | `manager_can_enter` admits any manager; several views lack record checks | `horilla/decorators.py:157-190`, `attendance/MODULE_SUMMARY.md` §5 |
| 27 | RISK | Notifications | Bot notices silently skipped without a "Horilla Bot" user | `base/scheduler.py:44-53` |
