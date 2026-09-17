# Agent Specification & Implementation Checklist v1.0

Use this checklist for **every agent**, without exception.

## A. Discovery & reuse
- [ ] Internal Raw-Repository search completed
- [ ] Existing AIOS assets searched
- [ ] External/open-source search completed where useful
- [ ] Ready-made agent candidates inspected, not just listed
- [ ] License/terms checked
- [ ] Security/privacy reviewed
- [ ] Dependencies/integration requirements reviewed
- [ ] Reuse/adapt/build-missing decision recorded
- [ ] Provenance recorded

## B. Identity & purpose
- [ ] Stable ID/name/version
- [ ] Owner
- [ ] Lifecycle status
- [ ] Objective/business outcome
- [ ] Scope
- [ ] Non-goals
- [ ] Escalation conditions
- [ ] Success/failure criteria

## C. Inputs
- [ ] Required fields and types
- [ ] Optional fields and types
- [ ] Source-of-truth identified
- [ ] Freshness requirements
- [ ] Tenant/company scope
- [ ] Validation rules
- [ ] Ambiguity handling
- [ ] Missing-data behavior

## D. Capabilities
- [ ] Every skill ID exists
- [ ] Every skill has implementation definition
- [ ] Every prompt ID exists
- [ ] Every prompt has executable body
- [ ] Variables/output format defined
- [ ] Knowledge packs exist
- [ ] Retrieval/access/freshness/conflict rules defined
- [ ] Memory read/write/retention policy defined
- [ ] Model policy defined
- [ ] Every tool exists and is authorized

## E. Workflow
- [ ] Trigger defined
- [ ] Steps defined
- [ ] Decision points defined
- [ ] States/transitions defined where applicable
- [ ] Handoffs/delegation defined
- [ ] Idempotency defined
- [ ] Retry policy defined
- [ ] Timeout/cancellation defined
- [ ] Failure/dead-letter path defined

## F. Governance & safety
- [ ] Least-privilege permissions
- [ ] Side effects classified
- [ ] Approval path for protected effects
- [ ] PII/data handling policy
- [ ] Consent/contact policy where applicable
- [ ] Prompt injection/tool abuse defenses
- [ ] Data egress restrictions
- [ ] Secrets excluded from prompts/logs
- [ ] Fail-closed behavior

## G. Outputs
- [ ] Structured output schema
- [ ] Status
- [ ] Result
- [ ] Actions taken
- [ ] Records changed
- [ ] Evidence
- [ ] Warnings/errors
- [ ] Confidence/quality indicator where appropriate
- [ ] Next action/handoff

## H. Verification & observability
- [ ] Explicit postconditions
- [ ] Authoritative-system verification
- [ ] Side-effect verification where applicable
- [ ] Duplicate/idempotency verification
- [ ] Run/task/correlation IDs
- [ ] Tool-call audit
- [ ] Approval audit
- [ ] Error/retry telemetry
- [ ] Cost/latency telemetry where available

## I. Evaluation
- [ ] Unit tests
- [ ] Positive golden cases
- [ ] Negative cases
- [ ] Policy/security tests
- [ ] Tool-call tests
- [ ] Workflow tests
- [ ] Integration tests
- [ ] Postcondition tests
- [ ] Regression tests
- [ ] Acceptance threshold recorded
- [ ] Evidence path recorded

## J. Release
- [ ] No critical unresolved defect
- [ ] Provenance/license complete
- [ ] Commit recorded
- [ ] Verification report recorded
- [ ] Known limitations recorded
- [ ] Rollback/deprecation path recorded
- [ ] Status changed to COMPLETE only after all required evidence
- [ ] ACTIVE only after runtime activation policy passes

**Rule:** one unchecked mandatory item means the agent is not COMPLETE.
