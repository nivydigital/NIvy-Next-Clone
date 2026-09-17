from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A094AnomalyError(RuntimeError): pass
REQUIRED = {"status","anomalies","severity","investigation_paths","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    if not isinstance(request.get("metric_series"), dict):
        raise A094AnomalyError("A094 requires metric_series as an object")

async def run_a094_anomaly(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"metric_series": request["metric_series"], "baselines": request.get("baselines") or {}, "detection_rules": request.get("detection_rules") or [], "analysis_constraints": request.get("analysis_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A094", "Detect anomalies and recommend investigation paths. Return ONLY A094 JSON.", "PR005", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A094AnomalyError("A094 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Route severe anomalies to Risk Analyst (A095) or ops owners.")
    missing = REQUIRED - set(output)
    if missing: raise A094AnomalyError(f"A094 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A094AnomalyError("A094 confidence must be high, medium, or low")
    for f in ["anomalies", "investigation_paths", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A094AnomalyError(f"A094 {f} must be an array")
    return RunResult(llm.run_id, "A094", "anomaly.detection+ollama", "completed", result=output)
