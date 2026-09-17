# Reuse & Existing-Solution Discovery Protocol v1.0

## Purpose

Prevent unnecessary custom development. Every agent must first determine whether a usable implementation already exists.

## Search order

1. Current AIOS repository
2. `nivyindia/Raw-Repository`
3. GitHub/open-source repositories
4. Official vendor/tool documentation and workflow libraries
5. Other reputable public sources
6. Commercial solutions only when they provide a materially useful capability

## Search targets

Search separately for:

- complete agents
- agent templates
- skills
- prompts
- system prompts
- workflows
- n8n templates
- MCP servers/connectors
- APIs
- tools
- knowledge bases/playbooks
- SOPs/templates
- evaluation datasets/evaluators
- observability/testing utilities

## Candidate evaluation

Score is **not** used to rank political or other unrelated choices; for engineering reuse, use explicit technical decision criteria rather than a generic quality score. Record:

- functional coverage
- implementation maturity/evidence
- license compatibility
- maintenance/freshness
- security/privacy
- dependencies
- model/provider lock-in
- integration fit
- data requirements
- cost
- performance/latency
- test/evaluation evidence
- customization effort
- operational risk

The record must state why the candidate is accepted, adapted, rejected, or deferred.

## Adaptation rules

A reused asset may be:

- imported unchanged when compatible;
- wrapped with an AIOS adapter;
- modified while preserving upstream provenance;
- decomposed into reusable skills/prompts/workflows;
- rejected when security, license, quality, dependency or compatibility requirements are not met.

Never copy external code or prompts without retaining source and license/terms information.

## Raw-Repository priority

The Raw-Repository already contains relevant AIOS agent lists, agent/skill mappings, open-source agent reference maps, skill registries, tool registries, execution contracts, sales/marketing workflows and playbooks. These are source material, not automatically canonical runtime truth. Inspect and reconcile them before reuse.

## Required reuse record

Each agent's implementation record must contain:

`candidate → source → evidence → license → compatibility → security review → reuse/adapt/reject decision → modifications → resulting AIOS asset`

## Stop condition

Do not start custom implementation until the discovery gate has either found a reusable solution or documented sufficient evidence that no suitable existing solution was found for the missing capability.
