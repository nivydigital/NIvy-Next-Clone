from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A004CompetitorError(RuntimeError): pass
REQUIRED={"status","competitors","comparison","positioning","gaps","evidence","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _evidence(req: dict[str,Any]) -> list:
    mr=req.get("market_research")
    if not isinstance(mr,dict): raise A004CompetitorError("A004 requires market_research as an object")
    evidence=mr.get("evidence") or mr.get("sources") or []
    if not isinstance(evidence,list) or not evidence: raise A004CompetitorError("A004 requires market research evidence")
    if any(not isinstance(x,dict) or not (x.get("url") or x.get("source_url") or x.get("provenance")) for x in evidence): raise A004CompetitorError("A004 evidence items missing provenance")
    return evidence

async def run_a004_competitor(request:dict[str,Any])->RunResult:
    evidence=_evidence(request)
    context={"market_research":request["market_research"],"icp_definition":request.get("icp_definition") or {},"business_offer":request.get("business_offer") or {},"competitor_set":request.get("competitor_set") or [],"geography":request.get("geography"),"approved_evidence":evidence,"output_schema":{"required":sorted(REQUIRED),"confidence_values":["high","medium","low"]}}
    llm=await runtime_engine.run_llm("A004","Build source-traceable competitor intelligence from supplied approved evidence. Return ONLY A004 JSON.","PR010",context)
    if llm.status!="completed": return llm
    raw=llm.result.get("response") if isinstance(llm.result,dict) else llm.result
    try: output=json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A004CompetitorError("A004 model did not return valid JSON") from exc
    output.setdefault("warnings",[]); output.setdefault("errors",[]); output.setdefault("next_action","Pass competitor intelligence to channel, offer and messaging strategy.")
    missing=REQUIRED-set(output)
    if missing: raise A004CompetitorError(f"A004 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high","medium","low"}: raise A004CompetitorError("A004 confidence must be high, medium, or low")
    for f in ["competitors","comparison","positioning","gaps","evidence","assumptions","derived_from"]:
        if not isinstance(output.get(f),list): raise A004CompetitorError(f"A004 {f} must be an array")
    return RunResult(llm.run_id,"A004","competitor.intelligence+ollama","completed",result=output)
