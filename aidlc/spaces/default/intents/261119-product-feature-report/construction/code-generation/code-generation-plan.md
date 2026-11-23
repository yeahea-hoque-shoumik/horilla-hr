# Code Generation Plan: Product Feature Report

## Summary

- Builds: the plain-English product report in `docs/features/` (index, overall file, 22 area files, glossary) plus a small checker for it
- Touches: new files only, all under `docs/features/` (no application code, settings or data change)
- Tests: 8 unit tests of the report checker, then the checker run over the finished report

## Inputs

- Requirements: `aidlc/spaces/default/intents/261119-product-feature-report/inception/requirements-analysis/requirements.md` (FR1 to FR6, NFR1 to NFR4).
- Source knowledge base: `aidlc/spaces/default/codekb/horilla-hr/` (mainly `business-overview.md` §3 to §6 and `component-inventory.md`), checked against the code at commit `f2ab49933cfb40d295b3a9e65eba21996df2b0dc`.
- No Units Generation: this is one zero-Unit build; the work is planned file by file in index order (FR6.1).

## Writing rules applied to every report file

These rules settle the points the requirements review raised (R-01 to R-06) so the writer and the checker share one definition.

- **One home per flag (R-01).** Each flagged issue is written in full in exactly one home file, next to the feature it affects; any other area it touches gets a one-line link to it. A link is not a repeated fact (NFR2). Homes for the cross-area flags in business-overview.md §6: #1 time zones and #26 manager access in `00-how-the-system-works.md`; #5 penalty restore in `06-leave.md` (linked from `05-attendance.md`); #16 Excel import and #18 extra background pollers in `05-attendance.md` (#18 linked from `18-integrations.md`); #24 removed web-server protections and #25 access log in `21-security-and-access.md`; #27 silent bot notices in `17-automations-and-notifications.md`.
- **Verification (R-02, FR4).** Payroll, leave and attendance claims marked "per doc" in the knowledge base are checked in the code before they are written; this explicitly includes flag #16 (Excel attendance import). Every other unchecked claim carries the exact note "*Not yet verified in the code.*".
- **Not built and fork changes (R-03, FR3.5).** The planned-but-not-built list and the fork's own changes (business-overview.md §5) live in `00-how-the-system-works.md`; an area file that a not-built item concerns links to it.
- **Measurable style (R-04, FR5).** No fenced code block longer than 5 lines. Every technical or HR term is written in **bold** on its first use in a file and has an entry in `glossary.md`.
- **Who can do what (R-05, FR2.5).** Drawn from the permission checks read in the code (decorators and permission names). Where the code checks inconsistently, the section says so and links to flag #26.
- **Audience (R-06).** The index states that the report is for people with access to this repository, because it describes security weaknesses.
- **Reasons (FR2.4).** A rule whose reason the code does not state carries exactly "Reason: not stated in the code".
- **Recommendations (FR2.6).** Each area file has a `## Recommendations` section, worded as suggestions.
- **Area file sections, in order:** `## Summary`, `## Who uses it`, `## Features` (each feature with its business logic, reasons and flags), `## Who can do what`, `## Recommendations`, `## Related documents`, `## Change log`.

## Testing Contract

```json
{
  "version": 1,
  "methodology": "test-after",
  "source": "org",
  "ordering": "implement each applicable testable layer, then write and run that layer's tests.",
  "scope": "bugfix",
  "test_strategy": "standard",
  "project_type": "brownfield",
  "applicable_notes": [
    {
      "layer": "org",
      "text": "We treat tests as a first-class deliverable in every Bolt. The specific\nmethodology (TDD, BDD, ATDD, or classic test-after) is affirmed at\npractices-discovery and recorded in `team.md` under this heading with explicit\n`Methodology` and `Ordering` fields; Code Generation resolves those fields\nindependently from coverage, tooling, and scope notes.\n\nWhen no posture has been affirmed, our default per scope is:\n- **Methodology**: test-after\n- **Ordering**: implement each applicable testable layer, then write and run\n  that layer's tests.\n- `mvp`, `enterprise`, `feature`, `infra` add an 80% line-coverage\n  floor and CI execution before merge.\n- `bugfix`, `security-patch` add a targeted regression for the specific\n  bug/vulnerability and require the existing suite to remain green.\n- `express` uses the Minimal strategy: requirement-driven unit tests (one per\n  requirement, with a happy-path floor per component); existing tests remain\n  green.\n- `poc`, `refactor`, `workshop`, `classic` add no extra new-test floor and require the\n  existing suite to remain green.\n\nThe active `Test Strategy` still applies in every scope and determines test\nvolume/types. Scope floors are additive; they never reduce or replace the\nselected strategy.\n\nBuild and Test verifies defined coverage floors and affirmed quality targets;\nthey may not be weakened to make a step pass.\n\nAffirm a stricter posture in `team.md` if the team commits to one."
    }
  ],
  "obligations": {
    "strategy": "standard",
    "strategy_volume": [
      "Five to eight tests per component.",
      "Unit tests plus integration tests for key boundaries.",
      "Add E2E, performance, or security tests when requirements demand them."
    ],
    "scope_floor": [
      "Include a targeted regression for the bug or vulnerability.",
      "Keep the existing test suite green."
    ],
    "combination_rule": "Apply every selected-strategy obligation and every scope-floor obligation; neither replaces the other, and a targeted scope regression may add the narrowest necessary test type beyond the strategy default."
  },
  "plan_profile": {
    "methodology": "test-after",
    "runner_step": "Verify the existing test runner/configuration and record the exact unit-scoped command.",
    "runner_ready_before_first_test": true,
    "testable_layers": [
      "Data model / database behavior",
      "Repository / data access",
      "Business logic",
      "API / endpoint",
      "Frontend behavior"
    ],
    "steps": [
      "Project structure and production configuration skeleton.",
      "Verify the existing test runner/configuration and record the exact unit-scoped command.",
      "Data model / database behavior - implement.",
      "Data model / database behavior - write and run its tests after implementation.",
      "Repository / data access - implement.",
      "Repository / data access - write and run its tests after implementation.",
      "Business logic - implement.",
      "Business logic - write and run its tests after implementation.",
      "API / endpoint - implement.",
      "API / endpoint - write and run its tests after implementation.",
      "Frontend behavior - implement.",
      "Frontend behavior - write and run its tests after implementation.",
      "Environment/build configuration.",
      "Documentation and traceability."
    ]
  },
  "input_sha256": "sha256:299c066197237c6d7918782f94fb07819a69d754e00ac4b4698ed2674a646583",
  "contract_sha256": "sha256:cc61d59d82034341370db942efc30f0a2f9331647081132ff6189c2a7673cb11"
}
```

How the contract applies here: the only testable layer is "Business logic" (the report checker). Data model, repository, API and frontend layers do not exist in a documentation deliverable and are omitted. The order stays test-after: the checker is implemented, then its tests are written and run. The bugfix scope's "targeted regression" has no bug to reproduce here; its equivalent is the checker run over the finished report (Step 29), and the existing application test suite stays untouched because no application code changes.

## Steps

### Structure

- [x] **Step 1. Report folder and index.** Create `docs/features/README.md`: purpose, audience line (people with repository access, R-06), code version described, how to read the flags, and the list of all 22 area files plus `00-how-the-system-works.md` and `glossary.md`, each with a one-line description and a link. (FR1.1, FR1.2, FR1.3, FR1.5, FR4.3)
- [x] **Step 2. Verify the test runner.** Confirm `python3` runs and record the exact command in `unit-test-instructions.md` (already written before approval; this step re-checks it runs). (Testing Contract runner step)

### Report content (written one file at a time, in index order)

- [x] **Step 3. `docs/features/00-how-the-system-works.md`.** Ideas that run through every area (multiple companies, the employee record as the hub, approvals, notifications, background jobs, time zones, archive instead of delete, roles), the code version, the fork's own changes, the planned-but-not-built list, and the home entries for flags #1 and #26. (FR1.4, FR3.4, FR3.5, FR4.3)
- [x] **Step 4. `01-organisation-and-company-setup.md`** (business-overview.md §4.1). (FR2.1-FR2.7, FR3.1-FR3.3)
- [x] **Step 5. `02-employees.md`** (§4.2). (FR2, FR3)
- [x] **Step 6. `03-shifts-and-work-types.md`** (§4.3: shifts, work types, rotations, rosters, change requests). (FR2, FR3)
- [x] **Step 7. `04-holidays-and-announcements.md`** (§4.4). (FR2, FR3)
- [x] **Step 8. `05-attendance.md`** (§4.5, including biometric devices, geofencing and face check; "per doc" claims and flag #16 verified in code). (FR2, FR3, FR4.1)
- [x] **Step 9. `06-leave.md`** (§4.6; "per doc" claims verified in code; home of flag #5). (FR2, FR3, FR4.1)
- [x] **Step 10. `07-payroll.md`** (§4.7; formulas, tax, encashment and calculation claims verified in `payroll/methods/` before they are stated). (FR2, FR3, FR4.1)
- [x] **Step 11. `08-recruitment.md`** (§4.8). (FR2, FR3, FR4.2)
- [x] **Step 12. `09-onboarding.md`** (§4.9). (FR2, FR3, FR4.2)
- [x] **Step 13. `10-offboarding.md`** (§4.10). (FR2, FR3)
- [x] **Step 14. `11-performance.md`** (§4.11). (FR2, FR3)
- [x] **Step 15. `12-projects.md`** (§4.12). (FR2, FR3)
- [x] **Step 16. `13-assets.md`** (§4.13). (FR2, FR3)
- [x] **Step 17. `14-helpdesk.md`** (§4.14). (FR2, FR3)
- [x] **Step 18. `15-employee-documents.md`** (§4.15). (FR2, FR3)
- [x] **Step 19. `16-reports.md`** (§4.16; each of the 34 reports named with what it shows; definitions not read in code marked "Not yet verified in the code"). (FR2, FR3, FR4.2)
- [x] **Step 20. `17-automations-and-notifications.md`** (§4.17, including WhatsApp; home of flag #27). (FR2, FR3)
- [x] **Step 21. `18-integrations.md`** (§4.18; switched-off integrations named as such). (FR2, FR3)
- [x] **Step 22. `19-data-import.md`** (§4.19). (FR2, FR3, FR4.2)
- [x] **Step 23. `20-platform-experience.md`** (§4.20). (FR2, FR3, FR4.2)
- [x] **Step 24. `21-security-and-access.md`** (§4.21; home of flags #24 and #25, explained by business effect). (FR2, FR3, FR3.4)
- [x] **Step 25. `22-mobile-app-api.md`** (§4.22; what the mobile app can do, not a route list; links to `aidlc/spaces/default/codekb/horilla-hr/api-documentation.md` for the technical list). (FR2, FR3, FR5.3)
- [x] **Step 26. `docs/features/glossary.md`.** Every term written in bold in any report file, with a plain-English definition. (FR1.5, NFR3)

### Checker (business logic layer: implement, then test)

- [x] **Step 27. Implement `docs/features/tools/check_report.py`** (Python standard library only). It checks the report folder and exits non-zero with a list of problems when:
  1. any of the 25 expected files is missing;
  2. the index does not link to every expected file;
  3. an area file lacks one of the required sections, in order;
  4. a file's change log has no entry;
  5. a fenced code block is longer than 5 lines;
  6. a bold term has no glossary entry;
  7. a rule-reason line uses anything other than a stated reason or the exact "Reason: not stated in the code" wording;
  8. one of the 27 consolidated flags (listed in the checker by home file and a key phrase) is missing from its home file.

  (NFR1, NFR3, FR2.4, FR2.7, FR5.2)
- [x] **Step 28. Write and run `docs/features/tools/test_check_report.py`.** 8 unit tests using `unittest` and a temporary folder: a complete minimal report passes; a missing file fails; a missing index link fails; a missing section fails; an empty change log fails; a 6-line code block fails; an undefined bold term fails; a missing flag fails. Run with the command in `unit-test-instructions.md`. (Testing Contract: business logic tests after implementation)

### Verification and documentation

- [x] **Step 29. Run the checker over the finished report** (`python3 docs/features/tools/check_report.py docs/features`) and fix every problem it lists until it exits 0. (NFR1, NFR3, NFR4)
- [x] **Step 30. Documentation and traceability.** Add a short `docs/features/tools/README.md` saying what the checker verifies and how to run it after editing the report. (FR6.1, NFR2)

## Out of plan

- No application code, migrations, settings, tests outside `docs/features/`, or deployment files change.
- No screenshots.
