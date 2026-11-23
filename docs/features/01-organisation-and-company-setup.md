# Organisation and company setup

## Summary

This area holds the building blocks of the organisation: companies, departments, job positions, job roles, employee types, work types and tags. It also holds system-wide preferences, mail servers and mail templates, the export permission setting and the first-run setup wizard. Everything else in the system refers to these records, so they are usually set up first.

## Who uses it

- HR and admin roles set up and maintain the organisation and the preferences.
- The person installing the system uses the first-run setup wizard once.
- Employees see the results (their department, position and company) but do not change them.

## Features

### Companies

- A company has a name, address, logo, a "headquarters" mark, its own date and time format, and its own **time zone** (added by this fork; see [How the system works overall](00-how-the-system-works.md)).
- Rule: no two companies can have the same name and address together. Reason: not stated in the code.
- Rule: a company or employee time zone must be a real name from the international time zone list (for example "Asia/Dhaka"). Reason: not stated in the code.
- Rule: creating a company automatically creates its announcement-expiry setting, its export-permission setting and its attendance settings. Reason: not stated in the code.

### Departments, job positions, job roles, employee types, work types and tags

- These are simple lists that HR maintains. Employees are placed in a department and job position, and can have a job role, an employee type (for example permanent or contract), a work type (for example office or remote) and tags.
- Work types are also used by shift and work-type requests; see [Shifts and work types](03-shifts-and-work-types.md).

### First-run setup wizard

- When the system is first installed, a setup wizard creates the first company and administrator. It is protected by a setup password set in the server's settings (`DB_INIT_PASSWORD`). *Not yet verified in the code.*

> Flag (risk): the shipped default setup password is a publicly known value. The production start-up check refuses to start with the default secret key, open host settings or the default setup password (`horilla/settings/security.py`), but that check runs only in production mode. Business effect: a test or staging installation that can be reached from the internet and still uses the default setup password can be taken over through the setup wizard.

### System preferences

- Records shown per page, chosen per user.
- The prefix of employee badge numbers, "PEP" by default.
- The currency symbol and whether it is shown before or after amounts.
- Date and time formats, the languages offered per company, and how long announcements stay visible.

### Who may export data

- Each company chooses either that everyone may export lists, or that exporting a list needs a separate export permission for that kind of record (created automatically for each record type). Reason: not stated in the code.

### Mail servers and mail templates

- A company can have several outgoing mail servers, one of them marked as the main one.
- HR can write reusable mail templates.
- Every e-mail the system sends is recorded in an e-mail log.

### Setup checklist

- A banner lists the setup steps still to do. A user can dismiss it.

## Who can do what

| Action | Who |
|---|---|
| Create and change companies, departments, positions, roles, employee types, work types and tags | People with the matching add or change permission, such as the Admin and HR Manager **role groups** |
| Set up mail servers and mail templates | People with the mail server or mail template permissions |
| Change who may export data | People with the export-permission setting permission |
| Run the first-run setup wizard | Anyone who knows the setup password |
| See the organisation structure | Every signed-in employee |

These checks come from the permission names on each settings screen (`base/views.py`).

## Recommendations

- Suggestion: require the setup password to be changed on every installation, not only in production, or switch the setup wizard off once the first company exists.
- Suggestion: explain on the export-permission screen what each choice means for managers and employees.
- Suggestion: offer a time zone picker instead of typed names, so HR cannot enter a name that is then refused.

## Related documents

- [How the system works overall](00-how-the-system-works.md): companies, time zones and roles.
- [Security and access](21-security-and-access.md): the production start-up check.
- [Employee setup guide](../EMPLOYEE_SETUP_GUIDE.md): the fork's guide to setting up employees.

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
