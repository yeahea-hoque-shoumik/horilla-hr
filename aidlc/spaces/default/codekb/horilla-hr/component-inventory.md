# Component Inventory: horilla-hr

Commit f2ab49933cfb40d295b3a9e65eba21996df2b0dc. Each component below is one Django app (top-level folder). "Lines" counts non-migration Python. Business rules for each domain are in `business-overview.md` §4; this file lists what each component holds and what it depends on.

Summary: 33 installed first-party apps (31 in `INSTALLED_APPS` at `horilla/settings/base.py:46-104`, plus `geofencing` and `facedetection` appended by `horilla_api/__init__.py`), 3 shipped but not installed, plus the `horilla` project package and the vendored `notifications`.

## Core HR domains

### base
- **Responsibility**: organisation (companies, departments, positions, roles, employee types, work types, tags), shifts and schedules, rotating shifts and work types, rosters, shift and work-type requests, holidays and weekly offs, announcements, mail servers and templates, multi-level approval conditions, penalty accounts, attendance IP allow-list, late/early tracking switch, dashboards, settings pages, setup wizard, company and timezone middleware, company-scoped permission backend.
- **Key models** (`base/models.py`, 3,364 lines): `Company`, `CompanyGroupAssignment`, `Department`, `JobPosition`, `JobRole`, `WorkType`, `RotatingWorkType`, `RotatingWorkTypeAssign`, `EmployeeType`, `EmployeeShiftDay`, `EmployeeShift`, `EmployeeShiftSchedule`, `RotatingShift`, `RotatingShiftAssign`, `Roster`, `RosterPublishLog`, `WorkTypeRequest`, `ShiftRequest`, `Tags`, `HorillaMailTemplate`, `DynamicEmailConfiguration`, `MultipleApprovalCondition`, `MultipleApprovalManagers`, `DynamicPagination`, `Announcement`, `AnnouncementExpire`, `AnnouncementView`, `EmailLog`, `DashboardEmployeeCharts`, `BiometricAttendance`, `AttendanceAllowedIP`, `TrackLateComeEarlyOut`, `Holidays`, `CompanyLeaves`, `PenaltyAccounts`, `NotificationSound`, `IntegrationApps`, `SetupChecklistDismissal`, `DefaultExportPermission`, `CompanyLanguageSetting`.
- **Scheduled jobs** (`base/scheduler.py`): `rotate_shift` (job1), `rotate_work_type` (job2), `undo_shift` (job3), `switch_shift` (job4), `switch_work_type` (job5), `undo_work_type` (job6), `recurring_holiday`, `sync_roster_shifts`; all every 4 h.
- **Signals** (`base/signals.py`): company created → announcement-expiry and export-permission rows; penalty saved/deleted → payroll deduction and leave cut/restore; post-migrate → shift days, default role groups, export permissions; announcement/policy targets → employees; failed login logged.
- **Middleware** (`base/middleware.py`): `CompanyMiddleware`, `UserTimezoneMiddleware` (fork), `ForcePasswordChangeMiddleware`, `TwoFactorAuthMiddleware`.
- **Size**: 131 Python files, ~54.5k lines, 261 templates, 450 routes, 25 test files (224 tests).
- **Depends on**: `horilla`, `horilla_auth`, `employee`, `horilla_views`, `notifications`; optional `attendance`, `leave`, `payroll` (fields and signals guarded by `apps.is_installed`).
- **Flags**: December crash in monthly rotation; roster never reverted (see business-overview §6 #10-11).

### employee
- **Responsibility**: the person record and work information (including fork timezone), bank details, notes, policies, disciplinary actions and action types, bonus points, general settings (badge prefix), profile-edit feature switch, org chart, birthdays, employee dashboards, archive/replace/delete.
- **Key models** (`employee/models.py`, 1,589 lines): `Employee`, `EmployeeTag`, `EmployeeWorkInformation`, `EmployeeBankDetails`, `NoteFiles`, `EmployeeNote`, `PolicyMultipleFile`, `Policy`, `BonusPoint`, `Actiontype`, `DisciplinaryAction`, `EmployeeGeneralSetting`, `ProfileEditFeature`.
- **Scheduled jobs** (`employee/scheduler.py`): `update_experience` (4 h), `block_unblock_disciplinary` (60 s).
- **Signals**: employee created → bonus-point account (`employee/models.py:1361-1378`).
- **Size**: 40 files, ~17.9k lines, 150 templates, 232 routes, 3 test files (21 tests).
- **Depends on**: `base`, `horilla_auth`, `horilla_audit`, `accessibility`, `horilla_views`; patched at import time by `attendance` (filters, list status dots, profile tabs).
- **Flags**: disciplinary job can override manual blocks (§6 #12).

### attendance
- **Responsibility**: check-in/out and activities, daily attendance, validation, overtime and hours balance, grace time, late/early with penalties, attendance requests and batches, daily work status, monthly summary and regularisation for payroll, settings and dashboards. Full module reference in `attendance/MODULE_SUMMARY.md`.
- **Key models** (`attendance/models.py`, 2,094 lines): `AttendanceActivity`, `BatchAttendance`, `Attendance`, `AttendanceRequestFile`, `AttendanceRequestComment`, `AttendanceOverTime`, `AttendanceLateComeEarlyOut`, `AttendanceValidationCondition`, `GraceTime`, `AttendanceGeneralSetting`, `WorkRecords`, `AttendanceConflictResolution`, `AttendanceSummaryHours`, `AttendanceSummaryOverride`, `AttendanceDailyHours`.
- **Key logic**: `attendance/views/clock_in_out.py` (all punch channels), `attendance/views/summary.py` (`build_monthly_summary`), `attendance/methods/utils.py` (`get_employee_attendance_summary` used by payroll, `employee_localtime` from the fork).
- **Scheduled jobs**: `create_work_record` (30 min), `create_daily_work_record` (00:30), `auto_punch_out` (5 min).
- **Signals** (`attendance/signals.py`): attendance saved → daily work status; attendance deleted → remove non-leave work records; company created → attendance settings row.
- **Size**: 64 files, ~26.3k lines, 148 templates, 228 routes, 16 test files (161 tests).
- **Depends on**: `base`, `employee`, `leave` (hard import in summary; migration dependency), `geofencing` (unguarded import), `horilla_views`, `horilla_audit`, `notifications`; optional `facedetection`, `biometric`.
- **Flags**: §6 #14-17.

### leave
- **Responsibility**: leave types and eligibility, assigned balances, requests with half days, multi-level approval stages, allocation requests, compensatory leave, restricted periods, past-date restriction, reset and carry-forward, leave dashboards.
- **Key models** (`leave/models.py`, 2,765 lines): `LeaveTypeCondition`, `LeaveType`, `AvailableLeave`, `LeaveRequest`, `LeaverequestFile`, `LeaverequestComment`, `LeaveAllocationRequest`, `LeaveallocationrequestComment`, `LeaveRequestConditionApproval`, `RestrictLeave`, `CompensatoryLeaveRequest` (only with attendance), `LeaveGeneralSetting`, `CompensatoryLeaverequestComment` (only with attendance), `EmployeePastLeaveRestrict`.
- **Key logic**: `leave/views.py` (approve 1044, bulk approve 1251, reject helper 1281, cancel 1375-1610, allocation approve 4519), `leave/services.py` (eligibility conditions, balance check), `leave/methods.py`.
- **Scheduled jobs**: `leave_reset` (4 h).
- **Signals** (`leave/signals.py`): leave saved/deleted → attendance work records; approval stage created → auto-approve when the approver is the requester.
- **Size**: 49 files, ~20.7k lines, 166 templates, 210 routes, 16 test files (120 tests).
- **Depends on**: `base` (holidays, company leaves, approval conditions), `employee`, `attendance` (work records, compensatory leave), `horilla_audit`, `notifications`.
- **Flags**: §6 #2-6.

### payroll
- **Responsibility**: contracts, filing status and tax brackets, salary structures, allowances and deductions with conditions and formulas, component library and system components, payslips, payroll runs, pay periods, auto payslip generation, loans/advances/fines, reimbursements and encashments, contributions and employer cost, payroll dashboard.
- **Key models** (`payroll/models/models.py` 4,369 lines, `payroll_batch.py` 425, `tax_models.py` 160): `FilingStatus`, `Contract`, `WorkRecord` (payroll's own), `MultipleCondition`, `ApplyCondition`, `Allowance`, `Deduction`, `SalaryStructure`, `Payslip`, `LoanAccount`, `ReimbursementMultipleAttachment`, `Reimbursement`, `ReimbursementFile`, `ReimbursementrequestComment`, `PayrollGeneralSetting`, `EncashmentGeneralSettings`, `PayslipAutoGenerate`, `PayPeriodSettings`, `PayrollBatch`, `PayrollBatchLine`, `PayrollSettings`, `TaxBracket`.
- **Key logic** (`payroll/methods/`): `component_engine.py`, `component_formula.py`, `payslip_calc.py`, `payroll_run.py`, `batch_run.py`, `tax_calc.py`, `federal_tax.py`, `safe_tax_code.py`, `structure_rules.py`, `proration.py`, `limits.py`, `earning_working.py`, `payslip_edit.py`, `contributions.py`, `employer_cost.py`; `payroll/tax_packs.py`, `payroll/component_library.py`, `payroll/system_components.py`.
- **Management commands**: `backfill_component_sequence`, `check_structure_invariants`, `create_payroll_fixtures`, `create_precise_payroll_fixtures`, `normalise_component_basis`, `normalise_payslip_basic_pay`, `normalise_payslip_deductions`, `payroll_snapshot`, `report_lop_deduction_mode`, `seed_tax_packs`, `sync_system_components`.
- **Scheduled jobs**: `expire_contract` (4 h), `auto_payslip_generate` (3 h).
- **Signals** (`payroll/signals.py`): encashment settings targets; work information saved → payroll sync; loan created → payout allowance and installments.
- **Size**: 134 files, ~48.3k lines, 182 templates, 239 routes, 39 test files (850 tests).
- **Depends on**: `base`, `employee`, `attendance` (monthly summary, conflicts), `leave` (encashment, loss of pay), `asset` (fines, optional), `horilla_views`, `notifications`.
- **Flags**: §6 #7-8.

### recruitment
- **Responsibility**: job openings, pipeline stages, candidates, rejections, notes and files, surveys and application forms, talent pool, ratings, interviews, resume screening, candidate document requests, LinkedIn posting, candidate self-tracking login.
- **Key models** (`recruitment/models.py`, 2,126 lines): `SurveyTemplate`, `Skill`, `Recruitment`, `Stage`, `Candidate`, `RejectReason`, `RejectedCandidate`, `StageFiles`, `StageNote`, `RecruitmentSurvey`, `QuestionOrdering`, `RecruitmentSurveyAnswer`, `SkillZone`, `SkillZoneCandidate`, `CandidateRating`, `RecruitmentGeneralSetting`, `InterviewSchedule`, `Resume`, `CandidateDocumentRequest`, `CandidateDocument`, `LinkedInAccount`.
- **Scheduled jobs**: `candidate_convert` (5 min), `recruitment_close` (1 h).
- **Signals**: recruitment created → initial stage; stage saved/deleted → pipeline cache version; document request candidates → document slots.
- **Size**: 54 files, ~21.8k lines, 184 templates, 271 routes, 7 test files (28 tests).
- **Depends on**: `base`, `employee`, `horilla_meet`, `horilla_views`, spaCy, PyMuPDF.
- **Flags**: §6 #9.

### onboarding
- **Responsibility**: onboarding stages and tasks, candidate stages and tasks, tokenised onboarding portal, conversion of hired candidates to employees.
- **Key models** (`onboarding/models.py`, 288 lines): `OnboardingStage`, `OnboardingTask`, `OnboardingCandidate` (proxy of `Candidate`), `CandidateStage`, `CandidateTask`, `OnboardingPortal`.
- **Size**: 24 files, ~6.7k lines, 54 templates, 82 routes, 1 test file (1 test).
- **Depends on**: `recruitment`, `employee`, `base`.
- **Flags**: §6 #22; very thin test coverage.

### offboarding
- **Responsibility**: exit pipelines and stages, offboarding employees with notice periods, exit tasks, resignation letters, exit reasons, notes, general settings.
- **Key models** (`offboarding/models.py`, 704 lines): `Offboarding`, `OffboardingStage`, `OffboardingStageMultipleFile`, `OffboardingEmployee`, `ResignationLetter`, `OffboardingTask`, `EmployeeTask`, `ExitReason`, `OffboardingNote`, `OffboardingGeneralSetting`.
- **Size**: 23 files, ~6.9k lines, 52 templates, 81 routes, 3 test files (9 tests).
- **Depends on**: `employee`, `base`, `payroll` (default notice period, optional).
- **Flags**: §6 #19.

### pms
- **Responsibility**: periods, objectives and key results, employee objectives and key results, comments, question templates, 360 feedback and cyclic rounds, anonymous feedback, 1:1 meetings, bonus point awarding rules.
- **Key models** (`pms/models.py`, 1,903 lines): `Period`, `KeyResult`, `Objective`, `EmployeeObjective`, `Comment`, `EmployeeKeyResult`, `QuestionTemplate`, `Question`, `QuestionOptions`, `Feedback`, `AnonymousFeedback`, `Answer`, `KeyResultFeedback`, `Meetings`, `MeetingsAnswer`, `EmployeeBonusPoint`, `BonusPointSetting`.
- **Scheduled jobs**: `cyclic_feedback_creation` (daily 08:00).
- **Signals** (`pms/signals.py`): runtime-connected handlers for bonus point rules.
- **Size**: 31 files, ~15k lines, 128 templates, 220 routes, 3 test files (19 tests).
- **Depends on**: `employee`, `base`, `notifications`.

### project
- **Responsibility**: projects, stages, tasks, timesheets, project dashboard.
- **Key models** (`project/models.py`, 799 lines): `Project`, `ProjectStage`, `Task`, `TimeSheet`.
- **Size**: 24 files, ~7.7k lines, 70 templates, 100 routes, 1 test file (2 tests).
- **Depends on**: `employee`, `base`, `attendance` (time format validator).
- **Flags**: §6 #20.

### asset
- **Responsibility**: asset categories, lots, assets and items, reports and documents, return images, assignments and returns, asset requests, service requests; expiry jobs for assets and (misplaced) employee documents.
- **Key models** (`asset/models.py`, 1,122 lines): `AssetCategory`, `AssetGeneralSetting`, `AssetLot`, `Asset`, `AssetItem`, `AssetReport`, `AssetDocuments`, `ReturnImages`, `AssetAssignment`, `AssetRequest`, `AssetRequestComment`, `AssetServiceRequest`, `AssetServiceRequestNote`.
- **Scheduled jobs** (`asset/scheduler.py`): `notify_expiring_assets` (daily), `mark_expired_assets` (daily), `notify_expiring_documents` (4 h, for `horilla_documents`).
- **Size**: 25 files, ~9.2k lines, 87 templates, 124 routes, 2 test files (16 tests).
- **Depends on**: `employee`, `base`, `horilla_documents`, `payroll` (fines, optional).
- **Flags**: §6 #13.

### helpdesk
- **Responsibility**: tickets, ticket types, claim requests, comments, attachments, department managers, FAQ categories and FAQs.
- **Key models** (`helpdesk/models.py`, 586 lines): `DepartmentManager`, `TicketType`, `Ticket`, `ClaimRequest`, `Comment`, `Attachment`, `FAQCategory`, `FAQ`.
- **Size**: 28 files, ~6.5k lines, 37 templates, 100 routes, 4 test files (11 tests).
- **Depends on**: `employee`, `base`.
- **Flags**: §6 #21.

### report
- **Responsibility**: 34 standard reports with filters, comparison, drill-down, KPIs, narrative, exports (Excel/CSV/PDF), personalisation, access matrix, subscriptions, pivot Explorer templates.
- **Key models** (`report/models.py`, 463 lines): `ReportTemplate`, `ReportSubscription`, `ReportFavorite`, `ReportSavedView`, `ReportFilterPreset`, `ReportRunLog`, `ReportAccess`.
- **Key logic**: `report/registry.py`, `report/engine.py`, `report/metrics/` (workforce, time_leave, payroll, talent, compliance, definitions), `report/delivery.py`, `report/export.py`, `report/async_export.py`, `report/access.py`.
- **Scheduled jobs**: `report_subscriptions` (1 h); command `run_report_subscriptions`.
- **Size**: 62 files, ~20.7k lines, 6 templates, 63 routes, 4 test files (114 tests).
- **Depends on**: every domain app it reports on (employee, attendance, leave, payroll, recruitment, onboarding, offboarding, pms, asset, horilla_documents, auditlog).

## Attendance capture channels

### biometric
- **Responsibility**: biometric devices (ZKTeco/eSSL, Anviz, Matrix COSEC, Dahua, e-Time Office), device users mapped to employees by badge ID, live capture and polling, conversion of logs into check-ins/outs.
- **Key models** (`biometric/models.py`): `BiometricDevices`, `BiometricEmployees`, `COSECAttendanceArguments`.
- **Scheduled jobs**: `biometric.poll_devices` (registered in `biometric/views.py:2704`); plus in-process schedulers started from views (`biometric/views.py:431-504`, `biometric/cbv/biometric.py:288-335`).
- **Size**: 18 files, ~5.8k lines, 30 templates, 32 routes, 5 tests.
- **Depends on**: `attendance` (`clock_in`, `clock_out`), `employee`, `base`, pyzk.

### geofencing
- **Responsibility**: company location and radius; check whether a mobile or web punch is inside it.
- **Key models**: `GeoFencing` (one per company).
- **Routes**: `/api/geofencing/` (5). Installed by `horilla_api/__init__.py`.
- **Depends on**: `base`, geopy.

### facedetection
- **Responsibility**: per-company face-check switch and a reference face image per employee for the mobile app.
- **Key models**: `FaceDetection`, `EmployeeFaceDetection`.
- **Routes**: `/api/facedetection/` (4). Installed by `horilla_api/__init__.py`.
- **Flags**: no server-side face comparison (§6 #17).

## API

### horilla_api
- **Responsibility**: REST API for the mobile app: auth (login, refresh, logout, reset password), base, employee, attendance, leave, payroll, recruitment, onboarding, offboarding, pms, helpdesk, project, asset, notifications, mobile home; capabilities payload; Swagger/ReDoc; tenant-scoped JWT authentication that also activates the user's timezone (fork).
- **Structure**: `api_urls/<domain>/urls.py`, `api_views/<domain>/`, `api_serializers/`, `api_filters/`, `api_methods/`, `api_decorators/`, `authentication.py`.
- **Size**: 116 files, ~22.6k lines, about 360 routes, 27 test files (167 tests).
- **Depends on**: every domain app; star imports from `attendance.views.views` and `attendance.views.clock_in_out`.
- **Flags**: leave approval re-implemented with a different deduction order (§6 #2).

## Platform and shared services

### horilla
- **Responsibility**: project package: settings (`base.py`, `security.py`, `addons.py`, `local_settings.py`), root URLs and health/ready/metrics, `HorillaModel` base model with XSS check and audit fields, decorators, scheduling registry, model extension (`inherit/`), menus, observability (logging, Sentry, request ID, access-log bodies from the fork), storage backends, test kit.
- **Size**: 48 files, ~6k lines, 6 test files (37 tests, not in CI smoke labels).

### horilla_auth
- **Responsibility**: custom user model `HorillaUser` (`AUTH_USER_MODEL`), legacy user migration.
- **Key models**: `HorillaUser`, `LegacyUser`, `AuthUserGroups`, `AuthUserUserPermissions`.

### accessibility
- **Responsibility**: feature-level access rules (default employee view, detailed view, profile edit, dashboard charts, birthdays) and the middleware that applies them.
- **Key models**: `DefaultAccessibility`.

### horilla_audit
- **Responsibility**: history/audit configuration, audit tags, history tracking fields per company, account block/unblock, audit model registry.
- **Key models**: `AuditTag`, `HorillaAuditInfo`, `HorillaAuditLog`, `HistoryTrackingFields`, `AccountBlockUnblock`, `AuditModelConfig`.

### horilla_views
- **Responsibility**: generic list, card, kanban, pipeline, detail, tab, form and history views; per-user UI preferences.
- **Key models**: `ToggleColumn`, `ActiveTab`, `ActiveGroup`, `SavedFilter`, `ActiveView`, `ColumnOrder`.

### horilla_theme
- **Responsibility**: Tailwind theme and template overrides (413 templates, which shadow app templates), colour themes per company.
- **Key models**: `HorillaColorTheme`, `CompanyTheme`.

### horilla_widgets
- **Responsibility**: custom form widgets and AJAX select/filter helpers.

### horilla_crumbs
- **Responsibility**: breadcrumbs (HTMX fragment and context processor).

### horilla_documents
- **Responsibility**: employee document requests, uploads, approval, expiry.
- **Key models**: `DocumentRequest`, `Document`.

### horilla_automations
- **Responsibility**: no-code mail/notification automations on model create, update and delete.
- **Key models**: `MailAutomation`.

### horilla_dbtemplate
- **Responsibility**: templates stored in the database with versions, activation windows, per-site and per-language overrides; the first template loader.
- **Key models**: `Template`, `TemplateVersion`.

### horilla_tour
- **Responsibility**: guided product tours with steps and per-user progress.
- **Key models**: `Tour`, `TourStep`, `TourProgress`.

### master_import
- **Responsibility**: spreadsheet import wizard for employees, employee updates, assets, asset allocations, assigned leave, salary structures.
- **Key models**: `ImportJob`. Datasets in `master_import/datasets/`.
- **Size**: 17 files, ~6.7k lines, 1 test file (132 tests, not in CI smoke labels).

### notifications
- **Responsibility**: vendored `django-notifications` (in-app notifications, inbox, mark read); excluded from ruff and coverage.

## Integrations

### horilla_backup
- **Responsibility**: Google Drive backups of the database dump and media.
- **Key models**: `LocalBackup`, `GoogleDriveBackup`. Runs its own in-process scheduler (`horilla_backup/scheduler.py:21`).

### horilla_meet
- **Responsibility**: Google OAuth per employee; create and delete Google Meet links for interviews and meetings.
- **Key models**: `GoogleCloudCredential`, `GoogleCredential`, `GoogleMeeting`.

### horilla_ldap
- **Responsibility**: LDAP settings page and import/export commands.
- **Key models**: `LDAPSettings`.
- **Flags**: login backend commented out; LDAP libraries not in requirements (§6 #23).

### whatsapp
- **Responsibility**: WhatsApp Business credentials, templates and flows; self-service requests through WhatsApp; WhatsApp notifications and announcements; webhook.
- **Key models**: `WhatsappCredientials`, `WhatsappFlowDetails`.

## Shipped but not installed

### outlook_auth
- **Responsibility**: Microsoft 365 mail through Azure OAuth, token refresh job every 50 min. Not in `INSTALLED_APPS`.
- **Key models**: `AzureApi`.

### dynamic_fields
- **Responsibility**: add custom fields to models at runtime (`/df/`). Not in `INSTALLED_APPS`.
- **Key models**: `Choice`, `DynamicField`.

### pg_backup
- **Responsibility**: local PostgreSQL dump scheduler with its own in-process scheduler. Not in `INSTALLED_APPS`.

## Non-app folders

| Folder / file | Purpose |
|---|---|
| `templates/` | Root templates (index, login, dashboard, sidebar, errors, setup wizard) |
| `static/` | Vendored front-end libraries and app static files |
| `load_data/` | Demo fixtures (JSON) and avatars |
| `docs/` | Fork-written product and DB documentation |
| `docker/` | `entrypoint.sh`, `gunicorn.conf.py`, `nginx.conf` (no longer used in fork prod), Docker Hub notes |
| `deploy.sh` | Fork deploy script: `init-env`, `setup-db`, deploy with DB backup, `status`, `logs`, `stop` |
| `fk_dependency_tree.py`, `fk_tree.html` | Fork tool and output for the foreign-key dependency tree |
| `perm_baseline.json` | Snapshot from `audit_perms` |
| `auth/login.html`, `media/` | Login template copy; uploads folder (gitignored) |
