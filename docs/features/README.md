# Product Feature Report: what this HR system does today

## Purpose

This report describes, in plain English, everything this HR system does today: its feature areas, the features in each area, the business rules behind each feature, and the reason for each rule where the code gives one. It is written for product owners and business analysts preparing a product review, so they can decide what to change, keep or remove.

The report was written from the code itself. Existing documents in the `docs/` folder were used as pointers only and are linked where they add detail.

## Who should read it

This report is for people who have access to this code repository. It describes security weaknesses and unfinished parts of the system, so do not share it outside the team without review.

## Which version of the system it describes

The report describes the code at commit `f2ab49933cfb40d295b3a9e65eba21996df2b0dc`, scanned on 2026-11-19. The system is a fork (a company-owned copy) of the open-source product Horilla HRMS, version 2.2.0. Later code changes are not covered until a file's change log says so.

## How to read the report

- Start with [How the system works overall](00-how-the-system-works.md). It explains the ideas that every area depends on (companies, the employee record, approvals, notifications, background jobs, time zones, archiving and roles), so the area files do not repeat them.
- Each area file has the same sections in the same order: Summary, Who uses it, Features, Who can do what, Recommendations, Related documents and Change log.
- Every term written in **bold** is explained in the [glossary](glossary.md).
- When a rule's reason is written in the code, the report gives it. When the code gives no reason, the report says exactly "Reason: not stated in the code" and does not guess.
- A claim that was not checked in the code carries the note "*Not yet verified in the code.*". Every payroll, leave and attendance claim taken from an existing document was checked in the code before it was written.
- Recommendations are suggestions from the writer of this report. They describe possible changes, not what the system does today.

### Flags

A **flag** marks something a product owner should know about. Each flag sits next to the feature it affects, says its type in plain words and explains the effect on the business, not the code cause. The types are:

- **Bug**: the system does something different from what it plainly intends.
- **Gap**: something a product owner would expect is missing.
- **Half-built**: started or partly connected, but not finished.
- **Switched off**: shipped with the product but turned off or not installed.
- **Inconsistent**: the same rule behaves differently depending on the screen or channel used.
- **Risk**: works, but can give a wrong or surprising result in realistic conditions.

A flag that affects several areas is written in full once, in the file it affects most, and the other files link to it.

## The report files

| File | What it covers |
|---|---|
| [00 How the system works overall](00-how-the-system-works.md) | Ideas shared by every area, the code version, the changes made in this fork, and what is planned but not built |
| [01 Organisation and company setup](01-organisation-and-company-setup.md) | Companies, departments, job positions, system preferences, mail servers and the first-run setup |
| [02 Employees](02-employees.md) | The employee profile, work information, policies, disciplinary actions, bonus points and archiving |
| [03 Shifts and work types](03-shifts-and-work-types.md) | Shifts, work types, rotating schedules, rosters and change requests |
| [04 Holidays and announcements](04-holidays-and-announcements.md) | Public holidays, weekly days off and company announcements |
| [05 Attendance](05-attendance.md) | Check-in and check-out, overtime, late arrival, biometric devices, location and face checks, and the monthly summary used by payroll |
| [06 Leave](06-leave.md) | Leave types, balances, requests, approvals, carry-forward and resets |
| [07 Payroll](07-payroll.md) | Contracts, salary structures, pay items, tax, payslips, payroll runs, loans and encashment |
| [08 Recruitment](08-recruitment.md) | Job openings, the hiring pipeline, candidates, interviews and resume screening |
| [09 Onboarding](09-onboarding.md) | Onboarding stages and tasks and the new-joiner portal |
| [10 Offboarding](10-offboarding.md) | Exit pipelines, notice periods, exit tasks and resignation letters |
| [11 Performance](11-performance.md) | Objectives and key results, feedback, one-to-one meetings and bonus point rules |
| [12 Projects](12-projects.md) | Projects, tasks and timesheets |
| [13 Assets](13-assets.md) | Company assets, requests, allocation, returns and service requests |
| [14 Helpdesk](14-helpdesk.md) | Support tickets, ticket claims and FAQs |
| [15 Employee documents](15-employee-documents.md) | Document requests, uploads, approval and expiry |
| [16 Reports](16-reports.md) | The 34 standard reports, exports and scheduled report e-mails |
| [17 Automations and notifications](17-automations-and-notifications.md) | Mail automations, in-app notifications and WhatsApp |
| [18 Integrations](18-integrations.md) | Google Meet, Google Drive backup, LinkedIn, storage, error tracking, and integrations that are switched off |
| [19 Data import](19-data-import.md) | The spreadsheet import wizard |
| [20 Platform experience](20-platform-experience.md) | Common screens, dashboards, themes, product tours, feature access rules and audit settings |
| [21 Security and access](21-security-and-access.md) | Login, lockout, sessions, mobile app tokens and the protections removed in this fork |
| [22 Mobile app API](22-mobile-app-api.md) | What the mobile app can do through the system's API |
| [Glossary](glossary.md) | Plain-English explanation of every term written in bold |

The report folder also holds a small checking tool in `tools/`; see [tools/README.md](tools/README.md).

## Related documents

- [Horilla HRM feature reference](../Horilla_HRM_FEATURES.md): the longer feature list this fork keeps in its `docs/` folder.
- [Apurba HRM v2 compared with Horilla](<../ApurbApurba_HRM-v2_vs_Horilla_HRMS—Feature_Comparison.md>): the feature comparison with the company's other HR product.
- [Plan to move Apurba HRM into Horilla](../APURBA_TO_HORILLA_INTEGRATION_PLAN.md): the planned work, some of which is listed as not built in the overall file.

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version of the index. | Claude (AI-DLC developer agent) |
