"""Phase 5 — Workflow orchestration (inbound/comms + generic runner)."""
from __future__ import annotations

from pathlib import Path
from typing import Any
from uuid import uuid4

import yaml

from .discovery import execute_agent
from .engine import ROOT, RuntimeDenied, runtime_engine

WORKFLOWS_DIR = ROOT / "workflows"


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise RuntimeDenied(f"workflow definition missing: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise RuntimeDenied(f"invalid workflow yaml: {path}")
    return data


def list_workflow_defs() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    if not WORKFLOWS_DIR.exists():
        return items
    for path in sorted(WORKFLOWS_DIR.rglob("workflow.yaml")):
        try:
            data = _load_yaml(path)
            items.append(
                {
                    "id": data.get("id") or path.parent.name,
                    "path": str(path.relative_to(ROOT)),
                    "version": data.get("version"),
                    "status": data.get("status"),
                    "trigger": data.get("trigger"),
                    "stages": [s.get("id") for s in (data.get("stages") or []) if isinstance(s, dict)],
                    "dry_run_default": data.get("dry_run_default", True),
                }
            )
        except Exception as exc:
            items.append({"path": str(path), "error": str(exc)})
    return items


def load_workflow(workflow_id: str) -> dict[str, Any]:
    # Prefer workflows/{id}/workflow.yaml
    path = WORKFLOWS_DIR / workflow_id / "workflow.yaml"
    if not path.exists():
        # search
        matches = list(WORKFLOWS_DIR.rglob("workflow.yaml"))
        for p in matches:
            data = _load_yaml(p)
            if data.get("id") == workflow_id:
                return data
        raise RuntimeDenied(f"unknown workflow: {workflow_id}")
    return _load_yaml(path)


def _get_path(data: dict[str, Any], dotted: str) -> Any:
    """Resolve $.a.b from a run context dict (leading $ optional)."""
    if not dotted.startswith("$"):
        return dotted
    parts = dotted.lstrip("$").lstrip(".").split(".")
    cur: Any = data
    for p in parts:
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur


def _map_inputs(input_map: dict[str, Any] | None, ctx: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, expr in (input_map or {}).items():
        if isinstance(expr, str) and expr.startswith("$"):
            out[key] = _get_path(ctx, expr)
        else:
            out[key] = expr
    return out


async def run_workflow(
    workflow_id: str,
    payload: dict[str, Any],
    *,
    dry_run: bool | None = None,
    stop_after_stage: str | None = None,
) -> dict[str, Any]:
    """
    Execute workflow stages in order.
    - Agent stages call execute_agent (structured).
    - type=gate / context_lookup are recorded only in dry_run or as stubs.
    - dry_run=True skips external side effects (default from workflow yaml).
    """
    wf = load_workflow(workflow_id)
    run_id = str(uuid4())
    if dry_run is None:
        dry_run = bool(wf.get("dry_run_default", True))

    ctx: dict[str, Any] = {
        "inbound": payload.get("inbound") or payload.get("email") or {},
        "input": payload.get("input") or payload,
        "outputs": {},
        "context": payload.get("context") or {},
    }
    # merge top-level convenience
    if "message" in payload and "message" not in ctx["inbound"]:
        ctx["inbound"]["message"] = payload["message"]

    state = "pending"
    history: list[dict[str, Any]] = []
    runtime_engine._record(
        event_type="workflow.started",
        actor="workflow",
        action=workflow_id,
        status="started",
        request_id=run_id,
        data={"dry_run": dry_run},
    )

    try:
        state = "running"
        for stage in wf.get("stages") or []:
            if not isinstance(stage, dict):
                continue
            stage_id = stage.get("id") or "stage"
            stage_type = stage.get("type") or "agent"

            entry: dict[str, Any] = {"stage_id": stage_id, "type": stage_type, "status": "started"}

            if stage_type == "context_lookup":
                # Stub: keep provided context
                ctx["outputs"][stage.get("output_key") or "context"] = ctx.get("context") or {}
                entry["status"] = "completed"
                entry["mode"] = "stub_context"
                history.append(entry)
                if stop_after_stage == stage_id:
                    break
                continue

            if stage_type == "gate":
                entry["status"] = "await_approval" if not dry_run else "skipped_dry_run"
                entry["policy"] = stage.get("policy")
                entry["mode"] = "gate"
                history.append(entry)
                if not dry_run:
                    state = "await_approval"
                    runtime_engine._record(
                        event_type="approval.requested",
                        actor="workflow",
                        action=workflow_id,
                        status="pending",
                        request_id=run_id,
                        data={"stage": stage_id, "policy": stage.get("policy")},
                    )
                    break
                if stop_after_stage == stage_id:
                    break
                continue

            # agent stage
            agent_id = stage.get("agent")
            if not agent_id:
                entry["status"] = "skipped"
                entry["reason"] = "no agent"
                history.append(entry)
                continue

            mapped = _map_inputs(stage.get("input_map"), ctx)
            # Ensure non-empty payload for agents that need objects
            if not mapped:
                mapped = {"request_id": run_id, "workflow_id": workflow_id, "stage_id": stage_id}
            mapped.setdefault("request_id", run_id)

            if dry_run:
                # Do not call LLM; record planned call
                result_stub = {
                    "status": "dry_run",
                    "agent_id": agent_id,
                    "planned_input_keys": sorted(mapped.keys()),
                    "message": f"dry_run: would execute {agent_id} for stage {stage_id}",
                }
                out_key = stage.get("output_key") or stage_id
                ctx["outputs"][out_key] = result_stub
                entry["status"] = "dry_run"
                entry["agent_id"] = agent_id
                entry["output_key"] = out_key
                history.append(entry)
            else:
                result = await execute_agent(agent_id, mapped, allow_llm_fallback=True)
                out_key = stage.get("output_key") or stage_id
                payload_out = result.result if hasattr(result, "result") else result
                ctx["outputs"][out_key] = payload_out
                entry["status"] = getattr(result, "status", "completed")
                entry["agent_id"] = agent_id
                entry["run_id"] = getattr(result, "run_id", None)
                entry["output_key"] = out_key
                history.append(entry)
                if entry["status"] == "failed":
                    state = "failed"
                    break

            runtime_engine._record(
                event_type="stage.completed",
                actor="workflow",
                action=f"{workflow_id}.{stage_id}",
                status=entry["status"],
                request_id=run_id,
                data={"agent_id": agent_id, "dry_run": dry_run},
            )
            if stop_after_stage == stage_id:
                break

        if state not in {"failed", "await_approval"}:
            state = "completed"

        runtime_engine._record(
            event_type="workflow.completed",
            actor="workflow",
            action=workflow_id,
            status=state,
            request_id=run_id,
            data={"dry_run": dry_run, "stages": len(history)},
        )

        return {
            "run_id": run_id,
            "workflow_id": workflow_id,
            "state": state,
            "dry_run": dry_run,
            "history": history,
            "outputs": ctx["outputs"],
        }
    except Exception as exc:
        runtime_engine._record(
            event_type="workflow.failed",
            actor="workflow",
            action=workflow_id,
            status="failed",
            request_id=run_id,
            data={"error": str(exc)},
        )
        return {
            "run_id": run_id,
            "workflow_id": workflow_id,
            "state": "failed",
            "dry_run": dry_run,
            "history": history,
            "error": str(exc),
            "outputs": ctx.get("outputs") or {},
        }
