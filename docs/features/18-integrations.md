# Integrations

## Summary

This area lists the outside services the system can connect to: Google Meet for interview and meeting links, Google Drive for backups, LinkedIn for job posts, cloud file storage and error tracking. Several integrations ship with the product but are switched off or not installed in this setup: LDAP login, Microsoft 365 mail, custom fields and a local database backup. Product owners should treat the switched-off ones as not available.

## Who uses it

- Administrators set up and switch on integrations.
- HR and recruiters use the results (Meet links, LinkedIn posts, backups).

## Features

### Integrations that are installed

| Integration | What it does | Status |
|---|---|---|
| Google Meet | Creates and deletes Meet links for interviews and meetings, using each person's own Google sign-in | Installed |
| Google Drive backup | Backs up the database and uploaded files to Google Drive | Installed; see the flag below |
| LinkedIn | Posts job openings to LinkedIn and removes them | Installed |
| Cloud file storage (AWS S3 or Google Cloud Storage) | Stores uploaded files in the cloud instead of on the server | Optional, chosen by server settings |
| Sentry error tracking | Sends technical errors to an error-tracking service | Optional, on when its address is set |

> Flag (risk), described in [Attendance](05-attendance.md) under biometric devices: the Google Drive backup runs its own timer inside the web process, so it is lost on restart and can run more than once.

### Integrations that are switched off or not installed

> Flag (switched off): these ship with the product but cannot be used in this setup. LDAP login and user sync: the login connection is commented out in the settings and the libraries it needs are not installed (`horilla/settings/base.py`). Microsoft 365 or Outlook mail: the app is not installed (`outlook_auth/`). Custom fields added at run time: not installed (`dynamic_fields/`). Local database backup on a schedule: not installed (`pg_backup/`). Business effect: customers who sign in with their company directory, send mail through Microsoft 365, or need extra fields on records cannot do so today, even though screens and code for these exist in the repository.

## Who can do what

| Action | Who |
|---|---|
| Set up Google Meet credentials | People with the Google cloud credential permissions (Admin) |
| Create Meet links | People with the meeting permission. *Not yet verified in the code.* |
| Set up backups | People with the backup permissions (Admin) |
| Connect a LinkedIn account | People with the LinkedIn account permissions (Admin, HR Manager, Recruiter) |

These come from the permission checks on the integration screens (`horilla_meet/views.py`, `horilla_backup/views.py`, `recruitment/views/`).

## Recommendations

- Suggestion: either finish and install LDAP and Microsoft 365 mail, or remove them from the product so they are not mistaken for features.
- Suggestion: run the Google Drive backup from the central scheduler, and alert someone when a backup fails.

## Related documents

- [Recruitment](08-recruitment.md): Meet links for interviews and LinkedIn posts.
- [Attendance](05-attendance.md): the extra background timers flag.
- [Horilla HRM feature reference](../Horilla_HRM_FEATURES.md)

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
