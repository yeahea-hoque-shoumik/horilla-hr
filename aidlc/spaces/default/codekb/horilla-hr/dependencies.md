# Dependencies: horilla-hr

Commit f2ab49933cfb40d295b3a9e65eba21996df2b0dc.

## 1. External runtime dependencies

### 1.1 Services

| Service | Required? | Used for | Configuration |
|---|---|---|---|
| PostgreSQL 16 | Yes in production (SQLite fallback for local) | All data, scheduler job store | `DATABASE_URL` or `DB_*` |
| Redis 7 | Optional (local memory otherwise); required by the fork's prod overlay (`REDIS_URL:?`) | Cache, readiness probe, pipeline cache version, accessibility cache | `REDIS_URL` |
| SMTP servers | Needed for any e-mail | Notifications, password reset, payslips, report subscriptions | `DynamicEmailConfiguration` rows per company (`base/models.py:2104`) |
| wkhtmltopdf | Needed by pdfkit PDFs | Payslip and document PDFs | system binary |
| Meta WhatsApp Cloud API | Optional | WhatsApp notifications, flows, webhook | `WhatsappCredientials` rows |
| Google Cloud (OAuth, Meet, Drive, GCS) | Optional | Meet links, Drive backup, GCS storage | `horilla_meet`, `horilla_backup`, `horilla/horilla_backends_gcp.py` |
| AWS S3 | Optional | Media storage | `AWS_*`, `DEFAULT_FILE_STORAGE`, `MEDIA_URL`, `NAMESPACE` (`horilla/settings/addons.py`) |
| LinkedIn API | Optional | Job posting | `LinkedInAccount` rows |
| Sentry | Optional | Error tracking | `SENTRY_DSN` |
| Biometric devices on the network | Optional | Punch capture | `BiometricDevices` rows (IP, port, credentials) |
| LDAP directory | Not usable as shipped | Login and user sync | backend commented out; libraries missing |
| Microsoft Azure (Outlook) | Not installed | Mail via OAuth | `outlook_auth` |
| spaCy model download (GitHub release asset) | Install time | Resume parsing | `requirements.txt` direct URL |

### 1.2 Python packages
Full list with versions in `technology-stack.md`. Packages with security-driven pins called out in `requirements.txt`: Django ~=5.2.17, djangorestframework 3.18.1, simplejwt 5.5.1, PyJWT 2.15.1, urllib3 >=2.8.0, pillow >=13, cryptography >=50, bleach 6.4.0, msgpack >=1.2.2, setuptools 84.0.0. Known unfixed advisory: pdfkit `from_string` (PYSEC-2026-2860), mitigated in `base.methods.generate_pdf` by an XSS check.

## 2. Internal cross-app dependencies

### 2.1 Dependency matrix (who imports or writes whom)

| From ↓ / To → | base | employee | attendance | leave | payroll | recruitment | others |
|---|---|---|---|---|---|---|---|
| base | — | models, dashboards | settings rows, dashboards | holidays used by leave; penalty → AvailableLeave | penalty → Deduction | — | horilla_views, notifications |
| employee | org models | — | (patched by attendance) | — | — | — | horilla_audit, accessibility |
| attendance | shifts, holidays, IP list, penalties, roster | Employee, work info | — | LeaveRequest (hard import), migration dependency | — | — | geofencing (unguarded), facedetection, biometric (guarded) |
| leave | holidays, company leaves, approval conditions | Employee, work info | WorkRecords, Attendance (compensatory) | — | — | — | notifications |
| payroll | company, settings | Employee, work info | monthly summary, conflict resolutions | leave types, encashment, loss of pay | — | — | asset (fines, guarded) |
| recruitment | org models | Employee (managers, interviewers) | — | — | — | — | horilla_meet |
| onboarding | — | creates Employee | — | — | — | Candidate, Recruitment | — |
| offboarding | — | archives Employee, disables login | — | — | default notice period | — | — |
| pms | — | Employee | — | — | bonus encashment via employee bonus points | — | — |
| asset | — | Employee | — | — | fines | — | horilla_documents (expiry job) |
| report | all | all | all | all | all | all | pms, asset, onboarding, offboarding, auditlog |
| horilla_api | all | all | star-imports views | views/models | models | models | all domains |
| biometric | — | Employee | clock_in/clock_out | — | — | — | pyzk |
| whatsapp | announcements, requests | Employee | attendance request view | leave views | reimbursement views | — | asset requests |

### 2.2 Coupling hot spots
- **attendance ⇄ leave** (two-way): `attendance/migrations/0002_initial.py` depends on `leave/0001_initial`; `attendance/views/summary.py` imports `LeaveRequest` unguarded; leave signals write `attendance.WorkRecords`; `leave.CompensatoryLeaveRequest` exists only when attendance is installed. Neither app can be removed alone (`attendance/MODULE_SUMMARY.md` §5).
- **payroll → attendance**: payroll runs, payslip recompute and overtime/loss-of-pay components read the attendance monthly summary; payroll templates include attendance templates unconditionally (`attendance/MODULE_SUMMARY.md` §6).
- **base → payroll and leave via signals**: `PenaltyAccounts` signals create payroll deductions and edit leave balances (`base/signals.py:61-186`).
- **Conditional schema**: `base.EmployeeShift.grace_time_id`, `base.PenaltyAccounts.late_early_id`, `leave_request_id`, `leave_type_id` and `attendance.WorkRecords.leave_request_id` exist only when the other app is installed, so installing or removing apps changes tables.
- **Import-time patching**: `attendance` patches `employee` filters, list views and profile tabs; `biometric` edits the attendance sidebar; `horilla_api/__init__.py` mutates `INSTALLED_APPS`.
- **Star imports**: `horilla_api/api_views/attendance/views.py` imports `*` from two attendance view modules.
- **Template shadowing**: `horilla_theme/templates/` overrides app templates (413 files).
- **Shared "Horilla Bot" user**: many notices are sent from a user looked up by the username "Horilla Bot".

### 2.3 Circular references
- `attendance` ⇄ `leave` (models, signals, migrations).
- `base` ⇄ `employee` (employee models import base org models; base signals, dashboards and scheduler import employee models lazily inside functions).
- `base` ⇄ `attendance` (base models declare FKs to attendance models when installed; attendance imports base models).
These are resolved with lazy imports inside functions and string model references.

## 3. Deployment dependencies

| Item | Detail |
|---|---|
| Processes | `web` (gunicorn, scale freely), `scheduler` (`manage.py run_scheduler`, exactly one replica) |
| Release tasks | `docker/entrypoint.sh`: wait for DB, generate a secret key if missing, compile messages, `migrate`, `collectstatic` (skipped in the scheduler container via `HORILLA_SKIP_RELEASE_TASKS=1`) |
| Seed data on migrate | `EmployeeShiftDay` rows and default role groups (`base/signals.py:213-500`); attendance and clock-in fail if shift days are missing |
| Fork deploy | `deploy.sh`: `init-env <domain>`, `setup-db`, deploy with a `pg_dump -Fc` backup into `backups/`, rebuild image every deploy, wait for healthy web; `status`, `logs`, `stop` |
