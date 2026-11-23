# Automations and notifications

## Summary

This area tells people about events. It offers no-code mail automations that send an e-mail or an in-app notice when a record is created, changed or deleted, an in-app notification inbox, and a WhatsApp Business connection through which employees can also raise requests. Many automatic messages are sent in the name of a system user called "Horilla Bot".

## Who uses it

- HR and admins set up mail automations, mail templates and the WhatsApp connection.
- Employees and managers receive notifications, and employees can raise requests through WhatsApp.

## Features

### Mail automations

- HR picks a kind of record (for example leave requests), a trigger (when it is created, changed or deleted), conditions, who receives the message (found through links on the record, for example "the employee's reporting manager"), a mail template, and whether to send an e-mail, an in-app notification or both.

### In-app notifications

- Every user has a notification inbox, with an optional sound for new notices.

### Notices sent by the system

- Many automatic notices, for example about shift and work-type changes made by background jobs, are sent in the name of a user called "Horilla Bot".

> Flag (risk): if no user named exactly "Horilla Bot" exists, those notices are skipped without any warning (`base/scheduler.py`). Business effect: employees are not told that their shift or work type changed, and nobody knows the notices are missing.

### WhatsApp Business

- The system connects to WhatsApp Business (Meta) with message templates and interactive flows.
- Through WhatsApp, employees can ask for a shift change, a work-type change, leave, an asset, an attendance correction, a bonus point cash-in or a reimbursement.
- Notifications and announcements can go out on WhatsApp.
- Incoming WhatsApp messages are checked for a valid signature from Meta before they are accepted.
- Rule: WhatsApp requests are passed through the same web forms and screens as requests made on the web, so the web's checks apply. Reason: not stated in the code.

> Flag (risk): WhatsApp attendance requests call an older attendance request screen that is no longer reachable on the web, but still exists in the code (`whatsapp/utils.py`, `attendance/urls.py`). Business effect: improvements or fixes to the web's attendance request rules may not reach requests made through WhatsApp, so the two channels can behave differently.

## Who can do what

| Action | Who |
|---|---|
| Set up mail automations | People with the mail automation permissions (Admin) |
| Set up the WhatsApp connection | People with the WhatsApp credential permissions (Admin) |
| Raise requests through WhatsApp | Employees, for themselves, when the WhatsApp connection is switched on |
| Receive notifications | Every user |

These come from the permission checks on the automation and WhatsApp screens (`horilla_automations/views/`, `whatsapp/views.py`).

## Recommendations

- Suggestion: create the "Horilla Bot" user automatically, or send system notices without depending on it.
- Suggestion: route WhatsApp attendance requests through the same screen the web uses today.
- Suggestion: show HR a log of automation messages that were sent or failed.

## Related documents

- [Holidays and announcements](04-holidays-and-announcements.md): announcements sent on WhatsApp.
- [Organisation and company setup](01-organisation-and-company-setup.md): mail servers and mail templates.
- [Horilla HRM feature reference](../Horilla_HRM_FEATURES.md)

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
