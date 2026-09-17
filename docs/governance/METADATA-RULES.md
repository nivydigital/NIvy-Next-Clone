# AIOS Governance Metadata Rules

All executable or reusable AIOS capabilities must be registered before runtime use.

## Minimum identity
Every asset needs a stable ID, name, version, lifecycle status, owner and provenance.

## Capability metadata
Agents, skills, prompts, tools and workflows additionally declare compatibility, permissions, dependencies, evaluation state, cost class and deprecation state.

## Evidence
`declared` means the contract exists. `testing` means validation is running. `active` requires verified runtime evidence. `production`/autonomous operation must never be inferred from documentation.

## Security
Assets that can access confidential/restricted data or create external side effects must declare those boundaries. Missing/ambiguous permission data fails closed.
