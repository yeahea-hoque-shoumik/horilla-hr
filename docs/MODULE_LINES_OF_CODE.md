# Lines of Code per Module

Line and file counts for each of the 37 Django apps in Horilla HRMS, plus the shared folders that aren't apps, with a line count for every file. Generated on 2026-11-05 from the `2.0` branch working copy.

## How it was counted

- **Files:** only files git tracks, plus new files not in `.gitignore`. The virtual environment (`.venv`), `__pycache__` and other ignored files are left out.
- **File types counted:** Python (`.py`), HTML templates (`.html`), JavaScript (`.js`) and stylesheets (`.css`, `.scss`). Images, fonts, translations, JSON and Markdown aren't counted.
- **Lines:** physical lines (`wc -l` style), including blank lines and comments.
- **Categories:** *Python* is app code (not migrations or tests). *Test* is a `.py` file in a `tests/` folder or whose name starts with `test`. *Migration* is a `.py` file in a `migrations/` folder. *JS / CSS* is hand-written scripts and styles.
- **Minified files** (`*.min.js`, `*.min.css`) are listed in the per-file tables but left out of the file counts and totals.

## 1. Summary per Django app (sorted by total lines)

| # | Module | Files | **Total lines** | Python | Tests | Migrations | HTML | JS / CSS |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | [`horilla_theme`](#horilla_theme) | 446 | **94,091** | 1,717 | 23 | 103 | 74,005 | 18,243 |
| 2 | [`base`](#base) | 424 | **85,994** | 50,847 | 3,195 | 4,653 | 24,886 | 2,413 |
| 3 | [`payroll`](#payroll) | 334 | **78,802** | 34,507 | 13,762 | 3,333 | 25,777 | 1,423 |
| 4 | [`attendance`](#attendance) | 229 | **56,938** | 23,465 | 2,710 | 1,844 | 26,129 | 2,790 |
| 5 | [`recruitment`](#recruitment) | 271 | **49,801** | 21,199 | 643 | 2,635 | 23,656 | 1,668 |
| 6 | [`leave`](#leave) | 237 | **45,383** | 18,423 | 2,310 | 2,339 | 19,829 | 2,482 |
| 7 | [`employee`](#employee) | 210 | **40,744** | 17,355 | 508 | 1,695 | 19,315 | 1,871 |
| 8 | [`pms`](#pms) | 177 | **36,186** | 14,709 | 337 | 2,206 | 17,723 | 1,211 |
| 9 | [`horilla_api`](#horilla_api) | 117 | **22,549** | 19,148 | 3,401 | – | – | – |
| 10 | [`report`](#report) | 75 | **21,803** | 17,852 | 2,805 | 269 | 122 | 755 |
| 11 | [`asset`](#asset) | 127 | **21,030** | 8,952 | 237 | 1,212 | 10,385 | 244 |
| 12 | [`project`](#project) | 111 | **16,654** | 7,681 | 13 | 617 | 7,129 | 1,214 |
| 13 | [`helpdesk`](#helpdesk) | 73 | **16,510** | 6,242 | 260 | 952 | 8,569 | 487 |
| 14 | [`onboarding`](#onboarding) | 91 | **15,736** | 6,694 | 21 | 629 | 7,154 | 1,238 |
| 15 | [`offboarding`](#offboarding) | 84 | **15,278** | 6,656 | 255 | 1,056 | 7,191 | 120 |
| 16 | [`horilla_views`](#horilla_views) | 68 | **14,292** | 6,935 | 344 | 367 | 6,238 | 408 |
| 17 | [`horilla_tour`](#horilla_tour) | 101 | **11,855** | 903 | 290 | 10,532 | 130 | – |
| 18 | [`biometric`](#biometric) | 52 | **8,325** | 5,799 | 39 | 295 | 1,986 | 206 |
| 19 | [`master_import`](#master_import) | 27 | **7,930** | 4,342 | 2,369 | 46 | 1,173 | – |
| 20 | [`whatsapp`](#whatsapp) | 22 | **3,459** | 2,940 | 135 | 146 | 238 | – |
| 21 | [`horilla_automations`](#horilla_automations) | 31 | **3,072** | 2,104 | 179 | 215 | 260 | 314 |
| 22 | [`horilla_audit`](#horilla_audit) | 29 | **2,545** | 1,822 | 136 | 228 | 359 | – |
| 23 | [`notifications`](#notifications) | 40 | **2,482** | 949 | 1,102 | 253 | 47 | 131 |
| 24 | [`horilla_meet`](#horilla_meet) | 25 | **2,475** | 1,661 | 21 | 286 | 507 | – |
| 25 | [`horilla_dbtemplate`](#horilla_dbtemplate) | 16 | **1,929** | 1,711 | – | 70 | 148 | – |
| 26 | [`horilla_widgets`](#horilla_widgets) | 27 | **1,327** | 433 | 16 | – | 878 | – |
| 27 | [`horilla_backup`](#horilla_backup) | 20 | **1,111** | 786 | 21 | 161 | 143 | – |
| 28 | [`dynamic_fields`](#dynamic_fields) | 23 | **1,021** | 728 | 3 | 1 | 289 | – |
| 29 | [`horilla_crumbs`](#horilla_crumbs) | 10 | **1,005** | 977 | 28 | – | – | – |
| 30 | [`accessibility`](#accessibility) | 23 | **972** | 572 | 74 | 130 | 196 | – |
| 31 | [`outlook_auth`](#outlook_auth) | 16 | **759** | 719 | 3 | – | 37 | – |
| 32 | [`horilla_documents`](#horilla_documents) | 12 | **649** | 366 | 23 | 260 | – | – |
| 33 | [`horilla_auth`](#horilla_auth) | 14 | **530** | 203 | 139 | 188 | – | – |
| 34 | [`horilla_ldap`](#horilla_ldap) | 15 | **480** | 382 | 12 | 60 | 26 | – |
| 35 | [`geofencing`](#geofencing) | 13 | **440** | 324 | 25 | 52 | 39 | – |
| 36 | [`facedetection`](#facedetection) | 14 | **431** | 315 | 21 | 91 | 4 | – |
| 37 | [`pg_backup`](#pg_backup) | 8 | **190** | 187 | 3 | – | – | – |
| | **All 37 apps** | **3,612** | **684,778** | **290,605** | **35,463** | **36,924** | **284,568** | **37,218** |

## 2. Shared folders that aren't apps

| Folder | What it is | Files | **Total lines** | Python | Tests | HTML | JS / CSS |
|---|---|---:|---:|---:|---:|---:|---:|
| [`horilla`](#horilla) | Project core: settings, URLs, middleware, testkit, scheduling | 48 | **5,843** | 5,267 | 576 | – | – |
| [`templates`](#templates) | Site-wide templates | 40 | **9,809** | – | – | 9,476 | 333 |
| [`static`](#static) | Site-wide static assets, mostly third-party libraries | 290 | **244,799** | – | – | 504 | 244,295 |
| [`docker`](#docker) | Container helper scripts | 1 | **51** | 51 | – | – | – |
| [`auth`](#auth) | Auth page templates | 1 | **70** | – | – | 70 | – |
| **All shared folders** | | **380** | **260,572** | | | | |

**Minified files left out of the totals:** `horilla_theme`: 5 files, 8,797 lines; `static`: 21 files, 52,309 lines.

## 3. Highlights

- **All 37 apps:** 3,612 files and 684,778 lines.
- **Whole project** (apps plus shared folders, minified files left out): 3,992 files and about 945,350 lines.
- **Largest apps by lines:** `horilla_theme` (94,091), `base` (85,994), `payroll` (78,802), `attendance` (56,938), `recruitment` (49,801).
- **Most files:** `horilla_theme` (446), `base` (424), `payroll` (334), `recruitment` (271), `leave` (237).
- **Smallest apps:** `pg_backup` (190 lines, 8 files), `facedetection` (431 lines, 14 files), `geofencing` (440 lines, 13 files), `horilla_ldap` (480 lines, 15 files), `horilla_auth` (530 lines, 14 files).

**15 largest files across all apps:**

| # | File | Type | Lines |
|---:|---|---|---:|
| 1 | `base/views.py` | Python | 8,914 |
| 2 | `leave/views.py` | Python | 6,678 |
| 3 | `base/management/commands/create_branch_demo_fixtures.py` | Python | 4,967 |
| 4 | `horilla_theme/static/horilla_theme/assets/css/v1_styles.css` | CSS | 4,965 |
| 5 | `horilla_theme/static/horilla_theme/assets/css/tailwind.css` | CSS | 4,873 |
| 6 | `employee/views.py` | Python | 4,657 |
| 7 | `recruitment/views/views.py` | Python | 4,569 |
| 8 | `horilla_theme/static/horilla_theme/assets/js/htmxSelect2.js` | JS | 4,444 |
| 9 | `payroll/models/models.py` | Python | 4,369 |
| 10 | `pms/views.py` | Python | 4,272 |
| 11 | `base/forms.py` | Python | 3,733 |
| 12 | `attendance/views/views.py` | Python | 3,472 |
| 13 | `base/models.py` | Python | 3,322 |
| 14 | `attendance/templates/attendance/dashboard.html` | HTML | 3,316 |
| 15 | `attendance/views/summary.py` | Python | 3,214 |

## 4. Things to know when reading the numbers

- **`horilla_theme` is mostly templates.** It holds the themed copies of other apps' templates; about 309 of its 413 templates replace an app template of the same name. So part of each feature's template size sits here, not in the feature's own folder.
- **`horilla_tour`'s migrations are unusually large** (over 10,000 lines). They are 86 migration files, nearly all of them data migrations that load the step-by-step guided-tour content for each screen (`0002_seed_default_tours.py` … `0087_seed_faq_view_tour.py`), not schema changes.
- **`payroll` has the most tests** (about 13,800 lines), more than any other app.
- **`horilla_api` has no templates.** It's the JSON API for the mobile app; its code is grouped by the feature it exposes (leave, attendance, payroll, ...).
- **Very small test counts** (3–40 lines) usually mean an empty `tests/__init__.py` or a placeholder file, not real test coverage.
- **`static/` is mostly third-party code** (JavaScript and CSS libraries), not Horilla's own code.

## 5. Line count of every file

Each module's files are listed by folder path. Click a module to expand its list.

### accessibility

**23 files, 972 lines**.

<details>
<summary>Show all 23 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `accessibility.py` | Python | 10 |
| `admin.py` | Python | 5 |
| `apps.py` | Python | 15 |
| `cbv_decorators.py` | Python | 44 |
| `decorators.py` | Python | 40 |
| `filters.py` | Python | 122 |
| `methods.py` | Python | 51 |
| `middlewares.py` | Python | 48 |
| `migrations/0001_initial.py` | Migration | 74 |
| `migrations/0002_initial.py` | Migration | 38 |
| `migrations/0003_alter_defaultaccessibility_is_active.py` | Migration | 18 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 23 |
| `signals.py` | Python | 71 |
| `templates/accessibility/accessibility.html` | HTML | 174 |
| `templates/accessibility/filter_form_body.html` | HTML | 22 |
| `templatetags/__init__.py` | Python | 0 |
| `templatetags/accessibility_filters.py` | Python | 19 |
| `tests/__init__.py` | Test | 1 |
| `tests/test_middleware_access.py` | Test | 73 |
| `urls.py` | Python | 25 |
| `views.py` | Python | 99 |

</details>

### asset

**127 files, 21,030 lines**.

<details>
<summary>Show all 127 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 1 |
| `admin.py` | Python | 36 |
| `apps.py` | Python | 33 |
| `cbv/accessibility.py` | Python | 31 |
| `cbv/asset.py` | Python | 137 |
| `cbv/asset_batch_no.py` | Python | 154 |
| `cbv/asset_category.py` | Python | 446 |
| `cbv/asset_history.py` | Python | 226 |
| `cbv/asset_tab.py` | Python | 180 |
| `cbv/dashboard.py` | Python | 77 |
| `cbv/request_and_allocation.py` | Python | 1,321 |
| `dashboard.py` | Python | 407 |
| `filters.py` | Python | 971 |
| `forms.py` | Python | 692 |
| `migrations/0001_initial.py` | Migration | 396 |
| `migrations/0002_initial.py` | Migration | 322 |
| `migrations/0003_asset_quantity.py` | Migration | 18 |
| `migrations/0004_alter_asset_owner.py` | Migration | 20 |
| `migrations/0005_assetitem_assetassignment_asset_item_id.py` | Migration | 39 |
| `migrations/0006_backfill_asset_items.py` | Migration | 61 |
| `migrations/0007_assetgeneralsetting.py` | Migration | 83 |
| `migrations/0008_alter_asset_asset_tracking_id_and_more.py` | Migration | 33 |
| `migrations/0009_assetrequestcomment.py` | Migration | 87 |
| `migrations/0010_assetservicerequest_assetservicerequestnote.py` | Migration | 57 |
| `migrations/0011_alter_assetassignment_return_status.py` | Migration | 18 |
| `migrations/0012_alter_asset_is_active_and_more.py` | Migration | 78 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 1,122 |
| `resources.py` | Python | 21 |
| `scheduler.py` | Python | 110 |
| `sidebar.py` | Python | 117 |
| `static/src/asset/dashboard.js` | JS | 129 |
| `static/src/asset_category/assetCategoryView.js` | JS | 115 |
| `templates/asset/action_column.html` | HTML | 101 |
| `templates/asset/asset_creation.html` | HTML | 156 |
| `templates/asset/asset_import.html` | HTML | 36 |
| `templates/asset/asset_information.html` | HTML | 209 |
| `templates/asset/asset_item_bulk_edit.html` | HTML | 69 |
| `templates/asset/asset_list.html` | HTML | 310 |
| `templates/asset/asset_report_form.html` | HTML | 61 |
| `templates/asset/asset_return_form.html` | HTML | 92 |
| `templates/asset/asset_update.html` | HTML | 277 |
| `templates/asset/dashboard.html` | HTML | 1,744 |
| `templates/asset/dashboard_allocated_assets.html` | HTML | 47 |
| `templates/asset/dashboard_asset_requests.html` | HTML | 107 |
| `templates/asset/settings/asset_rule.html` | HTML | 66 |
| `templates/asset_history/asset_history_filter.html` | HTML | 109 |
| `templates/asset_history/asset_history_list.html` | HTML | 215 |
| `templates/asset_history/asset_history_nav.html` | HTML | 108 |
| `templates/asset_history/asset_history_single_view.html` | HTML | 150 |
| `templates/asset_history/asset_history_view.html` | HTML | 12 |
| `templates/asset_history/group_by.html` | HTML | 204 |
| `templates/batch/asset_batch_empty.html` | HTML | 45 |
| `templates/batch/asset_batch_number_creation.html` | HTML | 66 |
| `templates/batch/asset_batch_number_list.html` | HTML | 158 |
| `templates/batch/asset_batch_number_update.html` | HTML | 60 |
| `templates/batch/asset_batch_number_view.html` | HTML | 76 |
| `templates/category/asset_category.html` | HTML | 234 |
| `templates/category/asset_category_form.html` | HTML | 60 |
| `templates/category/asset_category_view.html` | HTML | 210 |
| `templates/category/asset_empty.html` | HTML | 79 |
| `templates/category/asset_filter_export.html` | HTML | 105 |
| `templates/cbv/asset/asset_form.html` | HTML | 18 |
| `templates/cbv/asset/asset_items_action.html` | HTML | 14 |
| `templates/cbv/asset/asset_list_with_count.html` | HTML | 21 |
| `templates/cbv/asset/detail_action.html` | HTML | 45 |
| `templates/cbv/asset_batch_no/actions.html` | HTML | 42 |
| `templates/cbv/asset_batch_no/asset_batch_no.html` | HTML | 51 |
| `templates/cbv/asset_batch_no/assets_col.html` | HTML | 10 |
| `templates/cbv/asset_batch_no/detail_actions.html` | HTML | 42 |
| `templates/cbv/asset_category/accordion_actions.html` | HTML | 49 |
| `templates/cbv/asset_category/asset_category_group_by.html` | HTML | 320 |
| `templates/cbv/asset_category/filter.html` | HTML | 119 |
| `templates/cbv/asset_history/asset_history_export.html` | HTML | 81 |
| `templates/cbv/asset_history/asset_history_filter.html` | HTML | 119 |
| `templates/cbv/asset_history/asset_history_home.html` | HTML | 143 |
| `templates/cbv/asset_history/assign_condition.html` | HTML | 16 |
| `templates/cbv/asset_history/return_condition.html` | HTML | 18 |
| `templates/cbv/request_and_allocation/allocation_option.html` | HTML | 23 |
| `templates/cbv/request_and_allocation/asset_actions.html` | HTML | 25 |
| `templates/cbv/request_and_allocation/asset_allocation_action.html` | HTML | 23 |
| `templates/cbv/request_and_allocation/asset_allocation_filter.html` | HTML | 100 |
| `templates/cbv/request_and_allocation/asset_detail_action.html` | HTML | 41 |
| `templates/cbv/request_and_allocation/asset_filter.html` | HTML | 69 |
| `templates/cbv/request_and_allocation/asset_renewal.html` | HTML | 19 |
| `templates/cbv/request_and_allocation/asset_renewal_filter.html` | HTML | 81 |
| `templates/cbv/request_and_allocation/asset_request_action.html` | HTML | 97 |
| `templates/cbv/request_and_allocation/asset_request_detail_action.html` | HTML | 31 |
| `templates/cbv/request_and_allocation/asset_request_filter.html` | HTML | 101 |
| `templates/cbv/request_and_allocation/asset_request_option.html` | HTML | 62 |
| `templates/cbv/request_and_allocation/asset_service_request_filter.html` | HTML | 34 |
| `templates/cbv/request_and_allocation/detail_action_asset_allocation.html` | HTML | 15 |
| `templates/cbv/request_and_allocation/filter.html` | HTML | 212 |
| `templates/cbv/request_and_allocation/forms/allo_form.html` | HTML | 11 |
| `templates/cbv/request_and_allocation/forms/asset_approve_form.html` | HTML | 11 |
| `templates/cbv/request_and_allocation/forms/asset_item_field.html` | HTML | 15 |
| `templates/cbv/request_and_allocation/forms/reassign_form.html` | HTML | 37 |
| `templates/cbv/request_and_allocation/forms/req_form.html` | HTML | 8 |
| `templates/cbv/request_and_allocation/forms/service_request_action_form.html` | HTML | 31 |
| `templates/cbv/request_and_allocation/forms/service_request_add_note_form.html` | HTML | 30 |
| `templates/cbv/request_and_allocation/forms/service_request_add_note_success.html` | HTML | 5 |
| `templates/cbv/request_and_allocation/forms/service_request_form.html` | HTML | 6 |
| `templates/cbv/request_and_allocation/forms/service_request_notes.html` | HTML | 21 |
| `templates/cbv/request_and_allocation/forms/service_request_status_edit.html` | HTML | 33 |
| `templates/cbv/request_and_allocation/nav.html` | HTML | 85 |
| `templates/cbv/request_and_allocation/request_and_allocation.html` | HTML | 122 |
| `templates/cbv/request_and_allocation/return_status.html` | HTML | 11 |
| `templates/cbv/request_and_allocation/service_request_history.html` | HTML | 54 |
| `templates/cbv/request_and_allocation/service_request_list_action.html` | HTML | 45 |
| `templates/cbv/request_and_allocation/service_request_status.html` | HTML | 11 |
| `templates/cbv/request_and_allocation/status.html` | HTML | 11 |
| `templates/request_allocation/asset_allocation_creation.html` | HTML | 68 |
| `templates/request_allocation/asset_approve.html` | HTML | 41 |
| `templates/request_allocation/asset_request_allocation_list.html` | HTML | 717 |
| `templates/request_allocation/asset_request_allocation_view.html` | HTML | 408 |
| `templates/request_allocation/asset_request_creation.html` | HTML | 63 |
| `templates/request_allocation/group_by.html` | HTML | 935 |
| `templates/request_allocation/individual_allocation.html` | HTML | 128 |
| `templates/request_allocation/individual_own.html` | HTML | 139 |
| `templates/request_allocation/individual_request.html` | HTML | 132 |
| `templatetags/__init__.py` | Python | 0 |
| `templatetags/assets_custom_filter.py` | Python | 22 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_asset_page.py` | Test | 222 |
| `tests/test_category_smoke.py` | Test | 15 |
| `urls.py` | Python | 611 |
| `views.py` | Python | 2,237 |

</details>

### attendance

**229 files, 56,938 lines**.

<details>
<summary>Show all 229 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `admin.py` | Python | 28 |
| `apps.py` | Python | 34 |
| `cbv/__init__.py` | Python | 0 |
| `cbv/accessibility.py` | Python | 53 |
| `cbv/attendance_activity.py` | Python | 280 |
| `cbv/attendance_request.py` | Python | 672 |
| `cbv/attendance_tab.py` | Python | 198 |
| `cbv/attendances.py` | Python | 1,009 |
| `cbv/break_point.py` | Python | 131 |
| `cbv/check_in_check_out.py` | Python | 42 |
| `cbv/dashboard.py` | Python | 114 |
| `cbv/dashboard_offline_online.py` | Python | 98 |
| `cbv/grace_time.py` | Python | 221 |
| `cbv/hour_account.py` | Python | 284 |
| `cbv/ip_restriction.py` | Python | 79 |
| `cbv/late_come_and_early_out.py` | Python | 321 |
| `cbv/my_attendances.py` | Python | 254 |
| `cbv/tab_shell.py` | Python | 39 |
| `dashboard.py` | Python | 952 |
| `filters.py` | Python | 1,522 |
| `forms.py` | Python | 1,456 |
| `management/__init__.py` | Python | 0 |
| `management/commands/__init__.py` | Python | 0 |
| `management/commands/create_summary_fixtures.py` | Python | 576 |
| `methods/__init__.py` | Python | 0 |
| `methods/utils.py` | Python | 818 |
| `migrations/0001_initial.py` | Migration | 785 |
| `migrations/0002_initial.py` | Migration | 615 |
| `migrations/0003_alter_attendanceovertime_year.py` | Migration | 18 |
| `migrations/0004_historicalattendanceactivity.py` | Migration | 57 |
| `migrations/0005_alter_attendanceovertime_options_and_more.py` | Migration | 31 |
| `migrations/0006_workrecords_unique_work_record_per_employee_per_date.py` | Migration | 20 |
| `migrations/0007_attendanceconflictresolution_attendancedailyhours_and_more.py` | Migration | 76 |
| `migrations/0008_attendance_attendance_date_idx_and_more.py` | Migration | 25 |
| `migrations/0009_attendancesummaryoverride.py` | Migration | 40 |
| `migrations/0010_alter_attendance_is_active_and_more.py` | Migration | 113 |
| `migrations/0011_attendancevalidationcondition_minimum_at_work_to_validate_and_more.py` | Migration | 25 |
| `migrations/0012_alter_workrecords_message.py` | Migration | 21 |
| `migrations/0013_alter_attendanceconflictresolution_resolution.py` | Migration | 18 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 2,094 |
| `scheduler.py` | Python | 122 |
| `sidebar.py` | Python | 243 |
| `signals.py` | Python | 242 |
| `static/attendance/actions.js` | JS | 1,640 |
| `static/cbv/attendance/hour_account.js` | JS | 208 |
| `static/cbv/attendance_activity.js` | JS | 443 |
| `static/dashboard/attendanceChart.js` | JS | 499 |
| `templates/attendance/attendance/attendance_activites_view.html` | HTML | 54 |
| `templates/attendance/attendance/attendance_add_batch.html` | HTML | 49 |
| `templates/attendance/attendance/attendance_empty.html` | HTML | 173 |
| `templates/attendance/attendance/attendance_filters.html` | HTML | 148 |
| `templates/attendance/attendance/attendance_nav.html` | HTML | 282 |
| `templates/attendance/attendance/attendance_on_time.html` | HTML | 190 |
| `templates/attendance/attendance/attendance_request_one.html` | HTML | 366 |
| `templates/attendance/attendance/attendance_view.html` | HTML | 122 |
| `templates/attendance/attendance/batch_attendance_form.html` | HTML | 41 |
| `templates/attendance/attendance/batches_list.html` | HTML | 99 |
| `templates/attendance/attendance/export_filter.html` | HTML | 172 |
| `templates/attendance/attendance/form.html` | HTML | 9 |
| `templates/attendance/attendance/group_by.html` | HTML | 999 |
| `templates/attendance/attendance/import_error_alert.html` | HTML | 14 |
| `templates/attendance/attendance/tab_content.html` | HTML | 1,204 |
| `templates/attendance/attendance/update_form.html` | HTML | 9 |
| `templates/attendance/attendance/update_hx_form.html` | HTML | 1 |
| `templates/attendance/attendance/validate_attendance.html` | HTML | 265 |
| `templates/attendance/attendance/validate_attendance_empty.html` | HTML | 9 |
| `templates/attendance/attendance_account/attendance_account_export_filter.html` | HTML | 214 |
| `templates/attendance/attendance_account/attendance_account_filter.html` | HTML | 157 |
| `templates/attendance/attendance_account/attendance_overtime_view.html` | HTML | 38 |
| `templates/attendance/attendance_account/form.html` | HTML | 20 |
| `templates/attendance/attendance_account/group_by.html` | HTML | 321 |
| `templates/attendance/attendance_account/nav.html` | HTML | 178 |
| `templates/attendance/attendance_account/overtime_empty.html` | HTML | 42 |
| `templates/attendance/attendance_account/overtime_list.html` | HTML | 214 |
| `templates/attendance/attendance_account/update_form.html` | HTML | 20 |
| `templates/attendance/attendance_activity/activity_empty.html` | HTML | 21 |
| `templates/attendance/attendance_activity/activity_filters.html` | HTML | 151 |
| `templates/attendance/attendance_activity/activity_list.html` | HTML | 312 |
| `templates/attendance/attendance_activity/attendance_activity_view.html` | HTML | 35 |
| `templates/attendance/attendance_activity/export_filter.html` | HTML | 183 |
| `templates/attendance/attendance_activity/group_by.html` | HTML | 336 |
| `templates/attendance/attendance_activity/import_activity.html` | HTML | 84 |
| `templates/attendance/attendance_activity/nav.html` | HTML | 173 |
| `templates/attendance/attendance_activity/single_attendance_activity.html` | HTML | 167 |
| `templates/attendance/break_point/condition.html` | HTML | 93 |
| `templates/attendance/break_point/condition_form.html` | HTML | 47 |
| `templates/attendance/break_point/condition_view.html` | HTML | 0 |
| `templates/attendance/components/in_out_component.html` | HTML | 118 |
| `templates/attendance/dashboard.html` | HTML | 3,316 |
| `templates/attendance/dashboard/dashboard.html` | HTML | 252 |
| `templates/attendance/dashboard/on_break_employees.html` | HTML | 34 |
| `templates/attendance/dashboard/overtime_table.html` | HTML | 131 |
| `templates/attendance/dashboard/to_validate_table.html` | HTML | 156 |
| `templates/attendance/grace_time/assign_shift.html` | HTML | 21 |
| `templates/attendance/grace_time/grace_time.html` | HTML | 124 |
| `templates/attendance/grace_time/grace_time_form.html` | HTML | 121 |
| `templates/attendance/grace_time/grace_time_table.html` | HTML | 38 |
| `templates/attendance/grace_time/validation_condition_tab.html` | HTML | 24 |
| `templates/attendance/ip_restriction/action_col.html` | HTML | 62 |
| `templates/attendance/ip_restriction/add_more_ip_fields.html` | HTML | 26 |
| `templates/attendance/ip_restriction/restrict_form.html` | HTML | 50 |
| `templates/attendance/ip_restriction/restrict_update_form.html` | HTML | 24 |
| `templates/attendance/late_come_early_out/export_filter.html` | HTML | 246 |
| `templates/attendance/late_come_early_out/group_by.html` | HTML | 279 |
| `templates/attendance/late_come_early_out/late_come_early_out_filters.html` | HTML | 202 |
| `templates/attendance/late_come_early_out/nav.html` | HTML | 145 |
| `templates/attendance/late_come_early_out/report_list.html` | HTML | 382 |
| `templates/attendance/late_come_early_out/reports.html` | HTML | 48 |
| `templates/attendance/late_come_early_out/reports_empty.html` | HTML | 21 |
| `templates/attendance/late_come_early_out/single_report.html` | HTML | 237 |
| `templates/attendance/late_come_early_out/tracking.html` | HTML | 12 |
| `templates/attendance/monthly_summary/_calendar_modal_host.html` | HTML | 826 |
| `templates/attendance/monthly_summary/_regularise_opener.html` | HTML | 18 |
| `templates/attendance/monthly_summary/bulk_resolve_panel.html` | HTML | 127 |
| `templates/attendance/monthly_summary/cal_day_hours.html` | HTML | 45 |
| `templates/attendance/monthly_summary/calendar_modal.html` | HTML | 498 |
| `templates/attendance/monthly_summary/conflict_resolve_panel.html` | HTML | 460 |
| `templates/attendance/monthly_summary/crp_hours.html` | HTML | 50 |
| `templates/attendance/monthly_summary/detail_popover.html` | HTML | 338 |
| `templates/attendance/monthly_summary/monthly_summary.html` | HTML | 975 |
| `templates/attendance/monthly_summary/regularise_confirm.html` | HTML | 116 |
| `templates/attendance/monthly_summary/table_partial.html` | HTML | 1,326 |
| `templates/attendance/own_attendance/attendances.html` | HTML | 337 |
| `templates/attendance/own_attendance/filters.html` | HTML | 139 |
| `templates/attendance/own_attendance/group_by.html` | HTML | 238 |
| `templates/attendance/own_attendance/nav.html` | HTML | 80 |
| `templates/attendance/own_attendance/own_empty.html` | HTML | 21 |
| `templates/attendance/own_attendance/view_own_attendances.html` | HTML | 7 |
| `templates/attendance/penalty/form.html` | HTML | 113 |
| `templates/attendance/settings/attendance_rule.html` | HTML | 358 |
| `templates/attendance/settings/settings.html` | HTML | 28 |
| `templates/attendance/work_record/work_record_list.html` | HTML | 271 |
| `templates/attendance/work_record/work_record_view.html` | HTML | 163 |
| `templates/attendance_form.html` | HTML | 52 |
| `templates/cbv/attendance_activity/attendance_activity_home.html` | HTML | 127 |
| `templates/cbv/attendance_activity/attendance_export.html` | HTML | 30 |
| `templates/cbv/attendance_activity/delete_action.html` | HTML | 14 |
| `templates/cbv/attendance_activity/delete_inherit.html` | HTML | 8 |
| `templates/cbv/attendance_activity/detail_delete_action.html` | HTML | 25 |
| `templates/cbv/attendance_activity/filter.html` | HTML | 204 |
| `templates/cbv/attendance_request/attendance_request.html` | HTML | 110 |
| `templates/cbv/attendance_request/attendance_request_option.html` | HTML | 25 |
| `templates/cbv/attendance_request/attendance_request_tab.html` | HTML | 839 |
| `templates/cbv/attendance_request/comment.html` | HTML | 15 |
| `templates/cbv/attendance_request/request_actions.html` | HTML | 27 |
| `templates/cbv/attendance_request/status.html` | HTML | 11 |
| `templates/cbv/attendances/attendance_actions.html` | HTML | 41 |
| `templates/cbv/attendances/attendance_view_page.html` | HTML | 110 |
| `templates/cbv/attendances/attendances_export_page.html` | HTML | 180 |
| `templates/cbv/attendances/attendances_filter_page.html` | HTML | 221 |
| `templates/cbv/attendances/detail_view_activity_col.html` | HTML | 15 |
| `templates/cbv/attendances/ot_actions.html` | HTML | 117 |
| `templates/cbv/attendances/ot_cell.html` | HTML | 12 |
| `templates/cbv/attendances/ot_confirmation.html` | HTML | 83 |
| `templates/cbv/attendances/ot_tab_action.html` | HTML | 133 |
| `templates/cbv/attendances/validate_actions.html` | HTML | 76 |
| `templates/cbv/attendances/validate_button.html` | HTML | 37 |
| `templates/cbv/attendances/validate_tab_action.html` | HTML | 74 |
| `templates/cbv/attendances/validated_tab_action.html` | HTML | 48 |
| `templates/cbv/hour_account/hour_account.html` | HTML | 124 |
| `templates/cbv/hour_account/hour_account_main.html` | HTML | 9 |
| `templates/cbv/hour_account/hour_actions.html` | HTML | 37 |
| `templates/cbv/hour_account/hour_detail_action.html` | HTML | 35 |
| `templates/cbv/hour_account/hour_export.html` | HTML | 185 |
| `templates/cbv/hour_account/hour_filter.html` | HTML | 151 |
| `templates/cbv/hour_account/nav_hour_account.html` | HTML | 10 |
| `templates/cbv/late_come_and_early_out/actions_column.html` | HTML | 40 |
| `templates/cbv/late_come_and_early_out/detail_action.html` | HTML | 49 |
| `templates/cbv/late_come_and_early_out/late_come_and_early_out.html` | HTML | 130 |
| `templates/cbv/late_come_and_early_out/late_early_export.html` | HTML | 224 |
| `templates/cbv/late_come_and_early_out/late_early_filter.html` | HTML | 226 |
| `templates/cbv/late_come_and_early_out/penality.html` | HTML | 3 |
| `templates/cbv/my_attendances/my_attendance_filter.html` | HTML | 144 |
| `templates/cbv/my_attendances/my_attendances.html` | HTML | 54 |
| `templates/cbv/settings/applicable_on_clock_in_col.html` | HTML | 28 |
| `templates/cbv/settings/applicable_on_clock_out_col.html` | HTML | 28 |
| `templates/cbv/settings/break_point_action.html` | HTML | 29 |
| `templates/cbv/settings/check_in_check_out_col.html` | HTML | 21 |
| `templates/cbv/settings/grace_time_default_action.html` | HTML | 54 |
| `templates/cbv/settings/grace_time_shift.html` | HTML | 8 |
| `templates/cbv/settings/is_active_col_grace_time.html` | HTML | 31 |
| `templates/requests/attendance/attendance_comment.html` | HTML | 160 |
| `templates/requests/attendance/comment_view.html` | HTML | 74 |
| `templates/requests/attendance/filter.html` | HTML | 153 |
| `templates/requests/attendance/form.html` | HTML | 23 |
| `templates/requests/attendance/form_field.html` | HTML | 3 |
| `templates/requests/attendance/group_by.html` | HTML | 649 |
| `templates/requests/attendance/individual_view.html` | HTML | 146 |
| `templates/requests/attendance/nav.html` | HTML | 157 |
| `templates/requests/attendance/request_form.html` | HTML | 3 |
| `templates/requests/attendance/request_lines.html` | HTML | 514 |
| `templates/requests/attendance/request_new_form.html` | HTML | 69 |
| `templates/requests/attendance/requests_empty.html` | HTML | 98 |
| `templates/requests/attendance/update_form.html` | HTML | 12 |
| `templates/requests/attendance/view-requests.html` | HTML | 199 |
| `templatetags/__init__.py` | Python | 0 |
| `templatetags/attendancefilters.py` | Python | 256 |
| `tests/__init__.py` | Test | 0 |
| `tests/fixtures.py` | Test | 102 |
| `tests/test_adjust_minimum_hour.py` | Test | 60 |
| `tests/test_bulk_validate.py` | Test | 110 |
| `tests/test_company_leave_and_range.py` | Test | 67 |
| `tests/test_conflict_bulk_resolve.py` | Test | 159 |
| `tests/test_date_indexes.py` | Test | 114 |
| `tests/test_day_checking.py` | Test | 60 |
| `tests/test_export_holiday.py` | Test | 43 |
| `tests/test_export_scoping.py` | Test | 119 |
| `tests/test_half_day_resolution.py` | Test | 783 |
| `tests/test_hour_account_rebuild.py` | Test | 68 |
| `tests/test_ip_and_geofence_web.py` | Test | 215 |
| `tests/test_leave_dates_filtering.py` | Test | 45 |
| `tests/test_summary_override.py` | Test | 646 |
| `tests/test_top_absentees.py` | Test | 82 |
| `tests/test_workrecord_message_length.py` | Test | 37 |
| `urls.py` | Python | 1,126 |
| `views/__init__.py` | Python | 0 |
| `views/clock_in_out.py` | Python | 608 |
| `views/dashboard.py` | Python | 511 |
| `views/geofaceconfig.py` | Python | 12 |
| `views/handle_attendance_errors.py` | Python | 81 |
| `views/penalty.py` | Python | 75 |
| `views/process_attendance_data.py` | Python | 209 |
| `views/regularisation_import.py` | Python | 582 |
| `views/requests.py` | Python | 947 |
| `views/search.py` | Python | 490 |
| `views/summary.py` | Python | 3,214 |
| `views/views.py` | Python | 3,472 |

</details>

### base

**424 files, 85,994 lines**.

<details>
<summary>Show all 424 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 1 |
| `admin.py` | Python | 78 |
| `announcement.py` | Python | 458 |
| `apps.py` | Python | 31 |
| `auth_backends.py` | Python | 258 |
| `backends.py` | Python | 274 |
| `cbv/__init__.py` | Python | 0 |
| `cbv/announcement_cbv.py` | Python | 201 |
| `cbv/company.py` | Python | 211 |
| `cbv/company_leaves.py` | Python | 155 |
| `cbv/dashboard/dashboard.py` | Python | 241 |
| `cbv/department.py` | Python | 206 |
| `cbv/employee_shift.py` | Python | 131 |
| `cbv/employee_shift_shedule.py` | Python | 177 |
| `cbv/employee_type.py` | Python | 130 |
| `cbv/holidays.py` | Python | 282 |
| `cbv/job_position.py` | Python | 155 |
| `cbv/job_role.py` | Python | 152 |
| `cbv/mail_log_tab.py` | Python | 132 |
| `cbv/mail_server.py` | Python | 124 |
| `cbv/mail_template.py` | Python | 123 |
| `cbv/multiple_approval_condition.py` | Python | 274 |
| `cbv/penalty.py` | Python | 40 |
| `cbv/roster.py` | Python | 853 |
| `cbv/rotating_shift.py` | Python | 169 |
| `cbv/rotating_shift_assign.py` | Python | 424 |
| `cbv/rotating_work_type.py` | Python | 427 |
| `cbv/settings_rotatingwork.py` | Python | 177 |
| `cbv/settings_work_type.py` | Python | 126 |
| `cbv/shift_request.py` | Python | 690 |
| `cbv/work_shift_tab.py` | Python | 498 |
| `cbv/work_type_request.py` | Python | 516 |
| `checks.py` | Python | 104 |
| `context_processors.py` | Python | 493 |
| `countries.py` | Python | 855 |
| `dashboard.py` | Python | 2,050 |
| `dashboard_roles.py` | Python | 134 |
| `decorators.py` | Python | 108 |
| `demo_data/__init__.py` | Python | 10 |
| `demo_data/catalog.py` | Python | 121 |
| `demo_data/companies.py` | Python | 36 |
| `demo_data/dates.py` | Python | 218 |
| `demo_data/fixtures.py` | Python | 47 |
| `demo_data/inventory.py` | Python | 61 |
| `demo_data/media.py` | Python | 52 |
| `demo_data/modules/__init__.py` | Python | 6 |
| `demo_data/modules/announcements.py` | Python | 190 |
| `demo_data/modules/asset_expansion.py` | Python | 88 |
| `demo_data/modules/asset_features.py` | Python | 57 |
| `demo_data/modules/attendance_trend.py` | Python | 733 |
| `demo_data/modules/date_clamp.py` | Python | 436 |
| `demo_data/modules/employee_features.py` | Python | 200 |
| `demo_data/modules/employee_lifecycle.py` | Python | 165 |
| `demo_data/modules/employee_work_history.py` | Python | 92 |
| `demo_data/modules/helpdesk_expansion.py` | Python | 118 |
| `demo_data/modules/helpdesk_trend.py` | Python | 160 |
| `demo_data/modules/leave_trend.py` | Python | 303 |
| `demo_data/modules/offboarding_expansion.py` | Python | 142 |
| `demo_data/modules/offboarding_trend.py` | Python | 91 |
| `demo_data/modules/onboarding_trend.py` | Python | 139 |
| `demo_data/modules/payroll_features.py` | Python | 258 |
| `demo_data/modules/payroll_precise.py` | Python | 426 |
| `demo_data/modules/payroll_trend.py` | Python | 171 |
| `demo_data/modules/pms_trend.py` | Python | 295 |
| `demo_data/modules/project_trend.py` | Python | 286 |
| `demo_data/modules/recruitment.py` | Python | 63 |
| `demo_data/modules/recruitment_expansion.py` | Python | 189 |
| `demo_data/modules/recruitment_features.py` | Python | 231 |
| `demo_data/modules/request_windows.py` | Python | 307 |
| `demo_data/org.py` | Python | 132 |
| `demo_data/runner.py` | Python | 189 |
| `demo_data/sanitize.py` | Python | 186 |
| `demo_roles.py` | Python | 70 |
| `email_redaction.py` | Python | 72 |
| `ess_dashboard.py` | Python | 818 |
| `filters.py` | Python | 1,335 |
| `forms.py` | Python | 3,733 |
| `horilla_company_manager.py` | Python | 265 |
| `import_template_data.py` | Python | 241 |
| `management/commands/audit_perms.py` | Python | 91 |
| `management/commands/create_branch_demo_fixtures.py` | Python | 4,967 |
| `management/commands/createhorillauser.py` | Python | 75 |
| `management/commands/demo_data_inventory.py` | Python | 37 |
| `management/commands/horilladumpdata.py` | Python | 55 |
| `management/commands/load_demo_data.py` | Python | 145 |
| `management/commands/run_scheduler.py` | Python | 133 |
| `management/commands/seed_dashboard_demo_data.py` | Python | 581 |
| `management/commands/trigger_save.py` | Python | 44 |
| `methods.py` | Python | 1,935 |
| `middleware.py` | Python | 501 |
| `migrations/0001_initial.py` | Migration | 2,075 |
| `migrations/0002_initial.py` | Migration | 1,757 |
| `migrations/0003_alter_dynamicemailconfiguration_company_id_and_more.py` | Migration | 59 |
| `migrations/0004_rosterpublishlog_roster.py` | Migration | 56 |
| `migrations/0005_attendanceallowedip_company_id_and_more.py` | Migration | 43 |
| `migrations/0006_holidays_assigning_type_holidays_department_and_more.py` | Migration | 39 |
| `migrations/0007_setupchecklistdismissal.py` | Migration | 30 |
| `migrations/0008_companygroupassignment.py` | Migration | 35 |
| `migrations/0009_defaultexportpermission.py` | Migration | 31 |
| `migrations/0010_companylanguagesetting.py` | Migration | 31 |
| `migrations/0011_alter_companyleaves_options_and_more.py` | Migration | 21 |
| `migrations/0012_remove_companyleaves_company_id_and_more.py` | Migration | 22 |
| `migrations/0013_announcementexpire_company_id_and_more.py` | Migration | 31 |
| `migrations/0014_alter_rotatingworktype_name.py` | Migration | 18 |
| `migrations/0015_defaultexportpermission_unique_default_export_permission_per_company_and_more.py` | Migration | 23 |
| `migrations/0016_seed_default_export_permission.py` | Migration | 98 |
| `migrations/0017_alter_announcement_is_active_and_more.py` | Migration | 210 |
| `migrations/0018_alter_holidays_is_specific.py` | Migration | 18 |
| `migrations/0019_announcement_is_visible_to_all.py` | Migration | 18 |
| `migrations/0020_alter_company_address_alter_company_city_and_more.py` | Migration | 38 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 3,322 |
| `request_and_approve.py` | Python | 56 |
| `scheduler.py` | Python | 464 |
| `shift_decorators.py` | Python | 45 |
| `sidebar.py` | Python | 802 |
| `signals.py` | Python | 684 |
| `static/base/actions.js` | JS | 905 |
| `static/base/date_formatting.js` | JS | 85 |
| `static/base/date_settings.js` | JS | 27 |
| `static/base/filter.js` | JS | 25 |
| `static/base/time_formatting.js` | JS | 72 |
| `static/base/time_settings.js` | JS | 26 |
| `static/base/toggleColumn.js` | JS | 74 |
| `static/basedOn.js` | JS | 30 |
| `static/cbv/deleteFunc.js` | JS | 27 |
| `static/cbv/shift_request/shift_request_bulk_actions.js` | JS | 443 |
| `static/cbv/work_type_request/work_request_bulk_action.js` | JS | 410 |
| `static/holiday/action.js` | JS | 289 |
| `templates/announcement/announcement_form.html` | HTML | 51 |
| `templates/announcement/announcement_one.html` | HTML | 251 |
| `templates/announcement/announcement_update_form.html` | HTML | 41 |
| `templates/announcement/announcements_list.html` | HTML | 64 |
| `templates/announcement/as_p.html` | HTML | 62 |
| `templates/announcement/comment_view.html` | HTML | 130 |
| `templates/announcement/expiry_day.html` | HTML | 46 |
| `templates/announcement/viewed_by.html` | HTML | 23 |
| `templates/base/action_type/action_type.html` | HTML | 102 |
| `templates/base/action_type/action_type_form.html` | HTML | 75 |
| `templates/base/action_type/action_type_view.html` | HTML | 77 |
| `templates/base/audit_tag/audit_tag_form.html` | HTML | 57 |
| `templates/base/audit_tag/employee_account_block_unblock.html` | HTML | 101 |
| `templates/base/audit_tag/history_tracking_fields.html` | HTML | 4 |
| `templates/base/audit_tag/history_tracking_fields_content.html` | HTML | 148 |
| `templates/base/auth/filters.html` | HTML | 137 |
| `templates/base/auth/group.html` | HTML | 59 |
| `templates/base/auth/group_accordion.html` | HTML | 205 |
| `templates/base/auth/group_assign.html` | HTML | 60 |
| `templates/base/auth/group_assign_view.html` | HTML | 144 |
| `templates/base/auth/group_lines.html` | HTML | 157 |
| `templates/base/auth/group_user_assign.html` | HTML | 23 |
| `templates/base/auth/group_view.html` | HTML | 101 |
| `templates/base/auth/password_change.html` | HTML | 3 |
| `templates/base/auth/password_change_form.html` | HTML | 96 |
| `templates/base/auth/permission.html` | HTML | 20 |
| `templates/base/auth/permission_accordion.html` | HTML | 101 |
| `templates/base/auth/permission_assign.html` | HTML | 70 |
| `templates/base/auth/permission_lines.html` | HTML | 129 |
| `templates/base/auth/permission_table.html` | HTML | 162 |
| `templates/base/auth/roles_permissions.html` | HTML | 103 |
| `templates/base/auth/two_factor_auth.html` | HTML | 186 |
| `templates/base/auth/username_change.html` | HTML | 3 |
| `templates/base/auth/username_change_form.html` | HTML | 83 |
| `templates/base/company/company.html` | HTML | 24 |
| `templates/base/company/company_form.html` | HTML | 82 |
| `templates/base/company/condition.html` | HTML | 26 |
| `templates/base/company/condition_view.html` | HTML | 32 |
| `templates/base/company/payroll_settings.html` | HTML | 22 |
| `templates/base/department/department.html` | HTML | 43 |
| `templates/base/department/department_form.html` | HTML | 25 |
| `templates/base/department/department_view.html` | HTML | 42 |
| `templates/base/dynamic_pagination/pagination_settings.html` | HTML | 42 |
| `templates/base/employee_tag/employee_tag_form.html` | HTML | 54 |
| `templates/base/employee_tag/employee_tag_view.html` | HTML | 52 |
| `templates/base/employee_type/employee_type.html` | HTML | 49 |
| `templates/base/employee_type/employee_type_form.html` | HTML | 29 |
| `templates/base/employee_type/type_view.html` | HTML | 42 |
| `templates/base/encashment_general_settings.html` | HTML | 17 |
| `templates/base/ess_dashboard.html` | HTML | 1,336 |
| `templates/base/general_settings.html` | HTML | 11 |
| `templates/base/job_position/job_position.html` | HTML | 57 |
| `templates/base/job_position/job_position_form.html` | HTML | 41 |
| `templates/base/job_position/job_position_view.html` | HTML | 91 |
| `templates/base/job_role/job_role.html` | HTML | 57 |
| `templates/base/job_role/job_role_form.html` | HTML | 34 |
| `templates/base/job_role/job_role_view.html` | HTML | 89 |
| `templates/base/mail_server/form.html` | HTML | 25 |
| `templates/base/mail_server/form_email_test.html` | HTML | 121 |
| `templates/base/mail_server/mail_server.html` | HTML | 56 |
| `templates/base/mail_server/replace_mail.html` | HTML | 141 |
| `templates/base/mail_templates/leave_request_template.html` | HTML | 170 |
| `templates/base/mail_templates/password_reset_email.html` | HTML | 134 |
| `templates/base/navbar_components/breadcrumbs_view.html` | HTML | 27 |
| `templates/base/navbar_components/company_selection.html` | HTML | 28 |
| `templates/base/navbar_components/language_settings.html` | HTML | 36 |
| `templates/base/roster/my_roster.html` | HTML | 44 |
| `templates/base/roster/publish_form.html` | HTML | 85 |
| `templates/base/roster/roster_cell.html` | HTML | 20 |
| `templates/base/roster/roster_cell_form.html` | HTML | 128 |
| `templates/base/roster/roster_filter.html` | HTML | 103 |
| `templates/base/roster/roster_grid.html` | HTML | 412 |
| `templates/base/roster/roster_home.html` | HTML | 52 |
| `templates/base/roster/roster_import_form.html` | HTML | 117 |
| `templates/base/roster/roster_import_result.html` | HTML | 53 |
| `templates/base/rotating_shift/filters.html` | HTML | 99 |
| `templates/base/rotating_shift/htmx/add_more_shift_fields.html` | HTML | 29 |
| `templates/base/rotating_shift/htmx/group_by.html` | HTML | 492 |
| `templates/base/rotating_shift/htmx/rotating_shift_as_p.html` | HTML | 43 |
| `templates/base/rotating_shift/htmx/rotating_shift_assign_form.html` | HTML | 24 |
| `templates/base/rotating_shift/htmx/rotating_shift_assign_update_form.html` | HTML | 69 |
| `templates/base/rotating_shift/htmx/rotating_shift_form.html` | HTML | 24 |
| `templates/base/rotating_shift/individual_view.html` | HTML | 214 |
| `templates/base/rotating_shift/rotating_shift.html` | HTML | 47 |
| `templates/base/rotating_shift/rotating_shift_assign.html` | HTML | 28 |
| `templates/base/rotating_shift/rotating_shift_assign_empty.html` | HTML | 8 |
| `templates/base/rotating_shift/rotating_shift_assign_export.html` | HTML | 117 |
| `templates/base/rotating_shift/rotating_shift_assign_nav.html` | HTML | 470 |
| `templates/base/rotating_shift/rotating_shift_assign_view.html` | HTML | 396 |
| `templates/base/rotating_shift/rotating_shift_view.html` | HTML | 55 |
| `templates/base/rotating_work_type/filters.html` | HTML | 99 |
| `templates/base/rotating_work_type/htmx/add_more_work_type_fields.html` | HTML | 27 |
| `templates/base/rotating_work_type/htmx/group_by.html` | HTML | 427 |
| `templates/base/rotating_work_type/htmx/rotating_work_type_as_p.html` | HTML | 42 |
| `templates/base/rotating_work_type/htmx/rotating_work_type_assign_form.html` | HTML | 24 |
| `templates/base/rotating_work_type/htmx/rotating_work_type_assign_update_form.html` | HTML | 70 |
| `templates/base/rotating_work_type/htmx/rotating_work_type_form.html` | HTML | 24 |
| `templates/base/rotating_work_type/individual_view.html` | HTML | 216 |
| `templates/base/rotating_work_type/rotating_work_type.html` | HTML | 47 |
| `templates/base/rotating_work_type/rotating_work_type_assign.html` | HTML | 28 |
| `templates/base/rotating_work_type/rotating_work_type_assign_empty.html` | HTML | 8 |
| `templates/base/rotating_work_type/rotating_work_type_assign_export.html` | HTML | 116 |
| `templates/base/rotating_work_type/rotating_work_type_assign_nav.html` | HTML | 184 |
| `templates/base/rotating_work_type/rotating_work_type_assign_view.html` | HTML | 399 |
| `templates/base/rotating_work_type/rotating_work_type_view.html` | HTML | 47 |
| `templates/base/settings/audit_history.html` | HTML | 42 |
| `templates/base/settings/company_leaves.html` | HTML | 40 |
| `templates/base/settings/date_time_format_section.html` | HTML | 66 |
| `templates/base/settings/default_export_access.html` | HTML | 89 |
| `templates/base/settings/default_export_access_toggle.html` | HTML | 87 |
| `templates/base/settings/holidays.html` | HTML | 102 |
| `templates/base/settings/language_settings.html` | HTML | 168 |
| `templates/base/settings/mail_templates.html` | HTML | 77 |
| `templates/base/settings/system_preferences.html` | HTML | 107 |
| `templates/base/setup_checklist_banner.html` | HTML | 262 |
| `templates/base/setup_checklist_step.html` | HTML | 41 |
| `templates/base/shift/schedule.html` | HTML | 59 |
| `templates/base/shift/schedule_form.html` | HTML | 27 |
| `templates/base/shift/schedule_view.html` | HTML | 97 |
| `templates/base/shift/shift.html` | HTML | 26 |
| `templates/base/shift/shift_form.html` | HTML | 25 |
| `templates/base/shift/shift_view.html` | HTML | 147 |
| `templates/base/tags/employee_tags.html` | HTML | 49 |
| `templates/base/tags/helpdesk_tags.html` | HTML | 97 |
| `templates/base/tags/tags_form.html` | HTML | 25 |
| `templates/base/tags/tags_view.html` | HTML | 52 |
| `templates/base/ticket_type/ticket_type.html` | HTML | 93 |
| `templates/base/ticket_type/ticket_type_form.html` | HTML | 14 |
| `templates/base/ticket_type/ticket_type_view.html` | HTML | 46 |
| `templates/base/work_type/work_type.html` | HTML | 47 |
| `templates/base/work_type/work_type_form.html` | HTML | 25 |
| `templates/base/work_type/work_type_view.html` | HTML | 43 |
| `templates/cbv/announcement/announcement_form.html` | HTML | 15 |
| `templates/cbv/auth/user_assign_to_group.html` | HTML | 13 |
| `templates/cbv/company/company_form.html` | HTML | 114 |
| `templates/cbv/company_leaves/company_leave_actions.html` | HTML | 18 |
| `templates/cbv/company_leaves/company_leave_filter.html` | HTML | 22 |
| `templates/cbv/company_leaves/company_leave_home.html` | HTML | 47 |
| `templates/cbv/company_leaves/detail_view_actions.html` | HTML | 41 |
| `templates/cbv/company_leaves/on_week.html` | HTML | 11 |
| `templates/cbv/company_leaves/on_week_day.html` | HTML | 7 |
| `templates/cbv/dashboard/announcement_title.html` | HTML | 25 |
| `templates/cbv/dashboard/announcement_viewed_by.html` | HTML | 10 |
| `templates/cbv/dashboard/job_position_field.html` | HTML | 10 |
| `templates/cbv/dashboard/job_role_field.html` | HTML | 10 |
| `templates/cbv/dashboard/progress.html` | HTML | 16 |
| `templates/cbv/holidays/detail_view_actions.html` | HTML | 33 |
| `templates/cbv/holidays/holiday_filter.html` | HTML | 65 |
| `templates/cbv/holidays/holidays_actions.html` | HTML | 37 |
| `templates/cbv/holidays/holidays_export.html` | HTML | 84 |
| `templates/cbv/holidays/holidays_home.html` | HTML | 102 |
| `templates/cbv/mail_log_tab/iframe.html` | HTML | 56 |
| `templates/cbv/mail_template/form_inherit.html` | HTML | 59 |
| `templates/cbv/multiple_approval_condition/actions.html` | HTML | 20 |
| `templates/cbv/multiple_approval_condition/approval_managers.html` | HTML | 6 |
| `templates/cbv/multiple_approval_condition/detail_action.html` | HTML | 29 |
| `templates/cbv/multiple_approval_condition/form.html` | HTML | 46 |
| `templates/cbv/multiple_approval_condition/form_edit.html` | HTML | 103 |
| `templates/cbv/multiple_approval_condition/multiple_approval_condition.html` | HTML | 24 |
| `templates/cbv/rotating_shift/actions_rotaing_shift.html` | HTML | 37 |
| `templates/cbv/rotating_shift/extended_rotating_shift.html` | HTML | 8 |
| `templates/cbv/rotating_shift/rot_shift_form.html` | HTML | 67 |
| `templates/cbv/rotating_shift/rotating_column.html` | HTML | 19 |
| `templates/cbv/rotating_shift/rotating_shift.html` | HTML | 332 |
| `templates/cbv/rotating_shift/rotating_shift_detail_actions.html` | HTML | 47 |
| `templates/cbv/rotating_shift/rotating_shift_filter.html` | HTML | 139 |
| `templates/cbv/rotating_shift/rshift_export.html` | HTML | 32 |
| `templates/cbv/rotating_work_type/extended_rotating_work.html` | HTML | 8 |
| `templates/cbv/rotating_work_type/filter_work_rotate.html` | HTML | 138 |
| `templates/cbv/rotating_work_type/forms/inherit.html` | HTML | 56 |
| `templates/cbv/rotating_work_type/rotate_detail_view_actions.html` | HTML | 41 |
| `templates/cbv/rotating_work_type/rotating_action_export.html` | HTML | 32 |
| `templates/cbv/rotating_work_type/rotating_work_home.html` | HTML | 20 |
| `templates/cbv/rotating_work_type/rotation_col.html` | HTML | 20 |
| `templates/cbv/rotating_work_type/work_rotate_actions.html` | HTML | 38 |
| `templates/cbv/settings/employee_shift_schedule_action.html` | HTML | 19 |
| `templates/cbv/settings/employee_shift_schedule_detail_action.html` | HTML | 38 |
| `templates/cbv/settings/employee_shift_schedule_form.html` | HTML | 9 |
| `templates/cbv/settings/employee_shift_schedule_group_by.html` | HTML | 132 |
| `templates/cbv/settings/extended_mail_server.html` | HTML | 10 |
| `templates/cbv/settings/job_position_col_in_job_role.html` | HTML | 19 |
| `templates/cbv/settings/job_position_dpt.html` | HTML | 19 |
| `templates/cbv/settings/job_position_group_by.html` | HTML | 211 |
| `templates/cbv/settings/job_role.html` | HTML | 46 |
| `templates/cbv/settings/job_role_group_by.html` | HTML | 212 |
| `templates/cbv/settings/mail_server_action.html` | HTML | 56 |
| `templates/cbv/settings/position_in_job_position.html` | HTML | 51 |
| `templates/cbv/shift_request/actions_shift_requst.html` | HTML | 73 |
| `templates/cbv/shift_request/allocated_confirm_action.html` | HTML | 112 |
| `templates/cbv/shift_request/comment.html` | HTML | 13 |
| `templates/cbv/shift_request/confirm_allocated.html` | HTML | 35 |
| `templates/cbv/shift_request/confirmations.html` | HTML | 48 |
| `templates/cbv/shift_request/export_shift.html` | HTML | 35 |
| `templates/cbv/shift_request/extended_shift.html` | HTML | 8 |
| `templates/cbv/shift_request/filter.html` | HTML | 157 |
| `templates/cbv/shift_request/shift_detail_actions.html` | HTML | 44 |
| `templates/cbv/shift_request/shift_request.html` | HTML | 153 |
| `templates/cbv/shift_request/shift_request_form.html` | HTML | 24 |
| `templates/cbv/shift_request/user_availability.html` | HTML | 16 |
| `templates/cbv/work_shift_tab/extended_work-shift.html` | HTML | 20 |
| `templates/cbv/work_shift_tab/profile_tab_shell.html` | HTML | 17 |
| `templates/cbv/work_type_request/actions.html` | HTML | 43 |
| `templates/cbv/work_type_request/confirmation.html` | HTML | 40 |
| `templates/cbv/work_type_request/detail_view_actions.html` | HTML | 43 |
| `templates/cbv/work_type_request/filter.html` | HTML | 157 |
| `templates/cbv/work_type_request/form/form.html` | HTML | 27 |
| `templates/cbv/work_type_request/note.html` | HTML | 14 |
| `templates/cbv/work_type_request/work_export.html` | HTML | 32 |
| `templates/cbv/work_type_request/work_type_home.html` | HTML | 53 |
| `templates/common_form.html` | HTML | 54 |
| `templates/company_leave/company_leave.html` | HTML | 126 |
| `templates/company_leave/company_leave_creation_form.html` | HTML | 64 |
| `templates/company_leave/company_leave_update_form.html` | HTML | 63 |
| `templates/company_leave/company_leave_view.html` | HTML | 88 |
| `templates/holiday/holiday.html` | HTML | 207 |
| `templates/holiday/holiday_cbv_form.html` | HTML | 47 |
| `templates/holiday/holiday_detail_view.html` | HTML | 123 |
| `templates/holiday/holiday_export_filter_form.html` | HTML | 79 |
| `templates/holiday/holiday_filter.html` | HTML | 51 |
| `templates/holiday/holiday_form.html` | HTML | 72 |
| `templates/holiday/holiday_update_form.html` | HTML | 70 |
| `templates/holiday/holiday_view.html` | HTML | 238 |
| `templates/holiday/upcoming_holidays.html` | HTML | 23 |
| `templates/horilla_form.html` | HTML | 52 |
| `templates/mail/htmx/form.html` | HTML | 103 |
| `templates/multi_approval_condition/add_more_approval_manager.html` | HTML | 61 |
| `templates/multi_approval_condition/condition.html` | HTML | 37 |
| `templates/multi_approval_condition/condition_create_form.html` | HTML | 106 |
| `templates/multi_approval_condition/condition_edit_form.html` | HTML | 178 |
| `templates/multi_approval_condition/condition_table.html` | HTML | 103 |
| `templates/multi_approval_condition/condition_value_fields.html` | HTML | 33 |
| `templates/penalty/penalty_view.html` | HTML | 51 |
| `templates/request_and_approve/shift_request.html` | HTML | 100 |
| `templates/request_and_approve/work_type_request.html` | HTML | 99 |
| `templates/shift_request/allocation_request_update_form.html` | HTML | 4 |
| `templates/shift_request/htmx/allocation_details.html` | HTML | 202 |
| `templates/shift_request/htmx/comment_view.html` | HTML | 54 |
| `templates/shift_request/htmx/empty_request.html` | HTML | 8 |
| `templates/shift_request/htmx/group_by.html` | HTML | 1,138 |
| `templates/shift_request/htmx/requests.html` | HTML | 1,050 |
| `templates/shift_request/htmx/shift_allocation_form.html` | HTML | 26 |
| `templates/shift_request/htmx/shift_comment.html` | HTML | 104 |
| `templates/shift_request/htmx/shift_reallocate_employees.html` | HTML | 10 |
| `templates/shift_request/htmx/shift_request_create_form.html` | HTML | 52 |
| `templates/shift_request/htmx/shift_request_detail.html` | HTML | 173 |
| `templates/shift_request/request_form.html` | HTML | 11 |
| `templates/shift_request/request_update_form.html` | HTML | 25 |
| `templates/shift_request/shift_request.html` | HTML | 28 |
| `templates/shift_request/shift_request_export.html` | HTML | 129 |
| `templates/shift_request/shift_request_nav.html` | HTML | 347 |
| `templates/shift_request/shift_request_view.html` | HTML | 163 |
| `templates/work_type_request/htmx/empty_request.html` | HTML | 8 |
| `templates/work_type_request/htmx/group_by.html` | HTML | 623 |
| `templates/work_type_request/htmx/requests.html` | HTML | 549 |
| `templates/work_type_request/htmx/work_type_comment.html` | HTML | 111 |
| `templates/work_type_request/htmx/work_type_request_single_view.html` | HTML | 206 |
| `templates/work_type_request/request_form.html` | HTML | 43 |
| `templates/work_type_request/work_type_request.html` | HTML | 17 |
| `templates/work_type_request/work_type_request_export.html` | HTML | 129 |
| `templates/work_type_request/work_type_request_nav.html` | HTML | 355 |
| `templates/work_type_request/work_type_request_view.html` | HTML | 101 |
| `templatetags/__init__.py` | Python | 0 |
| `templatetags/basefilters.py` | Python | 630 |
| `templatetags/horillafilters.py` | Python | 535 |
| `tests/__init__.py` | Test | 1 |
| `tests/test_bulk_approve_reject.py` | Test | 223 |
| `tests/test_dashboard_roles.py` | Test | 205 |
| `tests/test_demo_data_payroll_features.py` | Test | 166 |
| `tests/test_demo_data_payroll_trend.py` | Test | 78 |
| `tests/test_demo_date_windows.py` | Test | 222 |
| `tests/test_email_log_privacy.py` | Test | 117 |
| `tests/test_export_access.py` | Test | 80 |
| `tests/test_export_permission_seeding.py` | Test | 63 |
| `tests/test_holiday_form.py` | Test | 210 |
| `tests/test_initialize_database_guard.py` | Test | 169 |
| `tests/test_login_bruteforce.py` | Test | 105 |
| `tests/test_mail_template_sanitizer.py` | Test | 169 |
| `tests/test_multi_tenancy.py` | Test | 58 |
| `tests/test_normalize_demo_payslips.py` | Test | 159 |
| `tests/test_observability.py` | Test | 326 |
| `tests/test_password_reset_domain.py` | Test | 135 |
| `tests/test_pdf_xss_guard.py` | Test | 65 |
| `tests/test_protected_media_hidden_paths.py` | Test | 43 |
| `tests/test_rotate_shift.py` | Test | 58 |
| `tests/test_sanitize_html_filter.py` | Test | 126 |
| `tests/test_scheduler_job_errors.py` | Test | 41 |
| `tests/test_scheduling.py` | Test | 270 |
| `tests/test_tenancy_check.py` | Test | 86 |
| `tests/test_testkit.py` | Test | 20 |
| `threading.py` | Python | 0 |
| `translator.py` | Python | 400 |
| `urls.py` | Python | 2,100 |
| `views.py` | Python | 8,914 |
| `widgets.py` | Python | 96 |
| `work_type_decorators.py` | Python | 45 |

</details>

### biometric

**52 files, 8,325 lines**.

<details>
<summary>Show all 52 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 7 |
| `admin.py` | Python | 16 |
| `anviz.py` | Python | 172 |
| `apps.py` | Python | 34 |
| `cbv/biometric.py` | Python | 353 |
| `context_processors.py` | Python | 41 |
| `cosec.py` | Python | 744 |
| `dahua.py` | Python | 521 |
| `etimeoffice.py` | Python | 122 |
| `filters.py` | Python | 38 |
| `forms.py` | Python | 398 |
| `migrations/0001_initial.py` | Migration | 277 |
| `migrations/0002_alter_biometricdevices_is_active.py` | Migration | 18 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 403 |
| `settings.py` | Python | 12 |
| `sidebar.py` | Python | 46 |
| `static/actions.js` | JS | 206 |
| `templates/biometric/actions_html.html` | HTML | 66 |
| `templates/biometric/add_biometric_user.html` | HTML | 37 |
| `templates/biometric/biometric_device_filter.html` | HTML | 35 |
| `templates/biometric/biometric_device_form.html` | HTML | 238 |
| `templates/biometric/edit_cosec_user.html` | HTML | 75 |
| `templates/biometric/empty_view_biometric.html` | HTML | 8 |
| `templates/biometric/list_employees_biometric.html` | HTML | 177 |
| `templates/biometric/list_employees_cosec_biometric.html` | HTML | 202 |
| `templates/biometric/live_capture.html` | HTML | 29 |
| `templates/biometric/nav_biometric_devices.html` | HTML | 80 |
| `templates/biometric/nav_employees_biometric.html` | HTML | 89 |
| `templates/biometric/nav_employees_cosec_biometric.html` | HTML | 88 |
| `templates/biometric/scheduler_device_form.html` | HTML | 39 |
| `templates/biometric/test_connection_script.html` | HTML | 13 |
| `templates/biometric/view_biometric_devices.html` | HTML | 144 |
| `templates/biometric/view_cosec_employees.html` | HTML | 23 |
| `templates/biometric/view_employees_biometric.html` | HTML | 22 |
| `templates/biometric_users/dahua/add_dahua_user.html` | HTML | 37 |
| `templates/biometric_users/dahua/list_dahua_employees.html` | HTML | 63 |
| `templates/biometric_users/dahua/map_dahua_users.html` | HTML | 36 |
| `templates/biometric_users/dahua/nav_dahua_employees.html` | HTML | 88 |
| `templates/biometric_users/dahua/view_dahua_employees.html` | HTML | 23 |
| `templates/biometric_users/etimeoffice/list_etimeoffice_employees.html` | HTML | 63 |
| `templates/biometric_users/etimeoffice/map_etimeoffice_users.html` | HTML | 36 |
| `templates/biometric_users/etimeoffice/nav_etimeoffice_employees.html` | HTML | 72 |
| `templates/biometric_users/etimeoffice/view_etimeoffice_employees.html` | HTML | 23 |
| `templates/cbv/biometric_card_action.html` | HTML | 34 |
| `templates/cbv/biometric_card_body.html` | HTML | 15 |
| `templates/cbv/biometric_filter.html` | HTML | 30 |
| `templates/cbv/biometric_form.html` | HTML | 101 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_device_smoke.py` | Test | 39 |
| `urls.py` | Python | 183 |
| `views.py` | Python | 2,709 |

</details>

### dynamic_fields

**23 files, 1,021 lines**.

<details>
<summary>Show all 23 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `admin.py` | Python | 9 |
| `apps.py` | Python | 66 |
| `df_not_allowed_models.py` | Python | 5 |
| `forms.py` | Python | 162 |
| `management/__init__.py` | Python | 0 |
| `management/commands/__init__.py` | Python | 0 |
| `management/commands/add_field.py` | Python | 68 |
| `management/commands/delete_field.py` | Python | 59 |
| `methods.py` | Python | 35 |
| `migrations/__init__.py` | Migration | 1 |
| `models.py` | Python | 180 |
| `signals.py` | Python | 18 |
| `templates/admin/includes/fieldset.html` | HTML | 38 |
| `templates/dynamic_fields/add_df.html` | HTML | 6 |
| `templates/dynamic_fields/common/form.html` | HTML | 99 |
| `templates/dynamic_fields/df.html` | HTML | 66 |
| `templates/dynamic_fields/form.html` | HTML | 80 |
| `templatetags/__init__.py` | Python | 0 |
| `templatetags/hdf_tags.py` | Python | 20 |
| `tests.py` | Test | 3 |
| `urls.py` | Python | 25 |
| `views.py` | Python | 81 |

</details>

### employee

**210 files, 40,744 lines**.

<details>
<summary>Show all 210 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 1 |
| `accessibility.py` | Python | 7 |
| `admin.py` | Python | 77 |
| `apps.py` | Python | 21 |
| `cbv/__init__.py` | Python | 0 |
| `cbv/accessibility.py` | Python | 347 |
| `cbv/action_type.py` | Python | 146 |
| `cbv/allocations.py` | Python | 1,490 |
| `cbv/disciplinary_actions.py` | Python | 296 |
| `cbv/document_request.py` | Python | 585 |
| `cbv/employee_profile.py` | Python | 454 |
| `cbv/employee_tags.py` | Python | 150 |
| `cbv/employees.py` | Python | 916 |
| `cbv/policy_cbv.py` | Python | 69 |
| `cbv/requests_nav.py` | Python | 49 |
| `dashboard.py` | Python | 401 |
| `employee_settings.py` | Python | 73 |
| `filters.py` | Python | 1,152 |
| `forms.py` | Python | 957 |
| `history.py` | Python | 371 |
| `management/commands/import_ldap_users.py` | Python | 78 |
| `methods/__init__.py` | Python | 0 |
| `methods/duration_methods.py` | Python | 25 |
| `methods/methods.py` | Python | 1,104 |
| `migrations/0001_initial.py` | Migration | 1,385 |
| `migrations/0002_alter_employeeworkinformation_location_and_more.py` | Migration | 23 |
| `migrations/0003_alter_actiontype_action_type_alter_employee_dob_and_more.py` | Migration | 59 |
| `migrations/0004_alter_employee_phone_and_more.py` | Migration | 29 |
| `migrations/0005_alter_employee_phone_and_more.py` | Migration | 29 |
| `migrations/0006_alter_bonuspoint_encashment_condition_and_more.py` | Migration | 23 |
| `migrations/0007_remove_policy_specific_employees_policy_department_and_more.py` | Migration | 57 |
| `migrations/0008_alter_employee_options.py` | Migration | 17 |
| `migrations/0009_alter_actiontype_is_active_and_more.py` | Migration | 73 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 1,556 |
| `not_in_out_dashboard.py` | Python | 340 |
| `policies.py` | Python | 614 |
| `requests.py` | Python | 74 |
| `scheduler.py` | Python | 101 |
| `sidebar.py` | Python | 174 |
| `static/cbv/employee_view/actions.js` | JS | 558 |
| `static/dashboard/employeeChart.js` | JS | 521 |
| `static/dashboard/getBirthday.js` | JS | 67 |
| `static/document/actions.js` | JS | 85 |
| `static/employee/actions.js` | JS | 440 |
| `static/employee/importExport.js` | JS | 110 |
| `static/employee/search.js` | JS | 84 |
| `templates/asset-tab.html` | HTML | 47 |
| `templates/cbv/allocations/allocations.html` | HTML | 58 |
| `templates/cbv/allocations/asset/actions.html` | HTML | 9 |
| `templates/cbv/allocations/asset/allocation_status.html` | HTML | 16 |
| `templates/cbv/allocations/asset/asset_list.html` | HTML | 29 |
| `templates/cbv/allocations/asset/assets.html` | HTML | 66 |
| `templates/cbv/allocations/asset/category_actions.html` | HTML | 9 |
| `templates/cbv/allocations/asset/return_form.html` | HTML | 89 |
| `templates/cbv/allocations/auth/group_form.html` | HTML | 12 |
| `templates/cbv/allocations/auth/group_view.html` | HTML | 50 |
| `templates/cbv/allocations/auth/groups.html` | HTML | 483 |
| `templates/cbv/allocations/employee/form_structure.html` | HTML | 53 |
| `templates/cbv/allocations/employee/forms.html` | HTML | 50 |
| `templates/cbv/allocations/leave/toggle_type.html` | HTML | 14 |
| `templates/cbv/allocations/leave/type_list.html` | HTML | 30 |
| `templates/cbv/allocations/leave/types.html` | HTML | 61 |
| `templates/cbv/allocations/payroll/allowance/actions.html` | HTML | 9 |
| `templates/cbv/allocations/payroll/allowance/allowance_list.html` | HTML | 28 |
| `templates/cbv/allocations/payroll/allowance/allowance_view.html` | HTML | 61 |
| `templates/cbv/allocations/payroll/deduction/actions.html` | HTML | 9 |
| `templates/cbv/allocations/payroll/deduction/deduction_list.html` | HTML | 28 |
| `templates/cbv/allocations/payroll/deduction/deduction_view.html` | HTML | 61 |
| `templates/cbv/allocations/summary.html` | HTML | 189 |
| `templates/cbv/dashboard/offline_action.html` | HTML | 14 |
| `templates/cbv/disciplinary_actions/action_date.html` | HTML | 10 |
| `templates/cbv/disciplinary_actions/action_taken.html` | HTML | 14 |
| `templates/cbv/disciplinary_actions/actions.html` | HTML | 28 |
| `templates/cbv/disciplinary_actions/attachments.html` | HTML | 13 |
| `templates/cbv/disciplinary_actions/detail_action.html` | HTML | 44 |
| `templates/cbv/disciplinary_actions/disciplinary_actions.html` | HTML | 252 |
| `templates/cbv/disciplinary_actions/employee_col.html` | HTML | 47 |
| `templates/cbv/disciplinary_actions/filters.html` | HTML | 144 |
| `templates/cbv/disciplinary_actions/forms/create_form.html` | HTML | 102 |
| `templates/cbv/document/notify_field.html` | HTML | 8 |
| `templates/cbv/documents/_document_colgroup.html` | HTML | 13 |
| `templates/cbv/documents/document_filter.html` | HTML | 151 |
| `templates/cbv/documents/document_list.html` | HTML | 293 |
| `templates/cbv/documents/document_row_actions.html` | HTML | 81 |
| `templates/cbv/documents/inherit_form.html` | HTML | 45 |
| `templates/cbv/documents/pipeline.html` | HTML | 402 |
| `templates/cbv/employees/history_col.html` | HTML | 19 |
| `templates/cbv/employees_view/bulk_update_page.html` | HTML | 124 |
| `templates/cbv/employees_view/card_body.html` | HTML | 29 |
| `templates/cbv/employees_view/employee_actions.html` | HTML | 128 |
| `templates/cbv/employees_view/employee_export.html` | HTML | 129 |
| `templates/cbv/employees_view/filter_employee.html` | HTML | 213 |
| `templates/cbv/employees_view/offline_online.html` | HTML | 8 |
| `templates/cbv/employees_view/view_employees.html` | HTML | 437 |
| `templates/cbv/profile/profile_view.html` | HTML | 75 |
| `templates/dashboard/birthdays_container.html` | HTML | 30 |
| `templates/dashboard/not_in_yet.html` | HTML | 62 |
| `templates/dashboard/not_out_yet.html` | HTML | 48 |
| `templates/disciplinary_actions/disciplinary_nav.html` | HTML | 235 |
| `templates/disciplinary_actions/disciplinary_records.html` | HTML | 217 |
| `templates/disciplinary_actions/form.html` | HTML | 63 |
| `templates/disciplinary_actions/update_form.html` | HTML | 58 |
| `templates/documents/document_nav.html` | HTML | 253 |
| `templates/documents/document_reject_reason.html` | HTML | 32 |
| `templates/documents/document_request_create_form.html` | HTML | 84 |
| `templates/documents/document_requests.html` | HTML | 43 |
| `templates/documents/requests.html` | HTML | 339 |
| `templates/employee/create_form/form_view.html` | HTML | 32 |
| `templates/employee/create_form/personal_info.html` | HTML | 117 |
| `templates/employee/create_form/personal_info_as_p.html` | HTML | 55 |
| `templates/employee/dashboard.html` | HTML | 1,507 |
| `templates/employee/dashboard/dashboard_employee.html` | HTML | 156 |
| `templates/employee/employee_import.html` | HTML | 164 |
| `templates/employee/employee_import_result.html` | HTML | 68 |
| `templates/employee/employees_select.html` | HTML | 3 |
| `templates/employee/export_data_employee.html` | HTML | 169 |
| `templates/employee/history_sidebar.html` | HTML | 12 |
| `templates/employee/mail_templates/invitation_email.html` | HTML | 14 |
| `templates/employee/profile/bank_info.html` | HTML | 92 |
| `templates/employee/profile/personal_info.html` | HTML | 237 |
| `templates/employee/profile/profile.html` | HTML | 86 |
| `templates/employee/profile/profile_modal.html` | HTML | 42 |
| `templates/employee/profile/profile_view.html` | HTML | 789 |
| `templates/employee/profile/work_info.html` | HTML | 106 |
| `templates/employee/reset_password_result.html` | HTML | 174 |
| `templates/employee/send_mail.html` | HTML | 282 |
| `templates/employee/update_form/bank_details.html` | HTML | 31 |
| `templates/employee/update_form/bank_info_as_p.html` | HTML | 57 |
| `templates/employee/update_form/edit_form_back_button.html` | HTML | 41 |
| `templates/employee/update_form/form_view.html` | HTML | 71 |
| `templates/employee/update_form/form_view_fragment.html` | HTML | 75 |
| `templates/employee/update_form/personal_info.html` | HTML | 122 |
| `templates/employee/update_form/work_details.html` | HTML | 239 |
| `templates/employee/view/individual.html` | HTML | 289 |
| `templates/employee_export_filter.html` | HTML | 137 |
| `templates/employee_filters.html` | HTML | 156 |
| `templates/employee_nav.html` | HTML | 449 |
| `templates/employee_personal_info/bulk_update.html` | HTML | 91 |
| `templates/employee_personal_info/employee_card.html` | HTML | 185 |
| `templates/employee_personal_info/employee_empty_view.html` | HTML | 14 |
| `templates/employee_personal_info/employee_list.html` | HTML | 507 |
| `templates/employee_personal_info/employee_personal_info.html` | HTML | 89 |
| `templates/employee_personal_info/employee_update_form.html` | HTML | 24 |
| `templates/employee_personal_info/employee_view.html` | HTML | 60 |
| `templates/employee_personal_info/employee_work_info.html` | HTML | 180 |
| `templates/employee_personal_info/first_last_badge.html` | HTML | 5 |
| `templates/employee_personal_info/group_by.html` | HTML | 400 |
| `templates/employee_personal_info/script.js` | JS | 3 |
| `templates/employee_personal_info/style.css` | CSS | 3 |
| `templates/leave-tab.html` | HTML | 279 |
| `templates/navbar_component/profile_section.html` | HTML | 33 |
| `templates/organisation_chart/chart.html` | HTML | 62 |
| `templates/organisation_chart/org_chart.html` | HTML | 58 |
| `templates/payroll-tab.html` | HTML | 79 |
| `templates/performance-tab.html` | HTML | 47 |
| `templates/policies/attachments.html` | HTML | 69 |
| `templates/policies/filter.html` | HTML | 0 |
| `templates/policies/form.html` | HTML | 38 |
| `templates/policies/nav.html` | HTML | 47 |
| `templates/policies/policy_form.html` | HTML | 45 |
| `templates/policies/records.html` | HTML | 175 |
| `templates/policies/view_policies.html` | HTML | 30 |
| `templates/policies/view_policy.html` | HTML | 79 |
| `templates/related_models.html` | HTML | 149 |
| `templates/settings/encashment_eligibility.html` | HTML | 115 |
| `templates/settings/encashment_settings.html` | HTML | 53 |
| `templates/settings/settings.html` | HTML | 40 |
| `templates/tabs/add_note.html` | HTML | 25 |
| `templates/tabs/allowance_deduction-tab.html` | HTML | 267 |
| `templates/tabs/asset-tab.html` | HTML | 112 |
| `templates/tabs/asset_request_tab.html` | HTML | 78 |
| `templates/tabs/attendance-tab.html` | HTML | 571 |
| `templates/tabs/bonus_points.html` | HTML | 98 |
| `templates/tabs/contract-tab.html` | HTML | 86 |
| `templates/tabs/document_tab.html` | HTML | 270 |
| `templates/tabs/forms/add_points.html` | HTML | 49 |
| `templates/tabs/forms/redeem_points_form.html` | HTML | 37 |
| `templates/tabs/group_permissions.html` | HTML | 85 |
| `templates/tabs/history.html` | HTML | 6 |
| `templates/tabs/htmx/document_create_form.html` | HTML | 37 |
| `templates/tabs/htmx/document_form.html` | HTML | 106 |
| `templates/tabs/htmx/reject_form.html` | HTML | 22 |
| `templates/tabs/htmx/view_file.html` | HTML | 151 |
| `templates/tabs/leave-tab.html` | HTML | 355 |
| `templates/tabs/mail_log.html` | HTML | 73 |
| `templates/tabs/main_asset_tab.html` | HTML | 3 |
| `templates/tabs/main_note_tab.html` | HTML | 3 |
| `templates/tabs/note_tab.html` | HTML | 223 |
| `templates/tabs/payroll-tab.html` | HTML | 100 |
| `templates/tabs/penalty_account.html` | HTML | 4 |
| `templates/tabs/performance-tab.html` | HTML | 53 |
| `templates/tabs/personal_tab.html` | HTML | 396 |
| `templates/tabs/profile-asset-tab.html` | HTML | 126 |
| `templates/tabs/profile-attendance-tab.html` | HTML | 94 |
| `templates/tabs/resignation.html` | HTML | 25 |
| `templates/tabs/scheduled_interview.html` | HTML | 189 |
| `templates/tabs/shift-tab.html` | HTML | 1,169 |
| `templates/tabs/update_note.html` | HTML | 29 |
| `templatetags/__init__ .py` | Python | 0 |
| `templatetags/employee_filter.py` | Python | 19 |
| `templatetags/migrations/__init__.py` | Migration | 0 |
| `tests/__init__.py` | Test | 1 |
| `tests/test_archive_revokes_login.py` | Test | 169 |
| `tests/test_employee_company.py` | Test | 75 |
| `tests/test_last_superuser_delete_guard.py` | Test | 263 |
| `threading.py` | Python | 36 |
| `urls.py` | Python | 970 |
| `views.py` | Python | 4,657 |
| `work_schedules.py` | Python | 45 |

</details>

### facedetection

**14 files, 431 lines**.

<details>
<summary>Show all 14 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `admin.py` | Python | 8 |
| `apps.py` | Python | 16 |
| `forms.py` | Python | 21 |
| `migrations/0001_initial.py` | Migration | 73 |
| `migrations/0002_alter_facedetection_start.py` | Migration | 18 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 57 |
| `serializers.py` | Python | 15 |
| `templates/face_config.html` | HTML | 4 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_config_smoke.py` | Test | 21 |
| `urls.py` | Python | 10 |
| `views.py` | Python | 188 |

</details>

### geofencing

**13 files, 440 lines**.

<details>
<summary>Show all 13 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `admin.py` | Python | 7 |
| `apps.py` | Python | 16 |
| `forms.py` | Python | 14 |
| `migrations/0001_initial.py` | Migration | 52 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 56 |
| `serializers.py` | Python | 29 |
| `templates/geo_config.html` | HTML | 39 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_geofencing_smoke.py` | Test | 25 |
| `urls.py` | Python | 11 |
| `views.py` | Python | 191 |

</details>

### helpdesk

**73 files, 16,510 lines**.

<details>
<summary>Show all 73 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `admin.py` | Python | 22 |
| `apps.py` | Python | 23 |
| `cbv/department_managers.py` | Python | 158 |
| `cbv/faq.py` | Python | 100 |
| `cbv/pipeline.py` | Python | 600 |
| `cbv/settings_tabs.py` | Python | 98 |
| `cbv/tags.py` | Python | 165 |
| `cbv/ticket_type.py` | Python | 303 |
| `dashboard.py` | Python | 468 |
| `decorators.py` | Python | 61 |
| `filter.py` | Python | 357 |
| `forms.py` | Python | 356 |
| `management/commands/__init__.py` | Python | 0 |
| `management/commands/create_faqs.py` | Python | 69 |
| `methods.py` | Python | 18 |
| `migrations/0001_initial.py` | Migration | 825 |
| `migrations/0002_alter_historicalticket_priority_and_more.py` | Migration | 23 |
| `migrations/0003_alter_tickettype_prefix_alter_tickettype_title.py` | Migration | 23 |
| `migrations/0004_alter_historicalticket_assigning_type_and_more.py` | Migration | 23 |
| `migrations/0005_alter_attachment_is_active_and_more.py` | Migration | 58 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 586 |
| `sidebar.py` | Python | 45 |
| `static/tickets/action.js` | JS | 449 |
| `static/tickets/tickets.js` | JS | 38 |
| `templates/cbv/helpdesk_settings/department_manager_tab.html` | HTML | 23 |
| `templates/cbv/helpdesk_settings/helpdesk_settings_main.html` | HTML | 10 |
| `templates/cbv/helpdesk_settings/tags_tab.html` | HTML | 23 |
| `templates/cbv/helpdesk_settings/ticket_type_tab.html` | HTML | 23 |
| `templates/cbv/pipeline/empty_list.html` | HTML | 8 |
| `templates/cbv/pipeline/kanban_action_method.html` | HTML | 91 |
| `templates/cbv/pipeline/pipeline_action_col.html` | HTML | 117 |
| `templates/cbv/pipeline/ticket_filter_form.html` | HTML | 114 |
| `templates/cbv/pipeline/ticket_section_view.html` | HTML | 48 |
| `templates/cbv/tickets/inherit_form.html` | HTML | 90 |
| `templates/department_managers/department_managers.html` | HTML | 75 |
| `templates/department_managers/department_managers_form.html` | HTML | 49 |
| `templates/department_managers/department_managers_view.html` | HTML | 59 |
| `templates/helpdesk/dashboard.html` | HTML | 799 |
| `templates/helpdesk/faq/faq_category_create.html` | HTML | 53 |
| `templates/helpdesk/faq/faq_category_list.html` | HTML | 91 |
| `templates/helpdesk/faq/faq_category_nav.html` | HTML | 117 |
| `templates/helpdesk/faq/faq_create.html` | HTML | 52 |
| `templates/helpdesk/faq/faq_list.html` | HTML | 92 |
| `templates/helpdesk/faq/faq_list_view.html` | HTML | 86 |
| `templates/helpdesk/faq/faq_nav.html` | HTML | 108 |
| `templates/helpdesk/faq/faq_view.html` | HTML | 76 |
| `templates/helpdesk/faq/load_faq.html` | HTML | 98 |
| `templates/helpdesk/mail_templates/ticket_mail.html` | HTML | 146 |
| `templates/helpdesk/ticket/forms/change_assinees.html` | HTML | 18 |
| `templates/helpdesk/ticket/forms/change_raised_on.html` | HTML | 86 |
| `templates/helpdesk/ticket/ticket_card.html` | HTML | 1,271 |
| `templates/helpdesk/ticket/ticket_claim_requests.html` | HTML | 123 |
| `templates/helpdesk/ticket/ticket_detail.html` | HTML | 944 |
| `templates/helpdesk/ticket/ticket_document.html` | HTML | 62 |
| `templates/helpdesk/ticket/ticket_filter.html` | HTML | 208 |
| `templates/helpdesk/ticket/ticket_form.html` | HTML | 267 |
| `templates/helpdesk/ticket/ticket_group.html` | HTML | 1,318 |
| `templates/helpdesk/ticket/ticket_individual_view.html` | HTML | 178 |
| `templates/helpdesk/ticket/ticket_list.html` | HTML | 1,231 |
| `templates/helpdesk/ticket/ticket_nav.html` | HTML | 150 |
| `templates/helpdesk/ticket/ticket_view.html` | HTML | 265 |
| `templatetags/__init__.py` | Python | 0 |
| `templatetags/helpdeskfilters.py` | Python | 27 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_claim_request_access.py` | Test | 124 |
| `tests/test_faq_view_xss.py` | Test | 30 |
| `tests/test_ticket_type_smoke.py` | Test | 16 |
| `tests/test_ticket_view_authz.py` | Test | 90 |
| `threading.py` | Python | 257 |
| `urls.py` | Python | 384 |
| `views.py` | Python | 2,145 |

</details>

### horilla_api

**117 files, 22,549 lines**.

<details>
<summary>Show all 117 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 4 |
| `admin.py` | Python | 3 |
| `api_decorators/base/decorators.py` | Python | 260 |
| `api_decorators/employee/decorators.py` | Python | 77 |
| `api_filters/asset/filters.py` | Python | 15 |
| `api_methods/base/announcements.py` | Python | 126 |
| `api_methods/base/capabilities.py` | Python | 93 |
| `api_methods/base/methods.py` | Python | 101 |
| `api_methods/base/pagination.py` | Python | 27 |
| `api_methods/employee/methods.py` | Python | 54 |
| `api_serializers/asset/serializers.py` | Python | 152 |
| `api_serializers/attendance/serializers.py` | Python | 233 |
| `api_serializers/auth/serializers.py` | Python | 50 |
| `api_serializers/base/serializers.py` | Python | 461 |
| `api_serializers/employee/serializers.py` | Python | 220 |
| `api_serializers/helpdesk/__init__.py` | Python | 3 |
| `api_serializers/helpdesk/serializers.py` | Python | 224 |
| `api_serializers/leave/serializers.py` | Python | 514 |
| `api_serializers/notifications/serializers.py` | Python | 9 |
| `api_serializers/offboarding/__init__.py` | Python | 3 |
| `api_serializers/offboarding/serializers.py` | Python | 357 |
| `api_serializers/onboarding/__init__.py` | Python | 3 |
| `api_serializers/onboarding/serializers.py` | Python | 266 |
| `api_serializers/payroll/serializers.py` | Python | 330 |
| `api_serializers/pms/__init__.py` | Python | 3 |
| `api_serializers/pms/serializers.py` | Python | 886 |
| `api_serializers/project/__init__.py` | Python | 3 |
| `api_serializers/project/serializers.py` | Python | 212 |
| `api_serializers/recruitment/__init__.py` | Python | 3 |
| `api_serializers/recruitment/serializers.py` | Python | 556 |
| `api_urls/__init__.py` | Python | 0 |
| `api_urls/asset/urls.py` | Python | 38 |
| `api_urls/attendance/urls.py` | Python | 61 |
| `api_urls/auth/urls.py` | Python | 15 |
| `api_urls/base/urls.py` | Python | 269 |
| `api_urls/employee/urls.py` | Python | 121 |
| `api_urls/helpdesk/__init__.py` | Python | 3 |
| `api_urls/helpdesk/urls.py` | Python | 45 |
| `api_urls/leave/urls.py` | Python | 56 |
| `api_urls/mobile/__init__.py` | Python | 0 |
| `api_urls/mobile/urls.py` | Python | 7 |
| `api_urls/notifications/urls.py` | Python | 14 |
| `api_urls/offboarding/__init__.py` | Python | 3 |
| `api_urls/offboarding/urls.py` | Python | 75 |
| `api_urls/onboarding/__init__.py` | Python | 3 |
| `api_urls/onboarding/urls.py` | Python | 59 |
| `api_urls/payroll/serializers.py` | Python | 325 |
| `api_urls/payroll/urls.py` | Python | 33 |
| `api_urls/pms/__init__.py` | Python | 3 |
| `api_urls/pms/urls.py` | Python | 132 |
| `api_urls/project/__init__.py` | Python | 3 |
| `api_urls/project/urls.py` | Python | 26 |
| `api_urls/recruitment/__init__.py` | Python | 3 |
| `api_urls/recruitment/urls.py` | Python | 108 |
| `api_views/asset/views.py` | Python | 396 |
| `api_views/attendance/permission_views.py` | Python | 14 |
| `api_views/attendance/views.py` | Python | 1,227 |
| `api_views/auth/views.py` | Python | 258 |
| `api_views/base/example_view.py` | Python | 29 |
| `api_views/base/views.py` | Python | 1,495 |
| `api_views/employee/views.py` | Python | 1,142 |
| `api_views/helpdesk/__init__.py` | Python | 3 |
| `api_views/helpdesk/views.py` | Python | 631 |
| `api_views/leave/views.py` | Python | 1,302 |
| `api_views/mobile/__init__.py` | Python | 0 |
| `api_views/mobile/views.py` | Python | 275 |
| `api_views/notifications/views.py` | Python | 63 |
| `api_views/offboarding/__init__.py` | Python | 3 |
| `api_views/offboarding/views.py` | Python | 667 |
| `api_views/onboarding/__init__.py` | Python | 3 |
| `api_views/onboarding/views.py` | Python | 498 |
| `api_views/payroll/views.py` | Python | 630 |
| `api_views/pms/__init__.py` | Python | 3 |
| `api_views/pms/views.py` | Python | 1,463 |
| `api_views/project/__init__.py` | Python | 3 |
| `api_views/project/views.py` | Python | 394 |
| `api_views/recruitment/__init__.py` | Python | 3 |
| `api_views/recruitment/views.py` | Python | 1,270 |
| `apps.py` | Python | 80 |
| `auth.py` | Python | 45 |
| `authentication.py` | Python | 118 |
| `decorators.py` | Python | 25 |
| `docs.py` | Python | 103 |
| `middleware.py` | Python | 23 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 3 |
| `schema.py` | Python | 245 |
| `swagger_settings.py` | Python | 29 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_api_login_lockout.py` | Test | 59 |
| `tests/test_api_versioning.py` | Test | 60 |
| `tests/test_api_write_target_scoping.py` | Test | 190 |
| `tests/test_attendance_mail_authz.py` | Test | 199 |
| `tests/test_capabilities.py` | Test | 110 |
| `tests/test_directory_access.py` | Test | 97 |
| `tests/test_document_api_authz.py` | Test | 158 |
| `tests/test_employee_self_edit.py` | Test | 156 |
| `tests/test_geofence_bypass_vector.py` | Test | 89 |
| `tests/test_geofence_enforcement.py` | Test | 89 |
| `tests/test_health_version.py` | Test | 42 |
| `tests/test_jwt_auth.py` | Test | 142 |
| `tests/test_leave_allocation_approval.py` | Test | 183 |
| `tests/test_leave_request_write_scoping.py` | Test | 229 |
| `tests/test_linkedin_account_scoping.py` | Test | 130 |
| `tests/test_manager_permission_403.py` | Test | 41 |
| `tests/test_manager_target_scoping.py` | Test | 139 |
| `tests/test_mobile_home.py` | Test | 234 |
| `tests/test_onboarding_portal_token.py` | Test | 57 |
| `tests/test_pagination_page_size.py` | Test | 62 |
| `tests/test_project_task_detail_scoping.py` | Test | 70 |
| `tests/test_reimbursement_approval.py` | Test | 167 |
| `tests/test_tenant_scoping.py` | Test | 212 |
| `tests/test_throttling.py` | Test | 145 |
| `tests/test_token_refresh.py` | Test | 151 |
| `tests/test_token_revocation.py` | Test | 84 |
| `tests/test_write_permissions.py` | Test | 106 |
| `urls.py` | Python | 55 |

</details>

### horilla_audit

**29 files, 2,545 lines**.

<details>
<summary>Show all 29 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 3 |
| `activity_feed.py` | Python | 272 |
| `admin.py` | Python | 11 |
| `apps.py` | Python | 39 |
| `cbv/audit.py` | Python | 154 |
| `context_processors.py` | Python | 33 |
| `filters.py` | Python | 23 |
| `forms.py` | Python | 192 |
| `methods.py` | Python | 243 |
| `migrations/0001_initial.py` | Migration | 141 |
| `migrations/0002_auditmodelconfig.py` | Migration | 35 |
| `migrations/0003_alter_historytrackingfields_options_and_more.py` | Migration | 24 |
| `migrations/0004_alter_accountblockunblock_is_active_and_more.py` | Migration | 28 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 417 |
| `registry.py` | Python | 152 |
| `settings.py` | Python | 11 |
| `templates/horilla_audit/audit_model_fields_form.html` | HTML | 56 |
| `templates/horilla_audit/audit_tracking_section.html` | HTML | 168 |
| `templates/horilla_audit/history_tracking.html` | HTML | 21 |
| `templates/horilla_audit/horilla_audit_log.html` | HTML | 114 |
| `templatetags/__init__.py` | Python | 0 |
| `templatetags/activity_history.py` | Python | 69 |
| `templatetags/audit_filters.py` | Python | 32 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_activity_feed_helpers.py` | Test | 30 |
| `tests/test_default_tracked_models.py` | Test | 106 |
| `urls.py` | Python | 28 |
| `views.py` | Python | 143 |

</details>

### horilla_auth

**14 files, 530 lines**.

<details>
<summary>Show all 14 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `admin.py` | Python | 6 |
| `apps.py` | Python | 8 |
| `management/commands/__init__.py` | Python | 0 |
| `management/commands/migrateusers.py` | Python | 100 |
| `methods.py` | Python | 38 |
| `migrations/0001_initial.py` | Migration | 188 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 48 |
| `signals.py` | Python | 0 |
| `tests/__init__.py` | Test | 1 |
| `tests/test_migrateusers.py` | Test | 54 |
| `tests/test_user_auth.py` | Test | 84 |
| `views.py` | Python | 3 |

</details>

### horilla_automations

**31 files, 3,072 lines**.

<details>
<summary>Show all 31 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `admin.py` | Python | 12 |
| `apps.py` | Python | 83 |
| `filters.py` | Python | 18 |
| `forms.py` | Python | 129 |
| `methods/__init__.py` | Python | 0 |
| `methods/methods.py` | Python | 293 |
| `methods/recursive_relation.py` | Python | 169 |
| `methods/serialize.py` | Python | 83 |
| `migrations/0001_initial.py` | Migration | 130 |
| `migrations/0002_alter_mailautomation_delivery_channel.py` | Migration | 26 |
| `migrations/0003_alter_mailautomation_mail_details_and_more.py` | Migration | 40 |
| `migrations/0004_alter_mailautomation_is_active.py` | Migration | 18 |
| `migrations/__init__.py` | Migration | 1 |
| `models.py` | Python | 165 |
| `signals.py` | Python | 616 |
| `static/automation/automation.js` | JS | 314 |
| `templates/horilla_automations/automation_form.html` | HTML | 44 |
| `templates/horilla_automations/conditions.html` | HTML | 1 |
| `templates/horilla_automations/load_automation.html` | HTML | 68 |
| `templates/horilla_automations/mail_automations_settings.html` | HTML | 115 |
| `templates/horilla_automations/mail_cc.html` | HTML | 10 |
| `templates/horilla_automations/mail_to.html` | HTML | 5 |
| `templates/horilla_automations/section_view.html` | HTML | 17 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_condition_helpers.py` | Test | 95 |
| `tests/test_mail_thread_race.py` | Test | 84 |
| `urls.py` | Python | 65 |
| `views/__init__.py` | Python | 0 |
| `views/cbvs.py` | Python | 348 |
| `views/views.py` | Python | 123 |

</details>

### horilla_backup

**20 files, 1,111 lines**.

<details>
<summary>Show all 20 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 1 |
| `admin.py` | Python | 8 |
| `apps.py` | Python | 16 |
| `forms.py` | Python | 200 |
| `gdrive.py` | Python | 28 |
| `migrations/0001_initial.py` | Migration | 79 |
| `migrations/0002_remove_googledrivebackup_service_account_file_and_more.py` | Migration | 42 |
| `migrations/0003_alter_googledrivebackup_gdrive_folder_id.py` | Migration | 18 |
| `migrations/__init__.py` | Migration | 22 |
| `models.py` | Python | 101 |
| `pgdump.py` | Python | 44 |
| `scheduler.py` | Python | 166 |
| `templates/backup/404.html` | HTML | 8 |
| `templates/backup/gdrive_setup_form.html` | HTML | 67 |
| `templates/backup/local_setup_form.html` | HTML | 68 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_zip_folder.py` | Test | 21 |
| `urls.py` | Python | 12 |
| `views.py` | Python | 197 |
| `zip.py` | Python | 13 |

</details>

### horilla_crumbs

**10 files, 1,005 lines**.

<details>
<summary>Show all 10 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `admin.py` | Python | 3 |
| `apps.py` | Python | 6 |
| `context_processors.py` | Python | 904 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 3 |
| `settings.py` | Python | 5 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_uuid_and_section.py` | Test | 28 |
| `views.py` | Python | 56 |

</details>

### horilla_dbtemplate

**16 files, 1,929 lines**.

<details>
<summary>Show all 16 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 12 |
| `admin.py` | Python | 828 |
| `apps.py` | Python | 19 |
| `conf.py` | Python | 34 |
| `loaders.py` | Python | 202 |
| `migrations/0001_initial.py` | Migration | 69 |
| `migrations/__init__.py` | Migration | 1 |
| `models.py` | Python | 341 |
| `signals.py` | Python | 51 |
| `templates/admin/horilla_dbtemplate/template/diff.html` | HTML | 63 |
| `templates/admin/horilla_dbtemplate/template/preview.html` | HTML | 43 |
| `templates/admin/horilla_dbtemplate/template/restore_version.html` | HTML | 42 |
| `utils/__init__.py` | Python | 1 |
| `utils/cache.py` | Python | 147 |
| `utils/site.py` | Python | 59 |
| `utils/template.py` | Python | 17 |

</details>

### horilla_documents

**12 files, 649 lines**.

<details>
<summary>Show all 12 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `admin.py` | Python | 7 |
| `apps.py` | Python | 8 |
| `forms.py` | Python | 129 |
| `migrations/0001_initial.py` | Migration | 219 |
| `migrations/0002_alter_document_reject_reason.py` | Migration | 18 |
| `migrations/0003_alter_document_is_active_and_more.py` | Migration | 23 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 222 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_document_title.py` | Test | 23 |
| `views.py` | Python | 0 |

</details>

### horilla_ldap

**15 files, 480 lines**.

<details>
<summary>Show all 15 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `admin.py` | Python | 6 |
| `apps.py` | Python | 33 |
| `forms.py` | Python | 24 |
| `management/commands/import_ldap_users.py` | Python | 157 |
| `management/commands/import_users_to_ldap.py` | Python | 107 |
| `migrations/0001_initial.py` | Migration | 43 |
| `migrations/0002_alter_ldapsettings_options.py` | Migration | 17 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 16 |
| `templates/ldap_settings.html` | HTML | 26 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_settings_smoke.py` | Test | 12 |
| `urls.py` | Python | 13 |
| `views.py` | Python | 26 |

</details>

### horilla_meet

**25 files, 2,475 lines**.

<details>
<summary>Show all 25 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `admin.py` | Python | 8 |
| `apps.py` | Python | 21 |
| `cbv.py` | Python | 564 |
| `filters.py` | Python | 31 |
| `form.py` | Python | 35 |
| `methods.py` | Python | 132 |
| `migrations/0001_initial.py` | Migration | 263 |
| `migrations/0002_alter_googlecredential_is_active_and_more.py` | Migration | 23 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 420 |
| `signals.py` | Python | 43 |
| `templates/gmeet/attendees_custom_column.html` | HTML | 37 |
| `templates/gmeet/filter.html` | HTML | 53 |
| `templates/gmeet/gmeet_detailed_view.html` | HTML | 126 |
| `templates/gmeet/gmeet_meetings_tab.html` | HTML | 154 |
| `templates/gmeet/gmeet_view.html` | HTML | 14 |
| `templates/gmeet/meet_form.html` | HTML | 39 |
| `templates/gmeet_credentials/gmeet_credential_section.html` | HTML | 32 |
| `templates/gmeet_credentials/gmeet_credential_section_view.html` | HTML | 5 |
| `templates/gmeet_credentials/gmeet_rules_tab.html` | HTML | 47 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_credentials_smoke.py` | Test | 21 |
| `urls.py` | Python | 127 |
| `views.py` | Python | 280 |

</details>

### horilla_theme

**446 files, 94,091 lines** (plus 5 minified files, 8,797 lines, not in the total).

<details>
<summary>Show all 451 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 3 |
| `admin.py` | Python | 11 |
| `apps.py` | Python | 39 |
| `filters.py` | Python | 5 |
| `forms.py` | Python | 49 |
| `management/commands/create_default_themes.py` | Python | 43 |
| `migrations/0001_initial.py` | Migration | 80 |
| `migrations/0002_alter_companytheme_is_active_and_more.py` | Migration | 23 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 641 |
| `overrides.py` | Python | 640 |
| `signals.py` | Python | 48 |
| `static/cdn/ajax/scripts/moment-with-locales.min.js` | Minified | 2 |
| `static/cdn/alpine/alpine.min.js` | Minified | 5 |
| `static/cdn/chartJs/scripts/chart.js` | JS | 14 |
| `static/cdn/font-awsome/css/all.min.css` | Minified | 8,788 |
| `static/cdn/googleapi/css/inter-font-style.css` | CSS | 126 |
| `static/cdn/googleapi/css/plus-jakarta-sans-font-style.css` | CSS | 36 |
| `static/cdn/hyperscript/script/_hyperscript.min.js` | Minified | 1 |
| `static/cdn/orgChart/orgchart.js` | JS | 1 |
| `static/cdn/select2/css/select2.min.css` | Minified | 1 |
| `static/cdn/tailwind/css/input.css` | CSS | 3 |
| `static/horilla_theme/assets/css/dark.css` | CSS | 567 |
| `static/horilla_theme/assets/css/global.css` | CSS | 1,651 |
| `static/horilla_theme/assets/css/tailwind.css` | CSS | 4,873 |
| `static/horilla_theme/assets/css/v1_styles.css` | CSS | 4,965 |
| `static/horilla_theme/assets/js/footerScripts.js` | JS | 864 |
| `static/horilla_theme/assets/js/global.js` | JS | 255 |
| `static/horilla_theme/assets/js/htmxSelect2.js` | JS | 4,444 |
| `static/horilla_theme/assets/js/tailwind.config.js` | JS | 92 |
| `static/horilla_theme/assets/js/tailwind.js` | JS | 83 |
| `static/horilla_theme/assets/js/tailwindcdn.js` | JS | 239 |
| `static/horilla_theme/assets/js/timeRunner.js` | JS | 30 |
| `templates/accessibility/accessibility.html` | HTML | 124 |
| `templates/accessibility/accessibility_form.html` | HTML | 44 |
| `templates/announcement/announcement_one.html` | HTML | 299 |
| `templates/announcement/comment_view.html` | HTML | 155 |
| `templates/announcement/expiry_day.html` | HTML | 38 |
| `templates/announcement/viewed_by.html` | HTML | 24 |
| `templates/asset/action_column.html` | HTML | 101 |
| `templates/asset/asset_list.html` | HTML | 166 |
| `templates/asset/asset_return_form.html` | HTML | 86 |
| `templates/attendance/components/in_out_component.html` | HTML | 195 |
| `templates/attendance/dashboard/dashboard.html` | HTML | 248 |
| `templates/attendance/late_come_early_out/tracking.html` | HTML | 26 |
| `templates/attendance/penalty/form.html` | HTML | 164 |
| `templates/attendance/settings/settings.html` | HTML | 27 |
| `templates/attendance/work_record/work_record_list.html` | HTML | 258 |
| `templates/attendance/work_record/work_record_view.html` | HTML | 177 |
| `templates/base/audit_tag/employee_account_block_unblock.html` | HTML | 128 |
| `templates/base/audit_tag/history_tracking_fields.html` | HTML | 4 |
| `templates/base/audit_tag/history_tracking_fields_content.html` | HTML | 181 |
| `templates/base/auth/group_accordion.html` | HTML | 368 |
| `templates/base/auth/group_assign.html` | HTML | 41 |
| `templates/base/auth/group_detail.html` | HTML | 124 |
| `templates/base/auth/group_lines.html` | HTML | 170 |
| `templates/base/auth/group_member_row.html` | HTML | 80 |
| `templates/base/auth/group_user_assign.html` | HTML | 95 |
| `templates/base/auth/password_change_form.html` | HTML | 205 |
| `templates/base/auth/permission.html` | HTML | 138 |
| `templates/base/auth/permission_accordion.html` | HTML | 146 |
| `templates/base/auth/permission_lines.html` | HTML | 270 |
| `templates/base/auth/permission_table.html` | HTML | 442 |
| `templates/base/auth/username_change_form.html` | HTML | 166 |
| `templates/base/dynamic_pagination/pagination_settings.html` | HTML | 38 |
| `templates/base/encashment_general_settings.html` | HTML | 36 |
| `templates/base/general_settings.html` | HTML | 9 |
| `templates/base/mail_templates/leave_request_template.html` | HTML | 150 |
| `templates/base/navbar_components/breadcrumbs_view.html` | HTML | 33 |
| `templates/base/navbar_components/company_selection.html` | HTML | 55 |
| `templates/base/navbar_components/language_settings.html` | HTML | 46 |
| `templates/base/navbar_components/profile_section.html` | HTML | 94 |
| `templates/base/settings/audit_history.html` | HTML | 42 |
| `templates/base/settings/date_time_format_section.html` | HTML | 93 |
| `templates/base/settings/system_preferences.html` | HTML | 112 |
| `templates/biometric/list_employees_biometric.html` | HTML | 330 |
| `templates/biometric/list_employees_cosec_biometric.html` | HTML | 229 |
| `templates/biometric/nav_employees_biometric.html` | HTML | 70 |
| `templates/biometric/nav_employees_cosec_biometric.html` | HTML | 70 |
| `templates/biometric_users/dahua/list_dahua_employees.html` | HTML | 147 |
| `templates/biometric_users/dahua/nav_dahua_employees.html` | HTML | 82 |
| `templates/biometric_users/etimeoffice/list_etimeoffice_employees.html` | HTML | 147 |
| `templates/biometric_users/etimeoffice/nav_etimeoffice_employees.html` | HTML | 64 |
| `templates/candidate/application_form.html` | HTML | 649 |
| `templates/candidate/candidate_create_form_as_p.html` | HTML | 164 |
| `templates/candidate/document.html` | HTML | 380 |
| `templates/candidate/history.html` | HTML | 2 |
| `templates/candidate/individual_view_note.html` | HTML | 262 |
| `templates/candidate/rating_tab.html` | HTML | 125 |
| `templates/category/asset_category.html` | HTML | 256 |
| `templates/category/asset_category_view.html` | HTML | 71 |
| `templates/cbv/360_feedback/anonymous_action.html` | HTML | 43 |
| `templates/cbv/360_feedback/anonymous_detail_action.html` | HTML | 46 |
| `templates/cbv/allocations/allocations.html` | HTML | 83 |
| `templates/cbv/allocations/asset/allocation_status.html` | HTML | 13 |
| `templates/cbv/allocations/asset/asset_list.html` | HTML | 31 |
| `templates/cbv/allocations/asset/assets.html` | HTML | 53 |
| `templates/cbv/allocations/asset/return_form.html` | HTML | 70 |
| `templates/cbv/allocations/employee/forms.html` | HTML | 99 |
| `templates/cbv/allocations/leave/type_list.html` | HTML | 38 |
| `templates/cbv/allocations/leave/types.html` | HTML | 53 |
| `templates/cbv/allocations/payroll/allowance/allowance_list.html` | HTML | 35 |
| `templates/cbv/allocations/payroll/allowance/allowance_view.html` | HTML | 53 |
| `templates/cbv/allocations/payroll/deduction/deduction_list.html` | HTML | 35 |
| `templates/cbv/allocations/payroll/deduction/deduction_view.html` | HTML | 53 |
| `templates/cbv/allocations/summary.html` | HTML | 121 |
| `templates/cbv/allowance_deduction/allowance/detail_view_actions.html` | HTML | 50 |
| `templates/cbv/allowance_deduction/allowance_action.html` | HTML | 62 |
| `templates/cbv/allowance_deduction/allowance_deduction.html` | HTML | 33 |
| `templates/cbv/allowance_deduction/deductions/deductions_actions.html` | HTML | 56 |
| `templates/cbv/allowance_deduction/deductions/detail_view_actions.html` | HTML | 52 |
| `templates/cbv/asset/detail_action.html` | HTML | 54 |
| `templates/cbv/asset_batch_no/detail_actions.html` | HTML | 35 |
| `templates/cbv/assigned_leave/assigned_leave_detail_actions.html` | HTML | 42 |
| `templates/cbv/attendance_activity/detail_delete_action.html` | HTML | 30 |
| `templates/cbv/attendance_request/attendance_request_option.html` | HTML | 25 |
| `templates/cbv/attendance_request/attendance_request_tab.html` | HTML | 496 |
| `templates/cbv/attendance_request/detail_actions.html` | HTML | 28 |
| `templates/cbv/attendance_request/request_actions.html` | HTML | 81 |
| `templates/cbv/attendances/detail_view_activity_col.html` | HTML | 27 |
| `templates/cbv/attendances/ot_actions.html` | HTML | 117 |
| `templates/cbv/attendances/ot_confirmation.html` | HTML | 97 |
| `templates/cbv/attendances/ot_tab_action.html` | HTML | 140 |
| `templates/cbv/attendances/validate_actions.html` | HTML | 76 |
| `templates/cbv/attendances/validate_button.html` | HTML | 87 |
| `templates/cbv/attendances/validate_tab_action.html` | HTML | 110 |
| `templates/cbv/attendances/validated_tab_action.html` | HTML | 60 |
| `templates/cbv/candidates/actions.html` | HTML | 30 |
| `templates/cbv/candidates/profile_about_tab.html` | HTML | 88 |
| `templates/cbv/candidates/profile_interview_tab.html` | HTML | 249 |
| `templates/cbv/candidates/profile_survey_tab.html` | HTML | 142 |
| `templates/cbv/candidates/rating.html` | HTML | 27 |
| `templates/cbv/company_leaves/detail_view_actions.html` | HTML | 37 |
| `templates/cbv/compensatory_leave/compensatory_detail_actions.html` | HTML | 106 |
| `templates/cbv/compensatory_leave/compensatory_tab_actions.html` | HTML | 5 |
| `templates/cbv/contracts/cal_leave_amount.html` | HTML | 19 |
| `templates/cbv/contracts/detail_action.html` | HTML | 41 |
| `templates/cbv/contracts/document.html` | HTML | 11 |
| `templates/cbv/contracts/note.html` | HTML | 9 |
| `templates/cbv/disciplinary_actions/actions.html` | HTML | 28 |
| `templates/cbv/disciplinary_actions/detail_action.html` | HTML | 54 |
| `templates/cbv/documents/document_list.html` | HTML | 482 |
| `templates/cbv/employee_individual/leave_tab.html` | HTML | 84 |
| `templates/cbv/employees_view/employee_actions.html` | HTML | 103 |
| `templates/cbv/exit_process/detail_action_col.html` | HTML | 109 |
| `templates/cbv/exit_process/detail_view_tasks.html` | HTML | 71 |
| `templates/cbv/exit_process/pipeline_action_col.html` | HTML | 97 |
| `templates/cbv/exit_process/stage_order.html` | HTML | 73 |
| `templates/cbv/exit_process/stages.html` | HTML | 72 |
| `templates/cbv/federal_tax/tax_bracket.html` | HTML | 32 |
| `templates/cbv/holidays/detail_view_actions.html` | HTML | 38 |
| `templates/cbv/holidays/holidays_actions.html` | HTML | 37 |
| `templates/cbv/hour_account/hour_actions.html` | HTML | 68 |
| `templates/cbv/hour_account/hour_detail_action.html` | HTML | 99 |
| `templates/cbv/hour_account/hour_options.html` | HTML | 36 |
| `templates/cbv/interview/detail_view_actions.html` | HTML | 137 |
| `templates/cbv/interview/status_custom_col.html` | HTML | 31 |
| `templates/cbv/key_results/actions.html` | HTML | 61 |
| `templates/cbv/key_results/detail_view_actions.html` | HTML | 63 |
| `templates/cbv/late_come_and_early_out/detail_action.html` | HTML | 52 |
| `templates/cbv/leave_allocation_request/allocation_tab_actions.html` | HTML | 5 |
| `templates/cbv/leave_allocation_request/confirmations.html` | HTML | 28 |
| `templates/cbv/leave_allocation_request/detail_action.html` | HTML | 56 |
| `templates/cbv/leave_allocation_request/leave_detail_action.html` | HTML | 97 |
| `templates/cbv/leave_requests/confirmation.html` | HTML | 138 |
| `templates/cbv/leave_requests/leave_request_detail_actions.html` | HTML | 186 |
| `templates/cbv/leave_requests/leave_request_tab_actions.html` | HTML | 5 |
| `templates/cbv/leave_requests/multiple_approval_action.html` | HTML | 29 |
| `templates/cbv/leave_types/detail_actions.html` | HTML | 47 |
| `templates/cbv/leave_types/leave_type_list_actions.html` | HTML | 67 |
| `templates/cbv/loan/loan_detail_view.html` | HTML | 190 |
| `templates/cbv/loan/loan_installment_table.html` | HTML | 106 |
| `templates/cbv/mail_log_tab/iframe.html` | HTML | 90 |
| `templates/cbv/meetings/actions.html` | HTML | 228 |
| `templates/cbv/meetings/detail_action.html` | HTML | 253 |
| `templates/cbv/multiple_approval_condition/detail_action.html` | HTML | 41 |
| `templates/cbv/my_leave_request/detail_leave_actions.html` | HTML | 71 |
| `templates/cbv/my_leave_request/leave_actions.html` | HTML | 43 |
| `templates/cbv/objectives/actions.html` | HTML | 77 |
| `templates/cbv/objectives/compact_empty.html` | HTML | 4 |
| `templates/cbv/objectives/self_objective_action.html` | HTML | 70 |
| `templates/cbv/objectives/tab_empty.html` | HTML | 5 |
| `templates/cbv/onboarding_candidates/actions.html` | HTML | 149 |
| `templates/cbv/period/detail_view_actions.html` | HTML | 31 |
| `templates/cbv/pipeline/candidate_column.html` | HTML | 79 |
| `templates/cbv/pipeline/interview_template.html` | HTML | 93 |
| `templates/cbv/pipeline/onboarding/stage_order.html` | HTML | 71 |
| `templates/cbv/pipeline/onboarding/stages.html` | HTML | 84 |
| `templates/cbv/pipeline/onboarding/tasks.html` | HTML | 33 |
| `templates/cbv/pipeline/pipeline_action_col.html` | HTML | 117 |
| `templates/cbv/pipeline/rating.html` | HTML | 61 |
| `templates/cbv/pipeline/stage_order.html` | HTML | 71 |
| `templates/cbv/pipeline/stages.html` | HTML | 151 |
| `templates/cbv/projects/actions.html` | HTML | 78 |
| `templates/cbv/projects/compact_empty.html` | HTML | 4 |
| `templates/cbv/projects/project_details.html` | HTML | 115 |
| `templates/cbv/projects/project_tab.html` | HTML | 73 |
| `templates/cbv/recruitment/actions.html` | HTML | 66 |
| `templates/cbv/recruitment/detail_action.html` | HTML | 127 |
| `templates/cbv/recruitment_survey/detail_actions.html` | HTML | 34 |
| `templates/cbv/recruitment_survey/option_col.html` | HTML | 12 |
| `templates/cbv/recruitment_survey/survey_form.html` | HTML | 116 |
| `templates/cbv/reimbursements/actions.html` | HTML | 88 |
| `templates/cbv/reimbursements/detail_actions.html` | HTML | 95 |
| `templates/cbv/reimbursements/forms.html` | HTML | 86 |
| `templates/cbv/request_and_allocation/asset_request_action.html` | HTML | 114 |
| `templates/cbv/request_and_allocation/asset_request_detail_action.html` | HTML | 141 |
| `templates/cbv/resignation/actions.html` | HTML | 63 |
| `templates/cbv/resignation/options.html` | HTML | 64 |
| `templates/cbv/restricted_days/detail_action.html` | HTML | 40 |
| `templates/cbv/rotating_shift/actions_rotaing_shift.html` | HTML | 37 |
| `templates/cbv/rotating_shift/rotating_shift_detail_actions.html` | HTML | 61 |
| `templates/cbv/rotating_work_type/rotate_detail_view_actions.html` | HTML | 62 |
| `templates/cbv/rotating_work_type/work_rotate_actions.html` | HTML | 38 |
| `templates/cbv/salary_structure/detail_view_actions.html` | HTML | 51 |
| `templates/cbv/settings/employee_shift_schedule_detail_action.html` | HTML | 31 |
| `templates/cbv/settings/mail_server_action.html` | HTML | 56 |
| `templates/cbv/shift_request/actions_shift_requst.html` | HTML | 73 |
| `templates/cbv/shift_request/allocated_confirm_action.html` | HTML | 100 |
| `templates/cbv/shift_request/allocated_detail_confirm_action.html` | HTML | 118 |
| `templates/cbv/shift_request/confirmations.html` | HTML | 71 |
| `templates/cbv/shift_request/detail_confirmations.html` | HTML | 71 |
| `templates/cbv/shift_request/shift_detail_actions.html` | HTML | 49 |
| `templates/cbv/shift_request/shift_detail_confirm_action.html` | HTML | 100 |
| `templates/cbv/stages/actions.html` | HTML | 44 |
| `templates/cbv/stages/detail_action.html` | HTML | 50 |
| `templates/cbv/tasks/task_actions.html` | HTML | 57 |
| `templates/cbv/tasks/task_detail_actions.html` | HTML | 76 |
| `templates/cbv/timesheet/actions.html` | HTML | 64 |
| `templates/cbv/timesheet/detail_actions.html` | HTML | 46 |
| `templates/cbv/work_shift_tab/extended_work-shift.html` | HTML | 23 |
| `templates/cbv/work_type_request/actions.html` | HTML | 43 |
| `templates/cbv/work_type_request/confirmation.html` | HTML | 76 |
| `templates/cbv/work_type_request/detail_confirmation.html` | HTML | 135 |
| `templates/cbv/work_type_request/detail_view_actions.html` | HTML | 59 |
| `templates/common_form.html` | HTML | 63 |
| `templates/compensatory_settings.html` | HTML | 53 |
| `templates/contract_form.html` | HTML | 101 |
| `templates/dashboard/dashboard.html` | HTML | 329 |
| `templates/dashboard/pms_dashboard.html` | HTML | 205 |
| `templates/dashboard/project_dashboard.html` | HTML | 131 |
| `templates/dashboard_chart_form.html` | HTML | 120 |
| `templates/documents/document_requests.html` | HTML | 36 |
| `templates/documents/requests.html` | HTML | 227 |
| `templates/employee/create_form/form_view.html` | HTML | 78 |
| `templates/employee/create_form/personal_info.html` | HTML | 241 |
| `templates/employee/create_form/personal_info_as_p.html` | HTML | 75 |
| `templates/employee/export_data_employee.html` | HTML | 166 |
| `templates/employee/update_form/bank_details.html` | HTML | 110 |
| `templates/employee/update_form/bank_info_as_p.html` | HTML | 62 |
| `templates/employee/update_form/form_view.html` | HTML | 150 |
| `templates/employee/update_form/form_view_fragment.html` | HTML | 176 |
| `templates/employee/update_form/personal_info.html` | HTML | 243 |
| `templates/employee/update_form/work_details.html` | HTML | 302 |
| `templates/employee/view/individual.html` | HTML | 285 |
| `templates/employee_settings/employee_settings.html` | HTML | 183 |
| `templates/employee_settings/employee_settings_employee_tags_tab.html` | HTML | 23 |
| `templates/employee_settings/employee_settings_employee_type_tab.html` | HTML | 27 |
| `templates/employee_settings/employee_settings_rotating_shift_tab.html` | HTML | 23 |
| `templates/employee_settings/employee_settings_rotating_work_type_tab.html` | HTML | 23 |
| `templates/employee_settings/employee_settings_shift_schedule_tab.html` | HTML | 39 |
| `templates/employee_settings/employee_settings_shift_tab.html` | HTML | 27 |
| `templates/employee_settings/employee_settings_work_type_tab.html` | HTML | 27 |
| `templates/feedback/answer/feedback_answer.html` | HTML | 246 |
| `templates/feedback/answer/feedback_answer_view.html` | HTML | 84 |
| `templates/feedback/feedback_detailed_view.html` | HTML | 677 |
| `templates/feedback/feedback_detailed_view_answer.html` | HTML | 51 |
| `templates/feedback/feedback_overview.html` | HTML | 154 |
| `templates/feedback/question/question_all.html` | HTML | 158 |
| `templates/feedback/question_template/question_template_detailed_view.html` | HTML | 147 |
| `templates/feedback/question_template/question_template_related_view.html` | HTML | 63 |
| `templates/floating_button.html` | HTML | 297 |
| `templates/forgot_password.html` | HTML | 158 |
| `templates/generic/_group_row_colgroup.html` | HTML | 21 |
| `templates/generic/_group_row_table.html` | HTML | 144 |
| `templates/generic/_group_row_thead.html` | HTML | 150 |
| `templates/generic/_saved_filter_chip.html` | HTML | 54 |
| `templates/generic/activity_history_feed.html` | HTML | 346 |
| `templates/generic/as_list.html` | HTML | 178 |
| `templates/generic/delete_confirmation.html` | HTML | 341 |
| `templates/generic/export_fields_modal.html` | HTML | 170 |
| `templates/generic/filter_count_and_custom_builder.html` | HTML | 367 |
| `templates/generic/filter_result.html` | HTML | 102 |
| `templates/generic/form.html` | HTML | 161 |
| `templates/generic/group_by_table.html` | HTML | 319 |
| `templates/generic/horilla_card.html` | HTML | 376 |
| `templates/generic/horilla_detailed_view.html` | HTML | 171 |
| `templates/generic/horilla_history_view.html` | HTML | 23 |
| `templates/generic/horilla_list_table.html` | HTML | 530 |
| `templates/generic/horilla_nav.html` | HTML | 569 |
| `templates/generic/horilla_profile_view.html` | HTML | 474 |
| `templates/generic/horilla_tabs.html` | HTML | 312 |
| `templates/generic/import_block.html` | HTML | 163 |
| `templates/generic/inline_nav.html` | HTML | 520 |
| `templates/generic/modern_filter_panel.html` | HTML | 644 |
| `templates/generic/nested_group_by_node.html` | HTML | 232 |
| `templates/generic/nested_group_by_table.html` | HTML | 718 |
| `templates/generic/pipeline/pipeline.html` | HTML | 51 |
| `templates/generic/quick_actions.html` | HTML | 243 |
| `templates/helpdesk/faq/faq_category_list.html` | HTML | 95 |
| `templates/helpdesk/faq/faq_category_nav.html` | HTML | 111 |
| `templates/helpdesk/faq/faq_list.html` | HTML | 226 |
| `templates/helpdesk/faq/faq_list_view.html` | HTML | 86 |
| `templates/helpdesk/faq/faq_nav.html` | HTML | 93 |
| `templates/helpdesk/faq/faq_view.html` | HTML | 81 |
| `templates/helpdesk/faq/load_faq.html` | HTML | 115 |
| `templates/helpdesk/ticket/forms/change_assinees.html` | HTML | 31 |
| `templates/helpdesk/ticket/forms/change_raised_on.html` | HTML | 104 |
| `templates/helpdesk/ticket/ticket_claim_requests.html` | HTML | 113 |
| `templates/helpdesk/ticket/ticket_detail.html` | HTML | 844 |
| `templates/horilla_automations/detail_actions.html` | HTML | 25 |
| `templates/horilla_automations/load_automation.html` | HTML | 72 |
| `templates/horilla_theme/components/dashboard.html` | HTML | 311 |
| `templates/horilla_theme/components/dashboard_tiles.html` | HTML | 725 |
| `templates/horilla_theme/components/footer_scripts.html` | HTML | 65 |
| `templates/horilla_theme/components/header.html` | HTML | 188 |
| `templates/horilla_theme/components/header_scripts.html` | HTML | 394 |
| `templates/horilla_theme/components/reorder_dashboard_charts.html` | HTML | 86 |
| `templates/horilla_theme/components/sidebar.html` | HTML | 1,364 |
| `templates/horilla_theme/components/sidebar/top_menu.html` | HTML | 25 |
| `templates/horilla_widgets/horilla_multiselect_widget.html` | HTML | 218 |
| `templates/horilla_widgets/multiselect_components/filter_tags.html` | HTML | 36 |
| `templates/horilla_widgets/multiselect_components/nav.html` | HTML | 212 |
| `templates/horilla_widgets/multiselect_components/pagination.html` | HTML | 0 |
| `templates/horilla_widgets/multiselect_components/table.html` | HTML | 318 |
| `templates/index.html` | HTML | 416 |
| `templates/initialize_database/horilla_company.html` | HTML | 92 |
| `templates/initialize_database/horilla_department_form.html` | HTML | 69 |
| `templates/initialize_database/horilla_job_position_form.html` | HTML | 68 |
| `templates/initialize_database/horilla_user.html` | HTML | 183 |
| `templates/initialize_database/horilla_user_signup.html` | HTML | 233 |
| `templates/leave/compensatory_leave/compensatory_leave_type.html` | HTML | 75 |
| `templates/leave/leave_allocation_request/leave_allocation_comment.html` | HTML | 220 |
| `templates/leave/leave_request/dashboard_leave_requests.html` | HTML | 298 |
| `templates/leave/leave_request/leave_comment.html` | HTML | 217 |
| `templates/leave/leave_request/penalty/form.html` | HTML | 164 |
| `templates/leave/leave_type/leave_type_creation.html` | HTML | 690 |
| `templates/leave/leave_type/leave_type_update.html` | HTML | 623 |
| `templates/leave/user_leave/user_leave.html` | HTML | 51 |
| `templates/login.html` | HTML | 258 |
| `templates/meetings/meeting_answer.html` | HTML | 261 |
| `templates/notification/all_notifications.html` | HTML | 43 |
| `templates/notification/notification.html` | HTML | 144 |
| `templates/notification/notification_items.html` | HTML | 49 |
| `templates/offboarding/dashboard/dashboard.html` | HTML | 227 |
| `templates/offboarding/note/view_notes.html` | HTML | 242 |
| `templates/offboarding/settings/settings.html` | HTML | 34 |
| `templates/okr/emp_objective/emp_objective_list.html` | HTML | 300 |
| `templates/okr/objective_detailed_view_activity.html` | HTML | 337 |
| `templates/okr/okr_detailed_view.html` | HTML | 316 |
| `templates/onboarding/employee_bank_details.html` | HTML | 218 |
| `templates/onboarding/employee_creation.html` | HTML | 265 |
| `templates/onboarding/empty_task.html` | HTML | 15 |
| `templates/onboarding/mail_templates/default.html` | HTML | 141 |
| `templates/onboarding/profile_view.html` | HTML | 131 |
| `templates/onboarding/user_creation.html` | HTML | 181 |
| `templates/onboarding/welcome_aboard.html` | HTML | 80 |
| `templates/organisation_chart/chart.html` | HTML | 821 |
| `templates/organisation_chart/org_chart.html` | HTML | 71 |
| `templates/payroll/dashboard/contribution.html` | HTML | 45 |
| `templates/payroll/loan/installments.html` | HTML | 217 |
| `templates/payroll/payslip/_earning_popover.html` | HTML | 39 |
| `templates/payroll/payslip/_loss_of_pay_popover.html` | HTML | 98 |
| `templates/payroll/payslip/_loss_of_pay_row.html` | HTML | 18 |
| `templates/payroll/payslip/individual_payslip.html` | HTML | 183 |
| `templates/payroll/payslip/individual_payslip_summery.html` | HTML | 653 |
| `templates/payroll/reimbursement/reimbursement_comment.html` | HTML | 236 |
| `templates/payroll/settings/payroll_settings.html` | HTML | 46 |
| `templates/payroll/settings/settings.html` | HTML | 18 |
| `templates/payroll/tax/filing_status_list.html` | HTML | 85 |
| `templates/pipeline/matching_resumes.html` | HTML | 114 |
| `templates/pipeline/pipeline_components/view_note.html` | HTML | 291 |
| `templates/policies/policies_discipline.html` | HTML | 144 |
| `templates/policies/policies_discipline_action_type_tab.html` | HTML | 23 |
| `templates/policies/policies_discipline_disciplinary_tab.html` | HTML | 177 |
| `templates/policies/policies_discipline_faq_list.html` | HTML | 21 |
| `templates/policies/policies_discipline_faq_tab.html` | HTML | 58 |
| `templates/policies/policies_discipline_policies_tab.html` | HTML | 21 |
| `templates/policies/records.html` | HTML | 95 |
| `templates/policies/view_policies.html` | HTML | 14 |
| `templates/recruitment/open_recruitments.html` | HTML | 434 |
| `templates/recruitment/recruitment_details.html` | HTML | 125 |
| `templates/recruitment/settings/settings.html` | HTML | 88 |
| `templates/related_models.html` | HTML | 133 |
| `templates/report/_catalog_chip_list.html` | HTML | 20 |
| `templates/report/asset_report.html` | HTML | 1,621 |
| `templates/report/attendance_report.html` | HTML | 1,726 |
| `templates/report/employee_report.html` | HTML | 1,639 |
| `templates/report/explorer_picker.html` | HTML | 90 |
| `templates/report/leave_report.html` | HTML | 1,771 |
| `templates/report/payroll_report.html` | HTML | 1,787 |
| `templates/report/pms_report.html` | HTML | 1,812 |
| `templates/report/recruitment_report.html` | HTML | 1,874 |
| `templates/report/standard_catalog.html` | HTML | 1,656 |
| `templates/report/standard_report.html` | HTML | 1,641 |
| `templates/report/standard_report_inspector.html` | HTML | 56 |
| `templates/report/standard_report_pdf.html` | HTML | 418 |
| `templates/report/standard_report_print_modal.html` | HTML | 159 |
| `templates/requests/attendance/individual_view.html` | HTML | 122 |
| `templates/requests/attendance/request_new_form.html` | HTML | 94 |
| `templates/requests/requests.html` | HTML | 161 |
| `templates/requests/requests_document_tab.html` | HTML | 31 |
| `templates/requests/requests_shift_inbox_tab.html` | HTML | 27 |
| `templates/requests/requests_shift_request_tab.html` | HTML | 35 |
| `templates/requests/requests_work_type_tab.html` | HTML | 27 |
| `templates/settings.html` | HTML | 514 |
| `templates/settings/encashment_eligibility.html` | HTML | 104 |
| `templates/settings/encashment_settings.html` | HTML | 43 |
| `templates/settings/linkedin/linkedin_setting_section.html` | HTML | 70 |
| `templates/settings/settings.html` | HTML | 38 |
| `templates/shift_request/htmx/shift_comment.html` | HTML | 244 |
| `templates/skill_zone/_talent_pool_colgroup.html` | HTML | 15 |
| `templates/skill_zone/skill_zone_list.html` | HTML | 385 |
| `templates/skill_zone/skill_zone_nav.html` | HTML | 204 |
| `templates/skill_zone/skill_zone_view.html` | HTML | 12 |
| `templates/survey/question_card.html` | HTML | 173 |
| `templates/survey/question_tab_root.html` | HTML | 8 |
| `templates/survey/survey_card.html` | HTML | 216 |
| `templates/survey/template_accordion.html` | HTML | 347 |
| `templates/survey/template_tab_root.html` | HTML | 8 |
| `templates/survey/view_question_templates.html` | HTML | 89 |
| `templates/survey_preview_form.html` | HTML | 191 |
| `templates/tabs/_pay_bubble.html` | HTML | 40 |
| `templates/tabs/bonus_points.html` | HTML | 64 |
| `templates/tabs/bonus_points_history.html` | HTML | 124 |
| `templates/tabs/document_tab.html` | HTML | 295 |
| `templates/tabs/group_permissions.html` | HTML | 136 |
| `templates/tabs/history.html` | HTML | 337 |
| `templates/tabs/note_tab.html` | HTML | 295 |
| `templates/tabs/personal_tab.html` | HTML | 521 |
| `templates/tabs/scheduled_interview.html` | HTML | 209 |
| `templates/tabs/shift-tab.html` | HTML | 1,169 |
| `templates/task/new/_task_colgroup.html` | HTML | 16 |
| `templates/task/new/forms/quick_create_task_form.html` | HTML | 65 |
| `templates/task/new/overall.html` | HTML | 175 |
| `templates/task/new/task_kanban_view.html` | HTML | 603 |
| `templates/task/new/task_list_view.html` | HTML | 376 |
| `templates/task/new/task_navbar.html` | HTML | 132 |
| `templates/theme/theme_cards.html` | HTML | 94 |
| `templates/theme/theme_view.html` | HTML | 25 |
| `templates/time_sheet/chart.html` | HTML | 163 |
| `templates/work_schedules/work_schedules.html` | HTML | 131 |
| `templates/work_schedules/work_schedules_rotating_shift_tab.html` | HTML | 235 |
| `templates/work_schedules/work_schedules_rotating_work_type_tab.html` | HTML | 24 |
| `templates/work_schedules/work_schedules_shift_roster_tab.html` | HTML | 15 |
| `templates/work_type_request/htmx/work_type_comment.html` | HTML | 243 |
| `templatetags/__init__.py` | Python | 0 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_theme_create.py` | Test | 23 |
| `urls.py` | Python | 16 |
| `views.py` | Python | 222 |

</details>

### horilla_tour

**101 files, 11,855 lines**.

<details>
<summary>Show all 101 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `admin.py` | Python | 33 |
| `apps.py` | Python | 22 |
| `context_processors.py` | Python | 40 |
| `filters.py` | Python | 24 |
| `forms.py` | Python | 56 |
| `migrations/0001_initial.py` | Migration | 89 |
| `migrations/0002_seed_default_tours.py` | Migration | 148 |
| `migrations/0003_seed_dashboard_highlights_tour.py` | Migration | 97 |
| `migrations/0004_seed_module_tours.py` | Migration | 782 |
| `migrations/0005_fix_sidebar_step_selectors.py` | Migration | 56 |
| `migrations/0006_seed_settings_tours.py` | Migration | 474 |
| `migrations/0007_settings_tours_interactive.py` | Migration | 404 |
| `migrations/0008_fix_create_button_selector.py` | Migration | 59 |
| `migrations/0009_seed_recruitment_dashboard_tour.py` | Migration | 127 |
| `migrations/0010_seed_recruitment_survey_tour.py` | Migration | 135 |
| `migrations/0011_seed_candidate_tour.py` | Migration | 111 |
| `migrations/0012_seed_scheduled_interviews_tour.py` | Migration | 103 |
| `migrations/0013_seed_recruitment_view_tour.py` | Migration | 103 |
| `migrations/0014_seed_stage_tour.py` | Migration | 103 |
| `migrations/0015_fix_stage_create_button_selector.py` | Migration | 46 |
| `migrations/0016_seed_skill_zone_tour.py` | Migration | 111 |
| `migrations/0017_seed_onboarding_pipeline_tour.py` | Migration | 119 |
| `migrations/0018_seed_onboarding_hired_candidates_tour.py` | Migration | 111 |
| `migrations/0019_reseed_onboarding_hired_candidates_tour.py` | Migration | 117 |
| `migrations/0020_seed_employee_profile_tour.py` | Migration | 111 |
| `migrations/0021_seed_document_requests_tour.py` | Migration | 127 |
| `migrations/0022_seed_shift_requests_tour.py` | Migration | 135 |
| `migrations/0023_seed_work_type_requests_tour.py` | Migration | 119 |
| `migrations/0024_seed_rotating_shift_assign_tour.py` | Migration | 119 |
| `migrations/0025_fix_rotating_shift_assign_page_match.py` | Migration | 26 |
| `migrations/0026_seed_rotating_work_type_assign_tour.py` | Migration | 119 |
| `migrations/0027_seed_roster_planner_tour.py` | Migration | 111 |
| `migrations/0028_seed_disciplinary_actions_tour.py` | Migration | 111 |
| `migrations/0029_seed_policies_tour.py` | Migration | 103 |
| `migrations/0030_seed_attendances_tour.py` | Migration | 127 |
| `migrations/0031_seed_attendance_requests_tour.py` | Migration | 111 |
| `migrations/0032_seed_hour_account_tour.py` | Migration | 103 |
| `migrations/0033_seed_attendance_activity_tour.py` | Migration | 95 |
| `migrations/0034_seed_late_come_early_out_tour.py` | Migration | 111 |
| `migrations/0035_seed_my_attendances_tour.py` | Migration | 103 |
| `migrations/0036_seed_my_leave_request_tour.py` | Migration | 119 |
| `migrations/0037_seed_leave_requests_tour.py` | Migration | 135 |
| `migrations/0038_seed_leave_type_tour.py` | Migration | 111 |
| `migrations/0039_seed_assigned_leaves_tour.py` | Migration | 111 |
| `migrations/0040_seed_leave_allocation_requests_tour.py` | Migration | 111 |
| `migrations/0041_seed_compensatory_leave_tour.py` | Migration | 111 |
| `migrations/0042_seed_contracts_tour.py` | Migration | 111 |
| `migrations/0043_seed_allowances_tour.py` | Migration | 111 |
| `migrations/0044_seed_deductions_tour.py` | Migration | 111 |
| `migrations/0045_seed_payslip_tour.py` | Migration | 119 |
| `migrations/0046_seed_loan_advance_salary_tour.py` | Migration | 119 |
| `migrations/0047_seed_reimbursements_tour.py` | Migration | 119 |
| `migrations/0048_fix_filter_search_selectors.py` | Migration | 101 |
| `migrations/0049_fix_actions_button_selectors.py` | Migration | 73 |
| `migrations/0052_seed_objectives_tour.py` | Migration | 135 |
| `migrations/0053_seed_objective_templates_tour.py` | Migration | 111 |
| `migrations/0054_seed_feedbacks_tour.py` | Migration | 143 |
| `migrations/0055_seed_meetings_tour.py` | Migration | 111 |
| `migrations/0056_seed_key_results_tour.py` | Migration | 111 |
| `migrations/0057_seed_employee_bonus_point_tour.py` | Migration | 95 |
| `migrations/0058_seed_period_tour.py` | Migration | 95 |
| `migrations/0059_seed_question_template_tour.py` | Migration | 103 |
| `migrations/0060_seed_exit_process_tour.py` | Migration | 135 |
| `migrations/0061_seed_asset_category_tour.py` | Migration | 111 |
| `migrations/0062_seed_asset_batch_number_tour.py` | Migration | 95 |
| `migrations/0063_seed_asset_section_tour.py` | Migration | 119 |
| `migrations/0064_seed_asset_history_tour.py` | Migration | 95 |
| `migrations/0065_seed_faq_categories_tour.py` | Migration | 103 |
| `migrations/0066_seed_tickets_tour.py` | Migration | 127 |
| `migrations/0067_seed_projects_tour.py` | Migration | 119 |
| `migrations/0068_seed_tasks_tour.py` | Migration | 119 |
| `migrations/0069_seed_timesheets_tour.py` | Migration | 119 |
| `migrations/0070_seed_employee_report_tour.py` | Migration | 95 |
| `migrations/0071_seed_recruitment_report_tour.py` | Migration | 103 |
| `migrations/0072_seed_attendance_report_tour.py` | Migration | 95 |
| `migrations/0073_seed_leave_report_tour.py` | Migration | 103 |
| `migrations/0074_seed_payroll_report_tour.py` | Migration | 103 |
| `migrations/0075_seed_asset_report_tour.py` | Migration | 95 |
| `migrations/0076_seed_pms_report_tour.py` | Migration | 103 |
| `migrations/0077_seed_multiple_approval_condition_tour.py` | Migration | 95 |
| `migrations/0078_seed_multiple_approval_condition_form_tour.py` | Migration | 119 |
| `migrations/0079_seed_mail_templates_tour.py` | Migration | 103 |
| `migrations/0080_seed_automations_tour.py` | Migration | 103 |
| `migrations/0081_seed_holidays_tour.py` | Migration | 111 |
| `migrations/0082_seed_company_leaves_tour.py` | Migration | 103 |
| `migrations/0083_seed_restricted_days_tour.py` | Migration | 111 |
| `migrations/0084_seed_individual_payslip_tour.py` | Migration | 103 |
| `migrations/0085_seed_filing_status_tour.py` | Migration | 103 |
| `migrations/0086_seed_objective_detailed_view_tour.py` | Migration | 127 |
| `migrations/0087_seed_faq_view_tour.py` | Migration | 95 |
| `migrations/0088_alter_tour_is_active_alter_tourprogress_is_active_and_more.py` | Migration | 28 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 258 |
| `sidebar.py` | Python | 58 |
| `templates/horilla_tour/step_form.html` | HTML | 32 |
| `templates/horilla_tour/steps_panel.html` | HTML | 71 |
| `templates/horilla_tour/tour_settings.html` | HTML | 27 |
| `tests.py` | Test | 290 |
| `urls.py` | Python | 25 |
| `views.py` | Python | 387 |

</details>

### horilla_views

**68 files, 14,292 lines**.

<details>
<summary>Show all 68 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `admin.py` | Python | 5 |
| `apps.py` | Python | 6 |
| `cbv_methods.py` | Python | 1,212 |
| `forms.py` | Python | 344 |
| `generic/__init__.py` | Python | 0 |
| `generic/cbv/__init__.py` | Python | 0 |
| `generic/cbv/history.py` | Python | 181 |
| `generic/cbv/kanban.py` | Python | 293 |
| `generic/cbv/pipeline.py` | Python | 78 |
| `generic/cbv/views.py` | Python | 2,743 |
| `history_methods.py` | Python | 280 |
| `migrations/0001_initial.py` | Migration | 291 |
| `migrations/0002_columnorder.py` | Migration | 33 |
| `migrations/0003_alter_activegroup_is_active_and_more.py` | Migration | 43 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 108 |
| `related_link_registry.py` | Python | 82 |
| `static/js/genericKanban.js` | JS | 408 |
| `templates/cbv/filter_form.html` | HTML | 0 |
| `templates/cbv/import_response.html` | HTML | 74 |
| `templates/generic/activity_history_feed.html` | HTML | 328 |
| `templates/generic/as_list.html` | HTML | 186 |
| `templates/generic/bulk_form.html` | HTML | 5 |
| `templates/generic/components.html` | HTML | 207 |
| `templates/generic/delete_confirmation.html` | HTML | 299 |
| `templates/generic/export_fields_modal.html` | HTML | 136 |
| `templates/generic/export_pdf.html` | HTML | 158 |
| `templates/generic/filter_result.html` | HTML | 10 |
| `templates/generic/filter_tags.html` | HTML | 171 |
| `templates/generic/form.html` | HTML | 134 |
| `templates/generic/group_by.html` | HTML | 423 |
| `templates/generic/group_by_table.html` | HTML | 476 |
| `templates/generic/history_col.html` | HTML | 19 |
| `templates/generic/horilla_card.html` | HTML | 227 |
| `templates/generic/horilla_detailed_view.html` | HTML | 108 |
| `templates/generic/horilla_form.html` | HTML | 77 |
| `templates/generic/horilla_history_view.html` | HTML | 28 |
| `templates/generic/horilla_kanban_view.html` | HTML | 236 |
| `templates/generic/horilla_list.html` | HTML | 360 |
| `templates/generic/horilla_list_table.html` | HTML | 414 |
| `templates/generic/horilla_nav.html` | HTML | 318 |
| `templates/generic/horilla_profile_view.html` | HTML | 431 |
| `templates/generic/horilla_section.html` | HTML | 43 |
| `templates/generic/horilla_tab_content_shell.html` | HTML | 44 |
| `templates/generic/horilla_tabs.html` | HTML | 127 |
| `templates/generic/import_block.html` | HTML | 112 |
| `templates/generic/index.html` | HTML | 37 |
| `templates/generic/messages.html` | HTML | 7 |
| `templates/generic/penalty_badge.html` | HTML | 25 |
| `templates/generic/pipeline/kanban.html` | HTML | 581 |
| `templates/generic/pipeline/kanban_items.html` | HTML | 119 |
| `templates/generic/pipeline/pipeline.html` | HTML | 63 |
| `templates/generic/profile_view.html` | HTML | 6 |
| `templates/generic/quick_actions.html` | HTML | 190 |
| `templates/generic/reload_select_field.html` | HTML | 32 |
| `templates/generic/saved_filter_form.html` | HTML | 27 |
| `templatetags/__init__.py` | Python | 0 |
| `templatetags/generic_template_filters.py` | Python | 411 |
| `templatetags/migrations/__init__.py` | Migration | 0 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_cbv_helpers.py` | Test | 20 |
| `tests/test_existing_ids.py` | Test | 92 |
| `tests/test_export_column_paths.py` | Test | 55 |
| `tests/test_history_and_payroll_authz.py` | Test | 159 |
| `tests/test_template_filters.py` | Test | 18 |
| `urls.py` | Python | 74 |
| `views.py` | Python | 1,118 |

</details>

### horilla_widgets

**27 files, 1,327 lines**.

<details>
<summary>Show all 27 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `admin.py` | Python | 3 |
| `apps.py` | Python | 11 |
| `forms.py` | Python | 46 |
| `generic_ajax.py` | Python | 89 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 3 |
| `templates/horilla_widgets/attr.html` | HTML | 1 |
| `templates/horilla_widgets/horilla_attr.html` | HTML | 1 |
| `templates/horilla_widgets/horilla_clearable_file_input.html` | HTML | 33 |
| `templates/horilla_widgets/horilla_multiselect_widget.html` | HTML | 216 |
| `templates/horilla_widgets/horilla_select_option.html` | HTML | 1 |
| `templates/horilla_widgets/multiselect_components/filter_tags.html` | HTML | 36 |
| `templates/horilla_widgets/multiselect_components/nav.html` | HTML | 216 |
| `templates/horilla_widgets/multiselect_components/pagination.html` | HTML | 9 |
| `templates/horilla_widgets/multiselect_components/search.html` | HTML | 59 |
| `templates/horilla_widgets/multiselect_components/table.html` | HTML | 275 |
| `templates/horilla_widgets/multiselect_components/user_tags.html` | HTML | 30 |
| `templates/horilla_widgets/select_option.html` | HTML | 1 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_pretty_file_name.py` | Test | 16 |
| `urls.py` | Python | 16 |
| `views.py` | Python | 74 |
| `widgets/__init__.py` | Python | 0 |
| `widgets/file_widgets.py` | Python | 42 |
| `widgets/horilla_multi_select_field.py` | Python | 12 |
| `widgets/select_widgets.py` | Python | 137 |

</details>

### leave

**237 files, 45,383 lines**.

<details>
<summary>Show all 237 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 1 |
| `admin.py` | Python | 42 |
| `apps.py` | Python | 19 |
| `cbv/__init__.py` | Python | 0 |
| `cbv/accessibility.py` | Python | 32 |
| `cbv/assigned_leave.py` | Python | 374 |
| `cbv/compensatory_leave_request.py` | Python | 421 |
| `cbv/dashboard.py` | Python | 187 |
| `cbv/leave_allocation_request.py` | Python | 537 |
| `cbv/leave_requests.py` | Python | 737 |
| `cbv/leave_tab.py` | Python | 100 |
| `cbv/leave_types.py` | Python | 456 |
| `cbv/my_leave_request.py` | Python | 698 |
| `cbv/restricted_days.py` | Python | 181 |
| `cbv/settings_tabs.py` | Python | 89 |
| `dashboard.py` | Python | 615 |
| `decorators.py` | Python | 121 |
| `filters.py` | Python | 966 |
| `forms.py` | Python | 1,353 |
| `methods.py` | Python | 305 |
| `migrations/0001_initial.py` | Migration | 2,002 |
| `migrations/0002_alter_leaverequest_options.py` | Migration | 21 |
| `migrations/0003_leavetype_payment_percentage_leavetype_payment_type_and_more.py` | Migration | 48 |
| `migrations/0004_employeepastleaverestrict_company_id.py` | Migration | 20 |
| `migrations/0005_remove_holiday_company_id_remove_holiday_created_by_and_more.py` | Migration | 41 |
| `migrations/0006_remove_leavetype_color.py` | Migration | 17 |
| `migrations/0007_alter_historicalleaverequest_reject_reason_and_more.py` | Migration | 23 |
| `migrations/0008_leaverequest_leaverequest_dates_idx_and_more.py` | Migration | 24 |
| `migrations/0009_alter_availableleave_is_active_and_more.py` | Migration | 103 |
| `migrations/0010_historicalleaverequest_cancellation_requested_and_more.py` | Migration | 33 |
| `migrations/__init__.py` | Migration | 7 |
| `models.py` | Python | 2,765 |
| `scheduler.py` | Python | 63 |
| `services.py` | Python | 135 |
| `sidebar.py` | Python | 180 |
| `signals.py` | Python | 146 |
| `static/cbv/assigned_leave/assigned_leave.js` | JS | 90 |
| `static/cbv/holidays/holiday_action.js` | JS | 122 |
| `static/cbv/leave_allocation_request/bulk_actions.js` | JS | 88 |
| `static/cbv/leave_requests/leave_requests.js` | JS | 286 |
| `static/cbv/my_leave_request/my_leave_request.js` | JS | 111 |
| `static/dashboard/dashboard.js` | JS | 564 |
| `static/dashboard/leaveChart.js` | JS | 172 |
| `static/dashboard/onLeave.js` | JS | 34 |
| `static/leave_assign/action.js` | JS | 238 |
| `static/leave_request/action.js` | JS | 536 |
| `static/restrict_days/action.js` | JS | 241 |
| `templates/cbv/assigned_leave/assigned_filter.html` | HTML | 134 |
| `templates/cbv/assigned_leave/assigned_leave_actions.html` | HTML | 31 |
| `templates/cbv/assigned_leave/assigned_leave_detail_actions.html` | HTML | 30 |
| `templates/cbv/assigned_leave/assigned_leave_export.html` | HTML | 148 |
| `templates/cbv/assigned_leave/assigned_leave_home.html` | HTML | 111 |
| `templates/cbv/assigned_leave/leave_ledger_sidebar.html` | HTML | 94 |
| `templates/cbv/assigned_leave/nav_fixed_filter.html` | HTML | 17 |
| `templates/cbv/compensatory_leave/compensatory_actions.html` | HTML | 32 |
| `templates/cbv/compensatory_leave/compensatory_comment.html` | HTML | 5 |
| `templates/cbv/compensatory_leave/compensatory_confirmation.html` | HTML | 37 |
| `templates/cbv/compensatory_leave/compensatory_detail_actions.html` | HTML | 106 |
| `templates/cbv/compensatory_leave/compensatory_home.html` | HTML | 63 |
| `templates/cbv/compensatory_leave/compensatory_leave_filter.html` | HTML | 56 |
| `templates/cbv/compensatory_leave/compensatory_tab_actions.html` | HTML | 5 |
| `templates/cbv/compensatory_leave/custom_date.html` | HTML | 6 |
| `templates/cbv/compensatory_leave/detail_reject_reason.html` | HTML | 16 |
| `templates/cbv/compensatory_leave/inherit_class.html` | HTML | 3 |
| `templates/cbv/compensatory_leave/my_compensatory_detail_action.html` | HTML | 57 |
| `templates/cbv/employee_individual/leave_tab.html` | HTML | 409 |
| `templates/cbv/leave_allocation_request/action_column.html` | HTML | 49 |
| `templates/cbv/leave_allocation_request/allocation_tab_actions.html` | HTML | 5 |
| `templates/cbv/leave_allocation_request/attachment.html` | HTML | 7 |
| `templates/cbv/leave_allocation_request/comment.html` | HTML | 19 |
| `templates/cbv/leave_allocation_request/confirmations.html` | HTML | 28 |
| `templates/cbv/leave_allocation_request/detail_action.html` | HTML | 47 |
| `templates/cbv/leave_allocation_request/filter.html` | HTML | 121 |
| `templates/cbv/leave_allocation_request/history.html` | HTML | 21 |
| `templates/cbv/leave_allocation_request/leave_allocation_request.html` | HTML | 87 |
| `templates/cbv/leave_allocation_request/leave_detail_action.html` | HTML | 32 |
| `templates/cbv/leave_allocation_request/reject.html` | HTML | 11 |
| `templates/cbv/leave_requests/actions_col.html` | HTML | 60 |
| `templates/cbv/leave_requests/clashed_due_to.html` | HTML | 9 |
| `templates/cbv/leave_requests/comment_action.html` | HTML | 7 |
| `templates/cbv/leave_requests/confirmation.html` | HTML | 117 |
| `templates/cbv/leave_requests/custom_status_col.html` | HTML | 15 |
| `templates/cbv/leave_requests/filter.html` | HTML | 157 |
| `templates/cbv/leave_requests/form/inherit.html` | HTML | 111 |
| `templates/cbv/leave_requests/leave_clash.html` | HTML | 11 |
| `templates/cbv/leave_requests/leave_request_detail_actions.html` | HTML | 59 |
| `templates/cbv/leave_requests/leave_request_emp_col.html` | HTML | 27 |
| `templates/cbv/leave_requests/leave_request_tab_actions.html` | HTML | 5 |
| `templates/cbv/leave_requests/leave_requests_export.html` | HTML | 162 |
| `templates/cbv/leave_requests/leave_requests_home.html` | HTML | 425 |
| `templates/cbv/leave_requests/multiple_approval_action.html` | HTML | 20 |
| `templates/cbv/leave_requests/penality.html` | HTML | 5 |
| `templates/cbv/leave_settings/leave_settings_main.html` | HTML | 10 |
| `templates/cbv/leave_settings/leave_types_tab.html` | HTML | 58 |
| `templates/cbv/leave_settings/multiple_approval_tab.html` | HTML | 26 |
| `templates/cbv/leave_types/conditions_display.html` | HTML | 11 |
| `templates/cbv/leave_types/detail_actions.html` | HTML | 45 |
| `templates/cbv/leave_types/inherit.html` | HTML | 89 |
| `templates/cbv/leave_types/leave_detail_carryforward.html` | HTML | 25 |
| `templates/cbv/leave_types/leave_detail_reset.html` | HTML | 34 |
| `templates/cbv/leave_types/leave_type_filter.html` | HTML | 111 |
| `templates/cbv/leave_types/leave_type_home.html` | HTML | 70 |
| `templates/cbv/leave_types/leave_type_list_actions.html` | HTML | 67 |
| `templates/cbv/my_leave_request/attachment_action.html` | HTML | 13 |
| `templates/cbv/my_leave_request/cancelled_action.html` | HTML | 18 |
| `templates/cbv/my_leave_request/comment.html` | HTML | 7 |
| `templates/cbv/my_leave_request/confirm_cancel.html` | HTML | 17 |
| `templates/cbv/my_leave_request/detail_leave_actions.html` | HTML | 41 |
| `templates/cbv/my_leave_request/filter.html` | HTML | 54 |
| `templates/cbv/my_leave_request/form/inherit.html` | HTML | 100 |
| `templates/cbv/my_leave_request/leave_actions.html` | HTML | 43 |
| `templates/cbv/my_leave_request/leave_type_col.html` | HTML | 36 |
| `templates/cbv/my_leave_request/my_leave_request_home.html` | HTML | 115 |
| `templates/cbv/my_leave_request/rejected_action.html` | HTML | 26 |
| `templates/cbv/restricted_days/actions.html` | HTML | 30 |
| `templates/cbv/restricted_days/detail_action.html` | HTML | 42 |
| `templates/cbv/restricted_days/filter.html` | HTML | 98 |
| `templates/cbv/restricted_days/job_position.html` | HTML | 9 |
| `templates/cbv/restricted_days/restrict_form.html` | HTML | 20 |
| `templates/cbv/restricted_days/restricted_days.html` | HTML | 34 |
| `templates/leave/company_leave/company_leave.html` | HTML | 127 |
| `templates/leave/company_leave/company_leave_creation_form.html` | HTML | 57 |
| `templates/leave/company_leave/company_leave_update_form.html` | HTML | 58 |
| `templates/leave/company_leave/company_leave_view.html` | HTML | 100 |
| `templates/leave/compensatory_leave/attendance_id.html` | HTML | 1 |
| `templates/leave/compensatory_leave/comp_leave_form.html` | HTML | 35 |
| `templates/leave/compensatory_leave/compensatory_leave_comment.html` | HTML | 201 |
| `templates/leave/compensatory_leave/compensatory_leave_reject_form..html` | HTML | 34 |
| `templates/leave/compensatory_leave/compensatory_leave_req_list.html` | HTML | 605 |
| `templates/leave/compensatory_leave/compensatory_leave_type.html` | HTML | 71 |
| `templates/leave/compensatory_leave/compensatory_leave_view.html` | HTML | 413 |
| `templates/leave/compensatory_leave/individual_view_compensatory.html` | HTML | 207 |
| `templates/leave/dashboard.html` | HTML | 930 |
| `templates/leave/dashboard/leave_allocation_approve.html` | HTML | 98 |
| `templates/leave/dashboard/leave_request_approve.html` | HTML | 87 |
| `templates/leave/dashboard/on_leave.html` | HTML | 46 |
| `templates/leave/holiday/holiday.html` | HTML | 262 |
| `templates/leave/holiday/holiday_export_filter_form.html` | HTML | 75 |
| `templates/leave/holiday/holiday_filter.html` | HTML | 45 |
| `templates/leave/holiday/holiday_form.html` | HTML | 66 |
| `templates/leave/holiday/holiday_update_form.html` | HTML | 58 |
| `templates/leave/holiday/holiday_view.html` | HTML | 308 |
| `templates/leave/job_position_field.html` | HTML | 9 |
| `templates/leave/leave_allocation_request/comment_view.html` | HTML | 66 |
| `templates/leave/leave_allocation_request/leave_allocation_comment.html` | HTML | 108 |
| `templates/leave/leave_allocation_request/leave_allocation_request_create.html` | HTML | 27 |
| `templates/leave/leave_allocation_request/leave_allocation_request_group_by.html` | HTML | 412 |
| `templates/leave/leave_allocation_request/leave_allocation_request_list.html` | HTML | 613 |
| `templates/leave/leave_allocation_request/leave_allocation_request_reject_form.html` | HTML | 40 |
| `templates/leave/leave_allocation_request/leave_allocation_request_single_view.html` | HTML | 222 |
| `templates/leave/leave_allocation_request/leave_allocation_request_update.html` | HTML | 18 |
| `templates/leave/leave_allocation_request/leave_allocation_request_view.html` | HTML | 385 |
| `templates/leave/leave_assign/assign_view.html` | HTML | 342 |
| `templates/leave/leave_assign/assigned_leave.html` | HTML | 175 |
| `templates/leave/leave_assign/assigned_leaves_export_form.html` | HTML | 145 |
| `templates/leave/leave_assign/assigned_leaves_filter.html` | HTML | 124 |
| `templates/leave/leave_assign/available_update_form.html` | HTML | 87 |
| `templates/leave/leave_assign/group_by.html` | HTML | 347 |
| `templates/leave/leave_assign/leave_assign_form.html` | HTML | 75 |
| `templates/leave/leave_assign/leave_assign_one_form.html` | HTML | 40 |
| `templates/leave/leave_assign/single_assign_view.html` | HTML | 163 |
| `templates/leave/leave_assign_form.html` | HTML | 30 |
| `templates/leave/leave_assign_one_form.html` | HTML | 26 |
| `templates/leave/leave_request/cancel_form.html` | HTML | 34 |
| `templates/leave/leave_request/cancellation_reject_form.html` | HTML | 22 |
| `templates/leave/leave_request/comment_view.html` | HTML | 61 |
| `templates/leave/leave_request/dashboard_leave_requests.html` | HTML | 59 |
| `templates/leave/leave_request/employee_available_leave_count.html` | HTML | 108 |
| `templates/leave/leave_request/filter_leave_requests.html` | HTML | 127 |
| `templates/leave/leave_request/group_by.html` | HTML | 452 |
| `templates/leave/leave_request/leave_clashes.html` | HTML | 191 |
| `templates/leave/leave_request/leave_comment.html` | HTML | 101 |
| `templates/leave/leave_request/leave_request_form.html` | HTML | 92 |
| `templates/leave/leave_request/leave_request_pdf.html` | HTML | 241 |
| `templates/leave/leave_request/leave_requests.html` | HTML | 598 |
| `templates/leave/leave_request/leave_requests_export_filter.html` | HTML | 207 |
| `templates/leave/leave_request/leave_type_field.html` | HTML | 8 |
| `templates/leave/leave_request/one_request_view.html` | HTML | 251 |
| `templates/leave/leave_request/penalty/form.html` | HTML | 85 |
| `templates/leave/leave_request/penalty/penalty_view.html` | HTML | 0 |
| `templates/leave/leave_request/request_update_form.html` | HTML | 84 |
| `templates/leave/leave_request/request_view.html` | HTML | 383 |
| `templates/leave/leave_request/user_cancel_form.html` | HTML | 48 |
| `templates/leave/leave_request_form.html` | HTML | 17 |
| `templates/leave/leave_type/conditions_panel.html` | HTML | 104 |
| `templates/leave/leave_type/leave_type_creation.html` | HTML | 531 |
| `templates/leave/leave_type/leave_type_empty_view.html` | HTML | 45 |
| `templates/leave/leave_type/leave_type_filter.html` | HTML | 105 |
| `templates/leave/leave_type/leave_type_form_fragment.html` | HTML | 775 |
| `templates/leave/leave_type/leave_type_individual_view.html` | HTML | 252 |
| `templates/leave/leave_type/leave_type_update_page.html` | HTML | 5 |
| `templates/leave/leave_type/leave_type_view.html` | HTML | 112 |
| `templates/leave/leave_type/leave_types.html` | HTML | 159 |
| `templates/leave/leave_type_creation.html` | HTML | 327 |
| `templates/leave/one_request_view.html` | HTML | 94 |
| `templates/leave/request_update_form.html` | HTML | 20 |
| `templates/leave/restrict/restrict.html` | HTML | 221 |
| `templates/leave/restrict/restrict_filter.html` | HTML | 54 |
| `templates/leave/restrict/restrict_form.html` | HTML | 191 |
| `templates/leave/restrict/restrict_update_form.html` | HTML | 187 |
| `templates/leave/restrict/view_restrict.html` | HTML | 109 |
| `templates/leave/settings/leave_rules.html` | HTML | 104 |
| `templates/leave/settings/restrict_leaves.html` | HTML | 43 |
| `templates/leave/user_leave/group_by.html` | HTML | 393 |
| `templates/leave/user_leave/request_form.html` | HTML | 29 |
| `templates/leave/user_leave/user_leave.html` | HTML | 57 |
| `templates/leave/user_leave/user_request_form.html` | HTML | 101 |
| `templates/leave/user_leave/user_request_one.html` | HTML | 105 |
| `templates/leave/user_leave/user_request_update.html` | HTML | 105 |
| `templates/leave/user_leave/user_request_view.html` | HTML | 440 |
| `templates/leave/user_leave/user_requests.html` | HTML | 332 |
| `templates/leave/user_request_form.html` | HTML | 44 |
| `templates/leave/user_request_one.html` | HTML | 52 |
| `templatetags/__init__.py` | Python | 0 |
| `templatetags/leavefilters.py` | Python | 14 |
| `tests/__init__.py` | Test | 0 |
| `tests/fixtures.py` | Test | 78 |
| `tests/helpers.py` | Test | 40 |
| `tests/test_allocation_approve.py` | Test | 88 |
| `tests/test_approve_balance.py` | Test | 94 |
| `tests/test_cancellation_request.py` | Test | 203 |
| `tests/test_carryforward.py` | Test | 72 |
| `tests/test_clean_gates.py` | Test | 106 |
| `tests/test_conditions.py` | Test | 194 |
| `tests/test_employee_leave_details.py` | Test | 73 |
| `tests/test_forecast.py` | Test | 55 |
| `tests/test_holiday_filters.py` | Test | 210 |
| `tests/test_leave_ledger.py` | Test | 475 |
| `tests/test_leave_manager_scope.py` | Test | 208 |
| `tests/test_leave_request_idor.py` | Test | 106 |
| `tests/test_leave_tab_authz.py` | Test | 95 |
| `tests/test_payment_type.py` | Test | 59 |
| `tests/test_requested_days.py` | Test | 45 |
| `tests/test_reset_scheduling.py` | Test | 109 |
| `threading.py` | Python | 252 |
| `urls.py` | Python | 956 |
| `views.py` | Python | 6,678 |

</details>

### master_import

**27 files, 7,930 lines**.

<details>
<summary>Show all 27 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `apps.py` | Python | 7 |
| `datasets/__init__.py` | Python | 21 |
| `datasets/asset_allocation.py` | Python | 930 |
| `datasets/assets.py` | Python | 334 |
| `datasets/assigned_leave.py` | Python | 438 |
| `datasets/base.py` | Python | 93 |
| `datasets/employee_update.py` | Python | 604 |
| `datasets/employees.py` | Python | 903 |
| `datasets/salary_structure.py` | Python | 79 |
| `datasets/scoping.py` | Python | 51 |
| `migrations/0001_initial.py` | Migration | 46 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 59 |
| `parsing.py` | Python | 88 |
| `templates/master_import/_cell.html` | HTML | 2 |
| `templates/master_import/_review.html` | HTML | 145 |
| `templates/master_import/base.html` | HTML | 235 |
| `templates/master_import/history.html` | HTML | 100 |
| `templates/master_import/step_done.html` | HTML | 123 |
| `templates/master_import/step_map.html` | HTML | 166 |
| `templates/master_import/step_review.html` | HTML | 267 |
| `templates/master_import/step_upload.html` | HTML | 135 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_import.py` | Test | 2,369 |
| `urls.py` | Python | 31 |
| `views.py` | Python | 704 |

</details>

### notifications

**40 files, 2,482 lines**.

<details>
<summary>Show all 40 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 13 |
| `admin.py` | Python | 37 |
| `apps.py` | Python | 18 |
| `base/__init__.py` | Python | 0 |
| `base/admin.py` | Python | 16 |
| `base/models.py` | Python | 400 |
| `helpers.py` | Python | 64 |
| `migrations/0001_initial.py` | Migration | 119 |
| `migrations/0002_alter_notification_options_and_more.py` | Migration | 102 |
| `migrations/0003_remove_notification_verb_ar_and_more.py` | Migration | 32 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 31 |
| `settings.py` | Python | 21 |
| `signals.py` | Python | 6 |
| `static/notifications/notify.js` | JS | 124 |
| `templates/notifications/list.html` | HTML | 5 |
| `templates/notifications/notice.html` | HTML | 24 |
| `templates/notifications/test_tags.html` | HTML | 8 |
| `templatetags/__init__.py` | Python | 0 |
| `templatetags/notifications_tags.py` | Python | 102 |
| `tests/__init__.py` | Test | 0 |
| `tests/sample_notifications/__init__.py` | Test | 3 |
| `tests/sample_notifications/admin.py` | Test | 11 |
| `tests/sample_notifications/apps.py` | Test | 6 |
| `tests/sample_notifications/migrations/__init__.py` | Migration | 0 |
| `tests/sample_notifications/models.py` | Test | 10 |
| `tests/sample_notifications/templatetags/__init__.py` | Test | 0 |
| `tests/sample_notifications/templatetags/notifications_tags.py` | Test | 1 |
| `tests/sample_notifications/tests.py` | Test | 62 |
| `tests/settings.py` | Test | 85 |
| `tests/static/notifications/live-test.js` | JS | 7 |
| `tests/templates/test_live.html` | HTML | 10 |
| `tests/test_models/migrations/__init__.py` | Migration | 0 |
| `tests/test_models/models.py` | Test | 17 |
| `tests/tests.py` | Test | 812 |
| `tests/urls.py` | Test | 53 |
| `tests/views.py` | Test | 42 |
| `urls.py` | Python | 40 |
| `utils.py` | Python | 15 |
| `views.py` | Python | 186 |

</details>

### offboarding

**84 files, 15,278 lines**.

<details>
<summary>Show all 84 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `admin.py` | Python | 25 |
| `apps.py` | Python | 18 |
| `cbv/__init__.py` | Python | 0 |
| `cbv/accessibility.py` | Python | 94 |
| `cbv/exit_process.py` | Python | 1,493 |
| `cbv/resignation.py` | Python | 331 |
| `cbv/resignation_tab.py` | Python | 90 |
| `cbv_decorators.py` | Python | 79 |
| `dashboard.py` | Python | 472 |
| `decorators.py` | Python | 110 |
| `filters.py` | Python | 652 |
| `forms.py` | Python | 332 |
| `migrations/0001_initial.py` | Migration | 867 |
| `migrations/0002_alter_offboardingemployee_notice_period_ends_and_more.py` | Migration | 28 |
| `migrations/0003_offboardingtask_is_required.py` | Migration | 18 |
| `migrations/0004_historicalresignationletter.py` | Migration | 52 |
| `migrations/0005_alter_employeetask_is_active_and_more.py` | Migration | 73 |
| `migrations/0006_alter_offboardingtask_is_required.py` | Migration | 18 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 704 |
| `sidebar.py` | Python | 122 |
| `static/offboarding/dashboard.js` | JS | 120 |
| `templates/cbv/employee_tasks/employee_task_filter.html` | HTML | 49 |
| `templates/cbv/employee_tasks/employee_tasks.html` | HTML | 12 |
| `templates/cbv/exit_process/detail_page_description.html` | HTML | 9 |
| `templates/cbv/exit_process/detail_view_tasks.html` | HTML | 50 |
| `templates/cbv/exit_process/detailed_page_empty.html` | HTML | 24 |
| `templates/cbv/exit_process/employee_list.html` | HTML | 479 |
| `templates/cbv/exit_process/offboarding_pipeline_shell.html` | HTML | 82 |
| `templates/cbv/exit_process/pipeline_action_col.html` | HTML | 96 |
| `templates/cbv/exit_process/pipeline_filter.html` | HTML | 178 |
| `templates/cbv/exit_process/pipeline_stage_col.html` | HTML | 12 |
| `templates/cbv/exit_process/pipeline_tab_filter.html` | HTML | 102 |
| `templates/cbv/exit_process/pipeline_view.html` | HTML | 46 |
| `templates/cbv/exit_process/quick_actions.html` | HTML | 267 |
| `templates/cbv/exit_process/stage_order.html` | HTML | 72 |
| `templates/cbv/exit_process/tasks_cols.html` | HTML | 44 |
| `templates/cbv/resignation/actions.html` | HTML | 181 |
| `templates/cbv/resignation/description.html` | HTML | 66 |
| `templates/cbv/resignation/detail_description.html` | HTML | 13 |
| `templates/cbv/resignation/detail_view.html` | HTML | 5 |
| `templates/cbv/resignation/filter.html` | HTML | 110 |
| `templates/cbv/resignation/options.html` | HTML | 91 |
| `templates/cbv/resignation/resignation.html` | HTML | 151 |
| `templates/cbv/resignation/resignation_tab.html` | HTML | 19 |
| `templates/offboarding/dashboard.html` | HTML | 1,507 |
| `templates/offboarding/dashboard/asset_returned_table.html` | HTML | 87 |
| `templates/offboarding/dashboard/dashboard.html` | HTML | 177 |
| `templates/offboarding/dashboard/employee_feedback_table.html` | HTML | 75 |
| `templates/offboarding/dashboard/employee_task_table.html` | HTML | 70 |
| `templates/offboarding/employee/form.html` | HTML | 17 |
| `templates/offboarding/note/view_notes.html` | HTML | 152 |
| `templates/offboarding/pipeline/employee_task.html` | HTML | 44 |
| `templates/offboarding/pipeline/filter.html` | HTML | 115 |
| `templates/offboarding/pipeline/form.html` | HTML | 17 |
| `templates/offboarding/pipeline/individual_view.html` | HTML | 160 |
| `templates/offboarding/pipeline/nav.html` | HTML | 69 |
| `templates/offboarding/pipeline/offboardings.html` | HTML | 309 |
| `templates/offboarding/pipeline/pipeline.html` | HTML | 58 |
| `templates/offboarding/resignation/filter.html` | HTML | 56 |
| `templates/offboarding/resignation/form.html` | HTML | 7 |
| `templates/offboarding/resignation/group_by.html` | HTML | 345 |
| `templates/offboarding/resignation/nav.html` | HTML | 171 |
| `templates/offboarding/resignation/request_cards.html` | HTML | 299 |
| `templates/offboarding/resignation/request_list.html` | HTML | 332 |
| `templates/offboarding/resignation/request_single_view.html` | HTML | 178 |
| `templates/offboarding/resignation/requests_view.html` | HTML | 153 |
| `templates/offboarding/settings/offboarding_rules.html` | HTML | 103 |
| `templates/offboarding/settings/settings.html` | HTML | 21 |
| `templates/offboarding/stage/form.html` | HTML | 17 |
| `templates/offboarding/stage/offboarding_body.html` | HTML | 184 |
| `templates/offboarding/stage/stages.html` | HTML | 43 |
| `templates/offboarding/task/form.html` | HTML | 43 |
| `templates/offboarding/task/table_body.html` | HTML | 224 |
| `templatetags/__init__.py` | Python | 0 |
| `templatetags/migrations/__init__.py` | Migration | 0 |
| `templatetags/offboarding_filter.py` | Python | 199 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_archive_revokes_login.py` | Test | 119 |
| `tests/test_dashboard_pipeline.py` | Test | 112 |
| `tests/test_offboarding_create.py` | Test | 24 |
| `urls.py` | Python | 392 |
| `views.py` | Python | 1,543 |

</details>

### onboarding

**91 files, 15,736 lines**.

<details>
<summary>Show all 91 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `admin.py` | Python | 15 |
| `apps.py` | Python | 18 |
| `cbv/__init__.py` | Python | 0 |
| `cbv/accessibility.py` | Python | 28 |
| `cbv/dashboard.py` | Python | 245 |
| `cbv/onboarding_candidates.py` | Python | 356 |
| `cbv/onboarding_view.py` | Python | 261 |
| `cbv/pipeline.py` | Python | 1,179 |
| `cbv_decorators.py` | Python | 76 |
| `dashboard.py` | Python | 277 |
| `decorators.py` | Python | 114 |
| `filters.py` | Python | 596 |
| `forms.py` | Python | 475 |
| `migrations/0001_initial.py` | Migration | 558 |
| `migrations/0002_onboardingtask_is_required.py` | Migration | 18 |
| `migrations/0003_alter_candidatestage_is_active_and_more.py` | Migration | 53 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 288 |
| `sidebar.py` | Python | 71 |
| `static/dashboard/onboardChart.js` | JS | 181 |
| `static/kanban/script.js` | JS | 140 |
| `static/onboarding_view/activeTab.js` | JS | 39 |
| `static/onboarding_view/dashboard.js` | JS | 123 |
| `static/onboarding_view/search.js` | JS | 238 |
| `templates/cbv/candidate_tasks/candidate_task_filter.html` | HTML | 43 |
| `templates/cbv/candidate_tasks/candidate_tasks.html` | HTML | 12 |
| `templates/cbv/dashboard/my_onboarding_task.html` | HTML | 6 |
| `templates/cbv/dashboard/status.html` | HTML | 64 |
| `templates/cbv/onboarding_candidates/actions.html` | HTML | 149 |
| `templates/cbv/onboarding_candidates/cand_email.html` | HTML | 7 |
| `templates/cbv/onboarding_candidates/date_of_joining.html` | HTML | 1 |
| `templates/cbv/onboarding_candidates/filter.html` | HTML | 99 |
| `templates/cbv/onboarding_candidates/offer_letter.html` | HTML | 7 |
| `templates/cbv/onboarding_candidates/onboarding_candidates.html` | HTML | 272 |
| `templates/cbv/onboarding_candidates/probation_date.html` | HTML | 1 |
| `templates/cbv/onboarding_view/detail_view.html` | HTML | 7 |
| `templates/cbv/onboarding_view/status.html` | HTML | 24 |
| `templates/cbv/onboarding_view/task.html` | HTML | 19 |
| `templates/cbv/pipeline/onboarding/candidate_filter.html` | HTML | 107 |
| `templates/cbv/pipeline/onboarding/candidate_list.html` | HTML | 479 |
| `templates/cbv/pipeline/onboarding/filters.html` | HTML | 142 |
| `templates/cbv/pipeline/onboarding/pipeline.html` | HTML | 62 |
| `templates/cbv/pipeline/onboarding/quick_actions.html` | HTML | 288 |
| `templates/cbv/pipeline/onboarding/recruitment_pipeline_shell.html` | HTML | 64 |
| `templates/cbv/pipeline/onboarding/stage_drop_down.html` | HTML | 17 |
| `templates/cbv/pipeline/onboarding/stage_order.html` | HTML | 70 |
| `templates/cbv/pipeline/onboarding/stages_v2.html` | HTML | 104 |
| `templates/cbv/pipeline/onboarding/tasks.html` | HTML | 22 |
| `templates/onboarding/candidate_creation.html` | HTML | 87 |
| `templates/onboarding/candidate_filter.html` | HTML | 87 |
| `templates/onboarding/candidate_task.html` | HTML | 128 |
| `templates/onboarding/candidate_update.html` | HTML | 103 |
| `templates/onboarding/candidates.html` | HTML | 514 |
| `templates/onboarding/candidates_view.html` | HTML | 488 |
| `templates/onboarding/dashboard.html` | HTML | 594 |
| `templates/onboarding/dashboard/status_list.html` | HTML | 61 |
| `templates/onboarding/dashboard/task_report.html` | HTML | 93 |
| `templates/onboarding/employee_bank_details.html` | HTML | 171 |
| `templates/onboarding/employee_creation.html` | HTML | 213 |
| `templates/onboarding/empty_task.html` | HTML | 8 |
| `templates/onboarding/filters.html` | HTML | 59 |
| `templates/onboarding/group_by.html` | HTML | 652 |
| `templates/onboarding/kanban/kanban.html` | HTML | 279 |
| `templates/onboarding/mail_templates/default.html` | HTML | 146 |
| `templates/onboarding/onboarding_table.html` | HTML | 397 |
| `templates/onboarding/onboarding_view.html` | HTML | 305 |
| `templates/onboarding/onboarding_view_nav.html` | HTML | 50 |
| `templates/onboarding/profile_view.html` | HTML | 128 |
| `templates/onboarding/rejection/form.html` | HTML | 7 |
| `templates/onboarding/send_mail_form.html` | HTML | 14 |
| `templates/onboarding/single_view.html` | HTML | 134 |
| `templates/onboarding/stage_form.html` | HTML | 24 |
| `templates/onboarding/stage_update.html` | HTML | 24 |
| `templates/onboarding/static/country.js` | JS | 300 |
| `templates/onboarding/static/index.js` | JS | 22 |
| `templates/onboarding/static/style.css` | CSS | 195 |
| `templates/onboarding/tabs.html` | HTML | 16 |
| `templates/onboarding/task_form.html` | HTML | 53 |
| `templates/onboarding/task_update.html` | HTML | 47 |
| `templates/onboarding/user_creation.html` | HTML | 128 |
| `templates/onboarding/welcome_aboard.html` | HTML | 78 |
| `templatetags/__init__.py` | Python | 0 |
| `templatetags/migrations/__init__.py` | Migration | 0 |
| `templatetags/onboardingfilters.py` | Python | 111 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_initial_stage.py` | Test | 21 |
| `threadings/__init__.py` | Python | 0 |
| `threadings/portal_send.py` | Python | 5 |
| `urls.py` | Python | 344 |
| `views.py` | Python | 2,235 |

</details>

### outlook_auth

**16 files, 759 lines**.

<details>
<summary>Show all 16 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 32 |
| `admin.py` | Python | 16 |
| `apps.py` | Python | 14 |
| `backends.py` | Python | 175 |
| `cbv/views.py` | Python | 103 |
| `filters.py` | Python | 26 |
| `forms.py` | Python | 20 |
| `methods.py` | Python | 16 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 84 |
| `scheduler.py` | Python | 36 |
| `templates/outlook/actions.html` | HTML | 16 |
| `templates/outlook/view_records.html` | HTML | 21 |
| `tests.py` | Test | 3 |
| `urls.py` | Python | 28 |
| `views.py` | Python | 169 |

</details>

### payroll

**334 files, 78,802 lines**.

<details>
<summary>Show all 334 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `admin.py` | Python | 35 |
| `apps.py` | Python | 58 |
| `cbv/accessibility.py` | Python | 50 |
| `cbv/allowance_deduction.py` | Python | 403 |
| `cbv/allowances.py` | Python | 432 |
| `cbv/asset_fine.py` | Python | 54 |
| `cbv/contracts.py` | Python | 336 |
| `cbv/dashboard.py` | Python | 212 |
| `cbv/deduction.py` | Python | 355 |
| `cbv/federal_tax.py` | Python | 344 |
| `cbv/loan_advance_salary.py` | Python | 436 |
| `cbv/payroll_batch.py` | Python | 92 |
| `cbv/payslip.py` | Python | 541 |
| `cbv/payslip_automation.py` | Python | 205 |
| `cbv/reimbursements.py` | Python | 568 |
| `cbv/salary_structure.py` | Python | 415 |
| `cbv/settings_tabs.py` | Python | 129 |
| `component_library.py` | Python | 354 |
| `context_processors.py` | Python | 60 |
| `dashboard.py` | Python | 732 |
| `decorators.py` | Python | 66 |
| `filters.py` | Python | 1,084 |
| `forms/__init__.py` | Python | 0 |
| `forms/batch_forms.py` | Python | 155 |
| `forms/component_forms.py` | Python | 1,582 |
| `forms/component_layout.py` | Python | 660 |
| `forms/forms.py` | Python | 461 |
| `forms/tax_forms.py` | Python | 236 |
| `management/__init__.py` | Python | 0 |
| `management/commands/__init__.py` | Python | 0 |
| `management/commands/backfill_component_sequence.py` | Python | 78 |
| `management/commands/check_structure_invariants.py` | Python | 82 |
| `management/commands/create_payroll_fixtures.py` | Python | 804 |
| `management/commands/create_precise_payroll_fixtures.py` | Python | 520 |
| `management/commands/normalise_component_basis.py` | Python | 75 |
| `management/commands/normalise_payslip_basic_pay.py` | Python | 141 |
| `management/commands/normalise_payslip_deductions.py` | Python | 110 |
| `management/commands/payroll_snapshot.py` | Python | 137 |
| `management/commands/report_lop_deduction_mode.py` | Python | 57 |
| `management/commands/seed_tax_packs.py` | Python | 71 |
| `management/commands/sync_system_components.py` | Python | 154 |
| `methods/__init__.py` | Python | 0 |
| `methods/basic_pay_source.py` | Python | 108 |
| `methods/batch_run.py` | Python | 401 |
| `methods/component_engine.py` | Python | 313 |
| `methods/component_formula.py` | Python | 114 |
| `methods/component_summary.py` | Python | 204 |
| `methods/contributions.py` | Python | 187 |
| `methods/deductions.py` | Python | 94 |
| `methods/earning_working.py` | Python | 289 |
| `methods/employer_cost.py` | Python | 121 |
| `methods/federal_tax.py` | Python | 49 |
| `methods/limits.py` | Python | 34 |
| `methods/methods.py` | Python | 1,114 |
| `methods/payroll_run.py` | Python | 753 |
| `methods/payslip_calc.py` | Python | 1,402 |
| `methods/payslip_edit.py` | Python | 873 |
| `methods/proration.py` | Python | 143 |
| `methods/safe_tax_code.py` | Python | 363 |
| `methods/structure_rules.py` | Python | 262 |
| `methods/tax_calc.py` | Python | 364 |
| `migrations/0001_initial.py` | Migration | 2,312 |
| `migrations/0002_alter_allowance_maximum_amount_and_more.py` | Migration | 49 |
| `migrations/0003_alter_payrollsettings_position.py` | Migration | 18 |
| `migrations/0004_alter_allowance_include_active_employees_and_more.py` | Migration | 33 |
| `migrations/0005_alter_allowance_based_on.py` | Migration | 18 |
| `migrations/0006_payslip_unique_payslip_per_employee_period.py` | Migration | 20 |
| `migrations/0007_alter_allowance_amount_and_more.py` | Migration | 297 |
| `migrations/0008_payslip_payslip_end_date_idx_and_more.py` | Migration | 24 |
| `migrations/0009_encashmentgeneralsettings_department_and_more.py` | Migration | 66 |
| `migrations/0010_applycondition_allowance_code_allowance_formula_and_more.py` | Migration | 350 |
| `migrations/0011_filingstatus_name_length.py` | Migration | 18 |
| `migrations/0012_alter_allowance_is_active_and_more.py` | Migration | 128 |
| `migrations/__init__.py` | Migration | 0 |
| `models/__init__.py` | Python | 0 |
| `models/models.py` | Python | 4,369 |
| `models/payroll_batch.py` | Python | 425 |
| `models/tax_models.py` | Python | 160 |
| `scheduler.py` | Python | 141 |
| `settings.py` | Python | 20 |
| `sidebar.py` | Python | 168 |
| `signals.py` | Python | 179 |
| `static/cbv/actions.js` | JS | 64 |
| `static/cbv/payslip.js` | JS | 124 |
| `static/payroll/action.js` | JS | 596 |
| `static/payroll/dashboard.js` | JS | 639 |
| `system_components.py` | Python | 270 |
| `tax_packs.py` | Python | 235 |
| `templates/cbv/allowance_deduction/allowance/custom_amount.html` | HTML | 20 |
| `templates/cbv/allowance_deduction/allowance/detail_view_actions.html` | HTML | 51 |
| `templates/cbv/allowance_deduction/allowance/max_limit_col.html` | HTML | 12 |
| `templates/cbv/allowance_deduction/allowance_action.html` | HTML | 35 |
| `templates/cbv/allowance_deduction/allowance_deduction.html` | HTML | 36 |
| `templates/cbv/allowance_deduction/deductions/amount.html` | HTML | 15 |
| `templates/cbv/allowance_deduction/deductions/deductions_actions.html` | HTML | 43 |
| `templates/cbv/allowance_deduction/deductions/detail_view_actions.html` | HTML | 33 |
| `templates/cbv/allowance_deduction/deductions/has_maximum_limit.html` | HTML | 8 |
| `templates/cbv/allowances/allowance_filter.html` | HTML | 74 |
| `templates/cbv/allowances/allowances_home.html` | HTML | 109 |
| `templates/cbv/contracts/actions.html` | HTML | 55 |
| `templates/cbv/contracts/cal_leave_amount.html` | HTML | 10 |
| `templates/cbv/contracts/contract_detail.html` | HTML | 257 |
| `templates/cbv/contracts/contracts.html` | HTML | 125 |
| `templates/cbv/contracts/detail_action.html` | HTML | 38 |
| `templates/cbv/contracts/document.html` | HTML | 5 |
| `templates/cbv/contracts/export.html` | HTML | 169 |
| `templates/cbv/contracts/filter.html` | HTML | 171 |
| `templates/cbv/contracts/note.html` | HTML | 9 |
| `templates/cbv/contracts/status.html` | HTML | 7 |
| `templates/cbv/dashboard/contract_ending.html` | HTML | 11 |
| `templates/cbv/dashboard/contract_expired.html` | HTML | 11 |
| `templates/cbv/deduction/deduction.html` | HTML | 91 |
| `templates/cbv/deduction/filter.html` | HTML | 96 |
| `templates/cbv/federal_tax/form_inherit.html` | HTML | 4 |
| `templates/cbv/federal_tax/pipeline.html` | HTML | 77 |
| `templates/cbv/federal_tax/tax_bracket.html` | HTML | 32 |
| `templates/cbv/federal_tax/tax_bracket_list.html` | HTML | 37 |
| `templates/cbv/federal_tax/tax_brackets_col.html` | HTML | 38 |
| `templates/cbv/loan/loan_actions.html` | HTML | 19 |
| `templates/cbv/loan/loan_card.html` | HTML | 16 |
| `templates/cbv/loan/loan_detail_view.html` | HTML | 189 |
| `templates/cbv/loan/loan_filter.html` | HTML | 108 |
| `templates/cbv/loan/loan_installment_table.html` | HTML | 106 |
| `templates/cbv/loan/loan_main.html` | HTML | 79 |
| `templates/cbv/payroll_settings/allowance_tab.html` | HTML | 25 |
| `templates/cbv/payroll_settings/auto_payslip_tab.html` | HTML | 45 |
| `templates/cbv/payroll_settings/deduction_tab.html` | HTML | 25 |
| `templates/cbv/payroll_settings/payroll_settings_main.html` | HTML | 28 |
| `templates/cbv/payroll_settings/salary_structure_tab.html` | HTML | 21 |
| `templates/cbv/payslip/pay_display.html` | HTML | 3 |
| `templates/cbv/payslip/payslip_actions.html` | HTML | 54 |
| `templates/cbv/payslip/payslip_download_tab.html` | HTML | 5 |
| `templates/cbv/payslip/payslip_export.html` | HTML | 146 |
| `templates/cbv/payslip/payslip_filter.html` | HTML | 141 |
| `templates/cbv/payslip/payslip_home.html` | HTML | 161 |
| `templates/cbv/payslip/payslip_inherit_form.html` | HTML | 18 |
| `templates/cbv/payslip/payslip_status_col.html` | HTML | 17 |
| `templates/cbv/reimbursements/actions.html` | HTML | 87 |
| `templates/cbv/reimbursements/amount.html` | HTML | 20 |
| `templates/cbv/reimbursements/attachments.html` | HTML | 14 |
| `templates/cbv/reimbursements/comment.html` | HTML | 20 |
| `templates/cbv/reimbursements/detail_actions.html` | HTML | 90 |
| `templates/cbv/reimbursements/filter.html` | HTML | 102 |
| `templates/cbv/reimbursements/forms.html` | HTML | 88 |
| `templates/cbv/reimbursements/options.html` | HTML | 36 |
| `templates/cbv/reimbursements/reimbursements.html` | HTML | 158 |
| `templates/cbv/salary_structure/allowances_detail_col.html` | HTML | 37 |
| `templates/cbv/salary_structure/components_detail_col.html` | HTML | 125 |
| `templates/cbv/salary_structure/deductions_detail_col.html` | HTML | 38 |
| `templates/cbv/salary_structure/detail_view_actions.html` | HTML | 51 |
| `templates/cbv/salary_structure/employees_detail_col.html` | HTML | 368 |
| `templates/cbv/salary_structure/example_detail_col.html` | HTML | 502 |
| `templates/cbv/salary_structure/salary_structure_action.html` | HTML | 31 |
| `templates/cbv/salary_structure/structure_detail.html` | HTML | 265 |
| `templates/cbv/settings/is_active_col.html` | HTML | 11 |
| `templates/contract_form.html` | HTML | 170 |
| `templates/one_time_deduction.html` | HTML | 417 |
| `templates/payroll/_picker_modal.html` | HTML | 95 |
| `templates/payroll/allowance/allowance_form.html` | HTML | 78 |
| `templates/payroll/allowance/allowance_form_body.html` | HTML | 8 |
| `templates/payroll/allowance/card_allowance.html` | HTML | 169 |
| `templates/payroll/allowance/filter_allowance.html` | HTML | 66 |
| `templates/payroll/allowance/list_allowance.html` | HTML | 201 |
| `templates/payroll/allowance/quick_allowance_form.html` | HTML | 21 |
| `templates/payroll/allowance/view_allowance.html` | HTML | 242 |
| `templates/payroll/allowance/view_single_allowance.html` | HTML | 140 |
| `templates/payroll/asset_fine/form.html` | HTML | 11 |
| `templates/payroll/batch/_batch.css.html` | HTML | 624 |
| `templates/payroll/batch/_batch_filter.html` | HTML | 55 |
| `templates/payroll/batch/_pagination.html` | HTML | 58 |
| `templates/payroll/batch/_progress.html` | HTML | 115 |
| `templates/payroll/batch/_progress_modal.html` | HTML | 17 |
| `templates/payroll/batch/_run_actions.html` | HTML | 12 |
| `templates/payroll/batch/_steps.html` | HTML | 27 |
| `templates/payroll/batch/batch_detail.html` | HTML | 222 |
| `templates/payroll/batch/batch_home.html` | HTML | 76 |
| `templates/payroll/batch/pay_period_settings.html` | HTML | 86 |
| `templates/payroll/batch/wizard_progress.html` | HTML | 32 |
| `templates/payroll/batch/wizard_review.html` | HTML | 602 |
| `templates/payroll/batch/wizard_scope.html` | HTML | 116 |
| `templates/payroll/bonus/form.html` | HTML | 87 |
| `templates/payroll/common/form.html` | HTML | 138 |
| `templates/payroll/common/form_fragment.html` | HTML | 192 |
| `templates/payroll/common/form_modal.html` | HTML | 32 |
| `templates/payroll/component/_applies_rows.html` | HTML | 31 |
| `templates/payroll/component/_applies_table.html` | HTML | 211 |
| `templates/payroll/component/_apply_condition_row.html` | HTML | 115 |
| `templates/payroll/component/_component_form.html` | HTML | 583 |
| `templates/payroll/component/_condition_inputs.html` | HTML | 44 |
| `templates/payroll/component/_field.html` | HTML | 37 |
| `templates/payroll/component/_formula_builder.html` | HTML | 693 |
| `templates/payroll/component/_library_modal.html` | HTML | 100 |
| `templates/payroll/contract/bulk_components_modal.html` | HTML | 177 |
| `templates/payroll/contract/components_modal.html` | HTML | 86 |
| `templates/payroll/contract/contract_empty.html` | HTML | 31 |
| `templates/payroll/contract/contract_export_filter.html` | HTML | 227 |
| `templates/payroll/contract/contract_list.html` | HTML | 239 |
| `templates/payroll/contract/contract_single_view.html` | HTML | 198 |
| `templates/payroll/contract/contract_view.html` | HTML | 320 |
| `templates/payroll/contract/filter_contract.html` | HTML | 160 |
| `templates/payroll/contract/group_by.html` | HTML | 269 |
| `templates/payroll/contribution/contribution_deduction_list.html` | HTML | 81 |
| `templates/payroll/contribution/contribution_detail.html` | HTML | 93 |
| `templates/payroll/contribution/contribution_home.html` | HTML | 178 |
| `templates/payroll/dashboard.html` | HTML | 1,085 |
| `templates/payroll/dashboard/contribution.html` | HTML | 41 |
| `templates/payroll/deduction/card_deduction.html` | HTML | 155 |
| `templates/payroll/deduction/deduction_form.html` | HTML | 77 |
| `templates/payroll/deduction/deduction_form_body.html` | HTML | 8 |
| `templates/payroll/deduction/filter_deduction.html` | HTML | 67 |
| `templates/payroll/deduction/list_deduction.html` | HTML | 222 |
| `templates/payroll/deduction/payslip_deduct.html` | HTML | 19 |
| `templates/payroll/deduction/quick_deduction_form.html` | HTML | 21 |
| `templates/payroll/deduction/view_deduction.html` | HTML | 239 |
| `templates/payroll/deduction/view_single_deduction.html` | HTML | 143 |
| `templates/payroll/htmx/form.html` | HTML | 134 |
| `templates/payroll/loan/filter.html` | HTML | 59 |
| `templates/payroll/loan/form.html` | HTML | 11 |
| `templates/payroll/loan/installments.html` | HTML | 203 |
| `templates/payroll/loan/nav.html` | HTML | 113 |
| `templates/payroll/loan/records.html` | HTML | 95 |
| `templates/payroll/loan/records_card.html` | HTML | 328 |
| `templates/payroll/loan/records_list.html` | HTML | 817 |
| `templates/payroll/loan/view_loan.html` | HTML | 33 |
| `templates/payroll/mail_templates/default.html` | HTML | 156 |
| `templates/payroll/payslip/_income_tax_detail.html` | HTML | 128 |
| `templates/payroll/payslip/_tax_side_panel.html` | HTML | 209 |
| `templates/payroll/payslip/bulk_create_payslip.html` | HTML | 61 |
| `templates/payroll/payslip/create_payslip.html` | HTML | 59 |
| `templates/payroll/payslip/edit_components_modal.html` | HTML | 657 |
| `templates/payroll/payslip/filter_payslips.html` | HTML | 160 |
| `templates/payroll/payslip/group_by.html` | HTML | 393 |
| `templates/payroll/payslip/group_payslips.html` | HTML | 261 |
| `templates/payroll/payslip/individual_payslip.html` | HTML | 65 |
| `templates/payroll/payslip/individual_payslip_summery.html` | HTML | 376 |
| `templates/payroll/payslip/list_payslips.html` | HTML | 16 |
| `templates/payroll/payslip/payslip_export_filter.html` | HTML | 241 |
| `templates/payroll/payslip/payslip_pdf.html` | HTML | 322 |
| `templates/payroll/payslip/payslip_table.html` | HTML | 254 |
| `templates/payroll/payslip/payslips_quick_filter.html` | HTML | 74 |
| `templates/payroll/payslip/pending_attendance_row.html` | HTML | 32 |
| `templates/payroll/payslip/view_payslips.html` | HTML | 494 |
| `templates/payroll/reimbursement/attachments.html` | HTML | 46 |
| `templates/payroll/reimbursement/bonus_points_note.html` | HTML | 12 |
| `templates/payroll/reimbursement/comment_view.html` | HTML | 54 |
| `templates/payroll/reimbursement/filter.html` | HTML | 54 |
| `templates/payroll/reimbursement/form.html` | HTML | 60 |
| `templates/payroll/reimbursement/nav.html` | HTML | 79 |
| `templates/payroll/reimbursement/reimbursement_comment.html` | HTML | 160 |
| `templates/payroll/reimbursement/reimbursement_list.html` | HTML | 1,125 |
| `templates/payroll/reimbursement/reimbursenent_individual.html` | HTML | 207 |
| `templates/payroll/reimbursement/request_cards.html` | HTML | 980 |
| `templates/payroll/reimbursement/view_reimbursement.html` | HTML | 166 |
| `templates/payroll/salary_structure/_component_picker.html` | HTML | 198 |
| `templates/payroll/salary_structure/structure_form.html` | HTML | 115 |
| `templates/payroll/settings/auto_payslip_create_or_update.html` | HTML | 27 |
| `templates/payroll/settings/auto_payslip_settings.html` | HTML | 75 |
| `templates/payroll/settings/payroll_settings.html` | HTML | 65 |
| `templates/payroll/settings/payslip_auto_generate_table.html` | HTML | 114 |
| `templates/payroll/settings/settings.html` | HTML | 18 |
| `templates/payroll/tax/_python_editor.html` | HTML | 118 |
| `templates/payroll/tax/_python_editor_standalone.html` | HTML | 122 |
| `templates/payroll/tax/_tax_pack_modal.html` | HTML | 110 |
| `templates/payroll/tax/filing_status_edit.html` | HTML | 50 |
| `templates/payroll/tax/filing_status_list.html` | HTML | 118 |
| `templates/payroll/tax/filing_status_rules.html` | HTML | 268 |
| `templates/payroll/tax/filing_status_view.html` | HTML | 529 |
| `templates/payroll/tax/tax_bracket_creation.html` | HTML | 49 |
| `templates/payroll/tax/tax_bracket_edit.html` | HTML | 50 |
| `templates/payroll/tax/tax_bracket_view.html` | HTML | 70 |
| `templatetags/__inti__.py` | Python | 0 |
| `templatetags/current_month_record.py` | Python | 24 |
| `templatetags/migrations/__init__.py` | Migration | 0 |
| `templatetags/payrollfilters.py` | Python | 210 |
| `tests/__init__.py` | Test | 0 |
| `tests/factories_payroll.py` | Test | 117 |
| `tests/test_apply_conditions.py` | Test | 214 |
| `tests/test_batch_run.py` | Test | 390 |
| `tests/test_batch_views.py` | Test | 578 |
| `tests/test_calc_units.py` | Test | 243 |
| `tests/test_component_conditions.py` | Test | 155 |
| `tests/test_component_form_ui.py` | Test | 603 |
| `tests/test_component_library.py` | Test | 417 |
| `tests/test_component_list_pages.py` | Test | 129 |
| `tests/test_component_references.py` | Test | 261 |
| `tests/test_compute_salary_on_period.py` | Test | 110 |
| `tests/test_contract_components.py` | Test | 366 |
| `tests/test_contract_structure_validation.py` | Test | 230 |
| `tests/test_contributions.py` | Test | 276 |
| `tests/test_ctc_down.py` | Test | 688 |
| `tests/test_deduction_cap.py` | Test | 211 |
| `tests/test_employer_formula.py` | Test | 255 |
| `tests/test_filing_status_page.py` | Test | 485 |
| `tests/test_formula_lop_context.py` | Test | 137 |
| `tests/test_hourly_computation.py` | Test | 181 |
| `tests/test_lop_daily_amount.py` | Test | 267 |
| `tests/test_normalise_payslip_basic_pay.py` | Test | 199 |
| `tests/test_normalise_payslip_deductions.py` | Test | 138 |
| `tests/test_payroll_calculation_golden.py` | Test | 322 |
| `tests/test_payroll_fixtures.py` | Test | 294 |
| `tests/test_payslip_attendance_summary.py` | Test | 390 |
| `tests/test_payslip_edit.py` | Test | 1,378 |
| `tests/test_payslip_redirect_reverses.py` | Test | 74 |
| `tests/test_proration.py` | Test | 284 |
| `tests/test_review_regularisation.py` | Test | 294 |
| `tests/test_salary_structure_detail.py` | Test | 888 |
| `tests/test_structure_employees.py` | Test | 660 |
| `tests/test_structure_heads.py` | Test | 522 |
| `tests/test_structure_invariants.py` | Test | 332 |
| `tests/test_summary_half_days.py` | Test | 130 |
| `tests/test_system_components.py` | Test | 403 |
| `tests/test_tax_calc.py` | Test | 312 |
| `tests/test_tax_forms.py` | Test | 421 |
| `tests/test_tax_packs.py` | Test | 224 |
| `tests/test_tax_sandbox_security.py` | Test | 184 |
| `threadings/__init__.py` | Python | 0 |
| `threadings/mail.py` | Python | 82 |
| `urls/__init__.py` | Python | 0 |
| `urls/component_urls.py` | Python | 558 |
| `urls/tax_urls.py` | Python | 110 |
| `urls/urls.py` | Python | 458 |
| `views/__init__.py` | Python | 1 |
| `views/batch_views.py` | Python | 535 |
| `views/component_formula_views.py` | Python | 444 |
| `views/component_views.py` | Python | 2,551 |
| `views/contract_components.py` | Python | 217 |
| `views/contribution_views.py` | Python | 180 |
| `views/payslip_edit_views.py` | Python | 252 |
| `views/salary_structure_preview.py` | Python | 590 |
| `views/tax_views.py` | Python | 590 |
| `views/views.py` | Python | 2,120 |
| `widgets/__init__.py` | Python | 0 |
| `widgets/component_widgets.py` | Python | 146 |

</details>

### pg_backup

**8 files, 190 lines**.

<details>
<summary>Show all 8 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `admin.py` | Python | 3 |
| `apps.py` | Python | 11 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 3 |
| `scheduler.py` | Python | 167 |
| `tests.py` | Test | 3 |
| `views.py` | Python | 3 |

</details>

### pms

**177 files, 36,186 lines**.

<details>
<summary>Show all 177 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 1 |
| `admin.py` | Python | 43 |
| `apps.py` | Python | 43 |
| `cbv/__init__.py` | Python | 0 |
| `cbv/accessibility.py` | Python | 32 |
| `cbv/dashboard.py` | Python | 141 |
| `cbv/employee_objectives.py` | Python | 163 |
| `cbv/feedback.py` | Python | 817 |
| `cbv/key_result.py` | Python | 373 |
| `cbv/meetings.py` | Python | 313 |
| `cbv/objectives.py` | Python | 1,022 |
| `cbv/period.py` | Python | 157 |
| `cbv/question_template.py` | Python | 138 |
| `cbv/settings_tabs.py` | Python | 153 |
| `cbvs.py` | Python | 498 |
| `dashboard.py` | Python | 372 |
| `filters.py` | Python | 1,208 |
| `forms.py` | Python | 1,435 |
| `methods.py` | Python | 126 |
| `migrations/0001_initial.py` | Migration | 1,924 |
| `migrations/0002_alter_bonuspointsetting_applicable_for_and_more.py` | Migration | 120 |
| `migrations/0003_historicalobjective_is_template_and_more.py` | Migration | 23 |
| `migrations/0004_bonuspointsetting_company_id.py` | Migration | 20 |
| `migrations/0005_alter_period_period_name.py` | Migration | 18 |
| `migrations/0006_alter_employeebonuspoint_is_active_and_more.py` | Migration | 78 |
| `migrations/0007_alter_bonuspointsetting_is_active_and_more.py` | Migration | 23 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 1,903 |
| `scheduler.py` | Python | 44 |
| `sidebar.py` | Python | 107 |
| `signals.py` | Python | 209 |
| `static/cbv/360_feedback.js` | JS | 203 |
| `static/css/pms.css` | CSS | 25 |
| `static/src/dashboard/pmsChart.js` | JS | 198 |
| `static/src/feedback/action.js` | JS | 195 |
| `static/src/feedback/feedback_answer.js` | JS | 45 |
| `static/src/feedback/feedback_creation.js` | JS | 28 |
| `static/src/feedback/feedback_detailed_view.js` | JS | 54 |
| `static/src/okr/action.js` | JS | 387 |
| `static/src/okr/objective_creation.js` | JS | 19 |
| `static/src/period/period.js` | JS | 57 |
| `templates/anonymous/anonymous_feedback_form.html` | HTML | 79 |
| `templates/anonymous/single_view.html` | HTML | 90 |
| `templates/bonus/bonus_form.html` | HTML | 27 |
| `templates/bonus/bonus_point_action.html` | HTML | 27 |
| `templates/bonus/bonus_point_nav.html` | HTML | 7 |
| `templates/bonus/bonus_point_setting_detail_actions.html` | HTML | 31 |
| `templates/bonus/bonus_point_setting_section.html` | HTML | 52 |
| `templates/bonus/bonus_seetting_action.html` | HTML | 27 |
| `templates/bonus/employee_bonus_point_section.html` | HTML | 37 |
| `templates/bonus/is_active_toggle.html` | HTML | 26 |
| `templates/cbv/360_feedback/anonymous_action.html` | HTML | 43 |
| `templates/cbv/360_feedback/custom_actions.html` | HTML | 155 |
| `templates/cbv/360_feedback/custom_status_col.html` | HTML | 3 |
| `templates/cbv/360_feedback/due_in_col.html` | HTML | 2 |
| `templates/cbv/360_feedback/feedback_filter.html` | HTML | 197 |
| `templates/cbv/360_feedback/feedback_home.html` | HTML | 224 |
| `templates/cbv/360_feedback/form/feedback_creation_fragment.html` | HTML | 235 |
| `templates/cbv/360_feedback/form/form_inherit.html` | HTML | 34 |
| `templates/cbv/360_feedback/inherit.html` | HTML | 30 |
| `templates/cbv/dashboard/actions.html` | HTML | 39 |
| `templates/cbv/dashboard/current_value.html` | HTML | 76 |
| `templates/cbv/dashboard/keyresult_col.html` | HTML | 15 |
| `templates/cbv/employee_objectives/employee_key_result_filter.html` | HTML | 19 |
| `templates/cbv/employee_objectives/employee_key_results.html` | HTML | 12 |
| `templates/cbv/employee_objectives/employee_objective_filter.html` | HTML | 21 |
| `templates/cbv/employee_objectives/employee_objectives.html` | HTML | 12 |
| `templates/cbv/key_results/actions.html` | HTML | 61 |
| `templates/cbv/key_results/detail_view_actions.html` | HTML | 42 |
| `templates/cbv/key_results/key_result_filter.html` | HTML | 108 |
| `templates/cbv/key_results/key_result_home.html` | HTML | 17 |
| `templates/cbv/meetings/actions.html` | HTML | 228 |
| `templates/cbv/meetings/date.html` | HTML | 3 |
| `templates/cbv/meetings/detail_action.html` | HTML | 45 |
| `templates/cbv/meetings/employees.html` | HTML | 46 |
| `templates/cbv/meetings/filter.html` | HTML | 167 |
| `templates/cbv/meetings/forms/meet_create.html` | HTML | 21 |
| `templates/cbv/meetings/managers.html` | HTML | 46 |
| `templates/cbv/meetings/meetings.html` | HTML | 37 |
| `templates/cbv/meetings/mom_col.html` | HTML | 5 |
| `templates/cbv/meetings/mom_detail_col.html` | HTML | 13 |
| `templates/cbv/meetings/title.html` | HTML | 2 |
| `templates/cbv/objectives/actions.html` | HTML | 77 |
| `templates/cbv/objectives/assignees.html` | HTML | 47 |
| `templates/cbv/objectives/emp_obj_actions.html` | HTML | 67 |
| `templates/cbv/objectives/employee_objective_status.html` | HTML | 17 |
| `templates/cbv/objectives/extended_objectives.html` | HTML | 15 |
| `templates/cbv/objectives/filter.html` | HTML | 86 |
| `templates/cbv/objectives/form.html` | HTML | 33 |
| `templates/cbv/objectives/key_results.html` | HTML | 36 |
| `templates/cbv/objectives/manager.html` | HTML | 47 |
| `templates/cbv/objectives/objective_templates.html` | HTML | 198 |
| `templates/cbv/objectives/objectives.html` | HTML | 242 |
| `templates/cbv/objectives/self_key_results.html` | HTML | 37 |
| `templates/cbv/objectives/self_objective_action.html` | HTML | 75 |
| `templates/cbv/objectives/title.html` | HTML | 3 |
| `templates/cbv/performance_settings/bonus_point_tab.html` | HTML | 39 |
| `templates/cbv/performance_settings/objective_template_tab.html` | HTML | 19 |
| `templates/cbv/performance_settings/performance_settings_main.html` | HTML | 10 |
| `templates/cbv/performance_settings/period_tab.html` | HTML | 19 |
| `templates/cbv/performance_settings/question_template_tab.html` | HTML | 19 |
| `templates/cbv/period/actions.html` | HTML | 37 |
| `templates/cbv/period/detail_view_actions.html` | HTML | 33 |
| `templates/cbv/period/period.html` | HTML | 25 |
| `templates/cbv/question_template/actions.html` | HTML | 38 |
| `templates/cbv/question_template/question_template.html` | HTML | 53 |
| `templates/dashboard/feedback_answer.html` | HTML | 106 |
| `templates/dashboard/pms_dashboard.html` | HTML | 273 |
| `templates/feedback/answer/feedback_answer.html` | HTML | 259 |
| `templates/feedback/answer/feedback_answer_view.html` | HTML | 147 |
| `templates/feedback/bulk_feedback_form.html` | HTML | 172 |
| `templates/feedback/feedback_detailed_view.html` | HTML | 786 |
| `templates/feedback/feedback_detailed_view_answer.html` | HTML | 195 |
| `templates/feedback/feedback_empty.html` | HTML | 74 |
| `templates/feedback/feedback_list.html` | HTML | 971 |
| `templates/feedback/feedback_list_view.html` | HTML | 333 |
| `templates/feedback/feedback_overview.html` | HTML | 224 |
| `templates/feedback/feedback_update.html` | HTML | 247 |
| `templates/feedback/question/edit_form.html` | HTML | 123 |
| `templates/feedback/question/question_all.html` | HTML | 158 |
| `templates/feedback/question_template/question_template_detailed_view.html` | HTML | 175 |
| `templates/feedback/question_template/question_template_form.html` | HTML | 23 |
| `templates/feedback/question_template/question_template_list.html` | HTML | 118 |
| `templates/feedback/question_template/question_template_view.html` | HTML | 75 |
| `templates/meetings/form.html` | HTML | 47 |
| `templates/meetings/meeting_answer.html` | HTML | 261 |
| `templates/meetings/meeting_answer_view.html` | HTML | 164 |
| `templates/meetings/meeting_question_template_view.html` | HTML | 51 |
| `templates/meetings/meeting_single_view.html` | HTML | 151 |
| `templates/meetings/meetings_filter.html` | HTML | 132 |
| `templates/meetings/meetings_list.html` | HTML | 404 |
| `templates/meetings/meetings_nav.html` | HTML | 99 |
| `templates/meetings/mom_form.html` | HTML | 46 |
| `templates/meetings/view_meetings.html` | HTML | 40 |
| `templates/messages.html` | HTML | 13 |
| `templates/okr/add_assignees.html` | HTML | 38 |
| `templates/okr/create_period.html` | HTML | 126 |
| `templates/okr/emp_obj_single.html` | HTML | 185 |
| `templates/okr/emp_objective/emp_objective_create_form.html` | HTML | 26 |
| `templates/okr/emp_objective/emp_objective_dashboard_view.html` | HTML | 238 |
| `templates/okr/emp_objective/emp_objective_list.html` | HTML | 225 |
| `templates/okr/emp_objective_form.html` | HTML | 47 |
| `templates/okr/group_by.html` | HTML | 808 |
| `templates/okr/key_result/key_result_creation.html` | HTML | 167 |
| `templates/okr/key_result/key_result_creation_htmx.html` | HTML | 122 |
| `templates/okr/key_result/key_result_form.html` | HTML | 51 |
| `templates/okr/key_result/key_result_update.html` | HTML | 117 |
| `templates/okr/key_result/kr_card.html` | HTML | 160 |
| `templates/okr/key_result/kr_dashboard_view.html` | HTML | 299 |
| `templates/okr/key_result/kr_filter.html` | HTML | 65 |
| `templates/okr/key_result/kr_form.html` | HTML | 52 |
| `templates/okr/key_result/kr_list.html` | HTML | 260 |
| `templates/okr/key_result/kr_nav.html` | HTML | 116 |
| `templates/okr/key_result/real_kr_form.html` | HTML | 32 |
| `templates/okr/key_result/view_kr.html` | HTML | 30 |
| `templates/okr/kr_list.html` | HTML | 226 |
| `templates/okr/objective_creation.html` | HTML | 131 |
| `templates/okr/objective_detailed_view_activity.html` | HTML | 229 |
| `templates/okr/objective_list.html` | HTML | 648 |
| `templates/okr/okr_detailed_view.html` | HTML | 274 |
| `templates/okr/okr_detailed_view_fragment.html` | HTML | 273 |
| `templates/okr/okr_list.html` | HTML | 922 |
| `templates/okr/okr_nav.html` | HTML | 229 |
| `templates/okr/okr_view.html` | HTML | 157 |
| `templates/period/period_create.html` | HTML | 28 |
| `templates/period/period_list.html` | HTML | 101 |
| `templates/period/period_update.html` | HTML | 28 |
| `templates/period/period_view.html` | HTML | 71 |
| `templates/pms/dashboard.html` | HTML | 1,742 |
| `templatetags/__init__.py` | Python | 0 |
| `templatetags/pmsfilters.py` | Python | 137 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_check_duplication.py` | Test | 21 |
| `tests/test_dashboard_kpi.py` | Test | 174 |
| `tests/test_progress_calculation.py` | Test | 142 |
| `urls.py` | Python | 1,002 |
| `views.py` | Python | 4,272 |

</details>

### project

**111 files, 16,654 lines**.

<details>
<summary>Show all 111 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `_seed_timesheet_pagination.py` | Python | 153 |
| `admin.py` | Python | 9 |
| `apps.py` | Python | 19 |
| `cbv/__init__.py` | Python | 0 |
| `cbv/accessibility.py` | Python | 39 |
| `cbv/cbv_decorators.py` | Python | 43 |
| `cbv/dashboard.py` | Python | 127 |
| `cbv/project_stage.py` | Python | 138 |
| `cbv/projects.py` | Python | 593 |
| `cbv/tasks.py` | Python | 648 |
| `cbv/timesheet.py` | Python | 794 |
| `dashboard.py` | Python | 353 |
| `decorator.py` | Python | 195 |
| `filters.py` | Python | 316 |
| `forms.py` | Python | 466 |
| `methods.py` | Python | 431 |
| `migrations/0001_initial.py` | Migration | 437 |
| `migrations/0002_alter_project_options_alter_task_options.py` | Migration | 28 |
| `migrations/0003_alter_timesheet_options.py` | Migration | 17 |
| `migrations/0004_remove_project_members.py` | Migration | 17 |
| `migrations/0005_alter_timesheet_options.py` | Migration | 21 |
| `migrations/0006_alter_timesheet_options.py` | Migration | 17 |
| `migrations/0007_task_allocated_hours.py` | Migration | 19 |
| `migrations/0008_alter_project_is_active_alter_project_title_and_more.py` | Migration | 43 |
| `migrations/0009_alter_projectstage_is_end_stage.py` | Migration | 18 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 799 |
| `sidebar.py` | Python | 128 |
| `static/dashboard/projectChart.js` | JS | 116 |
| `static/project/import.js` | JS | 236 |
| `static/project/project_action.js` | JS | 228 |
| `static/project/project_view.js` | JS | 25 |
| `static/project/task_pipeline.js` | JS | 180 |
| `static/task_all/task_all_action.js` | JS | 305 |
| `static/time_sheet/time_sheet_action.js` | JS | 124 |
| `templates/cbv/projects/actions.html` | HTML | 79 |
| `templates/cbv/projects/filter.html` | HTML | 63 |
| `templates/cbv/projects/project_details.html` | HTML | 108 |
| `templates/cbv/projects/project_form.html` | HTML | 9 |
| `templates/cbv/projects/project_list.html` | HTML | 37 |
| `templates/cbv/projects/project_nav.html` | HTML | 22 |
| `templates/cbv/projects/project_tab.html` | HTML | 25 |
| `templates/cbv/projects/projects.html` | HTML | 110 |
| `templates/cbv/tasks/task_actions.html` | HTML | 57 |
| `templates/cbv/tasks/task_card_extra.html` | HTML | 66 |
| `templates/cbv/tasks/task_detail_actions.html` | HTML | 32 |
| `templates/cbv/tasks/task_document.html` | HTML | 10 |
| `templates/cbv/tasks/task_filter.html` | HTML | 76 |
| `templates/cbv/tasks/task_form.html` | HTML | 21 |
| `templates/cbv/tasks/task_template_view.html` | HTML | 128 |
| `templates/cbv/timesheet/actions.html` | HTML | 58 |
| `templates/cbv/timesheet/description_col.html` | HTML | 1 |
| `templates/cbv/timesheet/detail_actions.html` | HTML | 26 |
| `templates/cbv/timesheet/employee_field.html` | HTML | 20 |
| `templates/cbv/timesheet/filter.html` | HTML | 70 |
| `templates/cbv/timesheet/form.html` | HTML | 3 |
| `templates/cbv/timesheet/task_field.html` | HTML | 7 |
| `templates/cbv/timesheet/task_timesheet.html` | HTML | 37 |
| `templates/cbv/timesheet/timesheet.html` | HTML | 43 |
| `templates/dashboard/project_dashboard.html` | HTML | 143 |
| `templates/dashboard/project_details.html` | HTML | 66 |
| `templates/project/dashboard.html` | HTML | 865 |
| `templates/project/new/filter_project.html` | HTML | 44 |
| `templates/project/new/forms/project_creation.html` | HTML | 31 |
| `templates/project/new/forms/project_update.html` | HTML | 31 |
| `templates/project/new/navbar.html` | HTML | 234 |
| `templates/project/new/overall.html` | HTML | 33 |
| `templates/project/new/project_kanban_view.html` | HTML | 201 |
| `templates/project/new/project_list_view.html` | HTML | 231 |
| `templates/project/project_import.html` | HTML | 166 |
| `templates/project_stage/forms/create_project_stage.html` | HTML | 31 |
| `templates/project_stage/forms/update_project_stage.html` | HTML | 31 |
| `templates/task/new/filter_task.html` | HTML | 75 |
| `templates/task/new/forms/create_task.html` | HTML | 31 |
| `templates/task/new/forms/create_task_project.html` | HTML | 55 |
| `templates/task/new/forms/create_timesheet.html` | HTML | 38 |
| `templates/task/new/forms/quick_create_task_form.html` | HTML | 27 |
| `templates/task/new/forms/update_task.html` | HTML | 55 |
| `templates/task/new/forms/update_timesheet.html` | HTML | 37 |
| `templates/task/new/overall.html` | HTML | 141 |
| `templates/task/new/task_details.html` | HTML | 139 |
| `templates/task/new/task_kanban_view.html` | HTML | 252 |
| `templates/task/new/task_list_view.html` | HTML | 318 |
| `templates/task/new/task_navbar.html` | HTML | 98 |
| `templates/task/new/task_timesheet.html` | HTML | 137 |
| `templates/task_all/forms/create_project_stage_taskall.html` | HTML | 89 |
| `templates/task_all/forms/create_taskall.html` | HTML | 118 |
| `templates/task_all/forms/update_taskall.html` | HTML | 113 |
| `templates/task_all/task_all_card.html` | HTML | 237 |
| `templates/task_all/task_all_filter.html` | HTML | 48 |
| `templates/task_all/task_all_list.html` | HTML | 180 |
| `templates/task_all/task_all_navbar.html` | HTML | 157 |
| `templates/task_all/task_all_overall.html` | HTML | 121 |
| `templates/task_all/update_task.html` | HTML | 42 |
| `templates/time_sheet/chart.html` | HTML | 237 |
| `templates/time_sheet/filters.html` | HTML | 66 |
| `templates/time_sheet/form-create.html` | HTML | 129 |
| `templates/time_sheet/form-update.html` | HTML | 93 |
| `templates/time_sheet/form_project_time_sheet.html` | HTML | 93 |
| `templates/time_sheet/form_task_time_sheet.html` | HTML | 111 |
| `templates/time_sheet/time_sheet_card_view.html` | HTML | 188 |
| `templates/time_sheet/time_sheet_list_view.html` | HTML | 188 |
| `templates/time_sheet/time_sheet_navbar.html` | HTML | 144 |
| `templates/time_sheet/time_sheet_single_view.html` | HTML | 92 |
| `templates/time_sheet/time_sheet_view.html` | HTML | 65 |
| `templatetags/taskfilters.py` | Python | 78 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_time_helpers.py` | Test | 13 |
| `urls.py` | Python | 355 |
| `views.py` | Python | 1,997 |

</details>

### recruitment

**271 files, 49,801 lines**.

<details>
<summary>Show all 271 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `accessibility.py` | Python | 42 |
| `admin.py` | Python | 34 |
| `apps.py` | Python | 34 |
| `auth.py` | Python | 36 |
| `cbv/accessibility.py` | Python | 197 |
| `cbv/candidate_document.py` | Python | 74 |
| `cbv/candidate_mail_log.py` | Python | 63 |
| `cbv/candidate_profile.py` | Python | 139 |
| `cbv/candidate_reject_reason.py` | Python | 165 |
| `cbv/candidates.py` | Python | 1,037 |
| `cbv/dashboard.py` | Python | 166 |
| `cbv/interview.py` | Python | 264 |
| `cbv/pipeline.py` | Python | 1,011 |
| `cbv/recruitment_survey.py` | Python | 399 |
| `cbv/recruitment_view.py` | Python | 466 |
| `cbv/settings_tabs.py` | Python | 80 |
| `cbv/skill_zone.py` | Python | 134 |
| `cbv/skills.py` | Python | 154 |
| `cbv/stage_view.py` | Python | 359 |
| `cbv_decorators.py` | Python | 103 |
| `cbvs.py` | Python | 133 |
| `dashboard.py` | Python | 726 |
| `decorators.py` | Python | 227 |
| `filters.py` | Python | 1,346 |
| `forms.py` | Python | 1,510 |
| `methods.py` | Python | 66 |
| `migrations/0001_initial.py` | Migration | 2,182 |
| `migrations/0002_alter_recruitment_options_and_more.py` | Migration | 33 |
| `migrations/0003_alter_candidate_portfolio_alter_candidate_resume_and_more.py` | Migration | 70 |
| `migrations/0004_alter_recruitmentgeneralsetting_company_id.py` | Migration | 20 |
| `migrations/0005_historicalstage.py` | Migration | 49 |
| `migrations/0006_alter_rejectreason_options_alter_skillzone_options_and_more.py` | Migration | 47 |
| `migrations/0007_candidate_referral_source_and_more.py` | Migration | 33 |
| `migrations/0008_alter_historicalstage_stage_type_and_more.py` | Migration | 23 |
| `migrations/0009_alter_candidate_is_active_and_more.py` | Migration | 138 |
| `migrations/0010_alter_recruitment_publish_in_linkedin.py` | Migration | 18 |
| `migrations/0011_remove_recruitmentsurvey_recruitment_ids_and_more.py` | Migration | 22 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 2,126 |
| `pipeline_grouper.py` | Python | 134 |
| `scheduler.py` | Python | 52 |
| `sidebar.py` | Python | 195 |
| `signals.py` | Python | 82 |
| `static/candidate/actions.js` | JS | 15 |
| `static/candidate/bulk.js` | JS | 232 |
| `static/dashboard/candidateChart.js` | JS | 67 |
| `static/dashboard/joiningChart.js` | JS | 71 |
| `static/dashboard/recruitmentChart.js` | JS | 307 |
| `static/dashboard/vacancyChart.js` | JS | 25 |
| `static/pipeline/activeTab.js` | JS | 47 |
| `static/pipeline/badge.js` | JS | 73 |
| `static/pipeline/load.js` | JS | 20 |
| `static/pipeline/paginator.js` | JS | 64 |
| `static/pipeline/pipeline.js` | JS | 135 |
| `static/pipeline/pipelineDrag.js` | JS | 259 |
| `static/pipeline/recruitment.js` | JS | 148 |
| `static/pipeline/search.js` | JS | 0 |
| `static/recruitment/candidate.js` | JS | 0 |
| `static/recruitment/pipeline.js` | JS | 142 |
| `static/recruitment/stageScript.js` | JS | 0 |
| `static/recruitment/widget/recruitmentAjax.js` | JS | 61 |
| `static/recruitment/widget/recruitment_widget_style.css` | CSS | 0 |
| `templates/candidate/application_form.html` | HTML | 538 |
| `templates/candidate/application_form_component.html` | HTML | 53 |
| `templates/candidate/candidate_card.html` | HTML | 321 |
| `templates/candidate/candidate_create_form.html` | HTML | 221 |
| `templates/candidate/candidate_create_form_as_p.html` | HTML | 44 |
| `templates/candidate/candidate_create_modal_form.html` | HTML | 197 |
| `templates/candidate/candidate_empty.html` | HTML | 56 |
| `templates/candidate/candidate_history.html` | HTML | 35 |
| `templates/candidate/candidate_interview_view.html` | HTML | 166 |
| `templates/candidate/candidate_list.html` | HTML | 572 |
| `templates/candidate/candidate_nav.html` | HTML | 339 |
| `templates/candidate/candidate_rejection_form.html` | HTML | 23 |
| `templates/candidate/candidate_self_tracking.html` | HTML | 698 |
| `templates/candidate/candidate_view.html` | HTML | 128 |
| `templates/candidate/document.html` | HTML | 302 |
| `templates/candidate/document_create_form.html` | HTML | 18 |
| `templates/candidate/document_form.html` | HTML | 68 |
| `templates/candidate/export_filter.html` | HTML | 255 |
| `templates/candidate/filters.html` | HTML | 198 |
| `templates/candidate/group_by.html` | HTML | 717 |
| `templates/candidate/history.html` | HTML | 2 |
| `templates/candidate/individual.html` | HTML | 693 |
| `templates/candidate/individual_view_note.html` | HTML | 94 |
| `templates/candidate/interview_form.html` | HTML | 14 |
| `templates/candidate/interview_list.html` | HTML | 323 |
| `templates/candidate/interview_nav.html` | HTML | 133 |
| `templates/candidate/interview_view.html` | HTML | 67 |
| `templates/candidate/mail_log.html` | HTML | 75 |
| `templates/candidate/rating_tab.html` | HTML | 107 |
| `templates/candidate/reject_form.html` | HTML | 22 |
| `templates/candidate/self_login.html` | HTML | 43 |
| `templates/candidate/success.html` | HTML | 128 |
| `templates/candidate/view_file.html` | HTML | 65 |
| `templates/cbv/candidate_documents/actions.html` | HTML | 82 |
| `templates/cbv/candidate_documents/list_tab.html` | HTML | 47 |
| `templates/cbv/candidates/candidates.html` | HTML | 410 |
| `templates/cbv/candidates/export.html` | HTML | 28 |
| `templates/cbv/candidates/filter.html` | HTML | 230 |
| `templates/cbv/candidates/onboarding_tasks_tab.html` | HTML | 6 |
| `templates/cbv/candidates/option.html` | HTML | 73 |
| `templates/cbv/candidates/profile_about_tab.html` | HTML | 154 |
| `templates/cbv/candidates/profile_interview_tab.html` | HTML | 104 |
| `templates/cbv/candidates/profile_notes_tab.html` | HTML | 4 |
| `templates/cbv/candidates/profile_onboarding_tab.html` | HTML | 101 |
| `templates/cbv/candidates/profile_resume_tab.html` | HTML | 16 |
| `templates/cbv/candidates/profile_survey_tab.html` | HTML | 116 |
| `templates/cbv/candidates/rating.html` | HTML | 16 |
| `templates/cbv/candidates/resume.html` | HTML | 14 |
| `templates/cbv/interview/detail_view_actions.html` | HTML | 26 |
| `templates/cbv/interview/interview_actions.html` | HTML | 110 |
| `templates/cbv/interview/interview_filter.html` | HTML | 68 |
| `templates/cbv/interview/interview_home_view.html` | HTML | 171 |
| `templates/cbv/interview/interviewer_custom_col.html` | HTML | 36 |
| `templates/cbv/interview/status_custom_col.html` | HTML | 29 |
| `templates/cbv/pipeline/candidate_column.html` | HTML | 23 |
| `templates/cbv/pipeline/candidate_list.html` | HTML | 479 |
| `templates/cbv/pipeline/count_of_interviews.html` | HTML | 4 |
| `templates/cbv/pipeline/empty.html` | HTML | 12 |
| `templates/cbv/pipeline/interview_template.html` | HTML | 30 |
| `templates/cbv/pipeline/mail_status.html` | HTML | 15 |
| `templates/cbv/pipeline/pipeline.html` | HTML | 153 |
| `templates/cbv/pipeline/pipeline_filter.html` | HTML | 186 |
| `templates/cbv/pipeline/quick_actions.html` | HTML | 286 |
| `templates/cbv/pipeline/rating.html` | HTML | 36 |
| `templates/cbv/pipeline/recruitment_pipeline_shell.html` | HTML | 89 |
| `templates/cbv/pipeline/recruitment_tabs.html` | HTML | 235 |
| `templates/cbv/pipeline/stage_drop_down.html` | HTML | 17 |
| `templates/cbv/pipeline/stage_order.html` | HTML | 70 |
| `templates/cbv/pipeline/stages.html` | HTML | 89 |
| `templates/cbv/recruitment/actions.html` | HTML | 66 |
| `templates/cbv/recruitment/detail_action.html` | HTML | 58 |
| `templates/cbv/recruitment/filters.html` | HTML | 79 |
| `templates/cbv/recruitment/managers_col.html` | HTML | 59 |
| `templates/cbv/recruitment/open_jobs.html` | HTML | 48 |
| `templates/cbv/recruitment/rec_main.html` | HTML | 14 |
| `templates/cbv/recruitment/recruitment.html` | HTML | 301 |
| `templates/cbv/recruitment/recruitment_col.html` | HTML | 15 |
| `templates/cbv/recruitment/recruitment_form.html` | HTML | 18 |
| `templates/cbv/recruitment/total_hires.html` | HTML | 4 |
| `templates/cbv/recruitment_settings/recruitment_settings_main.html` | HTML | 10 |
| `templates/cbv/recruitment_settings/reject_reason_tab.html` | HTML | 23 |
| `templates/cbv/recruitment_settings/skill_tab.html` | HTML | 23 |
| `templates/cbv/recruitment_settings/stage_tab.html` | HTML | 23 |
| `templates/cbv/recruitment_survey/filter.html` | HTML | 39 |
| `templates/cbv/recruitment_survey/option_col.html` | HTML | 6 |
| `templates/cbv/recruitment_survey/survey_card.html` | HTML | 182 |
| `templates/cbv/recruitment_survey/survey_form.html` | HTML | 81 |
| `templates/cbv/recruitment_survey_template/filter.html` | HTML | 27 |
| `templates/cbv/recruitment_survey_template/recruitment_survey_template_view.html` | HTML | 17 |
| `templates/cbv/recruitment_survey_template/template_accordion.html` | HTML | 306 |
| `templates/cbv/stages/actions.html` | HTML | 44 |
| `templates/cbv/stages/detail_action.html` | HTML | 33 |
| `templates/cbv/stages/filter.html` | HTML | 97 |
| `templates/cbv/stages/managers.html` | HTML | 31 |
| `templates/cbv/stages/stage_main.html` | HTML | 4 |
| `templates/cbv/stages/stages.html` | HTML | 95 |
| `templates/cbv/stages/title.html` | HTML | 18 |
| `templates/linkedin/linkedin_action.html` | HTML | 35 |
| `templates/pipeline/bulk_resume.html` | HTML | 65 |
| `templates/pipeline/components/candidate_stage_component.html` | HTML | 496 |
| `templates/pipeline/components/pipeline_search_components.html` | HTML | 130 |
| `templates/pipeline/components/stages_tab_content.html` | HTML | 88 |
| `templates/pipeline/filters.html` | HTML | 162 |
| `templates/pipeline/footer_components.html` | HTML | 100 |
| `templates/pipeline/form/candidate_form.html` | HTML | 3 |
| `templates/pipeline/form/recruitment_drop_down_form.html` | HTML | 0 |
| `templates/pipeline/form/recruitment_update.html` | HTML | 184 |
| `templates/pipeline/form/stage_update.html` | HTML | 54 |
| `templates/pipeline/kanban_components/candidate_kanban_components.html` | HTML | 274 |
| `templates/pipeline/kanban_components/kanban.html` | HTML | 73 |
| `templates/pipeline/kanban_components/kanban_stage_components.html` | HTML | 141 |
| `templates/pipeline/matching_resumes.html` | HTML | 42 |
| `templates/pipeline/nav.html` | HTML | 511 |
| `templates/pipeline/pipeline.html` | HTML | 227 |
| `templates/pipeline/pipeline_card.html` | HTML | 433 |
| `templates/pipeline/pipeline_components/add_note.html` | HTML | 13 |
| `templates/pipeline/pipeline_components/candidate_remark_view.html` | HTML | 47 |
| `templates/pipeline/pipeline_components/schedule_interview.html` | HTML | 83 |
| `templates/pipeline/pipeline_components/schedule_interview_update.html` | HTML | 50 |
| `templates/pipeline/pipeline_components/send_mail.html` | HTML | 271 |
| `templates/pipeline/pipeline_components/update_note.html` | HTML | 30 |
| `templates/pipeline/pipeline_components/update_note_individual.html` | HTML | 29 |
| `templates/pipeline/pipeline_components/view_note.html` | HTML | 199 |
| `templates/pipeline/pipeline_empty.html` | HTML | 97 |
| `templates/pipeline/pipeline_tabs.html` | HTML | 95 |
| `templates/rating_input.html` | HTML | 69 |
| `templates/recruitment/dashboard.html` | HTML | 1,908 |
| `templates/recruitment/filters.html` | HTML | 61 |
| `templates/recruitment/mail_templates/offer_letter.html` | HTML | 103 |
| `templates/recruitment/nav.html` | HTML | 84 |
| `templates/recruitment/open_recruitments.html` | HTML | 174 |
| `templates/recruitment/recruitment_component.html` | HTML | 319 |
| `templates/recruitment/recruitment_details.html` | HTML | 15 |
| `templates/recruitment/recruitment_empty.html` | HTML | 49 |
| `templates/recruitment/recruitment_form.html` | HTML | 227 |
| `templates/recruitment/recruitment_update_form.html` | HTML | 203 |
| `templates/recruitment/recruitment_view.html` | HTML | 46 |
| `templates/recruitment/settings/settings.html` | HTML | 46 |
| `templates/select2.js` | JS | 2 |
| `templates/settings/linkedin/linkedin_setting_section.html` | HTML | 60 |
| `templates/settings/reject_reason_form.html` | HTML | 7 |
| `templates/settings/reject_reason_lines.html` | HTML | 50 |
| `templates/settings/reject_reasons.html` | HTML | 52 |
| `templates/settings/skills/skills_form.html` | HTML | 30 |
| `templates/settings/skills/skills_list.html` | HTML | 50 |
| `templates/settings/skills/skills_view.html` | HTML | 51 |
| `templates/skill_zone/candidate_profile_tab.html` | HTML | 12 |
| `templates/skill_zone/empty_skill_zone.html` | HTML | 44 |
| `templates/skill_zone/skill_zone_card.html` | HTML | 144 |
| `templates/skill_zone/skill_zone_form.html` | HTML | 42 |
| `templates/skill_zone/skill_zone_list.html` | HTML | 347 |
| `templates/skill_zone/skill_zone_nav.html` | HTML | 198 |
| `templates/skill_zone/skill_zone_view.html` | HTML | 61 |
| `templates/skill_zone_cand/skill_zone_cand_card.html` | HTML | 138 |
| `templates/skill_zone_cand/skill_zone_cand_form.html` | HTML | 19 |
| `templates/skill_zone_cand/skill_zone_cand_list.html` | HTML | 88 |
| `templates/skill_zone_cand/skill_zone_cand_nav.html` | HTML | 201 |
| `templates/skill_zone_cand/skill_zone_cand_view.html` | HTML | 26 |
| `templates/skill_zone_cand/to_skill_zone_form.html` | HTML | 12 |
| `templates/stage/filters.html` | HTML | 44 |
| `templates/stage/nav.html` | HTML | 75 |
| `templates/stage/stage_component.html` | HTML | 276 |
| `templates/stage/stage_empty.html` | HTML | 42 |
| `templates/stage/stage_form.html` | HTML | 53 |
| `templates/stage/stage_group.html` | HTML | 209 |
| `templates/stage/stage_update_form.html` | HTML | 61 |
| `templates/stage/stage_view.html` | HTML | 20 |
| `templates/survey/add_form.html` | HTML | 63 |
| `templates/survey/add_more_options.html` | HTML | 30 |
| `templates/survey/candidate_survey_form.html` | HTML | 157 |
| `templates/survey/filter.html` | HTML | 43 |
| `templates/survey/form.html` | HTML | 1 |
| `templates/survey/main_form.html` | HTML | 24 |
| `templates/survey/question_template_organized_form.html` | HTML | 91 |
| `templates/survey/survey_card.html` | HTML | 174 |
| `templates/survey/survey_preview.html` | HTML | 30 |
| `templates/survey/survey_preview_container.html` | HTML | 22 |
| `templates/survey/template_accordion.html` | HTML | 319 |
| `templates/survey/template_form.html` | HTML | 30 |
| `templates/survey/template_update_form.html` | HTML | 30 |
| `templates/survey/templates.html` | HTML | 141 |
| `templates/survey/view_question_templates.html` | HTML | 208 |
| `templates/survey/view_single_template.html` | HTML | 113 |
| `templates/survey_form.html` | HTML | 191 |
| `templates/survey_preview_form.html` | HTML | 340 |
| `templatetags/__init__.py` | Python | 0 |
| `templatetags/migrations/__init__.py` | Migration | 0 |
| `templatetags/recruitmentfilters.py` | Python | 223 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_candidate_export_authz.py` | Test | 57 |
| `tests/test_candidate_note_idor.py` | Test | 147 |
| `tests/test_candidate_stage.py` | Test | 68 |
| `tests/test_document_idor.py` | Test | 129 |
| `tests/test_manager_helpers.py` | Test | 77 |
| `tests/test_resume_scoping.py` | Test | 79 |
| `tests/test_survey_attachment_extension.py` | Test | 86 |
| `urls.py` | Python | 1,221 |
| `views.py` | Python | 1,367 |
| `views/__init__.py` | Python | 0 |
| `views/actions.py` | Python | 582 |
| `views/dashboard.py` | Python | 407 |
| `views/linkedin.py` | Python | 159 |
| `views/mail_templates.py` | Python | 15 |
| `views/paginator_qry.py` | Python | 18 |
| `views/search.py` | Python | 269 |
| `views/surveys.py` | Python | 778 |
| `views/views.py` | Python | 4,569 |
| `widgets.py` | Python | 37 |

</details>

### report

**75 files, 21,803 lines**.

<details>
<summary>Show all 75 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `access.py` | Python | 173 |
| `admin.py` | Python | 82 |
| `apps.py` | Python | 28 |
| `async_export.py` | Python | 169 |
| `cbv/__init__.py` | Python | 0 |
| `cbv/audit.py` | Python | 67 |
| `cbv/subscriptions.py` | Python | 336 |
| `chart_render.py` | Python | 260 |
| `company_context.py` | Python | 124 |
| `compare.py` | Python | 259 |
| `delivery.py` | Python | 334 |
| `drilldown.py` | Python | 105 |
| `dynamic_filter_utils.py` | Python | 82 |
| `engine.py` | Python | 496 |
| `export.py` | Python | 1,423 |
| `filter_schema.py` | Python | 438 |
| `filters.py` | Python | 22 |
| `forms.py` | Python | 144 |
| `formulas.py` | Python | 48 |
| `management/__init__.py` | Python | 0 |
| `management/commands/__init__.py` | Python | 0 |
| `management/commands/run_report_subscriptions.py` | Python | 33 |
| `management/commands/seed_standard_report_templates.py` | Python | 264 |
| `metrics/__init__.py` | Python | 3 |
| `metrics/_calendar.py` | Python | 136 |
| `metrics/_exits.py` | Python | 287 |
| `metrics/_privacy.py` | Python | 23 |
| `metrics/compliance.py` | Python | 551 |
| `metrics/definitions.py` | Python | 685 |
| `metrics/packs.py` | Python | 625 |
| `metrics/payroll.py` | Python | 940 |
| `metrics/talent.py` | Python | 853 |
| `metrics/time_leave.py` | Python | 1,005 |
| `metrics/workforce.py` | Python | 1,370 |
| `migrations/0001_initial.py` | Migration | 36 |
| `migrations/0002_reporttemplate_is_standard_reporttemplate_visibility_and_more.py` | Migration | 155 |
| `migrations/0003_remove_reportsubscription_recipients_and_more.py` | Migration | 30 |
| `migrations/0004_alter_reportaccess_is_active_and_more.py` | Migration | 48 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 463 |
| `narrative.py` | Python | 61 |
| `personalization.py` | Python | 219 |
| `pivot_limits.py` | Python | 41 |
| `registry.py` | Python | 224 |
| `scheduler.py` | Python | 40 |
| `sidebar.py` | Python | 73 |
| `static/report/css/pivot_explorer.css` | CSS | 632 |
| `static/report/js/pivot_safety.js` | JS | 123 |
| `templates/cbv/audit/audit_filter.html` | HTML | 30 |
| `templates/cbv/audit/audit_home.html` | HTML | 16 |
| `templates/cbv/audit/audit_panel.html` | HTML | 10 |
| `templates/cbv/subscriptions/subscription_form.html` | HTML | 18 |
| `templates/cbv/subscriptions/subscriptions_home.html` | HTML | 27 |
| `templates/cbv/subscriptions/subscriptions_panel.html` | HTML | 21 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_access_helpers.py` | Test | 73 |
| `tests/test_dynamic_filter_utils.py` | Test | 25 |
| `tests/test_report_execution.py` | Test | 1,486 |
| `tests/test_standard_reports.py` | Test | 1,221 |
| `urls.py` | Python | 341 |
| `views.py` | Python | 3 |
| `views/__init__.py` | Python | 25 |
| `views/asset_report.py` | Python | 373 |
| `views/attendance_report.py` | Python | 501 |
| `views/employee_report.py` | Python | 357 |
| `views/explorer.py` | Python | 90 |
| `views/leave_report.py` | Python | 554 |
| `views/payroll_report.py` | Python | 671 |
| `views/pms_report.py` | Python | 659 |
| `views/recruitment_report.py` | Python | 583 |
| `views/report_templates.py` | Python | 140 |
| `views/saved_views.py` | Python | 98 |
| `views/standard_reports.py` | Python | 878 |
| `views/subscriptions.py` | Python | 93 |

</details>

### whatsapp

**22 files, 3,459 lines**.

<details>
<summary>Show all 22 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 0 |
| `admin.py` | Python | 7 |
| `apps.py` | Python | 16 |
| `cbv/whatsapp.py` | Python | 201 |
| `filters.py` | Python | 14 |
| `flows.py` | Python | 884 |
| `forms.py` | Python | 47 |
| `migrations/0001_initial.py` | Migration | 110 |
| `migrations/0002_whatsappcredientials_meta_app_secret.py` | Migration | 18 |
| `migrations/0003_alter_whatsappcredientials_is_active.py` | Migration | 18 |
| `migrations/__init__.py` | Migration | 0 |
| `models.py` | Python | 126 |
| `templates/whatsapp/credentials_view.html` | HTML | 75 |
| `templates/whatsapp/option_buttons.html` | HTML | 33 |
| `templates/whatsapp/send_test_message_form.html` | HTML | 39 |
| `templates/whatsapp/whatsapp_animation.html` | HTML | 91 |
| `test_webhook_signature.py` | Test | 122 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_meta_url.py` | Test | 13 |
| `urls.py` | Python | 52 |
| `utils.py` | Python | 1,016 |
| `views.py` | Python | 577 |

</details>

### Shared folders

### horilla

Project core: settings, URLs, middleware, testkit, scheduling: **48 files, 5,843 lines**.

<details>
<summary>Show all 48 files</summary>

| File | Type | Lines |
|---|---|---:|
| `__init__.py` | Python | 26 |
| `__version__.py` | Python | 16 |
| `asgi.py` | Python | 16 |
| `backends.py` | Python | 88 |
| `config.py` | Python | 139 |
| `decorators.py` | Python | 539 |
| `export_safety.py` | Python | 57 |
| `filters.py` | Python | 516 |
| `group_by.py` | Python | 220 |
| `horilla_backends.py` | Python | 24 |
| `horilla_backends_gcp.py` | Python | 23 |
| `horilla_middlewares.py` | Python | 178 |
| `http/__init__.py` | Python | 1 |
| `http/response.py` | Python | 60 |
| `inherit/__init__.py` | Python | 25 |
| `inherit/autodetect.py` | Python | 56 |
| `inherit/extension_registry.py` | Python | 13 |
| `inherit/migration_ops.py` | Python | 224 |
| `inherit/model_inherit.py` | Python | 146 |
| `inherit/view_inherit.py` | Python | 81 |
| `inherit/view_registry.py` | Python | 90 |
| `menu/__init__.py` | Python | 21 |
| `menu/registry.py` | Python | 89 |
| `menu/settings_menu.py` | Python | 119 |
| `methods.py` | Python | 137 |
| `models.py` | Python | 282 |
| `nested_group_by.py` | Python | 181 |
| `observability.py` | Python | 343 |
| `scheduling.py` | Python | 83 |
| `settings/__init__.py` | Python | 13 |
| `settings/addons.py` | Python | 32 |
| `settings/base.py` | Python | 701 |
| `settings/local_settings.py` | Python | 20 |
| `settings/security.py` | Python | 91 |
| `signals.py` | Python | 20 |
| `storage_backends.py` | Python | 21 |
| `testkit/__init__.py` | Python | 16 |
| `testkit/company.py` | Python | 31 |
| `testkit/factories.py` | Python | 344 |
| `tests/__init__.py` | Test | 0 |
| `tests/test_filterset_dict_data.py` | Test | 74 |
| `tests/test_has_xss_bypass.py` | Test | 107 |
| `tests/test_no_template_tags_in_comments.py` | Test | 208 |
| `tests/test_startup_diagnostics_ascii.py` | Test | 68 |
| `tests/test_version_exposed.py` | Test | 45 |
| `tests/test_xss_validation_on_save.py` | Test | 74 |
| `urls.py` | Python | 169 |
| `wsgi.py` | Python | 16 |

</details>

### templates

Site-wide templates: **40 files, 9,809 lines**.

<details>
<summary>Show all 40 files</summary>

| File | Type | Lines |
|---|---|---:|
| `403.html` | HTML | 157 |
| `404.html` | HTML | 275 |
| `405.html` | HTML | 151 |
| `animation.html` | HTML | 202 |
| `compensatory_settings.html` | HTML | 34 |
| `components/legend_prefs.html` | HTML | 69 |
| `components/pie_legend.html` | HTML | 297 |
| `dashboard.html` | HTML | 4,083 |
| `dashboard_chart_form.html` | HTML | 89 |
| `decorator_404.html` | HTML | 5 |
| `demo_database/animation_load_data.html` | HTML | 145 |
| `demo_database/auth_load_data.html` | HTML | 78 |
| `filter_country.js` | JS | 331 |
| `filter_tags.html` | HTML | 86 |
| `floating_button.html` | HTML | 281 |
| `forgot_password.html` | HTML | 80 |
| `import_popup.html` | HTML | 70 |
| `index.html` | HTML | 339 |
| `initialize_database/horilla_company.html` | HTML | 92 |
| `initialize_database/horilla_department.html` | HTML | 26 |
| `initialize_database/horilla_department_form.html` | HTML | 62 |
| `initialize_database/horilla_job_position.html` | HTML | 26 |
| `initialize_database/horilla_job_position_form.html` | HTML | 70 |
| `initialize_database/horilla_user.html` | HTML | 145 |
| `initialize_database/horilla_user_signup.html` | HTML | 233 |
| `is_active_toggle.html` | HTML | 12 |
| `login.html` | HTML | 177 |
| `navbar.html` | HTML | 161 |
| `no_perm.html` | HTML | 53 |
| `normal_form.html` | HTML | 47 |
| `notification/all_notifications.html` | HTML | 72 |
| `notification/notification.html` | HTML | 104 |
| `notification/notification_items.html` | HTML | 202 |
| `reset_password.html` | HTML | 117 |
| `reset_send.html` | HTML | 117 |
| `select2.js` | JS | 2 |
| `settings.html` | HTML | 814 |
| `sidebar.html` | HTML | 395 |
| `went_wrong.html` | HTML | 1 |
| `work_info_complete.html` | HTML | 109 |

</details>

### static

Site-wide static assets, mostly third-party libraries: **290 files, 244,799 lines** (plus 21 minified files, 52,309 lines, not in the total).

<details>
<summary>Show all 311 files</summary>

| File | Type | Lines |
|---|---|---:|
| `attendance/customizations.js` | JS | 10 |
| `auth/forgot-password.html` | HTML | 44 |
| `auth/login.html` | HTML | 70 |
| `auth/reset.html` | HTML | 91 |
| `bootstrap/bootsrtap.min.js` | Minified | 7 |
| `bootstrap/bootstrap.min.css` | Minified | 7 |
| `build/css/bootstrap.min.css` | Minified | 6 |
| `build/css/driver.min.css` | Minified | 288 |
| `build/css/orgChart.css` | CSS | 928 |
| `build/css/pivottable.min.css` | Minified | 1 |
| `build/css/style.min.css` | Minified | 16,637 |
| `build/css/styleWidget.css` | CSS | 21 |
| `build/css/summernote-lite.min.css` | Minified | 1 |
| `build/css/sweetalert2.min.css` | Minified | 1,559 |
| `build/js/allowanceWidget.js` | JS | 282 |
| `build/js/clearFilter.js` | JS | 117 |
| `build/js/dashboardDriver.js` | JS | 73 |
| `build/js/deductionWidget.js` | JS | 257 |
| `build/js/driver.js` | JS | 2 |
| `build/js/htmxSelect2.js` | JS | 4,246 |
| `build/js/jquery.min.js` | Minified | 2 |
| `build/js/moment.js` | JS | 1 |
| `build/js/orgChart.js` | JS | 1,686 |
| `build/js/pipelineDriver.js` | JS | 48 |
| `build/js/pivottable.min.js` | Minified | 2 |
| `build/js/pivottable_excel.min.js` | Minified | 45 |
| `build/js/pivottable_plot.min.js` | Minified | 8 |
| `build/js/pivottable_ploty.min.js` | Minified | 2 |
| `build/js/settingsDriver.js` | JS | 47 |
| `build/js/styleWidget.js` | JS | 2 |
| `build/js/summernote-lite.min.js` | Minified | 158 |
| `build/js/sweetAlert.js` | JS | 2,644 |
| `build/js/tourController.js` | JS | 272 |
| `build/js/vendor/jspdf.plugin.autotable.min.js` | Minified | 10 |
| `build/js/vendor/jspdf.umd.min.js` | Minified | 398 |
| `build/js/web.frontend.js` | JS | 27,609 |
| `build/js/web.frontend.min.js` | Minified | 28,013 |
| `build/vendor/ionicons/@stencil/core/cli/index.js` | JS | 2,583 |
| `build/vendor/ionicons/@stencil/core/compiler/stencil.js` | JS | 70,673 |
| `build/vendor/ionicons/@stencil/core/compiler/stencil.min.js` | Minified | 4 |
| `build/vendor/ionicons/@stencil/core/dev-server/client/index.js` | JS | 808 |
| `build/vendor/ionicons/@stencil/core/dev-server/connector.html` | HTML | 6 |
| `build/vendor/ionicons/@stencil/core/dev-server/index.js` | JS | 264 |
| `build/vendor/ionicons/@stencil/core/dev-server/open-in-editor-api.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/dev-server/server-process.js` | JS | 1,799 |
| `build/vendor/ionicons/@stencil/core/dev-server/server-worker-thread.js` | JS | 39 |
| `build/vendor/ionicons/@stencil/core/dev-server/templates/directory-index.html` | HTML | 132 |
| `build/vendor/ionicons/@stencil/core/dev-server/templates/initial-load.html` | HTML | 160 |
| `build/vendor/ionicons/@stencil/core/dev-server/ws.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/internal/app-data/index.js` | JS | 88 |
| `build/vendor/ionicons/@stencil/core/internal/client/css-shim.js` | JS | 4 |
| `build/vendor/ionicons/@stencil/core/internal/client/dom.js` | JS | 73 |
| `build/vendor/ionicons/@stencil/core/internal/client/index.js` | JS | 3,371 |
| `build/vendor/ionicons/@stencil/core/internal/client/patch-browser.js` | JS | 142 |
| `build/vendor/ionicons/@stencil/core/internal/client/patch-esm.js` | JS | 23 |
| `build/vendor/ionicons/@stencil/core/internal/client/polyfills/core-js.js` | JS | 11 |
| `build/vendor/ionicons/@stencil/core/internal/client/polyfills/css-shim.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/internal/client/polyfills/dom.js` | JS | 79 |
| `build/vendor/ionicons/@stencil/core/internal/client/polyfills/es5-html-element.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/internal/client/polyfills/index.js` | JS | 34 |
| `build/vendor/ionicons/@stencil/core/internal/client/polyfills/system.js` | JS | 6 |
| `build/vendor/ionicons/@stencil/core/internal/client/shadow-css.js` | JS | 387 |
| `build/vendor/ionicons/@stencil/core/internal/hydrate/index.js` | JS | 1,143 |
| `build/vendor/ionicons/@stencil/core/internal/hydrate/runner.js` | JS | 777 |
| `build/vendor/ionicons/@stencil/core/internal/hydrate/shadow-css.js` | JS | 143 |
| `build/vendor/ionicons/@stencil/core/internal/index.js` | JS | 2 |
| `build/vendor/ionicons/@stencil/core/internal/stencil-core/index.js` | JS | 16 |
| `build/vendor/ionicons/@stencil/core/internal/testing/index.js` | JS | 1,105 |
| `build/vendor/ionicons/@stencil/core/internal/testing/shadow-css.js` | JS | 143 |
| `build/vendor/ionicons/@stencil/core/mock-doc/index.js` | JS | 4,822 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/app.css` | CSS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/app.esm.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/app.js` | JS | 33 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/index.esm.js` | JS | 0 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/p-081b0641.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/p-227a1e18.entry.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/p-2c298727.entry.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/p-5479268c.entry.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/p-573ec8a4.entry.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/p-6ba08604.entry.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/p-6bc63295.entry.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/p-7a3759fd.entry.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/p-7b4e3ba7.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/p-988eb362.css` | CSS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/p-9b6a9315.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/p-b4cc611c.entry.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/p-d1bf53f5.entry.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/p-e2efe0df.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/p-e8ca6d97.entry.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/p-ec2f13e0.entry.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/p-f0b99977.entry.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/p-f4745c2f.entry.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/build/p-fbbae598.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/compare/index.html` | HTML | 1 |
| `build/vendor/ionicons/@stencil/core/screenshot/connector.js` | JS | 2 |
| `build/vendor/ionicons/@stencil/core/screenshot/index.js` | JS | 661 |
| `build/vendor/ionicons/@stencil/core/screenshot/local-connector.js` | JS | 2 |
| `build/vendor/ionicons/@stencil/core/screenshot/pixel-match.js` | JS | 2,807 |
| `build/vendor/ionicons/@stencil/core/sys/node/autoprefixer.js` | JS | 8 |
| `build/vendor/ionicons/@stencil/core/sys/node/glob.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/sys/node/graceful-fs.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/sys/node/index.js` | JS | 6,124 |
| `build/vendor/ionicons/@stencil/core/sys/node/node-fetch.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/sys/node/prompts.js` | JS | 1 |
| `build/vendor/ionicons/@stencil/core/sys/node/worker.js` | JS | 52 |
| `build/vendor/ionicons/@stencil/core/testing/index.js` | JS | 4,155 |
| `build/vendor/ionicons/@stencil/core/testing/jest-environment.js` | JS | 3 |
| `build/vendor/ionicons/@stencil/core/testing/jest-preprocessor.js` | JS | 3 |
| `build/vendor/ionicons/@stencil/core/testing/jest-preset.js` | JS | 37 |
| `build/vendor/ionicons/@stencil/core/testing/jest-runner.js` | JS | 3 |
| `build/vendor/ionicons/@stencil/core/testing/jest-setuptestframework.js` | JS | 3 |
| `css/style.css` | CSS | 1,043 |
| `htmx/htmx.min.js` | Minified | 5,154 |
| `images/ionicons/icons/index.js` | JS | 1,358 |
| `images/ionicons/ui_icons/cjs/index-4b66db81.js` | JS | 1,716 |
| `images/ionicons/ui_icons/cjs/index.cjs.js` | JS | 11 |
| `images/ionicons/ui_icons/cjs/ion-icon.cjs.entry.js` | JS | 223 |
| `images/ionicons/ui_icons/cjs/ionicons.cjs.js` | JS | 23 |
| `images/ionicons/ui_icons/cjs/loader.cjs.js` | JS | 13 |
| `images/ionicons/ui_icons/cjs/utils-b413c9c0.js` | JS | 175 |
| `images/ionicons/ui_icons/collection/components/icon/icon.css` | CSS | 144 |
| `images/ionicons/ui_icons/collection/components/icon/icon.js` | JS | 341 |
| `images/ionicons/ui_icons/collection/components/icon/request.js` | JS | 53 |
| `images/ionicons/ui_icons/collection/components/icon/test/icon.e2e.js` | JS | 52 |
| `images/ionicons/ui_icons/collection/components/icon/test/icon.spec.js` | JS | 69 |
| `images/ionicons/ui_icons/collection/components/icon/test/utils.spec.js` | JS | 115 |
| `images/ionicons/ui_icons/collection/components/icon/test/validate.spec.js` | JS | 61 |
| `images/ionicons/ui_icons/collection/components/icon/utils.js` | JS | 165 |
| `images/ionicons/ui_icons/collection/components/icon/validate.js` | JS | 45 |
| `images/ionicons/ui_icons/collection/index.js` | JS | 2 |
| `images/ionicons/ui_icons/collection/utils/test/playwright/index.js` | JS | 2 |
| `images/ionicons/ui_icons/collection/utils/test/playwright/page/utils/goto.js` | JS | 14 |
| `images/ionicons/ui_icons/collection/utils/test/playwright/page/utils/index.js` | JS | 1 |
| `images/ionicons/ui_icons/collection/utils/test/playwright/playwright-declarations.js` | JS | 1 |
| `images/ionicons/ui_icons/collection/utils/test/playwright/playwright-page.js` | JS | 31 |
| `images/ionicons/ui_icons/esm-es5/index-b72adede.js` | JS | 2 |
| `images/ionicons/ui_icons/esm-es5/index.js` | JS | 1 |
| `images/ionicons/ui_icons/esm-es5/ion-icon.entry.js` | JS | 1 |
| `images/ionicons/ui_icons/esm-es5/ionicons.js` | JS | 1 |
| `images/ionicons/ui_icons/esm-es5/loader.js` | JS | 1 |
| `images/ionicons/ui_icons/esm-es5/utils-2c56d1c8.js` | JS | 1 |
| `images/ionicons/ui_icons/esm/index-b72adede.js` | JS | 1,686 |
| `images/ionicons/ui_icons/esm/index.js` | JS | 2 |
| `images/ionicons/ui_icons/esm/ion-icon.entry.js` | JS | 219 |
| `images/ionicons/ui_icons/esm/ionicons.js` | JS | 18 |
| `images/ionicons/ui_icons/esm/loader.js` | JS | 9 |
| `images/ionicons/ui_icons/esm/polyfills/core-js.js` | JS | 11 |
| `images/ionicons/ui_icons/esm/polyfills/dom.js` | JS | 79 |
| `images/ionicons/ui_icons/esm/polyfills/es5-html-element.js` | JS | 1 |
| `images/ionicons/ui_icons/esm/polyfills/index.js` | JS | 34 |
| `images/ionicons/ui_icons/esm/polyfills/system.js` | JS | 6 |
| `images/ionicons/ui_icons/esm/utils-2c56d1c8.js` | JS | 168 |
| `images/ionicons/ui_icons/index.cjs.js` | JS | 1 |
| `images/ionicons/ui_icons/index.js` | JS | 1 |
| `images/ionicons/ui_icons/ionicons.js` | JS | 30 |
| `images/ionicons/ui_icons/ionicons/index.esm.js` | JS | 1 |
| `images/ionicons/ui_icons/ionicons/ionicons.esm.js` | JS | 1 |
| `images/ionicons/ui_icons/ionicons/ionicons.js` | JS | 127 |
| `images/ionicons/ui_icons/ionicons/p-006dba1a.js` | JS | 1 |
| `images/ionicons/ui_icons/ionicons/p-41a81ee2.system.entry.js` | JS | 1 |
| `images/ionicons/ui_icons/ionicons/p-5f68589a.system.js` | JS | 1 |
| `images/ionicons/ui_icons/ionicons/p-621fab66.system.js` | JS | 1 |
| `images/ionicons/ui_icons/ionicons/p-748a23b9.entry.js` | JS | 1 |
| `images/ionicons/ui_icons/ionicons/p-8f10164f.system.js` | JS | 1 |
| `images/ionicons/ui_icons/ionicons/p-e298ede3.js` | JS | 2 |
| `images/ionicons/ui_icons/ionicons/p-e7ae1e74.system.js` | JS | 2 |
| `images/ionicons/ui_icons/loader/cdn.js` | JS | 3 |
| `images/ionicons/ui_icons/loader/index.cjs.js` | JS | 3 |
| `images/ionicons/ui_icons/loader/index.es2017.js` | JS | 3 |
| `images/ionicons/ui_icons/loader/index.js` | JS | 4 |
| `index/country.js` | JS | 778 |
| `index/index.js` | JS | 2,333 |
| `index/saveFilters.js` | JS | 118 |
| `jquery/ajax.js` | JS | 10,909 |
| `jquery/alpine.min.js` | Minified | 5 |
| `jquery/jquery.min.js` | Minified | 2 |
| `jquery/jqueryui.css` | CSS | 1,314 |
| `jquery/jqueryui.js` | JS | 19,062 |
| `pipeline/pipeline.js` | JS | 149 |
| `proper/proper.js` | JS | 5 |
| `recruitment/candidate.js` | JS | 48 |
| `recruitment/recruitment.js` | JS | 139 |
| `src/css/main.css` | CSS | 17,364 |
| `src/js/componentForm.js` | JS | 531 |
| `src/js/customFooterScripts.js` | JS | 0 |
| `src/js/customHeaderScripts.js` | JS | 0 |
| `src/js/index.js` | JS | 49 |
| `src/js/modules/dashboard/Calendar.js` | JS | 65 |
| `src/js/modules/dashboard/Chat.js` | JS | 40 |
| `src/js/modules/dashboard/Dashboard.js` | JS | 105 |
| `src/js/modules/dashboard/Faq.js` | JS | 31 |
| `src/js/modules/dashboard/Generic.js` | JS | 333 |
| `src/js/modules/dashboard/Helpdesk.js` | JS | 25 |
| `src/js/modules/dashboard/ImageSelect.js` | JS | 72 |
| `src/js/modules/dashboard/ImageUpload.js` | JS | 47 |
| `src/js/modules/dashboard/Inputs.js` | JS | 213 |
| `src/js/modules/dashboard/Kanban.js` | JS | 514 |
| `src/js/modules/dashboard/LoadLayout.js` | JS | 26 |
| `src/js/modules/dashboard/ModalDialog.js` | JS | 62 |
| `src/js/modules/dashboard/OrgChart.js` | JS | 31 |
| `src/js/modules/dashboard/Recruitment.js` | JS | 32 |
| `src/js/modules/dashboard/ResizeInput.js` | JS | 36 |
| `src/js/modules/dashboard/Specifics.js` | JS | 49 |
| `src/js/modules/dashboard/Tables.js` | JS | 220 |
| `src/js/modules/dashboard/Tabs.js` | JS | 506 |
| `src/js/modules/dashboard/Tooltip.js` | JS | 26 |
| `src/js/modules/dashboard/WorkEntry.js` | JS | 207 |
| `src/js/modules/vendors/niceSelect.js` | JS | 262 |
| `src/scss/abstracts/_functions.scss` | CSS | 30 |
| `src/scss/abstracts/_mixins.scss` | CSS | 92 |
| `src/scss/abstracts/_variables.scss` | CSS | 254 |
| `src/scss/base/_base.scss` | CSS | 113 |
| `src/scss/base/_fonts.scss` | CSS | 185 |
| `src/scss/base/_helpers.scss` | CSS | 95 |
| `src/scss/base/_typography.scss` | CSS | 7 |
| `src/scss/components/_accordion.scss` | CSS | 171 |
| `src/scss/components/_alert.scss` | CSS | 77 |
| `src/scss/components/_badges.scss` | CSS | 87 |
| `src/scss/components/_button.scss` | CSS | 575 |
| `src/scss/components/_card.scss` | CSS | 251 |
| `src/scss/components/_dropdown.scss` | CSS | 151 |
| `src/scss/components/_hands.scss` | CSS | 4 |
| `src/scss/components/_input.scss` | CSS | 615 |
| `src/scss/components/_kanban.scss` | CSS | 283 |
| `src/scss/components/_modal-custom.scss` | CSS | 175 |
| `src/scss/components/_modal.scss` | CSS | 104 |
| `src/scss/components/_pagination.scss` | CSS | 94 |
| `src/scss/components/_profile.scss` | CSS | 165 |
| `src/scss/components/_progress.scss` | CSS | 38 |
| `src/scss/components/_sidebar.scss` | CSS | 424 |
| `src/scss/components/_table.scss` | CSS | 1,497 |
| `src/scss/components/_tabs.scss` | CSS | 318 |
| `src/scss/components/_tag.scss` | CSS | 114 |
| `src/scss/components/_timeoff.scss` | CSS | 192 |
| `src/scss/components/_tooltip.scss` | CSS | 9 |
| `src/scss/layout/_footer.scss` | CSS | 3 |
| `src/scss/layout/_general.scss` | CSS | 120 |
| `src/scss/layout/_header.scss` | CSS | 439 |
| `src/scss/main.css` | CSS | 14,944 |
| `src/scss/main.scss` | CSS | 35 |
| `src/scss/overrides/_datepicker.scss` | CSS | 102 |
| `src/scss/overrides/_fullcalendar.scss` | CSS | 33 |
| `src/scss/overrides/_responsive.scss` | CSS | 70 |
| `src/scss/overrides/_summernote.scss` | CSS | 7 |
| `src/scss/pages/_404.scss` | CSS | 36 |
| `src/scss/pages/_announcement.scss` | CSS | 90 |
| `src/scss/pages/_auth.scss` | CSS | 26 |
| `src/scss/pages/_chat.scss` | CSS | 765 |
| `src/scss/pages/_dashboard.scss` | CSS | 602 |
| `src/scss/pages/_faq.scss` | CSS | 259 |
| `src/scss/pages/_feedback.scss` | CSS | 25 |
| `src/scss/pages/_helpdesk.scss` | CSS | 527 |
| `src/scss/pages/_joblist.scss` | CSS | 176 |
| `src/scss/pages/_onboarding.scss` | CSS | 269 |
| `src/scss/pages/_payslip.scss` | CSS | 176 |
| `src/scss/pages/_profile.scss` | CSS | 415 |
| `src/scss/pages/_survey.scss` | CSS | 105 |
| `src/scss/pages/_workentry.scss` | CSS | 46 |
| `src/scss/themes/_default.scss` | CSS | 4 |
| `src/scss/vendors/_normalize.scss` | CSS | 349 |
| `src/scss/vendors/_orgchart.scss` | CSS | 754 |
| `src/scss/vendors/bootstrap/_bootstrap.scss` | CSS | 52 |
| `src/scss/vendors/bootstrap/_containers.scss` | CSS | 41 |
| `src/scss/vendors/bootstrap/_functions.scss` | CSS | 263 |
| `src/scss/vendors/bootstrap/_grid.scss` | CSS | 22 |
| `src/scss/vendors/bootstrap/_helpers.scss` | CSS | 7 |
| `src/scss/vendors/bootstrap/_mixins.scss` | CSS | 42 |
| `src/scss/vendors/bootstrap/_reboot.scss` | CSS | 621 |
| `src/scss/vendors/bootstrap/_root.scss` | CSS | 16 |
| `src/scss/vendors/bootstrap/_type.scss` | CSS | 104 |
| `src/scss/vendors/bootstrap/_utilities.scss` | CSS | 594 |
| `src/scss/vendors/bootstrap/_variables.scss` | CSS | 1,468 |
| `src/scss/vendors/bootstrap/bootstrap-grid.css` | CSS | 4,061 |
| `src/scss/vendors/bootstrap/bootstrap-grid.scss` | CSS | 65 |
| `src/scss/vendors/bootstrap/bootstrap-reboot.css` | CSS | 424 |
| `src/scss/vendors/bootstrap/bootstrap-reboot.scss` | CSS | 15 |
| `src/scss/vendors/bootstrap/bootstrap-utilities.css` | CSS | 3,956 |
| `src/scss/vendors/bootstrap/bootstrap-utilities.scss` | CSS | 18 |
| `src/scss/vendors/bootstrap/helpers/_clearfix.scss` | CSS | 3 |
| `src/scss/vendors/bootstrap/helpers/_colored-links.scss` | CSS | 12 |
| `src/scss/vendors/bootstrap/helpers/_position.scss` | CSS | 30 |
| `src/scss/vendors/bootstrap/helpers/_ratio.scss` | CSS | 26 |
| `src/scss/vendors/bootstrap/helpers/_stretched-link.scss` | CSS | 15 |
| `src/scss/vendors/bootstrap/helpers/_text-truncation.scss` | CSS | 7 |
| `src/scss/vendors/bootstrap/helpers/_visually-hidden.scss` | CSS | 8 |
| `src/scss/vendors/bootstrap/mixins/_alert.scss` | CSS | 11 |
| `src/scss/vendors/bootstrap/mixins/_border-radius.scss` | CSS | 78 |
| `src/scss/vendors/bootstrap/mixins/_box-shadow.scss` | CSS | 18 |
| `src/scss/vendors/bootstrap/mixins/_breakpoints.scss` | CSS | 127 |
| `src/scss/vendors/bootstrap/mixins/_buttons.scss` | CSS | 133 |
| `src/scss/vendors/bootstrap/mixins/_caret.scss` | CSS | 64 |
| `src/scss/vendors/bootstrap/mixins/_clearfix.scss` | CSS | 9 |
| `src/scss/vendors/bootstrap/mixins/_color-scheme.scss` | CSS | 7 |
| `src/scss/vendors/bootstrap/mixins/_container.scss` | CSS | 9 |
| `src/scss/vendors/bootstrap/mixins/_deprecate.scss` | CSS | 10 |
| `src/scss/vendors/bootstrap/mixins/_forms.scss` | CSS | 144 |
| `src/scss/vendors/bootstrap/mixins/_gradients.scss` | CSS | 47 |
| `src/scss/vendors/bootstrap/mixins/_grid.scss` | CSS | 132 |
| `src/scss/vendors/bootstrap/mixins/_image.scss` | CSS | 16 |
| `src/scss/vendors/bootstrap/mixins/_list-group.scss` | CSS | 24 |
| `src/scss/vendors/bootstrap/mixins/_lists.scss` | CSS | 7 |
| `src/scss/vendors/bootstrap/mixins/_pagination.scss` | CSS | 31 |
| `src/scss/vendors/bootstrap/mixins/_reset-text.scss` | CSS | 17 |
| `src/scss/vendors/bootstrap/mixins/_resize.scss` | CSS | 6 |
| `src/scss/vendors/bootstrap/mixins/_table-variants.scss` | CSS | 21 |
| `src/scss/vendors/bootstrap/mixins/_text-truncate.scss` | CSS | 8 |
| `src/scss/vendors/bootstrap/mixins/_transition.scss` | CSS | 26 |
| `src/scss/vendors/bootstrap/mixins/_utilities.scss` | CSS | 68 |
| `src/scss/vendors/bootstrap/mixins/_visually-hidden.scss` | CSS | 29 |
| `src/scss/vendors/bootstrap/utilities/_api.scss` | CSS | 47 |
| `src/scss/vendors/bootstrap/vendor/_rfs.scss` | CSS | 354 |

</details>

### docker

Container helper scripts: **1 files, 51 lines**.

<details>
<summary>Show all 1 files</summary>

| File | Type | Lines |
|---|---|---:|
| `gunicorn.conf.py` | Python | 51 |

</details>

### auth

Auth page templates: **1 files, 70 lines**.

<details>
<summary>Show all 1 files</summary>

| File | Type | Lines |
|---|---|---:|
| `login.html` | HTML | 70 |

</details>

