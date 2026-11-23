# Assets

## Summary

This area tracks company property such as laptops, phones and vehicles. HR keeps an inventory in categories and batches, employees ask for assets, and HR allocates them, takes them back with a condition report and handles service requests. The system warns before assets expire and marks expired assets as unavailable.

## Who uses it

- Asset managers and HR keep the inventory, allocate and take back assets, and handle service requests.
- Employees ask for assets, see what they hold, and raise service requests on them.

## Features

### Inventory

- Assets are grouped in categories and batches (lots). An asset is In use, Available or Not-Available, and has a quantity made up of individual items, each Available, In use, Damaged or Lost.
- Rule: an asset's status follows from its items. Saving an asset creates placeholder items up to its quantity and never removes items. Reason: not stated in the code.

### Asset requests and allocation

- Employees ask for an asset (Requested, Approved or Rejected). HR allocates assets to employees.
- When an asset comes back, HR records its condition (Healthy, Minor damage, Major damage or Lost), with images, reports and documents.

### Service requests

- A service request can be raised on an allocated asset: Requested, In Progress, Completed, Rejected or Returned, with notes.

### Fines, import, history and dashboard

- HR can charge a fine when an asset comes back damaged or lost (the fine form lives in payroll), import and export assets, see each asset's history, and use an asset dashboard. *Not yet verified in the code.*

### Expiry

- Rule: every day, assets past their expiry date become Not-Available, and the owner (or a superuser) is notified on the "notify before" date (`asset/scheduler.py`). Reason: not stated in the code.

> Flag (bug), described in [Employee documents](15-employee-documents.md): the same asset job file also runs the expiry check for employee documents, and that check does not work as intended.

## Who can do what

| Action | Who |
|---|---|
| Keep the inventory: categories, batches, assets | People with the asset, category and batch permissions (Admin, HR Manager, Asset Manager) |
| Allocate and take back assets | People with the asset allocation permissions |
| Ask for an asset or raise a service request | Every employee, for themselves |
| Approve or reject asset requests | People with the asset request or allocation permissions. *Not yet verified in the code.* |

These come from the permission and owner checks on the asset screens (`asset/views.py`).

## Recommendations

- Suggestion: move the employee document expiry check out of the asset jobs into the employee documents area.
- Suggestion: let HR reduce an asset's quantity, with a reason, instead of only adding items.

## Related documents

- [Employee documents](15-employee-documents.md): the document expiry check.
- [Offboarding](10-offboarding.md): getting assets back from leavers.
- [Reports](16-reports.md): the asset register.
- [Horilla HRM feature reference](../Horilla_HRM_FEATURES.md)

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
