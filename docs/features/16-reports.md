# Reports

## Summary

This area offers 34 standard reports across the workforce, time and leave, payroll, talent and compliance. Reports can be filtered, compared across periods, drilled into, exported and sent by e-mail on a schedule. Who may see, export or subscribe to each report can be controlled per report.

## Who uses it

- HR, payroll and leadership read reports and export them.
- Managers read reports about their own teams.
- Administrators decide who may see, export or subscribe to each report.

## Features

### The 34 standard reports

The names and descriptions below were read from the report definitions in the code (`report/metrics/definitions.py`). How each figure is calculated inside the report was not read. *Not yet verified in the code.*

| Report | What it shows | Permission it needs by default |
|---|---|---|
| Workforce Composition | Headcount and its spread by department, employee type, job and location | Employee view |
| Diversity Snapshot | Gender and age bands and the leadership mix; marital status is left out of the default view | Employee view |
| Tenure & Longevity | Average length of service and service bands by department | Employee view |
| Turnover (All Exits) | Hires against all exits, the period turnover rate and first-year exits; does not split voluntary and involuntary exits | Employee view |
| Joiners & Leavers | Joiners and leavers in the period (with how they left), net change and a month-end headcount trend | Employee view |
| Span of Control | Number of managers, average team size and the manager-to-headcount ratio | Employee view |
| Headcount Bridge | Opening headcount plus joiners minus leavers equals closing headcount | Employee view |
| Exit Analysis | Exits by how they left, department and length of service at exit | Employee view |
| New-Hire 90-Day Attrition | Share of the period's joiners who left within 90 days | Employee view |
| Attendance Summary | Present days, late arrivals, overtime and a department breakdown | Attendance view |
| Absenteeism Rate | Unplanned absence against expected working days (holidays and days off taken out, approved leave not counted as absence) | Attendance view |
| Overtime Analysis | Overtime hours by department; named employees only for people who can change attendance | Attendance view |
| Unscheduled Absence | Unplanned absence for the period, aware of holidays and days off | Attendance view |
| Leave Planning (Used vs Entitlement) | Leave days approved in the period against the current entitlement | Leave request view |
| Open Leave Balance (Days) | Open balances in days (available plus carried forward) by leave type and department; not a money figure | Leave request view |
| Labor Cost Summary | Gross pay, net pay and deductions by department; employer cost shown as gross until contribution items exist | Payslip view |
| Cost Composition | The mix of allowances and deductions from payslip lines | Payslip view |
| Payroll Headcount Cost | Gross cost per active employee and average pay by department | Payslip view |
| Payslip Register | The confidential list of payslips for the period; exporting needs export rights | Payslip view |
| Payroll Readiness | Active employees who cannot be paid because bank details or an active contract are missing; an empty report is good | Payslip or contract view |
| Loan & Advance Ledger | Outstanding loans and advances: amount lent, instalments recovered and balance left | Payslip or loan view |
| Reimbursement Register | Reimbursement and encashment claims by type and status, including what is still pending before a payroll run closes | Payslip or reimbursement view |
| Recruitment Funnel | How many candidates sit in each stage in the period, and the mix of sources | Recruitment view |
| Time to Hire / Fill | Average and middle number of days from application to joining, and how long openings have been open | Recruitment view |
| Offer & Acceptance | Offer letter status mix and the acceptance rate | Recruitment view |
| Onboarding Progress | Stage and task completion for candidates who started onboarding in the period | Recruitment view |
| Pipeline Aging | How long open candidates have been waiting since they applied, by stage | Recruitment view |
| Source Quality | How often each source leads to a hire, counting each candidate once (referrals first) | Recruitment view |
| Quality of Hire (90-day retention) | Share of hires who are still employed 90 days after joining; not a performance score | Recruitment view |
| Objective & KR Health | Status and progress bands of objectives and key results; not a performance rating | Objective view |
| Audit Activity | How many changes were logged, by action and record type, across all companies | Employee view or audit tag view |
| Document Expiry Aging | Employee documents that are overdue or expire within 90 days | Employee view or document view |
| Contracts & Document Expiry | Contracts ending and documents with an expiry date; "visa" is recognised from the document title only | Employee, document or contract view |
| Asset Register | Assets by status, and how long each allocated asset has been held | Asset view or employee view |

> Flag (risk): found while checking the code for this report. The Audit Activity report counts changes across all companies, not only the active one; the code itself advises using the per-report access settings for production. Business effect: anyone with the employee view permission in one company can see change volumes for every company in the installation.

### Working with reports

- Reports offer filters, comparison with an earlier period, drill-down into the people behind a figure, headline figures, charts and a written commentary.
- Reports export to Excel, CSV and PDF.
- Each user can keep favourites, saved views and filter presets.
- A pivot "Explorer" per area lets users build their own tables. *Not yet verified in the code.*
- Users without a company-wide permission see only the people who report to them. *Not yet verified in the code.*

### Access settings per report

- An access table can say, per report or per area and per role group or permission, who may view, export and subscribe. Rule: when no access rows exist, the report's own default permission (in the table above) and the company's export setting decide. Reason: not stated in the code.

### Scheduled report e-mails

- Users can subscribe to a report and receive it by e-mail on a schedule.
- Rule: due subscriptions are checked and sent every hour (`report/scheduler.py`). Reason: not stated in the code.

## Who can do what

| Action | Who |
|---|---|
| See a report | People with that report's default permission, or as the access table allows |
| Export a report | People allowed by the access table, or by the company's export setting |
| Subscribe to a report by e-mail | People allowed by the access table. *Not yet verified in the code.* |
| Change the access table | Administrators. *Not yet verified in the code.* |

These come from the report definitions and the access rules (`report/metrics/definitions.py`, `report/access.py`).

## Recommendations

- Suggestion: limit the Audit Activity report to the active company by default.
- Suggestion: add a way to split exits into voluntary and involuntary, which several reports say they cannot do today.
- Suggestion: show on each report how its figures are calculated, so readers can trust them.

## Related documents

- [Payroll](07-payroll.md), [Attendance](05-attendance.md), [Leave](06-leave.md), [Recruitment](08-recruitment.md): where the figures come from.
- [Horilla HRM feature reference](../Horilla_HRM_FEATURES.md)

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
