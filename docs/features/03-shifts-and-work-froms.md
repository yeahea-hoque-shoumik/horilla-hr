# Shifts and work from options

## Summary

This area decides when and how each employee works: their shift (working hours per weekday) and their work from (for example office or remote). Shifts and work from options can rotate automatically, be set day by day in a roster, or be changed through a request that a manager approves. Attendance uses the shift to work out lateness, overtime and minimum hours.

## Who uses it

- HR sets up shifts, work from options, rotations and rosters.
- Employees ask for a shift or work-from change and see their own roster.
- Reporting managers approve, reject or cancel their team's change requests.

## Features

### Shifts

- A shift has a schedule for each weekday: start time, end time, minimum working hours, a night-shift mark, an automatic check-out time and a **grace time** (how late someone can arrive without being counted late).

### Rotating shifts and rotating work from options

- An employee can be given two or more shifts or work from options that take turns. The switch happens after a set number of days, every week on a chosen day, or every month on a chosen date or the last day of the month.
- Rule: a rotation cannot start in the past, and an employee can have only one active rotation. Reason: not stated in the code.
- Rule: a rotation cannot list the same shift or work from twice in a row. Reason: not stated in the code.
- Rule: starting a new rotation switches off the employee's older rotations. Reason: not stated in the code.

> Flag (bug): monthly rotations crash in December. The job adds one to the month number and there is no thirteenth month (`base/scheduler.py`). Business effect: every monthly rotation stops working at the end of the year until someone fixes it by hand.

> Flag (risk): rotations and approved requests take effect only if the 4-hourly **background job** runs on the exact change date. A day on which the **scheduler** was down is never caught up. Business effect: an employee can stay on the wrong shift or work from after a server outage until someone notices.

### Shift requests and work-from requests

- An employee asks for a different shift or work from, either for a period with an end date or permanently, and can add comments and files.
- Managers approve, reject or cancel requests, one at a time or many at once.
- Rule: a request cannot start in the past ("Date must be greater than or equal to today"). Reason: not stated in the code.
- Rule: on the requested start date, an approved request switches the employee to the new shift or work from. After the end date it switches them back. The employee is notified. These checks run every 4 hours. Reason: not stated in the code.

### Roster

- A roster sets one shift (or a day off) for one employee on one date. Rosters are published, and each publication is logged. Employees see "My Roster".
- Rule: a published roster entry for today that is not a day off replaces the employee's shift. Reason: not stated in the code.

> Flag (risk): a roster change is never reverted. After the rostered day the employee keeps the rostered shift until something else changes it. The job's own note says it runs "daily at 00:05", but it runs every 4 hours (`base/scheduler.py`). Business effect: one rostered day can silently change an employee's shift for the following weeks, which then affects lateness, overtime and pay.

> Flag (gap): two employees cannot swap shifts with each other. *Not yet verified in the code.* (Comparison document, section 2.1)

## Who can do what

| Action | Who |
|---|---|
| Set up shifts, schedules, work from options and rotations | People with the shift, schedule, work from or rotation permissions (Admin, HR Manager, Attendance Manager) |
| Ask for a shift or work-from change | Every employee, for themselves |
| Approve, reject or cancel requests | People with the request change permission, and reporting managers (the wide manager check described in [How the system works overall](00-how-the-system-works.md)) |
| Publish rosters | People with the shift permissions. *Not yet verified in the code.* |

These come from the permission checks on the shift and request screens (`base/views.py`).

## Recommendations

- Suggestion: fix the December rollover so monthly rotations keep working into the new year.
- Suggestion: let rotation and request jobs catch up any change date that was missed while the scheduler was down.
- Suggestion: make rostered shifts apply only to the rostered day and then return to the normal shift.
- Suggestion: consider a shift swap request between two employees.

## Related documents

- [How the system works overall](00-how-the-system-works.md): background jobs and time zones.
- [Attendance](05-attendance.md): how shifts are used for lateness and overtime.
- [Apurba HRM v2 compared with Horilla](<../ApurbApurba_HRM-v2_vs_Horilla_HRMS—Feature_Comparison.md>)

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
