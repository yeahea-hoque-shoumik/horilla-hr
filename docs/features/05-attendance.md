# Attendance

## Summary

This area records when employees work. It takes check-ins and check-outs from the web, the mobile app, biometric devices, spreadsheets and automatic check-out, and turns them into a daily attendance record with worked hours, minimum hours and overtime. Managers validate attendance and approve overtime, and lateness and early departures can lead to penalties. At month end, a monthly summary classifies every day and feeds paid and unpaid days to payroll.

## Who uses it

- Employees check in and out, take breaks, and ask for attendance to be added or corrected.
- Reporting managers validate their team's attendance, approve overtime and decide on requests.
- HR and attendance managers set the rules (grace time, validation conditions, restrictions), resolve month-end conflicts and prepare the monthly summary for payroll.
- Biometric devices and the mobile app send punches in.

## Features

### Checking in and out

- Employees check in and out from the top of the screen, from the mobile app, through biometric devices, through a spreadsheet import, or by automatic check-out.
- A day can have several in-and-out pairs ("activities"), breaks, and a running "at work" timer.
- Web and mobile check-ins and check-outs use the employee's own **time zone** (see [How the system works overall](00-how-the-system-works.md)).
- Rule: a **night shift** (one that starts later in the day than it ends) runs from noon to noon. A check-in before 12:00 on a night shift belongs to the previous day's attendance. Reason (from a code comment): the system treats a night shift as a 24-hour period from noon to the next day's noon (`attendance/views/clock_in_out.py`).

### Restrictions on where and how people check in

- Per company, HR can switch check-in on or off, limit check-in to a list of office network addresses, limit check-in to a radius around the office (**geofence**, on the web and in the mobile app), and require a face image check in the mobile app.
- Rule: the geofence is also enforced on the web. Reason (from a code comment): the mobile app already enforced it, and without the web check an employee outside the area could still check in from a browser.
- Rule: the office network check trusts only as many forwarding servers as the setup declares. Reason (from a code comment): trusting the address the browser claims let anyone pretend to be on the office network.

> Flag (risk): the office network restriction and the login lockout both need the real address of the person's computer. This fork removed the web server gatekeeper and serves the system through a tunnel, so the setting that says how many forwarding servers sit in front of the system (`AXES_PROXY_COUNT`) must be correct. Business effect: if it is wrong, every user appears to come from the same address, so the network restriction either blocks everyone or lets everyone in, and one person's failed logins can lock others out. (`horilla/settings/base.py`, `docker-compose.prod.yml`)

> Flag (risk): face matching is not done by this system. The server only stores one reference face image per employee; no code in this repository compares faces, so the comparison is done, or simply trusted, inside the mobile app. Employees upload their own reference image and can replace it at any time. Business effect: the face check proves less than it appears to, and an employee could set someone else's photo as their reference. (`facedetection/views.py`)

### The daily attendance record

- Each day's record holds the shift, work from, first check-in, last check-out, worked hours, minimum hours, **overtime** and whether it has been validated.
- Rule: overtime for a day is worked hours minus minimum hours, and never below zero. Reason: not stated in the code.
- Rule: on a holiday or weekly day off the minimum is zero, so the whole day counts as overtime. Reason: not stated in the code.
- Rule: a check-in date cannot be before the attendance date, and a check-out cannot be before the check-in or in the future. Reason: not stated in the code.

### Validation

- Managers validate attendance records. A record can be validated automatically when its hours fall inside limits HR sets (validation conditions).
- Rule: people who are not **superusers** cannot validate their own attendance. Reason: not stated in the code.

### Overtime and the hours balance

- Each employee has a monthly **hours balance**: hours worked against hours required.
- Rule: the hours balance counts only validated days, leaves out days covered by approved leave (or leave whose cancellation is pending), and caps each day's worked time at that day's minimum. Reason: the balance measures whether the required hours were met; extra hours are tracked separately as overtime.
- Rule: overtime is capped at the validation condition's cut-off, and approved automatically when the condition allows it and the overtime reaches the condition's minimum. The condition used is the shift's own, or else the default one. Reason: not stated in the code.
- Managers approve overtime one record at a time or many at once. People who are not superusers cannot approve their own overtime. Reason: not stated in the code.

### Grace time, late arrival and early departure

- A grace time can be set on a shift, or a default one for everyone, for check-in and optionally for check-out. A shift's own grace time wins over the default.
- Rule: when late and early tracking is switched on, a check-in later than the shift start plus the grace time is recorded as a late arrival, and a check-out earlier than the shift end minus the grace time is recorded as an early departure. Reason: not stated in the code.
- A late arrival or early departure can carry a **penalty**: a fine, which becomes a one-time deduction in payroll (see [Payroll](07-payroll.md)), or a cut in leave days (see [Leave](06-leave.md)).

> Flag (bug), described in [Leave](06-leave.md): deleting a penalty can give back more leave than it took.

### Attendance requests

- Employees ask for a missing attendance to be added, or for an existing one to be corrected, with comments and files. They can also ask for a range of dates at once (bulk request) or group requests into batches.

> Flag (bug): an attendance that an employee asked to add is not deleted when it is rejected. It stays in the system as an unvalidated attendance (`attendance/views/requests.py`). Business effect: rejected days still appear in attendance lists and can be validated later by mistake.

> Flag (bug): a bulk attendance request with one invalid day crashes part-way (`attendance/forms.py`). Business effect: some days of the request are saved and others are not, and the employee sees an error instead of a clear message.

### Spreadsheet import

- HR can import attendance from an Excel sheet. Rows with errors are returned in an error sheet.
- Rule: the import refuses dates of today or later, and attendance that already exists for that employee and date. Reason: not stated in the code.

> Flag (risk): the Excel import writes the rows straight into the database in one go, which skips the normal save steps (`attendance/views/process_attendance_data.py`). Checked in the code: imported days get no overtime calculation, no zero minimum on holidays, no automatic overtime approval and no daily work status, and the month's hours balance is not updated at the time of import. Business effect: imported attendance can show no overtime and no daily status, so overtime pay and the daily status grid are wrong for those days until each record is saved again.

### Daily Work Status

- A grid shows each employee's status for each day: Present, Half Day, Absent, Holiday or Week-off, Conflict, or Draft.
- Rule: after each attendance save, a record that is not validated shows as Conflict ("Validate the attendance"); worked hours at or above the minimum give Present; at least half the minimum gives Half Day; less gives Absent; no check-out yet shows "Currently working". Reason: not stated in the code.
- Rule: every 30 minutes (and at 00:30) a draft status row is created for every employee who has a shift and no row yet for today. Reason: not stated in the code.

### Automatic check-out

- Rule: every 5 minutes, for shifts with automatic check-out switched on, open check-ins are closed at the set time (the next day for night shifts). Reason: not stated in the code.

> Flag (gap), described in [How the system works overall](00-how-the-system-works.md): automatic check-out and the daily status use the server's clock, not the company or employee time zone.

### Monthly summary for payroll

- At month end, the monthly summary classifies each day for each employee and is what payroll reads for paid and unpaid days and overtime.
- HR can resolve a day by hand (for example "full present", "half day", "paid leave", "holiday"), override hours for one day or a range, override a whole month's totals, and import corrections.
- Rule, checked in the code (`attendance/views/summary.py`):
  - worked hours at or above the minimum minus the default grace time count as 1 day; at least half of that counts as half a day; less counts as 0;
  - half a day that falls short is counted as absent;
  - a half-day leave covers its half, and the other half is present if attendance reaches it, otherwise absent;
  - attendance on a holiday or weekly day off counts as a holiday or week-off day (the hours go to overtime);
  - otherwise a day counts as attendance, then paid leave, unpaid leave, holiday, week-off, and finally absent;
  - an HR decision on a day always wins.
  Reason: not stated in the code.
- Rule: a day with both attendance and approved leave is a **conflict**. Payroll will not run for an employee with unresolved conflicts (see [Payroll](07-payroll.md)). A month-total override settles that employee's conflicts. Reason (from a code comment): once HR states the month's totals there is nothing left to decide about single days, and payroll would otherwise stay blocked on conflicts the override was written to answer.

### Biometric devices

- Supported devices: ZKTeco and eSSL, Anviz, Matrix COSEC, Dahua and e-Time Office. Each device is set as an "in", "out", "alternate" or system-direction device.
- Punches are captured live or collected every few seconds, and device users are matched to employees by badge number.

> Flag (risk): extra background pollers. Scheduling a biometric device from its screen starts an extra timer inside the web process, on top of the central job, so a device can be polled twice (`biometric/views.py`). The Google Drive backup also runs its own timer inside the web process, which is lost when the server restarts and can run more than once when the server runs several workers (`horilla_backup/scheduler.py`). Business effect: duplicate or missing punches from devices, and backups that silently stop after a restart or run twice.

### Dashboards

- Attendance dashboards show who is on time, late, left early, on a break, has pending hours, overtime by department, and who is absent.

### Things the comparison with Apurba HRM lists as missing

> Flag (gap): there is no automatic leave deduction for a shortfall in worked hours, no monthly limit on attendance correction requests, and no separate work-from-home request type (work-from requests can be used for it). Checked in the code: no such features exist. (Comparison document, sections 2.2 and 2.3)

## Who can do what

| Action | Who |
|---|---|
| Check in, check out, take breaks | Every employee with work information, when check-in is switched on for their company |
| Ask to add or correct attendance | Every employee, for themselves |
| Validate attendance and approve overtime | People with the attendance change permission, and anyone who is the reporting manager of at least one employee (see the manager access flag in [How the system works overall](00-how-the-system-works.md)); never for their own records unless they are a superuser |
| Set grace times, validation conditions, late and early tracking, network restrictions | People with the matching attendance or base permissions (Admin, HR Manager, Attendance Manager) |
| Set up biometric devices | People with the biometric device permissions |
| Set up the geofence and face check from the mobile app | People with the geofence or face detection permissions |
| Open the face check and geofence set-up pages on the web | In practice only superusers: these pages ask for a permission name that does not exist in the system (`geofencing.add_localbackup`), so no role can be given it (`facedetection/views.py`, `geofencing/views.py`) |
| Resolve conflicts and override the monthly summary | People allowed into the monthly summary screens (the wide manager check applies) |

These come from the permission checks on the attendance screens (`attendance/views/`).

## Recommendations

- Suggestion: make the Excel import save each row through the normal steps, so overtime, the hours balance and the daily status are always right.
- Suggestion: delete, or clearly mark, attendance whose add request was rejected.
- Suggestion: check on every manager screen that the record belongs to the manager's own team.
- Suggestion: do face matching on the server, or at least stop employees replacing their own reference image without HR approval.
- Suggestion: run device polling only from the central scheduler.
- Suggestion: fix the permission name on the web face check and geofence set-up pages so HR roles can use them.

## Related documents

- [Attendance module notes](../../attendance/MODULE_SUMMARY.md): the fork's detailed technical notes on this area.
- [How the system works overall](00-how-the-system-works.md): time zones, background jobs and manager access.
- [Leave](06-leave.md) and [Payroll](07-payroll.md): how attendance feeds them.
- [Apurba HRM v2 compared with Horilla](<../ApurbApurba_HRM-v2_vs_Horilla_HRMS—Feature_Comparison.md>)

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
