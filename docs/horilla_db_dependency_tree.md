# horilla_db — FK Dependency Tree

Generated from live PostgreSQL DB in `.env` (schema `public`). Edge = foreign key. `A → B` means **A depends on B** (A has FK to B, B must exist/be created first).

## Summary

- Tables: 416
- FK edges (distinct child→parent pairs, excl. self-ref): 801
- Root tables (no FK deps): 23 (7 fully isolated, 16 with dependents)
- Max dependency depth: 7
- Self-referencing tables: 0
- Circular dependency groups: 0

## 1. Creation / load order (levels)

Level 0 = no deps. Level N = 1 + max level of parents. Create/load tables level by level; delete in reverse.

### Level 0 (23)

- `auth_group`
- `axes_accessattempt`
- `axes_accessfailurelog`
- `axes_accesslog`
- `base_attachment`
- `base_baserequestfile`
- `base_employeeshiftday`
- `django_apscheduler_djangojob`
- `django_content_type`
- `django_migrations`
- `django_session`
- `django_site`
- `horilla_audit_audittag`
- `horilla_auth_horillauser`
- `horilla_backup_googledrivebackup`
- `horilla_backup_localbackup`
- `horilla_ldap_ldapsettings`
- `leave_leaverequestfile`
- `payroll_applycondition`
- `payroll_encashmentgeneralsettings`
- `payroll_multiplecondition`
- `payroll_reimbursementfile`
- `payroll_reimbursementmultipleattachment`

### Level 1 (75)

- `accessibility_defaultaccessibility` → `horilla_auth_horillauser`
- `asset_assetcategory` → `horilla_auth_horillauser`
- `asset_assetlot` → `horilla_auth_horillauser`
- `asset_returnimages` → `horilla_auth_horillauser`
- `attendance_attendancerequestfile` → `horilla_auth_horillauser`
- `attendance_attendancevalidationcondition` → `horilla_auth_horillauser`
- `attendance_batchattendance` → `horilla_auth_horillauser`
- `attendance_gracetime` → `horilla_auth_horillauser`
- `attendance_historicalattendance` → `horilla_auth_horillauser`
- `attendance_historicalattendanceactivity` → `horilla_auth_horillauser`
- `auditlog_logentry` → `django_content_type`, `horilla_auth_horillauser`
- `auth_permission` → `django_content_type`
- `axes_accessattemptexpiration` → `axes_accessattempt`
- `base_announcement` → `horilla_auth_horillauser`
- `base_company` → `horilla_auth_horillauser`
- `base_companyleaves` → `horilla_auth_horillauser`
- `base_department` → `horilla_auth_horillauser`
- `base_driverviewed` → `horilla_auth_horillauser`
- `base_employeetype` → `horilla_auth_horillauser`
- `base_historicalrotatingshiftassign` → `horilla_auth_horillauser`
- `base_historicalrotatingworktypeassign` → `horilla_auth_horillauser`
- `base_historicalshiftrequest` → `horilla_auth_horillauser`
- `base_historicalworktyperequest` → `horilla_auth_horillauser`
- `base_worktype` → `horilla_auth_horillauser`
- `django_admin_log` → `django_content_type`, `horilla_auth_horillauser`
- `django_apscheduler_djangojobexecution` → `django_apscheduler_djangojob`
- `employee_actiontype` → `horilla_auth_horillauser`
- `employee_employee` → `horilla_auth_horillauser`
- `employee_employeetag` → `horilla_auth_horillauser`
- `employee_historicalbonuspoint` → `horilla_auth_horillauser`
- `employee_historicalemployeeworkinformation` → `horilla_auth_horillauser`
- `employee_notefiles` → `horilla_auth_horillauser`
- `employee_policy` → `horilla_auth_horillauser`
- `employee_policymultiplefile` → `horilla_auth_horillauser`
- `employee_profileeditfeature` → `horilla_auth_horillauser`
- `helpdesk_historicalticket` → `horilla_auth_horillauser`
- `horilla_audit_accountblockunblock` → `horilla_auth_horillauser`
- `horilla_audit_auditmodelconfig` → `horilla_auth_horillauser`
- `horilla_auth_horillauser_groups` → `auth_group`, `horilla_auth_horillauser`
- `horilla_dbtemplate_template` → `horilla_auth_horillauser`
- `horilla_documents_documentrequest` → `horilla_auth_horillauser`
- `horilla_theme_horillacolortheme` → `horilla_auth_horillauser`
- `horilla_views_activegroup` → `horilla_auth_horillauser`
- `horilla_views_activetab` → `horilla_auth_horillauser`
- `horilla_views_activeview` → `horilla_auth_horillauser`
- `horilla_views_savedfilter` → `horilla_auth_horillauser`
- `horilla_views_togglecolumn` → `horilla_auth_horillauser`
- `leave_historicalavailableleave` → `horilla_auth_horillauser`
- `leave_historicalcompensatoryleaverequest` → `horilla_auth_horillauser`
- `leave_historicalleaveallocationrequest` → `horilla_auth_horillauser`
- `leave_historicalleaverequest` → `horilla_auth_horillauser`
- `leave_leavetypecondition` → `horilla_auth_horillauser`
- `notifications_notification` → `django_content_type`, `horilla_auth_horillauser`
- `offboarding_historicalemployeetask` → `horilla_auth_horillauser`
- `offboarding_historicalresignationletter` → `horilla_auth_horillauser`
- `offboarding_offboardingstagemultiplefile` → `horilla_auth_horillauser`
- `onboarding_historicalcandidatetask` → `horilla_auth_horillauser`
- `payroll_historicalcontract` → `horilla_auth_horillauser`
- `payroll_historicalpayslip` → `horilla_auth_horillauser`
- `pms_historicalcomment` → `horilla_auth_horillauser`
- `pms_historicalemployeekeyresult` → `horilla_auth_horillauser`
- `pms_historicalemployeeobjective` → `horilla_auth_horillauser`
- `pms_historicalkeyresult` → `horilla_auth_horillauser`
- `pms_historicalobjective` → `horilla_auth_horillauser`
- `pms_period` → `horilla_auth_horillauser`
- `pms_questiontemplate` → `horilla_auth_horillauser`
- `recruitment_candidatedocumentrequest` → `horilla_auth_horillauser`
- `recruitment_historicalcandidate` → `horilla_auth_horillauser`
- `recruitment_historicalrejectedcandidate` → `horilla_auth_horillauser`
- `recruitment_historicalstage` → `horilla_auth_horillauser`
- `recruitment_recruitmentsurvey` → `horilla_auth_horillauser`
- `recruitment_skill` → `horilla_auth_horillauser`
- `recruitment_stagefiles` → `horilla_auth_horillauser`
- `token_blacklist_outstandingtoken` → `horilla_auth_horillauser`
- `whatsapp_whatsappcredientials` → `horilla_auth_horillauser`

### Level 2 (149)

- `accessibility_defaultaccessibility_employees` → `accessibility_defaultaccessibility`, `employee_employee`
- `asset_asset` → `asset_assetcategory`, `asset_assetlot`, `employee_employee`, `horilla_auth_horillauser`
- `asset_assetcategory_company_id` → `asset_assetcategory`, `base_company`
- `asset_assetgeneralsetting` → `base_company`, `horilla_auth_horillauser`
- `asset_assetlot_company_id` → `asset_assetlot`, `base_company`
- `asset_assetrequest` → `asset_assetcategory`, `employee_employee`, `horilla_auth_horillauser`
- `attendance_attendanceactivity` → `base_employeeshiftday`, `employee_employee`, `horilla_auth_horillauser`
- `attendance_attendanceconflictresolution` → `employee_employee`, `horilla_auth_horillauser`
- `attendance_attendancedailyhours` → `employee_employee`, `horilla_auth_horillauser`
- `attendance_attendancegeneralsetting` → `base_company`, `horilla_auth_horillauser`
- `attendance_attendanceovertime` → `employee_employee`, `horilla_auth_horillauser`
- `attendance_attendancesummaryhours` → `employee_employee`, `horilla_auth_horillauser`
- `attendance_attendancesummaryoverride` → `employee_employee`, `horilla_auth_horillauser`
- `attendance_attendancevalidationcondition_company_id` → `attendance_attendancevalidationcondition`, `base_company`
- `attendance_gracetime_company_id` → `attendance_gracetime`, `base_company`
- `attendance_historicalattendance_history_tags` → `attendance_historicalattendance`, `horilla_audit_audittag`
- `attendance_historicalattendanceactivity_history_tags` → `attendance_historicalattendanceactivity`, `horilla_audit_audittag`
- `auth_group_permissions` → `auth_group`, `auth_permission`
- `base_announcement_attachments` → `base_announcement`, `base_attachment`
- `base_announcement_company_id` → `base_announcement`, `base_company`
- `base_announcement_department` → `base_announcement`, `base_department`
- `base_announcement_employees` → `base_announcement`, `employee_employee`
- `base_announcement_filtered_employees` → `base_announcement`, `employee_employee`
- `base_announcementcomment` → `base_announcement`, `employee_employee`, `horilla_auth_horillauser`
- `base_announcementexpire` → `base_company`
- `base_announcementview` → `base_announcement`, `horilla_auth_horillauser`
- `base_attendanceallowedip` → `base_company`
- `base_biometricattendance` → `base_company`
- `base_companygroupassignment` → `auth_group`, `base_company`, `horilla_auth_horillauser`
- `base_companylanguagesetting` → `base_company`, `horilla_auth_horillauser`
- `base_companyleaves_company_id` → `base_company`, `base_companyleaves`
- `base_dashboardemployeecharts` → `employee_employee`, `horilla_auth_horillauser`
- `base_defaultexportpermission` → `base_company`, `horilla_auth_horillauser`
- `base_department_company_id` → `base_company`, `base_department`
- `base_dynamicemailconfiguration` → `base_company`, `horilla_auth_horillauser`
- `base_dynamicpagination` → `base_company`, `horilla_auth_horillauser`
- `base_emaillog` → `base_company`
- `base_employeeshift` → `attendance_gracetime`, `horilla_auth_horillauser`
- `base_employeeshiftday_company_id` → `base_company`, `base_employeeshiftday`
- `base_employeetype_company_id` → `base_company`, `base_employeetype`
- `base_historicalrotatingshiftassign_history_tags` → `base_historicalrotatingshiftassign`, `horilla_audit_audittag`
- `base_historicalrotatingworktypeassign_history_tags` → `base_historicalrotatingworktypeassign`, `horilla_audit_audittag`
- `base_historicalshiftrequest_history_tags` → `base_historicalshiftrequest`, `horilla_audit_audittag`
- `base_historicalworktyperequest_history_tags` → `base_historicalworktyperequest`, `horilla_audit_audittag`
- `base_holidays` → `base_company`, `horilla_auth_horillauser`
- `base_horillamailtemplate` → `base_company`, `horilla_auth_horillauser`
- `base_integrationapps` → `base_company`, `horilla_auth_horillauser`
- `base_jobposition` → `base_department`, `horilla_auth_horillauser`
- `base_multipleapprovalcondition` → `base_company`, `base_department`, `horilla_auth_horillauser`
- `base_notificationsound` → `employee_employee`
- `base_rosterpublishlog` → `base_department`, `employee_employee`
- `base_rotatingworktype` → `base_worktype`, `horilla_auth_horillauser`
- `base_setupchecklistdismissal` → `base_company`, `horilla_auth_horillauser`
- `base_tags` → `base_company`, `horilla_auth_horillauser`
- `base_tracklatecomeearlyout` → `base_company`, `horilla_auth_horillauser`
- `base_worktype_company_id` → `base_company`, `base_worktype`
- `base_worktyperequest` → `base_worktype`, `employee_employee`, `horilla_auth_horillauser`
- `biometric_biometricdevices` → `base_company`, `horilla_auth_horillauser`
- `employee_bonuspoint` → `employee_employee`, `horilla_auth_horillauser`
- `employee_disciplinaryaction` → `employee_actiontype`, `horilla_auth_horillauser`
- `employee_employeebankdetails` → `employee_employee`, `horilla_auth_horillauser`
- `employee_employeegeneralsetting` → `base_company`, `horilla_auth_horillauser`
- `employee_employeenote` → `employee_employee`, `horilla_auth_horillauser`
- `employee_historicalbonuspoint_history_tags` → `employee_historicalbonuspoint`, `horilla_audit_audittag`
- `employee_historicalemployeeworkinformation_history_tags` → `employee_historicalemployeeworkinformation`, `horilla_audit_audittag`
- `employee_policy_attachments` → `employee_policy`, `employee_policymultiplefile`
- `employee_policy_company_id` → `base_company`, `employee_policy`
- `employee_policy_department` → `base_department`, `employee_policy`
- `employee_policy_employees` → `employee_employee`, `employee_policy`
- `employee_policy_filtered_employees` → `employee_employee`, `employee_policy`
- `facedetection_employeefacedetection` → `employee_employee`
- `facedetection_facedetection` → `base_company`
- `geofencing_geofencing` → `base_company`
- `helpdesk_departmentmanager` → `base_company`, `base_department`, `employee_employee`, `horilla_auth_horillauser`
- `helpdesk_faqcategory` → `base_company`, `horilla_auth_horillauser`
- `helpdesk_historicalticket_history_tags` → `helpdesk_historicalticket`, `horilla_audit_audittag`
- `helpdesk_tickettype` → `base_company`, `horilla_auth_horillauser`
- `horilla_audit_historytrackingfields` → `base_company`, `horilla_auth_horillauser`
- `horilla_auth_horillauser_user_permissions` → `auth_permission`, `horilla_auth_horillauser`
- `horilla_dbtemplate_template_sites` → `django_site`, `horilla_dbtemplate_template`
- `horilla_dbtemplate_templateversion` → `horilla_auth_horillauser`, `horilla_dbtemplate_template`
- `horilla_documents_document` → `employee_employee`, `horilla_auth_horillauser`, `horilla_documents_documentrequest`
- `horilla_documents_documentrequest_employee_id` → `employee_employee`, `horilla_documents_documentrequest`
- `horilla_meet_googlecloudcredential` → `base_company`
- `horilla_meet_googlecredential` → `employee_employee`, `horilla_auth_horillauser`
- `horilla_meet_googlemeeting` → `employee_employee`, `horilla_auth_horillauser`
- `horilla_theme_companytheme` → `base_company`, `horilla_auth_horillauser`, `horilla_theme_horillacolortheme`
- `horilla_tour_tour` → `base_company`, `horilla_auth_horillauser`
- `horilla_views_columnorder` → `employee_employee`, `horilla_auth_horillauser`
- `leave_employeepastleaverestrict` → `base_company`, `horilla_auth_horillauser`
- `leave_historicalavailableleave_history_tags` → `horilla_audit_audittag`, `leave_historicalavailableleave`
- `leave_historicalcompensatoryleaverequest_history_tags` → `horilla_audit_audittag`, `leave_historicalcompensatoryleaverequest`
- `leave_historicalleaveallocationrequest_history_tags` → `horilla_audit_audittag`, `leave_historicalleaveallocationrequest`
- `leave_historicalleaverequest_history_tags` → `horilla_audit_audittag`, `leave_historicalleaverequest`
- `leave_leavegeneralsetting` → `base_company`, `horilla_auth_horillauser`
- `leave_leavetype` → `base_company`, `horilla_auth_horillauser`
- `leave_restrictleave` → `base_company`, `base_department`, `horilla_auth_horillauser`
- `master_import_importjob` → `base_company`, `horilla_auth_horillauser`
- `offboarding_historicalemployeetask_history_tags` → `horilla_audit_audittag`, `offboarding_historicalemployeetask`
- `offboarding_historicalresignationletter_history_tags` → `horilla_audit_audittag`, `offboarding_historicalresignationletter`
- `offboarding_offboarding` → `base_company`, `horilla_auth_horillauser`
- `offboarding_offboardinggeneralsetting` → `base_company`, `horilla_auth_horillauser`
- `onboarding_historicalcandidatetask_history_tags` → `horilla_audit_audittag`, `onboarding_historicalcandidatetask`
- `payroll_deduction` → `base_company`, `horilla_auth_horillauser`
- `payroll_encashmentgeneralsettings_department` → `base_department`, `payroll_encashmentgeneralsettings`
- `payroll_encashmentgeneralsettings_employees` → `employee_employee`, `payroll_encashmentgeneralsettings`
- `payroll_encashmentgeneralsettings_filtered_employees` → `employee_employee`, `payroll_encashmentgeneralsettings`
- `payroll_filingstatus` → `base_company`, `horilla_auth_horillauser`
- `payroll_historicalcontract_history_tags` → `horilla_audit_audittag`, `payroll_historicalcontract`
- `payroll_historicalpayslip_history_tags` → `horilla_audit_audittag`, `payroll_historicalpayslip`
- `payroll_payperiodsettings` → `base_company`, `horilla_auth_horillauser`
- `payroll_payrollbatch` → `base_company`, `horilla_auth_horillauser`
- `payroll_payrollgeneralsetting` → `base_company`
- `payroll_payrollsettings` → `base_company`, `horilla_auth_horillauser`
- `payroll_payslipautogenerate` → `base_company`
- `payroll_salarystructure` → `base_company`, `horilla_auth_horillauser`
- `payroll_workrecord` → `employee_employee`
- `pms_bonuspointsetting` → `base_company`
- `pms_feedback` → `employee_employee`, `horilla_auth_horillauser`, `pms_questiontemplate`
- `pms_historicalcomment_history_tags` → `horilla_audit_audittag`, `pms_historicalcomment`
- `pms_historicalemployeekeyresult_history_tags` → `horilla_audit_audittag`, `pms_historicalemployeekeyresult`
- `pms_historicalemployeeobjective_history_tags` → `horilla_audit_audittag`, `pms_historicalemployeeobjective`
- `pms_historicalkeyresult_history_tags` → `horilla_audit_audittag`, `pms_historicalkeyresult`
- `pms_historicalobjective_history_tags` → `horilla_audit_audittag`, `pms_historicalobjective`
- `pms_keyresult` → `base_company`, `horilla_auth_horillauser`
- `pms_meetings` → `base_company`, `horilla_auth_horillauser`, `pms_questiontemplate`
- `pms_objective` → `base_company`, `horilla_auth_horillauser`
- `pms_period_company_id` → `base_company`, `pms_period`
- `pms_question` → `horilla_auth_horillauser`, `pms_questiontemplate`
- `pms_questiontemplate_company_id` → `base_company`, `pms_questiontemplate`
- `project_project` → `base_company`, `horilla_auth_horillauser`
- `recruitment_historicalcandidate_history_tags` → `horilla_audit_audittag`, `recruitment_historicalcandidate`
- `recruitment_historicalrejectedcandidate_history_tags` → `horilla_audit_audittag`, `recruitment_historicalrejectedcandidate`
- `recruitment_historicalstage_history_tags` → `horilla_audit_audittag`, `recruitment_historicalstage`
- `recruitment_linkedinaccount` → `base_company`, `horilla_auth_horillauser`
- `recruitment_recruitmentgeneralsetting` → `base_company`, `horilla_auth_horillauser`
- `recruitment_rejectreason` → `base_company`, `horilla_auth_horillauser`
- `recruitment_skillzone` → `base_company`, `horilla_auth_horillauser`
- `recruitment_surveytemplate` → `base_company`, `horilla_auth_horillauser`
- `report_reportaccess` → `auth_group`, `base_company`, `horilla_auth_horillauser`
- `report_reportfavorite` → `base_company`, `horilla_auth_horillauser`
- `report_reportfilterpreset` → `base_company`, `horilla_auth_horillauser`
- `report_reportrunlog` → `base_company`, `horilla_auth_horillauser`
- `report_reportsavedview` → `base_company`, `horilla_auth_horillauser`
- `report_reportsubscription` → `base_company`, `horilla_auth_horillauser`
- `report_reporttemplate` → `base_company`, `horilla_auth_horillauser`
- `token_blacklist_blacklistedtoken` → `token_blacklist_outstandingtoken`
- `whatsapp_whatsappcredientials_company_id` → `base_company`, `whatsapp_whatsappcredientials`
- `whatsapp_whatsappflowdetails` → `whatsapp_whatsappcredientials`

### Level 3 (70)

- `asset_assetitem` → `asset_asset`, `horilla_auth_horillauser`
- `asset_assetreport` → `asset_asset`, `horilla_auth_horillauser`
- `asset_assetrequestcomment` → `asset_assetrequest`, `employee_employee`, `horilla_auth_horillauser`
- `attendance_attendance` → `attendance_batchattendance`, `base_employeeshift`, `base_employeeshiftday`, `base_worktype`, `employee_employee`, `horilla_auth_horillauser`
- `attendance_attendancevalidationcondition_shift_ids` → `attendance_attendancevalidationcondition`, `base_employeeshift`
- `base_announcement_job_position` → `base_announcement`, `base_jobposition`
- `base_employeeshift_company_id` → `base_company`, `base_employeeshift`
- `base_employeeshiftschedule` → `base_employeeshift`, `base_employeeshiftday`, `horilla_auth_horillauser`
- `base_holidays_department` → `base_department`, `base_holidays`
- `base_holidays_employees` → `base_holidays`, `employee_employee`
- `base_holidays_job_position` → `base_holidays`, `base_jobposition`
- `base_jobposition_company_id` → `base_company`, `base_jobposition`
- `base_jobrole` → `base_jobposition`, `horilla_auth_horillauser`
- `base_multipleapprovalmanagers` → `base_multipleapprovalcondition`
- `base_roster` → `base_department`, `base_employeeshift`, `employee_employee`, `horilla_auth_horillauser`
- `base_rotatingshift` → `base_employeeshift`, `horilla_auth_horillauser`
- `base_rotatingworktypeassign` → `base_rotatingworktype`, `base_worktype`, `employee_employee`, `horilla_auth_horillauser`
- `base_shiftrequest` → `base_employeeshift`, `employee_employee`, `horilla_auth_horillauser`
- `base_worktyperequestcomment` → `base_worktyperequest`, `employee_employee`, `horilla_auth_horillauser`
- `biometric_biometricemployees` → `biometric_biometricdevices`, `employee_employee`
- `biometric_cosecattendancearguments` → `biometric_biometricdevices`
- `employee_disciplinaryaction_employee_id` → `employee_disciplinaryaction`, `employee_employee`
- `employee_employeenote_note_files` → `employee_employeenote`, `employee_notefiles`
- `employee_policy_job_position` → `base_jobposition`, `employee_policy`
- `helpdesk_faq` → `base_company`, `helpdesk_faqcategory`, `horilla_auth_horillauser`
- `helpdesk_ticket` → `employee_employee`, `helpdesk_tickettype`, `horilla_auth_horillauser`
- `horilla_automations_mailautomation` → `base_horillamailtemplate`, `horilla_auth_horillauser`
- `horilla_meet_pmsmeetinglink` → `horilla_meet_googlemeeting`, `pms_meetings`
- `horilla_tour_tourprogress` → `horilla_auth_horillauser`, `horilla_tour_tour`
- `horilla_tour_tourstep` → `horilla_auth_horillauser`, `horilla_tour_tour`
- `leave_availableleave` → `employee_employee`, `horilla_auth_horillauser`, `leave_leavetype`
- `leave_compensatoryleaverequest` → `employee_employee`, `horilla_auth_horillauser`, `leave_leavetype`
- `leave_leaveallocationrequest` → `employee_employee`, `horilla_auth_horillauser`, `leave_leavetype`
- `leave_leaverequest` → `employee_employee`, `horilla_auth_horillauser`, `leave_leavetype`
- `leave_leavetype_conditions` → `leave_leavetype`, `leave_leavetypecondition`
- `leave_restrictleave_exclued_leave_types` → `leave_leavetype`, `leave_restrictleave`
- `leave_restrictleave_job_position` → `base_jobposition`, `leave_restrictleave`
- `leave_restrictleave_spesific_leave_types` → `leave_leavetype`, `leave_restrictleave`
- `offboarding_offboarding_managers` → `employee_employee`, `offboarding_offboarding`
- `offboarding_offboardingstage` → `horilla_auth_horillauser`, `offboarding_offboarding`
- `payroll_allowance` → `base_company`, `base_employeeshift`, `base_worktype`, `horilla_auth_horillauser`
- `payroll_deduction_apply_conditions` → `payroll_applycondition`, `payroll_deduction`
- `payroll_deduction_exclude_employees` → `employee_employee`, `payroll_deduction`
- `payroll_deduction_other_conditions` → `payroll_deduction`, `payroll_multiplecondition`
- `payroll_deduction_specific_employees` → `employee_employee`, `payroll_deduction`
- `payroll_encashmentgeneralsettings_job_position` → `base_jobposition`, `payroll_encashmentgeneralsettings`
- `payroll_payslip` → `employee_employee`, `horilla_auth_horillauser`, `payroll_payrollbatch`
- `payroll_salarystructure_deductions` → `payroll_deduction`, `payroll_salarystructure`
- `payroll_taxbracket` → `horilla_auth_horillauser`, `payroll_filingstatus`
- `pms_anonymousfeedback` → `base_department`, `base_jobposition`, `employee_employee`
- `pms_answer` → `employee_employee`, `pms_feedback`, `pms_question`
- `pms_employeebonuspoint` → `employee_bonuspoint`, `employee_employee`, `horilla_auth_horillauser`
- `pms_employeeobjective` → `employee_employee`, `horilla_auth_horillauser`, `pms_objective`
- `pms_feedback_colleague_id` → `employee_employee`, `pms_feedback`
- `pms_feedback_others_id` → `employee_employee`, `pms_feedback`
- `pms_feedback_subordinate_id` → `employee_employee`, `pms_feedback`
- `pms_meetings_answer_employees` → `employee_employee`, `pms_meetings`
- `pms_meetings_employee_id` → `employee_employee`, `pms_meetings`
- `pms_meetings_manager` → `employee_employee`, `pms_meetings`
- `pms_meetingsanswer` → `employee_employee`, `pms_meetings`, `pms_question`
- `pms_objective_assignees` → `employee_employee`, `pms_objective`
- `pms_objective_key_result_id` → `pms_keyresult`, `pms_objective`
- `pms_objective_managers` → `employee_employee`, `pms_objective`
- `pms_questionoptions` → `horilla_auth_horillauser`, `pms_question`
- `project_project_managers` → `employee_employee`, `project_project`
- `project_projectstage` → `horilla_auth_horillauser`, `project_project`
- `recruitment_recruitment` → `base_company`, `horilla_auth_horillauser`, `recruitment_linkedinaccount`
- `recruitment_recruitmentsurvey_job_position_ids` → `base_jobposition`, `recruitment_recruitmentsurvey`
- `recruitment_recruitmentsurvey_template_id` → `recruitment_recruitmentsurvey`, `recruitment_surveytemplate`
- `report_reportsubscription_recipients_employees` → `employee_employee`, `report_reportsubscription`

### Level 4 (50)

- `asset_assetassignment` → `asset_asset`, `asset_assetitem`, `employee_employee`, `horilla_auth_horillauser`
- `asset_assetdocuments` → `asset_assetreport`, `horilla_auth_horillauser`
- `attendance_attendancelatecomeearlyout` → `attendance_attendance`, `employee_employee`, `horilla_auth_horillauser`
- `attendance_attendancerequestcomment` → `attendance_attendance`, `employee_employee`, `horilla_auth_horillauser`
- `attendance_workrecords` → `attendance_attendance`, `base_employeeshift`, `employee_employee`, `leave_leaverequest`
- `base_employeeshiftschedule_company_id` → `base_company`, `base_employeeshiftschedule`
- `base_jobrole_company_id` → `base_company`, `base_jobrole`
- `base_rotatingshiftassign` → `base_employeeshift`, `base_rotatingshift`, `employee_employee`, `horilla_auth_horillauser`
- `base_shiftrequestcomment` → `base_shiftrequest`, `employee_employee`, `horilla_auth_horillauser`
- `base_worktyperequestcomment_files` → `base_baserequestfile`, `base_worktyperequestcomment`
- `employee_employeeworkinformation` → `base_company`, `base_department`, `base_employeeshift`, `base_employeetype`, `base_jobposition`, `base_jobrole`, `base_worktype`, `employee_employee`
- `helpdesk_claimrequest` → `employee_employee`, `helpdesk_ticket`, `horilla_auth_horillauser`
- `helpdesk_comment` → `employee_employee`, `helpdesk_ticket`, `horilla_auth_horillauser`
- `helpdesk_faq_tags` → `base_tags`, `helpdesk_faq`
- `helpdesk_ticket_assigned_to` → `employee_employee`, `helpdesk_ticket`
- `helpdesk_ticket_tags` → `base_tags`, `helpdesk_ticket`
- `horilla_automations_mailautomation_also_sent_to` → `employee_employee`, `horilla_automations_mailautomation`
- `horilla_automations_mailautomation_template_attachments` → `base_horillamailtemplate`, `horilla_automations_mailautomation`
- `leave_compensatoryleaverequest_attendance_id` → `attendance_attendance`, `leave_compensatoryleaverequest`
- `leave_compensatoryleaverequestcomment` → `employee_employee`, `horilla_auth_horillauser`, `leave_compensatoryleaverequest`
- `leave_leaveallocationrequestcomment` → `employee_employee`, `horilla_auth_horillauser`, `leave_leaveallocationrequest`
- `leave_leaverequestcomment` → `employee_employee`, `horilla_auth_horillauser`, `leave_leaverequest`
- `leave_leaverequestconditionapproval` → `employee_employee`, `leave_leaverequest`
- `leave_overrideleaverequests` → `leave_leaverequest`
- `offboarding_offboardingemployee` → `employee_employee`, `horilla_auth_horillauser`, `offboarding_offboardingstage`
- `offboarding_offboardingstage_managers` → `employee_employee`, `offboarding_offboardingstage`
- `offboarding_offboardingtask` → `horilla_auth_horillauser`, `offboarding_offboardingstage`
- `onboarding_onboardingstage` → `horilla_auth_horillauser`, `recruitment_recruitment`
- `payroll_allowance_apply_conditions` → `payroll_allowance`, `payroll_applycondition`
- `payroll_allowance_exclude_employees` → `employee_employee`, `payroll_allowance`
- `payroll_allowance_other_conditions` → `payroll_allowance`, `payroll_multiplecondition`
- `payroll_allowance_specific_employees` → `employee_employee`, `payroll_allowance`
- `payroll_contract` → `base_department`, `base_employeeshift`, `base_jobposition`, `base_jobrole`, `base_worktype`, `employee_employee`, `horilla_auth_horillauser`, `payroll_filingstatus`, `payroll_salarystructure`
- `payroll_loanaccount` → `asset_asset`, `employee_employee`, `horilla_auth_horillauser`, `payroll_allowance`
- `payroll_overrideleaverequest` → `leave_leaverequest`
- `payroll_payrollbatchline` → `employee_employee`, `horilla_auth_horillauser`, `payroll_payrollbatch`, `payroll_payslip`
- `payroll_payslip_installment_ids` → `payroll_deduction`, `payroll_payslip`
- `payroll_reimbursement` → `employee_employee`, `horilla_auth_horillauser`, `leave_leavetype`, `payroll_allowance`
- `payroll_salarystructure_allowances` → `payroll_allowance`, `payroll_salarystructure`
- `pms_comment` → `employee_employee`, `pms_employeeobjective`
- `pms_employeekeyresult` → `pms_employeeobjective`, `pms_keyresult`
- `pms_employeeobjective_key_result_id` → `pms_employeeobjective`, `pms_keyresult`
- `project_task` → `horilla_auth_horillauser`, `project_project`, `project_projectstage`
- `recruitment_questionordering` → `horilla_auth_horillauser`, `recruitment_recruitment`, `recruitment_recruitmentsurvey`
- `recruitment_recruitment_open_positions` → `base_jobposition`, `recruitment_recruitment`
- `recruitment_recruitment_recruitment_managers` → `employee_employee`, `recruitment_recruitment`
- `recruitment_recruitment_skills` → `recruitment_recruitment`, `recruitment_skill`
- `recruitment_recruitment_survey_templates` → `recruitment_recruitment`, `recruitment_surveytemplate`
- `recruitment_resume` → `recruitment_recruitment`
- `recruitment_stage` → `horilla_auth_horillauser`, `recruitment_recruitment`

### Level 5 (28)

- `asset_assetassignment_assign_images` → `asset_assetassignment`, `asset_returnimages`
- `asset_assetassignment_return_images` → `asset_assetassignment`, `asset_returnimages`
- `asset_assetservicerequest` → `asset_assetassignment`, `employee_employee`, `horilla_auth_horillauser`
- `attendance_attendancerequestcomment_files` → `attendance_attendancerequestcomment`, `attendance_attendancerequestfile`
- `base_penaltyaccounts` → `attendance_attendancelatecomeearlyout`, `employee_employee`, `horilla_auth_horillauser`, `leave_leaverequest`, `leave_leavetype`
- `base_shiftrequestcomment_files` → `base_baserequestfile`, `base_shiftrequestcomment`
- `employee_employeeworkinformation_tags` → `employee_employeetag`, `employee_employeeworkinformation`
- `helpdesk_attachment` → `helpdesk_comment`, `helpdesk_ticket`, `horilla_auth_horillauser`
- `leave_compensatoryleaverequestcomment_files` → `leave_compensatoryleaverequestcomment`, `leave_leaverequestfile`
- `leave_leaveallocationrequestcomment_files` → `leave_leaveallocationrequestcomment`, `leave_leaverequestfile`
- `leave_leaverequestcomment_files` → `leave_leaverequestcomment`, `leave_leaverequestfile`
- `offboarding_employeetask` → `horilla_auth_horillauser`, `offboarding_offboardingemployee`, `offboarding_offboardingtask`
- `offboarding_exitreason` → `horilla_auth_horillauser`, `offboarding_offboardingemployee`
- `offboarding_offboardingnote` → `employee_employee`, `horilla_auth_horillauser`, `offboarding_offboardingemployee`, `offboarding_offboardingstage`
- `offboarding_offboardingtask_managers` → `employee_employee`, `offboarding_offboardingtask`
- `offboarding_resignationletter` → `employee_employee`, `horilla_auth_horillauser`, `offboarding_offboardingemployee`
- `onboarding_onboardingstage_employee_id` → `employee_employee`, `onboarding_onboardingstage`
- `onboarding_onboardingtask` → `horilla_auth_horillauser`, `onboarding_onboardingstage`
- `payroll_loanaccount_deduction_ids` → `payroll_deduction`, `payroll_loanaccount`
- `payroll_reimbursement_other_attachments` → `payroll_reimbursement`, `payroll_reimbursementmultipleattachment`
- `payroll_reimbursementrequestcomment` → `employee_employee`, `horilla_auth_horillauser`, `payroll_reimbursement`
- `pms_feedback_employee_key_results_id` → `pms_employeekeyresult`, `pms_feedback`
- `pms_keyresultfeedback` → `employee_employee`, `pms_employeekeyresult`, `pms_feedback`
- `project_task_task_managers` → `employee_employee`, `project_task`
- `project_task_task_members` → `employee_employee`, `project_task`
- `project_timesheet` → `employee_employee`, `horilla_auth_horillauser`, `project_project`, `project_task`
- `recruitment_candidate` → `base_jobposition`, `employee_employee`, `horilla_auth_horillauser`, `recruitment_recruitment`, `recruitment_stage`
- `recruitment_stage_stage_managers` → `employee_employee`, `recruitment_stage`

### Level 6 (17)

- `asset_assetservicerequestnote` → `asset_assetservicerequest`, `employee_employee`, `horilla_auth_horillauser`
- `offboarding_exitreason_attachments` → `offboarding_exitreason`, `offboarding_offboardingstagemultiplefile`
- `offboarding_offboardingnote_attachments` → `offboarding_offboardingnote`, `offboarding_offboardingstagemultiplefile`
- `onboarding_candidatestage` → `horilla_auth_horillauser`, `onboarding_onboardingstage`, `recruitment_candidate`
- `onboarding_candidatetask` → `horilla_auth_horillauser`, `onboarding_onboardingstage`, `onboarding_onboardingtask`, `recruitment_candidate`
- `onboarding_onboardingportal` → `horilla_auth_horillauser`, `recruitment_candidate`
- `onboarding_onboardingtask_candidates` → `onboarding_onboardingtask`, `recruitment_candidate`
- `onboarding_onboardingtask_employee_id` → `employee_employee`, `onboarding_onboardingtask`
- `payroll_reimbursementrequestcomment_files` → `payroll_reimbursementfile`, `payroll_reimbursementrequestcomment`
- `recruitment_candidatedocument` → `horilla_auth_horillauser`, `recruitment_candidate`, `recruitment_candidatedocumentrequest`
- `recruitment_candidatedocumentrequest_candidate_id` → `recruitment_candidate`, `recruitment_candidatedocumentrequest`
- `recruitment_candidaterating` → `employee_employee`, `horilla_auth_horillauser`, `recruitment_candidate`
- `recruitment_interviewschedule` → `horilla_auth_horillauser`, `recruitment_candidate`
- `recruitment_recruitmentsurveyanswer` → `base_jobposition`, `horilla_auth_horillauser`, `recruitment_candidate`, `recruitment_recruitment`
- `recruitment_rejectedcandidate` → `horilla_auth_horillauser`, `recruitment_candidate`
- `recruitment_skillzonecandidate` → `horilla_auth_horillauser`, `recruitment_candidate`, `recruitment_skillzone`
- `recruitment_stagenote` → `employee_employee`, `horilla_auth_horillauser`, `recruitment_candidate`, `recruitment_stage`

### Level 7 (4)

- `horilla_meet_interviewmeetinglink` → `horilla_meet_googlemeeting`, `recruitment_interviewschedule`
- `recruitment_interviewschedule_employee_id` → `employee_employee`, `recruitment_interviewschedule`
- `recruitment_rejectedcandidate_reject_reason_id` → `recruitment_rejectedcandidate`, `recruitment_rejectreason`
- `recruitment_stagenote_stage_files` → `recruitment_stagefiles`, `recruitment_stagenote`

## 4. Dependents tree (root → children)

Each root table, then tables that FK to it, recursively. A table is fully expanded at its **first** appearance (shallowest/alphabetical DFS); later appearances are marked `↩` (already expanded above). Label `(col)` = FK column on the child.

### `auth_group`  (direct dependents: 4, total: 4)

```
auth_group
├── `auth_group_permissions` (group_id)
├── `base_companygroupassignment` (group_id)
├── `horilla_auth_horillauser_groups` (group_id)
└── `report_reportaccess` (group_id)
```

### `axes_accessattempt`  (direct dependents: 1, total: 1)

```
axes_accessattempt
└── `axes_accessattemptexpiration` (access_attempt_id)
```

### `base_attachment`  (direct dependents: 1, total: 1)

```
base_attachment
└── `base_announcement_attachments` (attachment_id)
```

### `base_baserequestfile`  (direct dependents: 2, total: 2)

```
base_baserequestfile
├── `base_shiftrequestcomment_files` (baserequestfile_id)
└── `base_worktyperequestcomment_files` (baserequestfile_id)
```

### `base_employeeshiftday`  (direct dependents: 4, total: 11)

```
base_employeeshiftday
├── `attendance_attendance` (attendance_day_id)
│   ├── `attendance_attendancelatecomeearlyout` (attendance_id_id)
│   │   └── `base_penaltyaccounts` (late_early_id_id)
│   ├── `attendance_attendancerequestcomment` (request_id_id)
│   │   └── `attendance_attendancerequestcomment_files` (attendancerequestcomment_id)
│   ├── `attendance_workrecords` (attendance_id_id)
│   └── `leave_compensatoryleaverequest_attendance_id` (attendance_id)
├── `attendance_attendanceactivity` (shift_day_id)
├── `base_employeeshiftday_company_id` (employeeshiftday_id)
└── `base_employeeshiftschedule` (day_id)
    └── `base_employeeshiftschedule_company_id` (employeeshiftschedule_id)
```

### `django_apscheduler_djangojob`  (direct dependents: 1, total: 1)

```
django_apscheduler_djangojob
└── `django_apscheduler_djangojobexecution` (job_id)
```

### `django_content_type`  (direct dependents: 4, total: 6)

```
django_content_type
├── `auditlog_logentry` (content_type_id)
├── `auth_permission` (content_type_id)
│   ├── `auth_group_permissions` (permission_id)
│   └── `horilla_auth_horillauser_user_permissions` (permission_id)
├── `django_admin_log` (content_type_id)
└── `notifications_notification` (action_object_content_type_id,actor_content_type_id,target_content_type_id)
```

### `django_site`  (direct dependents: 1, total: 1)

```
django_site
└── `horilla_dbtemplate_template_sites` (site_id)
```

### `horilla_audit_audittag`  (direct dependents: 26, total: 26)

```
horilla_audit_audittag
├── `attendance_historicalattendance_history_tags` (audittag_id)
├── `attendance_historicalattendanceactivity_history_tags` (audittag_id)
├── `base_historicalrotatingshiftassign_history_tags` (audittag_id)
├── `base_historicalrotatingworktypeassign_history_tags` (audittag_id)
├── `base_historicalshiftrequest_history_tags` (audittag_id)
├── `base_historicalworktyperequest_history_tags` (audittag_id)
├── `employee_historicalbonuspoint_history_tags` (audittag_id)
├── `employee_historicalemployeeworkinformation_history_tags` (audittag_id)
├── `helpdesk_historicalticket_history_tags` (audittag_id)
├── `leave_historicalavailableleave_history_tags` (audittag_id)
├── `leave_historicalcompensatoryleaverequest_history_tags` (audittag_id)
├── `leave_historicalleaveallocationrequest_history_tags` (audittag_id)
├── `leave_historicalleaverequest_history_tags` (audittag_id)
├── `offboarding_historicalemployeetask_history_tags` (audittag_id)
├── `offboarding_historicalresignationletter_history_tags` (audittag_id)
├── `onboarding_historicalcandidatetask_history_tags` (audittag_id)
├── `payroll_historicalcontract_history_tags` (audittag_id)
├── `payroll_historicalpayslip_history_tags` (audittag_id)
├── `pms_historicalcomment_history_tags` (audittag_id)
├── `pms_historicalemployeekeyresult_history_tags` (audittag_id)
├── `pms_historicalemployeeobjective_history_tags` (audittag_id)
├── `pms_historicalkeyresult_history_tags` (audittag_id)
├── `pms_historicalobjective_history_tags` (audittag_id)
├── `recruitment_historicalcandidate_history_tags` (audittag_id)
├── `recruitment_historicalrejectedcandidate_history_tags` (audittag_id)
└── `recruitment_historicalstage_history_tags` (audittag_id)
```

### `horilla_auth_horillauser`  (direct dependents: 222, total: 389)

```
horilla_auth_horillauser
├── `accessibility_defaultaccessibility` (created_by_id,modified_by_id)
│   └── `accessibility_defaultaccessibility_employees` (defaultaccessibility_id)
├── `asset_asset` (created_by_id,modified_by_id)
│   ├── `asset_assetassignment` (asset_id_id)
│   │   ├── `asset_assetassignment_assign_images` (assetassignment_id)
│   │   ├── `asset_assetassignment_return_images` (assetassignment_id)
│   │   └── `asset_assetservicerequest` (assignment_id_id)
│   │       └── `asset_assetservicerequestnote` (request_id_id)
│   ├── `asset_assetitem` (asset_id_id)
│   │   └── `asset_assetassignment` (asset_item_id_id) ↩
│   ├── `asset_assetreport` (asset_id_id)
│   │   └── `asset_assetdocuments` (asset_report_id)
│   └── `payroll_loanaccount` (asset_id_id)
│       └── `payroll_loanaccount_deduction_ids` (loanaccount_id)
├── `asset_assetassignment` (created_by_id,modified_by_id) ↩
├── `asset_assetcategory` (created_by_id,modified_by_id)
│   ├── `asset_asset` (asset_category_id_id) ↩
│   ├── `asset_assetcategory_company_id` (assetcategory_id)
│   └── `asset_assetrequest` (asset_category_id_id)
│       └── `asset_assetrequestcomment` (request_id_id)
├── `asset_assetdocuments` (created_by_id,modified_by_id)
├── `asset_assetgeneralsetting` (created_by_id,modified_by_id)
├── `asset_assetitem` (created_by_id,modified_by_id) ↩
├── `asset_assetlot` (created_by_id,modified_by_id)
│   ├── `asset_asset` (asset_lot_number_id_id) ↩
│   └── `asset_assetlot_company_id` (assetlot_id)
├── `asset_assetreport` (created_by_id,modified_by_id) ↩
├── `asset_assetrequest` (created_by_id,modified_by_id) ↩
├── `asset_assetrequestcomment` (created_by_id,modified_by_id)
├── `asset_assetservicerequest` (created_by_id,modified_by_id) ↩
├── `asset_assetservicerequestnote` (created_by_id,modified_by_id)
├── `asset_returnimages` (created_by_id,modified_by_id)
│   ├── `asset_assetassignment_assign_images` (returnimages_id)
│   └── `asset_assetassignment_return_images` (returnimages_id)
├── `attendance_attendance` (created_by_id,modified_by_id) ↩
├── `attendance_attendanceactivity` (created_by_id,modified_by_id)
├── `attendance_attendanceconflictresolution` (created_by_id,modified_by_id)
├── `attendance_attendancedailyhours` (created_by_id,modified_by_id)
├── `attendance_attendancegeneralsetting` (created_by_id,modified_by_id)
├── `attendance_attendancelatecomeearlyout` (created_by_id,modified_by_id) ↩
├── `attendance_attendanceovertime` (created_by_id,modified_by_id)
├── `attendance_attendancerequestcomment` (created_by_id,modified_by_id) ↩
├── `attendance_attendancerequestfile` (created_by_id,modified_by_id)
│   └── `attendance_attendancerequestcomment_files` (attendancerequestfile_id)
├── `attendance_attendancesummaryhours` (created_by_id,modified_by_id)
├── `attendance_attendancesummaryoverride` (created_by_id,modified_by_id)
├── `attendance_attendancevalidationcondition` (created_by_id,modified_by_id)
│   ├── `attendance_attendancevalidationcondition_company_id` (attendancevalidationcondition_id)
│   └── `attendance_attendancevalidationcondition_shift_ids` (attendancevalidationcondition_id)
├── `attendance_batchattendance` (created_by_id,modified_by_id)
│   └── `attendance_attendance` (batch_attendance_id_id) ↩
├── `attendance_gracetime` (created_by_id,modified_by_id)
│   ├── `attendance_gracetime_company_id` (gracetime_id)
│   └── `base_employeeshift` (grace_time_id_id)
│       ├── `attendance_attendance` (shift_id_id) ↩
│       ├── `attendance_attendancevalidationcondition_shift_ids` (employeeshift_id)
│       ├── `attendance_workrecords` (shift_id_id)
│       ├── `base_employeeshift_company_id` (employeeshift_id)
│       ├── `base_employeeshiftschedule` (shift_id_id) ↩
│       ├── `base_roster` (shift_id)
│       ├── `base_rotatingshift` (shift1_id,shift2_id)
│       │   └── `base_rotatingshiftassign` (rotating_shift_id_id)
│       ├── `base_rotatingshiftassign` (current_shift_id,next_shift_id)
│       ├── `base_shiftrequest` (previous_shift_id_id,shift_id_id)
│       │   └── `base_shiftrequestcomment` (request_id_id)
│       │       └── `base_shiftrequestcomment_files` (shiftrequestcomment_id)
│       ├── `employee_employeeworkinformation` (shift_id_id)
│       │   └── `employee_employeeworkinformation_tags` (employeeworkinformation_id)
│       ├── `payroll_allowance` (shift_id_id)
│       │   ├── `payroll_allowance_apply_conditions` (allowance_id)
│       │   ├── `payroll_allowance_exclude_employees` (allowance_id)
│       │   ├── `payroll_allowance_other_conditions` (allowance_id)
│       │   ├── `payroll_allowance_specific_employees` (allowance_id)
│       │   ├── `payroll_loanaccount` (allowance_id_id) ↩
│       │   ├── `payroll_reimbursement` (allowance_id_id)
│       │   │   ├── `payroll_reimbursement_other_attachments` (reimbursement_id)
│       │   │   └── `payroll_reimbursementrequestcomment` (request_id_id)
│       │   │       └── `payroll_reimbursementrequestcomment_files` (reimbursementrequestcomment_id)
│       │   └── `payroll_salarystructure_allowances` (allowance_id)
│       └── `payroll_contract` (shift_id)
├── `attendance_historicalattendance` (history_user_id)
│   └── `attendance_historicalattendance_history_tags` (historicalattendance_id)
├── `attendance_historicalattendanceactivity` (history_user_id)
│   └── `attendance_historicalattendanceactivity_history_tags` (historicalattendanceactivity_id)
├── `auditlog_logentry` (actor_id)
├── `base_announcement` (created_by_id,modified_by_id)
│   ├── `base_announcement_attachments` (announcement_id)
│   ├── `base_announcement_company_id` (announcement_id)
│   ├── `base_announcement_department` (announcement_id)
│   ├── `base_announcement_employees` (announcement_id)
│   ├── `base_announcement_filtered_employees` (announcement_id)
│   ├── `base_announcement_job_position` (announcement_id)
│   ├── `base_announcementcomment` (announcement_id_id)
│   └── `base_announcementview` (announcement_id)
├── `base_announcementcomment` (created_by_id,modified_by_id)
├── `base_announcementview` (user_id)
├── `base_company` (created_by_id,modified_by_id)
│   ├── `asset_assetcategory_company_id` (company_id)
│   ├── `asset_assetgeneralsetting` (company_id_id)
│   ├── `asset_assetlot_company_id` (company_id)
│   ├── `attendance_attendancegeneralsetting` (company_id_id)
│   ├── `attendance_attendancevalidationcondition_company_id` (company_id)
│   ├── `attendance_gracetime_company_id` (company_id)
│   ├── `base_announcement_company_id` (company_id)
│   ├── `base_announcementexpire` (company_id_id)
│   ├── `base_attendanceallowedip` (company_id_id)
│   ├── `base_biometricattendance` (company_id_id)
│   ├── `base_companygroupassignment` (company_id)
│   ├── `base_companylanguagesetting` (company_id_id)
│   ├── `base_companyleaves_company_id` (company_id)
│   ├── `base_defaultexportpermission` (company_id_id)
│   ├── `base_department_company_id` (company_id)
│   ├── `base_dynamicemailconfiguration` (company_id_id)
│   ├── `base_dynamicpagination` (company_id_id)
│   ├── `base_emaillog` (company_id_id)
│   ├── `base_employeeshift_company_id` (company_id)
│   ├── `base_employeeshiftday_company_id` (company_id)
│   ├── `base_employeeshiftschedule_company_id` (company_id)
│   ├── `base_employeetype_company_id` (company_id)
│   ├── `base_holidays` (company_id_id)
│   │   ├── `base_holidays_department` (holidays_id)
│   │   ├── `base_holidays_employees` (holidays_id)
│   │   └── `base_holidays_job_position` (holidays_id)
│   ├── `base_horillamailtemplate` (company_id_id)
│   │   ├── `horilla_automations_mailautomation` (mail_template_id)
│   │   │   ├── `horilla_automations_mailautomation_also_sent_to` (mailautomation_id)
│   │   │   └── `horilla_automations_mailautomation_template_attachments` (mailautomation_id)
│   │   └── `horilla_automations_mailautomation_template_attachments` (horillamailtemplate_id)
│   ├── `base_integrationapps` (company_id)
│   ├── `base_jobposition_company_id` (company_id)
│   ├── `base_jobrole_company_id` (company_id)
│   ├── `base_multipleapprovalcondition` (company_id_id)
│   │   └── `base_multipleapprovalmanagers` (condition_id_id)
│   ├── `base_setupchecklistdismissal` (company_id)
│   ├── `base_tags` (company_id_id)
│   │   ├── `helpdesk_faq_tags` (tags_id)
│   │   └── `helpdesk_ticket_tags` (tags_id)
│   ├── `base_tracklatecomeearlyout` (company_id_id)
│   ├── `base_worktype_company_id` (company_id)
│   ├── `biometric_biometricdevices` (company_id_id)
│   │   ├── `biometric_biometricemployees` (device_id_id)
│   │   └── `biometric_cosecattendancearguments` (device_id_id)
│   ├── `employee_employeegeneralsetting` (company_id_id)
│   ├── `employee_employeeworkinformation` (company_id_id) ↩
│   ├── `employee_policy_company_id` (company_id)
│   ├── `facedetection_facedetection` (company_id_id)
│   ├── `geofencing_geofencing` (company_id_id)
│   ├── `helpdesk_departmentmanager` (company_id_id)
│   ├── `helpdesk_faq` (company_id_id)
│   │   └── `helpdesk_faq_tags` (faq_id)
│   ├── `helpdesk_faqcategory` (company_id_id)
│   │   └── `helpdesk_faq` (category_id) ↩
│   ├── `helpdesk_tickettype` (company_id_id)
│   │   └── `helpdesk_ticket` (ticket_type_id)
│   │       ├── `helpdesk_attachment` (ticket_id)
│   │       ├── `helpdesk_claimrequest` (ticket_id_id)
│   │       ├── `helpdesk_comment` (ticket_id)
│   │       │   └── `helpdesk_attachment` (comment_id)
│   │       ├── `helpdesk_ticket_assigned_to` (ticket_id)
│   │       └── `helpdesk_ticket_tags` (ticket_id)
│   ├── `horilla_audit_historytrackingfields` (company_id_id)
│   ├── `horilla_meet_googlecloudcredential` (company_id_id)
│   ├── `horilla_theme_companytheme` (company_id)
│   ├── `horilla_tour_tour` (company_id_id)
│   │   ├── `horilla_tour_tourprogress` (tour_id)
│   │   └── `horilla_tour_tourstep` (tour_id)
│   ├── `leave_employeepastleaverestrict` (company_id_id)
│   ├── `leave_leavegeneralsetting` (company_id_id)
│   ├── `leave_leavetype` (company_id_id)
│   │   ├── `base_penaltyaccounts` (leave_type_id_id)
│   │   ├── `leave_availableleave` (leave_type_id_id)
│   │   ├── `leave_compensatoryleaverequest` (leave_type_id_id)
│   │   │   ├── `leave_compensatoryleaverequest_attendance_id` (compensatoryleaverequest_id)
│   │   │   └── `leave_compensatoryleaverequestcomment` (request_id_id)
│   │   │       └── `leave_compensatoryleaverequestcomment_files` (compensatoryleaverequestcomment_id)
│   │   ├── `leave_leaveallocationrequest` (leave_type_id_id)
│   │   │   └── `leave_leaveallocationrequestcomment` (request_id_id)
│   │   │       └── `leave_leaveallocationrequestcomment_files` (leaveallocationrequestcomment_id)
│   │   ├── `leave_leaverequest` (leave_type_id_id)
│   │   │   ├── `attendance_workrecords` (leave_request_id_id)
│   │   │   ├── `base_penaltyaccounts` (leave_request_id_id)
│   │   │   ├── `leave_leaverequestcomment` (request_id_id)
│   │   │   │   └── `leave_leaverequestcomment_files` (leaverequestcomment_id)
│   │   │   ├── `leave_leaverequestconditionapproval` (leave_request_id_id)
│   │   │   ├── `leave_overrideleaverequests` (leaverequest_ptr_id)
│   │   │   └── `payroll_overrideleaverequest` (leaverequest_ptr_id)
│   │   ├── `leave_leavetype_conditions` (leavetype_id)
│   │   ├── `leave_restrictleave_exclued_leave_types` (leavetype_id)
│   │   ├── `leave_restrictleave_spesific_leave_types` (leavetype_id)
│   │   └── `payroll_reimbursement` (leave_type_id_id) ↩
│   ├── `leave_restrictleave` (company_id_id)
│   │   ├── `leave_restrictleave_exclued_leave_types` (restrictleave_id)
│   │   ├── `leave_restrictleave_job_position` (restrictleave_id)
│   │   └── `leave_restrictleave_spesific_leave_types` (restrictleave_id)
│   ├── `master_import_importjob` (company_id_id)
│   ├── `offboarding_offboarding` (company_id_id)
│   │   ├── `offboarding_offboarding_managers` (offboarding_id)
│   │   └── `offboarding_offboardingstage` (offboarding_id_id)
│   │       ├── `offboarding_offboardingemployee` (stage_id_id)
│   │       │   ├── `offboarding_employeetask` (employee_id_id)
│   │       │   ├── `offboarding_exitreason` (offboarding_employee_id_id)
│   │       │   │   └── `offboarding_exitreason_attachments` (exitreason_id)
│   │       │   ├── `offboarding_offboardingnote` (employee_id_id)
│   │       │   │   └── `offboarding_offboardingnote_attachments` (offboardingnote_id)
│   │       │   └── `offboarding_resignationletter` (offboarding_employee_id_id)
│   │       ├── `offboarding_offboardingnote` (stage_id_id) ↩
│   │       ├── `offboarding_offboardingstage_managers` (offboardingstage_id)
│   │       └── `offboarding_offboardingtask` (stage_id_id)
│   │           ├── `offboarding_employeetask` (task_id_id)
│   │           └── `offboarding_offboardingtask_managers` (offboardingtask_id)
│   ├── `offboarding_offboardinggeneralsetting` (company_id_id)
│   ├── `payroll_allowance` (company_id_id) ↩
│   ├── `payroll_deduction` (company_id_id)
│   │   ├── `payroll_deduction_apply_conditions` (deduction_id)
│   │   ├── `payroll_deduction_exclude_employees` (deduction_id)
│   │   ├── `payroll_deduction_other_conditions` (deduction_id)
│   │   ├── `payroll_deduction_specific_employees` (deduction_id)
│   │   ├── `payroll_loanaccount_deduction_ids` (deduction_id)
│   │   ├── `payroll_payslip_installment_ids` (deduction_id)
│   │   └── `payroll_salarystructure_deductions` (deduction_id)
│   ├── `payroll_filingstatus` (company_id_id)
│   │   ├── `payroll_contract` (filing_status_id)
│   │   └── `payroll_taxbracket` (filing_status_id_id)
│   ├── `payroll_payperiodsettings` (company_id_id)
│   ├── `payroll_payrollbatch` (company_id_id)
│   │   ├── `payroll_payrollbatchline` (payroll_batch_id)
│   │   └── `payroll_payslip` (payroll_batch_id)
│   │       ├── `payroll_payrollbatchline` (payslip_id)
│   │       └── `payroll_payslip_installment_ids` (payslip_id)
│   ├── `payroll_payrollgeneralsetting` (company_id_id)
│   ├── `payroll_payrollsettings` (company_id_id)
│   ├── `payroll_payslipautogenerate` (company_id_id)
│   ├── `payroll_salarystructure` (company_id_id)
│   │   ├── `payroll_contract` (salary_structure_id_id)
│   │   ├── `payroll_salarystructure_allowances` (salarystructure_id)
│   │   └── `payroll_salarystructure_deductions` (salarystructure_id)
│   ├── `pms_bonuspointsetting` (company_id_id)
│   ├── `pms_keyresult` (company_id_id)
│   │   ├── `pms_employeekeyresult` (key_result_id_id)
│   │   │   ├── `pms_feedback_employee_key_results_id` (employeekeyresult_id)
│   │   │   └── `pms_keyresultfeedback` (key_result_id_id)
│   │   ├── `pms_employeeobjective_key_result_id` (keyresult_id)
│   │   └── `pms_objective_key_result_id` (keyresult_id)
│   ├── `pms_meetings` (company_id_id)
│   │   ├── `horilla_meet_pmsmeetinglink` (meeting_id)
│   │   ├── `pms_meetings_answer_employees` (meetings_id)
│   │   ├── `pms_meetings_employee_id` (meetings_id)
│   │   ├── `pms_meetings_manager` (meetings_id)
│   │   └── `pms_meetingsanswer` (meeting_id_id)
│   ├── `pms_objective` (company_id_id)
│   │   ├── `pms_employeeobjective` (objective_id_id)
│   │   │   ├── `pms_comment` (employee_objective_id_id)
│   │   │   ├── `pms_employeekeyresult` (employee_objective_id_id) ↩
│   │   │   └── `pms_employeeobjective_key_result_id` (employeeobjective_id)
│   │   ├── `pms_objective_assignees` (objective_id)
│   │   ├── `pms_objective_key_result_id` (objective_id)
│   │   └── `pms_objective_managers` (objective_id)
│   ├── `pms_period_company_id` (company_id)
│   ├── `pms_questiontemplate_company_id` (company_id)
│   ├── `project_project` (company_id_id)
│   │   ├── `project_project_managers` (project_id)
│   │   ├── `project_projectstage` (project_id)
│   │   │   └── `project_task` (stage_id)
│   │   │       ├── `project_task_task_managers` (task_id)
│   │   │       ├── `project_task_task_members` (task_id)
│   │   │       └── `project_timesheet` (task_id_id)
│   │   ├── `project_task` (project_id) ↩
│   │   └── `project_timesheet` (project_id_id)
│   ├── `recruitment_linkedinaccount` (company_id_id)
│   │   └── `recruitment_recruitment` (linkedin_account_id_id)
│   │       ├── `onboarding_onboardingstage` (recruitment_id_id)
│   │       │   ├── `onboarding_candidatestage` (onboarding_stage_id_id)
│   │       │   ├── `onboarding_candidatetask` (stage_id_id)
│   │       │   ├── `onboarding_onboardingstage_employee_id` (onboardingstage_id)
│   │       │   └── `onboarding_onboardingtask` (stage_id_id)
│   │       │       ├── `onboarding_candidatetask` (onboarding_task_id_id)
│   │       │       ├── `onboarding_onboardingtask_candidates` (onboardingtask_id)
│   │       │       └── `onboarding_onboardingtask_employee_id` (onboardingtask_id)
│   │       ├── `recruitment_candidate` (recruitment_id_id)
│   │       │   ├── `onboarding_candidatestage` (candidate_id_id)
│   │       │   ├── `onboarding_candidatetask` (candidate_id_id)
│   │       │   ├── `onboarding_onboardingportal` (candidate_id_id)
│   │       │   ├── `onboarding_onboardingtask_candidates` (candidate_id)
│   │       │   ├── `recruitment_candidatedocument` (candidate_id_id)
│   │       │   ├── `recruitment_candidatedocumentrequest_candidate_id` (candidate_id)
│   │       │   ├── `recruitment_candidaterating` (candidate_id_id)
│   │       │   ├── `recruitment_interviewschedule` (candidate_id_id)
│   │       │   │   ├── `horilla_meet_interviewmeetinglink` (interview_id)
│   │       │   │   └── `recruitment_interviewschedule_employee_id` (interviewschedule_id)
│   │       │   ├── `recruitment_recruitmentsurveyanswer` (candidate_id_id)
│   │       │   ├── `recruitment_rejectedcandidate` (candidate_id_id)
│   │       │   │   └── `recruitment_rejectedcandidate_reject_reason_id` (rejectedcandidate_id)
│   │       │   ├── `recruitment_skillzonecandidate` (candidate_id_id)
│   │       │   └── `recruitment_stagenote` (candidate_id_id)
│   │       │       └── `recruitment_stagenote_stage_files` (stagenote_id)
│   │       ├── `recruitment_questionordering` (recruitment_id_id)
│   │       ├── `recruitment_recruitment_open_positions` (recruitment_id)
│   │       ├── `recruitment_recruitment_recruitment_managers` (recruitment_id)
│   │       ├── `recruitment_recruitment_skills` (recruitment_id)
│   │       ├── `recruitment_recruitment_survey_templates` (recruitment_id)
│   │       ├── `recruitment_recruitmentsurveyanswer` (recruitment_id_id)
│   │       ├── `recruitment_resume` (recruitment_id_id)
│   │       └── `recruitment_stage` (recruitment_id_id)
│   │           ├── `recruitment_candidate` (stage_id_id) ↩
│   │           ├── `recruitment_stage_stage_managers` (stage_id)
│   │           └── `recruitment_stagenote` (stage_id_id) ↩
│   ├── `recruitment_recruitment` (company_id_id) ↩
│   ├── `recruitment_recruitmentgeneralsetting` (company_id_id)
│   ├── `recruitment_rejectreason` (company_id_id)
│   │   └── `recruitment_rejectedcandidate_reject_reason_id` (rejectreason_id)
│   ├── `recruitment_skillzone` (company_id_id)
│   │   └── `recruitment_skillzonecandidate` (skill_zone_id_id)
│   ├── `recruitment_surveytemplate` (company_id_id)
│   │   ├── `recruitment_recruitment_survey_templates` (surveytemplate_id)
│   │   └── `recruitment_recruitmentsurvey_template_id` (surveytemplate_id)
│   ├── `report_reportaccess` (company_id_id)
│   ├── `report_reportfavorite` (company_id_id)
│   ├── `report_reportfilterpreset` (company_id_id)
│   ├── `report_reportrunlog` (company_id_id)
│   ├── `report_reportsavedview` (company_id_id)
│   ├── `report_reportsubscription` (company_id_id)
│   │   └── `report_reportsubscription_recipients_employees` (reportsubscription_id)
│   ├── `report_reporttemplate` (company_id_id)
│   └── `whatsapp_whatsappcredientials_company_id` (company_id)
├── `base_companygroupassignment` (created_by_id,modified_by_id,user_id)
├── `base_companylanguagesetting` (created_by_id,modified_by_id)
├── `base_companyleaves` (created_by_id,modified_by_id)
│   └── `base_companyleaves_company_id` (companyleaves_id)
├── `base_dashboardemployeecharts` (created_by_id,modified_by_id)
├── `base_defaultexportpermission` (created_by_id,modified_by_id)
├── `base_department` (created_by_id,modified_by_id)
│   ├── `base_announcement_department` (department_id)
│   ├── `base_department_company_id` (department_id)
│   ├── `base_holidays_department` (department_id)
│   ├── `base_jobposition` (department_id_id)
│   │   ├── `base_announcement_job_position` (jobposition_id)
│   │   ├── `base_holidays_job_position` (jobposition_id)
│   │   ├── `base_jobposition_company_id` (jobposition_id)
│   │   ├── `base_jobrole` (job_position_id_id)
│   │   │   ├── `base_jobrole_company_id` (jobrole_id)
│   │   │   ├── `employee_employeeworkinformation` (job_role_id_id) ↩
│   │   │   └── `payroll_contract` (job_role_id)
│   │   ├── `employee_employeeworkinformation` (job_position_id_id) ↩
│   │   ├── `employee_policy_job_position` (jobposition_id)
│   │   ├── `leave_restrictleave_job_position` (jobposition_id)
│   │   ├── `payroll_contract` (job_position_id)
│   │   ├── `payroll_encashmentgeneralsettings_job_position` (jobposition_id)
│   │   ├── `pms_anonymousfeedback` (job_position_id_id)
│   │   ├── `recruitment_candidate` (job_position_id_id) ↩
│   │   ├── `recruitment_recruitment_open_positions` (jobposition_id)
│   │   ├── `recruitment_recruitmentsurvey_job_position_ids` (jobposition_id)
│   │   └── `recruitment_recruitmentsurveyanswer` (job_position_id_id)
│   ├── `base_multipleapprovalcondition` (department_id) ↩
│   ├── `base_roster` (department_id)
│   ├── `base_rosterpublishlog` (department_id)
│   ├── `employee_employeeworkinformation` (department_id_id) ↩
│   ├── `employee_policy_department` (department_id)
│   ├── `helpdesk_departmentmanager` (department_id)
│   ├── `leave_restrictleave` (department_id) ↩
│   ├── `payroll_contract` (department_id)
│   ├── `payroll_encashmentgeneralsettings_department` (department_id)
│   └── `pms_anonymousfeedback` (department_id_id)
├── `base_driverviewed` (user_id)
├── `base_dynamicemailconfiguration` (created_by_id,modified_by_id)
├── `base_dynamicpagination` (user_id_id)
├── `base_employeeshift` (created_by_id,modified_by_id) ↩
├── `base_employeeshiftschedule` (created_by_id,modified_by_id) ↩
├── `base_employeetype` (created_by_id,modified_by_id)
│   ├── `base_employeetype_company_id` (employeetype_id)
│   └── `employee_employeeworkinformation` (employee_type_id_id) ↩
├── `base_historicalrotatingshiftassign` (history_user_id)
│   └── `base_historicalrotatingshiftassign_history_tags` (historicalrotatingshiftassign_id)
├── `base_historicalrotatingworktypeassign` (history_user_id)
│   └── `base_historicalrotatingworktypeassign_history_tags` (historicalrotatingworktypeassign_id)
├── `base_historicalshiftrequest` (history_user_id)
│   └── `base_historicalshiftrequest_history_tags` (historicalshiftrequest_id)
├── `base_historicalworktyperequest` (history_user_id)
│   └── `base_historicalworktyperequest_history_tags` (historicalworktyperequest_id)
├── `base_holidays` (created_by_id,modified_by_id) ↩
├── `base_horillamailtemplate` (created_by_id,modified_by_id) ↩
├── `base_integrationapps` (created_by_id,modified_by_id)
├── `base_jobposition` (created_by_id,modified_by_id) ↩
├── `base_jobrole` (created_by_id,modified_by_id) ↩
├── `base_multipleapprovalcondition` (created_by_id,modified_by_id) ↩
├── `base_penaltyaccounts` (created_by_id,modified_by_id)
├── `base_roster` (modified_by_id)
├── `base_rotatingshift` (created_by_id,modified_by_id) ↩
├── `base_rotatingshiftassign` (created_by_id,modified_by_id)
├── `base_rotatingworktype` (created_by_id,modified_by_id)
│   └── `base_rotatingworktypeassign` (rotating_work_type_id_id)
├── `base_rotatingworktypeassign` (created_by_id,modified_by_id)
├── `base_setupchecklistdismissal` (user_id)
├── `base_shiftrequest` (created_by_id,modified_by_id) ↩
├── `base_shiftrequestcomment` (created_by_id,modified_by_id) ↩
├── `base_tags` (created_by_id,modified_by_id) ↩
├── `base_tracklatecomeearlyout` (created_by_id,modified_by_id)
├── `base_worktype` (created_by_id,modified_by_id)
│   ├── `attendance_attendance` (work_type_id_id) ↩
│   ├── `base_rotatingworktype` (work_type1_id,work_type2_id) ↩
│   ├── `base_rotatingworktypeassign` (current_work_type_id,next_work_type_id)
│   ├── `base_worktype_company_id` (worktype_id)
│   ├── `base_worktyperequest` (previous_work_type_id_id,work_type_id_id)
│   │   └── `base_worktyperequestcomment` (request_id_id)
│   │       └── `base_worktyperequestcomment_files` (worktyperequestcomment_id)
│   ├── `employee_employeeworkinformation` (work_type_id_id) ↩
│   ├── `payroll_allowance` (work_type_id_id) ↩
│   └── `payroll_contract` (work_type_id)
├── `base_worktyperequest` (created_by_id,modified_by_id) ↩
├── `base_worktyperequestcomment` (created_by_id,modified_by_id) ↩
├── `biometric_biometricdevices` (created_by_id,modified_by_id) ↩
├── `django_admin_log` (user_id)
├── `employee_actiontype` (created_by_id,modified_by_id)
│   └── `employee_disciplinaryaction` (action_id)
│       └── `employee_disciplinaryaction_employee_id` (disciplinaryaction_id)
├── `employee_bonuspoint` (created_by_id,modified_by_id)
│   └── `pms_employeebonuspoint` (bonus_point_id_id)
├── `employee_disciplinaryaction` (created_by_id,modified_by_id) ↩
├── `employee_employee` (employee_user_id_id)
│   ├── `accessibility_defaultaccessibility_employees` (employee_id)
│   ├── `asset_asset` (owner_id) ↩
│   ├── `asset_assetassignment` (assigned_by_employee_id_id,assigned_to_employee_id_id) ↩
│   ├── `asset_assetrequest` (requested_employee_id_id) ↩
│   ├── `asset_assetrequestcomment` (employee_id_id)
│   ├── `asset_assetservicerequest` (requested_employee_id_id,resolved_by_employee_id_id) ↩
│   ├── `asset_assetservicerequestnote` (employee_id_id)
│   ├── `attendance_attendance` (approved_by_id,employee_id_id) ↩
│   ├── `attendance_attendanceactivity` (employee_id_id)
│   ├── `attendance_attendanceconflictresolution` (employee_id_id)
│   ├── `attendance_attendancedailyhours` (employee_id_id)
│   ├── `attendance_attendancelatecomeearlyout` (employee_id_id) ↩
│   ├── `attendance_attendanceovertime` (employee_id_id)
│   ├── `attendance_attendancerequestcomment` (employee_id_id) ↩
│   ├── `attendance_attendancesummaryhours` (employee_id_id)
│   ├── `attendance_attendancesummaryoverride` (employee_id_id)
│   ├── `attendance_workrecords` (employee_id_id)
│   ├── `base_announcement_employees` (employee_id)
│   ├── `base_announcement_filtered_employees` (employee_id)
│   ├── `base_announcementcomment` (employee_id_id)
│   ├── `base_dashboardemployeecharts` (employee_id)
│   ├── `base_holidays_employees` (employee_id)
│   ├── `base_notificationsound` (employee_id)
│   ├── `base_penaltyaccounts` (employee_id_id)
│   ├── `base_roster` (created_by_id,employee_id)
│   ├── `base_rosterpublishlog` (published_by_id)
│   ├── `base_rotatingshiftassign` (employee_id_id)
│   ├── `base_rotatingworktypeassign` (employee_id_id)
│   ├── `base_shiftrequest` (employee_id_id,reallocate_to_id) ↩
│   ├── `base_shiftrequestcomment` (employee_id_id) ↩
│   ├── `base_worktyperequest` (employee_id_id) ↩
│   ├── `base_worktyperequestcomment` (employee_id_id) ↩
│   ├── `biometric_biometricemployees` (employee_id_id)
│   ├── `employee_bonuspoint` (employee_id_id) ↩
│   ├── `employee_disciplinaryaction_employee_id` (employee_id)
│   ├── `employee_employeebankdetails` (employee_id_id)
│   ├── `employee_employeenote` (employee_id_id,updated_by_id)
│   │   └── `employee_employeenote_note_files` (employeenote_id)
│   ├── `employee_employeeworkinformation` (employee_id_id,reporting_manager_id_id) ↩
│   ├── `employee_policy_employees` (employee_id)
│   ├── `employee_policy_filtered_employees` (employee_id)
│   ├── `facedetection_employeefacedetection` (employee_id_id)
│   ├── `helpdesk_claimrequest` (employee_id_id)
│   ├── `helpdesk_comment` (employee_id_id) ↩
│   ├── `helpdesk_departmentmanager` (manager_id)
│   ├── `helpdesk_ticket` (employee_id_id) ↩
│   ├── `helpdesk_ticket_assigned_to` (employee_id)
│   ├── `horilla_automations_mailautomation_also_sent_to` (employee_id)
│   ├── `horilla_documents_document` (employee_id_id)
│   ├── `horilla_documents_documentrequest_employee_id` (employee_id)
│   ├── `horilla_meet_googlecredential` (employee_id_id)
│   ├── `horilla_meet_googlemeeting` (employee_id_id)
│   │   ├── `horilla_meet_interviewmeetinglink` (meeting_id)
│   │   └── `horilla_meet_pmsmeetinglink` (google_meeting_id)
│   ├── `horilla_views_columnorder` (employee_id)
│   ├── `leave_availableleave` (employee_id_id)
│   ├── `leave_compensatoryleaverequest` (employee_id_id) ↩
│   ├── `leave_compensatoryleaverequestcomment` (employee_id_id) ↩
│   ├── `leave_leaveallocationrequest` (employee_id_id) ↩
│   ├── `leave_leaveallocationrequestcomment` (employee_id_id) ↩
│   ├── `leave_leaverequest` (created_by_id,employee_id_id) ↩
│   ├── `leave_leaverequestcomment` (employee_id_id) ↩
│   ├── `leave_leaverequestconditionapproval` (manager_id_id)
│   ├── `offboarding_offboarding_managers` (employee_id)
│   ├── `offboarding_offboardingemployee` (employee_id_id) ↩
│   ├── `offboarding_offboardingnote` (note_by_id) ↩
│   ├── `offboarding_offboardingstage_managers` (employee_id)
│   ├── `offboarding_offboardingtask_managers` (employee_id)
│   ├── `offboarding_resignationletter` (employee_id_id)
│   ├── `onboarding_onboardingstage_employee_id` (employee_id)
│   ├── `onboarding_onboardingtask_employee_id` (employee_id)
│   ├── `payroll_allowance_exclude_employees` (employee_id)
│   ├── `payroll_allowance_specific_employees` (employee_id)
│   ├── `payroll_contract` (employee_id_id)
│   ├── `payroll_deduction_exclude_employees` (employee_id)
│   ├── `payroll_deduction_specific_employees` (employee_id)
│   ├── `payroll_encashmentgeneralsettings_employees` (employee_id)
│   ├── `payroll_encashmentgeneralsettings_filtered_employees` (employee_id)
│   ├── `payroll_loanaccount` (employee_id_id) ↩
│   ├── `payroll_payrollbatchline` (employee_id_id)
│   ├── `payroll_payslip` (employee_id_id) ↩
│   ├── `payroll_reimbursement` (approved_by_id,employee_id_id) ↩
│   ├── `payroll_reimbursementrequestcomment` (employee_id_id) ↩
│   ├── `payroll_workrecord` (employee_id_id)
│   ├── `pms_anonymousfeedback` (employee_id_id)
│   ├── `pms_answer` (employee_id_id)
│   ├── `pms_comment` (employee_id_id)
│   ├── `pms_employeebonuspoint` (employee_id_id)
│   ├── `pms_employeeobjective` (employee_id_id) ↩
│   ├── `pms_feedback` (employee_id_id,manager_id_id)
│   │   ├── `pms_answer` (feedback_id_id)
│   │   ├── `pms_feedback_colleague_id` (feedback_id)
│   │   ├── `pms_feedback_employee_key_results_id` (feedback_id)
│   │   ├── `pms_feedback_others_id` (feedback_id)
│   │   ├── `pms_feedback_subordinate_id` (feedback_id)
│   │   └── `pms_keyresultfeedback` (feedback_id_id)
│   ├── `pms_feedback_colleague_id` (employee_id)
│   ├── `pms_feedback_others_id` (employee_id)
│   ├── `pms_feedback_subordinate_id` (employee_id)
│   ├── `pms_keyresultfeedback` (employee_id_id)
│   ├── `pms_meetings_answer_employees` (employee_id)
│   ├── `pms_meetings_employee_id` (employee_id)
│   ├── `pms_meetings_manager` (employee_id)
│   ├── `pms_meetingsanswer` (employee_id_id)
│   ├── `pms_objective_assignees` (employee_id)
│   ├── `pms_objective_managers` (employee_id)
│   ├── `project_project_managers` (employee_id)
│   ├── `project_task_task_managers` (employee_id)
│   ├── `project_task_task_members` (employee_id)
│   ├── `project_timesheet` (employee_id_id)
│   ├── `recruitment_candidate` (converted_employee_id_id,referral_id) ↩
│   ├── `recruitment_candidaterating` (employee_id_id)
│   ├── `recruitment_interviewschedule_employee_id` (employee_id)
│   ├── `recruitment_recruitment_recruitment_managers` (employee_id)
│   ├── `recruitment_stage_stage_managers` (employee_id)
│   ├── `recruitment_stagenote` (updated_by_id) ↩
│   └── `report_reportsubscription_recipients_employees` (employee_id)
├── `employee_employeebankdetails` (created_by_id,modified_by_id)
├── `employee_employeegeneralsetting` (created_by_id,modified_by_id)
├── `employee_employeenote` (created_by_id,modified_by_id) ↩
├── `employee_employeetag` (created_by_id,modified_by_id)
│   └── `employee_employeeworkinformation_tags` (employeetag_id)
├── `employee_historicalbonuspoint` (history_user_id)
│   └── `employee_historicalbonuspoint_history_tags` (historicalbonuspoint_id)
├── `employee_historicalemployeeworkinformation` (history_user_id)
│   └── `employee_historicalemployeeworkinformation_history_tags` (historicalemployeeworkinformation_id)
├── `employee_notefiles` (created_by_id,modified_by_id)
│   └── `employee_employeenote_note_files` (notefiles_id)
├── `employee_policy` (created_by_id,modified_by_id)
│   ├── `employee_policy_attachments` (policy_id)
│   ├── `employee_policy_company_id` (policy_id)
│   ├── `employee_policy_department` (policy_id)
│   ├── `employee_policy_employees` (policy_id)
│   ├── `employee_policy_filtered_employees` (policy_id)
│   └── `employee_policy_job_position` (policy_id)
├── `employee_policymultiplefile` (created_by_id,modified_by_id)
│   └── `employee_policy_attachments` (policymultiplefile_id)
├── `employee_profileeditfeature` (created_by_id,modified_by_id)
├── `helpdesk_attachment` (created_by_id,modified_by_id)
├── `helpdesk_claimrequest` (created_by_id,modified_by_id)
├── `helpdesk_comment` (created_by_id,modified_by_id) ↩
├── `helpdesk_departmentmanager` (created_by_id,modified_by_id)
├── `helpdesk_faq` (created_by_id,modified_by_id) ↩
├── `helpdesk_faqcategory` (created_by_id,modified_by_id) ↩
├── `helpdesk_historicalticket` (history_user_id)
│   └── `helpdesk_historicalticket_history_tags` (historicalticket_id)
├── `helpdesk_ticket` (created_by_id,modified_by_id) ↩
├── `helpdesk_tickettype` (created_by_id,modified_by_id) ↩
├── `horilla_audit_accountblockunblock` (created_by_id,modified_by_id)
├── `horilla_audit_auditmodelconfig` (created_by_id,modified_by_id)
├── `horilla_audit_historytrackingfields` (created_by_id,modified_by_id)
├── `horilla_auth_horillauser_groups` (horillauser_id)
├── `horilla_auth_horillauser_user_permissions` (horillauser_id)
├── `horilla_automations_mailautomation` (created_by_id,modified_by_id) ↩
├── `horilla_dbtemplate_template` (created_by_id,locked_by_id,updated_by_id)
│   ├── `horilla_dbtemplate_template_sites` (template_id)
│   └── `horilla_dbtemplate_templateversion` (template_id)
├── `horilla_dbtemplate_templateversion` (created_by_id)
├── `horilla_documents_document` (created_by_id,modified_by_id)
├── `horilla_documents_documentrequest` (created_by_id,modified_by_id)
│   ├── `horilla_documents_document` (document_request_id_id)
│   └── `horilla_documents_documentrequest_employee_id` (documentrequest_id)
├── `horilla_meet_googlecredential` (created_by_id,modified_by_id)
├── `horilla_meet_googlemeeting` (created_by_id,modified_by_id) ↩
├── `horilla_theme_companytheme` (created_by_id,modified_by_id)
├── `horilla_theme_horillacolortheme` (created_by_id,modified_by_id)
│   └── `horilla_theme_companytheme` (theme_id)
├── `horilla_tour_tour` (created_by_id,modified_by_id) ↩
├── `horilla_tour_tourprogress` (created_by_id,modified_by_id,user_id)
├── `horilla_tour_tourstep` (created_by_id,modified_by_id)
├── `horilla_views_activegroup` (created_by_id,modified_by_id)
├── `horilla_views_activetab` (created_by_id,modified_by_id)
├── `horilla_views_activeview` (created_by_id,modified_by_id)
├── `horilla_views_columnorder` (created_by_id,modified_by_id)
├── `horilla_views_savedfilter` (created_by_id,modified_by_id)
├── `horilla_views_togglecolumn` (created_by_id,modified_by_id,user_id_id)
├── `leave_availableleave` (created_by_id,modified_by_id)
├── `leave_compensatoryleaverequest` (created_by_id,modified_by_id) ↩
├── `leave_compensatoryleaverequestcomment` (created_by_id,modified_by_id) ↩
├── `leave_employeepastleaverestrict` (created_by_id,modified_by_id)
├── `leave_historicalavailableleave` (history_user_id)
│   └── `leave_historicalavailableleave_history_tags` (historicalavailableleave_id)
├── `leave_historicalcompensatoryleaverequest` (history_user_id)
│   └── `leave_historicalcompensatoryleaverequest_history_tags` (historicalcompensatoryleaverequest_id)
├── `leave_historicalleaveallocationrequest` (history_user_id)
│   └── `leave_historicalleaveallocationrequest_history_tags` (historicalleaveallocationrequest_id)
├── `leave_historicalleaverequest` (history_user_id)
│   └── `leave_historicalleaverequest_history_tags` (historicalleaverequest_id)
├── `leave_leaveallocationrequest` (created_by_id,modified_by_id) ↩
├── `leave_leaveallocationrequestcomment` (created_by_id,modified_by_id) ↩
├── `leave_leavegeneralsetting` (created_by_id,modified_by_id)
├── `leave_leaverequest` (modified_by_id) ↩
├── `leave_leaverequestcomment` (created_by_id,modified_by_id) ↩
├── `leave_leavetype` (created_by_id,modified_by_id) ↩
├── `leave_leavetypecondition` (created_by_id,modified_by_id)
│   └── `leave_leavetype_conditions` (leavetypecondition_id)
├── `leave_restrictleave` (created_by_id,modified_by_id) ↩
├── `master_import_importjob` (created_by_id)
├── `notifications_notification` (recipient_id)
├── `offboarding_employeetask` (created_by_id,modified_by_id)
├── `offboarding_exitreason` (created_by_id,modified_by_id) ↩
├── `offboarding_historicalemployeetask` (history_user_id)
│   └── `offboarding_historicalemployeetask_history_tags` (historicalemployeetask_id)
├── `offboarding_historicalresignationletter` (history_user_id)
│   └── `offboarding_historicalresignationletter_history_tags` (historicalresignationletter_id)
├── `offboarding_offboarding` (created_by_id,modified_by_id) ↩
├── `offboarding_offboardingemployee` (created_by_id,modified_by_id) ↩
├── `offboarding_offboardinggeneralsetting` (created_by_id,modified_by_id)
├── `offboarding_offboardingnote` (created_by_id,modified_by_id) ↩
├── `offboarding_offboardingstage` (created_by_id,modified_by_id) ↩
├── `offboarding_offboardingstagemultiplefile` (created_by_id,modified_by_id)
│   ├── `offboarding_exitreason_attachments` (offboardingstagemultiplefile_id)
│   └── `offboarding_offboardingnote_attachments` (offboardingstagemultiplefile_id)
├── `offboarding_offboardingtask` (created_by_id,modified_by_id) ↩
├── `offboarding_resignationletter` (created_by_id,modified_by_id)
├── `onboarding_candidatestage` (created_by_id,modified_by_id)
├── `onboarding_candidatetask` (created_by_id,modified_by_id)
├── `onboarding_historicalcandidatetask` (history_user_id)
│   └── `onboarding_historicalcandidatetask_history_tags` (historicalcandidatetask_id)
├── `onboarding_onboardingportal` (created_by_id,modified_by_id)
├── `onboarding_onboardingstage` (created_by_id,modified_by_id) ↩
├── `onboarding_onboardingtask` (created_by_id,modified_by_id) ↩
├── `payroll_allowance` (created_by_id,modified_by_id) ↩
├── `payroll_contract` (created_by_id,modified_by_id)
├── `payroll_deduction` (created_by_id,modified_by_id) ↩
├── `payroll_filingstatus` (created_by_id,modified_by_id) ↩
├── `payroll_historicalcontract` (history_user_id)
│   └── `payroll_historicalcontract_history_tags` (historicalcontract_id)
├── `payroll_historicalpayslip` (history_user_id)
│   └── `payroll_historicalpayslip_history_tags` (historicalpayslip_id)
├── `payroll_loanaccount` (created_by_id,modified_by_id) ↩
├── `payroll_payperiodsettings` (created_by_id,modified_by_id)
├── `payroll_payrollbatch` (created_by_id,created_by_user_id,modified_by_id) ↩
├── `payroll_payrollbatchline` (created_by_id,modified_by_id)
├── `payroll_payrollsettings` (created_by_id,modified_by_id)
├── `payroll_payslip` (created_by_id,modified_by_id) ↩
├── `payroll_reimbursement` (created_by_id,modified_by_id) ↩
├── `payroll_reimbursementrequestcomment` (created_by_id,modified_by_id) ↩
├── `payroll_salarystructure` (created_by_id,modified_by_id) ↩
├── `payroll_taxbracket` (created_by_id,modified_by_id)
├── `pms_employeebonuspoint` (created_by_id,modified_by_id)
├── `pms_employeeobjective` (created_by_id,modified_by_id) ↩
├── `pms_feedback` (created_by_id,modified_by_id) ↩
├── `pms_historicalcomment` (history_user_id)
│   └── `pms_historicalcomment_history_tags` (historicalcomment_id)
├── `pms_historicalemployeekeyresult` (history_user_id)
│   └── `pms_historicalemployeekeyresult_history_tags` (historicalemployeekeyresult_id)
├── `pms_historicalemployeeobjective` (history_user_id)
│   └── `pms_historicalemployeeobjective_history_tags` (historicalemployeeobjective_id)
├── `pms_historicalkeyresult` (history_user_id)
│   └── `pms_historicalkeyresult_history_tags` (historicalkeyresult_id)
├── `pms_historicalobjective` (history_user_id)
│   └── `pms_historicalobjective_history_tags` (historicalobjective_id)
├── `pms_keyresult` (created_by_id,modified_by_id) ↩
├── `pms_meetings` (created_by_id,modified_by_id) ↩
├── `pms_objective` (created_by_id,modified_by_id) ↩
├── `pms_period` (created_by_id,modified_by_id)
│   └── `pms_period_company_id` (period_id)
├── `pms_question` (created_by_id,modified_by_id)
│   ├── `pms_answer` (question_id_id)
│   ├── `pms_meetingsanswer` (question_id_id)
│   └── `pms_questionoptions` (question_id_id)
├── `pms_questionoptions` (created_by_id,modified_by_id)
├── `pms_questiontemplate` (created_by_id,modified_by_id)
│   ├── `pms_feedback` (question_template_id_id) ↩
│   ├── `pms_meetings` (question_template_id) ↩
│   ├── `pms_question` (template_id_id) ↩
│   └── `pms_questiontemplate_company_id` (questiontemplate_id)
├── `project_project` (created_by_id,modified_by_id) ↩
├── `project_projectstage` (created_by_id,modified_by_id) ↩
├── `project_task` (created_by_id,modified_by_id) ↩
├── `project_timesheet` (created_by_id,modified_by_id)
├── `recruitment_candidate` (created_by_id,modified_by_id) ↩
├── `recruitment_candidatedocument` (created_by_id,modified_by_id)
├── `recruitment_candidatedocumentrequest` (created_by_id,modified_by_id)
│   ├── `recruitment_candidatedocument` (document_request_id_id)
│   └── `recruitment_candidatedocumentrequest_candidate_id` (candidatedocumentrequest_id)
├── `recruitment_candidaterating` (created_by_id,modified_by_id)
├── `recruitment_historicalcandidate` (history_user_id)
│   └── `recruitment_historicalcandidate_history_tags` (historicalcandidate_id)
├── `recruitment_historicalrejectedcandidate` (history_user_id)
│   └── `recruitment_historicalrejectedcandidate_history_tags` (historicalrejectedcandidate_id)
├── `recruitment_historicalstage` (history_user_id)
│   └── `recruitment_historicalstage_history_tags` (historicalstage_id)
├── `recruitment_interviewschedule` (created_by_id,modified_by_id) ↩
├── `recruitment_linkedinaccount` (created_by_id,modified_by_id) ↩
├── `recruitment_questionordering` (created_by_id,modified_by_id)
├── `recruitment_recruitment` (created_by_id,modified_by_id) ↩
├── `recruitment_recruitmentgeneralsetting` (created_by_id,modified_by_id)
├── `recruitment_recruitmentsurvey` (created_by_id,modified_by_id)
│   ├── `recruitment_questionordering` (question_id_id)
│   ├── `recruitment_recruitmentsurvey_job_position_ids` (recruitmentsurvey_id)
│   └── `recruitment_recruitmentsurvey_template_id` (recruitmentsurvey_id)
├── `recruitment_recruitmentsurveyanswer` (created_by_id,modified_by_id)
├── `recruitment_rejectedcandidate` (created_by_id,modified_by_id) ↩
├── `recruitment_rejectreason` (created_by_id,modified_by_id) ↩
├── `recruitment_skill` (created_by_id,modified_by_id)
│   └── `recruitment_recruitment_skills` (skill_id)
├── `recruitment_skillzone` (created_by_id,modified_by_id) ↩
├── `recruitment_skillzonecandidate` (created_by_id,modified_by_id)
├── `recruitment_stage` (created_by_id,modified_by_id) ↩
├── `recruitment_stagefiles` (created_by_id,modified_by_id)
│   └── `recruitment_stagenote_stage_files` (stagefiles_id)
├── `recruitment_stagenote` (created_by_id,modified_by_id) ↩
├── `recruitment_surveytemplate` (created_by_id,modified_by_id) ↩
├── `report_reportaccess` (created_by_id,modified_by_id)
├── `report_reportfavorite` (created_by_id,modified_by_id,user_id)
├── `report_reportfilterpreset` (created_by_id,modified_by_id,user_id)
├── `report_reportrunlog` (created_by_id,modified_by_id,user_id)
├── `report_reportsavedview` (created_by_id,modified_by_id,owner_id)
├── `report_reportsubscription` (created_by_id,modified_by_id,owner_id) ↩
├── `report_reporttemplate` (created_by_id,modified_by_id)
├── `token_blacklist_outstandingtoken` (user_id)
│   └── `token_blacklist_blacklistedtoken` (token_id)
└── `whatsapp_whatsappcredientials` (created_by_id,modified_by_id)
    ├── `whatsapp_whatsappcredientials_company_id` (whatsappcredientials_id)
    └── `whatsapp_whatsappflowdetails` (whatsapp_id_id)
```

### `leave_leaverequestfile`  (direct dependents: 3, total: 3)

```
leave_leaverequestfile
├── `leave_compensatoryleaverequestcomment_files` (leaverequestfile_id)
├── `leave_leaveallocationrequestcomment_files` (leaverequestfile_id)
└── `leave_leaverequestcomment_files` (leaverequestfile_id)
```

### `payroll_applycondition`  (direct dependents: 2, total: 2)

```
payroll_applycondition
├── `payroll_allowance_apply_conditions` (applycondition_id)
└── `payroll_deduction_apply_conditions` (applycondition_id)
```

### `payroll_encashmentgeneralsettings`  (direct dependents: 4, total: 4)

```
payroll_encashmentgeneralsettings
├── `payroll_encashmentgeneralsettings_department` (encashmentgeneralsettings_id)
├── `payroll_encashmentgeneralsettings_employees` (encashmentgeneralsettings_id)
├── `payroll_encashmentgeneralsettings_filtered_employees` (encashmentgeneralsettings_id)
└── `payroll_encashmentgeneralsettings_job_position` (encashmentgeneralsettings_id)
```

### `payroll_multiplecondition`  (direct dependents: 2, total: 2)

```
payroll_multiplecondition
├── `payroll_allowance_other_conditions` (multiplecondition_id)
└── `payroll_deduction_other_conditions` (multiplecondition_id)
```

### `payroll_reimbursementfile`  (direct dependents: 1, total: 1)

```
payroll_reimbursementfile
└── `payroll_reimbursementrequestcomment_files` (reimbursementfile_id)
```

### `payroll_reimbursementmultipleattachment`  (direct dependents: 1, total: 1)

```
payroll_reimbursementmultipleattachment
└── `payroll_reimbursement_other_attachments` (reimbursementmultipleattachment_id)
```

### Isolated tables (no FKs in or out)

- `axes_accessfailurelog`
- `axes_accesslog`
- `django_migrations`
- `django_session`
- `horilla_backup_googledrivebackup`
- `horilla_backup_localbackup`
- `horilla_ldap_ldapsettings`

## 5. Per-table dependency closure (what each table needs)

For each table: direct parents, and total transitive ancestors (everything that must exist first) / total transitive descendants (everything that breaks if dropped).

| Table | Level | Direct parents | Ancestors | Direct children | Descendants |
|---|---|---|---|---|---|
| `accessibility_defaultaccessibility` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `accessibility_defaultaccessibility_employees` | 2 | `accessibility_defaultaccessibility`, `employee_employee` | 3 | 0 | 0 |
| `asset_asset` | 2 | `asset_assetcategory`, `asset_assetlot`, `employee_employee`, `horilla_auth_horillauser` | 4 | 4 | 10 |
| `asset_assetassignment` | 4 | `asset_asset`, `asset_assetitem`, `employee_employee`, `horilla_auth_horillauser` | 6 | 3 | 4 |
| `asset_assetassignment_assign_images` | 5 | `asset_assetassignment`, `asset_returnimages` | 8 | 0 | 0 |
| `asset_assetassignment_return_images` | 5 | `asset_assetassignment`, `asset_returnimages` | 8 | 0 | 0 |
| `asset_assetcategory` | 1 | `horilla_auth_horillauser` | 1 | 3 | 14 |
| `asset_assetcategory_company_id` | 2 | `asset_assetcategory`, `base_company` | 3 | 0 | 0 |
| `asset_assetdocuments` | 4 | `asset_assetreport`, `horilla_auth_horillauser` | 6 | 0 | 0 |
| `asset_assetgeneralsetting` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `asset_assetitem` | 3 | `asset_asset`, `horilla_auth_horillauser` | 5 | 1 | 5 |
| `asset_assetlot` | 1 | `horilla_auth_horillauser` | 1 | 2 | 12 |
| `asset_assetlot_company_id` | 2 | `asset_assetlot`, `base_company` | 3 | 0 | 0 |
| `asset_assetreport` | 3 | `asset_asset`, `horilla_auth_horillauser` | 5 | 1 | 1 |
| `asset_assetrequest` | 2 | `asset_assetcategory`, `employee_employee`, `horilla_auth_horillauser` | 3 | 1 | 1 |
| `asset_assetrequestcomment` | 3 | `asset_assetrequest`, `employee_employee`, `horilla_auth_horillauser` | 4 | 0 | 0 |
| `asset_assetservicerequest` | 5 | `asset_assetassignment`, `employee_employee`, `horilla_auth_horillauser` | 7 | 1 | 1 |
| `asset_assetservicerequestnote` | 6 | `asset_assetservicerequest`, `employee_employee`, `horilla_auth_horillauser` | 8 | 0 | 0 |
| `asset_returnimages` | 1 | `horilla_auth_horillauser` | 1 | 2 | 2 |
| `attendance_attendance` | 3 | `attendance_batchattendance`, `base_employeeshift`, `base_employeeshiftday`, `base_worktype`, `employee_employee`, `horilla_auth_horillauser` | 7 | 4 | 6 |
| `attendance_attendanceactivity` | 2 | `base_employeeshiftday`, `employee_employee`, `horilla_auth_horillauser` | 3 | 0 | 0 |
| `attendance_attendanceconflictresolution` | 2 | `employee_employee`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `attendance_attendancedailyhours` | 2 | `employee_employee`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `attendance_attendancegeneralsetting` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `attendance_attendancelatecomeearlyout` | 4 | `attendance_attendance`, `employee_employee`, `horilla_auth_horillauser` | 8 | 1 | 1 |
| `attendance_attendanceovertime` | 2 | `employee_employee`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `attendance_attendancerequestcomment` | 4 | `attendance_attendance`, `employee_employee`, `horilla_auth_horillauser` | 8 | 1 | 1 |
| `attendance_attendancerequestcomment_files` | 5 | `attendance_attendancerequestcomment`, `attendance_attendancerequestfile` | 10 | 0 | 0 |
| `attendance_attendancerequestfile` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `attendance_attendancesummaryhours` | 2 | `employee_employee`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `attendance_attendancesummaryoverride` | 2 | `employee_employee`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `attendance_attendancevalidationcondition` | 1 | `horilla_auth_horillauser` | 1 | 2 | 2 |
| `attendance_attendancevalidationcondition_company_id` | 2 | `attendance_attendancevalidationcondition`, `base_company` | 3 | 0 | 0 |
| `attendance_attendancevalidationcondition_shift_ids` | 3 | `attendance_attendancevalidationcondition`, `base_employeeshift` | 4 | 0 | 0 |
| `attendance_batchattendance` | 1 | `horilla_auth_horillauser` | 1 | 1 | 7 |
| `attendance_gracetime` | 1 | `horilla_auth_horillauser` | 1 | 2 | 34 |
| `attendance_gracetime_company_id` | 2 | `attendance_gracetime`, `base_company` | 3 | 0 | 0 |
| `attendance_historicalattendance` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `attendance_historicalattendance_history_tags` | 2 | `attendance_historicalattendance`, `horilla_audit_audittag` | 3 | 0 | 0 |
| `attendance_historicalattendanceactivity` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `attendance_historicalattendanceactivity_history_tags` | 2 | `attendance_historicalattendanceactivity`, `horilla_audit_audittag` | 3 | 0 | 0 |
| `attendance_workrecords` | 4 | `attendance_attendance`, `base_employeeshift`, `employee_employee`, `leave_leaverequest` | 11 | 0 | 0 |
| `auditlog_logentry` | 1 | `django_content_type`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `auth_group` | 0 | — | 0 | 4 | 4 |
| `auth_group_permissions` | 2 | `auth_group`, `auth_permission` | 3 | 0 | 0 |
| `auth_permission` | 1 | `django_content_type` | 1 | 2 | 2 |
| `axes_accessattempt` | 0 | — | 0 | 1 | 1 |
| `axes_accessattemptexpiration` | 1 | `axes_accessattempt` | 1 | 0 | 0 |
| `axes_accessfailurelog` | 0 | — | 0 | 0 | 0 |
| `axes_accesslog` | 0 | — | 0 | 0 | 0 |
| `base_announcement` | 1 | `horilla_auth_horillauser` | 1 | 8 | 8 |
| `base_announcement_attachments` | 2 | `base_announcement`, `base_attachment` | 3 | 0 | 0 |
| `base_announcement_company_id` | 2 | `base_announcement`, `base_company` | 3 | 0 | 0 |
| `base_announcement_department` | 2 | `base_announcement`, `base_department` | 3 | 0 | 0 |
| `base_announcement_employees` | 2 | `base_announcement`, `employee_employee` | 3 | 0 | 0 |
| `base_announcement_filtered_employees` | 2 | `base_announcement`, `employee_employee` | 3 | 0 | 0 |
| `base_announcement_job_position` | 3 | `base_announcement`, `base_jobposition` | 4 | 0 | 0 |
| `base_announcementcomment` | 2 | `base_announcement`, `employee_employee`, `horilla_auth_horillauser` | 3 | 0 | 0 |
| `base_announcementexpire` | 2 | `base_company` | 2 | 0 | 0 |
| `base_announcementview` | 2 | `base_announcement`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `base_attachment` | 0 | — | 0 | 1 | 1 |
| `base_attendanceallowedip` | 2 | `base_company` | 2 | 0 | 0 |
| `base_baserequestfile` | 0 | — | 0 | 2 | 2 |
| `base_biometricattendance` | 2 | `base_company` | 2 | 0 | 0 |
| `base_company` | 1 | `horilla_auth_horillauser` | 1 | 83 | 206 |
| `base_companygroupassignment` | 2 | `auth_group`, `base_company`, `horilla_auth_horillauser` | 3 | 0 | 0 |
| `base_companylanguagesetting` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `base_companyleaves` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `base_companyleaves_company_id` | 2 | `base_company`, `base_companyleaves` | 3 | 0 | 0 |
| `base_dashboardemployeecharts` | 2 | `employee_employee`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `base_defaultexportpermission` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `base_department` | 1 | `horilla_auth_horillauser` | 1 | 14 | 45 |
| `base_department_company_id` | 2 | `base_company`, `base_department` | 3 | 0 | 0 |
| `base_driverviewed` | 1 | `horilla_auth_horillauser` | 1 | 0 | 0 |
| `base_dynamicemailconfiguration` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `base_dynamicpagination` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `base_emaillog` | 2 | `base_company` | 2 | 0 | 0 |
| `base_employeeshift` | 2 | `attendance_gracetime`, `horilla_auth_horillauser` | 2 | 12 | 32 |
| `base_employeeshift_company_id` | 3 | `base_company`, `base_employeeshift` | 4 | 0 | 0 |
| `base_employeeshiftday` | 0 | — | 0 | 4 | 11 |
| `base_employeeshiftday_company_id` | 2 | `base_company`, `base_employeeshiftday` | 3 | 0 | 0 |
| `base_employeeshiftschedule` | 3 | `base_employeeshift`, `base_employeeshiftday`, `horilla_auth_horillauser` | 4 | 1 | 1 |
| `base_employeeshiftschedule_company_id` | 4 | `base_company`, `base_employeeshiftschedule` | 6 | 0 | 0 |
| `base_employeetype` | 1 | `horilla_auth_horillauser` | 1 | 2 | 3 |
| `base_employeetype_company_id` | 2 | `base_company`, `base_employeetype` | 3 | 0 | 0 |
| `base_historicalrotatingshiftassign` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `base_historicalrotatingshiftassign_history_tags` | 2 | `base_historicalrotatingshiftassign`, `horilla_audit_audittag` | 3 | 0 | 0 |
| `base_historicalrotatingworktypeassign` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `base_historicalrotatingworktypeassign_history_tags` | 2 | `base_historicalrotatingworktypeassign`, `horilla_audit_audittag` | 3 | 0 | 0 |
| `base_historicalshiftrequest` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `base_historicalshiftrequest_history_tags` | 2 | `base_historicalshiftrequest`, `horilla_audit_audittag` | 3 | 0 | 0 |
| `base_historicalworktyperequest` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `base_historicalworktyperequest_history_tags` | 2 | `base_historicalworktyperequest`, `horilla_audit_audittag` | 3 | 0 | 0 |
| `base_holidays` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 3 | 3 |
| `base_holidays_department` | 3 | `base_department`, `base_holidays` | 4 | 0 | 0 |
| `base_holidays_employees` | 3 | `base_holidays`, `employee_employee` | 4 | 0 | 0 |
| `base_holidays_job_position` | 3 | `base_holidays`, `base_jobposition` | 5 | 0 | 0 |
| `base_horillamailtemplate` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 2 | 3 |
| `base_integrationapps` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `base_jobposition` | 2 | `base_department`, `horilla_auth_horillauser` | 2 | 14 | 31 |
| `base_jobposition_company_id` | 3 | `base_company`, `base_jobposition` | 4 | 0 | 0 |
| `base_jobrole` | 3 | `base_jobposition`, `horilla_auth_horillauser` | 3 | 3 | 4 |
| `base_jobrole_company_id` | 4 | `base_company`, `base_jobrole` | 5 | 0 | 0 |
| `base_multipleapprovalcondition` | 2 | `base_company`, `base_department`, `horilla_auth_horillauser` | 3 | 1 | 1 |
| `base_multipleapprovalmanagers` | 3 | `base_multipleapprovalcondition` | 4 | 0 | 0 |
| `base_notificationsound` | 2 | `employee_employee` | 2 | 0 | 0 |
| `base_penaltyaccounts` | 5 | `attendance_attendancelatecomeearlyout`, `employee_employee`, `horilla_auth_horillauser`, `leave_leaverequest`, `leave_leavetype` | 12 | 0 | 0 |
| `base_roster` | 3 | `base_department`, `base_employeeshift`, `employee_employee`, `horilla_auth_horillauser` | 5 | 0 | 0 |
| `base_rosterpublishlog` | 2 | `base_department`, `employee_employee` | 3 | 0 | 0 |
| `base_rotatingshift` | 3 | `base_employeeshift`, `horilla_auth_horillauser` | 3 | 1 | 1 |
| `base_rotatingshiftassign` | 4 | `base_employeeshift`, `base_rotatingshift`, `employee_employee`, `horilla_auth_horillauser` | 5 | 0 | 0 |
| `base_rotatingworktype` | 2 | `base_worktype`, `horilla_auth_horillauser` | 2 | 1 | 1 |
| `base_rotatingworktypeassign` | 3 | `base_rotatingworktype`, `base_worktype`, `employee_employee`, `horilla_auth_horillauser` | 4 | 0 | 0 |
| `base_setupchecklistdismissal` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `base_shiftrequest` | 3 | `base_employeeshift`, `employee_employee`, `horilla_auth_horillauser` | 4 | 1 | 2 |
| `base_shiftrequestcomment` | 4 | `base_shiftrequest`, `employee_employee`, `horilla_auth_horillauser` | 5 | 1 | 1 |
| `base_shiftrequestcomment_files` | 5 | `base_baserequestfile`, `base_shiftrequestcomment` | 7 | 0 | 0 |
| `base_tags` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 2 | 2 |
| `base_tracklatecomeearlyout` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `base_worktype` | 1 | `horilla_auth_horillauser` | 1 | 8 | 28 |
| `base_worktype_company_id` | 2 | `base_company`, `base_worktype` | 3 | 0 | 0 |
| `base_worktyperequest` | 2 | `base_worktype`, `employee_employee`, `horilla_auth_horillauser` | 3 | 1 | 2 |
| `base_worktyperequestcomment` | 3 | `base_worktyperequest`, `employee_employee`, `horilla_auth_horillauser` | 4 | 1 | 1 |
| `base_worktyperequestcomment_files` | 4 | `base_baserequestfile`, `base_worktyperequestcomment` | 6 | 0 | 0 |
| `biometric_biometricdevices` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 2 | 2 |
| `biometric_biometricemployees` | 3 | `biometric_biometricdevices`, `employee_employee` | 4 | 0 | 0 |
| `biometric_cosecattendancearguments` | 3 | `biometric_biometricdevices` | 3 | 0 | 0 |
| `django_admin_log` | 1 | `django_content_type`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `django_apscheduler_djangojob` | 0 | — | 0 | 1 | 1 |
| `django_apscheduler_djangojobexecution` | 1 | `django_apscheduler_djangojob` | 1 | 0 | 0 |
| `django_content_type` | 0 | — | 0 | 4 | 6 |
| `django_migrations` | 0 | — | 0 | 0 | 0 |
| `django_session` | 0 | — | 0 | 0 | 0 |
| `django_site` | 0 | — | 0 | 1 | 1 |
| `employee_actiontype` | 1 | `horilla_auth_horillauser` | 1 | 1 | 2 |
| `employee_bonuspoint` | 2 | `employee_employee`, `horilla_auth_horillauser` | 2 | 1 | 1 |
| `employee_disciplinaryaction` | 2 | `employee_actiontype`, `horilla_auth_horillauser` | 2 | 1 | 1 |
| `employee_disciplinaryaction_employee_id` | 3 | `employee_disciplinaryaction`, `employee_employee` | 4 | 0 | 0 |
| `employee_employee` | 1 | `horilla_auth_horillauser` | 1 | 108 | 151 |
| `employee_employeebankdetails` | 2 | `employee_employee`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `employee_employeegeneralsetting` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `employee_employeenote` | 2 | `employee_employee`, `horilla_auth_horillauser` | 2 | 1 | 1 |
| `employee_employeenote_note_files` | 3 | `employee_employeenote`, `employee_notefiles` | 4 | 0 | 0 |
| `employee_employeetag` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `employee_employeeworkinformation` | 4 | `base_company`, `base_department`, `base_employeeshift`, `base_employeetype`, `base_jobposition`, `base_jobrole`, `base_worktype`, `employee_employee` | 10 | 1 | 1 |
| `employee_employeeworkinformation_tags` | 5 | `employee_employeetag`, `employee_employeeworkinformation` | 12 | 0 | 0 |
| `employee_historicalbonuspoint` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `employee_historicalbonuspoint_history_tags` | 2 | `employee_historicalbonuspoint`, `horilla_audit_audittag` | 3 | 0 | 0 |
| `employee_historicalemployeeworkinformation` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `employee_historicalemployeeworkinformation_history_tags` | 2 | `employee_historicalemployeeworkinformation`, `horilla_audit_audittag` | 3 | 0 | 0 |
| `employee_notefiles` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `employee_policy` | 1 | `horilla_auth_horillauser` | 1 | 6 | 6 |
| `employee_policy_attachments` | 2 | `employee_policy`, `employee_policymultiplefile` | 3 | 0 | 0 |
| `employee_policy_company_id` | 2 | `base_company`, `employee_policy` | 3 | 0 | 0 |
| `employee_policy_department` | 2 | `base_department`, `employee_policy` | 3 | 0 | 0 |
| `employee_policy_employees` | 2 | `employee_employee`, `employee_policy` | 3 | 0 | 0 |
| `employee_policy_filtered_employees` | 2 | `employee_employee`, `employee_policy` | 3 | 0 | 0 |
| `employee_policy_job_position` | 3 | `base_jobposition`, `employee_policy` | 4 | 0 | 0 |
| `employee_policymultiplefile` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `employee_profileeditfeature` | 1 | `horilla_auth_horillauser` | 1 | 0 | 0 |
| `facedetection_employeefacedetection` | 2 | `employee_employee` | 2 | 0 | 0 |
| `facedetection_facedetection` | 2 | `base_company` | 2 | 0 | 0 |
| `geofencing_geofencing` | 2 | `base_company` | 2 | 0 | 0 |
| `helpdesk_attachment` | 5 | `helpdesk_comment`, `helpdesk_ticket`, `horilla_auth_horillauser` | 6 | 0 | 0 |
| `helpdesk_claimrequest` | 4 | `employee_employee`, `helpdesk_ticket`, `horilla_auth_horillauser` | 5 | 0 | 0 |
| `helpdesk_comment` | 4 | `employee_employee`, `helpdesk_ticket`, `horilla_auth_horillauser` | 5 | 1 | 1 |
| `helpdesk_departmentmanager` | 2 | `base_company`, `base_department`, `employee_employee`, `horilla_auth_horillauser` | 4 | 0 | 0 |
| `helpdesk_faq` | 3 | `base_company`, `helpdesk_faqcategory`, `horilla_auth_horillauser` | 3 | 1 | 1 |
| `helpdesk_faq_tags` | 4 | `base_tags`, `helpdesk_faq` | 5 | 0 | 0 |
| `helpdesk_faqcategory` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 1 | 2 |
| `helpdesk_historicalticket` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `helpdesk_historicalticket_history_tags` | 2 | `helpdesk_historicalticket`, `horilla_audit_audittag` | 3 | 0 | 0 |
| `helpdesk_ticket` | 3 | `employee_employee`, `helpdesk_tickettype`, `horilla_auth_horillauser` | 4 | 5 | 5 |
| `helpdesk_ticket_assigned_to` | 4 | `employee_employee`, `helpdesk_ticket` | 5 | 0 | 0 |
| `helpdesk_ticket_tags` | 4 | `base_tags`, `helpdesk_ticket` | 6 | 0 | 0 |
| `helpdesk_tickettype` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 1 | 6 |
| `horilla_audit_accountblockunblock` | 1 | `horilla_auth_horillauser` | 1 | 0 | 0 |
| `horilla_audit_auditmodelconfig` | 1 | `horilla_auth_horillauser` | 1 | 0 | 0 |
| `horilla_audit_audittag` | 0 | — | 0 | 26 | 26 |
| `horilla_audit_historytrackingfields` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `horilla_auth_horillauser` | 0 | — | 0 | 222 | 389 |
| `horilla_auth_horillauser_groups` | 1 | `auth_group`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `horilla_auth_horillauser_user_permissions` | 2 | `auth_permission`, `horilla_auth_horillauser` | 3 | 0 | 0 |
| `horilla_automations_mailautomation` | 3 | `base_horillamailtemplate`, `horilla_auth_horillauser` | 3 | 2 | 2 |
| `horilla_automations_mailautomation_also_sent_to` | 4 | `employee_employee`, `horilla_automations_mailautomation` | 5 | 0 | 0 |
| `horilla_automations_mailautomation_template_attachments` | 4 | `base_horillamailtemplate`, `horilla_automations_mailautomation` | 4 | 0 | 0 |
| `horilla_backup_googledrivebackup` | 0 | — | 0 | 0 | 0 |
| `horilla_backup_localbackup` | 0 | — | 0 | 0 | 0 |
| `horilla_dbtemplate_template` | 1 | `horilla_auth_horillauser` | 1 | 2 | 2 |
| `horilla_dbtemplate_template_sites` | 2 | `django_site`, `horilla_dbtemplate_template` | 3 | 0 | 0 |
| `horilla_dbtemplate_templateversion` | 2 | `horilla_auth_horillauser`, `horilla_dbtemplate_template` | 2 | 0 | 0 |
| `horilla_documents_document` | 2 | `employee_employee`, `horilla_auth_horillauser`, `horilla_documents_documentrequest` | 3 | 0 | 0 |
| `horilla_documents_documentrequest` | 1 | `horilla_auth_horillauser` | 1 | 2 | 2 |
| `horilla_documents_documentrequest_employee_id` | 2 | `employee_employee`, `horilla_documents_documentrequest` | 3 | 0 | 0 |
| `horilla_ldap_ldapsettings` | 0 | — | 0 | 0 | 0 |
| `horilla_meet_googlecloudcredential` | 2 | `base_company` | 2 | 0 | 0 |
| `horilla_meet_googlecredential` | 2 | `employee_employee`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `horilla_meet_googlemeeting` | 2 | `employee_employee`, `horilla_auth_horillauser` | 2 | 2 | 2 |
| `horilla_meet_interviewmeetinglink` | 7 | `horilla_meet_googlemeeting`, `recruitment_interviewschedule` | 11 | 0 | 0 |
| `horilla_meet_pmsmeetinglink` | 3 | `horilla_meet_googlemeeting`, `pms_meetings` | 6 | 0 | 0 |
| `horilla_theme_companytheme` | 2 | `base_company`, `horilla_auth_horillauser`, `horilla_theme_horillacolortheme` | 3 | 0 | 0 |
| `horilla_theme_horillacolortheme` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `horilla_tour_tour` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 2 | 2 |
| `horilla_tour_tourprogress` | 3 | `horilla_auth_horillauser`, `horilla_tour_tour` | 3 | 0 | 0 |
| `horilla_tour_tourstep` | 3 | `horilla_auth_horillauser`, `horilla_tour_tour` | 3 | 0 | 0 |
| `horilla_views_activegroup` | 1 | `horilla_auth_horillauser` | 1 | 0 | 0 |
| `horilla_views_activetab` | 1 | `horilla_auth_horillauser` | 1 | 0 | 0 |
| `horilla_views_activeview` | 1 | `horilla_auth_horillauser` | 1 | 0 | 0 |
| `horilla_views_columnorder` | 2 | `employee_employee`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `horilla_views_savedfilter` | 1 | `horilla_auth_horillauser` | 1 | 0 | 0 |
| `horilla_views_togglecolumn` | 1 | `horilla_auth_horillauser` | 1 | 0 | 0 |
| `leave_availableleave` | 3 | `employee_employee`, `horilla_auth_horillauser`, `leave_leavetype` | 4 | 0 | 0 |
| `leave_compensatoryleaverequest` | 3 | `employee_employee`, `horilla_auth_horillauser`, `leave_leavetype` | 4 | 2 | 3 |
| `leave_compensatoryleaverequest_attendance_id` | 4 | `attendance_attendance`, `leave_compensatoryleaverequest` | 11 | 0 | 0 |
| `leave_compensatoryleaverequestcomment` | 4 | `employee_employee`, `horilla_auth_horillauser`, `leave_compensatoryleaverequest` | 5 | 1 | 1 |
| `leave_compensatoryleaverequestcomment_files` | 5 | `leave_compensatoryleaverequestcomment`, `leave_leaverequestfile` | 7 | 0 | 0 |
| `leave_employeepastleaverestrict` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `leave_historicalavailableleave` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `leave_historicalavailableleave_history_tags` | 2 | `horilla_audit_audittag`, `leave_historicalavailableleave` | 3 | 0 | 0 |
| `leave_historicalcompensatoryleaverequest` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `leave_historicalcompensatoryleaverequest_history_tags` | 2 | `horilla_audit_audittag`, `leave_historicalcompensatoryleaverequest` | 3 | 0 | 0 |
| `leave_historicalleaveallocationrequest` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `leave_historicalleaveallocationrequest_history_tags` | 2 | `horilla_audit_audittag`, `leave_historicalleaveallocationrequest` | 3 | 0 | 0 |
| `leave_historicalleaverequest` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `leave_historicalleaverequest_history_tags` | 2 | `horilla_audit_audittag`, `leave_historicalleaverequest` | 3 | 0 | 0 |
| `leave_leaveallocationrequest` | 3 | `employee_employee`, `horilla_auth_horillauser`, `leave_leavetype` | 4 | 1 | 2 |
| `leave_leaveallocationrequestcomment` | 4 | `employee_employee`, `horilla_auth_horillauser`, `leave_leaveallocationrequest` | 5 | 1 | 1 |
| `leave_leaveallocationrequestcomment_files` | 5 | `leave_leaveallocationrequestcomment`, `leave_leaverequestfile` | 7 | 0 | 0 |
| `leave_leavegeneralsetting` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `leave_leaverequest` | 3 | `employee_employee`, `horilla_auth_horillauser`, `leave_leavetype` | 4 | 6 | 7 |
| `leave_leaverequestcomment` | 4 | `employee_employee`, `horilla_auth_horillauser`, `leave_leaverequest` | 5 | 1 | 1 |
| `leave_leaverequestcomment_files` | 5 | `leave_leaverequestcomment`, `leave_leaverequestfile` | 7 | 0 | 0 |
| `leave_leaverequestconditionapproval` | 4 | `employee_employee`, `leave_leaverequest` | 5 | 0 | 0 |
| `leave_leaverequestfile` | 0 | — | 0 | 3 | 3 |
| `leave_leavetype` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 9 | 23 |
| `leave_leavetype_conditions` | 3 | `leave_leavetype`, `leave_leavetypecondition` | 4 | 0 | 0 |
| `leave_leavetypecondition` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `leave_overrideleaverequests` | 4 | `leave_leaverequest` | 5 | 0 | 0 |
| `leave_restrictleave` | 2 | `base_company`, `base_department`, `horilla_auth_horillauser` | 3 | 3 | 3 |
| `leave_restrictleave_exclued_leave_types` | 3 | `leave_leavetype`, `leave_restrictleave` | 5 | 0 | 0 |
| `leave_restrictleave_job_position` | 3 | `base_jobposition`, `leave_restrictleave` | 5 | 0 | 0 |
| `leave_restrictleave_spesific_leave_types` | 3 | `leave_leavetype`, `leave_restrictleave` | 5 | 0 | 0 |
| `master_import_importjob` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `notifications_notification` | 1 | `django_content_type`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `offboarding_employeetask` | 5 | `horilla_auth_horillauser`, `offboarding_offboardingemployee`, `offboarding_offboardingtask` | 7 | 0 | 0 |
| `offboarding_exitreason` | 5 | `horilla_auth_horillauser`, `offboarding_offboardingemployee` | 6 | 1 | 1 |
| `offboarding_exitreason_attachments` | 6 | `offboarding_exitreason`, `offboarding_offboardingstagemultiplefile` | 8 | 0 | 0 |
| `offboarding_historicalemployeetask` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `offboarding_historicalemployeetask_history_tags` | 2 | `horilla_audit_audittag`, `offboarding_historicalemployeetask` | 3 | 0 | 0 |
| `offboarding_historicalresignationletter` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `offboarding_historicalresignationletter_history_tags` | 2 | `horilla_audit_audittag`, `offboarding_historicalresignationletter` | 3 | 0 | 0 |
| `offboarding_offboarding` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 2 | 12 |
| `offboarding_offboarding_managers` | 3 | `employee_employee`, `offboarding_offboarding` | 4 | 0 | 0 |
| `offboarding_offboardingemployee` | 4 | `employee_employee`, `horilla_auth_horillauser`, `offboarding_offboardingstage` | 5 | 4 | 6 |
| `offboarding_offboardinggeneralsetting` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `offboarding_offboardingnote` | 5 | `employee_employee`, `horilla_auth_horillauser`, `offboarding_offboardingemployee`, `offboarding_offboardingstage` | 6 | 1 | 1 |
| `offboarding_offboardingnote_attachments` | 6 | `offboarding_offboardingnote`, `offboarding_offboardingstagemultiplefile` | 8 | 0 | 0 |
| `offboarding_offboardingstage` | 3 | `horilla_auth_horillauser`, `offboarding_offboarding` | 3 | 4 | 10 |
| `offboarding_offboardingstage_managers` | 4 | `employee_employee`, `offboarding_offboardingstage` | 5 | 0 | 0 |
| `offboarding_offboardingstagemultiplefile` | 1 | `horilla_auth_horillauser` | 1 | 2 | 2 |
| `offboarding_offboardingtask` | 4 | `horilla_auth_horillauser`, `offboarding_offboardingstage` | 4 | 2 | 2 |
| `offboarding_offboardingtask_managers` | 5 | `employee_employee`, `offboarding_offboardingtask` | 6 | 0 | 0 |
| `offboarding_resignationletter` | 5 | `employee_employee`, `horilla_auth_horillauser`, `offboarding_offboardingemployee` | 6 | 0 | 0 |
| `onboarding_candidatestage` | 6 | `horilla_auth_horillauser`, `onboarding_onboardingstage`, `recruitment_candidate` | 10 | 0 | 0 |
| `onboarding_candidatetask` | 6 | `horilla_auth_horillauser`, `onboarding_onboardingstage`, `onboarding_onboardingtask`, `recruitment_candidate` | 11 | 0 | 0 |
| `onboarding_historicalcandidatetask` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `onboarding_historicalcandidatetask_history_tags` | 2 | `horilla_audit_audittag`, `onboarding_historicalcandidatetask` | 3 | 0 | 0 |
| `onboarding_onboardingportal` | 6 | `horilla_auth_horillauser`, `recruitment_candidate` | 9 | 0 | 0 |
| `onboarding_onboardingstage` | 4 | `horilla_auth_horillauser`, `recruitment_recruitment` | 4 | 4 | 6 |
| `onboarding_onboardingstage_employee_id` | 5 | `employee_employee`, `onboarding_onboardingstage` | 6 | 0 | 0 |
| `onboarding_onboardingtask` | 5 | `horilla_auth_horillauser`, `onboarding_onboardingstage` | 5 | 3 | 3 |
| `onboarding_onboardingtask_candidates` | 6 | `onboarding_onboardingtask`, `recruitment_candidate` | 11 | 0 | 0 |
| `onboarding_onboardingtask_employee_id` | 6 | `employee_employee`, `onboarding_onboardingtask` | 7 | 0 | 0 |
| `payroll_allowance` | 3 | `base_company`, `base_employeeshift`, `base_worktype`, `horilla_auth_horillauser` | 5 | 7 | 11 |
| `payroll_allowance_apply_conditions` | 4 | `payroll_allowance`, `payroll_applycondition` | 7 | 0 | 0 |
| `payroll_allowance_exclude_employees` | 4 | `employee_employee`, `payroll_allowance` | 7 | 0 | 0 |
| `payroll_allowance_other_conditions` | 4 | `payroll_allowance`, `payroll_multiplecondition` | 7 | 0 | 0 |
| `payroll_allowance_specific_employees` | 4 | `employee_employee`, `payroll_allowance` | 7 | 0 | 0 |
| `payroll_applycondition` | 0 | — | 0 | 2 | 2 |
| `payroll_contract` | 4 | `base_department`, `base_employeeshift`, `base_jobposition`, `base_jobrole`, `base_worktype`, `employee_employee`, `horilla_auth_horillauser`, `payroll_filingstatus`, `payroll_salarystructure` | 11 | 0 | 0 |
| `payroll_deduction` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 7 | 7 |
| `payroll_deduction_apply_conditions` | 3 | `payroll_applycondition`, `payroll_deduction` | 4 | 0 | 0 |
| `payroll_deduction_exclude_employees` | 3 | `employee_employee`, `payroll_deduction` | 4 | 0 | 0 |
| `payroll_deduction_other_conditions` | 3 | `payroll_deduction`, `payroll_multiplecondition` | 4 | 0 | 0 |
| `payroll_deduction_specific_employees` | 3 | `employee_employee`, `payroll_deduction` | 4 | 0 | 0 |
| `payroll_encashmentgeneralsettings` | 0 | — | 0 | 4 | 4 |
| `payroll_encashmentgeneralsettings_department` | 2 | `base_department`, `payroll_encashmentgeneralsettings` | 3 | 0 | 0 |
| `payroll_encashmentgeneralsettings_employees` | 2 | `employee_employee`, `payroll_encashmentgeneralsettings` | 3 | 0 | 0 |
| `payroll_encashmentgeneralsettings_filtered_employees` | 2 | `employee_employee`, `payroll_encashmentgeneralsettings` | 3 | 0 | 0 |
| `payroll_encashmentgeneralsettings_job_position` | 3 | `base_jobposition`, `payroll_encashmentgeneralsettings` | 4 | 0 | 0 |
| `payroll_filingstatus` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 2 | 2 |
| `payroll_historicalcontract` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `payroll_historicalcontract_history_tags` | 2 | `horilla_audit_audittag`, `payroll_historicalcontract` | 3 | 0 | 0 |
| `payroll_historicalpayslip` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `payroll_historicalpayslip_history_tags` | 2 | `horilla_audit_audittag`, `payroll_historicalpayslip` | 3 | 0 | 0 |
| `payroll_loanaccount` | 4 | `asset_asset`, `employee_employee`, `horilla_auth_horillauser`, `payroll_allowance` | 10 | 1 | 1 |
| `payroll_loanaccount_deduction_ids` | 5 | `payroll_deduction`, `payroll_loanaccount` | 12 | 0 | 0 |
| `payroll_multiplecondition` | 0 | — | 0 | 2 | 2 |
| `payroll_overrideleaverequest` | 4 | `leave_leaverequest` | 5 | 0 | 0 |
| `payroll_payperiodsettings` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `payroll_payrollbatch` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 2 | 3 |
| `payroll_payrollbatchline` | 4 | `employee_employee`, `horilla_auth_horillauser`, `payroll_payrollbatch`, `payroll_payslip` | 5 | 0 | 0 |
| `payroll_payrollgeneralsetting` | 2 | `base_company` | 2 | 0 | 0 |
| `payroll_payrollsettings` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `payroll_payslip` | 3 | `employee_employee`, `horilla_auth_horillauser`, `payroll_payrollbatch` | 4 | 2 | 2 |
| `payroll_payslip_installment_ids` | 4 | `payroll_deduction`, `payroll_payslip` | 6 | 0 | 0 |
| `payroll_payslipautogenerate` | 2 | `base_company` | 2 | 0 | 0 |
| `payroll_reimbursement` | 4 | `employee_employee`, `horilla_auth_horillauser`, `leave_leavetype`, `payroll_allowance` | 8 | 2 | 3 |
| `payroll_reimbursement_other_attachments` | 5 | `payroll_reimbursement`, `payroll_reimbursementmultipleattachment` | 10 | 0 | 0 |
| `payroll_reimbursementfile` | 0 | — | 0 | 1 | 1 |
| `payroll_reimbursementmultipleattachment` | 0 | — | 0 | 1 | 1 |
| `payroll_reimbursementrequestcomment` | 5 | `employee_employee`, `horilla_auth_horillauser`, `payroll_reimbursement` | 9 | 1 | 1 |
| `payroll_reimbursementrequestcomment_files` | 6 | `payroll_reimbursementfile`, `payroll_reimbursementrequestcomment` | 11 | 0 | 0 |
| `payroll_salarystructure` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 3 | 3 |
| `payroll_salarystructure_allowances` | 4 | `payroll_allowance`, `payroll_salarystructure` | 7 | 0 | 0 |
| `payroll_salarystructure_deductions` | 3 | `payroll_deduction`, `payroll_salarystructure` | 4 | 0 | 0 |
| `payroll_taxbracket` | 3 | `horilla_auth_horillauser`, `payroll_filingstatus` | 3 | 0 | 0 |
| `payroll_workrecord` | 2 | `employee_employee` | 2 | 0 | 0 |
| `pms_anonymousfeedback` | 3 | `base_department`, `base_jobposition`, `employee_employee` | 4 | 0 | 0 |
| `pms_answer` | 3 | `employee_employee`, `pms_feedback`, `pms_question` | 5 | 0 | 0 |
| `pms_bonuspointsetting` | 2 | `base_company` | 2 | 0 | 0 |
| `pms_comment` | 4 | `employee_employee`, `pms_employeeobjective` | 5 | 0 | 0 |
| `pms_employeebonuspoint` | 3 | `employee_bonuspoint`, `employee_employee`, `horilla_auth_horillauser` | 3 | 0 | 0 |
| `pms_employeekeyresult` | 4 | `pms_employeeobjective`, `pms_keyresult` | 6 | 2 | 2 |
| `pms_employeeobjective` | 3 | `employee_employee`, `horilla_auth_horillauser`, `pms_objective` | 4 | 3 | 5 |
| `pms_employeeobjective_key_result_id` | 4 | `pms_employeeobjective`, `pms_keyresult` | 6 | 0 | 0 |
| `pms_feedback` | 2 | `employee_employee`, `horilla_auth_horillauser`, `pms_questiontemplate` | 3 | 6 | 6 |
| `pms_feedback_colleague_id` | 3 | `employee_employee`, `pms_feedback` | 4 | 0 | 0 |
| `pms_feedback_employee_key_results_id` | 5 | `pms_employeekeyresult`, `pms_feedback` | 9 | 0 | 0 |
| `pms_feedback_others_id` | 3 | `employee_employee`, `pms_feedback` | 4 | 0 | 0 |
| `pms_feedback_subordinate_id` | 3 | `employee_employee`, `pms_feedback` | 4 | 0 | 0 |
| `pms_historicalcomment` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `pms_historicalcomment_history_tags` | 2 | `horilla_audit_audittag`, `pms_historicalcomment` | 3 | 0 | 0 |
| `pms_historicalemployeekeyresult` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `pms_historicalemployeekeyresult_history_tags` | 2 | `horilla_audit_audittag`, `pms_historicalemployeekeyresult` | 3 | 0 | 0 |
| `pms_historicalemployeeobjective` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `pms_historicalemployeeobjective_history_tags` | 2 | `horilla_audit_audittag`, `pms_historicalemployeeobjective` | 3 | 0 | 0 |
| `pms_historicalkeyresult` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `pms_historicalkeyresult_history_tags` | 2 | `horilla_audit_audittag`, `pms_historicalkeyresult` | 3 | 0 | 0 |
| `pms_historicalobjective` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `pms_historicalobjective_history_tags` | 2 | `horilla_audit_audittag`, `pms_historicalobjective` | 3 | 0 | 0 |
| `pms_keyresult` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 3 | 5 |
| `pms_keyresultfeedback` | 5 | `employee_employee`, `pms_employeekeyresult`, `pms_feedback` | 9 | 0 | 0 |
| `pms_meetings` | 2 | `base_company`, `horilla_auth_horillauser`, `pms_questiontemplate` | 3 | 5 | 5 |
| `pms_meetings_answer_employees` | 3 | `employee_employee`, `pms_meetings` | 5 | 0 | 0 |
| `pms_meetings_employee_id` | 3 | `employee_employee`, `pms_meetings` | 5 | 0 | 0 |
| `pms_meetings_manager` | 3 | `employee_employee`, `pms_meetings` | 5 | 0 | 0 |
| `pms_meetingsanswer` | 3 | `employee_employee`, `pms_meetings`, `pms_question` | 6 | 0 | 0 |
| `pms_objective` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 4 | 9 |
| `pms_objective_assignees` | 3 | `employee_employee`, `pms_objective` | 4 | 0 | 0 |
| `pms_objective_key_result_id` | 3 | `pms_keyresult`, `pms_objective` | 4 | 0 | 0 |
| `pms_objective_managers` | 3 | `employee_employee`, `pms_objective` | 4 | 0 | 0 |
| `pms_period` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `pms_period_company_id` | 2 | `base_company`, `pms_period` | 3 | 0 | 0 |
| `pms_question` | 2 | `horilla_auth_horillauser`, `pms_questiontemplate` | 2 | 3 | 3 |
| `pms_questionoptions` | 3 | `horilla_auth_horillauser`, `pms_question` | 3 | 0 | 0 |
| `pms_questiontemplate` | 1 | `horilla_auth_horillauser` | 1 | 4 | 16 |
| `pms_questiontemplate_company_id` | 2 | `base_company`, `pms_questiontemplate` | 3 | 0 | 0 |
| `project_project` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 4 | 6 |
| `project_project_managers` | 3 | `employee_employee`, `project_project` | 4 | 0 | 0 |
| `project_projectstage` | 3 | `horilla_auth_horillauser`, `project_project` | 3 | 1 | 4 |
| `project_task` | 4 | `horilla_auth_horillauser`, `project_project`, `project_projectstage` | 4 | 3 | 3 |
| `project_task_task_managers` | 5 | `employee_employee`, `project_task` | 6 | 0 | 0 |
| `project_task_task_members` | 5 | `employee_employee`, `project_task` | 6 | 0 | 0 |
| `project_timesheet` | 5 | `employee_employee`, `horilla_auth_horillauser`, `project_project`, `project_task` | 6 | 0 | 0 |
| `recruitment_candidate` | 5 | `base_jobposition`, `employee_employee`, `horilla_auth_horillauser`, `recruitment_recruitment`, `recruitment_stage` | 8 | 12 | 16 |
| `recruitment_candidatedocument` | 6 | `horilla_auth_horillauser`, `recruitment_candidate`, `recruitment_candidatedocumentrequest` | 10 | 0 | 0 |
| `recruitment_candidatedocumentrequest` | 1 | `horilla_auth_horillauser` | 1 | 2 | 2 |
| `recruitment_candidatedocumentrequest_candidate_id` | 6 | `recruitment_candidate`, `recruitment_candidatedocumentrequest` | 10 | 0 | 0 |
| `recruitment_candidaterating` | 6 | `employee_employee`, `horilla_auth_horillauser`, `recruitment_candidate` | 9 | 0 | 0 |
| `recruitment_historicalcandidate` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `recruitment_historicalcandidate_history_tags` | 2 | `horilla_audit_audittag`, `recruitment_historicalcandidate` | 3 | 0 | 0 |
| `recruitment_historicalrejectedcandidate` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `recruitment_historicalrejectedcandidate_history_tags` | 2 | `horilla_audit_audittag`, `recruitment_historicalrejectedcandidate` | 3 | 0 | 0 |
| `recruitment_historicalstage` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `recruitment_historicalstage_history_tags` | 2 | `horilla_audit_audittag`, `recruitment_historicalstage` | 3 | 0 | 0 |
| `recruitment_interviewschedule` | 6 | `horilla_auth_horillauser`, `recruitment_candidate` | 9 | 2 | 2 |
| `recruitment_interviewschedule_employee_id` | 7 | `employee_employee`, `recruitment_interviewschedule` | 10 | 0 | 0 |
| `recruitment_linkedinaccount` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 1 | 30 |
| `recruitment_questionordering` | 4 | `horilla_auth_horillauser`, `recruitment_recruitment`, `recruitment_recruitmentsurvey` | 5 | 0 | 0 |
| `recruitment_recruitment` | 3 | `base_company`, `horilla_auth_horillauser`, `recruitment_linkedinaccount` | 3 | 10 | 29 |
| `recruitment_recruitment_open_positions` | 4 | `base_jobposition`, `recruitment_recruitment` | 6 | 0 | 0 |
| `recruitment_recruitment_recruitment_managers` | 4 | `employee_employee`, `recruitment_recruitment` | 5 | 0 | 0 |
| `recruitment_recruitment_skills` | 4 | `recruitment_recruitment`, `recruitment_skill` | 5 | 0 | 0 |
| `recruitment_recruitment_survey_templates` | 4 | `recruitment_recruitment`, `recruitment_surveytemplate` | 5 | 0 | 0 |
| `recruitment_recruitmentgeneralsetting` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `recruitment_recruitmentsurvey` | 1 | `horilla_auth_horillauser` | 1 | 3 | 3 |
| `recruitment_recruitmentsurvey_job_position_ids` | 3 | `base_jobposition`, `recruitment_recruitmentsurvey` | 4 | 0 | 0 |
| `recruitment_recruitmentsurvey_template_id` | 3 | `recruitment_recruitmentsurvey`, `recruitment_surveytemplate` | 4 | 0 | 0 |
| `recruitment_recruitmentsurveyanswer` | 6 | `base_jobposition`, `horilla_auth_horillauser`, `recruitment_candidate`, `recruitment_recruitment` | 9 | 0 | 0 |
| `recruitment_rejectedcandidate` | 6 | `horilla_auth_horillauser`, `recruitment_candidate` | 9 | 1 | 1 |
| `recruitment_rejectedcandidate_reject_reason_id` | 7 | `recruitment_rejectedcandidate`, `recruitment_rejectreason` | 11 | 0 | 0 |
| `recruitment_rejectreason` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 1 | 1 |
| `recruitment_resume` | 4 | `recruitment_recruitment` | 4 | 0 | 0 |
| `recruitment_skill` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `recruitment_skillzone` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 1 | 1 |
| `recruitment_skillzonecandidate` | 6 | `horilla_auth_horillauser`, `recruitment_candidate`, `recruitment_skillzone` | 10 | 0 | 0 |
| `recruitment_stage` | 4 | `horilla_auth_horillauser`, `recruitment_recruitment` | 4 | 3 | 18 |
| `recruitment_stage_stage_managers` | 5 | `employee_employee`, `recruitment_stage` | 6 | 0 | 0 |
| `recruitment_stagefiles` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `recruitment_stagenote` | 6 | `employee_employee`, `horilla_auth_horillauser`, `recruitment_candidate`, `recruitment_stage` | 9 | 1 | 1 |
| `recruitment_stagenote_stage_files` | 7 | `recruitment_stagefiles`, `recruitment_stagenote` | 11 | 0 | 0 |
| `recruitment_surveytemplate` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 2 | 2 |
| `report_reportaccess` | 2 | `auth_group`, `base_company`, `horilla_auth_horillauser` | 3 | 0 | 0 |
| `report_reportfavorite` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `report_reportfilterpreset` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `report_reportrunlog` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `report_reportsavedview` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `report_reportsubscription` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 1 | 1 |
| `report_reportsubscription_recipients_employees` | 3 | `employee_employee`, `report_reportsubscription` | 4 | 0 | 0 |
| `report_reporttemplate` | 2 | `base_company`, `horilla_auth_horillauser` | 2 | 0 | 0 |
| `token_blacklist_blacklistedtoken` | 2 | `token_blacklist_outstandingtoken` | 2 | 0 | 0 |
| `token_blacklist_outstandingtoken` | 1 | `horilla_auth_horillauser` | 1 | 1 | 1 |
| `whatsapp_whatsappcredientials` | 1 | `horilla_auth_horillauser` | 1 | 2 | 2 |
| `whatsapp_whatsappcredientials_company_id` | 2 | `base_company`, `whatsapp_whatsappcredientials` | 3 | 0 | 0 |
| `whatsapp_whatsappflowdetails` | 2 | `whatsapp_whatsappcredientials` | 2 | 0 | 0 |

### Most depended-on tables (by descendants)

- `horilla_auth_horillauser` — 389 descendants, 222 direct
- `base_company` — 206 descendants, 83 direct
- `employee_employee` — 151 descendants, 108 direct
- `base_department` — 45 descendants, 14 direct
- `attendance_gracetime` — 34 descendants, 2 direct
- `base_employeeshift` — 32 descendants, 12 direct
- `base_jobposition` — 31 descendants, 14 direct
- `recruitment_linkedinaccount` — 30 descendants, 1 direct
- `recruitment_recruitment` — 29 descendants, 10 direct
- `base_worktype` — 28 descendants, 8 direct
- `horilla_audit_audittag` — 26 descendants, 26 direct
- `leave_leavetype` — 23 descendants, 9 direct
- `recruitment_stage` — 18 descendants, 3 direct
- `pms_questiontemplate` — 16 descendants, 4 direct
- `recruitment_candidate` — 16 descendants, 12 direct
- `asset_assetcategory` — 14 descendants, 3 direct
- `asset_assetlot` — 12 descendants, 2 direct
- `offboarding_offboarding` — 12 descendants, 2 direct
- `base_employeeshiftday` — 11 descendants, 4 direct
- `payroll_allowance` — 11 descendants, 7 direct

