# Agent Waves (P3 C5)

**Rule:** Do not promote later waves to `active` until revenue path (A034–A052) is testing-green.

## Wave 0 — Core control (done scaffolds)

A001–A010: routing, planning, evaluation harness agents.

## Wave 1 — Revenue path (priority)

A034–A052: lead discovery through reply triage.  
Skills: SK034–SK050. Workflow: `lead-outreach`.

**Exit:** completeness matrix + golden fixtures + dry-run E2E.

## Wave 2 — Inbound / comms

A066–A071: classify, draft, QA, meeting intel.  
Workflows: `inbound-email-triage`, `response-qa`, `conversation-intel`.

**Exit:** STD-05 parity (idempotency, dry-run, gates, audit).

## Wave 3 — Marketing

A084–A091: content, SEO, social, campaign QA.  
Workflows: `content-calendar`, `seo-audit`, `social-content-pipeline`.

**Exit:** publish gated; dry-run default; no auto-publish.

## Wave 4+ — Expand

Remaining agent IDs after Waves 1–3 are testing-green. Prefer depth over coverage.

## Status ladder

`declared` → `implementation` → `testing` → `active`  
No `active` without evidence under `docs/improvement/evidence/`.
