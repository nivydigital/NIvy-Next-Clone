"""Lead-outreach step → skill/prompt contracts (P2 / D1)."""
from __future__ import annotations

from typing import Any

from ..skill_resolver import SkillResolveError, run_skill

STEP_ORDER = ["discover", "enrich", "quality", "verify", "score", "research", "plan", "personalize", "draft"]

STEP_SKILL_MAP: dict[str, str] = {
    "discover": "SK034",
    "enrich": "SK036",
    "quality": "SK037",
    "verify": "SK038",
    "score": "SK039",
    "research": "SK041",
    "plan": "SK043",
    "personalize": "SK049",
    "draft": "SK044",
}

STEP_PROMPT_MAP: dict[str, str] = {
    "discover": "PR003",
    "enrich": "PR003",
    "quality": "PR003",
    "verify": "PR003",
    "score": "PR003",
    "research": "PR003",
    "plan": "PR002",
    "personalize": "PR004",
    "draft": "PR004",
}


def run_pipeline_steps(
    *,
    lead: dict[str, Any],
    campaign_id: str,
    dry_run: bool,
    actor: str,
    steps_completed: list[str],
    artifacts: dict[str, Any],
    mock_step,
) -> tuple[list[str], dict[str, Any], list[str]]:
    errors: list[str] = []
    for step in STEP_ORDER:
        if step in steps_completed:
            continue
        skill_id = STEP_SKILL_MAP.get(step)
        prompt_id = STEP_PROMPT_MAP.get(step)
        context = {
            "step": step,
            "lead": lead,
            "campaign_id": campaign_id,
            "prior_artifacts": {k: artifacts.get(k) for k in steps_completed},
            "prompt_id": prompt_id,
            "dry_run": dry_run,
        }
        if skill_id:
            try:
                skill_result = run_skill(skill_id, context=context, actor=actor, agent_id=None)
                skill_payload: dict[str, Any] = {
                    "skill_id": skill_id,
                    "prompt_id": prompt_id,
                    "skill_status": skill_result.status,
                    "skill_run_id": skill_result.run_id,
                    "result": skill_result.result,
                    "warnings": skill_result.warnings,
                    "errors": skill_result.errors,
                    "mode": "skill_contract",
                }
                if skill_result.status == "failed":
                    errors.extend(skill_result.errors or [f"{skill_id} failed"])
                    skill_payload["fallback"] = mock_step(step, lead, artifacts)
            except SkillResolveError as exc:
                skill_payload = {
                    "skill_id": skill_id,
                    "prompt_id": prompt_id,
                    "skill_status": "unresolved",
                    "error": str(exc),
                    "fallback": mock_step(step, lead, artifacts),
                    "mode": "mock_fallback",
                }
                errors.append(f"{step}:{exc}")
        else:
            skill_payload = {
                "skill_id": None,
                "prompt_id": prompt_id,
                "fallback": mock_step(step, lead, artifacts),
                "mode": "mock_only",
            }
        base = mock_step(step, lead, artifacts)
        if isinstance(base, dict):
            merged = dict(base)
            merged["skill"] = skill_payload
        else:
            merged = {"value": base, "skill": skill_payload}
        artifacts[step] = merged
        steps_completed.append(step)
    return steps_completed, artifacts, errors
