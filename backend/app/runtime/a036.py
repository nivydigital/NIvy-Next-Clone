from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A036LeadEnrichmentError(RuntimeError): pass
REQUIRED = {"status","enriched_records","fields_added","sources","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("discovered_leads"), dict):
        raise A036LeadEnrichmentError("A036 requires discovered_leads as an object")

async def run_a036_lead_enrichment(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"discovered_leads": request["discovered_leads"], "discovered_contacts": request.get("discovered_contacts") or {}, "enrichment_fields": request.get("enrichment_fields") or [], "enrichment_constraints": request.get("enrichment_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A036", "Enrich leads and contacts with firmographic and contextual attributes from public sources. Return ONLY A036 JSON.", "PR003", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A036LeadEnrichmentError("A036 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass enriched leads to Data Quality (A037).")
    missing = REQUIRED - set(output)
    if missing: raise A036LeadEnrichmentError(f"A036 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A036LeadEnrichmentError("A036 confidence must be high, medium, or low")
    for f in ["enriched_records", "fields_added", "sources", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A036LeadEnrichmentError(f"A036 {f} must be an array")
    return RunResult(llm.run_id, "A036", "lead.enrichment+ollama", "completed", result=output)
