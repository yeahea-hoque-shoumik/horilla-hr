# Intent Statement: Product Feature Report for the HR System

## Problem Statement

There is no single plain-English description of what this HR system does: which feature domains it covers, which features each domain offers, and the business logic behind each feature. [desc]

The requester wants one report, saved in the `docs/` folder, that answers three questions: what feature domains the project covers, what specific features each domain has, and what business logic applies to every feature, including the reason a thing is done one specific way. [desc]

The report must not skip any domain, feature, business rule, or reason behind a rule. [desc]

## Target Customer

The first readers are product owners and business analysts: the people who plan changes to the product. [Q1]

They are non-technical stakeholders who want to understand the system from the product perspective, so the report is written in plain English, with no code sections unless a small piece of code makes an explanation simpler. [desc]

Readers will use the report to decide what to change, keep, or remove, so known gaps and half-built features are flagged where they are found. [Q2]

## Success Metrics

- Every feature domain found in the codebase has its own section in the report; zero domains are left out. [desc] [Q4]
- Every feature listed under a domain has its business logic described, including the reason it works that way where the code shows one. [desc]
- The report contains no code sections, except a short snippet where it makes an explanation simpler. [desc]
- Every gap or half-built feature that is found is flagged in the section it belongs to. [Q2]
- The report is a folder with one file per domain plus an index page that links to every domain file. [Q6]

## Initiative Trigger

A product review or planning cycle is coming up, and readers need an accurate picture of the current system before it. [Q3]

## Initial Scope Signal

- Workflow-selected scope: `bugfix` (workflow-selected; this plan was tailored from it for a documentation-only task). [scope]
- Domains in this report: all HR business areas (employees, attendance, leave, payroll, recruitment, onboarding, offboarding, performance, assets, helpdesk, projects and similar). [Q4]
- Also in this report: the supporting features users still see (reports and dashboards, notifications, bulk data import, geofencing, face detection, biometric devices, the mobile app connection, document requests). [Q4]
- Also in this report: administration and platform features (multi-company setup, roles and permissions, audit history, backups, theming, settings). [Q4]
- The report is written fresh from the code, and links to the existing documents in `docs/` where they add detail. [Q5]
- Nothing is left out of this first version: screenshots, recommendations, and a permission matrix are all allowed where they help a non-technical reader. [Q8]
- The work is done step by step, with at most one helper agent running at a time. [desc]
- The report is built so it can be reviewed and updated later. [desc] [Q6]

## Assumptions & Open Questions

None.
