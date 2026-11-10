# `attendance` — Module Summary

`attendance` is Horilla's time-and-attendance app. Employees check in and out from the navbar button, the mobile API or a biometric device, or they raise attendance requests. Managers and HR validate attendances, approve overtime, track late arrivals and early departures, keep the monthly hours balance, settle attendance/leave conflicts on the **Monthly Summary**, and set the time policies (grace time, validation conditions, IP restriction, check-in toggle). Its monthly summary (`build_monthly_summary`) is the attendance input to **payroll**. Its `WorkRecords` table ("Daily Work Status") is shared with **leave**.

### Quick facts

| Item | Value |
|---|---|
| URL prefix | `/attendance/` (appended in `attendance/apps.py:AttendanceConfig.ready`, also added to `settings.APPS` and `settings.APP_URLS`) |
| Sidebar entry | Yes. `settings.SIDEBARS` lists `"attendance"` (`horilla/settings/base.py:458`). `attendance/sidebar.py` has 9 submenus and registers an "Attendance" settings-menu section. `biometric/sidebar.py` inserts one more submenu at import time. |
| Models | 15: `AttendanceActivity`, `BatchAttendance`, `Attendance`, `AttendanceRequestFile`, `AttendanceRequestComment`, `AttendanceOverTime`, `AttendanceLateComeEarlyOut`, `AttendanceValidationCondition`, `GraceTime`, `AttendanceGeneralSetting`, `WorkRecords`, `AttendanceConflictResolution`, `AttendanceSummaryHours`, `AttendanceSummaryOverride`, `AttendanceDailyHours` |
| Approx. LOC | about 26.2k lines of Python, excluding migrations. That includes about 2.6k lines of tests. The largest files are `views/views.py` (3.5k), `views/summary.py` (3.2k), `models.py` (2.1k), `filters.py` (1.5k), `forms.py` (1.5k), `urls.py` (1.1k). |
| Templates | 148 under `attendance/templates/`. 24 of them are shadowed by `horilla_theme/templates/` (listed in §1). |
| URL patterns | about 228 `path()` entries, some commented out. Several names and paths are duplicated (see §5). |
| Scheduler jobs | 3, all in `attendance/scheduler.py`: `create_work_record` (every 30 min), `create_daily_work_record` (cron 00:30), `auto_punch_out` (every 5 min) |
| Tests | Yes. 15 modules in `attendance/tests/`, about 150 test methods. Areas: half-day resolution (53), summary override (44), conflict bulk resolve, IP/geofence web (GHSA-r59f-4xh4-58cf), export scoping, bulk validate, date indexes, holiday/minimum-hour logic, hour-account rebuild, top absentees, WorkRecord message length. `attendance` is in `SMOKE_LABELS`. |
| Company-scoped | **Partial.** Every model with employee or company data uses `HorillaCompanyManager` (through `employee_id__employee_work_info__company_id`, or its own `company_id`). `BatchAttendance`, `AttendanceRequestFile` and `AttendanceRequestComment` have no company manager; they also have no `company_id` field, so the `horilla.tenancy` check does not flag them. |

---

## 1. Code layout

| Path | Purpose |
|---|---|
| `apps.py` | `ready()` imports `scheduler` and `signals`, appends `path("attendance/", include("attendance.urls"))` to `horilla.urls.urlpatterns`, and adds the app to `settings.APPS` and `APP_URLS`. It imports `MIDDLEWARE` but does not use it; the docstring mentions an `AttendanceMiddleware` that is never added. |
| `models.py` | The 15 models, plus most business rules: overtime, hour-account rebuild, holiday minimum-hour, validation-condition lookup (see §3). |
| `signals.py` | `post_save` and `pre_delete` on `Attendance` keep `WorkRecords` in sync. `post_save` on `Company` creates an `AttendanceGeneralSetting`. Three `post_migrate` repair functions are present but commented out. |
| `scheduler.py` | `auto_punch_out`, `create_work_record`, and their `register_job` calls. |
| `sidebar.py` | `MENU`, `IMG_SRC`, `SUBMENUS` and the accessibility callables. `@settings_menu.register class AttendanceSettings` adds the "Attendance Rules" settings item. |
| `urls.py` | About 228 routes. The newer CBVs (`attendance/cbv/*`) and the older FBVs (`attendance/views/*`) are mixed together. |
| `admin.py` | Registers 8 models with Django admin. |
| `forms.py` | `AttendanceForm` (multi-employee create), `AttendanceUpdateForm`, `AttendanceRequestForm` and `NewRequestForm` (requests store JSON in `requested_data`), `BulkAttendanceRequestForm` (date range → one request per working day), `AttendanceOverTimeForm`, `AttendanceValidationConditionForm` (no overlapping shift/company conditions), `GraceTimeForm` and `GraceTimeAssignForm`, the export forms, `AttendanceRequestCommentForm`, `BatchAttendanceForm`, and `get_date_list()`. |
| `filters.py` | FilterSets (`AttendanceFilters`, `AttendanceOverTimeFilter`, `LateComeEarlyOutFilter`, `AttendanceActivityFilter`, `GraceTimeFilter`, …) and the `*ReGroup` group-by lists. It also **monkeypatches `employee.filters.EmployeeFilter`** (`filters.py:1449-1522`), adding `working_today`, `present_on`, `present_from`/`present_to`, `checked_in_on`, `not_present_on`, `expected_to_check_in` and `attendance_status`. |
| `dashboard.py` (top level) | The current attendance dashboard page (`attendance-dashboard`) and its JSON chart endpoints under `dashboard/api/*`: KPIs, late/early, overtime, hours distribution, attendance/absence % by dimension, average hours, top absentees, calendar heatmap, overview. |
| `methods/utils.py` | Shared helpers: `format_time`, `strtime_seconds`, the validators, `get_client_ip` (ipware with `AXES_IPWARE_PROXY_COUNT`), `geofence_denial_web`, `employee_exists`, `shift_schedule_today`, `attendance_day_checking`, `monthly_leave_days`, `month_date_range`, the fake `Request`/`Session`/`META` classes used for biometric, import and scheduler punches, and `get_employee_attendance_summary()` (the public entry point used by payroll). |
| `views/views.py` | The large FBV module: CRUD, import/export, validation, overtime approval, grace time, comments, work records and work-record export, settings toggles, allowed IPs. Defines `attendance_validate()`. |
| `views/clock_in_out.py` | `clock_in`, `clock_out`, `late_come`, `early_out` and the activity/attendance writers. Used by the web, biometric, API and import flows, and by the scheduler. |
| `views/requests.py` | The attendance-request workflow: create or change, approve, reject, bulk approve or reject, batches, `get_employee_shift`. |
| `views/summary.py` | The monthly summary engine (`build_monthly_summary`), the summary page, table, export, detail popover, calendar modal, conflict resolve (single and bulk), bulk override, undo, daily-hours edit. |
| `views/regularisation_import.py` | Excel template, import and confirm for month-level `AttendanceSummaryOverride`. |
| `views/dashboard.py` | Older dashboard helpers. These are still routed (`on-break-employees`, `dashboard-attendance`, `pending-hours`, `department-overtime-chart`, …), and the API and `base/dashboard.py` also call them. |
| `views/search.py` | Older HTMX search and filter endpoints (`attendance-search`, `search-attendance-requests`, `filter-own-attendance`, `attendance-widget-filter`, …). |
| `views/penalty.py` | `cut_available_leave`: creates `base.PenaltyAccounts` for a late/early record. |
| `views/process_attendance_data.py`, `views/handle_attendance_errors.py` | Excel import of attendances (`bulk_create`), plus a per-import error-sheet URL registered at runtime. |
| `views/geofaceconfig.py` | Redirects the old Geo & Face page to `attendance-rule-view`. |
| `cbv/attendances.py` | The Attendances page: three tabs (to validate, OT, validated), the list, nav and detail views, the create and update forms, the penalty list, and the individual validate tab. **At import time it also** adds the "Attendance" and "Penalty Account" tabs to `EmployeeProfileView`, re-patches `EmployeeFilter.__init__`, and sets `EmployeeNav.filter_instance`, `EmployeeCard/EmployeesList` status dots and `Employee.offline_online` (`cbv/attendances.py:920-1009`). |
| `cbv/attendance_request.py` | The Attendance Requests page (requested and all tabs), the new, bulk and update request form views, and the detail view. |
| `cbv/attendance_activity.py`, `cbv/hour_account.py`, `cbv/late_come_and_early_out.py`, `cbv/my_attendances.py` | List, nav, detail, export and form CBVs for activities (the check-in/out log), the hours balance (`AttendanceOverTime`), late/early records, and the employee's own attendances. |
| `cbv/attendance_tab.py` | The employee-profile Attendance tab and its sub-lists (requested, validate, all attendances, hour account). |
| `cbv/dashboard.py`, `cbv/dashboard_offline_online.py` | Dashboard widgets: to validate, OT to approve, on break, not-in-yet and not-out-yet employees. |
| `cbv/grace_time.py`, `cbv/break_point.py`, `cbv/check_in_check_out.py`, `cbv/ip_restriction.py` | Settings lists and forms: grace times, validation conditions ("break points"), check-in toggle, allowed IPs. |
| `cbv/accessibility.py`, `cbv/tab_shell.py` | Accessibility callables for profile tabs, and a shared tab-content shell. |
| `templatetags/attendancefilters.py` | `is_clocked_in`, `checkmanager`, `checkminimumot`, `any_permission`, `dynamic_regroup` (a tag), `current_month_record`, `get_item`, `get_employee_specific_holidays`, … **Templates in other apps load it** (see §4). |
| `management/commands/create_summary_fixtures.py` | Creates demo employees and attendance for Monthly Summary edge cases (`--month`, `--flush`). |
| `migrations/` | `0001`–`0013`. Recent ones: `0009` `AttendanceSummaryOverride`, `0010` field alters, `0011` `minimum_at_work_to_validate` and `shift_ids` on validation conditions, `0012` `WorkRecords.message` length, `0013` new `resolution` choices. `0002_initial` depends on `leave.0001_initial`. |
| `static/` | `attendance/actions.js`, `cbv/attendance_activity.js`, `cbv/attendance/hour_account.js`, `dashboard/attendanceChart.js`. |
| `templates/` | `attendance/` (87 files: attendance, attendance_account, attendance_activity, break_point, components, dashboard, grace_time, ip_restriction, late_come_early_out, monthly_summary (11), own_attendance, penalty, settings, work_record), `cbv/` (47), `requests/attendance/` (14), `attendance_form.html`. |
| `tests/` | See Quick facts. `tests/fixtures.py` has `HolidayFixtureMixin`. |

**Templates shadowed by `horilla_theme/templates/` (24).** Edit the theme copy, or the change will not show:
`attendance/components/in_out_component.html` (navbar check-in button), `attendance/dashboard/dashboard.html`, `attendance/late_come_early_out/tracking.html`, `attendance/penalty/form.html`, `attendance/settings/settings.html`, `attendance/work_record/work_record_list.html`, `attendance/work_record/work_record_view.html`, `cbv/attendance_activity/detail_delete_action.html`, `cbv/attendance_request/{attendance_request_option,attendance_request_tab,request_actions}.html`, `cbv/attendances/{detail_view_activity_col,ot_actions,ot_confirmation,ot_tab_action,validate_actions,validate_button,validate_tab_action,validated_tab_action}.html`, `cbv/hour_account/{hour_actions,hour_detail_action}.html`, `cbv/late_come_and_early_out/detail_action.html`, `requests/attendance/{individual_view,request_new_form}.html`.

---

## 2. Core problems solved

- **Record time worked.** Employees check in and out (several times a day). The system keeps the first check-in, the last check-out and the total worked hours per day, including night shifts that cross midnight.
- **Capture punches from every channel.** Web button, mobile API, biometric devices (ZKTeco/Anviz through `biometric`), Excel import of activities or attendances, and automatic punch-out at the end of a shift.
- **Restrict where people can punch.** Office IP allow-list per company, geofence (via `geofencing`), face detection settings.
- **Correct attendance.** Employees or managers raise create or update requests (single, or bulk over a date range). Managers approve or reject them, can comment and attach files, and requests can be grouped into batches.
- **Validate attendance and approve overtime.** Auto-validate within configured hour bounds. Overtime is computed over the shift minimum, capped at a cutoff, and auto-approved above a threshold.
- **Track discipline.** Late arrival and early departure are flagged against shift schedules with grace time, and fines or leave deductions can be applied (penalty accounts).
- **Keep a monthly hours balance** per employee: worked, pending and approved overtime hours.
- **Show daily work status** per employee per day (Present, Half Day, Absent, Holiday, Conflict, Draft) in a month grid, with Excel export.
- **Close the month for payroll.** Count present, paid leave, unpaid leave, absent, week-off and holiday days per employee. Detect attendance-vs-leave conflicts, let HR regularise days, override daily hours or state the month totals, and give payroll clean figures.
- **Give managers visibility.** Dashboards (KPIs, late/early, overtime, absentees, heatmap), who has not checked in, who is on break.

---

## 3. How it works — technical design and business logic

### 3.1 Data model (key fields and relations)

| Model | Key fields / relations | Notes |
|---|---|---|
| `AttendanceActivity` | `employee_id` FK Employee (PROTECT), `attendance_date`, `shift_day` FK EmployeeShiftDay, `clock_in_date`/`clock_in`, `clock_out_date`/`clock_out`, `in_datetime`/`out_datetime` | One row per punch pair. Audited (`HorillaAuditLog`). `duration()` uses *now* while the activity is still open. |
| `Attendance` | `employee_id` (nullable FK, PROTECT), `attendance_date`, `shift_id`, `work_type_id`, `attendance_day`, clock-in and clock-out date/time, `attendance_worked_hour`/`minimum_hour`/`attendance_overtime` as "HH:MM" strings, `at_work_second`, `overtime_second`, `approved_overtime_second`, `attendance_validated`, `attendance_overtime_approve`, `is_validate_request`, `is_validate_request_approved`, `request_type` (`create_request`/`update_request`/`created_request`), `requested_data` (JSON string), `request_description`, `is_holiday`, `is_bulk_request`, `batch_attendance_id`, `approved_by` | `unique_together(employee_id, attendance_date)`. Indexes `attendance_date_idx` and `attendance_date_validated_idx`. Custom permissions `change_validateattendance` and `change_approveovertime`. Audited. |
| `AttendanceOverTime` ("Hours Balance") | `employee_id`, `month` (lower-case name), `month_sequence`, `year` (string), `worked_hours`/`pending_hours`/`overtime` strings, plus `*_second` integers | `unique_together(employee_id, month, year)`. `save()` rebuilds the strings from the `*_second` fields (`models.py:1356`). |
| `AttendanceLateComeEarlyOut` | `attendance_id` FK Attendance (PROTECT), `employee_id`, `type` (`late_come`/`early_out`) | Unique per `(attendance, type)`. `save()` writes twice to copy the employee from the attendance (`models.py:1417`). `base.PenaltyAccounts.late_early_id` points to it. |
| `AttendanceValidationCondition` | `minimum_at_work_to_validate`, `validation_at_work`, `minimum_overtime_to_approve`, `overtime_cutoff`, `auto_approve_ot`, M2M `shift_ids`, M2M `company_id` | `for_shift(shift)` returns the shift-specific condition, else the shift-less default (`models.py:1537`). `min_overtime_q()` builds a per-shift overtime Q. |
| `GraceTime` | `allowed_time` "HH:MM:SS", `allowed_time_in_secs`, `allowed_clock_in`/`allowed_clock_out`, `is_default`, M2M `company_id` | At most one default (`clean`). `base.EmployeeShift.grace_time_id` points to it (PROTECT). |
| `AttendanceGeneralSetting` | `time_runner`, `enable_check_in`, `company_id` (nullable FK; `None` = global) | Created per company by a signal. |
| `WorkRecords` | `employee_id` (CASCADE), `date`, `work_record_type` (FDP/HDP/ABS/HD/CONF/DFT), `at_work`/`min_hour` (+ seconds), `day_percentage`, `message`, `is_attendance_record`/`attendance_id`, `is_leave_record`/`leave_request_id` (**only defined when `leave` is installed**, `models.py:1820`), `shift_id`, `last_update` | A plain `models.Model`, **not** a `HorillaModel` (no `has_xss` check, no audit fields). `UniqueConstraint(employee_id, date)`. Written by attendance signals, leave signals and the scheduler. |
| `AttendanceConflictResolution` | `employee_id`, `date`, `resolution` (full/half present, half absent, partial hours, absent, paid/unpaid leave, holiday, week off, `split:X+Y`, legacy `attendance`/`leave`), `conflict_type` | Unique per `(employee, date)`. The HR regularisation of one day. Audited (`horilla_audit/registry.py:63`). |
| `AttendanceSummaryHours` | `employee_id`, `from_date`, `to_date`, `hours_second`, `is_manually_edited` | Cache of summary hours. Upserted on **every** summary build (`summary.py:854`). |
| `AttendanceSummaryOverride` | `employee_id`, period, nullable `present`/`paid_leave`/`unpaid_leave`/`absent`, `note` | Month totals stated by HR. `applied_to(row)` overlays the figures and clears the unresolved conflicts (`models.py:2028`). |
| `AttendanceDailyHours` | `employee_id`, `date`, `hours_second`, `is_manually_edited` | Per-day manual hours from the calendar modal. Audited. |
| `BatchAttendance`, `AttendanceRequestComment`, `AttendanceRequestFile` | title; comment → `Attendance`, `Employee`, M2M files | Grouping of requests, and the request discussion. |

### 3.2 Attendance save pipeline (`models.py:Attendance.save`, lines 847-926)

1. If `attendance_day` is missing, it is looked up with `EmployeeShiftDay.objects.get(day=<weekday>)`. This needs the seven shift days that `base.signals.create_shift_days` seeds on `post_migrate`.
2. `update_attendance_overtime()`: `overtime = max(0, worked − minimum)`, and `at_work_second` and `overtime_second` are set.
3. `adjust_minimum_hour()`: on a holiday (`base.methods.is_holiday`) or company leave (`is_company_leave`), `minimum_hour` is set to `"00:00"` and `is_holiday=True`, so the whole day counts as overtime.
4. `handle_overtime_conditions()`: overtime is capped at `overtime_cutoff`, and auto-approved when `auto_approve_ot` is set and overtime ≥ `minimum_overtime_to_approve`. A pending `is_validate_request` resets validation.
5. `approved_overtime_second` follows the approve flag.
6. After `super().save()`, if anything changed, the month's `AttendanceOverTime` row is fetched or created inside `transaction.atomic()`. Approved overtime moves by its delta. `update_ot()` (`models.py:996`) **rebuilds** the worked and pending seconds from the month's *validated* attendances, excluding approved or cancel-requested leave days (when `leave` is installed). Worked time is capped per day at `minimum_hour`.
7. `delete()` removes that day's activities, then rebuilds the hour account.
8. `clean()` rejects a check-in date before the attendance date, a check-out before the check-in, and a check-out in the future.
9. HorillaModel side effects also run: `clean_fields()`/`has_xss`, `created_by`/`modified_by` from the thread-local request, and the audit log.

### 3.3 Check-in / check-out flow (`views/clock_in_out.py`)

- `clock_in` (`login_required` + `hx_request_required`):
  1. Reads `AttendanceGeneralSetting.enable_check_in` for the session company (`selected_company`; `"all"` means the global row). If the request carries `datetime` (biometric, scheduler or import fake `Request`), the check is skipped.
  2. If the company's `base.AttendanceAllowedIP` is enabled, the client IP from `get_client_ip()` must fall inside one of the allowed networks (`clock_in_out.py:228-262`).
  3. `geofence_denial_web()` enforces `geofencing.GeoFencing` and fails closed when coordinates are missing.
  4. Resolves the employee's shift and today's `EmployeeShiftSchedule` (`shift_schedule_today`). **Night-shift rule:** when the shift starts after it ends and the punch is before 12:00, the attendance belongs to *yesterday* (`clock_in_out.py:293-309`).
  5. `clock_in_attendance_and_activity()` closes any open activity, creates a new `AttendanceActivity`, and creates the `Attendance` if missing (then runs `late_come()`). If the attendance exists, it clears the clock-out and deletes any early-out flag.
  6. Renders `attendance/components/in_out_component.html` (theme-shadowed).
- `clock_out`: the same gates, then `clock_out_attendance_and_activity()` closes the last open activity and sums all of that day's activity durations into `attendance_worked_hour`. It computes overtime, sets `attendance_validated = attendance_validate(attendance)` and saves. `early_out()` runs if the record is not already flagged.
- **Late / early rules** (`late_come`, `early_out`): they run only when `TrackLateComeEarlyOut` is enabled (`base.context_processors.enable_late_come_early_out_tracking`). Grace time comes from the shift's `grace_time_id` (when active and applicable to in or out) first, then the default active `GraceTime`. Late = check-in minus grace is after the shift start. Early = check-out plus grace is before the shift end. Night-shift branches use the 12:00 midpoint.
- **Auto-validation** (`views/views.py:attendance_validate`, line 136): `minimum_at_work_to_validate ≤ worked ≤ validation_at_work` of `AttendanceValidationCondition.for_shift()`. The default upper bound is 09:00.

### 3.4 Attendance requests (`views/requests.py`, `cbv/attendance_request.py`, `forms.py`)

- **New request** (`NewAttendanceRequestFormView` → `NewRequestForm.clean`, `forms.py:846`). If an attendance already exists for that employee and date, `clean()` itself writes the stringified requested values into `requested_data` and **saves** the existing row (`is_validate_request=True`, `request_type=update_request`). Otherwise it prepares a new `Attendance` with `request_type="create_request"`, which the view saves.
- **Bulk request** (`BulkAttendanceRequestForm`). `get_date_list()` (`forms.py:1140`) returns the working days (`base.methods.get_working_days`) minus existing attendances and approved leave days. The form then creates one `NewRequestForm` per date (`is_bulk_request=True`, optional batch).
- **Change request** (`attendance_request_changes`, `UpdateAttendanceRequestFormView`). `AttendanceRequestForm.save()` never commits. The serialized instance is stored as `requested_data`, and the reporting manager is notified (`notifications.signals.notify`).
- **Approve** (`approve_validate_attendance_request`, `bulk_approve_attendance_request`). The record is marked validated with `approved_by`. `requested_data` is applied with `Attendance.objects.filter(id=..).update(**data)` and then `.save()` runs again to recompute overtime (`requests.py:478-485`). Missing activities are created or updated, late/early is re-evaluated, and the employee and manager are notified. Bulk approve skips the approver's own records unless the approver is a superuser.
- **Reject** (`cancel_attendance_request`, `bulk_reject_attendance_request`): clears the request fields and notifies the employee.
- **Comments** (`create/view/delete_attendancerequest_comment`): notifications are sent to the employee and/or the manager. Deleting a comment is scoped to the owner or the manager's visibility (`views.py:2487`).

### 3.5 Validation and overtime approval

- `validate_this_attendance`, `validate_bulk_attendance`, `approve_overtime`, `approve_bulk_overtime` are under `manager_can_enter("attendance.change_attendance")`. Self-validation and self-approval are blocked for non-superusers. When worked hours are `00:00`, they are recomputed from activities before validating (issue #1055). Each action notifies the employee. Bulk endpoints return `with_bulk_result` counts.
- `revalidate_this_attendance` resets validation and notifies the reporting manager.
- The OT tab lists validated rows with `overtime_second > 0`. `Attendance.overtime_cell()` flags overtime below the shift's minimum.

### 3.6 Work records / Daily Work Status

- `signals.attendance_post_save` (`signals.py:19`). Status rule: not validated → `CONF`; worked ≥ minimum → `FDP`; ≥ half of minimum → `HDP`; otherwise `ABS`. No clock-out yet → `FDP` "Currently working". Sets `day_percentage` to 1.0 or 0.5. It skips `raw` saves (loaddata). `pre_delete` removes non-leave work records.
- `scheduler.create_work_record` creates `DFT` rows for every employee with a shift schedule who has no row for today. It runs every 30 minutes and at 00:30.
- `leave/signals.py:75-102` and `leave/methods.py:116` write, delete and read leave work records.
- Views: `work_records` and `work_records_change_month` (a month grid with holidays and company leaves from `monthly_leave_days`). `work_record_export` builds an XLSX or CSV with a company header, the applied-filters banner and colour codes.

### 3.7 Monthly Summary and payroll feed (`views/summary.py`)

`build_monthly_summary(from_date, to_date, employee_qs)` (`summary.py:327`). Each part is loaded in one batch:

- Working days, holidays and company leaves (`base.methods.get_working_days`, `get_holiday_dates`, `get_company_leave_dates`).
- Attendances, classified per day using the **default grace time**: worked ≥ `min − grace` → 1.0, worked ≥ half of that → 0.5, otherwise 0. A day with no minimum counts 1.0.
- Shift schedules, used for an 8 h default when no schedule exists.
- Manual `AttendanceSummaryHours` and `AttendanceDailyHours`.
- Approved or cancel-requested `leave.LeaveRequest` rows, including half-day breakdowns (`partial_leave_days`, `natural_halves`).
- `base.Roster` week-offs, falling back to company leaves.
- `AttendanceConflictResolution`.

Per employee and per date, an HR resolution wins first: a split day, a direct bucket, or `partial_hours`. Otherwise these rules apply in order:

1. Half-day leave plus attendance for the other half.
2. Attendance on a holiday counts as holiday; on a week-off, as week-off; otherwise as present, with the short part counted absent.
3. Paid leave, then unpaid leave, then holiday, then week-off.
4. Any other working day with no attendance counts absent.

**Conflicts** are attendance days that overlap a full leave day. Hours, worked, regular and overtime figures are split into regular, week-off and holiday overtime. After that, **`AttendanceSummaryOverride`** rows are applied on top. The function upserts `AttendanceSummaryHours` (`bulk_create(update_conflicts=True)`) as a side effect.

- `methods/utils.get_employee_attendance_summary()` wraps it and adds `paid_days`/`unpaid_days`. Payroll uses this wrapper.
- UI: `attendance_monthly_summary` (page), `_table`, `_export` (XLSX), `_detail` (metric popover), `_calendar` (`_build_calendar_context`, also used by the ESS dashboard), `_conflict_resolve` (one day; `update_or_create` through `_base_manager`), `_conflict_bulk_resolve`, `_bulk_override`, `_undo_bulk`, `_daily_hours_edit`. `day_history()` reads `auditlog.LogEntry` for the audited models.
- `views/regularisation_import.py`: download a template pre-filled with computed rows, upload it, check it against the computed summary, stash it in the session (`attendance_summary_pending`), confirm, then write `AttendanceSummaryOverride` rows atomically. Scope comes from `filtersubordinatesemployeemodel` (`_scope`, line 64).

### 3.8 Settings / policies

- The **Attendance Rules** page (`attendance_rule_settings_view`, `views.py:3300`) brings together: late/early tracking (`base.TrackLateComeEarlyOut`), check-in toggle and time runner (`AttendanceGeneralSetting`), biometric (`base.BiometricAttendance`), IP restriction (`base.AttendanceAllowedIP.additional_data["allowed_ips"]`) and face detection. Many older pages redirect here.
- **Time Policies** (`grace-time-view`): grace times (FBV and CBV forms; you can assign a grace time to shifts) and validation conditions (break points).
- The **Penalty** (`cut_available_leave`) creates `base.PenaltyAccounts` with an optional leave deduction (`leave.AvailableLeave`).

### 3.9 Import / export

- Attendance import (`attendance_import` → `process_attendance_data`) requires 10 columns. Valid rows go in with **`Attendance.objects.bulk_create`** (`process_attendance_data.py:118`).
- Activity import (`attendance_activity_import` → `process_activity_dicts`) replays each row through `clock_in` and `clock_out` with a fake `Request`.
- Error sheets are served from a one-off URL appended to `attendance.urls.urlpatterns` at runtime (`handle_attendance_errors.py:78`, `views.py:1110`).
- Exports use `base.methods.export_data` (scoped; see `tests/test_export_scoping.py`) or the CBV export navs.

### 3.10 Permissions and decorators

- Decorators used: `horilla.decorators.login_required`, `hx_request_required`, `permission_required`, `manager_can_enter` (also re-exported in `base.decorators`), `install_required` (late/early page needs tracking enabled); `horilla_views.cbv_methods.login_required` for CBVs; `django.contrib.auth.decorators.login_required` in the top-level `dashboard.py`.
- Scoping helpers: `base.methods.filtersubordinates`, `filtersubordinatesemployeemodel`, `choosesubordinates`, `is_reportingmanager`, `check_manager`.
- `manager_can_enter(perm)` lets in **any user who is the reporting manager of anyone** (`horilla/decorators.py:181-185`). The view is responsible for scoping the object.

### 3.11 Scheduler jobs (`scheduler.py`)

| Job | Trigger | What it does |
|---|---|---|
| `create_work_record` | interval 30 min (misfire grace 3 h) and cron 00:30 (`create_daily_work_record`) | `bulk_create(ignore_conflicts=True)` of `DFT` WorkRecords for today |
| `auto_punch_out` | interval 5 min (`auto_punch_out`) | For each `EmployeeShiftSchedule` with `is_auto_punch_out_enabled`, open activities on that shift day are clocked out at `auto_punch_out_time`, through `clock_out(Request(...))`. Adds one day for night shifts. |

They run only under `python manage.py run_scheduler`. No company ContextVar is set there, so the queries cover all tenants.

---

## 4. Communication with other modules

### 4.1 What `attendance` depends on

| Module | What is used | Where |
|---|---|---|
| `base` | Models `Company`, `EmployeeShift`, `EmployeeShiftDay`, `EmployeeShiftSchedule`, `WorkType`, `Holidays`, `CompanyLeaves`, `WEEK_DAYS`, `AttendanceAllowedIP`, `TrackLateComeEarlyOut`, `BiometricAttendance`, `PenaltyAccounts`, `Roster`, `Department`, `JobPosition` | `models.py:35`, `views/views.py:117`, `views/clock_in_out.py:45`, `views/summary.py:38`, `methods/utils.py:19` |
| `base` | Methods: `filtersubordinates*`, `choosesubordinates`, `export_data`, `get_working_days`, `get_holiday_dates`, `get_company_leave_dates`, `is_holiday`, `is_company_leave`, `eval_validate`, `closest_numbers`, `get_session_company`, `get_pagination`, `has_export_access`, `is_reportingmanager`, `check_manager` | across views, cbv, forms |
| `base` | `HorillaCompanyManager`, `context_processors.enable_late_come_early_out_tracking`/`timerunner_enabled`, `forms.ModelForm`/`AttendanceAllowedIPForm`/`PenaltyAccountForm`, `import_template_data`, `views.add_remove_dynamic_fields`, `cbv.work_shift_tab.ProfileTabShellView`, `backends.logger`, `templatetags.basefilters.is_reportingmanager` | `models.py:33`, `sidebar.py:9-10`, `urls.py:30-32`, `scheduler.py:6` |
| `base` signals | `create_shift_days` (post_migrate) seeds the `EmployeeShiftDay` rows that `Attendance.save()` and `clock_in` `.get()` | `base/signals.py` |
| `employee` | FK `Employee` (all models), `EmployeeWorkInformation` (shift, work type, reporting manager, company), `EmployeeTag`, `EmployeeFilter`, `EmployeeProfileView`, `EmployeeNav/EmployeeCard/EmployeesList` (patched) | `models.py:36`, `cbv/attendances.py:30-33` |
| `leave` | `LeaveRequest` (hard import in `views/summary.py:341`, `:1317`, `:2302`; `filters.py:get_checked_in_on`/`get_expected_to_check_in`; `dashboard.py:_missing_punches_employees`). `leave.filters.LeaveRequestFilter` (guarded, `forms.py:1150`). `AvailableLeave` (guarded, `views/penalty.py`). FK `WorkRecords.leave_request_id` (conditional). **Migration dependency** in `0002_initial`. | see cites |
| `horilla` | `HorillaModel`, `upload_path`, `decorators`, `horilla_middlewares._thread_locals`, `scheduling.register_job`, `http.response.HorillaRedirect`/`with_bulk_result`, `methods.get_horilla_model_class`/`remove_dynamic_url`, `filters.HorillaFilterSet`, `menu.settings_menu`, `horilla.urls.urlpatterns` | `models.py:39-40`, `apps.py`, `scheduler.py:7`, `sidebar.py:11` |
| `horilla_views` | Generic CBVs (`HorillaListView`, `HorillaNavView`, `HorillaDetailedView`, `HorillaFormView`, `HorillaTabView`, `HorillaTabContentShell`), `cbv_methods.render_template` (used by model column methods) | `models.py:42`, `cbv/*` |
| `horilla_audit` / `auditlog` | `HorillaAuditLog`, `HorillaAuditInfo` history; `auditlog.LogEntry` in `day_history`; the registry whitelists the Attendance models | `models.py:41`, `views/summary.py:195`, `horilla_audit/registry.py:59-64` |
| `notifications` (vendored) | `notify.send` on validate, OT approve, request create/approve/reject, comments | `views/views.py:133`, `views/requests.py:54`, `cbv/attendance_request.py:39` |
| `geofencing` | `GeoFencing` (unconditional import inside `geofence_denial_web`) | `methods/utils.py:202-204` |
| `facedetection`, `biometric` | `FaceDetection` (guarded) on the rules page; `apps.is_installed("biometric")` in sidebar accessibility | `views/views.py:3326`, `sidebar.py:151` |
| Third-party | `pandas`, `xlsxwriter`, `PIL`, `django-ipware`, `geopy`, `django_filters` | imports in views and utils |
| Settings | `AXES_IPWARE_PROXY_COUNT`/`AXES_IPWARE_META_PRECEDENCE_ORDER` (`AXES_PROXY_COUNT` env), `HORILLA_TIME_FORMATS`, `HORILLA_DATE_FORMATS`, `DYNAMIC_URL_PATTERNS`, `APPS`, `APP_URLS`, `MEDIA_ROOT` | `methods/utils.py:180`, `horilla/settings/base.py:571-654` |

### 4.2 What depends on `attendance`

| Module | What they use | Where |
|---|---|---|
| `payroll` | `get_employee_attendance_summary` (batch run and review); `build_monthly_summary` (component views); `AttendanceConflictResolution` (OT and pay calculation); `Attendance` model; templates `attendance/monthly_summary/_calendar_modal_host.html` and `_regularise_opener.html` (unconditional include) | `payroll/methods/batch_run.py:167,337`, `payroll/views/component_views.py:814`, `payroll/methods/methods.py:248`, `payroll/methods/payslip_calc.py:1124`, `payroll/models/models.py:1220`, `payroll/templates/payroll/batch/wizard_review.html:15,22` |
| `base` | `get_employee_attendance_summary` (payslip recompute), `attendance.views.dashboard.dashboard_attendance`/`department_overtime_chart`, `Attendance`, `AttendanceLateComeEarlyOut`, `AttendanceGeneralSetting` (navbar `is_check_in_enabled`), `_build_calendar_context` (ESS dashboard), request-tab CBVs, `WorkRecords` (signals). FKs `EmployeeShift.grace_time_id` → `GraceTime` and `PenaltyAccounts.late_early_id` → `AttendanceLateComeEarlyOut` (conditional on the app being installed). | `base/views.py:366`, `base/dashboard.py:566,668,1384,1973,1989`, `base/ess_dashboard.py:138,345,382,509`, `base/templatetags/horillafilters.py:351,425`, `base/signals.py:193`, `base/models.py:842-850,3104-3110`, `base/context_processors.py:271` |
| `leave` | `WorkRecords` read/write; `CompensatoryLeaveRequest.attendance_id` M2M → `Attendance` (defined only if attendance is installed); `attendance_days()`; sidebar checks attendance perms | `leave/signals.py:87,102`, `leave/methods.py:116`, `leave/models.py:2445-2455`, `leave/sidebar.py:138-149` |
| `horilla_api` | `api_views/attendance/views.py` does `from attendance.views.views import *` and `from attendance.views.clock_in_out import *`, and also imports `clock_out`, `clock_in_attendance_and_activity`, `views.dashboard.find_*`, `NewRequestForm`, `AttendanceRequestForm`. Mobile home uses `Attendance` and `AttendanceActivity`. Endpoints under `/api/attendance/…`: clock-in, clock-out, attendance CRUD/list, validate, requests, overtime approve, hour account, late/early, activity, today, offline employees, my-attendance, … | `horilla_api/api_views/attendance/views.py:19-32,184,227`, `horilla_api/api_urls/attendance/urls.py`, `horilla_api/api_views/mobile/views.py:24` |
| `biometric` | `clock_in`, `clock_out`, the fake `Request`, `AttendanceActivity` for device punches; inserts into `attendance.sidebar.SUBMENUS` | `biometric/views.py:30-32`, `biometric/sidebar.py:8,21` |
| `employee` | `EmployeeFilter`, list/card status dots and `Employee.offline_online` are patched by attendance; `Employee.get_forecasted_at_work()` / clocked-in logic reads `employee_attendances` (guarded); `not_in_out_dashboard` uses `AttendanceFilters`, `AttendanceExportForm`, `Attendance`; profile tabs are registered from attendance | `employee/models.py:337-382`, `employee/not_in_out_dashboard.py:154-156`, `attendance/cbv/attendances.py:920-1009` |
| `report` | `Attendance`, `AttendanceLateComeEarlyOut`, `AttendanceFilters` in metrics and the attendance report; `export_model="attendance.Attendance"` | `report/views/attendance_report.py:12-13`, `report/metrics/time_leave.py`, `report/metrics/definitions.py:186-570`, `report/metrics/packs.py:474` |
| `horilla_theme` | 24 shadowing templates; `overrides.py` patches `DashboardaAttendanceOT`/`DashboardAttendanceToValidate` (guarded) | `horilla_theme/overrides.py:560-575` |
| `project` | `validate_time_format` validator | `project/models.py:20` |
| `whatsapp` | `NewRequestForm`, `requests.request_new` (an FBV that is no longer routed but is still called) | `whatsapp/utils.py:753-754` |
| Templates of other apps | `{% load attendancefilters %}` (for `dynamic_regroup`) in `onboarding/.../group_by.html`, `offboarding/.../resignation/group_by.html`, `payroll/.../payslip/group_payslips.html`, `pms/templates/okr/group_by.html`, `recruitment/templates/survey_preview_form.html`; navbar includes `attendance/components/in_out_component.html` (guarded by `app_installed`) in `templates/index.html:148-151` and `horilla_theme/.../components/header.html:36-39` | |
| `horilla_crumbs` | URL names `attendance-view`, `request-attendance-view`, `attendance-overtime-view`, `attendance-activity-view`, `view-my-attendance` | `horilla_crumbs/context_processors.py:165-172` |
| `horilla.testkit` | the `Attendance` factory | `horilla/testkit/factories.py:123` |

### 4.3 Integration mechanisms

- **Django signals:** `post_save`/`pre_delete` `Attendance` → `WorkRecords`; `post_save` `Company` → `AttendanceGeneralSetting`. Leave's own receivers write `WorkRecords`. It does not use the custom `horilla/signals.py` signals directly, but `QuerySet.update` (used in request approval) sends `pre/post_bulk_update` through the base monkeypatch.
- **Import-time monkeypatching:** `EmployeeFilter`, employee CBV attributes, `Employee.offline_online`, `EmployeeProfileView.add_tab`, `biometric` editing `SUBMENUS`. These run when `attendance.urls` (→ `attendance.cbv`) and `attendance.filters` are imported.
- **URLs:** 100+ named routes are used by templates across `base`, `employee`, `horilla_theme`, `payroll`, `pms` and the root `templates/`.
- **Notifications:** in-app `notify.send`. No email is sent from this module, except through `horilla_api` (`OfflineEmployeeMailsend`).
- **Context / templates:** `base.context_processors` reads `AttendanceGeneralSetting`; the `attendancefilters` library; the navbar check-in component.
- **Scheduler:** `horilla.scheduling.register_job` (3 jobs).
- **Settings menu:** `horilla.menu.settings_menu.register`.

---

## 5. What can break this module

**Dependencies and setup**
- **`leave` not installed.** `migrations/0002_initial.py` depends on `leave.0001_initial`, so migrations fail. Without `leave`, the summary (`views/summary.py:341`), summary detail and conflict views, the dashboard missing-punch KPI (`dashboard.py:_missing_punches_employees`) and the `EmployeeFilter` attendance filters (`filters.py:get_checked_in_on`) raise `ImportError`. `WorkRecords.leave_request_id` would also disappear from the model while the migration still has it.
- **`geofencing` not loadable.** `geofence_denial_web` imports `geofencing.models` with no guard (`methods/utils.py:204`). Web clock-in and clock-out raise if the app is missing. It is appended to `INSTALLED_APPS` only by `horilla_api/__init__.py`.
- **`EmployeeShiftDay` rows missing** (the `base` post_migrate seeding did not run, or rows were deleted). `EmployeeShiftDay.objects.get(...)` raises `DoesNotExist` in `Attendance.save()` (`models.py:852`), `clock_in` (`clock_in_out.py:284,304`), `clock_out` (`:546,555`) and request approval (`requests.py:520,751`).
- **Migrations not applied** (0007–0013 add the summary/override/daily-hours models and the condition fields `shift_ids`/`minimum_at_work_to_validate`). The summary and `AttendanceValidationCondition.for_shift`, which every save and clock-out calls, fail with DB errors.
- **Scheduler not running** (`run_scheduler` / the `scheduler` service). No `DFT` WorkRecords, and **no auto punch-out**: open activities stay open, worked hours are never closed, and the summary counts those days short or absent.
- **Behind a reverse proxy without `AXES_PROXY_COUNT`.** `get_client_ip` sees the proxy IP (`methods/utils.py:178-183`, `horilla/settings/base.py:648-654`), so the IP restriction either blocks everyone or allows everyone.
- **Database feature.** `AttendanceSummaryHours.objects.bulk_create(update_conflicts=True, unique_fields=…)` (`summary.py:855`) needs a backend that supports upserts (Postgres in CI; SQLite works when recent).

**Data assumptions**
- **Employee without `employee_work_info`.**
  - `clock_out` uses `work_info.shift_id` with no check (`clock_in_out.py:541`), giving an `AttributeError` (`clock_in` does check, at `:277`).
  - Request approval, the comment notification and update requests access `employee_work_info.reporting_manager_id` directly (`requests.py:375,545,784`; `cbv/attendance_request.py:628`).
  - `clock_in_attendance_and_activity` reads `employee_work_info.work_type_id` (`clock_in_out.py:179`).
- **Employee without a shift**, or a shift with no schedule for the day: minimum hour becomes `00:00` and start/end become 0, so every hour is overtime and late/early is skipped.
- **`Attendance.employee_id` is nullable**, but `__str__`, `serialize()` and many column methods dereference it (`models.py:470,936`).
- **No `AttendanceGeneralSetting` row** for the session company (and none global): check-in is reported as "not enabled" (`clock_in_out.py:211-226,334-341`). Rows are created only by the `Company` post_save signal or on a visit to the rules page.
- **`AttendanceOverTime.year` default** is evaluated once at import (`models.py:1135`: `default=datetime.now().strftime("%Y")`). A long-running worker uses last year's value after New Year wherever the default is relied on (for example forms). The save pipeline passes the year explicitly.
- **Global calendar state.** `monthly_leave_days` calls `calendar.setfirstweekday()`, which is process-global and not thread-safe (`methods/utils.py:539,553`). It can also raise `IndexError` when `based_on_week` exceeds the weeks in the month (`:541`).

**Fragile code paths**
- `signals.attendance_post_save`: if `get_or_create` raises anything other than `MultipleObjectsReturned`, the `except Exception` at `signals.py:65` logs and then falls through to `work_record.employee_id = …` (`:68`). `work_record` is unbound there, so an `UnboundLocalError` breaks the attendance save.
- `clock_out_attendance_and_activity` writes the clock-out onto the employee's **latest-dated** `Attendance`, not the attendance of the open activity (`clock_in_out.py:382-384`). A later-dated row created by a request can receive the punch.
- Request rejection sets `request_type = None`, saves, *then* checks `request_type == "create_request"` (`requests.py:601-605`, `:833-836`). The condition is never true, so rejected *create* requests are never deleted; they stay as unvalidated attendances.
- `BulkAttendanceRequestForm.save` calls `logger(form.errors)` (`forms.py:1405`). A `Logger` is not callable, so any invalid per-day sub-form raises `TypeError` and aborts the bulk request part-way.
- `NewRequestForm.clean()` writes to the DB during validation (`forms.py:~915-925`). A failed `is_valid()` later in the view still leaves the change saved.
- Attendance Excel import uses `bulk_create` (`process_attendance_data.py:118`). This skips `save()`: no `attendance_day`, no overtime/seconds, no hour-account update, and **no post_save signal, so no WorkRecords**. `update_ot` already works around the empty `at_work_second` (`models.py:1043-1047`).
- Import error-sheet URLs are appended to `urlpatterns` at runtime (`handle_attendance_errors.py:78`, `views.py:1110`). They exist only in the worker that handled the upload; with several gunicorn workers the download link can 404. Patterns build up until downloaded. The download view has no auth decorator.
- **Non-existent permissions.** `permission_required("attendance.update_gracetime")` (`views.py:2244,2274`) can only pass for superusers, so the grace-time toggles fail for HR roles. `filtersubordinates(..., perm="attendance.change_overtime")` (`views/dashboard.py:~168,~205`) never matches a granted permission, so HR users without superuser see only subordinates.
- `delete_allowed_ips` pops several indexes in turn from the same list (`views.py:3417-3418`), so the indexes shift and the wrong IPs are removed. In `edit_allowed_ips`, `form` is unbound when the id is invalid, so render raises (`views.py:3440-3471`).
- **Duplicate routes.** `attendance-create/` (CBV then FBV, `urls.py:164,198`) and `get-attendance-activities/<int>/` (CBV then FBV, `urls.py:569-579`) are each defined twice; only the first resolves. `attendance-view`, `view-my-attendance`, `attendance-overtime-update` and others also repeat names, which makes `{% url %}` resolution order-dependent.
- **Star imports.** `horilla_api` does `from attendance.views.views import *` and `from attendance.views.clock_in_out import *`, so renaming or removing a helper in those modules (for example `Request`, `strtime_seconds`, `shift_schedule_today`) silently breaks the API views.
- **Template shadowing.** Edits to the 24 app templates listed in §1 (notably `in_out_component.html`, `work_record_list.html`, the request and OT action templates) have no effect while the `horilla_theme` copy exists. In production the cached loader also needs a restart.
- **Tenancy.** No ContextVar is set in scheduler or management-command contexts, so the managers return all companies (intended for the jobs, but note it for custom scripts). `.distinct()` is added to every scoped queryset (`base/horilla_company_manager.py:172-174`).

**Authorization gaps noticed** (bare-id lookups; same class as the repo's `*_idor` fixes; not exhaustively verified)
- Only `login_required`, no object scope:
  - `user_request_one_view`, `validate_attendance_request`, `attendance_request_changes` (any user can create an update request on any attendance id).
  - `view_attendancerequest_comment` (also attaches files to any `comment_id`), `delete_comment_file` (deletes any `AttendanceRequestFile` id), `update_title`, `create_batch_attendance`, `attendance_add_to_batch` (its `manager_can_enter` is commented out, `views.py:1645`).
  - `on_time_view` (unscoped `AttendanceFilters(request.GET).qs`, `views.py:1187`).
  - `attendance_monthly_summary_detail` and `_calendar` (any `employee_id`, `summary.py:1309,2264`).
  - `on_break_employees` and `pending_hours`.
- CBVs with only `login_required` and no queryset scoping:
  - `AttendancesListView` (`attendances-list-view/`, `cbv/attendances.py:61`), `CheckInCheckOutListView`, `DashboardOnBreak`.
  - The profile sub-tabs `HourAccountIndividualTabView`, `AllAttendancesList`, `RequestedAttendanceIndividualView`, `PenaltyAccountListView` (filter by URL `pk` only).
  - `ValidateAttendancesIndividualTabView`, whose `filtersubordinates(...) | queryset` makes the filter a no-op (`cbv/attendances.py:863-866`).
  - Detail views without `get_queryset` overrides (`MyAttendancesDetailView`, `AttendanceDetailView`, `HourAccountDetailView`, `LateComeEarlyOutDetailView`, `AttendanceListTabDetailView`).
- `NewAttendanceRequestFormView` with `?emp_id=` replaces the employee queryset with that employee (`cbv/attendance_request.py:521-526`).
- Views guarded only by `manager_can_enter` operate on any id (`validate_this_attendance`, `approve_overtime`, `approve_validate_attendance_request`, `AttendanceUpdateFormView`, `attendance_monthly_summary_conflict_resolve`). Because of how `manager_can_enter` works (§3.10), any reporting manager can act on employees outside their team.
- `cancel_attendance_request` and `bulk_reject` accept `is_reportingmanager(request)` (manager of anyone) rather than the record's own manager (`requests.py:594`, `:826`).

---

## 6. Blast radius — what breaks if this module breaks

Ordered by severity:

1. **Payroll runs and payslips (critical).** `payroll/methods/batch_run.py:167,337` and `base/views.py:366` call `get_employee_attendance_summary` → `build_monthly_summary`. `payroll/views/component_views.py:814` calls `build_monthly_summary` directly. `payroll/methods/payslip_calc.py:1124` and `payroll/methods/methods.py:248` read `AttendanceConflictResolution`. If the summary errors, batch review and run, payslip recompute and OT/LOP components fail; if it returns wrong numbers, pay is wrong (unresolved conflicts block runs). The payroll wizard template includes attendance templates unconditionally (`wizard_review.html:15,22`), so removing them breaks that page.
2. **Every authenticated page's navbar (high).** `templates/index.html:151` and `horilla_theme/.../header.html:39` include `in_out_component.html` (which uses `attendancefilters.is_clocked_in`, `base.horillafilters.is_check_in_enabled` → `AttendanceGeneralSetting`, and `Employee.get_forecasted_at_work`). A template or model error there renders on every page while the app is installed.
3. **Check-in from all channels (high).** Web `clock-in/`/`clock-out/`, mobile `/api/attendance/clock-in|clock-out/` (`horilla_api/api_views/attendance/views.py:184,227`), biometric device sync (`biometric/views.py:30-32`), activity import and `auto_punch_out` all go through `views/clock_in_out.py`. One bug there stops time capture everywhere.
4. **URL loading and import-time patches (high).** `attendance/urls.py` imports every CBV module, and `cbv/attendances.py` patches `employee` classes at import. An import error in any of them makes `include("attendance.urls")` fail in `AttendanceConfig.ready()`, and with it app startup. It would also drop the employee list's Online/Offline status, the `working_today`/`present_on`/… filters the main dashboard KPI cards link to (`filters.py`), and the employee profile "Attendance" and "Penalty Account" tabs.
5. **Leave ↔ work records (medium-high).** `leave/signals.py:87,102` and `leave/methods.py:116` write and read `WorkRecords`, and `CompensatoryLeaveRequest` has an M2M to `Attendance` (`leave/models.py:2455`). A schema or migration break in `attendance` breaks leave approval and deletion side effects and the compensatory-leave day counts.
6. **Dashboards and reports (medium).** `base/dashboard.py:566,668,1384,1973,1989` (main HR dashboard attendance widgets and charts) and `base/ess_dashboard.py:138,345,382,509` (employee self-service calendar via `_build_calendar_context`). `report/*` attendance metrics and the attendance report (`report/metrics/time_leave.py`, `report/views/attendance_report.py`). `employee/not_in_out_dashboard.py`. `horilla_theme/overrides.py:560`.
7. **Mobile API surface (medium).** All `/api/attendance/*` endpoints (`horilla_api/api_urls/attendance/urls.py`) and the mobile home (`horilla_api/api_views/mobile/views.py:24`). The star imports make them brittle to any change in `attendance/views/views.py`.
8. **Other apps' templates (medium).** `onboarding`, `offboarding`, `payroll` (group payslips), `pms` (OKR group-by) and `recruitment` templates `{% load attendancefilters %}`. If the app is removed or the library raises at import, those pages fail with `TemplateSyntaxError`.
9. **Base schema coupling (medium, structural).** `base.EmployeeShift.grace_time_id` (PROTECT, so deleting a grace time assigned to a shift is blocked) and `base.PenaltyAccounts.late_early_id` (CASCADE, so deleting a late/early record deletes its penalties) exist only when attendance is installed. Toggling the app changes the `base` schema.
10. **Smaller consumers (low).** `whatsapp/utils.py:753` (attendance requests over WhatsApp through the unrouted `request_new`), `project/models.py:20` (`validate_time_format`), `biometric/sidebar.py` (inserts into `SUBMENUS`), `horilla_crumbs` breadcrumbs for attendance URL names, `horilla.testkit` factories and the payroll/base/report test suites that build attendance fixtures.
