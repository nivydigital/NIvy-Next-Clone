from __future__ import annotations
import json
from typing import Any
from .engine import RunResult, runtime_engine

class A025ForecastingError(RuntimeError): pass
REQUIRED = {"status","forecast_model","required_inputs","confidence_bands","review_process","variance_rules","confidence","assumptions","derived_from","warnings","errors","next_action"}

def _check(request: dict[str, Any]) -> None:
    for name in ("pipeline_deal_strategy", "revenue_operations_strategy"):
        if not isinstance(request.get(name), dict):
            raise A025ForecastingError(f"A025 requires {name} as an object")

async def run_a025_forecast(request: dict[str, Any]) -> RunResult:
    _check(request)
    context = {"pipeline_deal_strategy": request["pipeline_deal_strategy"], "revenue_operations_strategy": request["revenue_operations_strategy"], "historical_pipeline": request.get("historical_pipeline") or {}, "gtm_strategy": request.get("gtm_strategy") or {}, "forecast_constraints": request.get("forecast_constraints") or [], "output_schema": {"required": sorted(REQUIRED), "confidence_values": ["high", "medium", "low"]}}
    llm = await runtime_engine.run_llm("A025", "Define forecasting model, inputs and review process from the supplied pipeline and RevOps context. Return ONLY A025 JSON.", "PR031", context)
    if llm.status != "completed": return llm
    raw = llm.result.get("response") if isinstance(llm.result, dict) else llm.result
    try: output = json.loads(str(raw))
    except json.JSONDecodeError as exc: raise A025ForecastingError("A025 model did not return valid JSON") from exc
    output.setdefault("warnings", []); output.setdefault("errors", []); output.setdefault("next_action", "Pass forecasting strategy to finance and sales ops agents.")
    missing = REQUIRED - set(output)
    if missing: raise A025ForecastingError(f"A025 output missing required fields: {sorted(missing)}")
    if output.get("confidence") not in {"high", "medium", "low"}: raise A025ForecastingError("A025 confidence must be high, medium, or low")
    for f in ["required_inputs", "variance_rules", "assumptions", "derived_from"]:
        if not isinstance(output.get(f), list): raise A025ForecastingError(f"A025 {f} must be an array")
    for f in ["forecast_model", "confidence_bands", "review_process"]:
        if not isinstance(output.get(f), dict): raise A025ForecastingError(f"A025 {f} must be an object")
    return RunResult(llm.run_id, "A025", "forecasting.strategy+ollama", "completed", result=output)
