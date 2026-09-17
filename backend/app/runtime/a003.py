from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A003BuyerPersonaError(RuntimeError): pass

REQUIRED = {"status","personas","evidence","assumptions","confidence","derived_from","warnings","errors","next_action"}

def _prov(items: Any) -> bool:
    return isinstance(items, list) and bool(items) and all(isinstance(x, dict) and (x.get("url") or x.get("source_url") or x.get("provenance")) for x in items)

async def run_a003_persona(request: dict[str, Any]) -> RunResult:
    icp = request.get("icp_definition")
    if not isinstance(icp, dict): raise A003BuyerPersonaError("A003 requires icp_definition as an object")
    evidence = request.get("market_research", {}).get("evidence", []) if isinstance(request.get("market_research"), dict) else []
    if evidence and not _prov(evidence): raise A003BuyerPersonaError("A003 supplied market evidence contains missing provenance")
    context = {"icp_definition": icp, "market_research": request.get("market_research") or {}, "business_offer": request.get("business_offer") or {}, "customer_interviews": request.get("customer_interviews") or [], "exclusions": request.get("exclusions") or [], "output_schema":{"required":sorted(REQUIRED)}}
    llm = await runtime_engine.run_llm("A003", "Build evidence-backed buyer personas from the supplied ICP and approved context. Return ONLY A003 JSON.", "PR009", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A003BuyerPersonaError("A003 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass validated personas to messaging and qualification agents.")
    missing = REQUIRED - set(output)
    if missing: raise A003BuyerPersonaError(f"A003 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high","medium","low"}: raise A003BuyerPersonaError("A003 confidence must be high, medium, or low")
    if not isinstance(output.get("personas"), list): raise A003BuyerPersonaError("A003 personas must be an array")
    return RunResult(llm.run_id, "A003", "buyer.persona+ollama", "completed", result=output)
