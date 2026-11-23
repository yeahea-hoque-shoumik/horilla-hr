# Apurba HRM → Horilla HRMS: Integration & Data Migration Plan

Prepared 2026-11-04. Status: **plan only**. No code has been changed yet.

**Inputs**
- `docs/APURBA_HRM_APPLICATION_FEATURE_REFERENCE.md`: Apurba HRM v2, `master` @ `6dd2884`.
- `docs/Horilla_HRM_FEATURES.md`: Horilla 2.2.0, branch `2.0`.
- `docs/ApurbApurba_HRM-v2_vs_Horilla_HRMS—Feature_Comparison.md`.
- A read of the Horilla source in this repo. File and line references below point at that code.

**Goal:** run ApurbaTech's HR on Horilla. That means two things:
1. Rebuild the Apurba features that Horilla lacks, or does differently, so that HR policy stays the same.
2. Move all of Apurba's live and historical data into Horilla, with a parallel run before the switch.

---

## Contents

1. [Summary](#1-summary)
2. [Decisions](#2-decisions)
3. [Gap map: Apurba feature → Horilla](#3-gap-map-apurba-feature--horilla)
4. [Target design](#4-target-design)
5. [Phases, tasks and steps](#5-phases-tasks-and-steps)
6. [Data migration](#6-data-migration)
7. [Parallel run and cutover](#7-parallel-run-and-cutover)
8. [Cross-cutting rules](#8-cross-cutting-rules)
9. [Risks](#9-risks)
10. [Appendix A: effort and dependencies](#appendix-a-effort-and-dependencies)
11. [Appendix B: ledger events and where Horilla emits them](#appendix-b-ledger-events-and-where-horilla-emits-them)
12. [Appendix C: starter permission mapping](#appendix-c-starter-permission-mapping)

---

## 1. Summary

- **Target platform is Horilla.** Apurba's features are added as **new first-party Django apps**, plus small hooks in Horilla's core apps (`leave`, `attendance`, `base`, `horilla_api`). Keeping the hooks small keeps future upstream merges manageable.
- **The core work is attendance and leave policy:**
  - an append-only leave ledger
  - per-employee timezone
  - Apurba's clock-in/out and penalty rules
  - attendance claims with a monthly quota
  - approver assignments with levels and effective dates
  - WFH requests
- **Peripheral features follow:** the onboarding quiz gate, Google sign-in, the calendar best-time finder, AI commit evaluation, the external summary API, the PWA and the ZKTeco ADMS push receiver.
- **Migration** uses a repeatable, idempotent management command, `import_apurba`. It reads a read-only copy of the Apurba PostgreSQL database and upserts into Horilla through an ID-map table, so it can run many times during the parallel run, followed by a final delta at cutover.
- **Sequence:** P0 foundations → P1 people and org → P2 leave → P3 attendance → P4 approvals and WFH → P5 reports → P6 peripheral features (in parallel from P1) → P7 parallel run → P8 cutover.
- **Rough size:** 26–40 person-weeks of build, plus a 4–6 week parallel run (Appendix A).

---

## 2. Decisions

### 2.1 Confirmed

| # | Decision | Effect |
|---|---|---|
| D1 | Port **all** Apurba-only or deeper features | Every row in §3 has a phase |
| D2 | **Parallel run, then cutover** | The import is idempotent and re-runnable. Horilla's penalty jobs run in compare mode during the parallel run (§7) |
| D3 | **Two Horilla companies: BD and USA** | Each has its own weekly offs (`CompanyLeaves`), holidays, allowed IPs, leave types, mail server and timezone default. Uses Horilla's company-scoped managers and permissions |
| D4 | **Leave balances may go negative** | The ledger writer does not clamp. Forms, validators and the penalty signal must stop clamping at 0 (`base/signals.py:62` `create_deduction_cutleave_from_penalty`) |

### 2.2 Open: recommended default shown, confirm before the phase starts

| # | Question | Recommended default | Needed by |
|---|---|---|---|
| O1 | Approval semantics | Apurba's: **level 1 (or a Super Admin / `approve` holder) finalises; levels 2+ are advisory remarks**. Horilla's condition-based chain stays available for companies that want it | P4 |
| O2 | Who sees approval inboxes | Assigned approvers see their assignees. HR users with the Django view permission still see everything in their company (Horilla's behaviour) | P4 |
| O3 | National ID / TIN | Store in encrypted fields (Fernet key from env) on the new employee-policy model, behind a dedicated permission. Decrypt with Apurba's key during import | P1 |
| O4 | Work-hours deficit | Apurba only **reports** `leaves to deduct` and does not deduct automatically. Keep it report-only; HR applies the deduction as an `ADMIN_ADJUSTMENT` | P3 |
| O5 | External summary API auth | Hashed **API key per client** (`ServiceClient`), scoped and throttled. Apurba's response shape is kept. A Basic-auth shim on that one path only if a consumer can't change | P6 |
| O6 | Biometric devices | Port Apurba's **ADMS push receiver** (`/iclock/*`) into `biometric` as a new device type. Horilla only has pull/live-capture today | P6 |
| O7 | Google Calendar tokens | Don't migrate them; users reconnect. Meeting templates are migrated | P6 |
| O8 | Annual allowance | Apurba stores a per-employee `total_paid_holiday` (default 15). Add a per-employee allowance override that the yearly reset uses | P2 |
| O9 | Clock-in back-dating | Keep Horilla's "clock in now". Apurba's back-date/future windows apply only to **editing today's times** for Home/non-restricted employees | P3 |
| O10 | Historical depth | Import all attendance, leave and ledger history. Logs go to an archive table, with the last 12 months of `activity_log` | P0 |

---

## 3. Gap map: Apurba feature → Horilla

Legend: **Reuse** = Horilla already does it, so only configure or map. **Extend** = add to an existing Horilla feature. **New** = build it.

| Apurba feature | Horilla today (code) | Approach | Phase |
|---|---|---|---|
| Append-only leave ledger (19 event types, actor, source, idempotent penalties, reconcile) | 30+ places write `AvailableLeave.available_days` / `carryforward_days` directly. `AvailableLeave.build_ledger()` (`leave/models.py:815`) only rebuilds a ledger from history | **New** `leave_ledger` app with a single writer. Refactor every writer to call it | P2 |
| Negative balances | Penalty signal clamps at 0 | **Extend** (D4) | P2 |
| Per-employee timezone ("today" in employee zone) | Only `TIME_ZONE` (`horilla/settings/base.py:376`). `clock_in`/`clock_out` use `date.today()`/`datetime.now()` (`attendance/views/clock_in_out.py:206`, `:474`) | **New** `employee_today()` helper used by web, API and jobs | P3 |
| Multi-region jobs (BD + USA), with no hard-coded shift IDs | One scheduler in the project timezone | **New** jobs that run every 15 min and act per employee local time | P3 |
| PRESENT / LATE / half-day-late at clock-in, 0.5-day deduction | Late/early via `GraceTime` + `AttendanceLateComeEarlyOut` (`late_come`, `clock_in_out.py:73`). `WorkRecords` HDP status | **Extend**: late threshold → `GraceTime` per shift; half-day threshold + ledger event | P3 |
| Office-IP rule vs Home/WFH location | IP check in web clock-in only (`clock_in_out.py` ~228–262). API clock-in skips it. `WorkFrom` has no home/office flag | **Extend**: flags on `WorkFrom`, `wfh_eligible` per employee, the same gate in the API | P3 |
| 18 h span cap, clock-out future window, edit today's times | Not present | **New** validation in `clock_out` + an "edit today" form | P3 |
| Holiday/weekend clock-in → extra work | Compensatory leave requests exist (`is_compensatory_leave`) | **Extend**: confirm dialog → pending compensatory request | P3 |
| Auto 0.5-day extra work when span > 1.5 × shift | Not present (overtime is paid via payroll buckets, `payroll/methods/payslip_calc.py:1106`) | **New**: day-close job | P3 |
| Clock-in on an approved leave day → auto cancellation request | Leave cancellation flow exists (`request_leave_cancellation`, `decide_leave_cancellation` `leave/methods.py:246`) | **Extend**: confirm dialog in clock-in | P3 |
| Mark absent + auto clock-out at 23:59 (biometric time first, clock-out penalty) | `create_work_record` (ABS) and `auto_punch_out` jobs | **Extend**: the day-close job replaces `auto_punch_out` for migrated shifts | P3 |
| Weekly late penalty (3+ lates Mon–Fri = 1 day) | Penalties are manual (`PenaltyAccounts`, `base/models.py:3091`) | **New** job + ledger event | P3 |
| Work-hours deficit → leaves to deduct | Monthly hour account exists (`AttendanceOverTime`, `attendance/models.py:1118`) | **New** `WorkDeficit` + monthly report | P3 / P5 |
| Attendance claims with monthly quota, cutoff day, refund | Attendance requests stored on `Attendance` rows (`is_validate_request`, `requested_data`) | **Extend**: claim policy + checks on create; refund = recount | P3 |
| Column-level attendance audit | auditlog is opt-in per model | **Reuse**: register `Attendance` in `horilla_audit` config | P3 |
| Approver assignment per employee/type, levels, effective dates | Multi-level only for leave (`MultipleApprovalCondition` `base/models.py:2185`, `LeaveRequestConditionApproval` `leave/models.py:2344`). Others use one `reporting_manager_id` (`employee/models.py:945`) | **New** `approval_assignment` app feeding all four request types | P4 |
| Bulk approval assignor (check / replace / merge) | Not present | **New** | P4 |
| Approver history page | Partial (per-request history) | **New**: combined history view | P4 |
| Reporting managers with levels and effective dates | Single `reporting_manager_id` | **New** `ReportingLine` model. Level 1 is synced to `reporting_manager_id` | P1 / P4 |
| WFH requests (date range, half day, attachment, overlap rules) | `WorkFromRequest` (`base/models.py:1451`) + `switch_work_from`/`undo_work_from` (`base/scheduler.py:321`, `:356`) | **Extend**: WFH = request for the "Home" work from, plus the extra fields and rules | P4 |
| Leave on behalf (HR creates, auto-approved) | HR can create, but it is auto-approved only when the type needs no approval | **Extend**: new permission + approve through the ledger | P2 |
| Mandatory emergency contact (another active employee) | `Employee.emergency_contact` is free text (`employee/models.py:123`). `LeaveRequest` has nothing | **Extend**: FK on leave request, required by company setting | P2 |
| Probation: can't apply for leave; auto-promotion to full-time | Probation end only on `Candidate` (`recruitment/models.py`) | **Extend**: probation fields on the employee policy + daily job | P1 / P2 |
| Year-end carry-forward (manual in Apurba) | `leave_reset` job (`leave/scheduler.py`) with carry-forward types | **Reuse + Extend**: writes `CARRY_FORWARD` ledger rows, keeps negatives, uses the per-employee allowance (O8) | P2 |
| Shift swap between two employees | `ShiftRequest.reallocate_to` (`base/models.py:1706`) | **Reuse** | — |
| Working-day exceptions | Not present | **New** `WorkingDayException` | P1 |
| Teams (with lead) | Not present | **New** `Team` model | P1 |
| Clock-in e-mail reminders (2 slots, per shift) | Not present | **New** job, honours email restriction | P3 |
| Negative-leave monthly Excel e-mail | Report subscriptions exist (hourly) | **New** standard report + subscription | P5 |
| Work-hours report, leave-record report + reconcile | 34 standard reports (`report`) | **New** standard reports | P5 |
| Per-event mail recipients (To/CC/BCC per department) | `horilla_automations` (`MailAutomation`) | **Reuse**: one automation per event | P5 |
| Onboarding knowledge quiz gate | Not present. `ForcePasswordChangeMiddleware` (`base/middleware.py:422`) is the pattern to copy | **New** `onboarding_quiz` app | P6 |
| Google sign-in | No social login (Google OAuth is used only by `horilla_meet`/backup) | **New** login view | P6 |
| Google Calendar: meetings, conflicts, day schedule, best-time finder, templates, holiday import | `horilla_meet` creates Calendar events with Meet links (`horilla_meet/methods.py`) | **Extend** `horilla_meet` | P6 |
| AI commit-quantity evaluation + git mapping + evaluations | Not present | **New** `evaluations` app | P6 |
| External attendance summary API | No machine-to-machine auth; Basic is rejected (`horilla_api/auth.py`) | **New** endpoint + API keys (O5) | P6 |
| PWA (manifest + service worker) | Manifest exists (`static/build/manifest.json`), no service worker | **Extend** | P6 |
| ZKTeco SenseFace 2A ADMS push | `biometric` supports ZK pull/live capture; no `/iclock` receiver | **New** device type (O6) | P6 |
| API activity log (all traffic, secrets masked) | Request IDs, auditlog, axes logs | **Optional**: middleware writing a capped log table | P6 |

Features Horilla already has and that need **configuration only**: holidays and weekly offs, half-day leave, working-days-only calculation (leave type `exclude_holiday` / `exclude_company_leave`), cancellation workflow, OTP password reset, RBAC (groups), SMTP accounts, attendance PDF/Excel export, dashboards, org chart.

---

## 4. Target design

### 4.1 New apps

Every new app follows the repo rules:
- models extend `HorillaModel`
- `objects = HorillaCompanyManager(...)`, or an entry in `base/checks.py` `EXEMPT` with a reason
- views use the decorators from `horilla/decorators.py`
- CBVs come from `horilla_views`
- templates live under `horilla_theme/templates/<app>/`
- jobs go in `<app>/scheduler.py` via `register_job`
- tests live in `<app>/tests/`, and the app is added to `SMOKE_LABELS`

| App | Models | Services / jobs |
|---|---|---|
| `leave_ledger` | `LeaveLedgerEntry`: employee, leave type, available_leave FK, event_type, delta_available, delta_carryforward, old/new values, source_type, source_id, attendance_date, actor_user, actor_employee, idempotency_key (unique), note, created_at | `apply_balance_change()`, `record_balance_set()`, `resolve_balance()` (configurable penalty leave-type order per company, which fixes Apurba's "lowest id" rule), reconcile (ledger sum vs balance) |
| `hr_policy` | `EmployeePolicy` (one-to-one Employee): timezone, attendance_restriction, email_restriction, wfh_eligible, attendance_track, employment_period, probation_end, annual_allowance, blood_group, national_id/tin (encrypted). `ShiftPolicy` (one-to-one `EmployeeShift`): late/half-day thresholds, clock-in/out windows, clock_out_penalty, duration_for_one_leave (540), max_span_hours (18), reminder times, day-close time. `WorkFromPolicy` (one-to-one `WorkFrom`): is_office_location, requires_wfh_approval. `Team`, `WorkingDayException`, `ClaimPolicy` (per company: max_claim_count = 2, cutoff_day = 5), `AttendanceClaim` (one-to-one attendance request: reason, source timezone), `WorkDeficit`, `DayCloseLog`, `ReminderLog` | `employee_today(employee)`, `employee_now(employee)`, `is_working_day(employee, date)`, the clock-in decision service, the claim checks. Jobs: `day_close` (every 15 min), `weekly_late_penalty` (hourly, keyed by ISO week), `clock_in_reminders` (every 15 min), `probation_promotion` (daily), `work_deficit_month` (daily, acts on day 1) |
| `approval_assignment` | `ApproverAssignment`: employee, approver, request_type (leave / attendance_claim / extra_work / wfh), level, effective_from/to, is_active. `ReportingLine`: employee, manager, level, effective dates. `ApprovalAction`: request type + id, approver, level, action (approve / reject / remark), remarks, at | `approvers_for(employee, type, on_date)`, `can_finalise()`, `inbox_queryset()`, bulk assignor (check / replace / merge) |
| `onboarding_quiz` | `QuizQuestion`, `QuizOption`, `QuizAnswer` (case_sensitive, trim, partial), `QuizResponse` (attempt_number), `QuizStatus`, `QuizAuditLog` | `OnboardingQuizMiddleware`, placed after `ForcePasswordChangeMiddleware` |
| `evaluations` | `EvaluationRecord`, `GitUsernameMapping` | HRM-AI proxy (`HRM_AI_BASE_URL`, timeout → 504, bad upstream → 502) |
| `apurba_migration` | `MigrationIdMap` (source_table, source_id, content_type, object_id, row_hash, imported_at), `LegacyArchive` (source_table, source_id, payload JSON, occurred_at), `MigrationRun` | The `import_apurba` command and the reconciliation command (§6) |

The policy models are **one-to-one side tables**, not `_inherit` field injection, so Horilla's own migrations and tables stay untouched. Use `_inherit` only if a field must appear in existing Horilla forms or filters without extra code.

### 4.2 Hooks in existing apps

| Where | Hook |
|---|---|
| `leave` | Every balance write goes through `leave_ledger.apply_balance_change` (list in §5 P2). New fields: `emergency_contact_employee` and `created_on_behalf`. Probation block in the self-service forms and the API |
| `attendance/views/clock_in_out.py` | Call the clock-in decision service from `clock_in`/`clock_out`. Replace `date.today()`/`datetime.now()` with `employee_today/now`. Add confirm dialogs (HTMX) for holiday/weekend and approved leave |
| `horilla_api/api_views/attendance/views.py` | `ClockInAPIView`/`ClockOutAPIView` use the same service, so the IP/WFH gate applies to mobile too |
| `base` (`WorkFromRequest`) | WFH fields and rules. `switch_work_from`/`undo_work_from` stay as they are |
| Approval views (leave approve `leave/views.py:1044`, attendance request approve, compensatory approve, work-from approve) | `approval_assignment.can_finalise()` + `ApprovalAction` rows. Inbox querysets filtered by `inbox_queryset()` |
| `horilla_meet` | Free/busy best-time finder, conflict check, day schedule, `MeetingTemplate`, public-holiday import into `Holidays` |
| `biometric` | ADMS device type and `/iclock/cdata`, `/iclock/getrequest`, `/iclock/devicecmd`. PIN = `badge_id`. Punches go through the existing `clock_in`/`clock_out` request pattern used by the other device types in `biometric/views.py` |
| `base` login | "Sign in with Google" button + callback. The user is matched by stored Google id or verified e-mail, then logged in normally so axes, 2FA and forced password change still apply |
| `horilla_api` | `/api/external/attendance/summary/` with `ServiceClientAuthentication` (O5) |
| `report` | Standard reports: Negative Leave, Work Hours & Deficit, Leave Record + Reconcile, Claim Usage |
| Shared helper (new, `horilla/context.py`) | `run_as(user, company)` context manager. It replaces the duplicated `_as_request()` in `payroll/management/commands/create_payroll_fixtures.py:672` and `base/management/commands/create_branch_demo_fixtures.py:4934`, and calls `set_selected_company` (`horilla/horilla_middlewares.py:141`). Used by jobs and the importer |

### 4.3 How the timezone-aware jobs work

Horilla's `run_scheduler` runs one scheduler in the project timezone (`TIME_ZONE=Asia/Dhaka` after P0). Apurba runs separate jobs at 23:59 Dhaka and 23:59 New York, each with hard-coded shift IDs. In Horilla:

- `day_close` runs every 15 minutes. For each active, tracked employee it computes the local time from `EmployeePolicy.timezone` (falling back to the shift timezone, then the company default).
- When local time passes the shift's day-close time **and** there is no `DayCloseLog(employee, date)`, it does the day-close work in one transaction:
  - mark absent
  - auto clock-out
  - apply penalties
  - create auto extra-work
  - write the log row
- Every penalty uses a ledger `idempotency_key`, so a re-run never double-charges.
- Reminders and the weekly late penalty use the same pattern.
- This removes `constants/scheduler_shifts.py`. A new shift needs only data, not a code change.

---

## 5. Phases, tasks and steps

Each phase ends with its exit criteria met, CI green (Postgres, `makemigrations --check`, coverage floor) and a CHANGELOG entry. Work happens on branches off `dev/v2.0`.

### P0: Foundations and decisions (1–2 weeks)

**Goal:** the decisions are final, there is a staging environment with a copy of the Apurba data, and the empty app skeletons exist.

1. **Decisions**
   1. Confirm O1–O10 with HR and the owners (§2.2).
   2. Write the **policy sign-off sheet**: every Apurba rule from reference §4.6–4.15 with "keep / change / drop". This sheet becomes the source for the test cases.
   3. Fill the role → group and permission mapping sheet (Appendix C).
2. **Environments**
   1. Create a staging Horilla (separate DB, `HORILLA_ENV=staging`) next to the current production checkout. Don't reuse the production DB on this host.
   2. Restore a `pg_dump` of Apurba into a **read-only** staging database. Create a read-only role for the importer.
   3. Measure the data volume (rows per table, attendance per year, ledger rows) so that batch sizes and import time can be planned.
   4. Collect the secrets the import needs: the Apurba encryption key for NID/TIN, file-service access for photos, SMTP credentials.
3. **Platform settings**
   1. `TIME_ZONE=Asia/Dhaka`.
   2. Add `bcrypt` to `requirements.txt` and add `django.contrib.auth.hashers.BCryptPasswordHasher` to `PASSWORD_HASHERS`, **after** PBKDF2. Migrated users can then log in with their old password, and Django re-hashes it to PBKDF2 on first login.
   3. Run `pip-audit` on the new dependency.
4. **Skeletons**
   1. Create the apps `leave_ledger`, `hr_policy`, `approval_assignment`, `onboarding_quiz`, `evaluations` and `apurba_migration`: `apps.py`, empty models, `tests/`, and entries in `SMOKE_LABELS`.
   2. Add `horilla/context.py` with `run_as()`, and refactor the two `_as_request()` copies to use it.
5. **Companies:** create the **BD** and **USA** companies, and an HR admin group assignment in both.

**Exit:** decisions signed off; staging up; the importer can connect read-only; the skeleton apps pass `manage.py check --tag horilla.tenancy`.

### P1: People, org structure and the first import (2–3 weeks)

**Goal:** every Apurba employee can log in to staging Horilla with their own password and sees correct org data.

1. **Models (`hr_policy`):** `EmployeePolicy`, `ShiftPolicy`, `WorkFromPolicy`, `Team`, `WorkingDayException`. Admin screens use `HorillaListView`/`HorillaFormView`, under Settings → Attendance / Organization.
2. **`approval_assignment.ReportingLine`:** a signal syncs the active level-1 line to `EmployeeWorkInformation.reporting_manager_id`. Add an org-hierarchy view by level.
3. **Probation:** `probation_end` + `employment_period` on the policy, and the daily `probation_promotion` job (switches `employee_type_id` to Full-Time on the day).
4. **Importer, phases `config`, `org`, `people`** (§6.3 rows 1–30). Steps:
   1. `MigrationIdMap` upsert helper and row hashing.
   2. Mapping of companies by region (office / holiday set → BD or USA).
   3. Users: hash with the `bcrypt$` prefix, `is_new_employee=False`; users with no password get an unusable password.
   4. Employee + work info + policy. `badge_id = employee_code`.
   5. Photos downloaded from the file service into media.
   6. NID/TIN decrypted, then re-encrypted (O3).
   7. Groups and `CompanyGroupAssignment` from roles; Super Admin → `is_superuser`.
5. **Dry run** on staging, then a fix → re-run loop until the counts reconcile (§6.5 checks 1–3).

**Tests:** policy defaults; probation job; ReportingLine sync; importer unit tests on a fixture source (a small SQL dump in `apurba_migration/tests/fixtures/`); a login with a migrated bcrypt hash.

**Exit:** 100 % of active employees imported; spot-checked by HR; logins work.

### P2: Leave ledger and leave rules (3–4 weeks)

**Goal:** every leave balance change is a ledger row, and Apurba's leave rules hold.

1. **Ledger core (`leave_ledger`)**
   1. `LeaveLedgerEntry` + `apply_balance_change(available_leave, *, delta_available, delta_carryforward=0, event, source, actor, attendance_date=None, idempotency_key=None)`. It runs inside `transaction.atomic()` + `select_for_update()` on the `AvailableLeave` row, writes old/new values, and skips silently on a duplicate idempotency key (it returns the existing row).
   2. A single deduction-order rule. Today the web approve path takes carry-forward first (`leave/views.py:1044` `leave_request_approve`) while `no_approval()` (`leave/models.py:1982`) and the create paths take available first. Pick one (recommended: carry-forward first, so expiring days go first) and store the split on the request (`approved_available_days` / `approved_carryforward_days` already exist).
   3. Allow negative values (D4): check the field validators, forms (`AvailableLeaveUpdateForm`) and serializers.
2. **Refactor every balance writer** to the ledger, one PR per group, each with a regression test:
   - leave approve, reject and cancellation: `leave/views.py` `leave_request_approve` (1044), `_reject_leave_request` (1281); `leave/methods.py:246` `decide_leave_cancellation`
   - auto-approve on create: `leave_request_creation`, `user_leave_request`, `leave_request_create` in `leave/views.py`; `leave/cbv/leave_requests.py` and `leave/cbv/my_leave_request.py`; `LeaveRequest.no_approval()`
   - assign, import and manual edit: `leave_assign_one`, `leave_assign`, `assign_leave_type_import`, `available_leave_update` (2030), `leave/cbv/assigned_leave.py`, `leave/cbv/leave_types.py`, `employee/cbv/allocations.py`, `master_import/datasets/assigned_leave.py` (`bulk_create` paths write one `INITIAL_ALLOCATION` row each)
   - allocation requests (`_approve_leave_allocation` / `_reject_leave_allocation`, `leave/forms.py`) and compensatory leave (`assign_compensatory_leave_type` / `exclude_compensatory_leave` in `leave/models.py`)
   - `leave/scheduler.py` `leave_reset` → `CARRY_FORWARD` / `ADMIN_ADJUSTMENT` events, with the per-employee allowance (O8) and carry-forward of negative balances
   - penalties: `base/signals.py` create/delete (62, 121). This also fixes the refund-more-than-taken bug caused by the clamp
   - payroll leave encashment (`Reimbursement.save` in `payroll/models/models.py`)
   - the API in `horilla_api/api_views/leave/views.py` (assign, approve, reject, allocation, bulk)
   - demo fixtures (`create_branch_demo_fixtures.py`)
3. **Guard rail:** a test that greps for `available_days =`, `available_days -=`, `available_days +=` and `carryforward_days` assignments outside `leave_ledger`, and fails on new ones. Add a nightly reconcile job that flags any balance whose ledger sum differs.
4. **Leave rules**
   1. `emergency_contact_employee` FK (an active employee, not the requester), required per company setting, on the web forms and the API.
   2. Probation employees can't self-apply (form + API). Add the permission `leave.add_leave_on_behalf`: an on-behalf request is created **approved** through the ledger (`LEAVE_ADMIN_CREATE`) and e-mails the employee.
   3. Overlap rule: block overlap with pending/approved leave **and with WFH**, except one FIRST_HALF + one SECOND_HALF on the same day.
   4. Unpaid leave: no balance effect.
   5. Late approval of a day already penalised as absent: reverse the `ABSENT_PENALTY` (`LEAVE_ATTENDANCE_ABSENT_CANCEL`) and set the day's work record to leave.
   6. Edit by HR: reverse (`LEAVE_EDIT_REVERT`), reset approvals, back to requested.
5. **Reconcile screen:** per employee and type, show opening, events and closing, with drill-down to the source request (the replacement for Apurba's `/api/reports/leave-record/reconcile`).
6. **Importer, phase `leave`** (§6.3 rows 42–49): leave types per company, current-year balances with a `MIGRATION_BASELINE` row, the ledger copied verbatim, leave requests **without re-applying effects**, cancellations.

**Exit:** for every employee and type, Horilla's balance equals Apurba's and the ledger sums to it. The guard-rail test passes. HR has signed off the leave scenarios from the P0 sheet.

### P3: Attendance policy, claims and day-close (4–6 weeks)

**Goal:** clock-in/out, statuses, penalties and claims behave as in Apurba, in each employee's timezone.

1. **Time helpers:** `employee_today/now`. Replace the process-local dates in `attendance/views/clock_in_out.py` (around lines 274–285 and 537–558), the API clock views, `create_work_record` and the dashboards. Night-shift handling stays as Horilla has it.
2. **Clock-in decision service** (one function shared by web, API and biometric), applied in this order (Apurba reference §4.6):
   1. Holiday or weekend → confirm → pending compensatory (extra work) request.
   2. Approved full-day leave → confirm → clock in + leave cancellation request for the day.
   3. Home location → allowed if `wfh_eligible` or an approved WFH covers today.
   4. Office location → client IP must be allowed (`AttendanceAllowedIP`, `base/models.py:2761`). Store the IP on the attendance (new column on an `hr_policy` side table, or an `additional_data` key).
   5. No shift → blocked.
   6. One clock-in per day.

   Status: PRESENT if not after shift start + late threshold, otherwise LATE (record via the existing `late_come`). After the half-day threshold (shift midpoint + late threshold / 2), LATE + `HALFDAY_LATE_CLOCKIN` 0.5 deduction. Add the FIRST_HALF / SECOND_HALF leave interplay. When `attendance_restriction` is off, the status is always PRESENT.
3. **Clock-out:** must be after clock-in (an earlier time counts as the next day when the span is 1–18 h); span cap 18 h; future window for restricted employees on office IP; holiday/weekend clock-out updates the extra-work request.
4. **Edit today's times** (O9): allowed for non-office locations and for employees with an approved WFH, within the shift windows.
5. **`day_close` job** (§4.3):
   - no clock-in on a working day and no **approved** full-day leave → absent (`WorkRecords` ABS) + `ABSENT_PENALTY` 1 day
   - approved FIRST_HALF with no clock-in → `HALF_ABSENT_PENALTY` 0.5
   - open attendance → auto clock-out at the last biometric punch (no penalty), else at shift end − `clock_out_penalty` (FIRST_HALF leave: shift midpoint − penalty)
   - span > 1.5 × shift and not Home → 0.5-day extra-work request
   - Turn off Horilla's `auto_punch_out` for shifts that have a `ShiftPolicy`, so the two don't race.
6. **Weekly late penalty:** previous Mon–Fri, 3+ lates → `LATE_PENALTY` 1 day, key `(employee, ISO week)`.
7. **Attendance claims**
   1. `ClaimPolicy` per company.
   2. On attendance-request create, check in order: on or before the cutoff day of the following month; the shift on that date has ended; monthly count < max (count of non-rejected claims for that month, computed rather than stored, so there is no counter to drift); one per date; end after start. Convert the source time zone (string offset → request tz → employee tz → default).
   3. The day shows as "claim pending".
   4. Approve → attendance PRESENT with the claimed times + `CLAIM_APPROVED` (reverses that day's absent penalty).
   5. Reject → absent; if it had been approved, `CLAIM_REVERSED`.
   6. Deleting a pending claim → absent. The quota frees up automatically because it is a count.
8. **Extra work approval:** the approver must pick FULL / FIRST_HALF / SECOND_HALF → credit +1 / +0.5 via `EXTRA_WORK_APPROVED`. A type change adjusts by the delta. Reject → `EXTRA_WORK_REVERSED` (never below 0) and remove the generated attendance.
9. **Clock-in reminders:** two slots per shift (from `ShiftPolicy`), working days only, skip employees with `email_restriction` or already reminded (`ReminderLog`).
10. **Work deficit:** monthly expected vs actual (attendance + approved extra work) → `WorkDeficit` with `floor(deficit / duration_for_one_leave)` leaves to deduct (report-only, O4).
11. **Audit:** register `Attendance` for column-level history in the `horilla_audit` configuration.
12. **Importer, phase `attendance`** (§6.3 rows 31–41, 50): attendance converted from UTC to employee local time, claims, extra work, work deficit, and a `DayCloseLog` seeded up to the import date so the new job never re-penalises imported days.

**Tests:** one test per row of Apurba's status and constraint tables (reference §4.6 and §4.15) for BD and USA employees; DST edge cases for America/New_York; idempotency (run day-close twice); claim quota and cutoff boundaries; an IP-gate parity test for web vs API.

**Exit:** on a replayed month of real punches, Horilla's statuses and penalties match Apurba's ledger for ≥ 99.5 % of employee-days. Every difference is explained.

### P4: Approvals and WFH (2–3 weeks; can overlap the end of P3)

1. **`ApproverAssignment` + `approvers_for()`** (active and effective on the request date).
2. **Leave:** when a leave request is saved in `requested` status (`LeaveRequest.save`, where `LeaveRequestConditionApproval` rows are built), use the assignments when the company is in assignment mode (O1). Level 1 finalises, levels 2+ can only remark (`ApprovalAction`). A Super Admin can override; after a Super Admin acts, only a Super Admin or an approve-permission holder can change the result; an approver can't change their own decision.
3. **Attendance claims, extra work (compensatory) and WFH:** the same `can_finalise()` in their approve/reject views (`attendance/views/requests.py` approve/reject, the compensatory approve view in `leave/views.py`, the work-from approve view `base/views.py` ~4670).
4. **Inbox scoping** (O2) via `inbox_queryset()`, in web views and the API. **IDOR tests:** an approver can't act on, or see, a non-assignee's request by id.
5. **Bulk approval assignor:** pick employees, request types, levels and approvers; preview the existing rows; apply as **replace** or **merge**.
6. **Approver history page:** `ApprovalAction` across all four types, filterable.
7. **WFH**
   1. "Home" work from with `requires_wfh_approval`. A WFH request is a `WorkFromRequest` with end date, optional half day, reason ≤ 1000 characters and an attachment.
   2. Working-days-only rule.
   3. Overlap blocked against WFH and leave.
   4. The owner can edit or cancel only while pending (an edit resets approvals). No balance effect.
8. **Importer, phase `approvals`** (rows 37–38, 46–47, 51–54): assignments, histories → `ApprovalAction`, pending requests' approval rows.

**Exit:** every approver's open inbox in Horilla equals Apurba's (§6.5 check 7).

### P5: Reports and notifications (1–2 weeks)

1. **Standard reports** in `report`, using the same registry pattern as the existing 34:
   - **Negative Leave**: month-on-month from the ledger, newly negative, absent, late and half-day penalties
   - **Work Hours & Deficit**
   - **Leave Record + Reconcile**
   - **Claim Usage**

   Each with Excel export.
2. **Subscriptions** replace Apurba's monthly e-mails: negative leave (1st, 01:00), work hours (1st, 11:00), claim reminder (1st, 10:00). Seed them from Apurba's `email_config` recipients. Seed the report run log so last month isn't sent again.
3. **Event e-mails:** map each Apurba `email_config` event to a `MailAutomation` (model, trigger, condition, recipients, CC/BCC), with a department condition where Apurba used one:
   - leave created / approved / rejected / cancelled
   - cancellation requested
   - claim submitted / decided
   - extra work requested / decided
   - WFH submitted / decided
   - new employee

   Honour `email_restriction` for reminders. In-app notifications come for free.
4. **Dashboards:** add the "clock status", "who's on leave", birthdays and monthly work-hours widgets where Horilla's employee dashboard lacks them.

**Exit:** HR receives the same monthly reports from staging as from Apurba for the same month.

### P6: Peripheral features (3–5 weeks; can start after P1, in parallel)

Ordered by go-live need. Items 1–4 are **day-1 must-haves**; items 5–8 can follow cutover.

1. **Onboarding quiz gate**
   1. Models and a question builder: MCQ and typed questions, reorder, activate, stats, audit.
   2. Questionnaire page with retry-wrong-only.
   3. `OnboardingQuizMiddleware`, modelled on `ForcePasswordChangeMiddleware` (`base/middleware.py:422`): an exempt list (login, logout, password reset/change, two-factor, the questionnaire, `/static/`, `/media/`, `/jsi18n/`, `/health/`, `/ready/`, `/api/`), HTMX `HX-Redirect`, and a pass-through for HTMX sub-requests from exempt pages.
   4. Add a `quiz_pending` flag to the API capabilities payload so the mobile app can gate too.
   5. Import responses and status so people who already passed aren't gated again.
2. **Google sign-in:** OAuth with the existing `google-auth-oauthlib` dependency, an HMAC-signed state (10-minute limit), and a match on the stored Google id, then a verified e-mail. Log in through Django's `login()`, so session, 2FA and forced-password-change rules apply, and send the attempt through axes. Import `google_oauth_id` onto a `UserSocialLink` model.
3. **ADMS push receiver** (O6): the `/iclock/cdata` GET handshake and POST, `getrequest`, `devicecmd`. Device time offset setting, dry-run flag, per-device counters **in the DB** (not process memory). Punches → the clock-in decision service. Test it with captured device payloads.
4. **External attendance summary API** (O5): `ServiceClient` (name, hashed key, company, scopes, active, last_used), throttle scope `external`, a response identical to Apurba's, and an audit row per call.
5. **Google Calendar (`horilla_meet`):**
   - create, update and delete meetings
   - attendee search
   - conflict check and day schedule, via the Calendar free/busy API
   - **best-time finder**: intersect attendees' free slots within working hours in each attendee's timezone
   - shared/private `MeetingTemplate`
   - public-holiday import per country into `Holidays` for the chosen company
6. **Evaluations + AI commit evaluation:** `EvaluationRecord` (interval, next date, history, stats), `GitUsernameMapping`, and the proxy view with 502/504 mapping.
7. **PWA:** a service worker served from the site root (a view at `/service-worker.js` so its scope covers the site). Cache-first for `/static/`, network-first for HTML/API, purge old caches. Update the manifest name and icons. An offline fallback page.
8. **API activity log (optional):** a middleware that writes method, path, status, latency, user and masked bodies to a capped table, with a retention job.

**Exit:** items 1–4 pass UAT on staging. Items 5–8 have a scheduled date.

### P7: Parallel run (4–6 weeks of calendar time, including at least one month-end)

See §7.1.

**Exit:** two consecutive weeks with zero unexplained differences, a clean month-end report comparison, and HR sign-off.

### P8: Cutover and decommission (1 week)

See §7.2.

**Exit:** Horilla is the system of record; Apurba is read-only, then archived.

---

## 6. Data migration

### 6.1 Approach

- **Tool:** `python manage.py import_apurba --source-url postgres://ro@…/hrm --phase {config,org,people,leave,attendance,approvals,quiz,mail,archive,all} [--dry-run] [--since <timestamp>] [--company BD|USA]`.
  - It reads with raw `psycopg2`, which is already a dependency; SQLAlchemy is not needed. It runs in **dependency order** (§6.2).
  - Each phase runs in batches inside `transaction.atomic()`.
  - `--dry-run` rolls back and prints the counts and errors.
- **Idempotent upsert:** every imported row gets a `MigrationIdMap(source_table, source_id → content_type, object_id, row_hash)`.
  - On re-run, an unchanged hash is skipped, a changed hash is updated, and a new row is created.
  - Rows deleted at the source are reported, never deleted automatically.
  - This is what makes the parallel run and the final delta possible.
- **Context:**
  - Run inside `run_as(<migration user>, company)` so `created_by`/`modified_by` are set and company-scoped managers resolve.
  - Wrap in `horilla_automations.signals.suspend_automations()` (`horilla_automations/signals.py:55`) so no e-mails or notifications fire.
  - `HorillaModel.save()` still runs the XSS check on every string. Rows that fail it are reported and fixed at the source, or stored with the offending markup escaped, and never bypassed.
- **No double effects:**
  - Balances come from Apurba's `leave_balance` + ledger. Imported approved leave, claims and extra work **must not** call the approve paths.
  - The importer writes those rows with the status set directly and `approved_available_days`/`approved_carryforward_days` filled from Apurba's ledger.
  - `LeaveRequest.save()` recomputes `requested_days` with Horilla's rules. Log any difference from Apurba's `no_of_days`; the ledger stays authoritative.
- **Derived data:**
  - Historical attendance uses `bulk_create` for speed (as `attendance/views/process_attendance_data.py` does).
  - Then rebuild `WorkRecords` and the monthly hour accounts. The `trigger_save` command or the hour-account rebuild (see `attendance/tests/test_hour_account_rebuild.py`) shows the way.
  - Current-month rows go through `save()`.
- **Time:**
  - Apurba stores naive UTC. Convert with the employee's timezone (policy → shift → company default) into Horilla's local date and time fields.
  - Keep `attendance_date` as Apurba's (it is already the local date).
- **Passwords:**
  - `users.password_hash` (bcrypt `$2b$12$…`) → `HorillaUser.password = "bcrypt$" + hash`.
  - Usernames: Horilla uses the e-mail as the username. Map `users.email` → `username`, keep Apurba's username in a `LegacyArchive` payload, and resolve collisions before the run.

### 6.2 Import order

1. `config`: companies, system settings, timezones, SMTP, claim policy.
2. `org`: departments, designations, teams, offices, shifts, work locations, IPs, holiday sets, holidays, weekends, working-day exceptions.
3. `people`: users, roles, employees, restrictions, reporting lines, blood group, photos.
4. `leave`: leave types, balances, ledger, leave requests, cancellations.
5. `attendance`: attendance, claims, extra work, work deficit, day-close seed.
6. `approvals`: assignments, histories, open approval rows.
7. `quiz`: questions, options, answers, responses, status.
8. `mail`: e-mail config → automations and subscriptions, meeting templates.
9. `archive`: logs → `LegacyArchive`.

### 6.3 Table mapping (all 67 Apurba tables)

| # | Apurba table | Horilla target | Notes |
|---|---|---|---|
| **auth_rbac** ||||
| 1 | `users` | `HorillaUser` | `bcrypt$` prefix; `is_new_employee=False`; no hash → unusable password |
| 2 | `role` | `auth.Group` | Via the mapping sheet. `is_super_admin` roles → `is_superuser` on members |
| 3 | `permission` | — | Mapping sheet only (Appendix C) |
| 4 | `permission_group` | skip | UI grouping only |
| 5 | `permission_group_map` | skip | UI grouping only |
| 6 | `role_permission_map` | `Group.permissions` | Through the mapping sheet |
| 7 | `user_role_mapping` | `CompanyGroupAssignment` (BD and/or USA) | Per the employee's company; admins in both |
| 8 | `rbac_audit_log` | `LegacyArchive` | |
| 9 | `password_reset_otps` | skip | Short-lived |
| **employee** ||||
| 10 | `employee_info` | `Employee` + `EmployeeWorkInformation` + `EmployeePolicy` | Company by region; `badge_id = employee_code`; work e-mail/phone; `date_joining`; `office` → work-info `location`; `designation` → `job_position_id`; `current_shift_id` → `shift_id`; `employment_period`/`probation_timeline` → policy; NID/TIN encrypted (O3); `photo_url` → downloaded into `employee_profile`; `last_working_day` → archive the employee if it is in the past; `salary_review_date`, `total_paid_holiday` → policy |
| 11 | `restrictions` | `EmployeePolicy` | attendance_restriction, email_restriction, wfh_eligible |
| 12 | `reporting_manager` | `ReportingLine` (+ level 1 → `reporting_manager_id`) | Levels and effective dates kept |
| 13 | `employee_blood_group_list` | `EmployeePolicy.blood_group` | |
| 14 | `evaluation_history` | `EvaluationRecord` | |
| 15 | `git_username_mapping` | `GitUsernameMapping` | |
| 16 | `activity_log` | `LegacyArchive` | Last 12 months (O10) |
| **org** ||||
| 17 | `department` | `Department` | Linked to each company where it is used |
| 18 | `designation` | `JobPosition` | Horilla job positions belong to a department: create one per (department, designation) pair in use |
| 19 | `team` | `Team` | Lead → employee |
| 20 | `office` | work-info `location` + company choice | |
| 21 | `shift` | `EmployeeShift` + `EmployeeShiftSchedule` (per weekday) + `GraceTime` + `ShiftPolicy` | `late_threshold_minutes` → grace time; thresholds, penalty, `duration_for_one_leave`, timezone and cron times → policy |
| 22 | `shift_assignment` | work-info `shift_id` (current); future-dated → roster; past → archive | |
| 23 | `work_location` | `WorkFrom` + `WorkFromPolicy` | Office / Home flags |
| 24 | `ip_address` | `AttendanceAllowedIP` per company | IPv4/IPv6, active only |
| 25 | `holiday_set` | company (BD / USA) | If there are more than 2 sets, use employee-specific `Holidays` |
| 26 | `yearly_holiday` | `Holidays` | Per company |
| 27 | `weekend` | `CompanyLeaves` | Per company (e.g. BD Fri+Sat, USA Sat+Sun) |
| 28 | `working_day_exception` | `WorkingDayException` | |
| 29 | `timezone` | IANA names on the policy / shift | |
| 30 | `system_setting` | Horilla settings, key by key | E.g. check-in enabled, restriction defaults |
| **attendance** ||||
| 31 | `attendance` | `Attendance` + `AttendanceActivity` + `AttendanceLateComeEarlyOut` + `WorkRecords` | Status mapping §6.4; UTC → local; IP stored |
| 32 | `attendance_audit_log` | `LegacyArchive` | |
| 33 | `attendance_sync_log` | `LegacyArchive` (last 90 days) | Kept for auto-clock-out evidence |
| 34 | `total_work_duration` | skip | Derived; Horilla computes worked hours |
| 35 | `work_deficit` | `WorkDeficit` | |
| 36 | `attendance_claim_request` | attendance request (`Attendance` with `is_validate_request`) + `AttendanceClaim` | Pending → request open; approved → validated; rejected → rejected flag |
| 37 | `attendance_claim_approval` | `ApproverAssignment(type=attendance_claim)` | |
| 38 | `attendance_claim_approvers_history` | `ApprovalAction` | |
| 39 | `max_claim` | skip (derived count) | Checked in reconciliation |
| 40 | `max_claim_config` | `ClaimPolicy` | |
| 41 | `cron_log` | `LegacyArchive` + seed `DayCloseLog` / `ReminderLog` | Prevents re-penalising |
| **leave** ||||
| 42 | `leave_info` | `LeaveRequest` | Status: PENDING→requested, APPROVED→approved, REJECTED→rejected, CANCELLED→cancelled, ADJUST→review by hand; `half_day_type` → start/end breakdown; `emergency_contact` → FK; `approved_by` → `ApprovalAction` |
| 43 | `leave_type` | `LeaveType` per company | exclude holidays / weekly offs = yes; Unpaid → unpaid, unlimited; yearly reset Jan 1, carry-forward without a cap (match Apurba) |
| 44 | `leave_balance` | `AvailableLeave` (current year) | `available_days = available_leave` (may be negative), `carryforward_days = 0`; Apurba's allowed / redeemed / achieved / carry_forward go into the `MIGRATION_BASELINE` row. Past years → archive |
| 45 | `leave_balance_ledger` | `LeaveLedgerEntry` | Verbatim; event types are identical; source ids mapped through `MigrationIdMap` |
| 46 | `leave_approval` | `ApproverAssignment(type=leave)` | |
| 47 | `leave_approvers_history` | `ApprovalAction` (+ `LeaveRequestConditionApproval` for pending) | |
| 48 | `leave_cancellation` | `LeaveRequest` status `cancel_requested` / `cancelled` + note | Stored clock times → archive payload |
| 49 | `leave_report_run_log` | Report run log seed | Stops the last month being sent again |
| **extra_work_wfh** ||||
| 50 | `extra_work` | Compensatory leave request + `Attendance` (holiday) | `half_day_type` kept |
| 51 | `extra_work_approval` | `ApproverAssignment(type=extra_work)` | |
| 52 | `extra_work_approval_history` | `ApprovalAction` | |
| 53 | `wfh_request` | `WorkFromRequest` (Home) + WFH fields | Attachment downloaded |
| 54 | `wfh_approval_history` | `ApprovalAction` | |
| **approvals** ||||
| 55 | `approval_request` | request-type choices | No rows needed |
| **onboarding** ||||
| 56 | `questions` | `QuizQuestion` | |
| 57 | `question_options` | `QuizOption` | |
| 58 | `question_answers` | `QuizAnswer` | |
| 59 | `user_question_responses` | `QuizResponse` | |
| 60 | `user_onboarding_status` | `QuizStatus` | Users who completed it stay ungated |
| 61 | `question_audit_log` | `LegacyArchive` | |
| **email** ||||
| 62 | `email_hrm` | `DynamicEmailConfiguration` per company | Re-enter the password if Apurba's can't be decrypted |
| 63 | `email_config` | `MailAutomation` rows + report subscriptions | Per event (§5 P5) |
| 64 | `email_log` | `LegacyArchive` | |
| **calendar** ||||
| 65 | `google_calendar_config` | `GoogleCloudCredential` | Only if the same OAuth client and redirect URIs are reused |
| 66 | `google_calendar_tokens` | skip | Users reconnect (O7) |
| 67 | `meeting_templates` | `MeetingTemplate` | |

**Database objects that don't move as SQL.** The behaviour is rebuilt in Python:

| Apurba object | Replacement |
|---|---|
| `fn_recalculate_attendance_status` | Status computed by the clock-in service and on attendance edit |
| `audit_attendance_changes` | auditlog registration of `Attendance` |
| `update_total_work_duration` / `delete_total_work_duration` | Horilla's worked-hours and hour-account logic |
| `decrement_claim_count` | Computed claim count |
| `update_leave_cancellation_updated_at` | `auto_now` field |
| Views `v_active_*_questions`, `v_user_onboarding_progress` | Querysets |

### 6.4 Attendance status mapping

| Apurba status | Horilla rows |
|---|---|
| PRESENT | `Attendance` + one `AttendanceActivity` |
| LATE | as PRESENT + `AttendanceLateComeEarlyOut(type="late_come")` |
| SIGNED_IN | Open `Attendance` (no clock-out). Only valid for today; older rows are flagged for review |
| ABSENT | No `Attendance`; `WorkRecords` ABS. The penalty is already in the imported ledger |
| ON_LEAVE | Covered by `LeaveRequest`; leave `WorkRecords`. Clock times, if any, are imported as attendance |
| OFF_DAY | Nothing; import attendance with `is_holiday` if times exist |
| EXTRA_WORK | `Attendance` (holiday) + approved compensatory request |
| ATTENDANCE_CLAIM_PENDING | Attendance request with `requested_data` = claimed times |

### 6.5 Reconciliation checks (run after every import and daily in P7)

1. Row counts per source table vs target (minus skips), per company.
2. Every active Apurba employee has a user, an employee, work info and a policy; e-mail and badge are unique.
3. Login smoke test: 10 sampled migrated accounts authenticate with their known test passwords on staging.
4. **Leave:** for every employee, type and current year, `AvailableLeave.available_days + carryforward_days` = Apurba `available_leave`, and the Horilla ledger sum = the Apurba ledger sum.
5. **Attendance:** per employee and month, counts of present / late / absent / leave / extra-work days are equal.
6. **Claims:** per employee and month, claim count and status equal; nobody is over quota.
7. **Approvals:** for every approver, the set of open requests in their Horilla inbox = their Apurba inbox.
8. Reports: Negative Leave and Work Hours for the last closed month match Apurba's Excel files cell for cell (allowing for rounding).
9. A manual sample: HR checks 20 employees end to end (profile, balance, last 30 days, open requests).

Output: `import_apurba --reconcile` writes a dated Excel with one sheet per check, plus a pass/fail summary.

---

## 7. Parallel run and cutover

### 7.1 Parallel run (P7)

- **Apurba stays the system of record.** Employees keep using Apurba. Horilla is read-only for staff, except for a UAT group.
- **Nightly delta:** `import_apurba --phase all --since <last run>` (hash compare), then `--reconcile`, and the report is mailed to the migration owner.
- **Biometric devices** can push ADMS to one server only, so they stay on Apurba. Horilla gets the punches through the nightly import of attendance. Optional: a small forwarder that relays the device posts to Horilla's receiver, which tests P6 item 3 with live traffic.
- **Horilla's own jobs in compare mode:**
  - `day_close`, `weekly_late_penalty`, reminders, carry-forward and the probation job run with a `HR_POLICY_DRY_RUN=1` setting. They compute what they **would** do and write it to a comparison table instead of the ledger.
  - The daily reconcile compares those would-be penalties with Apurba's actual ledger rows for the same day.
  - This is the strongest test of the P3 rules.
- **UAT:** HR runs the P0 sign-off sheet scenarios in staging. Approvers check their inboxes. A pilot team of employees uses Horilla for clock-in **in addition** to Apurba for one or two weeks; their Horilla data is discarded at cutover.
- **Calendar:** cover at least one month-end, so the claim cutoff (day 5), the monthly reports and the work-deficit run are all compared. Avoid the year-end: decide up front which system runs the 2026→2027 carry-forward (§9 R6).

### 7.2 Cutover runbook (P8)

1. **T−5 days:** announce the date. Freeze Apurba configuration changes (shifts, leave types, approvers).
2. **T−1:** final full rehearsal on a fresh staging copy; time it; the reconciliation must be clean.
3. **T0 (start of a month, outside working hours):**
   1. Put Apurba in maintenance mode, pause its scheduler, and take a final `pg_dump`.
   2. Run the final delta import with `--since` the last nightly run, then `--reconcile`. Go/no-go on a clean result.
   3. Back up the Horilla DB (`deploy.sh` takes a `pg_dump -Fc` before deploy).
   4. Turn off `HR_POLICY_DRY_RUN`; enable the jobs. Turn off `auto_punch_out` for migrated shifts. Check `run_scheduler --list`.
   5. Re-point the biometric devices (ADMS server URL) to Horilla, and confirm the first punches arrive.
   6. Hand over to consuming systems: external API keys issued, URL changed.
   7. Switch the DNS / Cloudflare Tunnel for the HRM hostname, and add a redirect from the old URL.
4. **T0 + 1 day:**
   1. Watch day-close results, the `/ready/` scheduler status and Sentry.
   2. HR checks a sample.
   3. Staff have to sign in again; passwords are unchanged (bcrypt), and Google sign-in works.
5. **Rollback** (within 48 h, if go/no-go fails or a blocking issue appears):
   1. Re-enable Apurba from its untouched DB.
   2. Re-point the devices and DNS.
   3. Re-import into Apurba any Horilla-only events captured since T0 (leave and claims entered), using the `MigrationIdMap` and ledger, or re-key them by hand if there are few.
   4. The rollback window closes after the first Horilla day-close plus HR sign-off.
6. **Decommission (T + 30 to 90 days):** keep Apurba read-only for lookups, then archive the DB dump and file-service objects per retention policy, and revoke its secrets (JWT, Google OAuth client, SonarQube token).

---

## 8. Cross-cutting rules

- **Repo conventions** (`CLAUDE.md`):
  - commit format `[ADD] HR_POLICY: …`
  - PRs to `dev/v2.0`
  - `CHANGELOG.md` `## [Unreleased]`
  - version only in `horilla/__version__.py`
- **Tests:**
  - Django test runner, `django.test.TestCase` + `setUpTestData`, `horilla.testkit` factories (`make_company`, `make_employee`, `make_leave_type`, `make_available_leave`, `make_attendance`, …), `CompanyFilterTestMixin` for scoped queries.
  - CI runs Postgres 16: test the ledger's `select_for_update` and unique-key behaviour there, not only on SQLite.
  - Raise `COV_FAIL_UNDER` as coverage grows, and never lower it.
- **Migrations:** each model change ships with its migration (`makemigrations --check` gate). Side-table design keeps Horilla's core migrations untouched.
- **Tenancy:** every new model with a company link gets `HorillaCompanyManager`; `check --tag horilla.tenancy` must stay clean.
- **Security:**
  - Every new view loads objects scoped to the owner, an assigned approver or a permission, with an IDOR test per view (the repo's `*_idor` pattern).
  - API keys are hashed and never logged.
  - NID/TIN are encrypted and permission-gated.
  - Google sign-in goes through axes and 2FA.
  - The ADMS receiver accepts only registered device serial numbers.
- **Templates:** put new and changed templates in `horilla_theme/templates/…`. Production uses the cached loader, so restart after template deploys.
- **Mobile API parity:** clock-in rules, WFH, claims and approvals must be available under `horilla_api` too, or the mobile app bypasses policy (today the API clock-in skips the IP check).
- **Fix before go-live** (from the Horilla review, they hit this project directly):
  - the two balance-deduction orders (P2)
  - the penalty refund clamp (P2)
  - the in-process scheduler started by `biometric_device_schedule` (double polling) if pull devices are used
  - `recruitment_close`'s import-time date, if recruitment is enabled
- **i18n:** wrap new strings in gettext. English is enough for go-live.
- **Docs:** update `docs/EMPLOYEE_SETUP_GUIDE.md` (policy, approvers, WFH), add an HR user guide for claims, WFH and the ledger screen, and an ops runbook for the importer.

---

## 9. Risks

| # | Risk | Mitigation |
|---|---|---|
| R1 | Missing one of the 30+ balance writers, so the ledger and balance drift | Guard-rail test + nightly reconcile job (P2) |
| R2 | Policy rules differ subtly (thresholds, half-day, DST in New York) | P0 sign-off sheet, a test per rule, P7 compare mode against Apurba's ledger |
| R3 | Double penalties (Horilla jobs + imported history, or two schedulers) | Idempotency keys, a seeded `DayCloseLog`, `auto_punch_out` off for migrated shifts, a single `run_scheduler` replica |
| R4 | Upstream Horilla merges conflict with core hooks | Side-table design; hooks behind small service calls; keep the list of touched core files in this doc current |
| R5 | Password / username mismatch (Apurba usernames vs Horilla e-mail usernames) | Resolve collisions in P1; bcrypt hasher; Google sign-in as a fallback; admin bulk reset as a last resort |
| R6 | Cutover near year-end, when carry-forward runs | Cut over at the start of a month that isn't January, or run the 2026→2027 carry-forward in Apurba and import the result |
| R7 | Biometric devices can't reach Horilla or speak a slightly different ADMS dialect | Capture real payloads in P6; test with one device first; keep Apurba as receiver until cutover |
| R8 | Approval semantics change (level-1 finaliser vs Horilla chain) confuses approvers | Default to Apurba semantics (O1); training; approver history page |
| R9 | XSS check rejects legacy text (remarks with HTML) | Importer reports them; clean at source or escape; never bypass `clean_fields()` |
| R10 | Data volume makes `save()`-based import slow | Bulk paths for history + rebuild; P0 volume measurement; batch sizes |
| R11 | Encrypted NID/TIN or SMTP secrets can't be decrypted | Get Apurba's key in P0; otherwise re-collect those fields |
| R12 | Bangladesh payroll expectations appear mid-project | Out of scope (Apurba has no payroll). Plan a separate BD tax pack project after cutover |

---

## Appendix A: effort and dependencies

Rough person-week estimates for one developer familiar with Django. They assume HR answers questions within days. Treat them as planning ranges, not commitments.

| Phase | Effort (person-weeks) | Depends on |
|---|---|---|
| P0 Foundations | 1–2 | — |
| P1 People & org + first import | 2–3 | P0 |
| P2 Leave ledger & rules | 3–4 | P1 |
| P3 Attendance policy & claims | 4–6 | P2 (ledger) |
| P4 Approvals & WFH | 2–3 | P1; finishes after P3 |
| P5 Reports & notifications | 1–2 | P2, P3 |
| P6 Peripheral (items 1–4 / 5–8) | 2–3 / 1–2 | P1 |
| P7 Parallel run | 4–6 calendar weeks (≈1–2 person-weeks of effort) | P1–P5, P6 items 1–4 |
| P8 Cutover | 1 | P7 sign-off |
| **Total build** | **≈ 26–40** | |

```
P0 ─► P1 ─┬─► P2 ─► P3 ─┬─► P5 ─┐
          │             └─► P4 ─┤
          └─► P6 (1–4) ─────────┼─► P7 ─► P8 ─► P6 (5–8) if not done
                                ┘
```

---

## Appendix B: ledger events and where Horilla emits them

| Event (same names as Apurba) | Emitted by |
|---|---|
| `INITIAL_ALLOCATION` | Leave assign (single, bulk, import, master_import) |
| `MIGRATION_BASELINE` | `import_apurba` (once per balance) |
| `CARRY_FORWARD` | `leave_reset` yearly run |
| `ADMIN_ADJUSTMENT` | Manual balance edit; work-deficit deduction applied by HR |
| `LEAVE_APPROVED` | Leave approve (web, API, bulk, auto-approve on create) |
| `LEAVE_ADMIN_CREATE` | Leave on behalf |
| `LEAVE_REVERSED` | Reject after approval; cancellation approved |
| `LEAVE_EDIT_REVERT` | HR edits an approved leave |
| `LEAVE_CANCELLED_BY_ATTENDANCE` | Clock-in on approved leave → cancellation approved |
| `LEAVE_ATTENDANCE_ABSENT_CANCEL` | Late approval of a day already penalised as absent |
| `HALF_LEAVE_REJECTED` | Half-day leave rejected after a half-day penalty interplay |
| `ABSENT_PENALTY` / `HALF_ABSENT_PENALTY` | `day_close` |
| `HALFDAY_LATE_CLOCKIN` | Clock-in service |
| `LATE_PENALTY` | `weekly_late_penalty` |
| `CLAIM_APPROVED` / `CLAIM_REVERSED` | Attendance claim approve / reject-after-approve |
| `EXTRA_WORK_APPROVED` / `EXTRA_WORK_REVERSED` | Compensatory (extra work) approve / reject / type change |
| `WORK_DEFICIT_PENALTY` (new, optional) | Only if O4 changes to automatic deduction |
| `ALLOCATION_APPROVED` / `ENCASHMENT` / `PENALTY_MANUAL` (Horilla-only, new) | Allocation requests, payroll leave encashment, manual `PenaltyAccounts` |

Idempotency key format: `<event>:<employee_id>:<date or source>`, for example `ABSENT_PENALTY:42:2026-11-03` or `LEAVE_APPROVED:leave_request:981`.

---

## Appendix C: starter permission mapping

To be confirmed in P0. Apurba roles: `ADMIN` → Horilla **Admin** group (or HR Manager), assigned in both companies. `EMPLOYEE` → no group (the default own-profile permissions). Super Admin → `is_superuser`.

| Apurba code | Horilla permission |
|---|---|
| `employee.view/create/edit/delete` | `employee.view/add/change/delete_employee` |
| `employee_attendance_directory.view/edit` | `attendance.view/change_attendance` |
| `employee_attendance_history.view` | `attendance.view_attendance` |
| `leave_request.view/edit/clear` | `leave.view/change/delete_leaverequest` |
| `leave_request.create_on_behalf` | new `leave.add_leave_on_behalf` |
| `leave_cancellation.clear` | `leave.change_leaverequest` |
| `wfh_request.view/edit/clear` | `base.view/change/delete_workfromrequest` |
| `extra_work.view/approve/clear` | compensatory leave request view / approve (new) / delete |
| `attendance_claim.view/approve/clear` | `attendance.view_attendance` / new `hr_policy.approve_attendanceclaim` / `attendance.delete_attendance` |
| `bulk_approval_assignor.manage` | `approval_assignment.change_approverassignment` |
| `utilities_dashboard.view/manage` | Settings permissions in `base` (view / change on shifts, work from options, holidays, …) |
| `restrictions.view/create/edit/delete` | `hr_policy.view/add/change/delete_employeepolicy` |
| `question_builder.*` | `onboarding_quiz.*_quizquestion` |
| `commit_evaluation.view` | `evaluations.view_evaluationrecord` |
| `meeting.*` | `horilla_meet.*_googlemeeting` |
| `rbac.audit_logs.view` | `horilla_audit` view permission |
| `report.view` | `report` access matrix (`ReportAccess`) |
| `module.view` | Sidebar/menu access settings |
