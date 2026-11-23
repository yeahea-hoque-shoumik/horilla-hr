<aside>
ℹ️

Based only on the two reference documents: **Apurba HRM v2** (`APPLICATION_FEATURE_REFERENCE.md`, generated 2026-11-04 from `master` @ `6dd2884`) and **Horilla HRMS 2.2.0** (`FEATURES.md`, reviewed 2026-11-03, branch `2.0`). "Not described" means the document doesn't mention it — not proof the code lacks it.

</aside>

## 1. At a glance

| Aspect | Apurba HRM v2 | Horilla HRMS 2.2.0 |
| --- | --- | --- |
| Purpose | Internal HRM for ApurbaTech (single organisation) | Open-source (LGPL-2.1) full-lifecycle HRMS, multi-company |
| Stack | FastAPI monolith, Jinja2 + vanilla JS, SQLAlchemy 2.0, Alembic | Django 5.2, templates + HTMX + Alpine.js, DRF + SimpleJWT |
| Database / cache | PostgreSQL; Redis optional (degrades gracefully) | PostgreSQL 16 (SQLite default locally); Redis optional |
| Scheduler | APScheduler in-process, lock-file owner among 4 Uvicorn workers | Dedicated `run_scheduler` process (DjangoJobStore) |
| Size | ~32.6k LOC core, 518 routes, 67 tables, 10 jobs | ~37 apps, ~250 models, 247 migrations, ~2,100 templates, ~25 jobs |
| Tests | 14 real pytest tests; no runner config; pytest not a dependency | ~1,994 tests, CI with coverage floor (27.6% branch coverage) |
| Languages | Not described (English) | 12 UI languages |
| Mobile | PWA (manifest + service worker) | REST API for a native mobile app (geofencing, face detection) |
| Scope breadth | Attendance, leave, WFH, overtime, approvals, onboarding quiz, calendar | Recruitment → onboarding → employee → attendance → leave → payroll → PMS → offboarding + assets, helpdesk, projects, reports |

## 2. Feature matrix

Legend: ✅ present · ⚠️ partial / different approach · ❌ not described

### 2.1 Core HR & organisation

| Feature | Apurba | Horilla | Notes |
| --- | --- | --- | --- |
| Employee master data & profiles | ✅ | ✅ | Horilla adds bank details, tags, notes, history tab |
| Org structure (dept, designation, team, office) | ✅ | ✅ |  |
| Org chart / hierarchy | ✅ | ✅ |  |
| Reporting managers with levels & effective dates | ✅ | ⚠️ | Horilla has one reporting manager in work info |
| Self-service profile edit (allow-listed fields) | ✅ | ✅ | Horilla gates it via an accessibility feature rule |
| Probation auto-promotion to full-time | ✅ | ❌ | Horilla tracks probation end date in onboarding only |
| Shift swap between two employees | ✅ | ⚠️ | Horilla has shift *requests*  • rotating shifts + rosters |
| Rotating shifts / rotating work from options | ❌ | ✅ |  |
| Roster planning & publishing | ❌ | ✅ |  |
| Multi-company tenancy | ❌ | ✅ | Company-scoped managers + company-scoped permissions |
| Disciplinary actions (warning/suspension/dismissal, auto login block) | ❌ | ✅ |  |
| Company policies & announcements | ❌ | ✅ |  |
| Employee document requests (upload/approve, expiry) | ❌ | ✅ |  |
| Bulk import wizard (map columns, row errors, history) | ❌ | ✅ | `master_import` |
| Onboarding knowledge quiz gate (must pass before using app) | ✅ | ❌ | Unique to Apurba (MCQ / typed, retry wrong answers) |
| Product tours | ❌ | ✅ | driver.js |

### 2.2 Attendance & time

| Feature | Apurba | Horilla | Notes |
| --- | --- | --- | --- |
| Web clock in/out | ✅ | ✅ | Horilla adds break activities + running at-work timer |
| Office-IP restriction | ✅ | ✅ |  |
| Geofencing / face detection (mobile) | ❌ | ✅ |  |
| Per-employee timezone ("today" in employee's zone) | ✅ | ❌ | Horilla uses project timezone (per doc) |
| Multi-region shift scheduling (BD + USA jobs) | ✅ | ⚠️ | Apurba hard-codes shift IDs per region |
| Clock-in back-date window / clock-out future window | ✅ | ⚠️ | Horilla has grace time + auto check-out |
| Late / half-day-late status logic with leave interplay | ✅ | ✅ | Apurba: detailed half-day threshold & 0.5-day deduction |
| Late/early penalties → leave deduction | ✅ | ✅ | Apurba: 3+ lates/week = 1 day; Horilla: configurable penalty → payroll deduction **or** leave cut |
| Auto clock-out | ✅ (23:59 job, biometric time preferred) | ✅ (every 5 min at shift auto-checkout) |  |
| Mark absent automatically | ✅ | ✅ (via work records) |  |
| Attendance claims / regularisation | ✅ | ✅ | Apurba: monthly quota + cutoff day + ledger refund; Horilla: requests, batch, spreadsheet import |
| Manager attendance validation | ❌ | ✅ |  |
| Monthly summary with conflict resolution & overrides | ❌ | ✅ |  |
| Work-hours deficit → leave deduction | ✅ | ❌ | `work_deficit`, `duration_for_one_leave` |
| Column-level attendance audit (DB trigger) | ✅ | ⚠️ | Horilla uses simple-history / auditlog (opt-in) |
| Biometric devices | ⚠️ ZKTeco SenseFace 2A only | ✅ ZKTeco/eSSL, Anviz, Matrix COSEC, Dahua, e-Time Office |  |
| Attendance PDF/Excel export | ✅ | ✅ |  |

### 2.3 Leave, WFH & overtime

| Feature | Apurba | Horilla | Notes |
| --- | --- | --- | --- |
| Leave types & balances | ✅ | ✅ | Horilla far richer: paid %, reset cycles, carry-forward with expiry, encashable, attachment required |
| Eligibility conditions (gender, service, dept…) | ❌ | ✅ |  |
| Half-day leave (first/second half) | ✅ single-day | ✅ at both range start & end |  |
| Working-days-only calculation | ✅ | ✅ |  |
| Emergency contact mandatory | ✅ | ❌ |  |
| Leave cancellation workflow | ✅ | ✅ |  |
| Leave on behalf (HR creates, auto-approved) | ✅ | ⚠️ | Not explicitly described for Horilla |
| **Append-only leave balance ledger** with event types, idempotent penalties, reconcile report | ✅ | ❌ | Apurba's standout; Horilla relies on balance rows + history |
| Carry-forward | ⚠️ manual script, not scheduled | ✅ automatic |  |
| Leave accrual | ❌ | ❌ | Horilla has unused `ACCRUAL_PLAN` |
| Leave allocation requests (ask for extra days) | ❌ | ✅ |  |
| Compensatory leave | ✅ via extra work approval | ✅ dedicated requests |  |
| Restricted leave periods | ❌ | ✅ |  |
| Leave encashment | ❌ | ✅ |  |
| Dedicated WFH request module (unlocks Home clock-in) | ✅ | ⚠️ | Horilla: work-from requests can model it |
| Overtime / extra work | ✅ holiday/weekend + auto 1.5× shift | ✅ monthly overtime accounts + approval |  |

### 2.4 Approvals & workflow

| Feature | Apurba | Horilla | Notes |
| --- | --- | --- | --- |
| Multi-level approvers | ✅ per employee, per request type, effective dates | ✅ condition-based chains (e.g. leave > 3 days) | Different models: assignment-based vs rule-based |
| Bulk approver assignment (check / replace / merge) | ✅ | ❌ |  |
| Bulk approve/reject from inbox | ⚠️ not described | ✅ |  |
| Approver history page | ✅ | ⚠️ |  |
| No-code automations (on create/update/delete → mail/notification) | ❌ | ✅ | `horilla_automations` |

### 2.5 Modules only Horilla has

| Module | Highlights |
| --- | --- |
| Payroll | Contracts, Gross-Up / CTC-Down structures, formula components, tax packs (India, US, UK), payslip PDF/email, payroll runs, loans, reimbursements, encashments |
| Recruitment | Pipeline kanban, candidates, interviews, surveys, public application form, resume NLP screening, talent pool, LinkedIn posting |
| Onboarding (hiring) | Stages/tasks, tokenised candidate portal, convert to employee |
| Offboarding | Exit pipelines, resignation letters, exit tasks, notice period |
| Performance (PMS) | OKRs, 360° feedback (cyclic), anonymous feedback, 1:1 meetings, bonus points |
| Projects | Projects, kanban stages, tasks, timesheets |
| Assets | Register, batches, requests, allocation/return, service requests, fines, expiry |
| Helpdesk | Tickets, claims, FAQs |
| Reports | 34 standard reports, pivot Explorer, saved views, scheduled report emails, access matrix |

### 2.6 Modules / features only Apurba has

| Feature | Highlights |
| --- | --- |
| Onboarding questionnaire gate | Middleware blocks every page until active questions are passed |
| Leave balance ledger | Single writer, 19 event types, actor + source tracking, reconcile endpoint |
| Attendance claim quota | Monthly max + cutoff day, auto refund on reject/delete |
| Google Calendar meeting scheduler | Create/update meetings, conflict check, day schedule, **best-time finder**, templates, public-holiday import |
| AI commit-quantity evaluation | Proxies to HRM AI engine using `git_username_mapping` |
| External attendance summary API | HTTP Basic for other internal systems |
| PWA | Installable, cache-first static assets |
| Negative-leave & work-hours Excel reports | Monthly e-mails, idempotent via run log |

### 2.7 Platform, security & ops

| Feature | Apurba | Horilla |
| --- | --- | --- |
| Auth | Password, Google sign-in, OTP reset | Password, LDAP, email 2FA OTP, forced first-login password change, reset |
| Brute-force protection | ❌ not described | ✅ django-axes lockout + DRF throttles + nginx rate limit |
| RBAC | Roles + permissions (union), super-admin flag, audit log | Django groups/permissions, company-scoped, permission matrix UI, feature accessibility rules |
| Production safety gate | ❌ (default `admin/admin123`, open CORS) | ✅ refuses default secret / `*` hosts / default init password |
| Input safety | Standard | XSS check on every save, SVG middleware, sandboxed formulas |
| API | JSON for own pages + Swagger | Versioned mobile REST API, JWT rotation/blacklist, capabilities payload |
| Notifications | E-mail only (+ email log) | E-mail, in-app inbox, WhatsApp |
| Integrations | Google Calendar/Sign-In, ZKTeco, MinIO file service, HRM AI, SMTP | LDAP, Google Meet, Drive backup, WhatsApp, LinkedIn, Outlook, S3, Sentry, Prometheus, 5 biometric vendors |
| Observability | `/health`, activity log of all API traffic | `/health`, `/ready`, `/metrics`, Sentry |
| CI / security scanning | SonarQube script only | CodeQL, Trivy, gitleaks, pip-audit, ruff, migration check |
| Deployment | Docker (single image), `deploy.sh` with Alembic migration gate | Multi-stage non-root image, gunicorn + nginx, prod overlay, entrypoint auto-migrate |
| UI framework | Mixed Tailwind + Bootstrap, inline JS, no build | Tailwind theme + legacy Bootstrap, generic list/kanban/pipeline views, saved filters, column prefs |
| Theming / white-label / i18n | Fixed theme, dark mode class | Colour themes per company, white-labelling, 12 languages, DB-stored templates |

## 3. Apurba HRM v2 — strengths & weaknesses

### ✅ Strengths

- **Deep, policy-specific attendance rules** — half-day thresholds, IP + WFH location logic, back-dating windows, 18 h span cap, leave/clock-in interplay. Built around how ApurbaTech actually works.
- **Append-only leave ledger** — every balance change has an event type, source and actor; penalties are idempotent per employee/date; a reconcile report exists. This is stronger auditability than Horilla's balance model.
- **Attendance claims with quota and cutoff** — a clean, bounded fix-a-missed-punch process with automatic refunds.
- **Per-employee timezone and multi-region shifts** (BD + USA) handled in the time model.
- **Assignment-based approval engine** with levels, effective dates, advisory higher levels and a bulk assignor — easy to reason about who approves whom.
- **Unique features**: onboarding knowledge gate, Google Calendar best-time meeting finder, AI commit evaluation, WFH module, external summary API, PWA.
- **DB-level consistency** — triggers recompute status, keep work duration in sync and refund claim counts.
- **Broad logging** — full API activity log with secret masking, column-level attendance audit, email/cron logs.
- **Simple to operate** — one process, Redis optional, `deploy.sh` refuses unsafe migrations and keeps the old container on build failure.

### ⚠️ Weaknesses

- **Narrow scope** — no payroll (package is empty), recruitment, offboarding, performance/OKR, assets, helpdesk or projects.
- **Single-company** — no tenancy model.
- **Almost no automated tests** — 14 real tests, no runner config, most `test_*.py` are live-DB scripts; core rules (clock-in, approvals, penalties, RBAC) are untested.
- **Security gaps** — CORS `.*` with credentials, seeded `admin/admin123`, SonarQube token in repo, 30-day JWT (role changes need re-login), no lockout/rate limiting or 2FA described.
- **Broken / unfinished pieces** — scheduler admin router not mounted (buttons 404); year-end carry-forward not scheduled.
- **Hard-coded configuration** — shift IDs per job, file-service URL/tenant, ADMS timezone; onboarding a new shift requires a code change.
- **Scaling limits** — container-local scheduler lock duplicates jobs with >1 replica; in-memory biometric counters per worker.
- **Penalty targeting** — always charges the lowest `leave_type_id`; missing balance row silently skips the penalty.
- **Tech debt & drift** — legacy routers/templates, ORM shims, mixed CSS frameworks, Python 3.11 vs 3.12, docs disagreeing with code (job times, 8 h vs 9 h divisor).
- **No i18n, no in-app notifications, single biometric vendor.**

## 4. Horilla HRMS — strengths & weaknesses

### ✅ Strengths

- **Full employee lifecycle** in one product — recruitment through offboarding, plus payroll, PMS, assets, helpdesk, projects.
- **Very capable payroll** — formula engine, Gross-Up/CTC-Down, tax packs, payroll runs with review step, loans/reimbursements/encashment.
- **Multi-company tenancy** with company-scoped data and permissions, plus a system check for unscoped models.
- **Strong security posture** — lockout, 2FA, forced password change, production gate, rate limits, XSS-on-save, protected media, sandboxed formulas, GHSA regression tests.
- **Engineering maturity** — ~2,000 tests, CI with CodeQL/Trivy/gitleaks/pip-audit, migration check, non-root multi-stage image, health/ready/metrics, Sentry.
- **Correct scheduler design** — a single dedicated scheduler process (with documented exceptions).
- **Reusable UI framework** — consistent list/kanban/pipeline/detail views with saved filters, column preferences, bulk actions, quick export.
- **Reporting** — 34 standard reports, pivot explorer, scheduled report subscriptions, access matrix.
- **Extensibility** — no-code mail automations, DB-stored templates, model extension (`_inherit`), many integrations, mobile API, 12 languages, white-labelling.
- **Open source** with an existing community and demo data.

### ⚠️ Weaknesses

- **Size and complexity** — ~37 apps, ~250 models, ~2,100 templates; heavy to learn, customise and keep in sync with upstream.
- **Low effective coverage** — 27.6% branch coverage despite the test count; several suites (`master_import`, core, notifications) aren't in CI.
- **Known bugs** — `recruitment_close` uses an import-time date and exact-date match; auto payslip regenerates mid-period joiners and resets status to draft every run.
- **Scheduler exceptions** — Drive backup and biometric "schedule" start in-process schedulers, risking duplicate runs/double polling; jobs are not idempotent.
- **Leave model gaps for us** — no accrual, no append-only ledger, no claim-quota concept, no mandatory emergency contact.
- **Time model** — per-employee timezone not described; single project timezone.
- **No Bangladesh tax pack** — packs cover India, US, UK, flat 10%; local payroll rules would need building.
- **Global monkeypatches** (`QuerySet.update` signals, clean signals) and heavy dependencies (spaCy model, PyMuPDF) increase upgrade risk and image size.
- **Operational gotchas** — `.env` doesn't override real env vars, prod overlay needs a rebuild per code change, cached templates need restart, Compose v2.24+ required.
- **Doc drift** — "Django 6.x" docstrings vs Django 5.2; API schema says BSD vs LGPL-2.1.
- **Mixed UI** — Tailwind theme plus legacy Bootstrap screens.

## 5. Summary & takeaways

<aside>
🎯

**Horilla is broader and more mature as a platform; Apurba is deeper in attendance/leave correctness for ApurbaTech's own policies.** Horilla wins on scope, payroll, tenancy, security, testing and ops. Apurba wins on the leave ledger, claim quotas, per-employee timezone, assignment-based approvals and a few unique features (onboarding gate, calendar best-time finder, AI commit evaluation).

</aside>

### Ideas Apurba could borrow from Horilla

- Production safety gate (refuse default secrets, open hosts, seeded admin) and restricted CORS.
- Login lockout, rate limiting and optional 2FA.
- A dedicated single scheduler process with `/ready` reporting, plus configurable (not hard-coded) shift-to-job mapping.
- CI pipeline: pytest + coverage floor, migration check, gitleaks, pip-audit, Trivy.
- Generic list-view patterns (saved filters, column prefs, bulk actions) to replace per-page inline JS.
- Leave-type configuration: reset cycles, carry-forward with expiry, eligibility conditions, restricted periods.
- In-app notifications and no-code automations.

### Ideas Horilla's approach could learn from Apurba

- Append-only balance ledger with idempotent penalties and a reconcile report.
- Bounded regularisation (monthly quota + cutoff day).
- Per-employee timezone in the attendance "today" calculation.
- Approver assignment with effective dates and a bulk assignor.

### Open questions

- Is the goal to extend Apurba HRM, adopt/fork Horilla, or cherry-pick ideas?
- If payroll is needed, what Bangladesh tax and statutory rules must it cover?
- Is multi-company / multi-tenant use on the roadmap?