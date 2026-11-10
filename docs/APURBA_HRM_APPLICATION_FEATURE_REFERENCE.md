# Apurba HRM v2 — Complete Application Reference

> Generated 2026-11-04 from a full read of the source tree on branch `master` (HEAD `6dd2884`).
> Route counts come from importing the live FastAPI app and walking `app.routes`, not from grep.
> Business rules were taken from the code and spot-checked against it; where this document and
> an older file in `docs/` disagree, **the code wins** and the difference is listed in
> [§12 Known gaps & documentation drift](#12-known-gaps--documentation-drift).

## Contents

1. [What the application is](#1-what-the-application-is)
2. [Architecture & code layout](#2-architecture--code-layout)
3. [Feature catalogue (at a glance)](#3-feature-catalogue-at-a-glance)
4. [Business logic layer](#4-business-logic-layer)
5. [UI / UX layer](#5-ui--ux-layer)
6. [Data layer](#6-data-layer)
7. [Schedulers & cron jobs](#7-schedulers--cron-jobs)
8. [Integrations](#8-integrations)
9. [Running the application](#9-running-the-application)
10. [Testing](#10-testing)
11. [Deployment](#11-deployment)
12. [Known gaps & documentation drift](#12-known-gaps--documentation-drift)
13. [Appendix A — Complete route inventory](#appendix-a--complete-route-inventory-generated-from-the-live-fastapi-app)

---

## 1. What the application is

**Apurba HRM Suite v2** (`hrm_v2`, API title "HRM System API", version `2.0.0`) is an internal
Human Resource Management system for ApurbaTech, deployed at `hrm.apurbatech.io`. It is a
**server-rendered FastAPI monolith**: one Python process serves both the HTML pages (Jinja2) and
the JSON API that those pages call.

| Aspect | Value |
|---|---|
| Language / runtime | Python (Docker image: 3.11-slim; local `.venv`: 3.12) |
| Web framework | FastAPI 0.128, Starlette 0.50, Uvicorn 0.40 |
| Database | PostgreSQL via SQLAlchemy 2.0.45 (`psycopg2-binary`) |
| Schema management | Alembic 1.20 + hand-maintained per-table SQL under `db/schema/` |
| Cache | Redis (optional; the app runs without it) |
| Scheduler | APScheduler 3.10.4 `BackgroundScheduler`, in-process |
| Auth | JWT (python-jose) in an HttpOnly cookie or Bearer header; bcrypt; Google OAuth2 |
| Files | External file service (`fs.apurbatech.io`, MinIO presigned URLs) |
| Reports | openpyxl (Excel), PDF export for attendance directory |
| Default timezone | `Asia/Dhaka`, overridable per employee |
| Users | Three practical types: **Employee**, **Admin**, **Super Admin** (derived from roles) |

Scale of the codebase: ~32.6 k lines in the core layers (routers, services, repositories, cron,
middleware, auth, utils), **518 registered routes** (86 HTML pages + 430 API/other + 2 framework),
**67 database tables**, 3 views, 6 DB functions/triggers, 10 scheduled jobs + 1 unscheduled job.

---

## 2. Architecture & code layout

### 2.1 Request flow

```
Browser / API client / SenseFace device
        │
        ▼
Uvicorn (4 workers in Docker)
        │
        ├─ CORSMiddleware            (allow_origin_regex=".*", credentials allowed)
        ├─ ActivityLoggerMiddleware  (logs API requests/responses to activity_log, masks secrets)
        ├─ OnboardingCheckMiddleware (redirects HTML pages to the questionnaire until completed)
        │
        ▼
Router (routers/*, pages/*)          ← auth dependency: require_roles / require_permission / *_html
        │
        ▼
Service (services/*)                 ← business rules, orchestration, emails
        │
        ▼
Repository (repositories/*)          ← SQLAlchemy queries, ledger writes
        │
        ▼
ORM models (db_models/*) ─► PostgreSQL           Redis (dashboard cache)
```

### 2.2 Directory map

| Path | Purpose |
|---|---|
| `fastapi_app/main.py` | App factory, lifespan (startup/shutdown), middleware, router wiring, ~34 top-level page routes |
| `fastapi_app/config.py` | `Settings` (pydantic-settings, reads `.env`) |
| `fastapi_app/database.py` | Engine (`pool_size=10`, `max_overflow=20`, `pool_pre_ping`, `pool_recycle=3600`), `SessionLocal`, `get_db`, `init_db` |
| `fastapi_app/scheduler.py` | APScheduler setup, lock-file ownership, job control helpers |
| `fastapi_app/constants/` | `scheduler_shifts.py` (shift IDs per job), `leave_filters.py` |
| `fastapi_app/auth/` | JWT, bcrypt, dependency guards (`utils.py`), login / Google / OTP endpoints (`routers.py`) |
| `fastapi_app/routers/<domain>/` | JSON APIs, grouped by domain (see Appendix A) |
| `fastapi_app/pages/` | HTML-only handlers (return `TemplateResponse`), split out of routers |
| `fastapi_app/services/` | Business logic per domain (`leave.py` 1.8k lines, `attendance.py` 1.6k, `employees.py`, `extra_work.py`, `wfh.py`, `approvals.py`, `dashboard.py`, `rbac.py`, `calendar_service.py`, `hrm_ai.py`, …) |
| `fastapi_app/repositories/` | Data access per domain (`attendance.py` 2.1k lines, `employees.py`, `leave.py`, `leave_ledger.py`, …) |
| `fastapi_app/db_models/` | **The real ORM models**, by domain (attendance, leave, employees, rbac, master_data, extra_work, wfh, approvals, question_builder, settings, misc, integrations). `payroll/` is an empty package. |
| `fastapi_app/schemas/` | Pydantic request/response models **plus backward-compat shims** that re-export ORM classes from `db_models` (e.g. `schemas/leave/approval.py`) |
| `fastapi_app/models.py` | Compatibility shim; imports every ORM class so mappers register |
| `fastapi_app/cron_jobs/` | Job bodies (importable *and* runnable as scripts) |
| `fastapi_app/middleware/` | `activity_logger.py`, `onboarding_check.py`, `exception_handler.py` |
| `fastapi_app/utils/` | email, timezone, holiday, Redis cache, encryption, RBAC audit, cron logger/utils, URL helpers |
| `fastapi_app/file_upload_api/` | Profile-photo upload/download via the external file service |
| `fastapi_app/routers/SenseFace_2A/` | ZKTeco ADMS receiver for biometric terminals |
| `fastapi_app/templates/` | Primary Jinja templates (43 entries, incl. `question_builder/`) |
| `templates/` (repo root) | Legacy Jinja templates (27 files), served by the "legacy root" template engine |
| `static/` | CSS, JS, icons, PWA manifest and service worker |
| `db/` | Alembic migrations (`db/migrations`), current schema as SQL (`db/schema`), `build_schema.sh` |
| `scripts/db/` | `check_schema.sh`, `check_orm.py`, `split_schema.py` |
| `docs/` | 45+ design/ops documents (including `ATTENDANCE_CLAIM_FLOW.md`, which `CLAUDE.md` requires to be kept current) |
| `tests/` | Pytest unit tests plus many ad-hoc/diagnostic scripts |
| `cron_logs/`, `logs/` | Runtime log output (git-ignored) |

### 2.3 Application startup (`lifespan`)

1. `init_db()` — imports models; runs `Base.metadata.create_all()` **only if** `AUTO_CREATE_TABLES=true`.
2. `create_admin_user()` — if no user named `admin` exists, creates `admin / admin123`
   (`admin@hrm.local`), assigns the `ADMIN` role and an "System Admin" employee profile.
3. `initialize_master_data()` — currently a no-op (seed lists are empty/commented out).
4. `get_redis()` — opens the Redis connection; non-blocking if Redis is down.
5. `start_scheduler()` — one worker acquires the lock file and starts APScheduler.
6. `_log_leave_report_status()` — logs whether this month's negative-leave email has been sent.

On shutdown the scheduler is stopped and the lock file removed.

### 2.4 Layering conventions

- **Routers → services → repositories → models.** Routers should hold no business rules.
- **Route prefix convention.** Many features expose three parallel URL families —
  `/admin/…`, `/super_admin/…`, `/employee/…` — that call the *same* handler logic. The prefix
  selects the page chrome; the actual access control is the permission/role dependency.
- **Legacy routers.** `routers/*/legacy.py` (attendance, leave, employees, extra_work) keep older
  endpoints with simple `ADMIN`/`HR`/`MANAGER` role checks; the approver-based flows are the main path.
- **Error handling.** `middleware/exception_handler.py` converts `HTTPException`, validation errors
  (422) and unhandled exceptions (500) into a uniform JSON body with a numeric `errorCode` and a
  request id; HTML requests get `error.html`/`unauthorized.html`.

---

## 3. Feature catalogue (at a glance)

| # | Module | What it does | Primary audience |
|---|---|---|---|
| 1 | **Authentication** | Email+password login, Google sign-in, OTP password reset, change password, logout | Everyone |
| 2 | **RBAC** | Roles, permissions, user-role mapping, super-admin flag, management UI, audit log | Super Admin |
| 3 | **Onboarding questionnaire** | Gate: users must pass active MCQ/typed questions before using the app; admin question builder | Everyone / Admin |
| 4 | **Employee management** | Create / list / edit / delete employees, profile & photo, hierarchy, reporting managers, shift swap | Admin |
| 5 | **Employee self-service** | Dashboard, profile edit, photo, blood group, birthdays, activity | Employee |
| 6 | **Attendance** | Clock in/out, status calc, today's edit, history, analytics, admin edit/directory, PDF export, work-hours report | Employee / Admin |
| 7 | **Attendance claims** | Fix a missed punch; monthly quota; cutoff; multi-level approval; ledger refund | Employee / Approvers |
| 8 | **Leave management** | Apply, half-day, overlap rules, balances, history, cancellation workflow, leave-on-behalf, edit | Employee / Approvers / Admin |
| 9 | **Leave balance ledger** | Append-only ledger of every balance change with source and actor | System / Admin |
| 10 | **WFH requests** | Request, approve, edit, cancel; unlocks "Home" clock-in | Employee / Approvers |
| 11 | **Extra work (overtime)** | Auto/created on holidays/weekends or long days; approval grants compensatory leave | Employee / Approvers |
| 12 | **Approval engine** | Per-employee, per-type, multi-level approvers; inboxes; histories; bulk assignor; approver history | Approvers / Admin |
| 13 | **Utilities / master data** | Departments, designations, teams, offices, shifts, work locations, office IPs, holiday sets, weekends, working-day exceptions, leave balances, claim limits, restrictions, email & SMTP config, timezones | Admin |
| 14 | **Reports** | Daily/monthly/summary attendance, leave-record report + reconcile, work-hours, negative-leave Excel, work-deficit | Admin |
| 15 | **Evaluations** | Periodic employee evaluations; AI-powered commit-quantity evaluation proxy | Admin |
| 16 | **Dashboards** | Employee, Admin and Super-Admin dashboards (stats, on-leave, holidays, birthdays) | All |
| 17 | **Google Calendar** | Connect account, create/update/delete meetings, conflicts, best-time finder, templates, holiday import | Users with `meeting.*` |
| 18 | **Biometric attendance** | ZKTeco SenseFace 2A ADMS push receiver | Devices |
| 19 | **External API** | `GET /api/external/attendance/summary` with HTTP Basic auth | Other systems |
| 20 | **Scheduler** | 10 in-app jobs (reminders, absent marking, penalties, monthly reports) + admin page | System / Super Admin |
| 21 | **Notifications** | Email for every request/decision, reminders, OTP, reports; per-event recipient config; email log | System |
| 22 | **Audit & logging** | `activity_log` (API traffic), `rbac_audit_log`, `attendance_audit_log`, `question_audit_log`, `email_log`, `cron_log` | Admin |
| 23 | **PWA** | Installable web app (manifest + service worker) | Mobile users |

---

## 4. Business logic layer

### 4.1 User types and landing pages

| User type | Determined by | Lands on after login |
|---|---|---|
| Super Admin | Any role with `is_super_admin = true` | `/super_admin/dashboard` |
| Admin | Role `ADMIN` | `/admin/dashboard` |
| Employee | Role `EMPLOYEE` (or any other role) | `/employee/dashboard` |

Redirect priority is Super Admin → `EMPLOYEE` → `ADMIN` → employee dashboard, so a user holding
both `EMPLOYEE` and `ADMIN` lands on the employee dashboard. If any active onboarding question
exists and the user has not completed them, the landing page is overridden to
`/onboarding/questionnaire`. Every person is an employee first: approving, clocking in or applying
for leave all require an `employee_info` profile linked to the user.

### 4.2 Authentication & account

| Feature | Rule |
|---|---|
| Password login | `POST /api/auth/login`; bcrypt (12 rounds); one generic "Invalid email or password" error for unknown email *and* wrong password |
| Session | JWT (`HS256`) carrying `sub`, `username`, `email`, `role[]`, `is_super_admin`, `exp`. Delivered as HttpOnly cookie `auth_token` (`secure` unless `DEBUG`, `samesite=lax`, `path=/`) and in the JSON body. **Login issues a 30-day token** (`_build_session`), overriding the 24 h `JWT_ACCESS_TOKEN_EXPIRES` default |
| Google sign-in | `/api/auth/google/auth-url|login|callback|complete`; HMAC-signed `state` (10 min max age); same session + redirect logic as password login |
| Forgot password | `POST /api/auth/forgot-password` → 6-digit OTP e-mailed, valid **15 minutes**, new OTP invalidates earlier unused ones; response never reveals whether the e-mail exists |
| Verify OTP / reset | `POST /api/auth/verify-otp`, `POST /api/auth/reset-password` |
| Change password | Requires the current password; new password must differ |
| Logout | `POST /api/auth/logout` clears the cookie |
| External summary API | HTTP Basic using `ATTENDANCE_SUMMARY_API_USERNAME/PASSWORD` from `.env` — not JWT |
| Sensitive data | National ID and TIN are encrypted at rest (`utils/sh_encryption.py`) |

### 4.3 RBAC (access control)

**Tables:** `permission` (unique `code`, `module.action` form), `permission_group` / `permission_group_map`
(UI grouping only — no effect on checks), `role` (`is_super_admin`), `role_permission_map`, `user_role_mapping`.

**Evaluation rules**

1. A user's effective permissions are the **union** over all roles. There are no deny rules.
2. Any role with `is_super_admin = true` makes the user a Super Admin; every check passes.
3. Codes match exactly (`leave_request.edit` does not imply `leave_request.view`).
4. A permission opens the page/API; it does **not** widen the data. Approval inboxes are additionally scoped by approver assignment (§4.9).

**Guards** (`auth/utils.py`)

| Guard | Source of truth | Failure |
|---|---|---|
| `require_roles([...])` | roles in the **JWT** (role changes need re-login) | 403 |
| `require_permission(code)` | **DB**, per request (changes apply immediately); Bearer only | 403 `PERMISSION_DENIED` |
| `require_permission_flexible(code)` | DB; Bearer **or** cookie (used by browser-page API calls) | 403 |
| `require_any_permission` / `require_all_permissions` | DB | 403 |
| `require_*_html` family (`require_roles_html`, `require_permission_html`, `require_super_admin_html`, `require_exact_role_html`, `require_onboarding_complete_html`, `require_authenticated_html`) | JWT (+DB for permissions) | **303 redirect to login** |
| `require_exact_role_html(role)` | URL prefix enforcement: `/super_admin/*`, `/admin/*`, `/employee/*` | 303 |

**Permission codes found in the code:** `employee.{view,create,edit,delete}`,
`employee_attendance_directory.{view,edit}`, `employee_attendance_history.view`,
`leave_request.{view,edit,clear,create_on_behalf}`, `leave_cancellation.clear`,
`wfh_request.{view,edit,clear}`, `extra_work.{view,approve,clear}`,
`attendance_claim.{view,approve,clear}`, `bulk_approval_assignor.manage`,
`utilities_dashboard.{view,manage}`, `restrictions.{view,create,edit,delete}`,
`question_builder.{view,create,edit,delete}`, `commit_evaluation.view`,
`meeting.{view,create,edit,delete}`, `rbac.audit_logs.view`, `module.view`, `report.view`.
Roles and permissions are data (managed in the RBAC UI); the list above is what the code *checks*.

**RBAC audit log** (`rbac_audit_log`): records successful use of a permission for meaningful actions
(`VIEW`, `CREATE`, `EDIT`, `DELETE`, `CLEAR`, `APPROVE`, `REJECT`, `ACCESS`) with actor, target
entity, old/new value, IP, user agent and success flag. It does **not** log every 403 denial.
Viewing/clearing needs `rbac.audit_logs.view`.

RBAC management (permissions, roles, role↔permission, user↔role) is Super Admin only; a role
cannot be deleted while users are assigned to it. `role.status` is not part of evaluation.

### 4.4 Onboarding gate

- Super/admin users maintain questions (MCQ or type-based) in the **Question Builder**:
  create/edit/delete, reorder, activate/deactivate, stats, audit log (`question_audit_log`).
- Type-based answers support `case_sensitive`, `trim_whitespace`, `allow_partial_match`.
- Users answer in `/onboarding/questionnaire`; attempts are stored in `user_question_responses`
  (with `attempt_number`) and progress in `user_onboarding_status`. `incorrect-questions` lets a
  user retry only wrong answers.
- `OnboardingCheckMiddleware` redirects **every HTML page** to the questionnaire while
  `all_questions_completed = false`. Exempt: `/login`, `/logout`, `/`, `/forgot-password`,
  `/verify-otp`, `/reset-password`, `/onboarding/questionnaire`, `/health`, `/url`, and prefixes
  `/api/`, `/static/`, `/photo_uploads/`, `/onboarding/api/`.

### 4.5 Employee management

- **Create** (`employee.create`): username, e-mail, password, role, first/last name, employee code,
  gender, personal e-mail/phone, office, designation, **leave type** are required. Uniqueness is
  enforced on username, e-mail, employee code, company e-mail and personal e-mail. Creates user +
  profile + role + approvers + leave balance; default `total_paid_holiday = 15`; a confirmation
  page/e-mail follows. `probation_timeline` is kept only when the employment period is probation.
- **Probation auto-promotion:** `utils/sh_probation_check.py` lazily promotes an employee to
  Full-Time once `probation_timeline` has passed.
- **List / search / edit / delete** (`employee.view|edit|delete`), photo upload, per-employee
  profile page, org **hierarchy** page, **reporting managers** (with level and effective dates),
  **shift swap** between two employees (`/api/swap_shift/*`).
- **Self-service edit** is restricted to an allow-listed set of fields (not designation, salary,
  shift, etc.). Photos go through the external file service (§8.3).
- **Evaluations:** admins record an evaluation, set an interval and a next-evaluation date,
  list history and see dashboard stats (`/api/evaluations/*`). Separately, `commit_evaluation`
  proxies to the **HRM AI engine** (`GET {HRM_AI_BASE_URL}/…`, timeout `HRM_AI_TIMEOUT_SECONDS`) and maps
  upstream failures to 502/504.

### 4.6 Attendance

**Time model.** "Today" is computed in the **employee's timezone**; times are stored as naive UTC.
A working day is a day that is not a weekend for the employee's holiday set, not a holiday in that
set, unless a `working_day_exception` exists.

**Clock-in rules (in order)**

1. Time is interpreted in the employee's timezone and stored in UTC.
2. **Holiday/weekend clock-in = Extra Work.** The user is asked to confirm; confirming creates a
   pending Extra Work request instead of a normal attendance row. A previously rejected request
   asks for confirmation to resubmit; pending/approved blocks a second clock-in (use update).
3. **Approved full-day leave today:** confirmation required; confirming clocks in and files a leave
   cancellation request for that day.
4. **Work location "Home"** (`requires_wfh_approval`): allowed anytime for `wfh_eligible` employees,
   otherwise only with an APPROVED WFH request covering today.
5. **Office locations need an office IP** (`is_office_location`); the client IP must be in the active
   `ip_address` list. The client IP is now stored in `attendance.ip_address` (migration 0004).
6. No shift assigned → blocked.
7. **Clock-in window** (attendance restriction ON and on office IP): cannot back-date earlier than
   *now − `shift.clock_in_threshold_minutes`*.
8. One clock-in per day; a second attempt must use "update".

**Status at clock-in** (when `attendance_restriction_status` is ON; OFF ⇒ always PRESENT):

| Situation | Status | Side effect |
|---|---|---|
| Approved FIRST_HALF leave | LATE if past half-day threshold, else PRESENT | remark "first halfday request approved" |
| Pending FIRST_HALF leave | LATE if past normal cutoff, else PRESENT | remark |
| After half-day threshold (shift midpoint + late_threshold/2) | LATE | remark "first halfday absent"; **0.5 day deducted** |
| Otherwise | PRESENT if ≤ shift start + `late_threshold_minutes` (default 60), else LATE | SECOND_HALF leave noted in remark |

A DB trigger (`fn_recalculate_attendance_status`) recomputes PRESENT/LATE whenever `clock_in_time`
changes (never overriding ABSENT / ON_LEAVE).

**Clock-out rules.** Must have clocked in; one clock-out per day; must be after clock-in (an earlier
time is treated as next day if the span is 1–18 h); **max span 18 h**; with restriction ON on office
IP it cannot be further than `clock_out_threshold_minutes` in the future. On holidays/weekends it
updates the Extra Work request; if a leave cancellation is pending the times are stored there.

**Update today's attendance** (`PUT /api/employee/attendance/today`): denied for
restriction-ON employees ("contact your supervisor") **unless** today's location is a non-office
location. Per recent commits, employees not WFH-eligible by config but working from home through an
approved WFH application can update their clock-out time via this endpoint.

**Admin attendance.** Directory (`employee_attendance_directory.view|edit`) with page-data, edit,
and **PDF export**; per-employee history, analytics and work-hours (`employee_attendance_history.view`);
admin work-hours report (`/api/employees-work-hours`); legacy admin CRUD (`/api/admin/attendance/*`).
Changes to `attendance` are written to `attendance_audit_log` by the `audit_attendance_changes`
trigger. `total_work_duration` is kept in sync by triggers (insert/update/delete cascade).

**Attendance statuses** (`attendance_status_enum`): `PRESENT, ABSENT, EXTRA_WORK, ON_LEAVE, LATE,
OFF_DAY, SIGNED_IN, ATTENDANCE_CLAIM_PENDING`.

**Biometric.** SenseFace 2A terminals push punches to `/iclock/cdata`; device PIN must equal
`employee_code`. Punches are logged in `attendance_sync_log` and used to set clock times
(see §8.2).

### 4.7 Attendance claims

Full flow lives in `docs/ATTENDANCE_CLAIM_FLOW.md` (mandatory to update on any change). Summary:

- **Submit** (`POST /api/employee/attendance/claim`): date, start, end, reason. Checks in order:
  profile + max-claim config exist → filed on/before `claim_cutoff_day` (default **5**) of the month
  after the claim month → claim date's shift already ended → monthly quota (`max_claim_count`,
  default **2**) → one claim per date, end after start. Source time zone precedence: offset in
  string → `request.timezone` → employee zone → `DEFAULT_TIMEZONE`; stored as naive UTC.
- The day's attendance becomes `ATTENDANCE_CLAIM_PENDING`; `current_count` increments; approvers are e-mailed.
- **Decide** (`POST …/attendance_claim_request/approval/{id}/action`, actions `approve|reject|remark`):
  Level-1, Super Admin or an `attendance_claim.approve` holder finalizes; Level 2+ is advisory.
  - *Approve:* claim `APPROVED`; attendance → `PRESENT` with claimed times; ledger `CLAIM_APPROVED`
    (available +1, redeemed −1 — reverses the absent penalty).
  - *Reject:* claim `REJECTED`; attendance → `ABSENT`; if previously approved, ledger `CLAIM_REVERSED`;
    the monthly count is refunded.
- Deleting a PENDING claim resets attendance to `ABSENT` and a DB trigger decrements the count.

### 4.8 Leave management

**Applying** (`POST /employee/leave-request/submit`)

- **Probation employees cannot apply** (HR creates leave on their behalf).
- Needs leave type, dates, and an **emergency contact** (another active employee); end ≥ start.
- **Working days only** — weekends/holidays are excluded; zero working days is rejected.
- Single-day requests may be `FULL_DAY`, `FIRST_HALF`, `SECOND_HALF` (0.5 day).
- Overlap with any pending/approved leave is blocked, except one FIRST_HALF + one SECOND_HALF on the same day.
- Status starts `PENDING`; **balance is deducted on approval, not at submission**.

**Cancelling:** PENDING → employee cancels directly (`CANCELLED`). APPROVED full-day → employee files a
**leave cancellation request** (one pending per leave), reviewed in the cancellation inbox; approval
re-derives that day's attendance from recorded clock times and deletes attendance for the remaining
future days. Approved half-day leave needs no cancellation.

**Approval effects**

- Approved: `redeemed += days`, `available −= days` (skipped for **Unpaid Leave**; probation rule
  deducts only `available_leave`), a ledger row is appended, attendance rows created/updated.
- Approved → rejected later: balance restored, attendance reverted.
- **Edit** (`leave_request.edit` or Super Admin): old effects reversed, approvals reset, status back to PENDING with recomputed days.
- **Create on behalf** (`leave_request.create_on_behalf`): immediately APPROVED, balance + attendance updated, e-mail sent.
- Late approval of leave that was already penalised as absent: the system flips ABSENT → ON_LEAVE and
  reverses the penalty (`utils/sh_leave_attendance_utils.py`).

**Ledger.** Every balance change goes through `repositories/leave_ledger.apply_balance_change` /
`record_balance_set` / `record_balance_removed`, writing `leave_balance_ledger` with `event_type`,
deltas, old/new available, `source_type/source_id`, attendance date and actor. Event types
(`LeaveLedgerEvent`, `schemas/enums.py`): `LEAVE_APPROVED`, `LEAVE_REVERSED`, `LEAVE_EDIT_REVERT`,
`LEAVE_ADMIN_CREATE`, `LEAVE_CANCELLED_BY_ATTENDANCE`, `LEAVE_ATTENDANCE_ABSENT_CANCEL`,
`CLAIM_APPROVED`, `CLAIM_REVERSED`, `EXTRA_WORK_APPROVED`, `EXTRA_WORK_REVERSED`, `ABSENT_PENALTY`,
`HALF_ABSENT_PENALTY`, `LATE_PENALTY`, `HALFDAY_LATE_CLOCKIN`, `HALF_LEAVE_REJECTED`,
`ADMIN_ADJUSTMENT`, `CARRY_FORWARD`, `INITIAL_ALLOCATION`, `MIGRATION_BASELINE`.
Penalties are **idempotent per employee and date**. The balance row to charge is chosen by
`resolve_balance`: the requested leave type, otherwise the lowest `leave_type_id` of the year
(deterministic `ORDER BY`).

### 4.9 Approval engine

Applies to Leave, Attendance Claims, Extra Work and WFH (WFH reuses the leave approver list; leave
cancellation is a simpler single-step admin action).

- **Approver configuration:** per employee and per type — `leave_approval`, `attendance_claim_approval`,
  `extra_work_approval` — each row has `approval_level` (1,2,3…), `effective_from/to`, `is_active`.
  Set at employee creation, from the employee record, or in bulk with the **Bulk Approval Assignor**
  (check-existing / replace / merge).
- **Inbox visibility:** Super Admin sees everything; everyone else (including Admins with `*.view`)
  sees only requests from employees for whom they hold an **active** approver row of the matching
  type. No assignment ⇒ empty inbox (not an error).
- **Who finalizes:** Level-1 approver or Super Admin (or an `*.approve` holder for claims / extra work).
  Level 2+ decisions/remarks are recorded as advisory only. Once a Super Admin has acted, only a
  Super Admin (or `*.approve` holder) can change the final status. A normal approver cannot change
  their own decision; Super Admin can.
- **Actions:** `approve`, `reject`, `remark` (remark needs text). Optional e-mail to the employee;
  reversals are labelled as such. Each finalizing action is written to the RBAC audit log.
- **History:** `leave_approvers_history`, `attendance_claim_approvers_history`,
  `extra_work_approval_history`, `wfh_approval_history`; combined view at the Approver History page.
- **Categories:** `approval_request` rows describe approval types; `/api/approval-categories` exposes them.

### 4.10 WFH requests

Any employee submits a date range (optional half day), reason (≤1000 chars) and optional attachment.
Same working-day rule as leave. Conflicts: blocked if it overlaps another pending/approved WFH or any
pending/approved leave. The owner can cancel or edit **only while PENDING** (an edit resets approvals).
Approved WFH is what lets a non-eligible employee choose the Home location on clock-in. No balance change.

### 4.11 Extra work (overtime)

- Created when an employee clocks in on a holiday/weekend and confirms, **or** automatically by the
  23:59 job when a normal-day span exceeds **1.5 × shift length** (not Home) — a 0.5-day request.
- Approver must pick `FULL_DAY | FIRST_HALF | SECOND_HALF`; approval sets attendance to `EXTRA_WORK`
  with the recorded times and credits **+1 / +0.5 day** to `achieved_leave` and `available_leave`
  (compensatory leave). Changing the type adjusts by the delta; rejection removes the generated
  attendance and reverses the credit (never below 0).
- Directory page for admins (`/admin/extra_work_directory`) lets them edit records.

### 4.12 Utilities / master data (system configuration)

Gated by `utilities_dashboard.view` (read) and `.manage` (write); restrictions by `restrictions.*`.

| Area | Configurable items |
|---|---|
| Organisation | departments, designations, teams (with lead), offices |
| Shifts | start/end, break, late threshold, clock-in/out thresholds, clock-out penalty, shift timezone, minutes that equal one leave day (`duration_for_one_leave`, default 540), reminder/cron times (`cron_job_time`, `cron_reminder_mail_minutes`, `cron_autoclockout_mark_absent`, `cron_weekly_penalty_time`) |
| Locations | work locations (`is_office_location`, `requires_wfh_approval`, icon, order), office IP addresses (IPv4/IPv6, active flag) |
| Calendars | holiday sets, yearly holidays, weekends (per set), working-day exceptions, Google public-holiday import per country |
| Leave | leave types, leave balances per employee/year (manual adjustment), max-claim config (per-month quota + cutoff day) |
| Restrictions | per employee: `attendance_restriction_status` (default ON), `email_restriction_status` (default ON), `wfh_eligible` (default OFF) |
| Messaging | e-mail configs (To/CC/BCC per event, optionally per department), SMTP account (`email_hrm`) with test-send, timezones |
| Onboarding | per-user onboarding status (edit/reset/delete) |

### 4.13 Reports & dashboards

- **Employee dashboard** (`/api/employee/dashboard/*`): stats, who's on leave, recent activity,
  birthdays this month, clock status, monthly work hours, yearly attendance. Redis-cached; caches are
  invalidated on attendance/leave/claim changes.
- **Admin / Super Admin dashboards**: data, quick stats, on-leave, (super) upcoming holidays and
  question-builder stats.
- **Attendance reports** (`/api/admin/attendance/reports/daily|monthly|summary`).
- **Leave-record report** (`/api/reports/leave-record/monthly|entries|reconcile`) built from the ledger.
- **Excel e-mail reports** from cron jobs (negative leave, work hours).
- **Work-deficit** tracked in `work_deficit` (expected vs actual minutes, penalty).

### 4.14 Notifications

E-mail is sent for: leave created/approved/rejected/cancelled, cancellation requested, claim
submitted/decided, extra work requested/decided, WFH submitted/decided, clock-in reminders, monthly
reports, OTP, new-employee confirmation. Recipients come from `email_config` (per event, optionally
per department); `email_restriction_status` suppresses reminders per employee. Failures are logged
and never block the primary action. Every send is recorded in `email_log` (`utils/email_log_util.py`).

### 4.15 Constraints (what is *not* possible)

| Not allowed | Reason |
|---|---|
| Probation employee applies for leave | Must go through HR on-behalf creation |
| Leave/WFH with only weekends/holidays | Zero working days rejected |
| Overlapping leave, or leave overlapping WFH | Blocked (only FIRST_HALF + SECOND_HALF pairing) |
| Self-cancel approved full-day leave | Needs cancellation request |
| Cancel/edit own WFH once decided | Only PENDING |
| Clock in at an office location off-network | Office-IP check |
| Choose Home without eligibility/approved WFH | Blocked |
| Clock in/out twice | Use update (blocked for restricted employees on office locations) |
| Shift span > 18 h | Clock-out rejected |
| Claim after cutoff day / beyond monthly max / duplicate date | Blocked |
| Approve without being the employee's approver | 403 unless Super Admin |
| Level 2+ changing final status; approver changing own decision | Advisory / Super Admin only |
| Manage roles, permissions | Super Admin only |
| Use any page before finishing onboarding | Middleware redirect |
| Approve extra work without picking the day type | `half_day_type` mandatory |

---

## 5. UI / UX layer

### 5.1 Rendering model

Server-rendered **Jinja2** pages with vanilla JavaScript calling the JSON API via `fetch`
(some pages use axios). There is **no SPA framework and no build step** — everything is loaded from
CDNs and `static/`. Two template engines coexist:

- `fastapi_app/templates/` via `utils/header_logged_template.CustomJinja2Templates`, which
  **auto-injects `logged_in_user`** (`id`, `role`, `roles`, `is_super_admin`, name, photo, timezone)
  into every page context by decoding the auth cookie.
- `templates/` (repo root) via a "legacy root" wrapper that injects `default_timezone`.

Responses carry an `X-Template-Name` header (useful when debugging which template rendered).

### 5.2 Design system

| Aspect | Implementation |
|---|---|
| CSS | Tailwind (CDN `cdn.tailwindcss.com` with forms + container-queries plugins) in newer pages; Bootstrap 5.3 + Font Awesome 6.4 in older ones; hand-written CSS in `static/css/*` (`layout`, `dashboard`, `employees`, `master_data`, `evaluations`, `auth`, `professional`, …) |
| Theme | Primary `#00BFFF` (also the PWA theme colour); Tailwind `darkMode: "class"` with `background-dark #0B1120` |
| Typography | Inter (primary), Manrope/Epilogue/Space Grotesk on some pages |
| Icons | Material Symbols Outlined (newer), Font Awesome (older) |
| Charts | Chart.js 4 (dashboards, attendance history); html2canvas for image export on one page |
| Layout | `base.html` provides a sticky glass-effect header, role-aware nav (admin vs employee links via `logged_in_user.roles`), profile dropdown (shows a "Super" badge), footer with docs links |

### 5.3 Page inventory (by audience)

**Public / auth:** `login`, `forgot_password`, `verify_otp`, `reset_password`, `unauthorized`, `error`,
`extension_privacy_policy` (for the browser extension), `url_list`.

**Employee:** `employee_dashboard`, `ss_attendance` (clock in/out + today), `ss_attendance_claim_history`,
`ss_leave_request`, `ss_leave_request_history`, `ss_yearly-holiday-info`, `employee_profile`,
onboarding questionnaire, claim/leave/WFH/extra-work **inbox & approval** pages under
`/employee/…` for people who are also approvers.

**Admin / Super Admin (`sh_*` = shared HR pages):** `admin_dashboard`, `super_admin_dashboard`,
`sh_all_employees`, `sh_employees_list`, `sh_create_employee` + confirmation,
`sh_employee_attendance_directory`, `sh_all_attendance_history`, `admin_work_hours_report`,
`sh_leave_request_inbox` / `_approval`, `sh_leave_cancellation_inbox`, `sh_attendance_claim_inbox` / `_approval`,
`sh_extra_work_inbox` / `_approval` / `_directory`, `sh_approver_history`, `sh_bulk_approval_assignor`,
`sh_utilities_dashboad` (sic), `restrictions_management`, `admin_question_builder`,
`rbac_management`, `rbac_audit_log`, `cron_management`, `create_meeting`, `evaluations`.

**Legacy root templates:** `dashboard`, `employees`, `hierarchy`, `master_data`, `office_hours_settings`,
`smtp_settings`, `attendance_claims`, `overtime_requests`, `approver_dashboard`, `approvers_management`,
`attendance_reports`, `admin_attendance*`, `clock_in`, `clock_out`, `blood_group_list`, etc.

### 5.4 Interaction patterns

- **Role-prefixed URLs** (`/admin`, `/super_admin`, `/employee`) with `require_exact_role_html` enforcing the prefix.
- **Inbox → detail → action** pattern for every approval type: list page loads `…/inbox/data`; detail page
  loads `…/approval/{id}/data`; actions post to `…/approval/{id}/action` with `approve|reject|remark`.
- **Page-data endpoints** (`/api/.../page-data`) return everything a page needs in one call.
- **Confirm-then-submit dialogs** on clock-in for holiday/weekend (extra work) and approved leave (cancellation).
- **Auth failures on HTML routes redirect to login** (303) instead of returning JSON errors.
- **Shared JS helpers:** `static/js/app.js` (core), `auth.js`, `navigation.js`, `modals.js`, `ui-enhancer.js`,
  plus page scripts (`dashboard.js`, `employees.js`, `master_data.js`, `onboarding_questionnaire.js`, …).
  Larger pages inline their JS in the template (e.g. `sh_all_employees.html` ~3.6 k lines).

### 5.5 PWA

`static/manifest.json` ("Apurba HRM Suite", standalone, theme `#00BFFF`, 192/512/maskable icons) and
`static/service-worker.js` (cache `hrm-suite-v1`): precaches `/`, the manifest and favicon; **cache-first
for `/static/*`, network-first for HTML/API**; skips non-GET and cross-origin requests; old caches are purged on activate.

### 5.6 Accessibility / responsiveness notes

Layouts use responsive Tailwind/Bootstrap utilities (mobile nav collapses at the `lg` breakpoint).
No explicit accessibility audit exists in the repo; treat ARIA coverage and contrast as unverified.

---

## 6. Data layer

### 6.1 Database & session handling

- PostgreSQL, SQLAlchemy 2.0 declarative models in `fastapi_app/db_models/**`, `Base` in `db_models/base.py`.
- Engine options: `pool_pre_ping=True`, `pool_recycle=3600`, `pool_size=10`, `max_overflow=20`.
- Per-request session via `Depends(get_db)`; cron jobs open their own `SessionLocal()`.
- `UserAuditMixin` adds `created_by` / `updated_by` FKs to `users`.
- **Timestamps are stored as naive UTC**; conversion to local time happens in `utils/timezone_utils.py`.
- Many history tables define `actioned_by_employee_id` without a DB-level FK (known gap, see `db/README.md`).

### 6.2 Tables (67) by domain

| Domain | Tables |
|---|---|
| **auth_rbac (9)** | `users`, `role`, `permission`, `permission_group`, `permission_group_map`, `role_permission_map`, `user_role_mapping`, `rbac_audit_log`, `password_reset_otps` |
| **employee (7)** | `employee_info`, `restrictions`, `reporting_manager`, `employee_blood_group_list`, `evaluation_history`, `git_username_mapping`, `activity_log` |
| **org (14)** | `department`, `designation`, `team`, `office`, `shift`, `shift_assignment`, `work_location`, `ip_address`, `holiday_set`, `yearly_holiday`, `weekend`, `working_day_exception`, `timezone`, `system_setting` |
| **attendance (11)** | `attendance`, `attendance_audit_log`, `attendance_sync_log`, `total_work_duration`, `work_deficit`, `attendance_claim_request`, `attendance_claim_approval`, `attendance_claim_approvers_history`, `max_claim`, `max_claim_config`, `cron_log` |
| **leave (8)** | `leave_info`, `leave_type`, `leave_balance`, `leave_balance_ledger`, `leave_approval`, `leave_approvers_history`, `leave_cancellation`, `leave_report_run_log` |
| **extra_work_wfh (5)** | `extra_work`, `extra_work_approval`, `extra_work_approval_history`, `wfh_request`, `wfh_approval_history` |
| **approvals (1)** | `approval_request` |
| **onboarding (6)** | `questions`, `question_options`, `question_answers`, `user_question_responses`, `user_onboarding_status`, `question_audit_log` |
| **email (3)** | `email_hrm` (SMTP account), `email_config` (recipients per event/department), `email_log` |
| **calendar (3)** | `google_calendar_config`, `google_calendar_tokens`, `meeting_templates` |

**Key tables in more detail**

| Table | Notable columns / rules |
|---|---|
| `users` | `username`, `email`, `password_hash`, `google_oauth_id` |
| `employee_info` | `user_id` (unique), `employee_code` (unique), names, DOB, `date_of_joining`, `office_id`, `designation_id`, `current_shift_id`, `holiday_set_id`, `primary_team_id`, `department_id`, `timezone_id`, `email_hrm_id`, `status`, `employment_period`, `probation_timeline`, `total_paid_holiday`, `attendance_track`, `national_id`/`tin` (encrypted), `photo_url`, `last_working_day`, `salary_review_date` |
| `shift` | `start_time`, `end_time`, `break_duration_minutes`, `late_threshold_minutes`, `clock_in_threshold_minutes`, `clock_out_threshold_minutes`, `clock_out_penalty`, `timezone`, `duration_for_one_leave`, `cron_job_time`, `cron_reminder_mail_minutes`, `cron_autoclockout_mark_absent`, `cron_weekly_penalty_time` |
| `attendance` | `employee_id`, `attendance_date`, `clock_in_time`, `clock_out_time`, `attendance_status`, `working_from` (→ `work_location`), `remarks`, `ip_address varchar(45)` |
| `leave_balance` | `employee_id`, `leave_type_id`, `year`, `allowed_leave`, `redeemed_leave`, `available_leave`, `achieved_leave`, `carry_forward` |
| `leave_balance_ledger` | `event_type`, `delta_available/redeemed/achieved`, `old_available`, `new_available`, `source_type/source_id`, `attendance_date`, `actor_employee_id`, `actor_user_id` |
| `leave_info` | `leave_start_date`, `leave_end_date`, `no_of_days`, `approval_status`, `half_day_type`, `emergency_contact`, `approved_by` |
| `*_approval` (leave / attendance_claim / extra_work) | `employee_id`, `approver_id`, `approval_level`, `effective_from/to`, `is_active` |
| `*_history` / `*_approvers_history` | one row per approver decision: `approval_status`, `remarks`, `action_taken_at`, `actioned_by_employee_id` |
| `restrictions` | `attendance_restriction_status`, `email_restriction_status`, `wfh_eligible` |
| `max_claim_config` / `max_claim` | `max_claim_count`, `claim_cutoff_day` / per employee-month `current_count` |

### 6.3 Enumerations (PostgreSQL types)

`attendance_status_enum`, `leave_approval_status_enum` (`PENDING, APPROVED, REJECTED, CANCELLED, ADJUST`),
`half_day_type_enum` (`FIRST_HALF, SECOND_HALF, FULL_DAY`), `active_status`, `activestatus`, `gender_types`,
`marital_status`, `blood_group` / `bloodgroup`, `employment_period`, `question_type` (`MCQ, TYPE_BASED`),
`audit_action_type`. Migration 0002 dropped unused enum types. Python-side enums live in
`db_models/enums.py` and `schemas/enums.py` (e.g. `LeaveLedgerEvent`, `RequestStatus`, `DayOfWeek`).

### 6.4 Database objects beyond tables

- **Views:** `v_active_mcq_questions`, `v_active_type_questions`, `v_user_onboarding_progress`.
- **Functions / triggers:** `audit_attendance_changes` (writes `attendance_audit_log`),
  `fn_recalculate_attendance_status`, `update_total_work_duration` / `delete_total_work_duration`
  (keep `total_work_duration` in sync), `decrement_claim_count` (refund quota when a claim row is deleted),
  `update_leave_cancellation_updated_at`.
- **Circular FK** `employee_info.primary_team_id → team` is applied in `900_circular_foreign_keys.sql`.

### 6.5 Schema management & migrations

```
db/
  schema/                 # CURRENT schema, one SQL file per table (hand-maintained)
    000_extensions_and_types.sql   010_functions.sql   800_views.sql   900_circular_foreign_keys.sql
    tables/<domain>/<table>.sql    tables/order.txt (dependency order)
  migrations/             # Alembic
    baseline_20261008.sql (frozen)
    versions/20261008_0001_baseline.py            # loads the frozen baseline
              20261008_0002_drop_unused_enum_types.py
              20261015_0003_wfh_request_reason_1000.py   # reason varchar(500→1000)
              20261017_0004_attendance_ip_address.py     # attendance.ip_address varchar(45)
```

Workflow for a schema change: create a revision (`alembic revision -m "…" --rev-id 000N`), write plain
idempotent SQL with `op.execute`, update the matching `db/schema/tables/<domain>/<table>.sql` (new
columns go at the **end** of `CREATE TABLE`), update the ORM model, run `scripts/db/check_schema.sh`
(files == Alembic == models), then apply. The **live database must be stamped once**
(`alembic stamp 0001`) before `upgrade head` is allowed; `deploy.sh` refuses to migrate an unstamped DB.
The app does **not** create tables at runtime (`AUTO_CREATE_TABLES=false` by default).

### 6.6 Repository & service data access

- `repositories/*` hold SQLAlchemy queries; `repositories/leave_ledger.py` is the single writer for balance changes.
- Some cron jobs and the admin directory use raw `text()` SQL for performance.
- `get_or_404(db, Model, id)` helper in `repositories/base.py`.

### 6.7 Caching (Redis)

`utils/redis_cache.py`: JSON values with TTL (default 300 s), `cache_get/set/delete/delete_pattern`.
Key families: dashboard stats / work-hours / on-leave / yearly / birthdays / clock-status / recent-activity,
employee profile, leave balance, yearly holidays, extra-work-day lookup. `invalidate_employee_dashboard()`
is called after attendance, leave and claim changes. If Redis is unavailable every call degrades to a
miss — the app stays functional.

### 6.8 Logging & audit data

| Store | Content |
|---|---|
| `activity_log` | Every API call (method, URL, client IP, request/response body, status, latency, user); secrets masked (`password`, `token`, `auth_token`, `client_secret`, upload/download URLs); `/health`, `/metrics`, `/ping`, favicons excluded; multipart bodies summarised |
| `rbac_audit_log` | Permission use (see §4.3) |
| `attendance_audit_log` | Column-level before/after of attendance edits, with app name and client IP |
| `question_audit_log` | Question-builder changes |
| `email_log` | Every e-mail send with status, recipients, attachment info |
| `cron_log` | Per-employee cron outcomes (reminders, absent marks, penalties) |
| `leave_report_run_log` | Whether a monthly report e-mail was already sent |
| Files | `logs/hrm.log` (daily rotation, 7 days), `cron_logs/<job>.log` (10 MB × 5) |

---

## 7. Schedulers & cron jobs

### 7.1 Mechanism

- `fastapi_app/scheduler.py` creates one `BackgroundScheduler(timezone=Asia/Dhaka)` at startup.
- **Single-owner guarantee:** with 4 Uvicorn workers, each tries to create `/tmp/hrm_scheduler.lock`
  with `O_CREAT|O_EXCL`; the winner owns the scheduler. A stale lock (PID not alive) is removed and
  re-acquired. The lock is deleted on graceful shutdown.
- Every job uses `max_instances=1`, `replace_existing=True` and a `misfire_grace_time`
  (300 s for daily jobs, 3600 s for weekly/monthly).
- A listener logs success/failure of every execution.
- Shift IDs processed per job live in `constants/scheduler_shifts.py`
  (BD shifts `[1, 5, 8, 9]`, USA shift `[7]`). **Onboarding a new shift/team requires editing that file.**
- Jobs can also be run as scripts, e.g.
  `python -m fastapi_app.cron_jobs.cron_11PM_markAbsent_autoClockOut --shift-ids 1 5` .

### 7.2 Registered jobs (source of truth: `scheduler.py`)

| ID | Function | Trigger (timezone) | Shifts |
|---|---|---|---|
| `email_reminder_slot_1` | `send_clock_in_reminders(slot=1)` | daily **09:30** (Asia/Dhaka) | 1, 5, 8, 9 |
| `email_reminder_slot_2` | `send_clock_in_reminders(slot=2)` | daily **17:00** (Asia/Dhaka) | 1, 5, 8, 9 |
| `mark_absent_autoclockout` | `mark_absent_employees` | daily **23:59** (Asia/Dhaka) | 1, 5, 8, 9 |
| `weekly_late_penalty` | `apply_weekly_late_penalty` | **Saturday 23:59** (Asia/Dhaka) | 1, 5, 8, 9 |
| `usa_email_reminder_slot_1` | `send_clock_in_reminders(slot=1)` | daily **10:00** (America/New_York) | 7 |
| `usa_email_reminder_slot_2` | `send_clock_in_reminders(slot=2)` | daily **17:00** (America/New_York) | 7 |
| `usa_mark_absent_autoclockout` | `mark_absent_employees` | daily **23:59** (America/New_York) | 7 |
| `negative_leave_report` | `send_negative_leave_reports` | **1st of month 01:00** (Asia/Dhaka) | all |
| `monthly_attendance_claim_reminder` | `send_attendance_claim_reminder` | **1st of month 10:00** (Asia/Dhaka) | — |
| `work_hours_report` | `send_work_hours_report` | **1st of month 11:00** (Asia/Dhaka) | all tracked |

Not registered: `cron_jobs/yearly_leave_carryforward.py` (see §7.4).

### 7.3 What each job does

**Clock-in reminders** — e-mails active employees of the given shifts who have not clocked in yet; skips
non-working days, employees with `email_restriction_status` off, and anyone already reminded in that
slot (`cron_log`). Sender is the active `email_hrm` account.

**Mark absent + auto clock-out (23:59 local)**
- Only active employees with `attendance_track` on a working day.
- No clock-in and not on approved full-day leave ⇒ `ABSENT` and `redeemed +1`, `available −1`
  (can go negative). Approved FIRST_HALF leave with no clock-in ⇒ 0.5 penalty. Only **APPROVED** leave
  exempts; a still-PENDING leave is penalised and reversed later if approved.
- Clocked in but no clock-out ⇒ auto clock-out: prefers the latest biometric sync time (no penalty),
  otherwise `shift.end − clock_out_penalty` (FIRST_HALF leave: shift midpoint − penalty).
- Span > 1.5 × shift (not Home) ⇒ auto 0.5-day Extra Work request.
- The penalty is written to the ledger as `ABSENT_PENALTY` (idempotent per employee/date) against the
  balance chosen by `resolve_balance` (lowest `leave_type_id` of the year). With no balance row the
  penalty is skipped (warning logged) but ABSENT is still saved.

**Weekly late penalty** — looks at the previous completed Mon–Fri week (works on any run day);
employees late **3+ times** get `redeemed +1`, `available −1`, logged to `cron_log`.

**Negative leave report** — compares each employee's net balance with the previous month's opening
balance (from `leave_balance_ledger`; falls back to attendance-derived penalties before the ledger
cut-over), builds an Excel (`openpyxl`) plus HTML e-mail covering worsened / newly negative balances,
absent-day and weekly-late penalties and half-day absences. Idempotent through `leave_report_run_log`.
Supports `force` / `init` flags.

**Monthly attendance-claim reminder** — e-mails the recipients configured under
`email_config.description = 'cron_monthly_attendance_claim'` to action last month's claims.

**Work-hours report** — for every active tracked employee computes the previous month's expected vs
actual hours (attendance + approved extra work), deficit, and **leaves to deduct = floor(deficit ÷
`shift.duration_for_one_leave`)** (default 540 min), writes `work_deficit`, and e-mails an Excel to
`email_config.description = 'cron_work_hours_report_mail'`. Includes a temporary 7 h/day override for
shifts 1 & 5 (19 Feb – 19 Mar 2026) and a calculation start boundary of 16 Feb 2026. CLI:
`--year`, `--month`.

### 7.4 Yearly leave carry-forward (manual)

`yearly_leave_carryforward.run_yearly_leave_carryforward_job()` creates next year's `leave_balance`
rows for all active employees: `allowed = total_paid_holiday`, `carry_forward = this year's available`,
`available = allowed + carry_forward`, `redeemed = 0`, `achieved = 0`, writing a ledger `set` event.
**It is documented as a 31 Dec 23:59 job but is not wired into `scheduler.py`** — run it from a system
cron / manually until it is registered.

### 7.5 Operating the scheduler

- Page: `GET /super_admin/scheduler/manage` (Super Admin) lists jobs and status via
  `get_scheduler_status()` / `utils/cron_utils.get_all_jobs_with_status()`.
- Helper functions exist for `pause_job`, `resume_job`, `trigger_job_now`, `reschedule_job`.
- **The JSON endpoints behind those buttons (`/super_admin/scheduler/jobs…`) are defined in
  `routers/integrations/scheduler.py` but that router is never included in `main.py`**, so the page's
  pause/resume/trigger/reschedule calls currently 404 (see §12).
- Logs: `cron_logs/<job>.log` (rotating, 10 MB × 5) and the main `logs/hrm.log`.

---

## 8. Integrations

### 8.1 Google (Calendar + Sign-In)

- **Sign-In:** OAuth2 authorization-code flow, redirect URI `GOOGLE_AUTH_REDIRECT_URI`.
- **Calendar** (`/api/google-calendar/*`, 16 endpoints): connect/disconnect, status, list meetings,
  create / update / delete / fetch event, attendee search, conflict check, day schedule, **best-time
  finder**, shared/private meeting templates. Tokens in `google_calendar_tokens` / `google_calendar_config`.
  Redirect URI `GOOGLE_REDIRECT_URI`. Public-holiday import by country with cache clearing.
  Setup guide: `docs/GOOGLE_CALENDAR_SETUP.md`.

### 8.2 SenseFace 2A (ZKTeco ADMS)

Endpoints `/iclock/cdata` (GET handshake, POST push), `/iclock/getrequest`, `/iclock/devicecmd`.
Handshake returns options (`TimeZone=6`, realtime on). Device PIN = `employee_code`. A module-level
`DRY_RUN` flag (currently `False`) switches to log-only; `DEVICE_TIME_OFFSET_MINUTES` corrects a
fast/slow device clock. Per-device log counts are held **in process memory**. Access-log noise for
the polling endpoints is suppressed.

### 8.3 File service (profile photos)

`file_upload_api/` implements init → presigned upload to MinIO → finalize → presigned download
against `https://fs.apurbatech.io` (tenant `hrm.apurbatech.io`). Endpoints:
`POST/GET/DELETE /api/employee/profile/photo`, `GET /api/employee/{emp_id}/photo`. Registered
before the profile router so it takes precedence. The service URL and tenant are **hard-coded**.

### 8.4 HRM AI engine

`services/hrm_ai.py` calls `GET {HRM_AI_BASE_URL}` commit-quantity evaluation (`hrm_id`, `start_date`,
`end_date`) for `POST /admin|super_admin/commit_evaluation/get_commit_quantity_evaluation`
(`commit_evaluation.view`). Maps timeouts → 504 and connection/invalid body → 502. `git_username_mapping`
links employees to git identities.

### 8.5 SMTP

Sender account is a DB row (`email_hrm`, host/port/TLS/credentials, active flag), editable and
test-sendable from the UI. Recipient lists (To/CC/BCC, optionally per department) come from
`email_config`, managed through `/api/email-configs` and `/api/email-config-recipients`.

### 8.6 External attendance summary API

`GET /api/external/attendance/summary` returns attendance + leave summary for an employee and date
range, protected by HTTP Basic credentials from `.env`.

---

## 9. Running the application

### 9.1 Prerequisites

PostgreSQL (schema applied via Alembic), Python 3.11/3.12, optionally Redis. SMTP credentials are
stored in the database (`email_hrm`), not in `.env`.

### 9.2 Environment variables (`.env`; template: `.env.example`)

| Variable | Purpose | Default in `config.py` |
|---|---|---|
| `POSTGRES_HOST/PORT/USER/PASSWORD/DATABASE` | DB connection | `localhost / 5432 / apurba / apurba / hrm-new` |
| `JWT_SECRET_KEY`, `SECRET_KEY` | Signing secrets — **must be changed** | `dev-secret-key-change-in-production` |
| `DEBUG` | Debug mode; also relaxes the `secure` cookie flag | `True` (compose default `False`) |
| `AUTO_CREATE_TABLES` | `create_all()` at startup (throw-away DBs only) | `false` |
| `DEFAULT_TIMEZONE` | Fallback timezone | `Asia/Dhaka` |
| `REDIS_HOST/PORT/DB/PASSWORD` | Cache | `localhost / 6379 / 0 / ''` |
| `GOOGLE_CLIENT_ID/SECRET`, `GOOGLE_REDIRECT_URI`, `GOOGLE_AUTH_REDIRECT_URI` | Calendar + sign-in | prod URLs |
| `ATTENDANCE_SUMMARY_API_USERNAME/PASSWORD` | Basic auth for the external API | empty |
| `HRM_AI_BASE_URL`, `HRM_AI_TIMEOUT_SECONDS` | AI engine | `https://hrmai-engine.apurbatech.io`, `30` |
| `ALLOWED_ORIGINS` | Listed in `.env.example` but **not read by the code** (CORS is `.*`) | — |

### 9.3 First-time setup (local)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # fill in DB, secrets, etc.

# Empty database:
createdb hrm_new
alembic upgrade head            # or: PGUSER=… db/build_schema.sh hrm_new

# Existing database that already has the baseline schema (once only):
alembic stamp 0001
```

### 9.4 Start the server

| Command | Notes |
|---|---|
| `./run.sh` | Frees the port, activates `.venv`, `uvicorn fastapi_app.main:app --reload` on `$PORT` (default 9000) / `$BIND_HOST` |
| `./start_zil.sh` | Same, but uses venv `fastapi_venv` |
| `uvicorn fastapi_app.main:app --host 0.0.0.0 --port 9000 --reload` | Manual |
| `docker compose up -d --build` | Containerised (see §11) |

**Default account:** on first start the app creates `admin / admin123` (`admin@hrm.local`) if no `admin`
user exists — change the password immediately in any shared environment.

### 9.5 Useful URLs

| URL | Purpose |
|---|---|
| `/` , `/login` | Login |
| `/health` | Health check (used by Docker) |
| `/api/docs`, `/api/redoc`, `/api/openapi.json` | Swagger / ReDoc / schema (HTML routes are excluded from the schema) |
| `/super_admin/scheduler/manage` | Scheduler console |
| `/rbac-management`, `/rbac-audit-logs` | RBAC UI |

### 9.6 Running a job by hand

```bash
python -m fastapi_app.cron_jobs.cron_11AM_email_reminder --shift-ids 1 5 8 9 --slot 1
python -m fastapi_app.cron_jobs.cron_11PM_markAbsent_autoClockOut --shift-ids 1 5 8 9
python -m fastapi_app.cron_jobs.cron_weekly_late_penalty --shift-ids 1 5 8 9
python -m fastapi_app.cron_jobs.cron_monthly_work_hours_report --year 2026 --month 10
python -m fastapi_app.cron_jobs.yearly_leave_carryforward
```

### 9.7 Logs

`logs/hrm.log` (rotated daily, 7 days kept, files named `YYYY-MM-DD.log`), `cron_logs/*.log`, plus
`activity_log`, `email_log` and `cron_log` tables.

---

## 10. Testing

### 10.1 Current state

There is **no test runner configuration** (`pytest.ini`, `pyproject.toml`, `conftest.py` are absent) and
**`pytest` is not in `requirements.txt` nor installed in `.venv`**. `tests/` mixes three kinds of files:

| Kind | Examples | Runs without live DB? |
|---|---|---|
| **Real pytest unit tests** | `test_leave_ledger.py` (9 tests, in-memory SQLite), `test_activity_logger.py` (5 tests: masking, URL filtering) | Yes |
| **Diagnostic / one-off scripts** named `test_*.py` | `test_api_simulation.py`, `test_cascade_triggers.py`, `test_work_hours_fix.py`, `test_work_hours_debug.py`, `test1_leave_request_approval.py` (all open `SessionLocal()`/`engine` from `.env`); `test_attendance_endpoints.py` (HTTP calls to a running server). `test_attendance_hours.py` is a standalone print-based script. `test_negative_leave_*.py` and `test_approver_tags.py` were not individually inspected | **No** (except `test_attendance_hours.py`) |
| **Data/ops scripts** | `seed_data.py`, `initialize_*.py`, `create_*_table.py`, `inspect_*.py`, `run_migration*.py`, `force_send_email_reminder.py`, `send_me_email.py`, `verify_*.py`, `add_permissions_script.py` | **No** — read/write the configured DB; `send_me_email.py` / `force_send_email_reminder.py` are intended to send real mail |

`tests/config.py` is a leftover SQLite/MySQL config from the Flask era. `.pytest_cache/lastfailed`
references test files that no longer exist (e.g. `test_usa_cron_jobs.py`, `test_system.py`).

### 10.2 How to run

```bash
pip install pytest                       # not in requirements.txt
python -m pytest tests/test_leave_ledger.py tests/test_activity_logger.py -q
```

Run diagnostic scripts only against a throw-away or staging database — several write data.

### 10.3 Schema/ORM consistency checks

```bash
scripts/db/check_schema.sh     # db/schema files == Alembic == ORM models
python scripts/db/check_orm.py # ORM models vs a real database (KNOWN_DIFFERENCES whitelist)
```

### 10.4 Static analysis

`sonar-project.properties` (project key `hrm_v2`, sources `fastapi_app`, excludes migrations/venv) and
`check_sonar.sh` (runs `pysonar` against an internal SonarQube host). **The script has the server URL
and an access token hard-coded — move it to an environment variable and rotate the token.**

### 10.5 Manual / API testing aids

Swagger UI at `/api/docs`; `tests/force_send_email_reminder.py` triggers the reminder mail on demand;
the cron modules are directly runnable (§9.6). Postman collections are not present in the repo.

### 10.6 Coverage gaps worth closing

No automated tests exist for: clock-in/out rules, leave approval effects, approval-level logic, RBAC
guards, WFH conflicts, extra-work credit, the cron jobs' penalty rules, or HTTP-level route tests
(FastAPI `TestClient` against a test DB). The ledger and activity-logger tests show the pattern to extend.

---

## 11. Deployment

### 11.1 Artifacts

| File | Role |
|---|---|
| `Dockerfile` | `python:3.11-slim`, installs `gcc libpq-dev`, `pip install -r requirements.txt`, copies the repo, creates `fastapi_app/photo_uploads` and `cron_logs`, exposes **9000**, runs `uvicorn fastapi_app.main:app --host 0.0.0.0 --port 9000 --workers 4` |
| `docker-compose.yml` | Service `hrm-app` (container `hrm-app`, `restart: unless-stopped`), host port **9009 → 9000**, `env_file: .env`, env overrides for DB/secrets/timezone/Google, volumes `photo_uploads`, `cron_logs`, `logs`, healthcheck hitting `/health` every 30 s (start period 15 s, 3 retries) |
| `deploy.sh` | One-command deploy (below) |
| `.dockerignore` | Excludes venvs, `.git`, `.env`, logs, `docs/`, `.idea`, zips |

PostgreSQL and Redis are **external** (not in compose). `POSTGRES_HOST` defaults to the Docker host
bridge `172.17.0.1`.

### 11.2 `deploy.sh` sequence

1. Verify Docker and Compose (v2 plugin or `docker-compose`).
2. Ensure `.env` exists (copies `.env.example` and **exits** so you can edit it).
3. Warn about the configured `POSTGRES_HOST`.
4. `compose build` — a failed build leaves the running app untouched.
5. **Migration gate:** `alembic current` in a throw-away container; if no revision is recorded it
   refuses to continue and prints the one-time `alembic stamp 0001` command; otherwise runs
   `alembic upgrade head`. Failure aborts before the old container is touched. Migrations must
   therefore be **backward compatible** with the still-running version (add/widen, don't drop/rename in one step).
6. `compose down --remove-orphans`, `compose up -d`.
7. After 5 s, confirm the container is running and print URLs (app `:9009`, `/health`, `/api/docs`) and elapsed time.

### 11.3 Release checklist (from `.env.example`)

- `DEBUG=False`; fresh strong `JWT_SECRET_KEY` and `SECRET_KEY` (different values).
- `GOOGLE_REDIRECT_URI` / `GOOGLE_AUTH_REDIRECT_URI` on the production HTTPS domain; rotate exposed OAuth credentials.
- HTTPS/TLS terminated in front of the app (the auth cookie is `secure` when `DEBUG=False`).
- Correct DB credentials; Redis reachable if caching is wanted.
- Change/remove the seeded `admin / admin123` account.
- Backups and monitoring on PostgreSQL and the three volumes.

### 11.4 Runtime considerations

- **4 workers, 1 scheduler:** only one worker holds `/tmp/hrm_scheduler.lock`. If you scale to several
  containers, each container will run its own scheduler (the lock is container-local) and jobs will
  **duplicate** — run a single replica or move the scheduler out.
- In-memory state (SenseFace per-device counters) is per worker.
- Volumes persist photos (legacy local uploads), cron logs and server logs; the scheduler lock lives in the
  container's `/tmp`.
- Branches in the repo: `master` (current), `prod/v1`, `dev`, and several `feature/*` / `issue/*` branches
  (e.g. `feature/wfh-request`, `feature/payroll`, `feature/upload_download`).
- Docs-maintenance rule (`CLAUDE.md`): any attendance-claim behaviour change must also update
  `docs/ATTENDANCE_CLAIM_FLOW.md` and add a dated Change Log row.

---

## 12. Known gaps & documentation drift

Findings from this audit. Each was checked against the code; none have been changed.

| # | Area | Finding | Impact / suggested action |
|---|---|---|---|
| 1 | Scheduler admin | `routers/integrations/scheduler.py` (status / jobs / pause / resume / trigger / reschedule) is **never included** in `main.py`; only the HTML page `/super_admin/scheduler/manage` is mounted. The page's JS calls `/super_admin/scheduler/jobs…` | Pause/resume/trigger/reschedule buttons 404. `app.include_router(...)` for that router |
| 2 | Scheduler | `yearly_leave_carryforward` is not registered; docs claim "11 scheduled jobs", the scheduler registers **10** | Year-end carry-forward must be run manually, or registered at 31 Dec 23:59 |
| 3 | Schedule times | Docstrings/logs disagree with the triggers: BD reminder slot 2 trigger is **17:00** (docstring 15:30, log text 16:00; slot-1 log text says 10:00 but the trigger is 09:30); claim reminder file says "4th, 7 PM" but trigger is **1st, 10:00**; work-hours report file says "8 PM" but trigger is **1st, 11:00** | `scheduler.py` is authoritative; fix comments |
| 4 | Work-hours rule | Report e-mail/Excel text says "8 hours = 1 leave day" (480 min), but the calculation uses `shift.duration_for_one_leave` (default **540 min / 9 h**) | Align wording or the constant |
| 5 | JWT lifetime | `JWT_ACCESS_TOKEN_EXPIRES = 24 h` in config, but login issues **30-day** tokens | Decide the intended lifetime; role changes only take effect on re-login |
| 6 | CORS | `allow_origin_regex=".*"` with `allow_credentials=True`; `ALLOWED_ORIGINS` in `.env.example` is unused | Effectively any origin can make credentialed requests; restrict for production |
| 7 | Default credentials | Startup creates `admin / admin123` if missing | Rotate/remove in shared environments |
| 8 | Secrets in repo | `check_sonar.sh` embeds a SonarQube token and host | Move to env var and rotate the token |
| 9 | Tests | No runner config; `pytest` not a dependency; most `test_*.py` are live-DB scripts; stale `.pytest_cache`; `tests/config.py` is legacy | See §10.6 |
| 10 | Hard-coded integration config | File service URL/tenant (`fs.apurbatech.io`, `hrm.apurbatech.io`), ADMS `TimeZone=6`, shift IDs in `constants/scheduler_shifts.py` | Make configurable before multi-tenant / new-region use |
| 11 | Penalty target | Absent/half-absent penalties are charged to the lowest-`leave_type_id` balance of the year and skipped (warning only) when the employee has no balance row | Employees with several leave types always pay from the same type; missing rows silently avoid the penalty |
| 12 | DB integrity | Three history tables lack an FK on `actioned_by_employee_id` (documented in `db/README.md`) | Separate migration after data check |
| 13 | Scheduler scaling | Lock file is container-local | Duplicate jobs if more than one replica runs |
| 14 | Legacy code | `routers/*/legacy.py`, root `templates/`, `schemas/*` ORM shims, empty `payroll` packages, `sh_all_employees.html.backup`, `sh_all_attendance_history1.html` | Candidates for cleanup |
| 15 | Python version | Docker image uses 3.11, local `.venv` is 3.12 | Pin one version |
| 16 | Doc drift | `docs/PRODUCT_DESCRIPTION.md` says "11 scheduled jobs", cites "11 AM / 11 PM" runs and Redis "session management" (real times: §7.2; Redis is only a cache). `docs/APP_FEATURES_AND_BUSINESS_RULES.md` still says the absent penalty hits an unordered "first" balance row (now deterministic via `resolve_balance`) and uses an 8 h work-hours divisor (code: `duration_for_one_leave`, default 9 h) | This file supersedes those points |

---
## Appendix A — Complete route inventory (generated from the live FastAPI app)

Generated 2026-11-04 by importing `fastapi_app.main:app` and walking `app.routes`. **516 routes** (86 HTML pages, 430 non-HTML/JSON-or-other). `HTML` = server-rendered Jinja page; `API` = JSON/other.

Note: `/admin/…`, `/super_admin/…` and `/employee/…` variants frequently map to the same handler logic; the real gate is the permission/role dependency (see §4.3).


### `auth.routers` (12)

| Method | Path | Handler | Type |
|---|---|---|---|
| POST | `/api/auth/login` | `login` | API |
| GET | `/api/auth/me` | `get_current_user_info` | API |
| GET | `/api/auth/check-permission/{permission_code}` | `check_permission` | API |
| POST | `/api/auth/logout` | `logout` | API |
| GET | `/api/auth/google/auth-url` | `google_auth_url` | API |
| GET | `/api/auth/google/login` | `google_login` | API |
| GET | `/api/auth/google/callback` | `google_callback` | API |
| GET | `/api/auth/google/complete` | `google_complete` | HTML |
| POST | `/api/auth/forgot-password` | `forgot_password` | API |
| POST | `/api/auth/verify-otp` | `verify_otp` | API |
| POST | `/api/auth/change-password` | `change_password` | API |
| POST | `/api/auth/reset-password` | `reset_password` | API |

### `file_upload_api.router` (4)

| Method | Path | Handler | Type |
|---|---|---|---|
| POST | `/api/employee/profile/photo` | `upload_profile_photo` | API |
| GET | `/api/employee/profile/photo` | `get_profile_photo` | API |
| GET | `/api/employee/{emp_id}/photo` | `get_employee_photo_by_id` | API |
| DELETE | `/api/employee/profile/photo` | `delete_profile_photo` | API |

### `framework (docs/static)` (4)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/openapi.json` | `openapi` | API |
| GET | `/api/docs` | `swagger_ui_html` | API |
| GET | `/docs/oauth2-redirect` | `swagger_ui_redirect` | API |
| GET | `/api/redoc` | `redoc_html` | API |

### `main` (34)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/` | `login_page` | HTML |
| GET | `/login` | `login_page_alt` | HTML |
| GET | `/logout` | `logout_page` | API |
| GET | `/forgot-password` | `forgot_password_page` | HTML |
| GET | `/verify-otp` | `verify_otp_page` | HTML |
| GET | `/reset-password` | `reset_password_page` | HTML |
| GET | `/extension/privacy-policy` | `extension_privacy_policy` | HTML |
| GET | `/dashboard` | `dashboard_page` | HTML |
| GET | `/admin/master-data` | `master_data_page` | HTML |
| GET | `/admin/employees` | `admin_employees_page` | HTML |
| GET | `/admin/employees/{employee_id}/profile` | `employee_profile_page` | HTML |
| GET | `/admin/hierarchy` | `hierarchy_page` | HTML |
| GET | `/employee/clock-in` | `employee_clock_in_page` | HTML |
| GET | `/employee/clock-out` | `employee_clock_out_page` | HTML |
| GET | `/employee/attendance` | `employee_attendance_page` | HTML |
| GET | `/employee/new_leave_request` | `employee_leave_request_page` | HTML |
| GET | `/employee/leave-history` | `employee_leave_request_history_page` | HTML |
| GET | `/employee/attendance/claims/history-page` | `employee_attendance_claim_history_page` | HTML |
| GET | `/admin/attendance` | `admin_attendance_overview_page` | HTML |
| GET | `/admin/attendance/manage` | `admin_attendance_manage_page` | HTML |
| GET | `/admin/settings/office-hours` | `admin_office_hours_page` | HTML |
| GET | `/admin/settings/smtp` | `admin_smtp_settings_page` | HTML |
| GET | `/employee/claims` | `employee_claims_page` | HTML |
| GET | `/employee/overtime` | `employee_overtime_page` | HTML |
| GET | `/employee/blood-group` | `employee_blood_group_page` | HTML |
| GET | `/approver/dashboard` | `approver_dashboard_page` | HTML |
| GET | `/admin/approvers` | `admin_approvers_page` | HTML |
| GET | `/admin/reports/attendance` | `admin_attendance_reports_page` | HTML |
| GET | `/yearly-holiday-info` | `yearly_holiday_info` | HTML |
| GET | `/api/check-ip` | `check_ip_public` | API |
| GET | `/url` | `list_urls_page` | HTML |
| GET | `/health` | `health_check` | API |
| GET | `/api` | `api_info` | API |
| GET | `/favicon.ico` | `favicon` | API |

### `pages.approvals` (4)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/admin/approver_history` | `admin_approver_history_page` | HTML |
| GET | `/super_admin/approver_history` | `super_admin_approver_history_page` | HTML |
| GET | `/{user_role}/approver_history` | `role_based_approver_history_page` | HTML |
| GET | `/{user_role}/bulk-approval-assignor` | `bulk_approval_assignor_page` | HTML |

### `pages.attendance` (12)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/employee/attendance_history` | `attendance_history_page` | HTML |
| GET | `/admin/attendance_claim_request/approval/{claim_id}` | `attendance_claim_approval_page_admin` | HTML |
| GET | `/super_admin/attendance_claim_request/approval/{claim_id}` | `attendance_claim_approval_page_super_admin` | HTML |
| GET | `/employee/attendance_claim_request/approval/{claim_id}` | `attendance_claim_approval_page_employee` | HTML |
| GET | `/admin/attendance_claim_request/inbox` | `attendance_claim_inbox_admin_page` | HTML |
| GET | `/super_admin/attendance_claim_request/inbox` | `attendance_claim_inbox_super_admin_page` | HTML |
| GET | `/employee/attendance_claim_request/inbox` | `attendance_claim_inbox_employee_page` | HTML |
| GET | `/admin/all_attendance_history` | `all_attendance_history_admin_page` | HTML |
| GET | `/super_admin/all_attendance_history` | `all_attendance_history_super_admin_page` | HTML |
| GET | `/admin/employees-work-hours` | `admin_work_hours_page` | HTML |
| GET | `/admin/employee_attendance_directory` | `employee_attendance_directory_page_admin` | HTML |
| GET | `/super_admin/employee_attendance_directory` | `employee_attendance_directory_page_super_admin` | HTML |

### `pages.dashboard` (2)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/admin/dashboard` | `admin_dashboard_page` | HTML |
| GET | `/super_admin/dashboard` | `super_admin_dashboard_page` | HTML |

### `pages.employees` (11)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/confirmation/{employee_code}` | `employee_confirmation_page` | HTML |
| GET | `/admin/create_employee` | `create_employee_page_admin` | HTML |
| GET | `/super_admin/create_employee` | `create_employee_page_super_admin` | HTML |
| GET | `/super_admin/create_employee/confirmation/{employee_code}` | `admin_employee_confirmation_page` | HTML |
| GET | `/admin/create_employee/confirmation/{employee_code}` | `admin_employee_confirmation_page` | HTML |
| GET | `/admin/all_employees` | `all_employees_page_admin` | HTML |
| GET | `/super_admin/all_employees` | `all_employees_page_super_admin` | HTML |
| GET | `/{user_role}/all_employees` | `all_employees_page_role_based` | HTML |
| GET | `/employee/dashboard` | `employee_dashboard_page` | HTML |
| GET | `/employee/profile` | `employee_profile_page` | HTML |
| GET | `/onboarding/questionnaire` | `onboarding_questionnaire_page` | HTML |

### `pages.evaluations` (1)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/admin/evaluations` | `evaluations_page` | HTML |

### `pages.extra_work` (7)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/admin/extra_work/inbox` | `extra_work_inbox_admin_page` | HTML |
| GET | `/admin/extra_work/approval/{work_id}` | `extra_work_approval_page_admin` | HTML |
| GET | `/super_admin/extra_work/inbox` | `extra_work_inbox_super_admin_page` | HTML |
| GET | `/super_admin/extra_work/approval/{work_id}` | `extra_work_approval_page_super_admin` | HTML |
| GET | `/employee/extra_work/inbox` | `extra_work_inbox_employee_page` | HTML |
| GET | `/employee/extra_work/approval/{work_id}` | `extra_work_approval_page_employee` | HTML |
| GET | `/admin/extra_work_directory` | `extra_work_directory_page` | HTML |

### `pages.integrations` (4)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/super_admin/create_meeting` | `super_admin_create_meeting_page` | HTML |
| GET | `/admin/create_meeting` | `admin_create_meeting_page` | HTML |
| GET | `/{user_role}/create_meeting` | `dynamic_create_meeting_page` | HTML |
| GET | `/super_admin/scheduler/manage` | `cron_management_page` | HTML |

### `pages.leave` (9)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/admin/leave_request/approval/{leave_id}` | `leave_approval_page_admin` | HTML |
| GET | `/admin/leave_request/inbox` | `leave_inbox_page_admin` | HTML |
| GET | `/super_admin/leave_request/approval/{leave_id}` | `leave_approval_page_super_admin` | HTML |
| GET | `/super_admin/leave_request/inbox` | `leave_inbox_page_super_admin` | HTML |
| GET | `/employee/leave_request/approval/{leave_id}` | `leave_approval_page_employee` | HTML |
| GET | `/employee/leave_request/inbox` | `leave_inbox_page_employee` | HTML |
| GET | `/admin/leave_cancellation_inbox` | `leave_cancellation_page_admin` | HTML |
| GET | `/super_admin/leave_cancellation_inbox` | `leave_cancellation_page_super_admin` | HTML |
| GET | `/employee/leave_cancellation_inbox` | `leave_cancellation_page_employee` | HTML |

### `pages.question_builder` (2)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/admin/question-builder` | `question_builder_admin_page` | HTML |
| GET | `/super_admin/question-builder` | `question_builder_super_admin_page` | HTML |

### `pages.rbac` (2)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/rbac-management` | `rbac_management_page` | HTML |
| GET | `/rbac-audit-logs` | `rbac_audit_logs_page` | HTML |

### `pages.utilities` (2)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/utilities-dashboard` | `utilities_dashboard_page` | HTML |
| GET | `/admin/restrictions-management` | `restrictions_management_page` | HTML |

### `routers.SenseFace_2A.adms_router` (4)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/iclock/cdata` | `adms_handshake` | API |
| POST | `/iclock/cdata` | `adms_receive_data` | API |
| GET | `/iclock/getrequest` | `adms_get_request` | API |
| POST | `/iclock/devicecmd` | `adms_device_cmd` | API |

### `routers.approvals.bulk_assignor` (6)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/bulk-approvals/page-data` | `bulk_approval_page_data` | API |
| GET | `/api/bulk-approvals/approvers` | `get_approvers_list` | API |
| GET | `/api/bulk-approvals/employees` | `get_employees_list` | API |
| POST | `/api/bulk-approvals/check-existing` | `check_existing_approvals` | API |
| POST | `/api/bulk-approvals/merge` | `merge_approvals` | API |
| POST | `/api/bulk-approvals/assign` | `bulk_assign_approvals` | API |

### `routers.approvals.categories` (3)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/approval-categories/` | `get_approval_categories` | API |
| GET | `/api/approval-categories/employee/{employee_id}/approvers` | `get_employee_approvers_by_type` | API |
| GET | `/api/approval-categories/employee/{employee_id}/all-approvers` | `get_all_employee_approvers` | API |

### `routers.approvals.history` (4)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/admin/approver_history` | `get_approver_history_api_admin` | API |
| GET | `/api/super_admin/approver_history` | `get_approver_history_api_super_admin` | API |
| GET | `/api/admin/search_employees` | `search_employees_admin` | API |
| GET | `/api/super_admin/search_employees` | `search_employees_super_admin` | API |

### `routers.attendance.admin` (6)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/admin/attendance/employee/{employee_id}` | `get_employee_attendance` | API |
| GET | `/api/admin/attendance/details/{attendance_id}` | `get_attendance_details` | API |
| PUT | `/api/admin/attendance/edit/{attendance_id}` | `edit_attendance` | API |
| PUT | `/api/admin/attendance/time-track/{time_track_id}` | `edit_time_track` | API |
| POST | `/api/admin/attendance/create` | `create_attendance` | API |
| DELETE | `/api/admin/attendance/{attendance_id}` | `delete_attendance` | API |

### `routers.attendance.all_history` (5)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/admin/attendance_history/page-data` | `attendance_history_page_data` | API |
| GET | `/api/admin/attendance_history/employees` | `search_employees_for_history` | API |
| GET | `/api/admin/attendance_history/{employee_id}/records` | `get_employee_attendance_records` | API |
| GET | `/api/admin/attendance_history/{employee_id}/analytics` | `get_employee_attendance_analytics` | API |
| GET | `/api/admin/attendance_history/{employee_id}/work-hours` | `get_employee_work_hours` | API |

### `routers.attendance.claim_approval` (6)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/admin/attendance_claim_request/approval/{claim_id}/data` | `get_approval_page_data` | API |
| POST | `/admin/attendance_claim_request/approval/{claim_id}/action` | `attendance_claim_action` | API |
| GET | `/super_admin/attendance_claim_request/approval/{claim_id}/data` | `get_approval_page_data_super_admin` | API |
| POST | `/super_admin/attendance_claim_request/approval/{claim_id}/action` | `attendance_claim_action_super_admin` | API |
| GET | `/employee/attendance_claim_request/approval/{claim_id}/data` | `get_approval_page_data_employee` | API |
| POST | `/employee/attendance_claim_request/approval/{claim_id}/action` | `attendance_claim_action_employee` | API |

### `routers.attendance.claim_inbox` (5)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/admin/attendance_claim_request/inbox/data` | `get_inbox_data_admin` | API |
| DELETE | `/admin/attendance_claim_request/inbox/clear` | `clear_inbox_admin` | API |
| GET | `/super_admin/attendance_claim_request/inbox/data` | `get_inbox_data_super_admin` | API |
| DELETE | `/super_admin/attendance_claim_request/inbox/clear` | `clear_inbox_super_admin` | API |
| GET | `/employee/attendance_claim_request/inbox/data` | `get_inbox_data_employee` | API |

### `routers.attendance.directory` (8)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/admin/employee_attendance_directory/page-data` | `get_directory_page_data_admin` | API |
| GET | `/api/super_admin/employee_attendance_directory/page-data` | `get_directory_page_data_super_admin` | API |
| GET | `/api/admin/employee_attendance_directory` | `get_employee_attendance_directory_data` | API |
| POST | `/api/admin/employee_attendance_directory/update_attendance` | `update_attendance` | API |
| GET | `/api/admin/employee_attendance_directory/export_pdf` | `export_attendance_pdf` | API |
| GET | `/api/super_admin/employee_attendance_directory` | `get_employee_attendance_directory_data_super_admin` | API |
| POST | `/api/super_admin/employee_attendance_directory/update_attendance` | `update_employee_attendance_super_admin` | API |
| GET | `/api/super_admin/employee_attendance_directory/export_pdf` | `export_attendance_pdf_super_admin` | API |

### `routers.attendance.employee` (17)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/employee/attendance/today` | `get_today_attendance` | API |
| POST | `/api/employee/attendance/cancel-leave` | `request_leave_cancellation` | API |
| POST | `/api/employee/attendance/clock-in` | `clock_in` | API |
| POST | `/api/employee/attendance/clock-out` | `clock_out` | API |
| PUT | `/api/employee/attendance/today` | `update_today_attendance` | API |
| GET | `/api/employee/attendance/history` | `get_attendance_history_data` | API |
| GET | `/api/employee/attendance/work-locations/all` | `get_work_locations` | API |
| GET | `/api/employee/attendance/wfh-eligibility` | `get_wfh_eligibility` | API |
| GET | `/api/employee/attendance/check-ip` | `check_ip_address` | API |
| GET | `/api/employee/attendance/office-ips` | `get_office_ips` | API |
| GET | `/api/employee/attendance/{attendance_id}` | `get_attendance_by_id` | API |
| GET | `/api/employee/attendance` | `get_attendance_history` | API |
| POST | `/api/employee/attendance/claim` | `submit_attendance_claim` | API |
| GET | `/api/employee/attendance/claims/history` | `get_attendance_claims_history` | API |
| GET | `/api/employee/attendance/claims/remaining` | `get_remaining_claims` | API |
| GET | `/api/employee/attendance/leave-cancellations/my-requests` | `get_my_leave_cancellation_requests` | API |
| GET | `/api/employee/attendance/clock-status/{user_id}` | `get_employee_clock_status` | API |

### `routers.attendance.external_summary` (1)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/external/attendance/summary` | `get_attendance_leave_summary` | API |

### `routers.attendance.history` (6)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/employee/attendance/history` | `get_attendance_history_data` | API |
| GET | `/api/employee/attendance/claim/{claim_id}/status` | `get_claim_status` | API |
| GET | `/api/employee/attendance/claims/history` | `get_attendance_claim_history` | API |
| GET | `/employee/attendance/history` | `get_attendance_history_data` | API |
| GET | `/employee/attendance/claim/{claim_id}/status` | `get_claim_status` | API |
| GET | `/employee/attendance/claims/history` | `get_attendance_claim_history` | API |

### `routers.attendance.legacy` (8)

| Method | Path | Handler | Type |
|---|---|---|---|
| POST | `/api/attendance/clock-in` | `clock_in` | API |
| POST | `/api/attendance/clock-out` | `clock_out` | API |
| GET | `/api/attendance/today` | `get_today_attendance` | API |
| POST | `/api/attendance/cancel-leave` | `cancel_leave_and_proceed` | API |
| GET | `/api/attendance/history` | `get_attendance_history` | API |
| GET | `/api/attendance/claim/pending` | `get_pending_claims` | API |
| POST | `/api/attendance/claim` | `create_attendance_claim` | API |
| POST | `/api/attendance/claim/{claim_id}/approve` | `approve_attendance_claim` | API |

### `routers.attendance.work_hours_report` (1)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/admin/api/employees-work-hours` | `get_employees_work_hours` | API |

### `routers.dashboard.admin` (3)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/admin/dashboard/data` | `get_admin_dashboard_data` | API |
| GET | `/admin/dashboard/quick-stats` | `get_admin_dashboard_quick_stats` | API |
| GET | `/admin/dashboard/on-leave` | `get_admin_on_leave` | API |

### `routers.dashboard.employee` (1)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/dashboard/employee` | `get_employee_dashboard` | API |

### `routers.dashboard.super_admin` (5)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/super_admin/dashboard/data` | `get_super_admin_dashboard_data` | API |
| GET | `/super_admin/dashboard/quick-stats` | `get_super_admin_dashboard_quick_stats` | API |
| GET | `/super_admin/dashboard/on-leave` | `get_super_admin_on_leave` | API |
| GET | `/super_admin/dashboard/question-builder-stats` | `get_question_builder_stats` | API |
| GET | `/super_admin/dashboard/upcoming-holidays` | `get_upcoming_holidays` | API |

### `routers.employees.create` (7)

| Method | Path | Handler | Type |
|---|---|---|---|
| POST | `/confirmation/{employee_code}` | `employee_confirmation_submit` | API |
| GET | `/api/admin/employees/search` | `search_employees` | API |
| GET | `/api/admin/create_employee/page-data` | `create_employee_page_data` | API |
| POST | `/super_admin/create_employee` | `create_employee_submit` | API |
| POST | `/admin/create_employee` | `create_employee_submit` | API |
| POST | `/super_admin/create_employee/confirmation/{employee_code}` | `update_employee_password` | API |
| POST | `/admin/create_employee/confirmation/{employee_code}` | `update_employee_password` | API |

### `routers.employees.dashboard` (7)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/employee/dashboard/stats` | `get_dashboard_stats` | API |
| GET | `/api/employee/dashboard/on-leave` | `get_employees_on_leave` | API |
| GET | `/api/employee/dashboard/recent-activity` | `get_recent_activity` | API |
| GET | `/api/employee/dashboard/birthdays-this-month` | `get_birthdays_this_month` | API |
| GET | `/api/employee/dashboard/clock-status` | `get_employee_clock_status` | API |
| GET | `/api/employee/dashboard/work-hours` | `get_work_hours` | API |
| GET | `/api/employee/dashboard/attendance-yearly` | `get_yearly_attendance` | API |

### `routers.employees.legacy` (12)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/employees` | `get_employees` | API |
| GET | `/api/employees/me` | `get_my_profile` | API |
| GET | `/api/employees/statistics` | `get_employee_statistics` | API |
| GET | `/api/employees/hierarchy` | `get_hierarchy` | API |
| GET | `/api/employees/{employee_id}` | `get_employee` | API |
| POST | `/api/employees` | `create_employee` | API |
| PUT | `/api/employees/{employee_id}` | `update_employee` | API |
| DELETE | `/api/employees/{employee_id}` | `delete_employee` | API |
| GET | `/api/employees/{employee_id}/reporting-managers` | `get_reporting_managers` | API |
| POST | `/api/employees/{employee_id}/reporting-managers` | `add_reporting_manager` | API |
| DELETE | `/api/employees/reporting-managers/{record_id}` | `remove_reporting_manager` | API |
| PUT | `/api/employees/{employee_id}/self-service` | `self_service_update` | API |

### `routers.employees.list` (14)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/admin/all_employees/page-data` | `all_employees_page_data` | API |
| GET | `/api/super_admin/all_employees/page-data` | `all_employees_page_data_super_admin` | API |
| GET | `/api/admin/all_employees` | `get_all_employees_data` | API |
| GET | `/api/admin/all_employees_list` | `get_all_employees_list_lightweight` | API |
| GET | `/api/admin/employee/{employee_id}` | `get_single_employee_details` | API |
| POST | `/api/admin/all_employees/update` | `update_employee` | API |
| POST | `/api/admin/all_employees/upload_photo` | `upload_employee_photo` | API |
| DELETE | `/api/admin/all_employees/delete/{employee_id}` | `delete_employee` | API |
| GET | `/api/super_admin/all_employees` | `get_all_employees_data_super_admin` | API |
| GET | `/api/super_admin/all_employees_list` | `get_all_employees_list_lightweight_super_admin` | API |
| GET | `/api/super_admin/employee/{employee_id}` | `get_single_employee_details_super_admin` | API |
| POST | `/api/super_admin/all_employees/update` | `update_all_employees_super_admin` | API |
| POST | `/api/super_admin/all_employees/upload_photo` | `upload_employee_photo_super_admin` | API |
| DELETE | `/api/super_admin/all_employees/delete/{employee_id}` | `delete_employee_super_admin` | API |

### `routers.employees.onboarding` (5)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/onboarding/api/status` | `get_onboarding_status` | API |
| GET | `/onboarding/api/questions` | `get_all_questions` | API |
| GET | `/onboarding/api/incorrect-questions` | `get_incorrect_questions` | API |
| POST | `/onboarding/api/submit` | `submit_questionnaire` | API |
| GET | `/onboarding/api/progress` | `get_progress_details` | API |

### `routers.employees.profile` (2)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/employee/profile` | `get_employee_profile` | API |
| PUT | `/api/employee/profile` | `update_employee_profile` | API |

### `routers.employees.swap_shift` (3)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/swap_shift/shifts` | `get_shifts_for_swap` | API |
| GET | `/api/swap_shift/employees_by_shift/{shift_id}` | `get_employees_by_shift` | API |
| POST | `/api/swap_shift/swap` | `swap_employee_shifts` | API |

### `routers.evaluations.commit_evaluation` (2)

| Method | Path | Handler | Type |
|---|---|---|---|
| POST | `/admin/commit_evaluation/get_commit_quantity_evaluation` | `get_commit_quantity_evaluation_admin` | API |
| POST | `/super_admin/commit_evaluation/get_commit_quantity_evaluation` | `get_commit_quantity_evaluation_super_admin` | API |

### `routers.evaluations.core` (6)

| Method | Path | Handler | Type |
|---|---|---|---|
| POST | `/api/evaluations/{employee_id}/complete` | `complete_evaluation` | API |
| PUT | `/api/evaluations/{employee_id}/interval` | `change_interval` | API |
| PUT | `/api/evaluations/{employee_id}/next-date` | `set_next_date` | API |
| GET | `/api/evaluations/history/{employee_id}` | `history` | API |
| GET | `/api/evaluations/list` | `list_evaluations` | API |
| GET | `/api/evaluations/dashboard-stats` | `dashboard_stats` | API |

### `routers.extra_work.approval` (6)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/admin/extra_work/approval/{work_id}/data` | `get_approval_data_admin` | API |
| POST | `/admin/extra_work/approval/{work_id}/action` | `extra_work_action_admin` | API |
| GET | `/super_admin/extra_work/approval/{work_id}/data` | `get_approval_data_super_admin` | API |
| POST | `/super_admin/extra_work/approval/{work_id}/action` | `extra_work_action_super_admin` | API |
| GET | `/employee/extra_work/approval/{work_id}/data` | `get_approval_data_employee` | API |
| POST | `/employee/extra_work/approval/{work_id}/action` | `extra_work_action_employee` | API |

### `routers.extra_work.directory` (2)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/admin/extra_work_directory` | `get_extra_work_directory_data` | API |
| POST | `/api/admin/extra_work_directory/update` | `update_extra_work` | API |

### `routers.extra_work.inbox` (5)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/admin/extra_work/inbox/data` | `get_inbox_data_admin` | API |
| DELETE | `/admin/extra_work/inbox/clear` | `clear_inbox_admin` | API |
| GET | `/super_admin/extra_work/inbox/data` | `get_inbox_data_super_admin` | API |
| DELETE | `/super_admin/extra_work/inbox/clear` | `clear_inbox_super_admin` | API |
| GET | `/employee/extra_work/inbox/data` | `get_inbox_data_employee` | API |

### `routers.extra_work.legacy` (4)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/admin/extra-work/pending` | `get_pending_extra_work` | API |
| POST | `/api/admin/extra-work/{extra_work_id}/approve` | `approve_extra_work` | API |
| GET | `/api/admin/extra-work/employee/{employee_id}` | `get_employee_extra_work` | API |
| GET | `/api/admin/extra-work/my-extra-work` | `get_my_extra_work` | API |

### `routers.integrations.google_calendar` (16)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/google-calendar/status` | `get_calendar_status` | API |
| GET | `/api/google-calendar/auth-url` | `get_auth_url` | API |
| GET | `/api/google-calendar/callback` | `oauth_callback` | API |
| GET | `/api/google-calendar/meetings` | `get_upcoming_meetings` | API |
| POST | `/api/google-calendar/disconnect` | `disconnect_calendar` | API |
| POST | `/api/google-calendar/create-meeting` | `create_meeting` | API |
| PUT | `/api/google-calendar/update-meeting/{event_id}` | `update_meeting` | API |
| DELETE | `/api/google-calendar/delete-meeting/{event_id}` | `delete_meeting` | API |
| GET | `/api/google-calendar/get-event/{event_id}` | `get_event` | API |
| GET | `/api/google-calendar/attendees` | `get_meeting_attendees` | API |
| POST | `/api/google-calendar/check-conflicts` | `check_conflicts` | API |
| POST | `/api/google-calendar/day-schedule` | `day_schedule` | API |
| GET | `/api/google-calendar/templates` | `list_templates` | API |
| POST | `/api/google-calendar/templates` | `save_template` | API |
| DELETE | `/api/google-calendar/templates/{template_id}` | `delete_template` | API |
| POST | `/api/google-calendar/find-best-times` | `find_best_times` | API |

### `routers.leave.approval` (9)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/admin/leave_request/approval/{leave_id}/data` | `get_approval_page_data_admin` | API |
| POST | `/admin/leave_request/approval/{leave_id}/action` | `leave_approval_action_admin` | API |
| POST | `/admin/leave_request/approval/{leave_id}/edit` | `edit_leave_request_admin` | API |
| GET | `/super_admin/leave_request/approval/{leave_id}/data` | `get_approval_page_data_super_admin` | API |
| POST | `/super_admin/leave_request/approval/{leave_id}/action` | `leave_approval_action_super_admin` | API |
| POST | `/super_admin/leave_request/approval/{leave_id}/edit` | `edit_leave_request_super_admin` | API |
| GET | `/employee/leave_request/approval/{leave_id}/data` | `get_approval_page_data_employee` | API |
| POST | `/employee/leave_request/approval/{leave_id}/action` | `leave_approval_action_employee` | API |
| POST | `/employee/leave_request/approval/{leave_id}/edit` | `edit_leave_request_employee` | API |

### `routers.leave.cancellation` (9)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/admin/leave_cancellation_inbox/data` | `get_inbox_data_admin` | API |
| POST | `/admin/leave_cancellation_inbox/{cancellation_id}/action` | `handle_cancellation_action_admin` | API |
| DELETE | `/admin/leave_cancellation_inbox/clear` | `clear_inbox_admin` | API |
| GET | `/super_admin/leave_cancellation_inbox/data` | `get_inbox_data_super_admin` | API |
| POST | `/super_admin/leave_cancellation_inbox/{cancellation_id}/action` | `handle_cancellation_action_super_admin` | API |
| DELETE | `/super_admin/leave_cancellation_inbox/clear` | `clear_inbox_super_admin` | API |
| GET | `/employee/leave_cancellation_inbox/data` | `get_inbox_data_employee` | API |
| POST | `/employee/leave_cancellation_inbox/{cancellation_id}/action` | `handle_cancellation_action_employee` | API |
| DELETE | `/employee/leave_cancellation_inbox/clear` | `clear_inbox_employee` | API |

### `routers.leave.employee` (18)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/employee/leave-request/leave-types` | `get_leave_types` | API |
| GET | `/api/employee/leave-request/calculate-days` | `calculate_leave_days_endpoint` | API |
| GET | `/api/employee/leave-request/balance` | `get_leave_balance` | API |
| POST | `/api/employee/leave-request/submit` | `submit_leave_request` | API |
| GET | `/api/employee/leave-request/my-requests` | `get_my_leave_requests` | API |
| DELETE | `/api/employee/leave-request/cancel/{leave_id}` | `cancel_leave_request` | API |
| GET | `/api/employee/leave-request/{leave_id}/status` | `get_leave_approval_status` | API |
| GET | `/api/employee/leave-request/history` | `get_leave_request_history` | API |
| GET | `/api/employee/leave-request/{leave_id}` | `get_leave_request` | API |
| GET | `/employee/leave-request/leave-types` | `get_leave_types` | API |
| GET | `/employee/leave-request/calculate-days` | `calculate_leave_days_endpoint` | API |
| GET | `/employee/leave-request/balance` | `get_leave_balance` | API |
| POST | `/employee/leave-request/submit` | `submit_leave_request` | API |
| GET | `/employee/leave-request/my-requests` | `get_my_leave_requests` | API |
| DELETE | `/employee/leave-request/cancel/{leave_id}` | `cancel_leave_request` | API |
| GET | `/employee/leave-request/{leave_id}/status` | `get_leave_approval_status` | API |
| GET | `/employee/leave-request/history` | `get_leave_request_history` | API |
| GET | `/employee/leave-request/{leave_id}` | `get_leave_request` | API |

### `routers.leave.inbox` (17)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/admin/leave_request/inbox/data` | `get_inbox_data_admin` | API |
| DELETE | `/admin/leave_request/inbox/clear` | `clear_inbox_admin` | API |
| GET | `/admin/leave_request/search-employees` | `_search` | API |
| GET | `/admin/leave_request/employee-leave-info/{employee_id}` | `_emp_info` | API |
| GET | `/admin/leave_request/calculate-leave-days` | `_calc_days` | API |
| POST | `/admin/leave_request/create-leave` | `_create` | API |
| GET | `/super_admin/leave_request/inbox/data` | `get_inbox_data_super_admin` | API |
| DELETE | `/super_admin/leave_request/inbox/clear` | `clear_inbox_super_admin` | API |
| GET | `/super_admin/leave_request/search-employees` | `_search` | API |
| GET | `/super_admin/leave_request/employee-leave-info/{employee_id}` | `_emp_info` | API |
| GET | `/super_admin/leave_request/calculate-leave-days` | `_calc_days` | API |
| POST | `/super_admin/leave_request/create-leave` | `_create` | API |
| GET | `/employee/leave_request/inbox/data` | `get_inbox_data_employee` | API |
| GET | `/employee/leave_request/search-employees` | `_search` | API |
| GET | `/employee/leave_request/employee-leave-info/{employee_id}` | `_emp_info` | API |
| GET | `/employee/leave_request/calculate-leave-days` | `_calc_days` | API |
| POST | `/employee/leave_request/create-leave` | `_create` | API |

### `routers.leave.legacy` (8)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/leaves/types` | `get_leave_types` | API |
| GET | `/api/leaves/balance` | `get_leave_balance` | API |
| POST | `/api/leaves/apply` | `apply_leave` | API |
| GET | `/api/leaves/my-leaves` | `get_my_leaves` | API |
| GET | `/api/leaves/pending` | `get_pending_leaves` | API |
| POST | `/api/leaves/{leave_id}/approve` | `approve_leave` | API |
| POST | `/api/leaves/{leave_id}/reject` | `reject_leave` | API |
| GET | `/api/leaves/on-leave-today` | `get_on_leave_today` | API |

### `routers.master_data.core` (18)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/master-data/departments` | `get_departments` | API |
| GET | `/api/master-data/departments/{department_id}` | `get_department` | API |
| POST | `/api/master-data/departments` | `create_department` | API |
| PUT | `/api/master-data/departments/{department_id}` | `update_department` | API |
| DELETE | `/api/master-data/departments/{department_id}` | `delete_department` | API |
| GET | `/api/master-data/teams` | `get_teams` | API |
| GET | `/api/master-data/teams/{team_id}` | `get_team` | API |
| POST | `/api/master-data/teams` | `create_team` | API |
| PUT | `/api/master-data/teams/{team_id}` | `update_team` | API |
| DELETE | `/api/master-data/teams/{team_id}` | `delete_team` | API |
| GET | `/api/master-data/offices` | `get_offices` | API |
| POST | `/api/master-data/offices` | `create_office` | API |
| GET | `/api/master-data/designations` | `get_designations` | API |
| POST | `/api/master-data/designations` | `create_designation` | API |
| GET | `/api/master-data/shifts` | `get_shifts` | API |
| POST | `/api/master-data/shifts` | `create_shift` | API |
| GET | `/api/master-data/working-from` | `get_working_from` | API |
| GET | `/api/master-data/summary` | `get_master_data_summary` | API |

### `routers.master_data.holidays` (2)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/yearly-holiday-info/holiday-sets` | `get_holiday_sets` | API |
| GET | `/yearly-holiday-info/data` | `get_yearly_holiday_data` | API |

### `routers.master_data.settings` (6)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/settings/office-hours` | `get_office_hours` | API |
| POST | `/api/settings/office-hours` | `update_office_hours` | API |
| GET | `/api/settings/timezone-list` | `get_timezone_list` | API |
| GET | `/api/settings/smtp-settings` | `get_smtp_settings` | API |
| POST | `/api/settings/smtp-settings` | `update_smtp_settings` | API |
| POST | `/api/settings/smtp-settings/test` | `test_smtp_settings` | API |

### `routers.question_builder.admin_question_builder` (16)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/admin/question-builder/api/questions` | `get_all_questions` | API |
| GET | `/admin/question-builder/api/questions/{question_id}` | `get_question` | API |
| POST | `/admin/question-builder/api/questions` | `create_question` | API |
| PUT | `/admin/question-builder/api/questions/{question_id}` | `update_question` | API |
| DELETE | `/admin/question-builder/api/questions/{question_id}` | `delete_question` | API |
| POST | `/admin/question-builder/api/questions/reorder` | `reorder_questions` | API |
| POST | `/admin/question-builder/api/questions/{question_id}/activate` | `activate_question` | API |
| GET | `/admin/question-builder/api/stats` | `get_question_stats` | API |
| GET | `/super_admin/question-builder/api/questions` | `get_all_questions_super_admin` | API |
| GET | `/super_admin/question-builder/api/questions/{question_id}` | `get_question_super_admin` | API |
| POST | `/super_admin/question-builder/api/questions` | `create_question_super_admin` | API |
| PUT | `/super_admin/question-builder/api/questions/{question_id}` | `update_question_super_admin` | API |
| DELETE | `/super_admin/question-builder/api/questions/{question_id}` | `delete_question_super_admin` | API |
| POST | `/super_admin/question-builder/api/questions/reorder` | `reorder_questions_super_admin` | API |
| POST | `/super_admin/question-builder/api/questions/{question_id}/activate` | `activate_question_super_admin` | API |
| GET | `/super_admin/question-builder/api/stats` | `get_question_stats_super_admin` | API |

### `routers.rbac.audit_log` (6)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/rbac/audit-logs/page-data` | `audit_logs_page_data` | API |
| GET | `/rbac/audit-logs` | `list_audit_logs` | API |
| GET | `/rbac/audit-logs/{log_id}` | `get_audit_log` | API |
| GET | `/rbac/audit-logs/stats/summary` | `get_audit_stats` | API |
| GET | `/rbac/audit-logs/filters/entity-types` | `get_entity_types` | API |
| DELETE | `/rbac/audit-logs/clear` | `clear_all_audit_logs` | API |

### `routers.rbac.management` (19)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/rbac/permissions` | `list_permissions` | API |
| POST | `/api/rbac/permissions` | `create_permission` | API |
| PUT | `/api/rbac/permissions/{permission_id}` | `update_permission` | API |
| DELETE | `/api/rbac/permissions/{permission_id}` | `delete_permission` | API |
| GET | `/api/rbac/roles` | `list_roles` | API |
| GET | `/api/rbac/roles/{role_id}` | `get_role_details` | API |
| POST | `/api/rbac/roles` | `create_role` | API |
| PUT | `/api/rbac/roles/{role_id}` | `update_role` | API |
| DELETE | `/api/rbac/roles/{role_id}` | `delete_role` | API |
| POST | `/api/rbac/roles/{role_id}/permissions` | `assign_permissions_to_role` | API |
| POST | `/api/rbac/roles/{role_id}/permissions/by-code` | `assign_permissions_by_code` | API |
| DELETE | `/api/rbac/roles/{role_id}/permissions` | `remove_permissions_from_role` | API |
| GET | `/api/rbac/roles/{role_id}/permissions` | `get_role_permissions` | API |
| GET | `/api/rbac/page-data` | `rbac_page_data` | API |
| GET | `/api/rbac/users/search` | `search_users` | API |
| GET | `/api/rbac/users/{user_id}/roles` | `get_user_roles` | API |
| POST | `/api/rbac/users/{user_id}/roles` | `assign_roles_to_user` | API |
| POST | `/api/rbac/users/{user_id}/roles/{role_id}` | `add_single_role_to_user` | API |
| DELETE | `/api/rbac/users/{user_id}/roles/{role_id}` | `remove_role_from_user` | API |

### `routers.reports.core` (3)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/admin/attendance/reports/daily` | `get_daily_report` | API |
| GET | `/api/admin/attendance/reports/monthly` | `get_monthly_report` | API |
| GET | `/api/admin/attendance/reports/summary` | `get_summary_report` | API |

### `routers.reports.leave_record` (3)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/reports/leave-record/monthly` | `get_monthly_leave_record` | API |
| GET | `/api/reports/leave-record/entries` | `get_leave_ledger_entries` | API |
| GET | `/api/reports/leave-record/reconcile` | `reconcile_leave_ledger` | API |

### `routers.utilities.claims_config` (4)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/max-claim-configs` | `get_max_claim_configs` | API |
| POST | `/api/max-claim-configs` | `create_max_claim_config` | API |
| PUT | `/api/max-claim-configs/{config_id}` | `update_max_claim_config` | API |
| DELETE | `/api/max-claim-configs/{config_id}` | `delete_max_claim_config` | API |

### `routers.utilities.departments` (16)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/departments` | `get_departments` | API |
| POST | `/api/departments` | `create_department` | API |
| PUT | `/api/departments/{department_id}` | `update_department` | API |
| DELETE | `/api/departments/{department_id}` | `delete_department` | API |
| GET | `/api/designations` | `get_designations` | API |
| POST | `/api/designations` | `create_designation` | API |
| PUT | `/api/designations/{designation_id}` | `update_designation` | API |
| DELETE | `/api/designations/{designation_id}` | `delete_designation` | API |
| GET | `/api/teams` | `get_teams` | API |
| POST | `/api/teams` | `create_team` | API |
| PUT | `/api/teams/{team_id}` | `update_team` | API |
| DELETE | `/api/teams/{team_id}` | `delete_team` | API |
| GET | `/api/offices` | `get_offices` | API |
| POST | `/api/offices` | `create_office` | API |
| PUT | `/api/offices/{office_id}` | `update_office` | API |
| DELETE | `/api/offices/{office_id}` | `delete_office` | API |

### `routers.utilities.holidays` (15)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/holiday-sets` | `get_holiday_sets` | API |
| POST | `/api/holiday-sets` | `create_holiday_set` | API |
| PUT | `/api/holiday-sets/{holiday_set_id}` | `update_holiday_set` | API |
| DELETE | `/api/holiday-sets/{holiday_set_id}` | `delete_holiday_set` | API |
| GET | `/api/yearly-holidays` | `get_yearly_holidays` | API |
| POST | `/api/yearly-holidays` | `create_yearly_holiday` | API |
| PUT | `/api/yearly-holidays/{holiday_id}` | `update_yearly_holiday` | API |
| DELETE | `/api/yearly-holidays/{holiday_id}` | `delete_yearly_holiday` | API |
| GET | `/api/working-day-exceptions` | `get_working_day_exceptions` | API |
| POST | `/api/working-day-exceptions` | `create_working_day_exception` | API |
| DELETE | `/api/working-day-exceptions/{exception_id}` | `delete_working_day_exception` | API |
| GET | `/api/weekends` | `get_weekends` | API |
| POST | `/api/weekends` | `create_weekend` | API |
| PUT | `/api/weekends/{weekend_id}` | `update_weekend` | API |
| DELETE | `/api/weekends/{weekend_id}` | `delete_weekend` | API |

### `routers.utilities.misc` (9)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/utilities-dashboard/data` | `utilities_dashboard_data` | API |
| GET | `/api/leave-balances/years` | `get_leave_balance_years` | API |
| GET | `/api/leave-balances` | `get_leave_balances` | API |
| POST | `/api/leave-balances` | `create_leave_balance` | API |
| PUT | `/api/leave-balances/{balance_id}` | `update_leave_balance` | API |
| DELETE | `/api/leave-balances/{balance_id}` | `delete_leave_balance` | API |
| GET | `/api/google-calendar/countries` | `get_available_countries` | API |
| GET | `/api/google-calendar/holidays/{country}` | `get_country_holidays` | API |
| POST | `/api/google-calendar/clear-cache` | `clear_holiday_cache` | API |

### `routers.utilities.onboarding` (3)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/user-onboarding-status` | `get_user_onboarding_statuses` | API |
| PUT | `/api/user-onboarding-status/{status_id}` | `update_user_onboarding_status` | API |
| DELETE | `/api/user-onboarding-status/{status_id}` | `delete_user_onboarding_status` | API |

### `routers.utilities.restrictions` (13)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/work-locations` | `get_work_locations` | API |
| POST | `/api/work-locations` | `create_work_location` | API |
| PUT | `/api/work-locations/{work_location_id}` | `update_work_location` | API |
| DELETE | `/api/work-locations/{work_location_id}` | `delete_work_location` | API |
| GET | `/api/ip-addresses` | `get_ip_addresses` | API |
| POST | `/api/ip-addresses` | `create_ip_address` | API |
| PUT | `/api/ip-addresses/{ip_address_id}` | `update_ip_address` | API |
| DELETE | `/api/ip-addresses/{ip_address_id}` | `delete_ip_address` | API |
| GET | `/api/restrictions` | `get_all_restrictions` | API |
| GET | `/api/restrictions/search-employees` | `search_employees_for_restrictions` | API |
| POST | `/api/restrictions` | `create_restriction` | API |
| PUT | `/api/restrictions/{restriction_id}` | `update_restriction` | API |
| DELETE | `/api/restrictions/{restriction_id}` | `delete_restriction` | API |

### `routers.utilities.settings` (12)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/email-configs` | `get_email_configs` | API |
| POST | `/api/email-configs` | `create_email_config` | API |
| PUT | `/api/email-configs/{email_config_id}` | `update_email_config` | API |
| DELETE | `/api/email-configs/{email_config_id}` | `delete_email_config` | API |
| GET | `/api/timezones` | `get_timezones` | API |
| POST | `/api/timezones` | `create_timezone` | API |
| PUT | `/api/timezones/{timezone_id}` | `update_timezone` | API |
| DELETE | `/api/timezones/{timezone_id}` | `delete_timezone` | API |
| GET | `/api/email-config-recipients` | `get_email_config_recipients` | API |
| POST | `/api/email-config-recipients` | `create_email_config_recipient` | API |
| PUT | `/api/email-config-recipients/{config_id}` | `update_email_config_recipient` | API |
| DELETE | `/api/email-config-recipients/{config_id}` | `delete_email_config_recipient` | API |

### `routers.utilities.shifts` (4)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/api/shifts` | `get_shifts` | API |
| POST | `/api/shifts` | `create_shift` | API |
| PUT | `/api/shifts/{shift_id}` | `update_shift` | API |
| DELETE | `/api/shifts/{shift_id}` | `delete_shift` | API |

### `routers.wfh.approval` (9)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/admin/wfh_request/approval/{wfh_id}/data` | `get_approval_page_data_admin` | API |
| POST | `/admin/wfh_request/approval/{wfh_id}/action` | `wfh_approval_action_admin` | API |
| POST | `/admin/wfh_request/approval/{wfh_id}/edit` | `edit_wfh_request_admin` | API |
| GET | `/super_admin/wfh_request/approval/{wfh_id}/data` | `get_approval_page_data_super_admin` | API |
| POST | `/super_admin/wfh_request/approval/{wfh_id}/action` | `wfh_approval_action_super_admin` | API |
| POST | `/super_admin/wfh_request/approval/{wfh_id}/edit` | `edit_wfh_request_super_admin` | API |
| GET | `/employee/wfh_request/approval/{wfh_id}/data` | `get_approval_page_data_employee` | API |
| POST | `/employee/wfh_request/approval/{wfh_id}/action` | `wfh_approval_action_employee` | API |
| POST | `/employee/wfh_request/approval/{wfh_id}/edit` | `edit_wfh_request_employee` | API |

### `routers.wfh.employee` (4)

| Method | Path | Handler | Type |
|---|---|---|---|
| POST | `/employee/wfh_request/submit` | `submit_wfh_request` | API |
| GET | `/employee/wfh_request/history` | `get_wfh_history` | API |
| GET | `/employee/wfh_request/{wfh_id}` | `get_wfh_request` | API |
| DELETE | `/employee/wfh_request/cancel/{wfh_id}` | `cancel_wfh_request` | API |

### `routers.wfh.inbox` (3)

| Method | Path | Handler | Type |
|---|---|---|---|
| GET | `/admin/wfh_request/inbox/data` | `get_inbox_data_admin` | API |
| GET | `/super_admin/wfh_request/inbox/data` | `get_inbox_data_super_admin` | API |
| GET | `/employee/wfh_request/inbox/data` | `get_inbox_data_employee` | API |
