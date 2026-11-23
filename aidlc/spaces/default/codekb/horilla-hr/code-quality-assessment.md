# Code Quality Assessment: horilla-hr

Commit f2ab49933cfb40d295b3a9e65eba21996df2b0dc. No tests or linters were run in this scan; figures come from config files, file counts and reading code.

## 1. Tests

| App | Test files | Test methods |
|---|---|---|
| payroll | 39 | 850 |
| base | 25 | 224 |
| horilla_api | 27 | 167 |
| attendance | 16 | 161 |
| master_import | 1 | 132 |
| leave | 16 | 120 |
| report | 4 | 114 |
| horilla (core) | 6 | 37 |
| recruitment | 7 | 28 |
| employee | 3 | 21 |
| horilla_views | 5 | 20 |
| pms | 3 | 19 |
| asset | 2 | 16 |
| horilla_automations | 2 | 12 |
| helpdesk | 4 | 11 |
| horilla_auth | 2 | 10 |
| offboarding | 3 | 9 |
| horilla_audit | 2 | 8 |
| accessibility, biometric | 1 each | 5 each |
| others (onboarding, project, geofencing, facedetection, whatsapp, horilla_meet, horilla_backup, horilla_ldap, horilla_documents, horilla_crumbs, horilla_theme, horilla_widgets) | 1 each | 1–3 each |

- Runner: Django `manage.py test`; fixtures in `horilla/testkit/`. About 2,000 test methods; notifications ships its own vendored tests (`notifications/tests/tests.py`).
- Coverage: branch coverage via `.coveragerc`; measured 27.6% on 2026-09-01; CI floor `COV_FAIL_UNDER=26` (`Makefile`). Coverage source is only leave, attendance, base, payroll, recruitment, report, horilla_auth, employee, accessibility, horilla_api.
- Not run in CI: `master_import` (132 tests), `horilla/tests` (37), `notifications` — they are missing from `SMOKE_LABELS` (`Makefile`).
- The fork added `attendance/tests/test_clock_in_timezone.py`, `base/tests/test_company_timezone.py`, `base/tests/test_observability.py`.
- Thinly tested domains relative to size: onboarding (1 test), project (2), offboarding (9), helpdesk (11), employee (21), recruitment (28), pms (19).

## 2. Linting and formatting
- ruff restricted to bug-class rules (F502, F602, F632, F701, F702, F706, F707, E902, F821, B023, B012, F823) (`pyproject.toml`). The file records outstanding counts in other families: F811 49, F601 7, E722 bare except 148, B006 mutable defaults 80, B904 71, F841 167, F401 494, E711/E712 71, E501 1,791, F403/F405 1,138.
- black and isort run in pre-commit; CI applies them only to `horilla/settings` and `horilla/urls.py` (per `docs/Horilla_HRM_FEATURES.md` §11).
- Vendored `notifications` and migrations excluded.

## 3. CI/CD
- `.github/workflows/unit-tests.yml`: Postgres 16 service, missing-migration check (`makemigrations --check --dry-run`), `make test-cov`.
- `quality.yml` (ruff, partial black/isort, `manage.py check`, pip-audit, gitleaks, production settings gate), `docker-ci.yml` (build, boot, probe `/health/` and `/ready/`, Trivy), `docker-publish.yml` (version must match tag), `codeql.yml`; Dependabot.
- **Fork gap**: workflows trigger on `dev/v2.0` and `2.0` only; the working branch `db-migration` and the `apurba` remote are not covered, and fork commits (timezone, observability) show no evidence of a CI run.
- Fork deployment: manual `deploy.sh` with a DB backup before each deploy; no staging environment or automated rollback described.

## 4. Documentation quality
- Upstream: `README.md`, `CHANGELOG.md` (660 lines), `SECURITY.md`, `CONTRIBUTING.md`, `docker/README.md`, `horilla_api/README_API_DOCS.md`, `horilla_dbtemplate/README.md`, `horilla_tour/HORILLA_TOUR.md`.
- Fork: `docs/Horilla_HRM_FEATURES.md` (feature and architecture reference, 2026-11-03), `attendance/MODULE_SUMMARY.md` (deep module reference), `docs/horilla_db.dbml` (8.4k lines), `docs/horilla_db_dependency_tree.md`, `docs/horilla_db_domains.md`, `docs/MODULE_LINES_OF_CODE.md`, the Apurba comparison and integration plan, `docs/EMPLOYEE_SETUP_GUIDE.md`.
- Inline comments: recent hardening code explains reasons and cites advisories (settings, scheduling, payroll batch, leave reset, offboarding archive). Older code has docstrings that only repeat the function name.
- Drift: some docstrings say "Django 6.x" while Django 5.2 is pinned (`horilla/__init__.py:13`); `sync_roster_shifts` docstring says "daily at 00:05" but it runs every 4 h; API schema licence says BSD.

## 5. Quick ratings (good / fair / poor)

| Aspect | Rating | Evidence |
|---|---|---|
| Naming clarity | fair | Mostly clear; typos in identifiers (`exclued_leave_types`, `spesific_leave_types`, `WhatsappCredientials`, `reimbusement/`, `ACCESSBILITY_FEATURE`) |
| Function size | poor | Very large view modules (`leave/views.py` 6.7k lines, `attendance/views/views.py` 3.5k, `attendance/views/summary.py` 3.2k); long view functions |
| Error handling | fair | Hardened paths log and explain; 131 bare `except:`; `print(e)` in `leave/signals.py:80`; `contextlib.suppress(Exception)` around notifications |
| Test presence | fair | Strong in payroll, base, API, attendance, leave; weak in onboarding, project, offboarding, helpdesk |
| Duplication | poor | Leave deduction logic in three places with different orders; FBV and CBV versions of the same screens; duplicate routes in attendance |
| Dead code | fair | Commented-out middleware, signals and save methods; unused `ACCRUAL_PLAN`; uninstalled apps shipped |

## 6. Technical debt and defects

### 6.1 Defects (business-visible)
| # | Defect | Source |
|---|---|---|
| D1 | Auto payslip regenerates mid-period joiners and resets them to draft | `payroll/scheduler.py:62-79` |
| D2 | `recruitment_close` uses an import-time date and exact match | `recruitment/scheduler.py:9-28` |
| D3 | Monthly rotation crashes in December | `base/scheduler.py:97, 101-103, 203, 207-209` |
| D4 | Expired employee documents are never saved inactive; link points to assets; repeated notices | `asset/scheduler.py:74-105` |
| D5 | Penalty delete over-restores clamped leave | `base/signals.py:172-186` |
| D6 | Rejected attendance create-requests are not deleted | `attendance/views/requests.py:595-610` |
| D7 | Bulk attendance request crashes on an invalid day | `attendance/forms.py:1405` |
| D8 | Leave deduction order differs between web approval, auto-approval and API | `leave/views.py:1118`, `leave/views.py:473`, `horilla_api/api_views/leave/views.py:738` |
| D9 | Multi-level leave approval completes on the last approver regardless of earlier stages | `leave/views.py:1150-1196` |
| D10 | Approval condition selection uses a text sort of numeric values | `leave/models.py:1751` |

### 6.2 Design debt
- Scheduled jobs use server dates and are not timezone-aware per company (fork timezone feature only covers requests).
- Jobs are not idempotent; exact-date matching means a missed run is never caught up (rotations, shift/work-type switches, recruitment close, cyclic feedback).
- Two in-process schedulers outside `horilla.scheduling` (`horilla_backup/scheduler.py:21`, `biometric/views.py:431-504`, `biometric/cbv/biometric.py:288-335`); `pg_backup` too (not installed).
- Business validation lives in model `clean()` but `HorillaModel.save()` runs only the XSS check, so imports (`bulk_create`) and some API paths skip rules.
- Models render HTML (`*_col()` methods), mixing presentation into the domain layer.
- Global monkeypatches (`QuerySet.update` signals, model clean signals) and import-time class patching.
- Runtime URL registration for import error sheets; download link only works in the worker that created it.
- Access control relies on `manager_can_enter` plus per-view checks; `attendance/MODULE_SUMMARY.md` §5 lists views missing record checks.

### 6.3 Half-built or disabled
- Leave accrual (`ACCRUAL_PLAN`, `count`, `period_in`) unused.
- Resignation approval branch empty (`offboarding/models.py:523-524`).
- LDAP login disabled and its libraries missing.
- `outlook_auth`, `dynamic_fields`, `pg_backup` shipped but not installed.
- Several `post_migrate` repair functions commented out (`attendance/signals.py`, `leave/signals.py:94`, `base/signals.py:189`).
- Commented-out legacy `CompanyMiddleware` block (`base/middleware.py:42-207`).

### 6.4 Security and privacy observations (fork)
- nginx removed from production: login rate limit, `/metrics/` deny and upload size limit no longer enforced at the proxy.
- Access log includes scrubbed and clipped JSON bodies; pay amounts, names and e-mails are not scrubbed (`horilla/observability.py:181-212`).
- Client-IP trust (`AXES_PROXY_COUNT`) must match the tunnel set-up or lockout and the IP allow-list work on the wrong address.

### 6.5 Markers
- TODO/FIXME/HACK in non-migration code: effectively none (one TODO in vendored notification tests). Debt is recorded in comments and docs instead of markers.
