# AIOS CONFLICT REGISTER — PHASE 0

| Conflict domain | Current authority | Conflicting source class | Resolution |
|---|---|---|---|
| Implementation sequencing | v3.1 master plan | v2 granular plan | v2 is historical evidence; v3.1 governs future sequencing |
| CRM system of record | Odoo | older CRM references | Odoo is canonical; external CRMs may only support acquisition/integration |
| Business workflow engine | n8n | multiple automation/orchestration references | n8n is primary business workflow engine; specialized agent orchestration has explicit boundary |
| Vector store | Qdrant | multiple vector-store references | Qdrant is canonical |
| Runtime completion | repository evidence | blueprints/catalogues | files/catalogues do not imply runtime completion |
| Workspace knowledge | approved classified packs | raw exports | raw workspace material must be reconciled and approved before runtime use |
| Agent count | capability-oriented factory | one-agent-per-function lists | preserve stable IDs, but implement reusable skills/workflows and factory patterns |

## Phase-0 decision
No source is silently deleted. Historical/draft material remains traceable, but only the declared canonical source may govern implementation sequencing.
