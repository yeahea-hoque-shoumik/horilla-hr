# Code Structure: horilla-hr

Commit f2ab49933cfb40d295b3a9e65eba21996df2b0dc.

## Repository layout

```
horilla-hr/
├── manage.py                  Django entry point
├── horilla/                   project package (settings, urls, base model, scheduling, decorators, observability, inherit, menu, testkit)
├── <app>/                     ~36 Django apps, one per domain or platform service
├── templates/                 root templates (index, login, sidebar, dashboard, setup wizard, errors)
├── static/                    vendored front-end libraries and shared assets
├── load_data/                 demo fixtures (JSON) and avatars
├── docs/                      fork-written product and DB documentation
├── docker/                    entrypoint, gunicorn config, nginx config, Docker Hub notes
├── Dockerfile, docker-compose.yml, docker-compose.prod.yml, Makefile, deploy.sh
├── requirements.txt, pyproject.toml (ruff), .coveragerc, .pre-commit-config.yaml
└── .github/                   CI workflows, CODEOWNERS, dependabot, issue/PR templates
```

## Size by app (non-migration Python)

| App | Py files | Lines | Templates | Routes |
|---|---|---|---|---|
| base | 131 | 54,456 | 261 | 450 |
| payroll | 134 | 48,269 | 182 | 239 |
| attendance | 64 | 26,339 | 148 | 228 |
| horilla_api | 116 | 22,562 | 0 | ~360 |
| recruitment | 54 | 21,842 | 184 | 271 |
| leave | 49 | 20,733 | 166 | 210 |
| report | 62 | 20,657 | 6 | 63 |
| employee | 40 | 17,908 | 150 | 232 |
| pms | 31 | 15,046 | 128 | 220 |
| asset | 25 | 9,189 | 87 | 124 |
| project | 24 | 7,694 | 70 | 100 |
| horilla_views | 24 | 7,279 | 38 | 18 |
| offboarding | 23 | 6,911 | 52 | 81 |
| onboarding | 24 | 6,715 | 54 | 82 |
| master_import | 17 | 6,711 | 8 | 13 |
| helpdesk | 28 | 6,502 | 37 | 100 |
| horilla | 48 | 5,959 | 0 | 21 |
| biometric | 18 | 5,838 | 30 | 32 |
| whatsapp | 14 | 3,075 | 4 | 9 |
| horilla_automations | 18 | 2,283 | 7 | 11 |
| notifications (vendored) | 28 | 2,051 | 4 | — |
| horilla_audit | 20 | 1,958 | 4 | 4 |
| horilla_theme | 14 | 1,740 | 413 | 3 |
| horilla_dbtemplate | 11 | 1,711 | 3 | — |
| horilla_meet | 13 | 1,682 | 9 | 22 |
| horilla_tour | 11 | 1,193 | 3 | 10 |
| horilla_crumbs | 9 | 1,005 | 0 | — |
| horilla_backup | 13 | 807 | 3 | 6 |
| dynamic_fields (not installed) | 17 | 731 | 5 | 3 |
| outlook_auth (not installed) | 13 | 722 | 2 | 9 |
| accessibility | 17 | 646 | 2 | 3 |
| horilla_widgets | 14 | 449 | 12 | 2 |
| horilla_documents | 8 | 389 | 0 | — |
| horilla_ldap | 11 | 394 | 1 | — |
| geofencing | 10 | 349 | 1 | 5 |
| horilla_auth | 12 | 342 | 0 | — |
| facedetection | 10 | 336 | 1 | 4 |
| pg_backup (not installed) | 7 | 190 | 0 | — |

Total about 370k lines of Python excluding migrations; 249 numbered migration files.

## Typical app layout

```
<app>/
├── apps.py          AppConfig.ready(): imports signals and scheduler, appends the app's URL include to horilla.urls.urlpatterns, registers in settings.APPS / APP_URLS
├── models.py        models plus most business rules (save(), clean(), helper methods, list-column render methods)
├── signals.py       cross-app side effects
├── scheduler.py     register_job(...) calls for horilla.scheduling
├── sidebar.py       menu definition for the sidebar and settings menu
├── urls.py          routes (FBV and CBV mixed)
├── views.py or views/   function-based views (older)
├── cbv/             class-based views built on horilla_views generics (newer)
├── forms.py, filters.py, templatetags/, templates/, static/
├── methods.py / methods/   shared helpers
├── management/commands/    maintenance and seed commands
├── migrations/
└── tests/test_*.py
```

Exceptions: `payroll` splits models (`models/models.py`, `models/payroll_batch.py`, `models/tax_models.py`), urls (`urls/urls.py`, `component_urls.py`, `tax_urls.py`), forms and views into packages; `report` is organised as an engine (`registry.py`, `engine.py`, `metrics/`, `delivery.py`, `export.py`); `horilla_api` mirrors domains under `api_urls/`, `api_views/`, `api_serializers/`.

## File classification

| Category | Where |
|---|---|
| Model / entity | `<app>/models.py`, `payroll/models/*`, `horilla/models.py` (`HorillaModel`) |
| Controller / handler | `<app>/views.py`, `<app>/views/*.py`, `<app>/cbv/*.py`, `horilla_api/api_views/*`, `whatsapp/views.py` |
| Service / business logic | model methods; `attendance/views/clock_in_out.py`, `attendance/views/summary.py`; `leave/services.py`, `leave/methods.py`; `payroll/methods/*`; `report/engine.py`, `report/metrics/*`; `master_import/datasets/*` |
| Background jobs | `<app>/scheduler.py`, `base/management/commands/run_scheduler.py` |
| Cross-app events | `<app>/signals.py`, `horilla/signals.py` (pre/post scheduler and bulk-update signals) |
| Repository / data access | Django ORM; `base/horilla_company_manager.py` (company scoping) |
| Utility | `horilla/methods.py`, `base/methods.py`, `attendance/methods/utils.py`, `horilla/filters.py`, `horilla/group_by.py` |
| Configuration | `horilla/settings/*`, `<app>/sidebar.py`, `horilla/menu/*`, `.env.dist` |
| Middleware | `horilla/horilla_middlewares.py`, `horilla/observability.py`, `base/middleware.py`, `accessibility/middlewares.py`, `horilla_api/middleware.py` |
| Test | `<app>/tests/`, `horilla/testkit/` |
| Migration | `<app>/migrations/` |
| Static / templates | `<app>/templates/`, `horilla_theme/templates/` (overrides), `templates/`, `static/` |

## Code patterns

- **Fat models**: business rules sit in `save()`, `clean()` and helper methods; models also expose many `*_col()` / `*_actions()` methods that render HTML for list columns (`render_template`), coupling models to templates.
- **`HorillaModel` base** (`horilla/models.py`): audit fields, `is_active` soft archive, auditlog history field, XSS check on every save, metaclass supporting `_inherit` model extension (`horilla/inherit/`).
- **Company scoping**: `objects = HorillaCompanyManager("<path to company>")` per model.
- **Conditional schema**: fields and models defined only when another app is installed (`if apps.is_installed("attendance"):`).
- **Generic CBVs** (`horilla_views`): `HorillaListView`, `HorillaNavView`, `HorillaDetailedView`, `HorillaFormView`, `HorillaTabView`, kanban and pipeline views, configured by class attributes.
- **HTMX responses**: views return partials and `HX-Trigger` headers; `hx_request_required` decorator.
- **Decorators for access**: `login_required`, `permission_required`, `manager_can_enter`, `owner_can_enter`, `install_required`, `hx_request_required` (`horilla/decorators.py`).
- **Fake request objects** let the same view logic serve scheduler, biometric, import and WhatsApp callers (`attendance/methods/utils.py: Request`, `whatsapp/utils.py: CustomRequestFactory`).
- **Template shadowing**: `horilla_theme/templates/` is searched before app templates, so 413 theme templates override app copies.
- **Import-time patching**: `attendance` patches `employee` filters, list views and profile tabs; `biometric` inserts into the attendance sidebar.
- **Dynamic URL registration**: some views append URL patterns at runtime (import error sheets, `attendance/views/handle_attendance_errors.py:78`).

## Notable non-domain modules

| Module | Role |
|---|---|
| `horilla/scheduling.py` | Job registry; `run_scheduler` is the only executor |
| `horilla/observability.py` | JSON logging, request id, Sentry with PII scrubbing, scheduler metrics, access-log body capture (fork) |
| `horilla/settings/security.py` | Production fail-closed gate |
| `horilla/inherit/` | `_inherit` model and view extension with a patched migration autodetector |
| `horilla/testkit/` | Test factories (`make_company`, `make_user`, `make_employee`, domain factories) |
| `base/auth_backends.py` | `CompanyScopedBackend`, `stamp_company_on_create` |
| `base/backends.py` | `ConfiguredEmailBackend` (company SMTP) |
| `base/dashboard.py`, `base/ess_dashboard.py`, `base/dashboard_roles.py` | Home and self-service dashboards |
| `fk_dependency_tree.py` (root, fork) | Script producing `fk_tree.html` and `docs/horilla_db_dependency_tree.md` |
