from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A005ChannelStrategyError(RuntimeError): pass
REQUIRED={"status","channels","prioritization","channel_fit","experiments","constraints","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(req:dict[str,Any])->list:
    for name in ("market_research","icp_definition"):
        if not isinstance(req.get(name),dict): raise A005ChannelStrategyError(f"A005 requires {name} as an object")
    mr=req["market_research"]; evidence=mr.get("evidence") or mr.get("sources") or []
    if not isinstance(evidence,list) or not evidence: raise A005ChannelStrategyError("A005 requires market research evidence")
    if any(not isinstance(x,dict) or not (x.get("url") or x.get("source_url") or x.get("provenance")) for x in evidence): raise A005ChannelStrategyError("A005 evidence items missing provenance")
    return evidence

async def run_a005_channel(request:dict[str,Any])->RunResult:
    evidence=_check(request)
    context={"market_research":request["market_research"],"icp_definition":request["icp_definition"],"competitor_intelligence":request.get("competitor_intelligence") or {},"business_offer":request.get("business_offer") or {},"channel_constraints":request.get("channel_constraints") or [],"historical_performance":request.get("historical_performance") or [],"approved_evidence":evidence,"output_schema":{"required":sorted(REQUIRED),"confidence_values":["high","medium","low"]}}
    llm=await runtime_engine.run_llm("A005","Build an evidence-backed channel strategy from supplied context. Return ONLY A005 JSON.","PR011",context)
    if llm.status!="completed": return llm
    raw=llm.result.get("response") if isinstance(llm.result,dict) else llm.result
    try: output=json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A005ChannelStrategyError("A005 model did not return valid JSON") from exc
    output.setdefault("warnings",[]); output.setdefault("errors",[]); output.setdefault("next_action","Pass channel strategy to campaign and content planning agents.")
    missing=REQUIRED-set(output)
    if missing: raise A005ChannelStrategyError(f"A005 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high","medium","low"}: raise A005ChannelStrategyError("A005 confidence must be high, medium, or low")
    for f in ["channels","prioritization","channel_fit","experiments","constraints","assumptions","derived_from"]:
        if not isinstance(output.get(f),list): raise A005ChannelStrategyError(f"A005 {f} must be an array")
    return RunResult(llm.run_id,"A005","channel.strategy+ollama","completed",result=output)
