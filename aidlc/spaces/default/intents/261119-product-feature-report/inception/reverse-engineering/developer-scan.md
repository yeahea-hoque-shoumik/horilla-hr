# Developer Code Scan: horilla-hr

Scan date: 2026-11-19. Commit: f2ab49933cfb40d295b3a9e65eba21996df2b0dc (branch `db-migration`). Scope: full rescan of the repository root (`./`) at Standard depth. No tests, builds or programs of the project were run.

## Developer Code Scan Results

### Scan Coverage
- **Analyzed deeply**:
  - `horilla/` (settings `horilla/settings/base.py`, `security.py`, `addons.py`, `local_settings.py`; `urls.py`; `models.py` (HorillaModel, XSS check); `scheduling.py`; `decorators.py` (`manager_can_enter`); `observability.py` fork changes; `__init__.py`; `__version__.py`)
  - `base/models.py` (Company with timezone, approval conditions, penalty accounts, shifts, rotations, requests, holidays, roster), `base/scheduler.py`, `base/signals.py`, `base/middleware.py` (company and timezone middleware)
  - `employee/models.py` (Employee, work info with timezone, bonus points, disciplinary actions), `employee/scheduler.py`, the archive and replace views in `employee/views.py`
  - `attendance/models.py`, `attendance/signals.py`, `attendance/scheduler.py`, the fork's timezone changes in `attendance/views/clock_in_out.py` and `attendance/methods/utils.py`; `attendance/MODULE_SUMMARY.md` read in full and spot-checked against `attendance/forms.py:1405`, `attendance/views/requests.py:595-610`, `attendance/signals.py`
  - `leave/models.py` (constants, LeaveType, AvailableLeave, LeaveRequest save/clean/approval helpers, allocation, restrictions, compensatory leave), `leave/signals.py`, `leave/scheduler.py`, the approve, reject and auto-approve paths in `leave/views.py` (lines ~455-500, 1044-1300)
  - `payroll/scheduler.py`, `payroll/signals.py`, `payroll/models/payroll_batch.py` (state machine), the Contract, Payslip, LoanAccount and Reimbursement fields in `payroll/models/models.py`, `payroll/tax_packs.py` pack names
  - `recruitment/scheduler.py`, `pms/scheduler.py`, `asset/scheduler.py`, `report/scheduler.py`; the status choices in `recruitment/models.py`, `onboarding/models.py`, `offboarding/models.py`, `pms/models.py`, `project/models.py`, `asset/models.py`, `helpdesk/models.py`
  - `offboarding/views.py:515-630` (archive stage turns off login), `offboarding/models.py:515-586` (resignation and notice period)
  - `horilla_api/__init__.py`, `horilla_api/urls.py`, the auth, attendance, leave and payroll API URL lists, `horilla_api/api_views/leave/views.py:729-770`
  - `whatsapp/utils.py` request-creation flows, `horilla_automations/models.py`, `accessibility/accessibility.py`, `geofencing/models.py`, `facedetection/models.py`, `biometric/models.py` device choices
  - Build and ops: `requirements.txt`, `pyproject.toml`, `.coveragerc`, `.pre-commit-config.yaml`, `Makefile`, `Dockerfile` (base images), `docker-compose.prod.yml`, `deploy.sh` commands, `.github/workflows/unit-tests.yml`
  - Fork history: `git log` and `git show --stat` of the 9 fork commits after the 2.2.0 release
- **Skimmed only**:
  - All app `views.py`, `cbv/`, `forms.py`, `filters.py`, `urls.py` (route counts only), `templates/` (counts only), `templatetags/`
  - `payroll/methods/` (component engine, tax calculation, batch run), `payroll/views/`, `payroll/forms/`
  - `report/` (`registry.py`, `metrics/*` slug list only), `recruitment/` views, `onboarding/` views, `pms/` views and signals, `helpdesk/` views, `asset/` views, `project/` views
  - `horilla_api/api_views/*` (except leave approve), `horilla_api/api_serializers/`
  - `horilla_views/`, `horilla_theme/`, `horilla_widgets/`, `horilla_crumbs/`, `horilla_audit/`, `horilla_dbtemplate/`, `horilla_tour/`, `horilla_documents/`, `horilla_meet/`, `horilla_backup/`, `horilla_ldap/`, `outlook_auth/`, `dynamic_fields/`, `pg_backup/`, `master_import/` (dataset file names), `notifications/` (vendored)
  - Tests: counted per app (`*/tests/test_*.py`), not read
  - `docs/` (in-repo feature references; used as cross-checks, flagged where not re-verified), `templates/` (root), `docker/`
- **Left out**:
  - `.venv/` (installed dependencies)
  - `static/` vendored libraries and `horilla_theme/static/cdn/` (third-party front-end assets)
  - `media/` (user uploads, gitignored)
  - `*/migrations/*` bodies (existence and count noted: 249 numbered migration files)
  - `__pycache__/`, `.idea/`, `.DS_Store`
  - `.env` (secrets; only the `TIME_ZONE`, `DEBUG` and `HORILLA_ENV` keys were read)
  - `load_data/*.json` demo fixtures, `fk_tree.html` (generated), `perm_baseline.json` (generated permission snapshot)
  - AI-DLC's install and workspace (`.claude/`, `aidlc/`, `.mcp.json`, the AI-DLC block of `.gitignore`)

### Packages Found
One Django project (`manage.py`, settings `horilla.settings`). Installed apps (from `INSTALLED_APPS`, `horilla/settings/base.py:44-100`, plus `geofencing` and `facedetection` appended by `horilla_api/__init__.py`):
- `base` — Django app — Python — company, org structure, shifts, rotations, requests, holidays, approvals, mail, dashboards, settings
- `employee` — Django app — Python — employee master data, work info, policies, discipline, bonus points
- `attendance` — Django app — Python — check-in/out, validation, overtime, late/early, work records, monthly summary
- `leave` — Django app — Python — leave types, balances, requests, allocation, restrictions, compensatory leave
- `payroll` — Django app — Python — contracts, salary structures, components, tax, payslips, payroll runs, loans, reimbursements
- `recruitment` — Django app — Python — job openings, pipeline, candidates, interviews, surveys, resume screening
- `onboarding` — Django app — Python — onboarding stages/tasks, candidate portal
- `offboarding` — Django app — Python — exit pipelines, resignation letters, exit tasks
- `pms` — Django app — Python — OKRs, 360 feedback, meetings, bonus point rules
- `project` — Django app — Python — projects, stages, tasks, timesheets
- `asset` — Django app — Python — asset register, requests, allocation, service requests
- `helpdesk` — Django app — Python — tickets, claims, FAQs
- `report` — Django app — Python — 34 standard reports, explorer, subscriptions
- `horilla_api` — DRF app — Python — mobile REST API
- `biometric`, `geofencing`, `facedetection` — Django apps — attendance capture channels
- `horilla_auth` — custom user model; `accessibility`, `horilla_audit`, `horilla_views`, `horilla_theme`, `horilla_widgets`, `horilla_crumbs`, `horilla_documents`, `horilla_automations`, `horilla_dbtemplate`, `horilla_tour`, `master_import`, `horilla_backup`, `horilla_meet`, `horilla_ldap`, `whatsapp` — platform and integration apps
- `notifications` — vendored django-notifications
- Shipped but not installed: `outlook_auth`, `dynamic_fields`, `pg_backup`

### Build System
- **Type**: pip (`requirements.txt`), Django management commands, Docker multi-stage image, Docker Compose (dev + prod overlay), `deploy.sh` (fork)
- **Config Files**: `requirements.txt`, `pyproject.toml` (ruff only), `.coveragerc`, `.pre-commit-config.yaml`, `Makefile`, `Dockerfile`, `docker-compose.yml`, `docker-compose.prod.yml`, `docker/entrypoint.sh`, `docker/gunicorn.conf.py`, `.env.dist`
- **Build Dependencies**: no internal packaging; apps import each other directly. Strong couplings: `attendance` ⇄ `leave` (migration `attendance/0002_initial` depends on `leave/0001_initial`; leave writes attendance `WorkRecords`), `payroll` → `attendance` (monthly summary feeds pay), `base` → `payroll`/`leave` (penalty signal creates deductions and cuts leave), `horilla_api` → every domain app (star imports from attendance views), `offboarding` → `payroll` (default notice period)

### APIs Discovered
- REST (DRF + SimpleJWT) — `horilla_api/urls.py` under `/api/` — about 360 routes across 15 groups (auth 4, base 57, pms 49, recruitment 39, leave 32, employee 27, attendance 26, offboarding 23, helpdesk 22, onboarding 18, payroll 17, project 12, asset 8, notifications 5, mobile 1) plus `/api/geofencing/` (5) and `/api/facedetection/` (4)
- Server-rendered web routes (HTMX) — about 2,400 `path()` entries; largest: `base/urls.py` 450, `recruitment/urls.py` 271, `employee/urls.py` 232, `attendance/urls.py` 228, `pms/urls.py` 220, `leave/urls.py` 210, payroll 239 across 3 modules
- Webhook — `whatsapp/views.py:whatsapp` (Meta webhook with signature check, `_webhook_signature_valid`)
- Ops endpoints — `/health/`, `/ready/`, `/metrics/` (`horilla/urls.py`)
- API docs — Swagger `/api/swagger/`, `/api/docs/`, ReDoc `/api/redoc/`

### Frameworks & Libraries
- Django — ~=5.2.17 — web framework
- djangorestframework — 3.18.1 — REST API; djangorestframework-simplejwt 5.5.1 + PyJWT 2.15.1 — JWT auth; drf-yasg 1.21.15 — API docs
- django-apscheduler 0.7.0 + APScheduler 3.11.3 — background jobs (one `run_scheduler` process)
- django-auditlog 3.4.1, django-simple-history 3.13.0 — audit/history
- django-axes 8.3.1 — login lockout; sentry-sdk 2.69.1 — error tracking
- django-filter 26.1, django-import-export 4.4.1, django-redis 5.4.0, django-storages 1.14.6, whitenoise 6.9.0, gunicorn 23.0.0
- psycopg2-binary >=2.9.13,<3 — PostgreSQL
- pandas >=2.1,<4, numpy >=1.26,<3, openpyxl 3.1.5, XlsxWriter 3.2.9 — import/export
- pdfkit 1.0.0, xhtml2pdf 0.2.17, reportlab 4.0.9, PyMuPDF >=1.28.2,<2 — PDF
- spacy >=3.8.16,<3.9 + en_core_web_sm 3.8.0 — resume parsing
- pyzk 0.9 — ZKTeco biometric; geopy 2.5.0 — geofence distance
- google-api-python-client 2.200.0, google-auth-oauthlib 1.4.1, google-cloud-storage 3.0.0 — Meet, Drive, GCS
- bleach 6.4.0, tinycss2 1.5.1 — HTML sanitising
- Front end (vendored, versions not determined): HTMX, Alpine.js, Tailwind CSS (theme), Bootstrap (legacy), jQuery, Select2, Chart.js, ApexCharts, Hyperscript, OrgChart, Font Awesome, Ionicons

### Test Coverage
- **Test Directories**: `<app>/tests/` in 33 apps; largest: `payroll/tests` (39 files, 850 tests), `base/tests` (25, 224), `horilla_api/tests` (27, 167), `attendance/tests` (16, 161), `master_import/tests` (1, 132), `leave/tests` (16, 120), `report/tests` (4, 114). Total about 2,000 test methods.
- **Test Frameworks**: Django test runner (`manage.py test`); no pytest. Fixtures in `horilla/testkit/`.
- **Coverage Config**: present (`.coveragerc`, branch coverage). `Makefile` floor `COV_FAIL_UNDER=26` (measured 27.6% on 2026-09-01). Coverage source covers only 10 apps.

### Code Quality Indicators
- **Linting**: ruff (bug-class rules only, `pyproject.toml`), black and isort via `.pre-commit-config.yaml`. The ruff config documents about 4,500 unfixed findings in other rule families.
- **CI/CD**: `.github/workflows/unit-tests.yml` (Postgres 16, missing-migration check, `make test-cov`), `quality.yml`, `docker-ci.yml`, `docker-publish.yml`, `codeql.yml`; `dependabot.yml`; CI triggers only on branches `dev/v2.0` and `2.0` (not the fork's `db-migration` branch).
- **Documentation**: upstream `README.md`, `CHANGELOG.md`, `SECURITY.md`, `CONTRIBUTING.md`; fork-written `docs/` (feature reference, Apurba comparison and integration plan, DB DBML, dependency tree, domains) and `attendance/MODULE_SUMMARY.md`. Inline comments explaining "why" are unusually thorough in recently hardened code (settings, scheduling, payroll batch, leave reset).

### Technical Debt Signals
- Scheduled jobs use server-local `date.today()`/`datetime.now()`, so the fork's new per-employee and per-company timezone does not reach `auto_punch_out`, `create_work_record`, `leave_reset`, payslip generation or disciplinary blocking (`attendance/scheduler.py`, `leave/scheduler.py`, `payroll/scheduler.py`, `employee/scheduler.py`). `Attendance.clean()` also checks "future check-out" against server time (`attendance/models.py:1061-1099`).
- Three leave-approval code paths deduct balance in different orders: manager approval in the web consumes carry-forward days first (`leave/views.py:1117-1131`); "no approval needed" types and the mobile API consume available days first (`leave/views.py:465-490`, `horilla_api/api_views/leave/views.py:738-752`).
- Multi-level leave approval does not enforce order: the request is approved when the last approver in the chain approves, whatever the earlier stages say (`leave/views.py:1150-1196`). Approval conditions are picked by `order_by("condition_value")`, a string sort (`leave/models.py:1745`).
- `recruitment_close` freezes "today" at import time and needs an exact date match (`recruitment/scheduler.py:9,25`).
- Auto payslip looks up existing payslips by period start but saves mid-period joiners with a later start, so they are recomputed and reset to draft every run (`payroll/scheduler.py:62-79`).
- `notify_expiring_documents` sets `document.is_active = False` but never saves, and runs every 4 h with an exact-day check, so the notice can repeat up to 6 times (`asset/scheduler.py:83-105`).
- Monthly shift and work-type rotation crashes in December (`today.replace(month=today.month + 1)`, `calendar.monthrange(year, month + 1)`) (`base/scheduler.py:118-131, 200-213`).
- `block_unblock_disciplinary` runs every 60 s over every past action and re-activates users after a suspension ends, which can override a later manual block (`employee/scheduler.py:20-95`).
- Penalty deletion restores the full deducted leave even when the deduction was clamped at zero (`base/signals.py:100-118, 172-186`).
- Attendance request rejection never deletes rejected "create" requests (`attendance/views/requests.py:601-605`); `BulkAttendanceRequestForm.save` calls a logger object (`attendance/forms.py:1405`).
- LDAP: the LDAP backend is commented out in `AUTHENTICATION_BACKENDS` and neither `django-auth-ldap` nor `python-ldap` is in `requirements.txt` (`horilla/settings/base.py:620-627`, `horilla_ldap/management/commands/import_ldap_users.py:13`).
- Two in-process schedulers outside the central design: `horilla_backup/scheduler.py:21`, `biometric/views.py:431-504` and `biometric/cbv/biometric.py:288-335`.
- `ACCRUAL_PLAN`, `LeaveType.count`, `period_in` are defined but unused (`leave/models.py:148, 247-248`).
- `ResignationLetter.save()` has an empty "approved" branch (`offboarding/models.py:519-523`).
- 131 bare `except:` clauses, 23 non-test modules with `print(`, star imports in `horilla_api`, import-time monkeypatching (attendance patches employee filters and views).
- The fork removed nginx from production (`fb8ff8eec`): the documented nginx login rate limit, `/metrics/` deny and upload limit no longer apply; gunicorn is published directly on host port 1000.
- The fork's access-log middleware logs scrubbed, clipped JSON request and response bodies; pay amounts such as `net_pay`, `gross_pay`, `wage` are not in the scrub list (`horilla/observability.py:181-212`).

## Handoff Summary
- **Intent-relevant finding**: The product is Horilla HRMS 2.2.0 (`horilla/__version__.py:8`) with a small set of fork additions (per-company and per-employee timezone in `base/models.py:121-153`, `employee/models.py:991-1056`, `base/middleware.py:507-562`, `attendance/views/clock_in_out.py`; structured access logging in `horilla/observability.py`; deploy script and nginx-free production overlay). The business rules a product report needs live mostly in model `save()`/`clean()` methods, signals and the 25 scheduled jobs, not in the views. Several rules behave differently by channel (web, mobile API, WhatsApp) and several jobs ignore the new timezone; these must be reported as gaps.
- **Risks / follow-up**: Payroll internals (`payroll/methods/`), report metric definitions and most view-level permission scoping were skimmed, not verified; claims about them in the knowledge base cite `docs/Horilla_HRM_FEATURES.md` or `attendance/MODULE_SUMMARY.md` and are marked as such. `docs/APURBA_TO_HORILLA_INTEGRATION_PLAN.md` describes planned (not built) features such as a leave ledger and claim quotas; do not report them as existing.
