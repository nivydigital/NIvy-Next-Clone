"""Skill resolver (Improvement Plan WP-A3 / P0).

Loads STD-01 skill YAML, validates mandatory fields, runs structural procedure.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import uuid4

import yaml

from .audit import audit_log

ROOT = Path(__file__).resolve().parents[3]
IMPL_DIR = ROOT / "skills" / "implementations"

STD01_REQUIRED = [
    "id", "name", "version", "status", "objective", "non_goals", "inputs", "outputs",
    "procedure", "quality_checks", "failure_policy", "evidence_policy", "dependencies",
    "acceptance_criteria", "evaluation", "provenance",
]


class SkillResolveError(RuntimeError):
    pass


@dataclass
class SkillResult:
    skill_id: str
    status: str
    confidence: str
    result: dict[str, Any] = field(default_factory=dict)
    assumptions: list[str] = field(default_factory=list)
    derived_from: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    next_action: str | None = None
    procedure_log: list[dict[str, Any]] = field(default_factory=list)
    run_id: str = field(default_factory=lambda: str(uuid4()))

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "status": self.status,
            "confidence": self.confidence,
            "result": self.result,
            "assumptions": self.assumptions,
            "derived_from": self.derived_from,
            "warnings": self.warnings,
            "errors": self.errors,
            "next_action": self.next_action,
            "procedure_log": self.procedure_log,
            "run_id": self.run_id,
        }


def list_skill_ids() -> list[str]:
    if not IMPL_DIR.exists():
        return []
    return sorted(p.stem for p in IMPL_DIR.glob("SK*.yaml"))


def load_skill(skill_id: str) -> dict[str, Any]:
    if not skill_id.startswith("SK"):
        raise SkillResolveError(f"invalid skill id: {skill_id}")
    path = IMPL_DIR / f"{skill_id}.yaml"
    if not path.exists():
        raise SkillResolveError(f"skill implementation not found: {skill_id}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise SkillResolveError(f"invalid skill yaml: {skill_id}")
    missing = [k for k in STD01_REQUIRED if k not in data]
    if missing:
        raise SkillResolveError(f"{skill_id} missing STD-01 fields: {missing}")
    if data.get("id") != skill_id:
        raise SkillResolveError(f"skill id mismatch in file: {data.get('id')} != {skill_id}")
    return data


def resolve_agent_skills(skill_ids: list[str]) -> list[dict[str, Any]]:
    return [load_skill(sid) for sid in skill_ids]


def _validate_inputs(skill: dict[str, Any], context: dict[str, Any] | None) -> list[str]:
    errors: list[str] = []
    if context is None or not isinstance(context, dict):
        errors.append("context must be a non-empty object")
        return errors
    if not context:
        errors.append("context is empty")
    return errors


def run_skill(
    skill_id: str,
    *,
    context: dict[str, Any] | None = None,
    actor: str = "runtime",
    agent_id: str | None = None,
) -> SkillResult:
    skill = load_skill(skill_id)
    result = SkillResult(skill_id=skill_id, status="failed", confidence="low")
    ctx = context if isinstance(context, dict) else {}
    procedure = skill.get("procedure") or []
    if not isinstance(procedure, list) or len(procedure) < 1:
        result.errors.append("procedure missing or empty")
        audit_log.record(event_type="skill.run", actor=actor, action=skill_id, status="failed", request_id=result.run_id, data={"agent_id": agent_id, "errors": result.errors})
        return result

    for step in procedure:
        if not isinstance(step, dict):
            continue
        name = str(step.get("name") or step.get("action") or "step")
        on_failure = str(step.get("on_failure") or "fail_closed")
        entry: dict[str, Any] = {"step": step.get("step"), "name": name, "status": "ok"}

        if name in {"validate_inputs", "validate"}:
            errs = _validate_inputs(skill, ctx)
            if errs:
                entry["status"] = "failed"
                entry["errors"] = errs
                result.procedure_log.append(entry)
                result.errors.extend(errs)
                if on_failure == "fail_closed":
                    result.status = "failed"
                    result.next_action = "fix_inputs"
                    audit_log.record(event_type="skill.run", actor=actor, action=skill_id, status="failed", request_id=result.run_id, data={"agent_id": agent_id, "step": name, "errors": errs})
                    return result
            else:
                result.procedure_log.append(entry)
            continue

        if name in {"prepare_context", "prepare"}:
            deps = skill.get("dependencies") or {}
            tools = deps.get("tools") if isinstance(deps, dict) else []
            result.derived_from.append(f"skill:{skill_id}")
            if tools:
                result.assumptions.append(f"declared_tools={tools}")
            result.procedure_log.append(entry)
            continue

        if name in {"execute_core", "execute"}:
            result.result = {
                "objective": skill.get("objective"),
                "skill_id": skill_id,
                "category": skill.get("category"),
                "context_keys": sorted(ctx.keys()),
                "mode": "contract_execution",
            }
            result.procedure_log.append(entry)
            continue

        if name in {"quality_check", "quality"}:
            result.procedure_log.append(entry)
            continue

        if name in {"verify_outputs", "verify"}:
            if not result.result:
                entry["status"] = "failed"
                result.errors.append("result payload missing after execute_core")
                result.procedure_log.append(entry)
                if on_failure == "fail_closed":
                    result.status = "failed"
                    return result
            else:
                result.procedure_log.append(entry)
            continue

        if name in {"return_audit", "audit", "return"}:
            result.procedure_log.append(entry)
            continue

        entry["status"] = "skipped"
        result.warnings.append(f"unknown_step:{name}")
        result.procedure_log.append(entry)

    if result.errors and result.status != "failed":
        result.status = "partial"
        result.confidence = "low"
        result.next_action = "review_warnings"
    elif not result.errors:
        result.status = "completed"
        result.confidence = "medium"
        result.next_action = "continue"

    audit_log.record(
        event_type="skill.run",
        actor=actor,
        action=skill_id,
        status=result.status,
        request_id=result.run_id,
        data={"agent_id": agent_id, "confidence": result.confidence, "steps": len(result.procedure_log)},
    )
    return result
