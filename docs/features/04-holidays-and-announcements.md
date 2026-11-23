# Holidays and announcements

## Summary

This area records the days the company does not work: public holidays and regular weekly days off. It also lets HR send announcements to chosen groups of employees. Holidays and days off feed into attendance (minimum hours and overtime) and leave (how many days a request uses).

## Who uses it

- HR sets up holidays and weekly days off and writes announcements.
- Employees see holidays and read announcements, and can comment on them.

## Features

### Public holidays

- A holiday is a single day or a range of days. It can apply to everyone or only to chosen employees, departments or job positions.
- A holiday can be marked as recurring. Holidays can be imported from and exported to a spreadsheet.
- Rule: the day after a recurring holiday ends, it is moved to the same dates next year. Reason: recurring holidays should not need to be entered again every year.

> Flag (risk): if moving a recurring holiday to next year would clash with a holiday that already exists, the move is skipped and only a technical log line is written (`base/scheduler.py`). Business effect: the holiday quietly disappears from next year's calendar, and nobody in HR is told.

### Weekly days off (company leaves)

- HR sets regular days off, such as "every Sunday" or "the second Saturday of the month".

### How holidays and days off affect other areas

- Rule: on a holiday or weekly day off, the day's minimum working hours become zero in attendance, so any hours worked count as **overtime**. Reason: not stated in the code.
- Rule: a leave type can be set to leave holidays and weekly days off out of the number of days a request uses. See [Leave](06-leave.md).

### Announcements

- HR writes announcements for chosen employees, departments or job positions, with attachments.
- Employees can comment, and the system records who has viewed each announcement.
- Announcements expire after a set time (a company preference), and can also be sent by WhatsApp; see [Automations and notifications](17-automations-and-notifications.md).

## Who can do what

| Action | Who |
|---|---|
| Create, change and delete holidays and weekly days off | People with the holiday or company-leave permissions (Admin, HR Manager) |
| Write, change and delete announcements | People with the announcement permissions |
| Read announcements and comment | The employees each announcement is aimed at |

These come from the permission checks on the holiday and announcement screens (`base/views.py`).

## Recommendations

- Suggestion: when a recurring holiday cannot be moved to next year, tell HR on screen or by notification instead of only writing a log line.
- Suggestion: show HR, before saving, how a new holiday changes leave day counts and overtime.

## Related documents

- [Attendance](05-attendance.md): minimum hours and overtime on holidays.
- [Leave](06-leave.md): leaving holidays out of leave day counts.

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
