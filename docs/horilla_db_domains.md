# horilla_db — Data Schemas by Domain

Generated from `docs/horilla_db.dbml` (live PostgreSQL, schema `public`). Groups all tables into business domains. FK dependency order lives in [`horilla_db_dependency_tree.md`](horilla_db_dependency_tree.md).

**Table kinds**

- **Core**: main entity tables.
- **Link**: many-to-many join tables (`id` + two FKs), e.g. `base_department_company_id`.
- **History**: `django-simple-history` audit copies (`historical*`, `*_history_tags`).

`References` lists the tables each core table has FKs to. `horilla_auth_horillauser` (`created_by` / `modified_by`) is left out because nearly every table references it.

## Summary

| # | Domain | Core | Link | History | Total |
|---|---|---:|---:|---:|---:|
| 1 | [Organization structure](#1-organization-structure) | 7 | 4 | 0 | 11 |
| 2 | [Employee information](#2-employee-information) | 8 | 2 | 2 | 12 |
| 3 | [Employee discipline, bonus & policies](#3-employee-discipline-bonus--policies) | 5 | 7 | 2 | 14 |
| 4 | [Shifts & rosters](#4-shifts--rosters) | 9 | 4 | 4 | 17 |
| 5 | [Work types](#5-work-types) | 5 | 2 | 4 | 11 |
| 6 | [Attendance](#6-attendance) | 18 | 4 | 4 | 26 |
| 7 | [Attendance capture (biometric / face / geofence)](#7-attendance-capture-biometric--face--geofence) | 7 | 0 | 0 | 7 |
| 8 | [Leave & holidays](#8-leave--holidays) | 17 | 12 | 8 | 37 |
| 9 | [Payroll](#9-payroll) | 23 | 18 | 4 | 45 |
| 10 | [Recruitment](#10-recruitment) | 21 | 12 | 6 | 39 |
| 11 | [Onboarding](#11-onboarding) | 5 | 3 | 2 | 10 |
| 12 | [Offboarding](#12-offboarding) | 10 | 5 | 4 | 19 |
| 13 | [Performance (PMS)](#13-performance-pms) | 17 | 14 | 10 | 41 |
| 14 | [Assets](#14-assets) | 13 | 4 | 0 | 17 |
| 15 | [Helpdesk](#15-helpdesk) | 8 | 3 | 2 | 13 |
| 16 | [Projects & timesheets](#16-projects--timesheets) | 4 | 3 | 0 | 7 |
| 17 | [Documents](#17-documents) | 2 | 1 | 0 | 3 |
| 18 | [Communication & notifications](#18-communication--notifications) | 12 | 9 | 0 | 21 |
| 19 | [Shared approvals, files & tags](#19-shared-approvals-files--tags) | 5 | 0 | 0 | 5 |
| 20 | [Reports & dashboards](#20-reports--dashboards) | 9 | 1 | 0 | 10 |
| 21 | [Users, auth & access control](#21-users-auth--access-control) | 13 | 4 | 0 | 17 |
| 22 | [Audit & history](#22-audit--history) | 6 | 0 | 0 | 6 |
| 23 | [UI preferences & personalization](#23-ui-preferences--personalization) | 13 | 0 | 0 | 13 |
| 24 | [Integrations, backup & system](#24-integrations-backup--system) | 14 | 1 | 0 | 15 |
| | **Total** | **251** | **113** | **52** | **416** |

## Cross-domain dependencies

Which domains each domain's tables point to through FKs (users table excluded).

| Domain | Depends on |
|---|---|
| Organization structure | Users, auth & access control (1) |
| Employee information | Organization structure (6), Shifts & rosters (1), Work types (1), Audit & history (1) |
| Employee discipline, bonus & policies | Employee information (4), Organization structure (3), Audit & history (1) |
| Shifts & rosters | Employee information (7), Organization structure (5), Audit & history (2), Attendance (1), Shared approvals, files & tags (1) |
| Work types | Employee information (3), Audit & history (2), Organization structure (1), Shared approvals, files & tags (1) |
| Attendance | Employee information (12), Shifts & rosters (5), Organization structure (5), Leave & holidays (3), Audit & history (2), Work types (1) |
| Attendance capture (biometric / face / geofence) | Organization structure (4), Employee information (2) |
| Leave & holidays | Organization structure (10), Employee information (10), Audit & history (4), Attendance (1) |
| Payroll | Organization structure (14), Employee information (14), Shifts & rosters (2), Work types (2), Audit & history (2), Leave & holidays (2), Assets (1) |
| Recruitment | Organization structure (10), Employee information (7), Audit & history (3), Integrations, backup & system (1) |
| Onboarding | Recruitment (5), Employee information (2), Audit & history (1) |
| Offboarding | Employee information (6), Audit & history (2), Organization structure (2) |
| Performance (PMS) | Employee information (17), Organization structure (8), Audit & history (5), Integrations, backup & system (1), Employee discipline, bonus & policies (1) |
| Assets | Employee information (8), Organization structure (3) |
| Helpdesk | Employee information (5), Organization structure (5), Shared approvals, files & tags (2), Audit & history (1) |
| Projects & timesheets | Employee information (4), Organization structure (1) |
| Documents | Employee information (2) |
| Communication & notifications | Organization structure (8), Employee information (5), Integrations, backup & system (3), Shared approvals, files & tags (1) |
| Shared approvals, files & tags | Organization structure (3) |
| Reports & dashboards | Organization structure (7), Employee information (2), Users, auth & access control (1) |
| Users, auth & access control | Employee information (1), Integrations, backup & system (1), Organization structure (1) |
| Audit & history | Integrations, backup & system (2), Organization structure (1) |
| UI preferences & personalization | Organization structure (4), Employee information (1) |
| Integrations, backup & system | Organization structure (3), Employee information (2) |

## 1. Organization structure

Companies, departments, job positions/roles, employee types. Most other domains point here.

| Table | Cols | References |
|---|---:|---|
| `base_company` | 15 | — |
| `base_companygroupassignment` | 8 | `auth_group`, `base_company` |
| `base_companylanguagesetting` | 7 | `base_company` |
| `base_department` | 6 | — |
| `base_employeetype` | 6 | — |
| `base_jobposition` | 7 | `base_department` |
| `base_jobrole` | 7 | `base_jobposition` |

**Link tables (4)**

- `base_department_company_id` — `base_company` ↔ `base_department`
- `base_employeetype_company_id` — `base_company` ↔ `base_employeetype`
- `base_jobposition_company_id` — `base_company` ↔ `base_jobposition`
- `base_jobrole_company_id` — `base_company` ↔ `base_jobrole`

## 2. Employee information

Employee master record, work info, bank details, notes, tags, profile settings.

| Table | Cols | References |
|---|---:|---|
| `employee_employee` | 26 | — |
| `employee_employeebankdetails` | 16 | `employee_employee` |
| `employee_employeegeneralsetting` | 7 | `base_company` |
| `employee_employeenote` | 8 | `employee_employee` |
| `employee_employeetag` | 7 | — |
| `employee_employeeworkinformation` | 19 | `base_company`, `base_department`, `base_employeeshift`, `base_employeetype`, `base_jobposition`, `base_jobrole`, `base_worktype`, `employee_employee` |
| `employee_notefiles` | 6 | — |
| `employee_profileeditfeature` | 6 | — |

**Link tables (2)**

- `employee_employeenote_note_files` — `employee_employeenote` ↔ `employee_notefiles`
- `employee_employeeworkinformation_tags` — `employee_employeetag` ↔ `employee_employeeworkinformation`

**History tables (2)**

`employee_historicalemployeeworkinformation`, `employee_historicalemployeeworkinformation_history_tags`

## 3. Employee discipline, bonus & policies

Disciplinary actions, bonus points, company policies.

| Table | Cols | References |
|---|---:|---|
| `employee_actiontype` | 8 | — |
| `employee_bonuspoint` | 10 | `employee_employee` |
| `employee_disciplinaryaction` | 12 | `employee_actiontype` |
| `employee_policy` | 8 | — |
| `employee_policymultiplefile` | 6 | — |

**Link tables (7)**

- `employee_disciplinaryaction_employee_id` — `employee_disciplinaryaction` ↔ `employee_employee`
- `employee_policy_attachments` — `employee_policy` ↔ `employee_policymultiplefile`
- `employee_policy_company_id` — `base_company` ↔ `employee_policy`
- `employee_policy_department` — `base_department` ↔ `employee_policy`
- `employee_policy_employees` — `employee_employee` ↔ `employee_policy`
- `employee_policy_filtered_employees` — `employee_employee` ↔ `employee_policy`
- `employee_policy_job_position` — `base_jobposition` ↔ `employee_policy`

**History tables (2)**

`employee_historicalbonuspoint`, `employee_historicalbonuspoint_history_tags`

## 4. Shifts & rosters

Shift definitions, shift days/schedules, rotating shifts, shift requests, rosters.

| Table | Cols | References |
|---|---:|---|
| `base_employeeshift` | 9 | `attendance_gracetime` |
| `base_employeeshiftday` | 2 | — |
| `base_employeeshiftschedule` | 13 | `base_employeeshift`, `base_employeeshiftday` |
| `base_roster` | 12 | `base_department`, `base_employeeshift`, `employee_employee` |
| `base_rosterpublishlog` | 7 | `base_department`, `employee_employee` |
| `base_rotatingshift` | 9 | `base_employeeshift` |
| `base_rotatingshiftassign` | 16 | `base_employeeshift`, `base_rotatingshift`, `employee_employee` |
| `base_shiftrequest` | 18 | `base_employeeshift`, `employee_employee` |
| `base_shiftrequestcomment` | 8 | `base_shiftrequest`, `employee_employee` |

**Link tables (4)**

- `base_employeeshift_company_id` — `base_company` ↔ `base_employeeshift`
- `base_employeeshiftday_company_id` — `base_company` ↔ `base_employeeshiftday`
- `base_employeeshiftschedule_company_id` — `base_company` ↔ `base_employeeshiftschedule`
- `base_shiftrequestcomment_files` — `base_baserequestfile` ↔ `base_shiftrequestcomment`

**History tables (4)**

`base_historicalrotatingshiftassign`, `base_historicalrotatingshiftassign_history_tags`, `base_historicalshiftrequest`, `base_historicalshiftrequest_history_tags`

## 5. Work types

Work type (office/remote/etc.) definitions, rotating work types, work type requests.

| Table | Cols | References |
|---|---:|---|
| `base_rotatingworktype` | 9 | `base_worktype` |
| `base_rotatingworktypeassign` | 16 | `base_rotatingworktype`, `base_worktype`, `employee_employee` |
| `base_worktype` | 6 | — |
| `base_worktyperequest` | 15 | `base_worktype`, `employee_employee` |
| `base_worktyperequestcomment` | 8 | `base_worktyperequest`, `employee_employee` |

**Link tables (2)**

- `base_worktype_company_id` — `base_worktype` ↔ `base_company`
- `base_worktyperequestcomment_files` — `base_baserequestfile` ↔ `base_worktyperequestcomment`

**History tables (4)**

`base_historicalrotatingworktypeassign`, `base_historicalrotatingworktypeassign_history_tags`, `base_historicalworktyperequest`, `base_historicalworktyperequest_history_tags`

## 6. Attendance

Clock in/out, activities, overtime, late/early, validation, grace time, daily/summary hours, requests.

| Table | Cols | References |
|---|---:|---|
| `attendance_attendance` | 31 | `attendance_batchattendance`, `base_employeeshift`, `base_employeeshiftday`, `base_worktype`, `employee_employee` |
| `attendance_attendanceactivity` | 14 | `base_employeeshiftday`, `employee_employee` |
| `attendance_attendanceconflictresolution` | 9 | `employee_employee` |
| `attendance_attendancedailyhours` | 10 | `employee_employee` |
| `attendance_attendancegeneralsetting` | 8 | `base_company` |
| `attendance_attendancelatecomeearlyout` | 8 | `attendance_attendance`, `employee_employee` |
| `attendance_attendanceovertime` | 15 | `employee_employee` |
| `attendance_attendancerequestcomment` | 8 | `attendance_attendance`, `employee_employee` |
| `attendance_attendancerequestfile` | 6 | — |
| `attendance_attendancesummaryhours` | 10 | `employee_employee` |
| `attendance_attendancesummaryoverride` | 13 | `employee_employee` |
| `attendance_attendancevalidationcondition` | 10 | — |
| `attendance_batchattendance` | 6 | — |
| `attendance_gracetime` | 10 | — |
| `attendance_workrecords` | 18 | `attendance_attendance`, `base_employeeshift`, `employee_employee`, `leave_leaverequest` |
| `base_attendanceallowedip` | 4 | `base_company` |
| `base_penaltyaccounts` | 12 | `attendance_attendancelatecomeearlyout`, `employee_employee`, `leave_leaverequest`, `leave_leavetype` |
| `base_tracklatecomeearlyout` | 7 | `base_company` |

**Link tables (4)**

- `attendance_attendancerequestcomment_files` — `attendance_attendancerequestcomment` ↔ `attendance_attendancerequestfile`
- `attendance_attendancevalidationcondition_company_id` — `attendance_attendancevalidationcondition` ↔ `base_company`
- `attendance_attendancevalidationcondition_shift_ids` — `attendance_attendancevalidationcondition` ↔ `base_employeeshift`
- `attendance_gracetime_company_id` — `base_company` ↔ `attendance_gracetime`

**History tables (4)**

`attendance_historicalattendance`, `attendance_historicalattendance_history_tags`, `attendance_historicalattendanceactivity`, `attendance_historicalattendanceactivity_history_tags`

## 7. Attendance capture (biometric / face / geofence)

Device and capture sources that feed attendance.

| Table | Cols | References |
|---|---:|---|
| `base_biometricattendance` | 3 | `base_company` |
| `biometric_biometricdevices` | 25 | `base_company` |
| `biometric_biometricemployees` | 7 | `biometric_biometricdevices`, `employee_employee` |
| `biometric_cosecattendancearguments` | 4 | `biometric_biometricdevices` |
| `facedetection_employeefacedetection` | 3 | `employee_employee` |
| `facedetection_facedetection` | 3 | `base_company` |
| `geofencing_geofencing` | 6 | `base_company` |

## 8. Leave & holidays

Leave types, balances, leave/allocation/compensatory requests, restrictions, holidays, company leaves.

| Table | Cols | References |
|---|---:|---|
| `base_companyleaves` | 7 | — |
| `base_holidays` | 12 | `base_company` |
| `leave_availableleave` | 13 | `employee_employee`, `leave_leavetype` |
| `leave_compensatoryleaverequest` | 12 | `employee_employee`, `leave_leavetype` |
| `leave_compensatoryleaverequestcomment` | 8 | `employee_employee`, `leave_compensatoryleaverequest` |
| `leave_employeepastleaverestrict` | 7 | `base_company` |
| `leave_leaveallocationrequest` | 13 | `employee_employee`, `leave_leavetype` |
| `leave_leaveallocationrequestcomment` | 8 | `employee_employee`, `leave_leaveallocationrequest` |
| `leave_leavegeneralsetting` | 7 | `base_company` |
| `leave_leaverequest` | 21 | `employee_employee`, `leave_leavetype` |
| `leave_leaverequestcomment` | 8 | `employee_employee`, `leave_leaverequest` |
| `leave_leaverequestconditionapproval` | 6 | `employee_employee`, `leave_leaverequest` |
| `leave_leaverequestfile` | 2 | — |
| `leave_leavetype` | 32 | `base_company` |
| `leave_leavetypecondition` | 7 | — |
| `leave_overrideleaverequests` | 1 | `leave_leaverequest` |
| `leave_restrictleave` | 12 | `base_company`, `base_department` |

**Link tables (12)**

- `base_companyleaves_company_id` — `base_company` ↔ `base_companyleaves`
- `base_holidays_department` — `base_department` ↔ `base_holidays`
- `base_holidays_employees` — `employee_employee` ↔ `base_holidays`
- `base_holidays_job_position` — `base_holidays` ↔ `base_jobposition`
- `leave_compensatoryleaverequest_attendance_id` — `attendance_attendance` ↔ `leave_compensatoryleaverequest`
- `leave_compensatoryleaverequestcomment_files` — `leave_compensatoryleaverequestcomment` ↔ `leave_leaverequestfile`
- `leave_leaveallocationrequestcomment_files` — `leave_leaveallocationrequestcomment` ↔ `leave_leaverequestfile`
- `leave_leaverequestcomment_files` — `leave_leaverequestcomment` ↔ `leave_leaverequestfile`
- `leave_leavetype_conditions` — `leave_leavetype` ↔ `leave_leavetypecondition`
- `leave_restrictleave_exclued_leave_types` — `leave_leavetype` ↔ `leave_restrictleave`
- `leave_restrictleave_job_position` — `base_jobposition` ↔ `leave_restrictleave`
- `leave_restrictleave_spesific_leave_types` — `leave_leavetype` ↔ `leave_restrictleave`

**History tables (8)**

`leave_historicalavailableleave`, `leave_historicalavailableleave_history_tags`, `leave_historicalcompensatoryleaverequest`, `leave_historicalcompensatoryleaverequest_history_tags`, `leave_historicalleaveallocationrequest`, `leave_historicalleaveallocationrequest_history_tags`, `leave_historicalleaverequest`, `leave_historicalleaverequest_history_tags`

## 9. Payroll

Contracts, salary structures, allowances, deductions, payslips, loans, reimbursements, tax, pay periods.

| Table | Cols | References |
|---|---:|---|
| `payroll_allowance` | 43 | `base_company`, `base_employeeshift`, `base_worktype` |
| `payroll_applycondition` | 7 | — |
| `payroll_contract` | 31 | `base_department`, `base_employeeshift`, `base_jobposition`, `base_jobrole`, `base_worktype`, `employee_employee`, `payroll_filingstatus`, `payroll_salarystructure` |
| `payroll_deduction` | 40 | `base_company` |
| `payroll_encashmentgeneralsettings` | 5 | — |
| `payroll_filingstatus` | 15 | `base_company` |
| `payroll_loanaccount` | 21 | `asset_asset`, `employee_employee`, `payroll_allowance` |
| `payroll_multiplecondition` | 4 | — |
| `payroll_overrideleaverequest` | 1 | `leave_leaverequest` |
| `payroll_payperiodsettings` | 9 | `base_company` |
| `payroll_payrollbatch` | 23 | `base_company` |
| `payroll_payrollbatchline` | 10 | `employee_employee`, `payroll_payrollbatch`, `payroll_payslip` |
| `payroll_payrollgeneralsetting` | 3 | `base_company` |
| `payroll_payrollsettings` | 8 | `base_company` |
| `payroll_payslip` | 19 | `employee_employee`, `payroll_payrollbatch` |
| `payroll_payslipautogenerate` | 4 | `base_company` |
| `payroll_reimbursement` | 19 | `employee_employee`, `leave_leavetype`, `payroll_allowance` |
| `payroll_reimbursementfile` | 2 | — |
| `payroll_reimbursementmultipleattachment` | 2 | — |
| `payroll_reimbursementrequestcomment` | 8 | `employee_employee`, `payroll_reimbursement` |
| `payroll_salarystructure` | 8 | `base_company` |
| `payroll_taxbracket` | 9 | `payroll_filingstatus` |
| `payroll_workrecord` | 15 | `employee_employee` |

**Link tables (18)**

- `payroll_allowance_apply_conditions` — `payroll_allowance` ↔ `payroll_applycondition`
- `payroll_allowance_exclude_employees` — `payroll_allowance` ↔ `employee_employee`
- `payroll_allowance_other_conditions` — `payroll_allowance` ↔ `payroll_multiplecondition`
- `payroll_allowance_specific_employees` — `payroll_allowance` ↔ `employee_employee`
- `payroll_deduction_apply_conditions` — `payroll_applycondition` ↔ `payroll_deduction`
- `payroll_deduction_exclude_employees` — `payroll_deduction` ↔ `employee_employee`
- `payroll_deduction_other_conditions` — `payroll_deduction` ↔ `payroll_multiplecondition`
- `payroll_deduction_specific_employees` — `payroll_deduction` ↔ `employee_employee`
- `payroll_encashmentgeneralsettings_department` — `base_department` ↔ `payroll_encashmentgeneralsettings`
- `payroll_encashmentgeneralsettings_employees` — `employee_employee` ↔ `payroll_encashmentgeneralsettings`
- `payroll_encashmentgeneralsettings_filtered_employees` — `employee_employee` ↔ `payroll_encashmentgeneralsettings`
- `payroll_encashmentgeneralsettings_job_position` — `payroll_encashmentgeneralsettings` ↔ `base_jobposition`
- `payroll_loanaccount_deduction_ids` — `payroll_deduction` ↔ `payroll_loanaccount`
- `payroll_payslip_installment_ids` — `payroll_deduction` ↔ `payroll_payslip`
- `payroll_reimbursement_other_attachments` — `payroll_reimbursement` ↔ `payroll_reimbursementmultipleattachment`
- `payroll_reimbursementrequestcomment_files` — `payroll_reimbursementfile` ↔ `payroll_reimbursementrequestcomment`
- `payroll_salarystructure_allowances` — `payroll_allowance` ↔ `payroll_salarystructure`
- `payroll_salarystructure_deductions` — `payroll_deduction` ↔ `payroll_salarystructure`

**History tables (4)**

`payroll_historicalcontract`, `payroll_historicalcontract_history_tags`, `payroll_historicalpayslip`, `payroll_historicalpayslip_history_tags`

## 10. Recruitment

Recruitment pipelines, stages, candidates, interviews, surveys, skills, resumes.

| Table | Cols | References |
|---|---:|---|
| `recruitment_candidate` | 37 | `base_jobposition`, `employee_employee`, `recruitment_recruitment`, `recruitment_stage` |
| `recruitment_candidatedocument` | 11 | `recruitment_candidate`, `recruitment_candidatedocumentrequest` |
| `recruitment_candidatedocumentrequest` | 9 | — |
| `recruitment_candidaterating` | 8 | `employee_employee`, `recruitment_candidate` |
| `recruitment_interviewschedule` | 10 | `recruitment_candidate` |
| `recruitment_linkedinaccount` | 10 | `base_company` |
| `recruitment_questionordering` | 8 | `recruitment_recruitment`, `recruitment_recruitmentsurvey` |
| `recruitment_recruitment` | 20 | `base_company`, `recruitment_linkedinaccount` |
| `recruitment_recruitmentgeneralsetting` | 8 | `base_company` |
| `recruitment_recruitmentsurvey` | 10 | — |
| `recruitment_recruitmentsurveyanswer` | 10 | `base_jobposition`, `recruitment_candidate`, `recruitment_recruitment` |
| `recruitment_rejectedcandidate` | 7 | `recruitment_candidate` |
| `recruitment_rejectreason` | 8 | `base_company` |
| `recruitment_resume` | 4 | `recruitment_recruitment` |
| `recruitment_skill` | 6 | — |
| `recruitment_skillzone` | 8 | `base_company` |
| `recruitment_skillzonecandidate` | 9 | `recruitment_candidate`, `recruitment_skillzone` |
| `recruitment_stage` | 9 | `recruitment_recruitment` |
| `recruitment_stagefiles` | 6 | — |
| `recruitment_stagenote` | 10 | `employee_employee`, `recruitment_candidate`, `recruitment_stage` |
| `recruitment_surveytemplate` | 9 | `base_company` |

**Link tables (12)**

- `horilla_meet_interviewmeetinglink` — `recruitment_interviewschedule` ↔ `horilla_meet_googlemeeting`
- `recruitment_candidatedocumentrequest_candidate_id` — `recruitment_candidate` ↔ `recruitment_candidatedocumentrequest`
- `recruitment_interviewschedule_employee_id` — `employee_employee` ↔ `recruitment_interviewschedule`
- `recruitment_recruitment_open_positions` — `base_jobposition` ↔ `recruitment_recruitment`
- `recruitment_recruitment_recruitment_managers` — `employee_employee` ↔ `recruitment_recruitment`
- `recruitment_recruitment_skills` — `recruitment_recruitment` ↔ `recruitment_skill`
- `recruitment_recruitment_survey_templates` — `recruitment_recruitment` ↔ `recruitment_surveytemplate`
- `recruitment_recruitmentsurvey_job_position_ids` — `base_jobposition` ↔ `recruitment_recruitmentsurvey`
- `recruitment_recruitmentsurvey_template_id` — `recruitment_recruitmentsurvey` ↔ `recruitment_surveytemplate`
- `recruitment_rejectedcandidate_reject_reason_id` — `recruitment_rejectedcandidate` ↔ `recruitment_rejectreason`
- `recruitment_stage_stage_managers` — `employee_employee` ↔ `recruitment_stage`
- `recruitment_stagenote_stage_files` — `recruitment_stagefiles` ↔ `recruitment_stagenote`

**History tables (6)**

`recruitment_historicalcandidate`, `recruitment_historicalcandidate_history_tags`, `recruitment_historicalrejectedcandidate`, `recruitment_historicalrejectedcandidate_history_tags`, `recruitment_historicalstage`, `recruitment_historicalstage_history_tags`

## 11. Onboarding

Onboarding stages/tasks for new hires and candidates.

| Table | Cols | References |
|---|---:|---|
| `onboarding_candidatestage` | 9 | `onboarding_onboardingstage`, `recruitment_candidate` |
| `onboarding_candidatetask` | 9 | `onboarding_onboardingstage`, `onboarding_onboardingtask`, `recruitment_candidate` |
| `onboarding_onboardingportal` | 10 | `recruitment_candidate` |
| `onboarding_onboardingstage` | 9 | `recruitment_recruitment` |
| `onboarding_onboardingtask` | 8 | `onboarding_onboardingstage` |

**Link tables (3)**

- `onboarding_onboardingstage_employee_id` — `employee_employee` ↔ `onboarding_onboardingstage`
- `onboarding_onboardingtask_candidates` — `recruitment_candidate` ↔ `onboarding_onboardingtask`
- `onboarding_onboardingtask_employee_id` — `employee_employee` ↔ `onboarding_onboardingtask`

**History tables (2)**

`onboarding_historicalcandidatetask`, `onboarding_historicalcandidatetask_history_tags`

## 12. Offboarding

Exit process: offboarding stages/tasks, resignation letters, exit reasons.

| Table | Cols | References |
|---|---:|---|
| `offboarding_employeetask` | 9 | `offboarding_offboardingemployee`, `offboarding_offboardingtask` |
| `offboarding_exitreason` | 8 | `offboarding_offboardingemployee` |
| `offboarding_offboarding` | 9 | `base_company` |
| `offboarding_offboardingemployee` | 11 | `employee_employee`, `offboarding_offboardingstage` |
| `offboarding_offboardinggeneralsetting` | 7 | `base_company` |
| `offboarding_offboardingnote` | 9 | `employee_employee`, `offboarding_offboardingemployee`, `offboarding_offboardingstage` |
| `offboarding_offboardingstage` | 9 | `offboarding_offboarding` |
| `offboarding_offboardingstagemultiplefile` | 6 | — |
| `offboarding_offboardingtask` | 8 | `offboarding_offboardingstage` |
| `offboarding_resignationletter` | 11 | `employee_employee`, `offboarding_offboardingemployee` |

**Link tables (5)**

- `offboarding_exitreason_attachments` — `offboarding_exitreason` ↔ `offboarding_offboardingstagemultiplefile`
- `offboarding_offboarding_managers` — `employee_employee` ↔ `offboarding_offboarding`
- `offboarding_offboardingnote_attachments` — `offboarding_offboardingnote` ↔ `offboarding_offboardingstagemultiplefile`
- `offboarding_offboardingstage_managers` — `employee_employee` ↔ `offboarding_offboardingstage`
- `offboarding_offboardingtask_managers` — `employee_employee` ↔ `offboarding_offboardingtask`

**History tables (4)**

`offboarding_historicalemployeetask`, `offboarding_historicalemployeetask_history_tags`, `offboarding_historicalresignationletter`, `offboarding_historicalresignationletter_history_tags`

## 13. Performance (PMS)

Objectives, key results, feedback, 1:1 meetings, question templates, periods.

| Table | Cols | References |
|---|---:|---|
| `pms_anonymousfeedback` | 11 | `base_department`, `base_jobposition`, `employee_employee` |
| `pms_answer` | 5 | `employee_employee`, `pms_feedback`, `pms_question` |
| `pms_bonuspointsetting` | 10 | `base_company` |
| `pms_comment` | 5 | `employee_employee`, `pms_employeeobjective` |
| `pms_employeebonuspoint` | 10 | `employee_bonuspoint`, `employee_employee` |
| `pms_employeekeyresult` | 15 | `pms_employeeobjective`, `pms_keyresult` |
| `pms_employeeobjective` | 15 | `employee_employee`, `pms_objective` |
| `pms_feedback` | 18 | `employee_employee`, `pms_questiontemplate` |
| `pms_keyresult` | 12 | `base_company` |
| `pms_keyresultfeedback` | 5 | `employee_employee`, `pms_employeekeyresult`, `pms_feedback` |
| `pms_meetings` | 11 | `base_company`, `pms_questiontemplate` |
| `pms_meetingsanswer` | 5 | `employee_employee`, `pms_meetings`, `pms_question` |
| `pms_objective` | 14 | `base_company` |
| `pms_period` | 8 | — |
| `pms_question` | 8 | `pms_questiontemplate` |
| `pms_questionoptions` | 10 | `pms_question` |
| `pms_questiontemplate` | 6 | — |

**Link tables (14)**

- `horilla_meet_pmsmeetinglink` — `horilla_meet_googlemeeting` ↔ `pms_meetings`
- `pms_employeeobjective_key_result_id` — `pms_employeeobjective` ↔ `pms_keyresult`
- `pms_feedback_colleague_id` — `employee_employee` ↔ `pms_feedback`
- `pms_feedback_employee_key_results_id` — `pms_employeekeyresult` ↔ `pms_feedback`
- `pms_feedback_others_id` — `employee_employee` ↔ `pms_feedback`
- `pms_feedback_subordinate_id` — `employee_employee` ↔ `pms_feedback`
- `pms_meetings_answer_employees` — `employee_employee` ↔ `pms_meetings`
- `pms_meetings_employee_id` — `employee_employee` ↔ `pms_meetings`
- `pms_meetings_manager` — `employee_employee` ↔ `pms_meetings`
- `pms_objective_assignees` — `employee_employee` ↔ `pms_objective`
- `pms_objective_key_result_id` — `pms_keyresult` ↔ `pms_objective`
- `pms_objective_managers` — `employee_employee` ↔ `pms_objective`
- `pms_period_company_id` — `base_company` ↔ `pms_period`
- `pms_questiontemplate_company_id` — `base_company` ↔ `pms_questiontemplate`

**History tables (10)**

`pms_historicalcomment`, `pms_historicalcomment_history_tags`, `pms_historicalemployeekeyresult`, `pms_historicalemployeekeyresult_history_tags`, `pms_historicalemployeeobjective`, `pms_historicalemployeeobjective_history_tags`, `pms_historicalkeyresult`, `pms_historicalkeyresult_history_tags`, `pms_historicalobjective`, `pms_historicalobjective_history_tags`

## 14. Assets

Asset catalogue, lots, assignment/return, requests, service requests, reports.

| Table | Cols | References |
|---|---:|---|
| `asset_asset` | 17 | `asset_assetcategory`, `asset_assetlot`, `employee_employee` |
| `asset_assetassignment` | 14 | `asset_asset`, `asset_assetitem`, `employee_employee` |
| `asset_assetcategory` | 7 | — |
| `asset_assetdocuments` | 7 | `asset_assetreport` |
| `asset_assetgeneralsetting` | 7 | `base_company` |
| `asset_assetitem` | 8 | `asset_asset` |
| `asset_assetlot` | 7 | — |
| `asset_assetreport` | 7 | `asset_asset` |
| `asset_assetrequest` | 10 | `asset_assetcategory`, `employee_employee` |
| `asset_assetrequestcomment` | 8 | `asset_assetrequest`, `employee_employee` |
| `asset_assetservicerequest` | 12 | `asset_assetassignment`, `employee_employee` |
| `asset_assetservicerequestnote` | 8 | `asset_assetservicerequest`, `employee_employee` |
| `asset_returnimages` | 6 | — |

**Link tables (4)**

- `asset_assetassignment_assign_images` — `asset_assetassignment` ↔ `asset_returnimages`
- `asset_assetassignment_return_images` — `asset_assetassignment` ↔ `asset_returnimages`
- `asset_assetcategory_company_id` — `asset_assetcategory` ↔ `base_company`
- `asset_assetlot_company_id` — `asset_assetlot` ↔ `base_company`

## 15. Helpdesk

Tickets, ticket types, FAQs, claims, department managers.

| Table | Cols | References |
|---|---:|---|
| `helpdesk_attachment` | 10 | `helpdesk_comment`, `helpdesk_ticket` |
| `helpdesk_claimrequest` | 9 | `employee_employee`, `helpdesk_ticket` |
| `helpdesk_comment` | 9 | `employee_employee`, `helpdesk_ticket` |
| `helpdesk_departmentmanager` | 8 | `base_company`, `base_department`, `employee_employee` |
| `helpdesk_faq` | 9 | `base_company`, `helpdesk_faqcategory` |
| `helpdesk_faqcategory` | 8 | `base_company` |
| `helpdesk_ticket` | 16 | `employee_employee`, `helpdesk_tickettype` |
| `helpdesk_tickettype` | 9 | `base_company` |

**Link tables (3)**

- `helpdesk_faq_tags` — `helpdesk_faq` ↔ `base_tags`
- `helpdesk_ticket_assigned_to` — `employee_employee` ↔ `helpdesk_ticket`
- `helpdesk_ticket_tags` — `base_tags` ↔ `helpdesk_ticket`

**History tables (2)**

`helpdesk_historicalticket`, `helpdesk_historicalticket_history_tags`

## 16. Projects & timesheets

Projects, stages, tasks, timesheets.

| Table | Cols | References |
|---|---:|---|
| `project_project` | 12 | `base_company` |
| `project_projectstage` | 9 | `project_project` |
| `project_task` | 15 | `project_project`, `project_projectstage` |
| `project_timesheet` | 12 | `employee_employee`, `project_project`, `project_task` |

**Link tables (3)**

- `project_project_managers` — `employee_employee` ↔ `project_project`
- `project_task_task_managers` — `employee_employee` ↔ `project_task`
- `project_task_task_members` — `employee_employee` ↔ `project_task`

## 17. Documents

Employee document requests and uploaded documents.

| Table | Cols | References |
|---|---:|---|
| `horilla_documents_document` | 15 | `employee_employee`, `horilla_documents_documentrequest` |
| `horilla_documents_documentrequest` | 9 | — |

**Link tables (1)**

- `horilla_documents_documentrequest_employee_id` — `horilla_documents_documentrequest` ↔ `employee_employee`

## 18. Communication & notifications

Announcements, in-app notifications, email config/logs/templates, mail automations, WhatsApp.

| Table | Cols | References |
|---|---:|---|
| `base_announcement` | 11 | — |
| `base_announcementcomment` | 8 | `base_announcement`, `employee_employee` |
| `base_announcementexpire` | 3 | `base_company` |
| `base_announcementview` | 5 | `base_announcement` |
| `base_dynamicemailconfiguration` | 18 | `base_company` |
| `base_emaillog` | 8 | `base_company` |
| `base_horillamailtemplate` | 8 | `base_company` |
| `base_notificationsound` | 3 | `employee_employee` |
| `horilla_automations_mailautomation` | 17 | `base_horillamailtemplate` |
| `notifications_notification` | 17 | `django_content_type` |
| `whatsapp_whatsappcredientials` | 13 | — |
| `whatsapp_whatsappflowdetails` | 4 | `whatsapp_whatsappcredientials` |

**Link tables (9)**

- `base_announcement_attachments` — `base_announcement` ↔ `base_attachment`
- `base_announcement_company_id` — `base_announcement` ↔ `base_company`
- `base_announcement_department` — `base_announcement` ↔ `base_department`
- `base_announcement_employees` — `base_announcement` ↔ `employee_employee`
- `base_announcement_filtered_employees` — `base_announcement` ↔ `employee_employee`
- `base_announcement_job_position` — `base_announcement` ↔ `base_jobposition`
- `horilla_automations_mailautomation_also_sent_to` — `employee_employee` ↔ `horilla_automations_mailautomation`
- `horilla_automations_mailautomation_template_attachments` — `base_horillamailtemplate` ↔ `horilla_automations_mailautomation`
- `whatsapp_whatsappcredientials_company_id` — `base_company` ↔ `whatsapp_whatsappcredientials`

## 19. Shared approvals, files & tags

Cross-module approval chains, generic attachments, request files, tags.

| Table | Cols | References |
|---|---:|---|
| `base_attachment` | 2 | — |
| `base_baserequestfile` | 2 | — |
| `base_multipleapprovalcondition` | 12 | `base_company`, `base_department` |
| `base_multipleapprovalmanagers` | 5 | `base_multipleapprovalcondition` |
| `base_tags` | 8 | `base_company` |

## 20. Reports & dashboards

Report templates, saved views, subscriptions, run logs, dashboard chart prefs.

| Table | Cols | References |
|---|---:|---|
| `base_dashboardemployeecharts` | 7 | `employee_employee` |
| `base_driverviewed` | 3 | — |
| `report_reportaccess` | 13 | `auth_group`, `base_company` |
| `report_reportfavorite` | 8 | `base_company` |
| `report_reportfilterpreset` | 10 | `base_company` |
| `report_reportrunlog` | 10 | `base_company` |
| `report_reportsavedview` | 9 | `base_company` |
| `report_reportsubscription` | 12 | `base_company` |
| `report_reporttemplate` | 11 | `base_company` |

**Link tables (1)**

- `report_reportsubscription_recipients_employees` — `employee_employee` ↔ `report_reportsubscription`

## 21. Users, auth & access control

Login users, groups/permissions, JWT tokens, lockout (axes), LDAP, sessions, feature access.

| Table | Cols | References |
|---|---:|---|
| `accessibility_defaultaccessibility` | 9 | — |
| `auth_group` | 2 | — |
| `auth_permission` | 4 | `django_content_type` |
| `axes_accessattempt` | 10 | — |
| `axes_accessattemptexpiration` | 2 | `axes_accessattempt` |
| `axes_accessfailurelog` | 8 | — |
| `axes_accesslog` | 9 | — |
| `base_defaultexportpermission` | 7 | `base_company` |
| `django_session` | 3 | — |
| `horilla_auth_horillauser` | 12 | — |
| `horilla_ldap_ldapsettings` | 5 | — |
| `token_blacklist_blacklistedtoken` | 3 | `token_blacklist_outstandingtoken` |
| `token_blacklist_outstandingtoken` | 6 | — |

**Link tables (4)**

- `accessibility_defaultaccessibility_employees` — `accessibility_defaultaccessibility` ↔ `employee_employee`
- `auth_group_permissions` — `auth_permission` ↔ `auth_group`
- `horilla_auth_horillauser_groups` — `auth_group` ↔ `horilla_auth_horillauser`
- `horilla_auth_horillauser_user_permissions` — `horilla_auth_horillauser` ↔ `auth_permission`

## 22. Audit & history

Audit log, history tracking config, admin log. (Per-model history tables are listed in their own domain.)

| Table | Cols | References |
|---|---:|---|
| `auditlog_logentry` | 16 | `django_content_type` |
| `django_admin_log` | 8 | `django_content_type` |
| `horilla_audit_accountblockunblock` | 6 | — |
| `horilla_audit_auditmodelconfig` | 9 | — |
| `horilla_audit_audittag` | 3 | — |
| `horilla_audit_historytrackingfields` | 8 | `base_company` |

## 23. UI preferences & personalization

Saved filters/views/columns, themes, product tours, pagination, setup checklist.

| Table | Cols | References |
|---|---:|---|
| `base_dynamicpagination` | 4 | `base_company` |
| `base_setupchecklistdismissal` | 4 | `base_company` |
| `horilla_theme_companytheme` | 7 | `base_company`, `horilla_theme_horillacolortheme` |
| `horilla_theme_horillacolortheme` | 35 | — |
| `horilla_tour_tour` | 18 | `base_company` |
| `horilla_tour_tourprogress` | 10 | `horilla_tour_tour` |
| `horilla_tour_tourstep` | 13 | `horilla_tour_tour` |
| `horilla_views_activegroup` | 8 | — |
| `horilla_views_activetab` | 7 | — |
| `horilla_views_activeview` | 7 | — |
| `horilla_views_columnorder` | 8 | `employee_employee` |
| `horilla_views_savedfilter` | 12 | — |
| `horilla_views_togglecolumn` | 8 | — |

## 24. Integrations, backup & system

Google/Meet credentials, integration apps, backups, DB templates, imports, scheduler, Django internals.

| Table | Cols | References |
|---|---:|---|
| `base_integrationapps` | 8 | `base_company` |
| `django_apscheduler_djangojob` | 3 | — |
| `django_apscheduler_djangojobexecution` | 8 | `django_apscheduler_djangojob` |
| `django_content_type` | 3 | — |
| `django_migrations` | 4 | — |
| `django_site` | 3 | — |
| `horilla_backup_googledrivebackup` | 14 | — |
| `horilla_backup_localbackup` | 10 | — |
| `horilla_dbtemplate_template` | 16 | — |
| `horilla_dbtemplate_templateversion` | 7 | `horilla_dbtemplate_template` |
| `horilla_meet_googlecloudcredential` | 6 | `base_company` |
| `horilla_meet_googlecredential` | 13 | `employee_employee` |
| `horilla_meet_googlemeeting` | 13 | `employee_employee` |
| `master_import_importjob` | 19 | `base_company` |

**Link tables (1)**

- `horilla_dbtemplate_template_sites` — `django_site` ↔ `horilla_dbtemplate_template`
