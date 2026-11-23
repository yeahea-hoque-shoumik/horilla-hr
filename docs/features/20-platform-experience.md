# Platform experience

## Summary

This area covers what every user sees regardless of the HR topic: the common list, card, board and detail screens, dashboards, colour themes and languages, product tours, screen templates that HR can change, feature access rules and audit settings. These features shape how easy the system is to use and to adapt. Most of the descriptions here come from the fork's feature reference and were only partly checked in the code.

## Who uses it

- Every user works with the common screens, dashboards and tours.
- Administrators set themes, feature access rules, screen templates and audit settings.

## Features

### Common screens

- Lists, cards, boards (kanban), pipelines and detail pages share the same tools: search, filters, saved filters, grouping, choice and order of columns remembered per user, bulk update, delete and archive, and quick export. *Not yet verified in the code.*

### Dashboards

- A home dashboard by role (leadership, HR, manager, employee), an employee self-service dashboard, and a chart layout each user can arrange. *Not yet verified in the code.*

### Themes and languages

- Colour themes per company, dark mode and 12 interface languages. *Not yet verified in the code.*
- A **white-labelling** switch (showing the company's own branding instead of the product's) exists and is off by default (`horilla/settings/base.py`).

### Product tours

- Guided tours of the screens, with each user's progress remembered. *Not yet verified in the code.*

### Screen templates stored in the database

- Administrators can override screen templates in the database, with drafts, versions, a comparison of changes and a preview. *Not yet verified in the code.*

### Feature access rules

- Administrators decide who gets these features: the default employee view, the detailed view, editing one's own profile, the dashboard charts (gender, department, employees) and the birthdays list (`accessibility/accessibility.py`).

### Audit settings

- Administrators set audit tags, which kinds of record are tracked, which fields keep a history, and can block or unblock accounts. *Not yet verified in the code.*

## Who can do what

| Action | Who |
|---|---|
| Use common screens, dashboards and tours | Every signed-in user, limited by their permissions in each area |
| Set feature access rules | People with the permission to change permissions (Admin) |
| Set audit tags and audit settings | People with the audit tag and audit setting permissions (Admin) |
| Change themes and screen templates | Administrators. *Not yet verified in the code.* |

These come from the permission checks on the feature access and audit screens (`accessibility/views.py`, `horilla_audit/views.py`).

## Recommendations

- Suggestion: check the common-screen, dashboard, theme and template features in the code before the product review relies on them.
- Suggestion: list in one place which features each role group can see, as the feature access rules are separate from the permission groups.

## Related documents

- [Employees](02-employees.md): editing one's own profile.
- [Horilla HRM feature reference](../Horilla_HRM_FEATURES.md), section 6.

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
