# Requirements Analysis Questions

Context: the code scan (`aidlc/spaces/default/codekb/horilla-hr/business-overview.md`) found 22 feature areas, 38 code components and 27 flagged issues. These questions settle how the report turns that into a checkable deliverable, and resolve the points the framing review raised.

## Q1. [Product] What list of domains should the report be checked against for completeness?

The framing review noted that "no domain left out" needs a fixed list to check against. The scan offers three natural lists.

A. The 22 feature areas the scan found (organisation setup, employees, shifts, holidays, attendance, leave, payroll, recruitment, onboarding, offboarding, performance, projects, assets, helpdesk, documents, reports, automations and notifications, integrations, data import, platform experience, security and access, mobile API), one file each
B. One file per code component (38 files, including small technical ones)
C. The 22 areas grouped into about 12 business chapters (for example "Time and attendance" holding shifts, holidays and attendance), with the grouping shown on the index page
D. Not yet defined
X. Other (please specify)

[Answer]: A

## Q2. [Product] How should claims the scan did not verify in code be handled?

Some rules came from existing documents, not from reading the code (payroll and tax formulas, the 34 report definitions, some attendance rules). The report is used to decide changes, so accuracy matters.

A. Verify every such claim in the code while writing, and state it only once verified
B. Verify the important ones (payroll, leave, attendance); keep the rest with a visible "not yet verified" note
C. Keep them all, each with a visible "not yet verified" note
D. Not yet defined
X. Other (please specify)

[Answer]: B

## Q3. [Product] When the code shows no reason for a rule, what should the report say?

You asked for the reason behind every rule. The code states a reason for some rules (in comments) but not for most.

A. Write "Reason: not stated in the code", and never guess
B. Give the most likely reason, clearly labelled "Likely reason (inferred)"
C. Give a likely reason where one is obvious and write "not stated" otherwise, always labelled
D. Not yet defined
X. Other (please specify)

[Answer]: A

## Q4. [Product] Where should the flagged issues (bugs, gaps, half-built features) appear?

Readers will use the report to decide what to change.

A. Inside each domain file, next to the feature they affect
B. On one separate "Known issues and gaps" page only
C. Both: next to the feature, and collected on one "Known issues and gaps" page linked from the index
D. Not yet defined
X. Other (please specify)

[Answer]: A

## Q5. [Product] How should technical risks be covered for non-technical readers?

Some findings are technical (removed web-server protections in production, an access log that can record pay amounts, background jobs that stop if one process is down, time zones not reaching scheduled jobs).

A. Explain each in plain English by its business effect (for example "late-night punches can be filed on the wrong day"), in the domain it affects
B. Put them in a separate "Platform and security" chapter in plain English
C. Leave purely technical risks out and keep only those with a visible business effect
D. Not yet defined
X. Other (please specify)

[Answer]: A

## Q6. [Product] What should each report file carry so it can be reviewed and updated later? (select all that apply)

The framing review asked that the header fields be decided now, so "reviewable and updatable" can be checked.

A. A header with owner, last-reviewed date and the code version (commit) it describes
B. A change log at the bottom of each file
C. Short stable references for each feature and rule (for example LV-4) that reviewers can point at
D. A "how to propose a change" note on the index page
X. Other (please specify)

[Answer]: B

## Q7. [Product] Where in `docs/` should the report folder live?

A. `docs/product-report/`
B. `docs/product/`
C. `docs/features/`
D. Not yet defined: choose a clear name
X. Other (please specify)

[Answer]: C

## Q8. [Product] Which extras should this first version include? (select all that apply)

At framing you chose to leave nothing out; the review asked whether these are required or optional.

A. A short "who can do what" summary per domain (not a full permission matrix)
B. Recommendations: what to fix or improve, per domain
C. A glossary of HR and system terms
D. None of these: description and flags only
X. Other (please specify)

[Answer]: A, B, C
