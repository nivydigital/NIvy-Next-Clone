# Dependency Map — Complete Automation

## Layer stack (bottom → top)

```
Infrastructure (DB, queue, Ollama, MinIO, Qdrant)
    → Tools (registered adapters + audit)
        → Skills (procedures using tools)
            → Prompts (model instructions)
                → Agents (contracts + runtime)
                    → Workflows (multi-agent state machines)
                        → Products / Campaigns (business journeys)
                            → Evaluation & Governance
```

## Hard dependencies

| If you want… | You must first have… |
|--------------|----------------------|
| Agent `active` | Resolvable skills + prompt bodies + authorized tools + eval evidence |
| Email send in workflow | `tool.email.send` + approval gate + audit |
| Lead outreach E2E | A034–A052 scaffolds + tools + prompts + workflow state machine |
| RAG answers | Knowledge ingest + vector store + retrieval skill |
| COMPLETE badge on agent | TESTING-PLAN-DEFERRED pyramid passed |
| Production campaign | Dry-run E2E + secrets externalized + DoD release gates |

## Recommended build order (critical path)

1. Tools (mock-first)  
2. Prompt bodies PR001–PR008  
3. Skills for lead path  
4. Wire Agent→Skill→Tool in runtime  
5. Lead-outreach workflow dry-run  
6. Approval gate  
7. Finish agents A100–A108  
8. Execute deferred testing  
9. Enable live providers under policy  

## Parallelizable

- Agent scaffold A100–A108 (while tools/prompts in progress)
- Knowledge pack authoring
- Marketing workflow design (depends on A084–A091 scaffolds — already present)
- Test fixture generation from schemas

## Anti-patterns

- Marking agents COMPLETE without tests  
- Calling external APIs without registered tools  
- Inventing new agent IDs when registry already defines them  
- Building social publish before approval + tool audit exist  
