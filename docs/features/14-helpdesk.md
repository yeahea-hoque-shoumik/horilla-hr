# Helpdesk

## Summary

This area lets employees raise tickets to HR or other teams: suggestions, complaints, service requests, meeting requests and anonymous complaints. Tickets have a priority, a status, assignees and a deadline, and department managers receive tickets raised against their department. A list of frequently asked questions is suggested while an employee writes a ticket.

## Who uses it

- Employees raise tickets, follow them and comment.
- Helpdesk agents and assignees work on tickets and can ask to take a ticket over.
- Department managers receive tickets raised against their department or job position.
- HR maintains ticket types and the FAQ list.

## Features

### Tickets

- Types: suggestion, complaint, service request, meeting request, anonymous complaint, others. Priority: low, medium or high. Status: new, in progress, on hold, resolved or canceled.
- A ticket is raised against an employee, a department or a job position, and has assignees, a deadline, tags, comments and attachments.
- Rule: tickets raised against a department or job position go to the managers set for that department. Reason: not stated in the code.

> Flag (gap): there are no service-level targets (SLA), no escalation and no handling of overdue deadlines; nothing happens when a ticket's deadline passes (`helpdesk/`). Business effect: tickets can sit unanswered past their deadline without anyone being told.

### Claim requests

- An agent can ask to take over a ticket; a manager approves the claim.

### FAQs

- HR keeps FAQ categories and questions. Matching FAQs are suggested while an employee writes a ticket.

## Who can do what

| Action | Who |
|---|---|
| Raise a ticket and comment on own tickets | Every employee |
| Work on a ticket | The ticket's owner, its assignees, and people with the ticket change permission (Admin, HR Manager, Helpdesk Agent) |
| Approve claim requests | Managers with the ticket permissions. *Not yet verified in the code.* |
| Set up ticket types, department managers and FAQs | People with the matching helpdesk permissions |

These come from the permission and ticket-owner checks on the helpdesk screens (`helpdesk/views.py`).

## Recommendations

- Suggestion: add service-level targets per ticket type and priority, with reminders and escalation when a deadline passes.
- Suggestion: report on ticket volumes and response times.

## Related documents

- [Horilla HRM feature reference](../Horilla_HRM_FEATURES.md)

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
