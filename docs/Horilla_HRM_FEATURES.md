# Horilla HRMS — Feature & Architecture Reference

Version **2.2.0** (`horilla/__version__.py`), branch `2.0`, reviewed 2026-11-03.

This document lists what the application does, built from a pass over the source code (models, views, URLs, signals, schedulers, settings, templates, tests, Docker and CI files). It is organised as:

1. [Overview](#1-overview)
2. [Module map](#2-module-map)
3. [Business logic](#3-business-logic) — what each module does and the rules it enforces
4. [Integrations](#4-integrations)
5. [Security and access control](#5-security-and-access-control)
6. [UI / UX layer](#6-ui--ux-layer)
7. [Data layer](#7-data-layer)
8. [REST API (mobile)](#8-rest-api-mobile)
9. [Schedulers and background jobs](#9-schedulers-and-background-jobs)
10. [Running the application](#10-running-the-application)
11. [Testing](#11-testing)
12. [Deployment](#12-deployment)
13. [Observations from the review](#13-observations-from-the-review)

---

## 1. Overview

Horilla is an open-source HR management system (LGPL-2.1) covering the full employee lifecycle: recruitment → onboarding → employee records → attendance → leave → payroll → performance → offboarding, plus assets, helpdesk, projects and reporting.

| Item | Value |
|---|---|
| Backend | Django 5.2 (`Django~=5.2.17`), Python 3.12–3.14 |
| UI | Server-rendered Django templates + HTMX, Alpine.js, Tailwind (theme app) |
| API | Django REST Framework + SimpleJWT (serves the mobile app) |
| Database | PostgreSQL 16 in production/CI; SQLite by default for a fresh local clone |
| Cache | Redis (`django-redis`) when `REDIS_URL` is set, otherwise local memory |
| Background jobs | APScheduler, run by one dedicated process: `manage.py run_scheduler` |
| App server | Gunicorn (gthread) behind nginx; static files via WhiteNoise |
| Languages | 12 UI languages: English, German, Spanish, French, Arabic, Portuguese (BR), Simplified and Traditional Chinese, Italian, Turkish, Ukrainian, Romanian |
| Size | ~37 Django apps, ~250 models, 247 migrations, ~2,100 HTML templates, ~2,000 test cases |

---

## 2. Module map

Most apps register their own URL prefix in `AppConfig.ready()`, not in `horilla/urls.py`.

### Core HR modules (have a sidebar menu)

| App | Purpose | URL prefix |
|---|---|---|
| `employee` | Employee master data, profiles, org chart, policies, discipline | `/employee/` |
| `attendance` | Check-in/out, attendance records, overtime, late/early tracking, monthly summary | `/attendance/` |
| `leave` | Leave types, balances, requests, allocation, holidays, restrictions | `/leave/` |
| `payroll` | Contracts, salary structures, allowances/deductions, tax, payslips, loans, reimbursements | `/payroll/` |
| `recruitment` | Job openings, pipeline, candidates, interviews, surveys, talent pool, resume matching | `/recruitment/` |
| `onboarding` | Onboarding stages/tasks, candidate portal, conversion to employee | `/onboarding/` |
| `offboarding` | Exit pipelines, resignation letters, exit tasks, notice periods | `/offboarding/` |
| `pms` | Performance: OKRs, 360 feedback, 1:1 meetings, bonus points | `/pms/` |
| `project` | Projects, task boards, timesheets | `/project/` |
| `asset` | Asset register, batches, requests, allocation/return, service requests | `/asset/` |
| `helpdesk` | Tickets, claims, FAQs | `/helpdesk/` |
| `report` | 34 standard reports + pivot "Explorer" per module, scheduled report emails | `/report/` |

### Platform / shared apps

| App | Purpose |
|---|---|
| `base` | Company, department, job position/role, shifts, work from options, rosters, requests, announcements, holidays, mail servers/templates, approvals, settings, dashboards, setup wizard, media protection |
| `horilla` | Project package: settings, root URLs, `HorillaModel`, decorators, scheduling registry, model-extension (`inherit`), observability, testkit |
| `horilla_auth` | Custom user model `HorillaUser` (`AUTH_USER_MODEL`) |
| `horilla_api` | REST API for the mobile app (`/api/`) |
| `horilla_views` | Generic class-based list/form/detail/kanban/pipeline views and per-user view preferences |
| `horilla_theme` | Tailwind theme and the template overrides (`horilla_theme/templates`), colour themes |
| `horilla_widgets` | Custom form widgets and AJAX select/filter helpers |
| `horilla_crumbs` | Breadcrumbs |
| `horilla_audit` | History/audit tracking configuration and tags |
| `horilla_automations` | Mail/notification automations on model events |
| `horilla_documents` | Employee document requests and uploads |
| `horilla_dbtemplate` | Templates stored in the database (versioned, per site/language) |
| `horilla_tour` | Guided product tours (driver.js) |
| `master_import` | Spreadsheet import wizard (employees, assets, leave, salary structures) |
| `accessibility` | Feature-level access toggles (e.g. who can use the employee views, profile edit) |
| `notifications` | Vendored `django-notifications` (in-app notifications) |
| `biometric` | Biometric attendance devices (`/biometric/`) |
| `geofencing`, `facedetection` | Location and face checks for mobile attendance (`/api/geofencing/`, `/api/facedetection/`); added to `INSTALLED_APPS` by `horilla_api/__init__.py` |
| `horilla_ldap` | LDAP authentication and user sync |
| `horilla_meet` | Google Meet links for interviews/meetings (`/meet/`) |
| `horilla_backup` | Google Drive backups of the DB and media (`/backup/`) |
| `whatsapp` | WhatsApp Business notifications (`/whatsapp/`) |

### Shipped but not enabled by default (not in `INSTALLED_APPS`)

| App | Purpose |
|---|---|
| `outlook_auth` | Send mail through Microsoft 365 / Outlook via Azure OAuth (`/outlook/`) |
| `dynamic_fields` | Add custom fields to models at runtime (`/df/`, `add_field` / `delete_field` commands) |
| `pg_backup` | Local PostgreSQL dump scheduler |

---

## 3. Business logic

### 3.1 Organisation and company setup (`base`)

- **Multi-company**: several `Company` records in one install. The user switches company in the navbar, and company-scoped data is filtered to the selected company (see §7.3).
- **Org structure**: departments (with manager), job positions, job roles, employee types, work from options, tags.
- **First-run setup wizard** (`initialize_database*` views): creates the first admin user, company, departments and job positions. It is protected by `DB_INIT_PASSWORD`.
- **Setup checklist** banner per user and company (`SetupChecklistDismissal`).
- **System preferences**: default records per page (`DynamicPagination`, per user), badge-ID prefix, currency symbol and position, date and time formats (`HORILLA_DATE_FORMATS` / `HORILLA_TIME_FORMATS`), the languages enabled per company (`CompanyLanguageSetting`) and announcement expiry days.
- **Default export permission** per company: either everyone may export, or export falls back to the per-model `export_<model>` permissions.

### 3.2 Shifts, work from options and rosters (`base`)

- **Shifts** (`EmployeeShift`) with a per-weekday schedule (`EmployeeShiftSchedule`: start/end, minimum working hours, auto check-out time).
- **Rotating shifts** and **rotating work from options**. An employee is assigned a rotation that switches *after N days*, *every weekend* or *on a set day/date each month*. The scheduler applies the rotations.
- **Shift requests / work from requests**: employees request a change for a date range, and managers approve, reject or cancel them, individually or in bulk. Requests support comments and attachments. The scheduler switches the shift or work from on the start date and reverts it after the end date.
- **Roster**: forward planning of one employee, one date, one shift. Rosters are published (`RosterPublishLog` audit trail), and employees see published entries in *My Roster*. A scheduled job syncs roster entries into shifts.

### 3.3 Holidays, weekly offs and announcements (`base`)

- **Public holidays**, with a recurring flag (rolled forward yearly by the scheduler) and CSV/Excel import and export.
- **Company leaves / weekly off days**: e.g. "2nd Saturday", "every Sunday".
- **Announcements**: target employees, departments or job positions. They support attachments, comments and a "viewed by" list, and expire per company (`AnnouncementExpire`). Optionally they are also sent on WhatsApp.
- **Multi-level approval rules** (`MultipleApprovalCondition` / `MultipleApprovalManagers`): a condition on a request field (e.g. leave days > 3) routes the request through an ordered chain of approving managers. Used by leave requests.

### 3.4 Employees (`employee`)

- **Employee record**: personal info, `EmployeeWorkInformation` (company, department, job position/role, shift, work from, reporting manager, employee type, location, joining date, salary details), `EmployeeBankDetails`, tags and profile picture.
- **Lifecycle actions**: create, update, archive, replace (hand responsibilities to another employee), delete (blocked while the employee is still referenced), and bulk archive, delete or update. Admins can reset passwords singly or in bulk and send invitation emails singly or in bulk.
- **Login blocking**: an admin can block or unblock an employee's login account (`AccountBlockUnblock`).
- **Self-service**: an employee edits their own profile when the *Profile Edit* feature is granted (`ProfileEditFeature`, accessibility rule).
- **Import/export**: an Excel import of employees and work information, plus export.
- **Notes** with file attachments, and a **history tab** that tracks changes to configured work-information fields (`HistoryTrackingFields`).
- **Policies**: rich-text company policies with attachments, targeted to employees, departments or job positions.
- **Disciplinary actions**: action types *warning*, *suspension* (days or hours) and *dismissal*. When the action type has the *block* option, the scheduler deactivates the user's login during a suspension, reactivates it afterwards, and deactivates it permanently on dismissal.
- **Bonus points**: awarded manually or automatically by `BonusPointSetting` rules (PMS), viewable as history, and redeemable. Redeemed points can feed payroll encashment.
- **Org chart**, a **birthdays** widget, and dashboard counts (joining today/this week, on leave today, gender and department charts).
- **Experience**: worked experience is recalculated by the scheduler every 4 h.
- **Documents** (`horilla_documents`): HR raises a document request (e.g. "upload passport") for selected employees. Employees upload the file and HR approves or rejects it, singly or in bulk. Expiry dates trigger notifications.

### 3.5 Attendance (`attendance`)

- **Check-in / check-out** from the web (and the mobile API), with *break* activities (`AttendanceActivity`: each in/out pair). The **at-work tracker** shows a running timer of hours at work.
- **Restrictions**, configurable per company:
  - **IP restriction**: attendance only from the allowed IPs (`AttendanceAllowedIP`).
  - **Geofencing**: mobile check-in must fall within a radius of the company location (`geopy` geodesic distance).
  - **Face detection**: a face image per employee is stored for the mobile app's face check.
  - **Check-in/out enable toggle** per company.
- **Attendance record** per employee per day: shift, work from, check-in/out times, worked hours, minimum hours, overtime, and whether it is validated.
- **Validation**: a manager validates attendance. Records that don't meet `AttendanceValidationCondition` (e.g. worked hours below the threshold or overtime above the cutoff) are flagged. Revalidation is supported.
- **Overtime**: `AttendanceOverTime` monthly hour accounts. Overtime requires approval, singly or in bulk.
- **Grace time** (`GraceTime`): a per-shift or default allowance before a check-in counts as late, optionally applied to check-out too.
- **Late come / early out** tracking (`AttendanceLateComeEarlyOut`), with a toggle. **Penalties** (`PenaltyAccounts`): a late or early record can generate a payroll deduction or deduct leave from a chosen leave type.
- **Attendance requests / regularisation**: an employee requests a new or corrected attendance, and the manager approves or rejects it singly or in bulk. Requests support comments and files. **Batch attendance** groups requests. A **regularisation import** loads corrections from a spreadsheet.
- **Work records** (`WorkRecords`): a daily status per employee (present, absent, half day, leave, holiday, etc.), created by the scheduler every 30 min and at 00:30. Signals keep it in sync with leave and attendance.
- **Auto punch-out**: every 5 min the scheduler closes open attendances past the shift's auto check-out time.
- **Monthly summary**: a calendar per employee and month, with:
  - **Conflict resolution** for days where attendance overlaps leave, a holiday or a week-off (`AttendanceConflictResolution`: count the day as attendance or as leave). Resolution can be done singly or in bulk, with undo.
  - **Daily hour overrides** (`AttendanceDailyHours`) and **range hour overrides** (`AttendanceSummaryHours`). Manually edited values are never overwritten by recomputation.
  - **Month-end overrides** (`AttendanceSummaryOverride`): HR states the month's totals directly.
  - Export of the summary.
- **Imports/exports**: attendance and activity Excel import (with an error report), attendance export, and *Daily Work Status* and *Check-in/Check-out log* views.
- **Dashboard**: on time, late, early out, on break, pending hours, department overtime chart, and pending validations and overtime approvals.

### 3.6 Biometric devices (`biometric`)

- Supported devices: **ZKTeco / eSSL**, **Anviz**, **Matrix COSEC**, **Dahua**, **e-Time Office**. Each device is set as an *in*, *out* or *alternate* direction device.
- Test the connection, fetch logs on demand (singly or in bulk), use **live capture** (ZK) or **scheduled polling** (every N seconds per device, run by the `biometric.poll_devices` job).
- Device user management: list, add, map to employees by badge ID, edit, delete and bulk delete. COSEC face recognition can be enabled.
- Logs are converted into Horilla attendance check-ins and check-outs.

### 3.7 Leave (`leave`)

- **Leave types** (`LeaveType`):
  - payment: paid, unpaid, or custom (paid at a given percentage)
  - a total-days limit, which may be unlimited
  - **reset**: yearly, monthly, weekly or custom, on a chosen month and day
  - **carry forward**: none, carry forward up to a maximum, or carry forward with expiry
  - flags: encashable, requires approval, requires attachment, exclude holidays, exclude company leaves (weekly offs)
  - compensatory leave flag
- **Eligibility conditions** (`LeaveTypeCondition`): gender, *once per employment*, marital status, nationality, department, employment type, grade and service duration.
- **Assignment and balances** (`AvailableLeave`): assign leave types to employees (also importable through `master_import`). The record tracks available days, carried-forward days, reset dates and expiry dates. The scheduler resets balances and expires carry-forward every 4 h.
- **Leave requests**:
  - full day, first half or second half, at both the start and the end of the range
  - statuses: requested → approved / rejected; approved → cancel requested → cancelled
  - an approved leave stays in force (balance deducted, attendance marked) until the cancellation is approved
  - comments and attachments
  - **multi-level approval** with automatic approval of a stage where the approver is the requester
  - managers approve, reject or cancel in bulk
- **Leave allocation requests**: an employee asks for extra days, and the manager approves or rejects with comments.
- **Compensatory leave requests**: earn leave for working on a holiday or week-off (toggle).
- **Restricted leave periods** (`RestrictLeave`): block leave in a date range for a department and/or job position, for all leave types or only specific (or all-but-excluded) types.
- **Restrict past-date leave** (`EmployeePastLeaveRestrict`) toggle.
- **Integration**: an approved leave updates attendance work records. Leave can be deducted as an attendance penalty, and unpaid leave feeds loss-of-pay in payroll. Leave encashment is handled in payroll.
- **Dashboard**: who's on leave, leave balances, and pending requests.

### 3.8 Payroll (`payroll`)

The most extensive module (≈850 tests).

- **Contracts** (`Contract`):
  - wage type: daily, monthly, or hourly (only when attendance is installed)
  - pay frequency: weekly, monthly or semi-monthly
  - status: draft → active → expired / terminated
  - a filing status for tax, a notice period and documents
  - a scheduler job expires contracts past their end date
- **Salary structures** (`SalaryStructure`), in two modes:
  - *Gross Up*: the contract wage is basic pay and allowances add to it.
  - *CTC Down*: the wage is the total package, and components divide it, with a *Balance of CTC* component absorbing the rest.
  - `structure_rules.py` validates coherence, e.g. a BASIC component inside a Gross Up structure would count basic twice.
- **Allowances** (earnings), based on:
  - basic pay, or a percentage of another component (by code)
  - a **custom formula**: a safe AST-evaluated expression such as `(BASIC + DA) * 0.12`
  - balance of CTC, or number of children
  - with attendance installed: regular, week-off or holiday overtime, shift, work from, or attendance
  - fixed or computed, taxable or not, with conditions (`if` field/operator/value), a maximum limit prorated for partial periods, and specific or excluded employees
- **Deductions**, based on basic, gross, taxable gross or net pay, another component, or a formula. They can be pre-tax or post-tax, employer contributions, one-time (on a date), or *exceed handling* (skip or cap when the deduction exceeds pay).
- **Component engine** (`methods/component_engine.py`): an ordered evaluation (explicit `sequence`) in which each component can read earlier results.
- **Component library**: ready-made HRA, DA, Conveyance, Special Allowance, PF, ESI, Professional Tax (India), 401(k), Social Security, Medicare (US), Housing, Transport, GOSI (GCC), Workplace Pension (UK).
- **System components**: loans, salary advances, fines, attendance penalties, reimbursements, leave and bonus encashment, and loss of pay as configurable components (`sync_system_components` command).
- **Income tax**:
  - `FilingStatus` with tax slabs (`TaxBracket`), standard deduction, rebate (income limit and maximum), and cess percentage
  - an optional Python formula mode in a sandbox (`safe_tax_code.py`)
  - **tax packs**: India New Regime and Old Regime (FY 2025-26), US Federal Single and Married Filing Jointly (2025), UK PAYE (2025-26), and Flat 10%
  - yearly tax is computed, then converted to the pay period
- **Payslips**:
  - generated singly or in bulk
  - status: draft → review ongoing → confirmed → paid
  - a PDF payslip (pdfkit/xhtml2pdf) and email to employees (threaded mail sender)
  - a per-line *how was this worked out* popover (`earning_working.py`)
  - manual overrides on a generated payslip (`payslip_edit.py`) that never touch the shared component definitions
- **Payroll runs** (`PayrollBatch`):
  - a reviewable 3-step run: **scope** (period and people), **review** (blocking and non-blocking problems per employee), **generate** in slices with progress
  - batch state machine: Draft → In review → Approved → Paid; or Cancelled. *Paid* is terminal.
  - per-employee lines (`PayrollBatchLine`) with status
- **Pay periods** (`PayPeriodSettings`): a configurable pay month, e.g. the 26th to the 25th.
- **Auto payslip generation** (`PayslipAutoGenerate`): per company, on a chosen day of the month or the last day. The scheduler checks every 3 h and creates draft payslips for the previous month.
- **Loans and salary advances** (`LoanAccount`): installments are auto-created as deductions on save.
- **Reimbursements and encashments**: reimbursement claims with attachments and comments, **leave encashment** (amount per leave day, `EncashmentGeneralSettings`), and **bonus point encashment**. Each needs approval.
- **Contributions / remittance** view: the employee and employer shares (PF, ESI, Social Security) are read from the issued payslips.
- **Employer cost** and a **cost composition** report.
- **Dashboard**: payroll totals, payslip status, department chart, and contract-expiry alerts.
- Maintenance commands: `check_structure_invariants`, `normalise_*`, `backfill_component_sequence`, `seed_tax_packs`, `payroll_snapshot`, `report_lop_deduction_mode`.

### 3.9 Recruitment (`recruitment`)

- **Recruitments (job openings)**: job positions, vacancies, start and end dates, recruitment managers, skills, a survey template, and a published/closed state. The scheduler closes them on the end date.
- **Pipeline** (kanban): stages typed *initial / applied / test / interview / cancelled / hired*, with per-stage managers, drag-and-drop between stages and reordering. An initial stage is auto-created by a signal.
- **Candidates**:
  - profile, resume, source and referral source, and offer letter status (not sent → sent → accepted / rejected → joined)
  - notes with files, history, ratings, **reject reasons**, and archive
  - export, and conversion to employee
- **Interviews**: schedule them with interviewer employees and optional Google Meet links. They appear in the employee's profile tab.
- **Recruitment surveys / application form**: question templates with 10 question types (checkbox, options, multiple, text, number, percentage, date, textarea, file, rating) and ordering. There is a public application form per recruitment.
- **Candidate self-tracking portal**: the candidate logs in to see their application status and stage (feature toggle).
- **Resume screening**: bulk upload resumes (PDF via PyMuPDF), then extract name, email, phone and DOB (spaCy `en_core_web_sm` NLP), match skills and rank resumes against a recruitment's skills.
- **Talent pool (Skill Zone)**: keep candidates per skill for future openings.
- **Candidate document requests**: ask candidates to upload documents, then approve or reject them.
- **LinkedIn**: connect an account and post or delete job openings.
- **Mail templates** for candidate emails, with preview and send. Acknowledgement mails are supported.
- **Dashboard**: pipeline, hiring, vacancy and hired-candidate charts.

### 3.10 Onboarding (`onboarding`)

- **Onboarding stages and tasks** per recruitment. Tasks are assigned to employees, and their status is *todo / scheduled / ongoing / stuck / done*.
- Candidates who reach *hired* appear in onboarding. Moving them through stages, bulk updates and kanban view are supported.
- **Onboarding portal**: a tokenised link where the candidate fills in personal info, a profile photo and bank details themselves. HR then creates the user and employee record ("welcome aboard").
- Offer letter status updates (single or bulk), joining date, probation end date, and reject or undo.
- Email the candidates, a task report, and a dashboard (stage chart).

### 3.11 Offboarding (`offboarding`)

- **Offboarding pipelines** with stages typed *notice period / FnF (full & final) / interview / handover / other / archived*, and managers.
- Employees are added to a pipeline, moved between stages and given notes and attachments. **Exit tasks** per stage have statuses *todo / in progress / stuck / completed*. Tasks marked required block the stage move.
- **Resignation letters**: an employee submits a resignation, and a manager approves or rejects it (*requested / approved / rejected*). A feature toggle controls this.
- **Exit reasons**, **default notice period** settings, and a notice-period end-date calculation.
- **Dashboard**: task table and department/job-position charts.

### 3.12 Performance management (`pms`)

- **OKRs**: objectives (company-level and per employee), key results with progress types (%, number, currency), statuses (*Not Started / On Track / Behind / At Risk / Closed*), managers, assignees, comments and activity history, and archive.
- **Periods** for review cycles.
- **360° feedback**: question templates (rating 1–5 and other types), feedback requests with manager, colleague, subordinate and other reviewers, linked to employee key results, plus answers and status. **Cyclic feedback** (every N days/months) is recreated by the scheduler daily at 08:00.
- **Anonymous feedback**, about employees, departments, job positions or general.
- **Meetings (1:1s)**: with managers and employees, question templates, answers and responses.
- **Bonus points settings**: award points automatically when an employee objective or key result reaches a condition (dynamic signals).
- **Dashboard**: objective, key-result and feedback status charts.

### 3.13 Projects (`project`)

- **Projects**: managers, members, start and end dates, document. Status is *new / in progress / completed / on hold / cancelled / expired*.
- **Stages** per project (kanban columns, drag-and-drop) and **tasks** (*to do / in progress / completed / expired*), with assignees, deadlines and quick create.
- **Timesheets**: time logged against a project and task by an employee, plus a personal timesheet view.
- Import (template), bulk export, archive and delete, and a dashboard with project and task status charts.

### 3.14 Assets (`asset`)

- **Asset categories**, **asset lots / batches**, **assets** (status *In use / Available / Not-Available*) and **asset items**: individual physical units with status *Available / In use / Damaged / Lost*, edited in bulk.
- **Asset requests**: an employee requests an asset, and the manager approves (allocate) or rejects with a reason.
- **Allocation and return**: return requests, condition on return (*Healthy / Minor damage / Major damage / Lost*), return images, and asset reports with documents.
- **Service requests**: an employee raises a complaint against an allocation. The status flows *Requested → In Progress → Completed / Rejected / Returned*, with notes.
- **Asset fine** toggle: when enabled, a fine can be added for the employee when an asset is returned (the fine form lives in payroll, `payroll/views/component_views.py: asset_fine`). Asset rules page.
- **Expiry**: notifications for expiring assets and asset documents. The scheduler marks expired assets.
- Excel import, export, asset history, and a dashboard with availability and category charts.

### 3.15 Helpdesk (`helpdesk`)

- **Tickets**:
  - types: suggestion, complaint, service request, meeting request, anonymous complaint, others
  - priority: low, medium or high
  - status: *new / in progress / on hold / resolved / canceled*
  - "raised on" an employee, department or job position, with assignees, deadline and tags
  - comments with attachments, and documents
- **Claim requests**: an agent claims a ticket, and a manager approves the claim.
- **Department managers** (by department or job position) receive the tickets raised against them.
- **FAQ categories and FAQs**, with suggestions while a ticket is being written.
- Bulk archive and delete, and a dashboard.

### 3.16 Reports (`report`)

- **34 standard reports** in 5 domains:
  - **Workforce**: Workforce Composition, Headcount Bridge, Joiners & Leavers, Turnover, Exit Analysis, New-Hire 90-Day Attrition, Tenure & Longevity, Span of Control, Diversity Snapshot
  - **Time & Leave**: Attendance Summary, Absenteeism Rate, Unscheduled Absence, Overtime Analysis, Leave Planning, Open Leave Balance
  - **Payroll**: Payslip Register, Labor Cost Summary, Cost Composition, Payroll Headcount Cost, Payroll Readiness, Loan & Advance Ledger, Reimbursement Register
  - **Talent**: Recruitment Funnel, Pipeline Aging, Time to Hire/Fill, Offer & Acceptance, Source Quality, Quality of Hire, Onboarding Progress, Objective & KR Health
  - **Compliance**: Asset Register, Audit Activity, Contracts & Document Expiry, Document Expiry Aging
- Per-report filter schemas, **period comparison**, **drill-down** to records, KPIs, charts and narrative text.
- **Exports**: Excel (cover, data and native chart sheets), CSV and PDF with the company letterhead. Heavy exports run in the background.
- **Personalisation**: favourites, named saved views (e.g. "Q3 board pack"), filter presets and recent runs.
- **Access matrix** (`ReportAccess`): view, export and subscribe rights per report, falling back to Django permissions. Users without global permission see only their subordinates.
- **Subscriptions**: scheduled delivery of a report as an Excel email attachment, checked hourly. A run log (`ReportRunLog`) is kept.
- **Explorer**: a pivot-table builder (pivottable.js) per module (employee, attendance, leave, payroll, PMS, recruitment, asset), with saved layouts (`ReportTemplate`).

### 3.17 Automations and notifications

- **Mail automations** (`horilla_automations`):
  - choose a model, a trigger (*on create / on update / on delete*) and conditions (field, operator, value, with nested relations)
  - recipients are resolved through relations
  - the mail template is rendered with the instance
  - delivery: email, in-app notification, or both
  - handlers are connected dynamically and refreshed when automations change
- **Mail templates** (`HorillaMailTemplate`): reusable rich-text bodies with placeholders.
- **Email servers** (`DynamicEmailConfiguration`): multiple SMTP servers per company, one primary, with a test email. A dynamic display name is supported. Every outbound mail is logged to `EmailLog`, with OTPs and reset links redacted.
- **In-app notifications**: vendored `django-notifications`, with an inbox, mark-read, a notification sound (`NotificationSound`) and API endpoints.
- **WhatsApp** notifications and announcements (§4).

### 3.18 Import (`master_import`)

A wizard: upload a sheet → map its columns → check (errors shown per row and editable in place) → run, with progress → summary and error workbook → import history. The datasets are:
- employees (person, work info and bank details in one sheet)
- update existing employees (matched by key; a blank cell never overwrites, and an ambiguous match is an error)
- assets, asset allocations, assigned leave, and salary structures

Names shared across companies are resolved by company scoping.

### 3.19 Demo and seed data

- `load_data/*.json` fixtures, plus the `load_demo_data`, `seed_dashboard_demo_data`, `create_branch_demo_fixtures`, `create_payroll_fixtures` and `create_summary_fixtures` commands.
- `create_faqs`, `create_default_themes`, `seed_standard_report_templates`, `seed_tax_packs`.
- Default role groups created on migrate: **Admin, HR Manager, Payroll Manager, Attendance Manager, Leave Manager, Recruiter, Asset Manager, Helpdesk Agent, Project Manager**.

---

## 4. Integrations

| Integration | App | What it does | Configuration |
|---|---|---|---|
| LDAP / Active Directory | `horilla_ldap` | LDAP login and attribute mapping; import users from LDAP and push users to LDAP (`import_ldap_users`, `import_users_to_ldap`) | Settings page + `AUTH_LDAP_*` |
| Google Meet | `horilla_meet` | OAuth per employee; create/delete Meet links for interviews and meetings | Google Cloud project ID, client ID/secret, redirect URIs |
| Google Drive backup | `horilla_backup` | `pg_dump` of the DB and zip of `MEDIA_ROOT`, uploaded to a Drive folder at an interval or a fixed time | Service-account JSON + folder ID |
| WhatsApp Business (Meta) | `whatsapp` | Templates and flows; sends notifications and announcements; verified webhook (signature check) | Meta token, business ID, phone number ID, webhook token |
| LinkedIn | `recruitment` | Post and delete job openings | API token per account |
| Microsoft 365 / Outlook mail | `outlook_auth` (optional) | Azure OAuth mail sending, token refreshed every 50 min | `AzureApi` records |
| AWS S3 media storage | settings `addons.py` | Media uploads to S3 via `django-storages` | `AWS_*`, `DEFAULT_FILE_STORAGE`, `MEDIA_URL`, `NAMESPACE` |
| Biometric devices | `biometric` | ZKTeco/eSSL, Anviz, Matrix COSEC, Dahua, e-Time Office | Device IP/port/credentials |
| Sentry | `horilla/observability.py` | Error reporting with sensitive keys scrubbed | `SENTRY_DSN` |
| Prometheus | `/metrics/` | Scheduler job metrics (staff only; nginx denies it externally) | — |

---

## 5. Security and access control

- **Authentication**:
  - username/password login
  - **django-axes** lockout: 5 failures, then a 30-min cooloff per username + IP
  - optional **two-factor OTP by email** (`TWO_FACTORS_AUTHENTICATION`, `TwoFactorAuthMiddleware`)
  - **force password change** on first login (`ForcePasswordChangeMiddleware`)
  - password reset by email, LDAP login, and the candidate portal login
- **Sessions**: 12 h lifetime (`SESSION_COOKIE_AGE`) and refreshed on every request. Secure cookies are set in production.
- **Authorisation**:
  - Django model permissions through groups, editable in a permission matrix UI (roles, employee permissions)
  - **company-scoped permissions** (`COMPANY_SCOPED_PERMISSIONS=True` by default): group membership applies per company through `CompanyGroupAssignment` and `CompanyScopedBackend`
  - view decorators: `login_required`, `permission_required`, `manager_can_enter`, `owner_can_enter`, `hx_request_required`, `install_required`
  - **feature accessibility** (`accessibility`): per-feature rules restricting who can use the employee views or profile edit
  - **menu access restrictions** in settings
- **Data isolation**: company-scoped managers on ~146 model declarations, plus a system check (`horilla.tenancy`) that warns about unscoped models.
- **Input safety**: `HorillaModel.save()` always runs `clean_fields()`, which includes an XSS check on string fields. An SVG security middleware is in place, and component and tax formulas run in sandboxes.
- **Media protection**: `/media/` is served by Django (`protected_media`) with access checks, not directly by nginx.
- **Production gate** (`horilla/settings/security.py`): with `DEBUG=False` or `HORILLA_ENV=production`, the app refuses to start on a known default `SECRET_KEY`, an empty or `*` `ALLOWED_HOSTS`, or the default `DB_INIT_PASSWORD`. It also sets secure cookies, nosniff and a referrer policy, and HSTS when `SECURE_SSL_REDIRECT` is on.
- **Rate limits**:
  - DRF throttles: anon 60/min, user 600/min, login 12/min, bulk 6/min
  - nginx: login 5 requests/min (burst 10)
- **Unauthenticated health endpoint** reports the product and API contract version, not the exact release.
- Security regression tests cite their GHSA advisories (29 files).

---

## 6. UI / UX layer

### 6.1 Technology

- Server-rendered Django templates; **HTMX** for partial page updates (modals, lists, filters, inline forms); **Alpine.js** (`x-data`, ~250 templates) for local state; Hyperscript in a few places.
- **Tailwind CSS** theme (`horilla_theme`), plus legacy Bootstrap assets for older screens.
- Libraries:
  - jQuery and **Select2** (searchable selects)
  - **ApexCharts** and Chart.js (dashboards)
  - **SweetAlert** (confirmations)
  - **Summernote** (rich text)
  - **pivottable.js** with Plotly and Excel renderers (Explorer)
  - **jsPDF**, an org-chart library, moment.js, Ionicons and Font Awesome
  - **driver.js** (product tours)

### 6.2 Layout and navigation

- **Sidebar** built per request from each module's `sidebar.py`: menu, icon and sub-menus, with each item gated by permission or accessibility. The 12 modules are Employee, Attendance, Leave, Payroll, Recruitment, Onboarding, Offboarding, Performance, Project, Assets, Helpdesk and Reports.
- **Navbar**: company switcher, language switcher (company-enabled languages only), notifications inbox, profile, and a theme toggle.
- **Breadcrumbs** (`horilla_crumbs`), loaded as an HTMX fragment.
- **Settings area**, grouped as:
  - *General*: preferences, login restriction, profile edit, history tracking, languages, menu access
  - *Roles & Permissions*
  - *Audit & History*
  - *Organization*: companies, departments, positions, roles, weekly offs, holidays
  - *Email*: servers, templates, automations
  - *Appearance*
  - *Integrations*: Drive backup, LinkedIn, LDAP, Google Meet, WhatsApp, Outlook
  - *Master Data*: import, import history
  - a rules page per module

### 6.3 Generic list and detail framework (`horilla_views`)

Most newer screens are built from the same generic CBVs, so they share behaviour:

- **Nav bar** (`HorillaNavView`): search, filter panel (classic or "modern" filter), group-by (including nested), view switcher (list, card, kanban), create button and actions.
- **List view** (`HorillaListView`):
  - **column toggling** and **column reordering**, remembered per user (`ToggleColumn`, `ColumnOrder`)
  - sorting, **filter tags**, **saved filters** (`SavedFilter`) and **quick date filters**
  - row status colours and legends
  - **bulk select** with bulk update, bulk delete (with a summary of what was blocked) and archive
  - **quick export** (Excel/CSV), import with column mapping
  - per-user records per page, record counts in tabs, and an accordion group-by
- **Card view**, **Kanban view** (drag-and-drop between columns) and **Pipeline view** (recruitment/onboarding/offboarding style stages).
- **Detail view** (side drawer/modal with next/previous navigation), **Tab view** (remembers the active tab, `ActiveTab`), **Profile view** and **History view** (field-level change history).
- **Form view** (HTMX modal forms, dynamic field reload) and **related-object auto-links** (`related_link_registry`).
- Remembered UI state: active view type (`ActiveView`), active group-by (`ActiveGroup`).

### 6.4 Dashboards

- **Home dashboard**, role-based (`dashboard_roles.py`):
  - *Leadership*: superuser, staff, or an employee with employee + leave + recruitment view
  - *HR*: view employee + view leave request
  - *Manager*: a reporting manager
  - *Employee*: everyone else, who gets the self-service dashboard
- **Modern dashboard** (`/dashboard/modern/`): KPI cards and ApexCharts.
- **Employee self-service dashboard** (`/my-dashboard/`): personal data only.
- **Dashboard customisation**: show or hide charts and reorder them per user (`DashboardEmployeeCharts`).
- A **requests and approvals** panel on the dashboard (leave, attendance, shift and work-from requests).
- Each module has its own dashboard: employee, attendance, leave, payroll, recruitment, onboarding, offboarding, PMS, project, asset and helpdesk.

### 6.5 Theming, i18n and onboarding UX

- **Colour themes** (`HorillaColorTheme`: a primary 50–900 palette and more) and a theme per company (`CompanyTheme`). Dark mode is supported (`darkMode`). White-labelling is available through the `WHITE_LABELLING` setting.
- **12 languages**, with gettext catalogs in `horilla/locale/` and a JS catalog at `/jsi18n/`.
- **Product tours** (`horilla_tour`): admin-defined tours with ordered steps, shown to target audiences on matching pages. Tours can auto-start, and completion is tracked per user.
- **Database templates** (`horilla_dbtemplate`): override any template from the DB, with draft/active/archived states, an activation window, per-site and per-language overrides, version history with restore, diff, live preview and edit locks.
- **Setup checklist** for new installs, and the empty-state templates.

---

## 7. Data layer

### 7.1 Databases and storage

- **Database**: `DATABASE_URL` (via django-environ) when set. Otherwise the `DB_ENGINE`/`DB_NAME`/... variables, defaulting to SQLite `TestDB.sqlite3`. PostgreSQL 16 is used in Docker and CI.
- **Cache**: Redis (`django-redis`, key prefix `horilla`) when `REDIS_URL` is set, otherwise local memory. Used for, among others, the accessibility cache, the pipeline stage cache version and the readiness probe.
- **Files**: local `media/` by default, or S3 when the `AWS_*` variables are set (`STORAGES["default"]`). Static files are served by WhiteNoise `CompressedStaticFilesStorage`.
- **Scheduler job store**: `django_apscheduler` tables (`DjangoJob`, `DjangoJobExecution`).

### 7.2 Base model (`horilla/models.py`)

Domain models extend `HorillaModel`, which provides:
- `created_at`, `created_by`, `modified_by`, `is_active` (soft archive), and an auditlog history field (`horilla_history`)
- `save()` fills `created_by`/`modified_by` from the current request (thread-local/ContextVar set by middleware)
- `save()` always calls `clean_fields()`, so the XSS check runs on every write path: forms, API, scripts
- the `HorillaModelBase` metaclass, which supports **model extension**: a subclass with `_inherit = "app.Model"` injects fields and methods into another app's model. A patched `makemigrations`/`migrate` (`HorillaAutodetector`) writes them as `InjectField` operations in the extending app.

### 7.3 Multi-company tenancy

- Opt-in per model: `objects = HorillaCompanyManager()`, or `HorillaCompanyManager("employee_id__employee_work_info__company_id")` to filter through a relation.
- The current company lives in the `current_company_id` ContextVar, set by `CompanyMiddleware` (web) or `TenantScopedJWTAuthentication` (API).
- A system check (`--tag horilla.tenancy`) warns about any model with a `company_id` but no company manager, unless the model is listed in `EXEMPT`.
- Global monkeypatches add `pre/post_bulk_update` signals (on `QuerySet.update`) and `pre/post_model_clean` signals.

### 7.4 History and audit

- **django-auditlog**: opt-in per model. By default it covers Employee, EmployeeWorkInformation and EmployeeBankDetails. `AuditModelConfig` rows override the set, down to individual fields.
- **django-simple-history** (`HorillaAuditLog` extends `HistoricalRecords`): `Historical*` shadow tables. Each history entry can carry a title, description, highlight and **audit tags** (`AuditTag`).
- Work-information history tracking per company (`HistoryTrackingFields`).
- **Other logs**: `EmailLog` (outbound mail, redacted), `RosterPublishLog`, `ReportRunLog`, master-import `ImportJob`, axes access logs, login-failure signal logging.

### 7.5 Key data relationships

- `HorillaUser` 1–1 `Employee` (`user.employee_get`). `Employee` 1–1 `EmployeeWorkInformation` (company, department, position, shift, manager). Nearly every module links to `Employee`.
- Recruitment `Candidate` → onboarding (`CandidateStage`/`CandidateTask`/`OnboardingPortal`) → `Employee`.
- `Employee` → `Contract` → `SalaryStructure` → `Allowance`/`Deduction` → `Payslip` (component snapshot in JSON `pay_head_data`) → `PayrollBatch`/`PayrollBatchLine`.
- `LeaveType` → `AvailableLeave` (balance per employee) → `LeaveRequest` → attendance `WorkRecords`.
- `Attendance` → `AttendanceActivity` (punches), `AttendanceOverTime` (monthly), `AttendanceLateComeEarlyOut` → `PenaltyAccounts` → payroll deduction or leave cut.

### 7.6 Signals (cross-module side effects)

| Signal source | Effect |
|---|---|
| `Company` created | Creates the announcement-expiry, default-export-permission and attendance settings |
| `post_migrate` | Creates shift days and the default HRMS role groups, and syncs export permissions |
| `PenaltyAccounts` saved/deleted | Creates/removes the matching payroll deduction or leave cut |
| `LeaveRequest` saved/deleted | Updates attendance work records; approval stages auto-approve self-approval |
| `Attendance` saved/deleted | Updates work records and late/early records |
| `Recruitment` created | Creates the initial pipeline stage |
| `CandidateDocumentRequest` m2m | Creates candidate document slots |
| `LoanAccount` created | Creates installment deductions |
| `EmployeeWorkInformation` saved | Payroll-side sync (e.g. contract/department) |
| `Announcement`/`Policy` m2m | Expands department/position targets into employees |
| `MailAutomation`/`BonusPointSetting` changes | Reconnects the dynamic automation handlers |
| `user_login_failed` | Logs the failed login |

### 7.7 Migrations

247 migration files. CI runs `makemigrations --check --dry-run`, so a model change without its migration fails the build.

---

## 8. REST API (mobile)

- Base path `/api/`. JWT auth: 60-min access token and 30-day refresh token with rotation, blacklisting after rotation, and revocation checks. Logout blacklists the refresh token.
- **Docs**: Swagger at `/api/swagger/` and `/api/docs/`, and ReDoc at `/api/redoc/`. They are public only when `DEBUG` is on; otherwise they are admin-only.
- **Endpoint groups** (approximate route counts):

| Group | Routes | Group | Routes |
|---|---|---|---|
| `auth/` (login, refresh, logout, reset-password) | 4 | `leave/` | 32 |
| `base/` (incl. `capabilities/`) | 57 | `payroll/` | 17 |
| `employee/` | 27 | `recruitment/` | 39 |
| `attendance/` | 26 | `onboarding/` | 18 |
| `pms/` | 49 | `offboarding/` | 23 |
| `helpdesk/` | 22 | `project/` | 12 |
| `asset/` | 8 | `notifications/` | 5 |
| `mobile/home/` (one call for the whole home screen) | 1 | `geofencing/`, `facedetection/` | separate prefixes |

- **Capabilities payload** at login and `/base/capabilities/`: the resolved role, permission booleans and installed features, so the mobile app can adapt its navigation in one call.
- Throttle scopes: `anon`, `user`, `login` and `bulk`. Pagination is page-number based with 20 per page, and filtering uses `django-filter`.

---

## 9. Schedulers and background jobs

**Design**: apps call `horilla.scheduling.register_job(func, trigger, ...)` in `<app>/scheduler.py`. Only `python manage.py run_scheduler` executes jobs. It is one `BlockingScheduler` in the project timezone with a `DjangoJobStore`, `max_instances=1`, `coalesce=True`, error and missed-run logging, and a clean shutdown on SIGTERM. Run **exactly one** scheduler replica, because the jobs are not idempotent. `python manage.py run_scheduler --list` prints the registered jobs.

| Job | App | Schedule | What it does |
|---|---|---|---|
| `rotate_shift` (job1) | base | every 4 h | Applies rotating-shift assignments |
| `rotate_work_from` (job2) | base | every 4 h | Applies rotating work from options |
| `switch_shift` / `undo_shift` (job4/job3) | base | every 4 h | Applies approved shift requests on the start date and reverts them after the end date |
| `switch_work_from` / `undo_work_from` (job5/job6) | base | every 4 h | Same for work-from requests |
| `recurring_holiday` | base | every 4 h | Rolls recurring holidays forward to the next year |
| `sync_roster_shifts` | base | every 4 h | Applies published roster entries |
| `update_experience` | employee | every 4 h | Recalculates employee experience |
| `block_unblock_disciplinary` | employee | every 60 s | Suspends, reactivates or dismisses user logins per disciplinary action |
| `create_work_record` | attendance | every 30 min + daily 00:30 | Creates the daily work-status records |
| `auto_punch_out` | attendance | every 5 min | Closes open attendances at the shift's auto check-out time |
| `biometric.poll_devices` | biometric | every 1 min | Polls each scheduler-enabled device once its own interval has elapsed |
| `leave_reset` | leave | every 4 h | Resets balances, applies carry-forward and expires carried leave |
| `expire_contract` | payroll | every 4 h | Marks active contracts past their end date as expired |
| `auto_payslip_generate` | payroll | every 3 h | On the configured day, creates draft payslips for the previous month |
| `cyclic_feedback_creation` | pms | daily 08:00 | Recreates cyclic 360-feedback rounds |
| `candidate_convert` | recruitment | every 5 min | Flags candidates whose email already belongs to a user |
| `recruitment_close` | recruitment | every 1 h | Closes and unpublishes recruitments on their end date |
| `notify_expiring_assets` / `mark_expired_assets` | asset | daily | Asset expiry notices and status |
| `notify_expiring_documents` | asset | every 4 h | Document expiry notices |
| `report_subscriptions` | report | every 1 h | Sends due report subscriptions (also `manage.py run_report_subscriptions`) |
| `refresh_outlook_auth_token` | outlook_auth (optional) | every 50 min | Refreshes Azure tokens |

**Monitoring**:
- `/ready/` reports `scheduler: ok|missing`. It returns 503 for a missing scheduler only when `HORILLA_REQUIRE_SCHEDULER=1`.
- `/metrics/` exposes job metrics in Prometheus format (staff only).
- Job errors go through the app logger, so Sentry sees them.

**Exceptions to the design**: see §13. Google Drive backup and the biometric "schedule" button still start their own in-process schedulers.

---

## 10. Running the application

### 10.1 Local (no Docker)

```bash
python -m pip install --upgrade pip      # upgrade first, or cryptography/PyMuPDF wheels fail
pip install -r requirements.txt          # includes spaCy + the en_core_web_sm model
cp .env.dist .env
touch horilla/settings/local_settings.py # gitignored; must exist
python manage.py migrate
python manage.py compilemessages
python manage.py collectstatic
python manage.py runserver               # web
python manage.py run_scheduler           # second terminal: background jobs
```

Open `http://localhost:8000` and complete the setup wizard using `DB_INIT_PASSWORD`. Optional extras:
- `python manage.py createhorillauser` creates an admin.
- `python manage.py load_demo_data` loads the demo data.

> **Environment gotcha.** `.env` is loaded with `overwrite=False`, so real environment variables win over it. If `.env` holds production values, override them on the command line for local work and tests (see §11).

### 10.2 Docker (development)

`make dev` (`docker compose up --build`) starts **web** (gunicorn, port 8000, source bind-mounted), **scheduler** (`run_scheduler`, no release tasks), **db** (postgres:16-alpine) and **redis** (redis:7-alpine). nginx is only in the `production` profile.

Other targets:
- `make shell`, `make db-shell`, `make logs` / `make logs-web`, `make status`, `make restart`, `make stop`
- `make clean` **deletes volumes**

### 10.3 Useful management commands

| Command | Purpose |
|---|---|
| `run_scheduler [--list]` | Run or list background jobs |
| `createhorillauser` | Create an admin user |
| `load_demo_data`, `seed_dashboard_demo_data`, `demo_data_inventory` | Demo data |
| `audit_perms` | Snapshot effective permissions per user (optionally per company) to JSON, for before/after diffs (`perm_baseline.json` in the repo root is such a snapshot) |
| `horilladumpdata`, `trigger_save` | Data utilities |
| `migrateusers` | Migrate legacy users to `HorillaUser` |
| `import_ldap_users`, `import_users_to_ldap` | LDAP sync |
| `create_default_themes`, `create_faqs`, `seed_standard_report_templates`, `seed_tax_packs` | Seed data |
| `sync_system_components`, `check_structure_invariants`, `normalise_*`, `payroll_snapshot` | Payroll maintenance |
| `run_report_subscriptions` | Send due report subscriptions now |

---

## 11. Testing

- **Runner**: the Django test runner; there is no pytest. Tests live in `<app>/tests/test_*.py`.
- **Size**: about **1,994 test cases** across 33 test packages. The largest suites:

| App | Test files | Tests |
|---|---|---|
| payroll | 39 | 850 |
| base | 24 | 204 |
| horilla_api | 27 | 167 |
| attendance | 15 | 156 |
| master_import | 1 | 132 |
| leave | 16 | 120 |
| report | 4 | 114 |
| horilla (core) | 6 | 37 |
| notifications | 2 | 31 |
| recruitment | 7 | 28 |

- **Fixtures**: `horilla.testkit` (`make_company`, `make_user`, `make_employee` and the domain factories in `factories.py`). `CompanyFilterTestMixin` provides company-scoped queries.
- **Commands**:

```bash
# Override production-style .env values the way CI does:
DEBUG=True HORILLA_ENV= SECRET_KEY=ci-dev-not-for-production ALLOWED_HOSTS=localhost,127.0.0.1 \
DATABASE_URL=sqlite:///test.sqlite3 REDIS_URL= python manage.py test leave

python manage.py test leave                                    # one app
python manage.py test leave.tests.test_leave_request_idor       # one module
python manage.py test leave.tests.test_leave_request_idor.LeaveRequestVisibilityTests.test_name
make test-smoke      # every app in SMOKE_LABELS
make test-cov        # smoke suite under coverage, fails under COV_FAIL_UNDER (26%)
```

- **Coverage**: branch coverage (`.coveragerc`) was measured at 27.6% on 2026-09-01, and the floor is 26%. The coverage source is leave, attendance, base, payroll, recruitment, report, horilla_auth, employee, accessibility and horilla_api.
- **CI** (`.github/workflows/`):

| Workflow | Checks |
|---|---|
| `unit-tests.yml` | Postgres 16 service; `makemigrations --check --dry-run`; `make test-cov` |
| `quality.yml` | `ruff check .` (bug-class rules only); Black + isort on `horilla/settings` and `horilla/urls.py`; `manage.py check`; `pip-audit`; gitleaks secret scan; production-settings gate |
| `docker-ci.yml` | Builds the image, boots it, curls `/health/` and `/ready/`, Trivy scan (CRITICAL) |
| `docker-publish.yml` | On tag: checks the version matches the tag, smoke-tests, then publishes the image |
| `codeql.yml` | CodeQL static analysis (push, PR, schedule) |

- Lint locally: `ruff check .`, `pre-commit install` (ruff --fix, black, isort, whitespace).

---

## 12. Deployment

### 12.1 Image (`Dockerfile`)

- Multi-stage build on `python:3.12-slim`. The builder stage installs build libraries, creates a venv and installs `requirements.txt`, then asserts the spaCy model version. The runtime stage has only runtime libraries.
- `apt-get upgrade` runs in both stages (Trivy gate), and the system `setuptools`/`msgpack` are patched.
- Runs as the non-root `appuser` (uid 1000). Gettext catalogs are compiled at build time.
- `HEALTHCHECK` curls `/health/`. The entrypoint is `docker/entrypoint.sh`, and the command is gunicorn with `docker/gunicorn.conf.py`.

### 12.2 Entrypoint (`docker/entrypoint.sh`)

1. Waits for PostgreSQL at `DB_HOST:DB_PORT` (30 s timeout).
2. If `SECRET_KEY` is unset or a known default, generates a random key and persists it in `media/.generated_secret_key`.
3. Compiles `.po` files when their `.mo` is missing (the dev bind-mount case).
4. Unless `HORILLA_SKIP_RELEASE_TASKS=1` (the scheduler container), runs `migrate --noinput` and `collectstatic --noinput --clear`.
5. Execs the command.

### 12.3 Gunicorn and nginx

- **Gunicorn**:
  - `gthread` workers: `GUNICORN_WORKERS`, or `cpu*2+1` capped at 8 with a minimum of 2; 4 threads each
  - 120 s timeout; worker recycling after 1,000 requests (with jitter)
  - access logs to stdout
- **nginx** (`docker/nginx.conf`):
  - serves `/static/` with immutable caching; proxies everything else, including `/media/` (auth-checked)
  - 50 MB upload limit; security headers (nosniff, SAMEORIGIN, referrer policy)
  - a login rate limit of 5/min (burst 10, HTTP 429); `/metrics/` denied

### 12.4 Production stack

```bash
cp .env.dist .env       # set SECRET_KEY, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, DATABASE_URL,
                        # DB_INIT_PASSWORD, REDIS_URL (and SECURE_SSL_REDIRECT behind TLS)
make prod               # docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```

- The prod overlay sets `DEBUG=0` and `HORILLA_ENV=production`, which turns on the security gate. It removes the source bind mount (**rebuild to deploy code changes**) and starts nginx.
- Needs Docker Compose v2.24+ (for `!override`/`!reset`).
- **Scale `web` freely. Keep `scheduler` at exactly one replica.**
- **Probes**:
  - `/health/`: liveness, with no dependencies
  - `/ready/`: checks the DB and Redis, and reports the scheduler
  - `/metrics/`: Prometheus, staff only
- **Configuration** (`.env.dist`): `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `TIME_ZONE`, `HORILLA_ENV`, `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS`, `DB_INIT_PASSWORD`, `DATABASE_URL`/`DB_*`, `REDIS_URL`, `GUNICORN_*`, `HORILLA_REQUIRE_SCHEDULER`, `AWS_*`/S3 or GCS storage, `SENTRY_DSN`, the `AXES_*` limits, the `THROTTLE_*` rates and `SESSION_COOKIE_AGE`.
- **Template cache**: in production the cached template loader is on, so template edits need a restart or redeploy.

### 12.5 This server's setup (local, uncommitted changes)

This checkout has local modifications for the host it runs on:
- `docker-compose.prod.yml` (modified):
  - uses the host's existing PostgreSQL and Redis at `172.17.0.1` instead of the bundled `db`/`redis`; those only run with `--profile bundled-db`
  - adds `restart: unless-stopped` to web
  - publishes nginx on host port **1000**, which a Cloudflare Tunnel points at
- `deploy.sh` (untracked):
  - `./deploy.sh init-env <domain>` writes a production `.env` with random secrets
  - `./deploy.sh setup-db` creates the DB user and database inside the `postgres_db` container
  - `./deploy.sh` checks `.env`, takes a `pg_dump -Fc` backup into `backups/` (skip with `--skip-backup`), builds, starts and waits for the web container to be healthy
  - `status`, `logs`, `stop`
- `backups/` (gitignored) holds the DB dumps and `.env` copies made by `deploy.sh`.

---

## 13. Observations from the review

These are things noticed while reading the code. They were not changed.

1. **Two jobs bypass the single-scheduler design.**
   - `horilla_backup/scheduler.py` starts its own `BackgroundScheduler` from the Google Drive setup view, so it runs inside a gunicorn worker. It doesn't survive a restart, and it can run in more than one worker.
   - `biometric_device_schedule` (`biometric/views.py` ~L431–480) also starts an in-process scheduler, on top of the central `biometric.poll_devices` job, so a device can be polled twice.
2. **`recruitment_close` uses a stale date.**
   - `today = datetime.now()` is set once, at module import (`recruitment/scheduler.py:9`). Inside the long-running `run_scheduler` process that date never advances.
   - The job also matches `end_date == today_date`, so a missed day is never closed. Recruitments may stay open past their end date.
3. **Auto payslip recomputes mid-period joiners on every run.**
   - `generate_payslip` checks for an existing payslip by `start_date=period_start`, but saves it with `start_date=max(period_start, contract_start)`.
   - For an employee whose contract started mid-period, the check never matches. Each 3-hourly run on the generate day recomputes that payslip and resets its status to `draft`.
4. **Some test suites are not in CI.** `master_import` (132 tests), `horilla/tests` (37) and `notifications` (31) are not in `SMOKE_LABELS`, so `make test-smoke`/CI don't run them.
5. **`ACCRUAL_PLAN`** is defined in `leave/models.py` but not used. There is no leave-accrual feature, only resets and carry-forward.
6. **A docstring says "Django 6.x compatible"** (`horilla_dbtemplate/conf.py`, `horilla/inherit/autodetect.py`), while the requirements pin Django 5.2.
7. **The API schema advertises "BSD License"** (`horilla_api/urls.py`), while the project is LGPL-2.1.
