# Intent Capture Questions

## Sources

- [desc] Initial description: "I want a full report about this project, save it in the docs folder. I want to understand,\n1. what are the feature domain this project covers\n2. what are the specific features in each domain\n3. what are the business logic for every feature. \nwrite everything in plain english , no need to any code sections. only add any piece of code  if that would make explanantion simpler.\nthis doc should be mostly for non tech stakeholders. who want to understand it from the product perspective. \ndon't skip any domain or feature or business logic or reason for doing one thing any specific way. \nDo the task step by step. don't start more than 1 sub agent at once. make the doc such that it can be reviewed and updated later."
- [scope] Workflow-selected scope: `bugfix`.

## Q1. [Product] Who exactly will read this report first?

You said the report is mostly for non-technical stakeholders who want the product view. Knowing which group reads it first sets the tone, how much HR vocabulary I can assume, and what each section opens with.

A. Company leadership and management (decision-makers deciding what to keep, change or invest in)
B. HR team and HR operations staff (the people who use the system every day)
C. Product owners and business analysts (people who plan changes to the product)
D. Not yet defined: write for a general non-technical reader
X. Other (please specify)

[Answer]: C

## Q2. [Product] What will readers do with the report once they have it?

This decides what each feature section ends with, for example "what this means for you" notes, open gaps, or nothing beyond the description.

A. Understand what the system does today (a reference only)
B. Decide what to change, keep or remove, so known gaps and half-built features should be flagged
C. Onboard new team members and stakeholders to the product
D. Not yet defined
X. Other (please specify)

[Answer]: B

## Q3. [Product] What prompted this report now?

The repository already holds migration documents comparing the older Apurba HRM with this Horilla-based system. Knowing the trigger tells me whether to point out where this system differs from the old one.

A. The migration from the older Apurba HRM system: readers need to know what the new system does
B. Customisations have been added on top of Horilla and there is no single description of the result
C. A product review or planning cycle is coming up
D. None in particular: a general documentation need
X. Other (please specify)

[Answer]: C

## Q4. [Product] Which parts of the system count as a "domain" to cover? (select all that apply)

The codebase has the HR business areas (employees, attendance, leave, payroll, recruitment, onboarding, offboarding, performance, assets, helpdesk, projects) and also supporting areas that are less visible to HR users. You asked not to skip any domain, so I want to confirm whether the supporting areas belong in this report too.

A. All HR business areas (employees, attendance, leave, payroll, recruitment, onboarding, offboarding, performance, assets, helpdesk, projects and similar)
B. Supporting features users still see: reports and dashboards, notifications, bulk data import, geofencing, face detection, biometric devices, the mobile app connection, document requests
C. Administration and platform features: companies and multi-company setup, roles and permissions, audit history, backups, theming, settings
D. Mark which features were added or changed by your team versus what came with standard Horilla
X. Other (please specify)

[Answer]: A, B, C

## Q5. [Product] How should the report relate to the documents already in `docs/`?

`docs/` already holds `Horilla_HRM_FEATURES.md`, `APURBA_HRM_APPLICATION_FEATURE_REFERENCE.md`, `horilla_db_domains.md` and others. The new report can stand alone or lean on them.

A. Write it fresh from the code, and do not rely on the existing documents (the code is the source of truth)
B. Write it fresh from the code, and link to the existing documents where they add detail
C. Extend or replace `Horilla_HRM_FEATURES.md` instead of creating a new document
D. Not yet defined
X. Other (please specify)

[Answer]: B

## Q6. [Product] How should the report be laid out so it can be reviewed and updated later?

You asked for a document that can be reviewed and updated later. A large system usually reads better split up, but one file is easier to share.

A. A folder with one file per domain plus an index page that lists every domain and links to it
B. One single long document with a table of contents
C. A folder per domain as in A, and every feature and business rule given a short stable reference (for example ATT-3, a rule inside attendance) so reviewers can point at it in comments
D. Not yet defined: choose what reads best
X. Other (please specify)

[Answer]: A

## Q7. [Product] Who reviews and signs off the report, and how often should it be refreshed?

This goes into the report's own header (owner, review date, how to propose changes) so it stays maintained.

A. I review it myself; it is refreshed when the system changes
B. A named product or HR owner reviews it; it is refreshed every release
C. Several stakeholders review it (for example HR, management and engineering); a review cadence will be agreed later
D. Not yet defined
X. Other (please specify)

[Answer]: A

## Q8. [Product] What should this first version of the report leave out? (select all that apply)

Everything below is something a product report sometimes contains. Picking one here keeps it out of this first version.

A. Screenshots and screen-by-screen walkthroughs
B. Recommendations or improvement ideas (describe what is there, not what should be)
C. A full who-can-do-what permission matrix for every role
D. None: include everything that helps a non-technical reader understand the product
X. Other (please specify)

[Answer]: D
