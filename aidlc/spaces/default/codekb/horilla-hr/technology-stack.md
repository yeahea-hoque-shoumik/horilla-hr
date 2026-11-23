# Technology Stack: horilla-hr

Commit f2ab49933cfb40d295b3a9e65eba21996df2b0dc. Versions from `requirements.txt`, `Dockerfile` and settings. `requirements.txt` documents its pinning rule: pure-Python packages pinned exactly, packages with compiled extensions given a floor and a major cap.

## Languages and runtime

| Item | Version / value | Source |
|---|---|---|
| Python | 3.12 (image and CI); supported 3.12–3.14; 3.15 blocked by spaCy | `Dockerfile` (`python:3.12-slim`), `requirements.txt` header |
| Product version | Horilla 2.2.0, API contract version 1 | `horilla/__version__.py` |
| HTML/JS/CSS | Django templates, HTMX, Alpine.js, Hyperscript, Tailwind CSS (theme), Bootstrap (legacy screens), jQuery | `static/`, `horilla_theme/static/cdn/` |

## Backend frameworks

| Library | Version | Purpose |
|---|---|---|
| Django | ~=5.2.17 | Web framework |
| django-environ | 0.14.0 | `.env` and `DATABASE_URL` parsing |
| djangorestframework | 3.18.1 | REST API |
| djangorestframework-simplejwt | 5.5.1 | JWT auth with rotation and blacklist |
| PyJWT | 2.15.1 | JWT library (pinned for advisories) |
| drf-yasg | 1.21.15 | Swagger / ReDoc |
| django-filter | 26.1 | List and API filtering |
| django-apscheduler | 0.7.0 | DB job store for APScheduler |
| APScheduler | 3.11.3 | Background jobs |
| django-auditlog | 3.4.1 | Field-level audit log |
| django-simple-history | 3.13.0 | Historical tables |
| django-axes[ipware] | 8.3.1 | Login lockout |
| django-cors-headers | 4.9.0 | CORS |
| django-import-export | 4.4.1 | Import/export |
| django-mathfilters | 1.0.0 | Template math |
| django-model-utils | 5.0.0 | Model helpers |
| django-redis | 5.4.0 | Redis cache |
| django-storages | 1.14.6 | S3 media storage |
| django-widget-tweaks | 1.5.1 | Form rendering |
| swapper | 1.5.0 | Swappable models (notifications) |
| whitenoise | 6.9.0 | Static files |
| gunicorn | 23.0.0 | App server (gthread workers) |
| sentry-sdk[django] | 2.69.1 | Error tracking (inert without `SENTRY_DSN`) |

## Data, documents and AI/NLP

| Library | Version | Purpose |
|---|---|---|
| psycopg2-binary | >=2.9.13,<3 | PostgreSQL driver |
| pandas | >=2.1,<4 | Import/export processing |
| numpy | >=1.26,<3 | Numeric support |
| openpyxl | 3.1.5 | Excel read/write |
| XlsxWriter | 3.2.9 | Excel exports with charts |
| pdfkit | 1.0.0 | HTML to PDF via wkhtmltopdf (advisory mitigated by an XSS check before rendering) |
| xhtml2pdf | 0.2.17 | HTML to PDF |
| reportlab | 4.0.9 | PDF generation |
| PyMuPDF | >=1.28.2,<2 | Resume PDF parsing |
| beautifulsoup4 | 4.15.0 | HTML parsing |
| bleach | 6.4.0 + tinycss2 1.5.1 | HTML sanitising |
| spacy | >=3.8.16,<3.9 | Resume entity extraction |
| en_core_web_sm | 3.8.0 (GitHub wheel) | spaCy English model |
| rapidfuzz | >=3.14.6,<4 | Fuzzy matching |
| phonenumbers | 9.0.39 | Phone validation |
| pycountry | 24.6.1 | Country data |
| arabic-reshaper 3.0.1, python-bidi >=0.6.11,<0.7 | — | Right-to-left PDF text |
| pillow | >=13.0.0,<14 | Images |
| cryptography | >=50.0.0,<51 | Crypto |
| python-dateutil 2.9.0.post0, pytz 2026.3.post1 | — | Dates and zones (the fork's timezone code uses stdlib `zoneinfo`) |

## Integrations

| Library | Version | Purpose |
|---|---|---|
| google-api-python-client | 2.200.0 | Google Meet, Drive |
| google-auth-oauthlib | 1.4.1 | Google OAuth |
| google-cloud-storage | 3.0.0 | GCS media backend |
| requests 2.34.2, requests-oauthlib 2.0.0, urllib3 >=2.8.0,<3 | — | HTTP (LinkedIn, WhatsApp, Outlook) |
| pyzk | 0.9 | ZKTeco biometric devices |
| geopy | 2.5.0 | Geofence distance |
| (not listed) python-ldap / django-auth-ldap | — | Needed by `horilla_ldap` but absent from requirements |

## Infrastructure and tooling

| Item | Version / value | Source |
|---|---|---|
| PostgreSQL | 16 (`postgres:16-alpine` in compose and CI); SQLite default for bare local runs | `docker-compose.yml`, `.github/workflows/unit-tests.yml`, `horilla/settings/base.py:238-256` |
| Redis | 7 (`redis:7-alpine`, compose) | `docker-compose.yml:91` |
| Docker | multi-stage, non-root `appuser`; Compose v2.24+ for `!override`/`!reset` | `Dockerfile`, `docker-compose.prod.yml` |
| nginx | config in `docker/nginx.conf`; removed from the fork's production overlay | commit fb8ff8eec |
| Fork production host | gunicorn on host port 1000 (Cloudflare Tunnel per `docs/Horilla_HRM_FEATURES.md` §12.5), host PostgreSQL/Redis at `172.17.0.1` | `docker-compose.prod.yml` |
| Linting | ruff (pre-commit rev v0.16.5), black 24.4.2, isort 5.13.2 | `.pre-commit-config.yaml`, `pyproject.toml` |
| Tests | Django test runner; coverage >=7.0; python-dotenv 1.2.1 | `requirements.txt`, `Makefile` |
| CI | GitHub Actions: unit tests, quality (ruff, black/isort subset, check, pip-audit, gitleaks), Docker CI (Trivy), publish, CodeQL; Dependabot | `.github/` |
| Localisation | 12 UI languages, gettext catalogs in `horilla/locale/` | `horilla/settings/base.py:386-399` |

## Front-end libraries (vendored; versions not determined in this scan)
HTMX, Alpine.js, Hyperscript, Tailwind CSS, Bootstrap, jQuery and jQuery UI, Select2, Chart.js, ApexCharts, Summernote, pivottable.js, jsPDF, OrgChart, driver.js, SweetAlert, moment.js, Font Awesome, Ionicons (folders in `static/` and `horilla_theme/static/cdn/`; library list partly per `docs/Horilla_HRM_FEATURES.md` §6.1).
