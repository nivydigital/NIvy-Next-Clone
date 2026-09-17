from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A070KnowledgeExtractError(RuntimeError): pass
REQUIRED = {"status","faqs","objection_handlers","playbook_snippets","tags","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("conversation_insights"), dict):
        raise A070KnowledgeExtractError("A070 requires conversation_insights as an object")

async def run_a070_knowledge_extract(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"conversation_insights": request["conversation_insights"], "meeting_intelligence": request.get("meeting_intelligence") or {}, "knowledge_constraints": request.get("knowledge_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A070", "Extract FAQs, objection handlers and playbook snippets. Return ONLY A070 JSON.", "PR003", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A070KnowledgeExtractError("A070 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Store knowledge extract in knowledge base for enablement agents.")
    missing = REQUIRED - set(output)
    if missing: raise A070KnowledgeExtractError(f"A070 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A070KnowledgeExtractError("A070 confidence must be high, medium, or low")
    for f in ["faqs", "objection_handlers", "playbook_snippets", "tags", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A070KnowledgeExtractError(f"A070 {f} must be an array")
    return RunResult(llm.run_id, "A070", "knowledge.extract+ollama", "completed", result=output)
