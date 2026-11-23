# API Documentation: horilla-hr

Commit f2ab49933cfb40d295b3a9e65eba21996df2b0dc. Route counts are `path()` entries in each URL module; individual request/response shapes were not traced in this scan (see the Swagger UI for live contracts).

## 1. API surfaces

| Surface | Base path | Consumers | Auth | Defined in |
|---|---|---|---|---|
| Web UI (HTML + HTMX partials) | `/`, `/<app>/` | Browsers | Django session; CSRF | each `<app>/urls.py`, included from `AppConfig.ready()` |
| REST API | `/api/` | Mobile app, integrations | JWT Bearer (`TenantScopedJWTAuthentication`) | `horilla_api/urls.py`, `horilla_api/api_urls/*` |
| Geofencing API | `/api/geofencing/` | Mobile app | JWT | `geofencing/urls.py` |
| Face detection API | `/api/facedetection/` | Mobile app | JWT | `facedetection/urls.py` |
| WhatsApp webhook | `/whatsapp/` | Meta WhatsApp Cloud | Webhook verify token + signature check (`whatsapp/views.py:116-152`) | `whatsapp/urls.py` |
| Notifications | `/inbox/notifications/` | Browser polling | Session | vendored `notifications` |
| Ops probes | `/health/`, `/ready/`, `/metrics/` | Docker, load balancer, Prometheus | none / none / staff session | `horilla/urls.py:37-136` |
| Django admin | `/admin/` | Superusers | Session | `horilla/urls.py` |
| i18n | `/i18n/`, `/jsi18n/` | Browser | none | `horilla/urls.py` |

## 2. REST API (`/api/`)

### 2.1 Authentication and session contract
- `POST /api/auth/login/` — returns access and refresh tokens and a capabilities payload (role, permission booleans, installed features, exact version) (`horilla_api/api_views/auth/`).
- `POST /api/auth/refresh/` — rotates: returns a new refresh token and blacklists the used one.
- `POST /api/auth/logout/` — blacklists the refresh token.
- `POST /api/auth/reset-password/`.
- Token lifetimes: access 60 min, refresh 30 days; `CHECK_REVOKE_TOKEN` revokes tokens after a password change (`horilla/settings/base.py:151-175`).
- Authentication class sets the company ContextVar (data scoping) and, since the fork, activates the user's timezone (`horilla_api/authentication.py`).
- Default permission: `IsAuthenticated`. Pagination: page number, 20 per page. Filtering: django-filter.
- Throttles: `anon` 60/min, `user` 600/min, `login` 12/min, `bulk` 6/min (env-overridable `THROTTLE_*`) (`horilla/settings/base.py:110-149`).

### 2.2 Documentation
- Swagger: `/api/swagger/`, `/api/docs/`; ReDoc: `/api/redoc/`; raw schema at `/api/swagger<format>/` (for example `.json`). Public only when `DEBUG` is on, otherwise admin-only (`horilla_api/urls.py:20-21`).
- Notes: the schema metadata advertises a BSD licence while the project is LGPL-2.1 (per `docs/Horilla_HRM_FEATURES.md` §13).

### 2.3 Endpoint groups

| Group | Routes | Main resources (from URL patterns) |
|---|---|---|
| `auth/` | 4 | login, refresh, logout, reset-password |
| `base/` | 57 | companies, departments, job-positions, job-roles, worktypes, employee-shift, employee-shift-schedules, rotating-shifts and assigns, rotating-worktypes and assigns, shift-requests (approve/cancel), worktype-requests (approve/cancel), individual requests and rotations, capabilities |
| `employee/` | 27 | list/employees, employees/<pk>, employee-work-information, employee-bank-details, employee-type, employee-archive, bulk archive/update, work-info import/export, employee-selector, manager-check, policies, disciplinary-action and types, document-request and documents (approve/reject, bulk) |
| `attendance/` | 26 | clock-in, clock-out, attendance CRUD, attendance-validate, overtime-approve, attendance-hour-account, late-come-early-out-view, attendance-activity, today-attendance, offline-employees count/list and mail, my-attendance and detail, attendance requests, permission and type checks, mail templates |
| `leave/` | 32 | available-leave, leave-type, assign-leave, request, user-request, approve, reject, cancel, request-bulk-action, allocation-request, allocation approve/reject, user-allocation-request, company-leave, holiday, status and permission checks |
| `payroll/` | 17 | payslip list/detail/download, payslip-send-mail, loan-account, reimbursement (path spelled `reimbusement/`), tax-bracket, allowance, deduction |
| `recruitment/` | 39 | recruitments, stages, candidates, interviews, surveys and related actions |
| `onboarding/` | 18 | onboarding stages, tasks, candidates |
| `offboarding/` | 23 | offboarding pipelines, stages, employees, tasks, resignation letters |
| `pms/` | 49 | periods, objectives, key results, feedback, anonymous feedback, meetings, questions |
| `helpdesk/` | 22 | tickets, ticket types, claim requests, comments, FAQs, department managers |
| `project/` | 12 | projects, stages, tasks, timesheets (list scope applied to detail since 2.2.0) |
| `asset/` | 8 | assets, categories, requests, allocations |
| `notifications/` | 5 | list, mark read, delete |
| `mobile/` | 1 | `home/` — one call returning the whole mobile home screen |
| `/api/geofencing/` | 5 | company geofence setup (get/post/put/delete), employee location check |
| `/api/facedetection/` | 4 | company face-detection switch, employee face image get/post |

Total about 360 REST routes.

### 2.4 Behavioural notes for API consumers
- Several API views re-implement web logic rather than calling shared services. Leave approval through `/api/leave/approve/<pk>/` deducts available days before carried-forward days, the opposite of web manager approval (`horilla_api/api_views/leave/views.py:738-752` vs `leave/views.py:1118-1131`).
- Attendance API views star-import `attendance.views.views` and `attendance.views.clock_in_out`; clock-in/out through the API runs the same `clock_in`/`clock_out` code as the web, including the fork's employee-timezone handling (`horilla_api/api_views/attendance/views.py`, changed in commit c5ba10744).
- Model `clean()` rules are not run by `HorillaModel.save()`; whether an API write enforces a business rule depends on the serializer or view.

## 3. Web routes (server-rendered)

About 2,400 `path()` entries. They return full pages or HTMX fragments and are not a stable contract.

| Module | Routes |
|---|---|
| `base/urls.py` | 450 |
| `recruitment/urls.py` | 271 |
| `payroll/urls/` (urls 96, component_urls 120, tax_urls 23) | 239 |
| `employee/urls.py` | 232 |
| `attendance/urls.py` | 228 (some duplicated names/paths, per `attendance/MODULE_SUMMARY.md` §5) |
| `pms/urls.py` | 220 |
| `leave/urls.py` | 210 |
| `asset/urls.py` | 124 |
| `project/urls.py`, `helpdesk/urls.py` | 100 each |
| `onboarding/urls.py` | 82 |
| `offboarding/urls.py` | 81 |
| `report/urls.py` | 63 |
| `biometric/urls.py` | 32 |
| `horilla_meet/urls.py` | 22 |
| `horilla_views/urls.py` | 18 |
| `master_import/urls.py` | 13 |
| `horilla_automations/urls.py` | 11 |
| `horilla_tour/urls.py` | 10 |
| `whatsapp/urls.py` | 9 |
| `horilla_backup/urls.py` | 6 |
| others | < 6 each |

Public (unauthenticated) web entry points worth noting: login, forgot/reset password, the first-run setup wizard (protected by `DB_INIT_PASSWORD`), the recruitment public application form, the candidate self-tracking login, and the tokenised onboarding portal (per `docs/Horilla_HRM_FEATURES.md` §3.9-3.10).

## 4. Operations endpoints

| Endpoint | Behaviour |
|---|---|
| `GET /health/` | Always 200 `{"status":"ok","product":"horilla","api":1}`; no dependency checks; deliberately hides the release version |
| `GET /ready/` | Checks DB (503 on failure) and Redis when configured; reports `scheduler: ok|missing`; 503 for a missing scheduler only when `HORILLA_REQUIRE_SCHEDULER=1` |
| `GET /metrics/` | Prometheus text of scheduler job metrics; 404 unless the user is signed-in staff |

## 5. Internal interfaces between apps

| Provider | Interface | Consumers |
|---|---|---|
| `attendance` | `methods/utils.get_employee_attendance_summary()`, `views/summary.build_monthly_summary()` | `payroll` (batch run, components, payslip recompute), `base` |
| `attendance` | `views/clock_in_out.clock_in` / `clock_out` with a fake `Request` | `biometric`, `horilla_api`, scheduler, activity import |
| `attendance` | `WorkRecords` model | `leave` signals and methods |
| `leave` | `LeaveRequest`, `AvailableLeave` | `attendance` summary and hours balance, `payroll` encashment and loss of pay, `base` penalty signal |
| `base` | `PenaltyAccounts` post-save / post-delete signals | creates `payroll.Deduction`, edits `leave.AvailableLeave` |
| `base` | `MultipleApprovalCondition.approval_managers()` | `leave.LeaveRequest.save()` |
| `payroll` | `PayrollGeneralSetting.notice_period` | `offboarding` resignation conversion |
| `horilla` | `scheduling.register_job()` | every app's `scheduler.py` |
| `horilla_automations` | dynamic signal handlers | any model listed in `MODEL_CHOICES` |
| `whatsapp` | `create_request()` calling web views through `CustomRequestFactory` | shift, work type, leave, asset, attendance, bonus, reimbursement flows |
