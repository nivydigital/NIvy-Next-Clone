# AIOS SOURCE MAP — PHASE 0

**Authority:** `nivyindia/Raw-Repository`

| Source | Classification | AIOS destination | Rule |
|---|---|---|---|
| `Chats/ChatGPT/Multi Agent AIOS/Billion-Dreams-United-Implementation-Plan-v3-Master.md` | CANONICAL PLAN | `docs/plans/AIOS-FINAL-IMPLEMENTATION-PLAN-v3.1.md` | sequencing authority |
| `Chats/ChatGPT/Multi Agent AIOS/ARCHITECTURE_DECISIONS.md` | CANONICAL BASELINE | `docs/governance/` | preserve locked ADRs |
| `Chats/ChatGPT/Multi Agent AIOS/03-skills/registry.yaml` | SOURCE REGISTRY | `skills/registry.yaml` | adapt to implementation-grade schema |
| `Chats/ChatGPT/Multi Agent AIOS/Agent List.txt` | REUSE CATALOG | `research/reusable-assets/` + `agents/registry.yaml` | reuse/adapt; not proof of completion |
| `Chats/ChatGPT/Multi Agent AIOS/02-agents/AGENT_SKILL_MAPPING.md` | BINDING SOURCE | `knowledge/agent-bindings/` | canonical mapping candidate |
| `Chats/ChatGPT/Multi Agent AIOS/02-agents/AGENT_TOOL_MAPPING.md` | BINDING SOURCE | `knowledge/agent-bindings/` | canonical mapping candidate |
| `Chats/ChatGPT/Multi Agent AIOS/04-tools/TOOL_REGISTRY.yaml` | TOOL SOURCE | `tools/` | audit before runtime |
| `Chats/ChatGPT/Multi Agent AIOS/06-data/DATA_CATALOG.md` | DATA SOURCE | `data/` | reconcile with current schemas |
| `Chats/ChatGPT/Multi Agent AIOS/09-runtime/` | RUNTIME SOURCE | `core/` + `infrastructure/` | adapt, do not blindly copy |
| `external-solutions/business-structure-planning-ai-library/*` | REUSE RESEARCH | `research/reusable-assets/` | license/provenance required |
| Company OS / Notion / Claude exports | WORKSPACE SOURCE | `knowledge/` | classify, reconcile, approve before runtime |

## Reuse rule
`DISCOVER → CLASSIFY → AUDIT → ADAPT → REGISTER → TEST → GOVERN → INTEGRATE`

Raw material never becomes a runtime capability solely because a file exists.
