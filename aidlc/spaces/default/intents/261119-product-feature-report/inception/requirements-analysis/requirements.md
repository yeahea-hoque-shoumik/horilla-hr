# Requirements: Product Feature Report

Inputs: `aidlc/spaces/default/intents/261119-product-feature-report/ideation/intent-capture/intent-statement.md` (approved framing), `aidlc/spaces/default/codekb/horilla-hr/business-overview.md` (feature areas, rules and flags found in the code), `aidlc/spaces/default/codekb/horilla-hr/architecture.md` and `aidlc/spaces/default/codekb/horilla-hr/code-structure.md` (how the system is built), and the answers in `requirements-analysis-questions.md` (RQ1 to RQ8 below).

## Intent Analysis

- **Goal:** give product owners and business analysts a complete, plain-English picture of what this HR system does today, so they can decide in an upcoming product review what to change, keep or remove (intent statement: Target Customer, Initiative Trigger).
- **Request type:** documentation only. No application code, configuration or data is changed; the only new files are under `docs/features/`.
- **Scope:** system-wide. The report covers all 22 feature areas the code scan found (business-overview.md §4.1 to §4.22), plus the ideas that run through every area (business-overview.md §3).
- **Complexity:** standard writing task over a large codebase (38 code components, about 360 API routes, 27 flagged issues).

## Functional Requirements

### FR1. Report location and structure

- **FR1.1** The report is a folder at `docs/features/` (RQ7).
- **FR1.2** The folder holds one Markdown file per feature area, 22 in total, one for each area listed in business-overview.md §4.1 to §4.22 (RQ1).
- **FR1.3** The folder holds an index page (`docs/features/README.md`) that lists all 22 feature areas with a one-line description and a link to each file (intent Q6).
- **FR1.4** The folder holds a "How the system works overall" file covering the ideas that run through every area: multiple companies in one install, the employee record as the hub, approvals, notifications, background jobs, time zones, and archiving instead of deleting (business-overview.md §3).
- **FR1.5** The folder holds a glossary file that explains every HR term and system term the report uses, and the index links to it (RQ8).
- Pass/fail: the folder exists at that path; it holds 22 area files, the index, the overall file and the glossary; every area file is linked from the index.

### FR2. Content of each feature-area file

- **FR2.1** Each area file opens with a short plain-English summary of what the area is for and who uses it.
- **FR2.2** Each area file lists every feature the code scan recorded for that area in business-overview.md §4. No feature from that list is left out.
- **FR2.3** For every feature, the file describes its business logic: what the system allows, refuses, calculates or does automatically, and when.
- **FR2.4** For every business rule, the file gives the reason it works that way when the code states one. When the code states none, it writes "Reason: not stated in the code" and never guesses (RQ3).
- **FR2.5** Each area file has a short "Who can do what" section naming which roles (employee, reporting manager, HR or admin roles, candidate) can do each main action. It is a summary, not a full permission matrix (RQ8).
- **FR2.6** Each area file has a "Recommendations" section with suggested fixes or improvements for that area, clearly labelled as recommendations rather than descriptions of today's system (RQ8).
- **FR2.7** Each area file ends with a change log listing date, what changed and who changed it, starting with the first version (RQ6).
- Pass/fail: a reviewer can tick every feature in business-overview.md §4.n against the matching file; every rule has either a stated reason or the exact "not stated" wording.

### FR3. Flagged issues

- **FR3.1** Every issue in the consolidated flag list (business-overview.md §6, 27 items), and every flag in the §4 area sections, appears in the area file it affects, next to the feature it affects (RQ4).
- **FR3.2** Each flagged issue states its type in plain words: a bug (does something different from what it plainly intends), a gap (something expected is missing), half-built (started but not finished), switched off, inconsistent (behaves differently depending on screen or channel), or a risk (works, but can produce a wrong or surprising result).
- **FR3.3** Each flagged issue is explained by its effect on the business or the people using the system, not by its code cause (RQ5).
- **FR3.4** Technical risks (for example removed web-server protections in production, an access log that can record pay amounts, background jobs that stop when one process is down, time zones not reaching scheduled jobs) are explained in plain English inside the area they affect; cross-cutting ones go in the overall file (FR1.4) (RQ5).
- **FR3.5** Features that are planned but not built (business-overview.md §5, "Planned but not built") are listed as not built, never as existing.
- Pass/fail: all 27 consolidated flags can be found in the area files; none is described only in code terms.

### FR4. Accuracy and verification

- **FR4.1** Claims about payroll, leave and attendance that the code scan marked "per doc" (not read in code) are checked in the code before the report states them (RQ2).
- **FR4.2** Any other claim that was not checked in the code carries a visible "Not yet verified in the code" note next to it (RQ2).
- **FR4.3** The overall file states the code version the report describes (commit `f2ab49933cfb40d295b3a9e65eba21996df2b0dc`, scanned 2026-11-19), so readers know which version it describes.
- Pass/fail: no "per doc" payroll, leave or attendance claim appears unverified; every unverified claim elsewhere carries the note.

### FR5. Writing style

- **FR5.1** The report is written in plain English for non-technical readers (intent statement: Target Customer).
- **FR5.2** The report contains no code sections, except a short snippet where it makes an explanation simpler (intent statement: Success Metrics).
- **FR5.3** File paths and code names appear only where needed for a reviewer to check a claim, and never as the explanation itself.
- **FR5.4** The report links to the existing documents in `docs/` where they add detail, and does not copy them (intent Q5).
- Pass/fail: no fenced code block longer than a few lines; every technical term used is in the glossary.

### FR6. Way of working

- **FR6.1** The report is written one area file at a time, in the order of the index, so each step can be reviewed (intent statement: Initial Scope Signal).
- **FR6.2** At most one helper agent runs at any time while the report is produced (intent statement: Initial Scope Signal).
- Pass/fail: the writing plan lists files in index order; no two helper agents run at once.

## Non-Functional Requirements

- **NFR1 Completeness:** 22 of 22 feature areas have a file; 100% of features in business-overview.md §4 and 27 of 27 consolidated flags appear in the report.
- **NFR2 Maintainability:** each area can be updated by editing one file plus its change log; no fact is repeated in more than one area file (shared ideas live in the overall file and are linked).
- **NFR3 Readability:** every area file opens with a summary of no more than 5 sentences; every technical term is defined in the glossary.
- **NFR4 Accuracy:** 0 claims in the payroll, leave and attendance files rely only on "per doc" sources; 0 unverified claims elsewhere lack the "Not yet verified in the code" note.

## Constraints

- Documentation only: no application code, settings, tests or data are changed (intent statement: Problem Statement).
- The code at commit `f2ab49933cfb40d295b3a9e65eba21996df2b0dc` is the source of truth; existing documents in `docs/` are linked, not trusted on their own (intent Q5).
- At most one helper agent at a time (FR6.2).

## Assumptions

- Grouping follows the 22 feature areas in business-overview.md; some areas cover several code components (for example attendance covers biometric devices, geofencing and face detection). Reason: the person chose the 22 areas as the completeness list (RQ1).
- Recommendations are the writer's suggestions and are labelled as such. Reason: the person asked for recommendations (RQ8), and also asked that reasons for rules are never guessed (RQ3), so the two must stay visibly separate.
- No per-file header (owner, review date, commit) is added; the change log is the upkeep record and the overall file states the code version. Reason: the person chose only the change log (RQ6).
- No screenshots are produced: the work only reads code and writes text. Reason: nothing is run, so there are no screens to capture.

## Out of Scope

- Changing or fixing any code, including the flagged bugs.
- A full role-by-permission matrix (a short per-area summary is in scope, FR2.5).
- Short stable reference IDs per feature or rule (not chosen, RQ6).
- Code-level API reference; `aidlc/spaces/default/codekb/horilla-hr/api-documentation.md` already covers it and can be linked.

## Open Questions

- None.
