# Reverse Engineering Timestamp

## Run Record

- Date: 2026-11-19
- Commit: f2ab49933cfb40d295b3a9e65eba21996df2b0dc
- Branch: db-migration
- Run type: first full scan (no prior code knowledge base), Standard depth
- Performed by: developer agent (scan and synthesis in one pass; no architect pass)
- Purpose: source for a plain-English product feature report for product owners and business analysts (intent `product-feature-report`)

## What was verified

- Read in code: settings, root URLs, `HorillaModel`, scheduling registry, decorators, the fork's timezone and observability changes; models of `base`, `employee`, `attendance`, `leave` (in full), and the status/choice definitions of `payroll`, `recruitment`, `onboarding`, `offboarding`, `pms`, `project`, `asset`, `helpdesk`; every registered scheduled job; the signals of `base`, `attendance`, `leave`, `payroll`, `recruitment`; leave approval, rejection and auto-approval views; the offboarding archive flow; the mobile API leave approval; WhatsApp request flows; build, test and deploy configuration.
- Skimmed: most view, CBV, form, filter, template and API serializer modules; payroll calculation internals; report metric definitions; platform and integration apps. Claims from these areas in the knowledge base are taken from the in-repo references `docs/Horilla_HRM_FEATURES.md` and `attendance/MODULE_SUMMARY.md` and are marked "per doc".
- Left out unopened: `.venv/`, vendored static libraries, `media/`, migration bodies, caches, `.env` values other than `TIME_ZONE`/`DEBUG`/`HORILLA_ENV`, demo fixtures, generated `fk_tree.html` and `perm_baseline.json`, and AI-DLC's own files.

## Scope of Analysis

```yaml
scope_version: 1
kind: full
intent: product-feature-report
fingerprint: 522d56b4a4548634c77d46b4f4c04054d14213bc
analyzed:
  paths:
    - ./
  components:
    - base
    - employee
    - attendance
    - leave
    - payroll
    - recruitment
    - onboarding
    - offboarding
    - pms
    - project
    - asset
    - helpdesk
    - report
    - biometric
    - geofencing
    - facedetection
    - horilla_api
    - horilla
    - horilla_auth
    - accessibility
    - horilla_audit
    - horilla_views
    - horilla_theme
    - horilla_widgets
    - horilla_crumbs
    - horilla_documents
    - horilla_automations
    - horilla_dbtemplate
    - horilla_tour
    - master_import
    - notifications
    - horilla_backup
    - horilla_meet
    - horilla_ldap
    - whatsapp
    - outlook_auth
    - dynamic_fields
    - pg_backup
shallow:
  paths:
    - payroll/methods/
    - payroll/views/
    - report/metrics/
    - horilla_api/api_views/
    - horilla_api/api_serializers/
    - recruitment/views/
    - horilla_views/
    - horilla_theme/
    - horilla_dbtemplate/
    - master_import/datasets/
    - notifications/
    - docs/
```
