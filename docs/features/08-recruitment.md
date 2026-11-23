# Recruitment

## Summary

This area runs hiring: job openings, a pipeline of hiring stages, candidates, interviews, application forms and surveys, resume screening and a talent pool. Candidates can apply through a public form and follow their application through a candidate login. Hired candidates move on to [Onboarding](09-onboarding.md).

## Who uses it

- Recruiters and recruitment managers create job openings, move candidates through stages and schedule interviews.
- Stage managers and interviewers work on the stages and interviews they are named on.
- Candidates apply, answer surveys and follow their application.

## Features

### Job openings (recruitments)

- A job opening has job positions, number of vacancies, start and end dates, managers, required skills, a survey template, and is published or closed.
- Rule: creating a job opening creates its first pipeline stage automatically. Reason: not stated in the code.
- Rule: every hour, job openings whose end date is today are closed and unpublished. Reason: not stated in the code.

> Flag (bug): recruitments past their end date stay open when the scheduler has been running for more than a day. The closing job reads "today" once, when the scheduler process starts, and then looks only for openings ending exactly on that date (`recruitment/scheduler.py`). Business effect: job openings keep accepting applications after their end date, and HR must close them by hand.

### Pipeline stages

- Stages are typed as initial, applied, test, interview, rejected (cancelled) or hired, each with its own managers. Candidates are moved by drag and drop on a board.

### Candidates

- A candidate has a profile, resume, source (application form, added inside the system, or other), referral source (job board, career site, social media, employee referral, recruiter, search engine, college, event or other), notes, ratings, rejection reasons and history.
- Offer letter status: not sent, sent, accepted or rejected, then joined.
- A hired candidate can be turned into an employee.
- Rule: every 5 minutes, active candidates whose e-mail address already belongs to a system user are marked as "converted". Reason: not stated in the code.

### Interviews

- Interviews have interviewers, a date and time, and an optional Google Meet link (see [Integrations](18-integrations.md)).

### Application forms and surveys

- Each job opening can have a public application form. Surveys support 10 question types: yes or no, single choice, multiple choice, text, number, percentage, date, long text, file and rating.

### Candidate self-tracking

- Candidates can sign in to see their own application. That this can be switched on and off comes from the feature reference. *Not yet verified in the code.*
- Checked in the code: the candidate signs in with their e-mail address as the user name and their phone number as the password, and the last 10 digits of the phone number are enough (`recruitment/auth.py`).

> Flag (risk): found while checking the code for this report. The candidate login uses the phone number as the password. Business effect: anyone who knows a candidate's e-mail address and phone number, which often appear together on a CV, can see that candidate's application.

### Resume screening

- HR can upload many resumes at once. The system reads names, e-mail addresses, phone numbers and dates of birth from them with a language-processing library, matches skills and ranks the resumes. *Not yet verified in the code.*
- Rule: the language model is loaded once when the recruitment screens start. Reason (from a code comment): loading the model is slow, so it must never be done while answering a request.

> Flag (risk): because the language model is loaded when the recruitment screens start, the whole application depends on that library and its model being installed (`recruitment/views/views.py`). Business effect: upgrading the server's Python version or reducing the size of the installation is limited by resume screening, even for customers who never use it.

### Talent pool

- A "Skill Zone" keeps promising candidates grouped by skill for future openings.

### Candidate document requests

- HR can ask candidates to upload documents. Asking creates an empty document slot for each chosen candidate.

### LinkedIn

- Job openings can be posted to LinkedIn and removed from it (see [Integrations](18-integrations.md)).

## Who can do what

| Action | Who |
|---|---|
| Create and change job openings, stages, surveys and reject reasons | People with the matching recruitment permissions (Admin, HR Manager, Recruiter) |
| Work on candidates in a job opening | People with the candidate permissions, and the managers named on that job opening or stage |
| Schedule interviews | People with the interview permission, and recruitment managers |
| Apply and follow an application | Candidates, through the public form and the candidate login |

These come from the permission checks and the recruitment-manager and stage-manager checks on the recruitment screens (`recruitment/views/`).

## Recommendations

- Suggestion: make the closing job close every opening whose end date has passed, not only those ending on the day the scheduler started.
- Suggestion: give candidates a proper password or a one-time e-mail link instead of their phone number.
- Suggestion: load the resume language model only when resume screening is used.

## Related documents

- [Onboarding](09-onboarding.md): what happens after a candidate is hired.
- [Reports](16-reports.md): recruitment funnel, time to hire and source quality.
- [Horilla HRM feature reference](../Horilla_HRM_FEATURES.md)

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
