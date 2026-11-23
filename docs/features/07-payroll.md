# Payroll

## Summary

This area works out and records pay. It holds employee contracts, salary structures, pay items (earnings and deductions), income tax rules, payslips and payroll runs, plus loans, salary advances, fines, reimbursements and the cashing-in of leave and bonus points. It reads paid and unpaid days and overtime from the attendance monthly summary. It is the largest area of the system, and every rule below was checked in the code unless it carries a note.

## Who uses it

- Payroll and HR staff set up contracts, salary structures, pay items and tax, run payroll and send payslips.
- Employees see and download their own payslips and ask for reimbursements and encashments.
- Managers and payroll staff approve reimbursement and encashment requests.

## Features

### Contracts

- A contract states the wage type (daily or monthly, and hourly when attendance is installed), the pay frequency (weekly, monthly or twice a month), the **filing status** used for tax, the notice period and attached documents.
- Status flow: draft, active, then expired or terminated.
- A contract also says how one unpaid day is priced: as a share of basic pay, of the monthly **cost to company (CTC)** or of gross pay, divided by the working days or the calendar days of the month; whether unpaid days are taken off basic pay; and whether a flat amount per leave day is used instead.
- Rule: every 4 hours, active contracts past their end date become expired (`payroll/scheduler.py`). Reason: not stated in the code.

### Salary structures

- A salary structure is a set of pay items in one of two modes: **Gross Up**, where the contract wage is basic pay and allowances are added to it, or **CTC Down**, where the contract wage is the whole package and the items divide it up.
- Rule: a structure is checked before it is saved and before it is run. Only one earning can be marked as basic pay. A CTC Down structure must have an earning marked as basic pay. A Gross Up structure must not count basic pay twice. Reason (from a code comment): both mistakes produced payslips that looked fine but were wrong, for example basic pay counted twice, or income tax based on basic pay worked out on nothing (`payroll/methods/structure_rules.py`).

### Pay items: allowances and deductions

- An allowance (earning) can be a fixed amount, a percentage of basic pay or of another item, a custom formula over other items (for example "(BASIC + DA) × 0.12"), the balance left of the package in a CTC Down structure, an amount per child, or, when attendance is installed, based on overtime (regular, weekly-day-off or holiday overtime), shift, work type or days attended.
- A deduction can be a fixed amount, a percentage of basic, gross, taxable gross or net pay or of another item, or a custom formula. It is marked as before tax or after tax, and can be marked as the income tax itself.
- An item can apply to everyone, to chosen employees or to everyone except chosen employees, can apply on one date only, and can depend on conditions about the employee (for example children, marital status, experience, gender, country, pay frequency, wage type or department) or on an amount (for example "only if basic pay is above a figure").
- An item can have a maximum amount. A monthly figure is shared out when the pay period is shorter than a month. Reason (from a code comment): a joiner paid for ten days should get ten days' worth of a monthly figure, not a whole month's (`payroll/methods/proration.py`).
- Items run in a set order, and an item can use only the value of an item that runs before it. Reason (from a code comment): before, the order was whatever the database returned, so "allowance = 50% of basic" could not be relied on.
- A deduction can carry an **employer contribution**: what the employer pays on top, as a percentage or a formula. Reason (from a code comment): rules such as a provident fund split between pension and fund, each capped separately, could not be expressed with one percentage.

### Ready-made pay items

- A component library offers example items for India, the United States, the Gulf countries and the United Kingdom.
- Standard system items handle loans, salary advances, fines, penalties, reimbursements, encashments and loss of pay.

### Income tax

- A filing status bases tax on basic pay, gross pay or taxable gross pay, and computes it in this order: scale the period's figure to a year, take off a standard deduction, apply the tax bands (each band's rate applies only to the part of income inside it) or a Python formula, apply a rebate when income is at or below a limit, add a cess or surcharge on the tax, then scale the yearly tax back to the pay period. Reason (from a code comment): the order matches how such taxes are levied, for example cess is charged on the tax still payable after relief (`payroll/methods/tax_calc.py`).
- The Python formula is checked against an allowed list of instructions before it is saved and runs with limits and a time-out.
- Rule: when a filing status is set up to compute tax and fails, the payslip stops with an error instead of showing zero tax. Reason (from a code comment): a payslip that silently showed no tax looked normal while the employee was underpaying tax and the employer owed the difference.
- Ready-made tax packs: India New Regime and Old Regime (financial year 2025-26), US Federal Single and Married Filing Jointly (2025), UK PAYE for England with National Insurance (2025-26), and a flat 10%.

> Flag (gap): there is no Bangladesh tax pack, although the production setup runs in the Asia/Dhaka time zone (`payroll/tax_packs.py`). Business effect: a Bangladesh company must build its income tax rules by hand.

### Payslips

- Payslips are made one at a time or in bulk. Status flow: draft, review ongoing, confirmed, paid.
- A payslip can be downloaded as a PDF and e-mailed, shows how each line was worked out, and can be adjusted by hand.

### Payroll runs

- A payroll run has three steps: choose the period and the people; review what will be used for each person and what is wrong; then generate payslips in small batches so progress is visible and an interrupted run can be resumed. Status flow: Draft, In review, Approved, Paid, or Cancelled.
- Rule: a person is left out of a run, with the reason shown, when they are inactive, have no active contract, have a contract that starts after the period, or already have a payslip for that period. Reason (from a code comment): payroll is for people who work here now on a contract in force, and catching a duplicate here avoids an error halfway through a run.
- Rule: the review stops the run for a person who has an unresolved attendance **conflict**, or whose contract has no wage and whose structure has no earning marked as basic pay. It only warns when there is no salary structure or no attendance in the period. Reason (from a code comment): warnings are worth seeing but are not a reason to hold up everyone's pay (`payroll/methods/batch_run.py`).
- Rule: a run can move only along the allowed steps, and Paid and Cancelled are final. Reason (from a code comment): "a system that lets a paid run be moved back to draft cannot be relied on to say what was paid".

> Flag (inconsistent): on the payroll run path, one unresolved attendance conflict day makes the employee's whole month unpaid; only that path reads the attendance monthly summary at all. The run's review now blocks such people, but payslips made outside a run are worked out without the monthly summary (`payroll/methods/methods.py`, explained in a code comment in `payroll/methods/batch_run.py`). Business effect: the same employee can get a different payslip depending on which button was used to make it.

### Pay periods

- HR sets the pay period, for example from the 26th of one month to the 25th of the next.

### Automatic payslips

- Rule: on the day set per company (a day beyond the month's length means the last day), draft payslips are made for the previous month for every employee with an active contract, starting at the later of the period start and the contract start. Employees whose tax setup is broken are skipped and logged rather than paid with zero tax. Reason: not stated in the code.

> Flag (bug): on the generate day, automatic payslips are recalculated every 3 hours for people who joined in the middle of the period, and their payslip is set back to draft each time. The job looks for the payslip by the period start but saves it with the contract start, so it never finds it (`payroll/scheduler.py`). Business effect: corrections or confirmations made to mid-period joiners' payslips on that day are lost, and they keep returning to draft.

> Flag (gap), described in [How the system works overall](00-how-the-system-works.md): automatic payslips and contract expiry use the server's clock, not the company time zone.

### Attendance and leave in pay

- Payroll reads the attendance monthly summary for paid days, unpaid days and overtime (see [Attendance](05-attendance.md)).
- Rule: an attendance penalty with an amount becomes a one-time deduction for that employee on the attendance date (`base/signals.py`). Reason: not stated in the code.

### Loans, salary advances and fines

- Rule: a loan or salary advance creates a one-time payout on the chosen date and a schedule of instalment deductions; a fine creates no payout (`payroll/signals.py`). Reason (from a code comment): the loan's tax and part-month treatment follow the standard item; before, someone joining mid-month received only a fraction of their loan.

### Reimbursements and encashment

- Employees ask for an expense to be paid back (with a required attachment), for leave days to be cashed in, or for bonus points to be cashed in.
- Rule: the amount is the number of days (or points) times the amount per day (or per point) set in the encashment settings. Leave days are rounded to half days. Reason: not stated in the code.
- Rule: on approval, the days are taken from available and carried-forward leave (or the points from the bonus account). If there are not enough, the request stays "requested" and a message says so. Otherwise a one-time payout is added to the next payslip. Reason: not stated in the code.
- Rule: expenses, cashed-in leave and cashed-in bonus points each follow their own tax treatment. Reason (from a code comment): they are different things for tax, and before all three were treated as taxable.
- Leave encashment can be switched off, or limited to chosen employees, departments or job positions.
- Employees without the reimbursement change permission can only make requests for themselves.

> Flag (bug): found while checking the code for this report. If an approved leave or bonus encashment is later set to rejected, the days or points are not given back and the payout is not removed, because the check compares the type with a misspelt name ("leave encashment" instead of "leave_encashment") and the step that would undo it is skipped (`payroll/models/models.py`). Business effect: the employee keeps the payout and the days or points stay taken, even though HR rejected the request. Whether any screen offers rejecting an already approved request: *Not yet verified in the code.*

### Contributions and employer cost

- A contributions page lists, for a period, each contribution item (for example provident fund) with what was taken from employees and what the employer owes, with the working behind each figure and an export. Reason (from a code comment): the figures are read from the payslips actually issued, so a remittance always agrees with them.
- The employer's share is worked out in one place and shown on payslips and in a structure's worked example.
- A payroll dashboard is available.

## Who can do what

| Action | Who |
|---|---|
| Set up contracts, salary structures, pay items, filing statuses and tax bands | People with the matching payroll add or change permissions (Admin, Payroll Manager) |
| Make payslips and run payroll | People with the payslip permissions |
| See own payslips | Every employee, for their own payslips only |
| Ask for a reimbursement or encashment | Every employee, for themselves |
| Approve reimbursements and encashments | People with the reimbursement change permission |
| Change the automatic payslip settings | People with the automatic payslip permission |

These come from the permission checks on the payroll screens (`payroll/views/`). Payroll screens rely almost entirely on permissions; being someone's reporting manager does not by itself open them.

## Recommendations

- Suggestion: fix the automatic payslip lookup for mid-period joiners.
- Suggestion: make every way of producing a payslip use the attendance monthly summary in the same way.
- Suggestion: fix the misspelt type name so rejecting an approved encashment gives the days or points back and removes the payout.
- Suggestion: add a Bangladesh income tax pack if Bangladesh companies are run on this system.
- Suggestion: add a full-and-final settlement calculation for leavers (see [Offboarding](10-offboarding.md)).

## Related documents

- [Attendance](05-attendance.md): the monthly summary payroll reads.
- [Leave](06-leave.md): balances used by encashment and unpaid days.
- [Reports](16-reports.md): payroll reports such as cost composition and the payslip register.
- [Horilla HRM feature reference](../Horilla_HRM_FEATURES.md)

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
