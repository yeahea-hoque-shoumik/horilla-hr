# Employee documents

## Summary

This area lets HR collect documents from employees, such as a passport copy or a certificate. HR raises a document request for chosen employees, the employees upload the file, and HR approves or rejects it. Documents can have an expiry date, and the system is meant to warn before and mark them when they expire.

## Who uses it

- HR raises document requests and approves or rejects uploads.
- Employees upload the documents asked of them.

## Features

### Document requests and uploads

- HR raises a document request (for example "upload passport"), with the accepted file format, for selected employees.
- Each chosen employee gets a document to upload. HR approves or rejects each upload.
- A document can have an expiry date and a number of "notify before" days.

### Expiry warnings

- A check of document expiry dates runs every 4 hours. It lives in the asset area's job file (`asset/scheduler.py`), not in this area.

> Flag (bug): expired documents are marked inactive only in the computer's memory and never actually saved, so they stay active. The expiry notice also links to the asset page instead of the document. Because the check runs every 4 hours and only compares the exact day, the same notice can be sent several times on that day (`asset/scheduler.py`). Business effect: expired documents look valid in the system, employees and HR receive repeated notices that open the wrong page, and expired passports or permits can go unnoticed.

## Who can do what

| Action | Who |
|---|---|
| Raise document requests | People with the document request add permission (Admin, HR Manager) |
| Approve or reject uploads | People with the document request change permission |
| Upload a requested document | The employee it was asked of |
| See documents | People with the document view permission, and the employee for their own documents |

These come from the permission checks on the document screens, which live in the employee area (`employee/views.py`).

## Recommendations

- Suggestion: fix the expiry check so it saves the inactive state, links to the document, and sends each notice once.
- Suggestion: move the document expiry check into this area.

## Related documents

- [Assets](13-assets.md): where the expiry check currently runs.
- [Reports](16-reports.md): the document expiry ageing and contract and document expiry reports.

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
