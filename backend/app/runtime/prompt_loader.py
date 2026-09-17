"""Prompt body loader (Improvement Plan WP-B1 / P0).

Loads executable prompt specs from prompts/executable.yaml and merges
markdown bodies from prompts/bodies/PR*.md when present.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[3]
EXECUTABLE_PATH = ROOT / "prompts" / "executable.yaml"
BODIES_DIR = ROOT / "prompts" / "bodies"


class PromptLoadError(RuntimeError):
    """Raised when a prompt cannot be loaded or is incomplete."""


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise PromptLoadError(f"invalid yaml structure: {path}")
    return data


def load_executable_index() -> dict[str, Any]:
    data = _read_yaml(EXECUTABLE_PATH)
    data.setdefault("common", {})
    data.setdefault("prompts", {})
    return data


def load_body_file(prompt_id: str) -> str | None:
    path = BODIES_DIR / f"{prompt_id}.md"
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8").strip()


def resolve_prompt(prompt_id: str, *, require_body: bool = True) -> dict[str, Any]:
    index = load_executable_index()
    prompts = index.get("prompts") or {}
    spec = prompts.get(prompt_id)
    if not isinstance(spec, dict):
        body = load_body_file(prompt_id)
        if body is None:
            raise PromptLoadError(f"unknown prompt: {prompt_id}")
        return {
            "id": prompt_id,
            "name": prompt_id,
            "body": body,
            "source": "bodies",
            "common": index.get("common") or {},
        }

    body_file = load_body_file(prompt_id)
    body = body_file if body_file else (spec.get("body") or "")
    if require_body and not str(body).strip():
        raise PromptLoadError(f"executable prompt body missing: {prompt_id}")

    merged = dict(spec)
    merged["id"] = prompt_id
    merged["body"] = body
    merged["source"] = "bodies" if body_file else "executable"
    merged["common"] = index.get("common") or {}
    return merged


def build_messages(
    prompt_id: str,
    *,
    agent_id: str,
    agent_name: str = "",
    context: dict[str, Any] | None = None,
    require_body: bool = True,
) -> str:
    import json

    resolved = resolve_prompt(prompt_id, require_body=require_body)
    common = resolved.get("common") or {}
    system = str(common.get("system") or "").strip()
    output = str(common.get("output") or "").strip()
    variable_text = json.dumps(context or {}, ensure_ascii=False, default=str)
    parts = []
    if system:
        parts.append(system)
    parts.append(f"AGENT: {agent_name or agent_id} ({agent_id})")
    parts.append(f"PROMPT_ID: {prompt_id}")
    parts.append(f"TASK CONTEXT:\n{variable_text}")
    parts.append(f"TASK INSTRUCTIONS:\n{resolved['body']}")
    if output:
        parts.append(output)
    return "\n\n".join(parts)


def list_available_prompts() -> list[str]:
    index = load_executable_index()
    ids = set((index.get("prompts") or {}).keys())
    if BODIES_DIR.exists():
        for p in BODIES_DIR.glob("PR*.md"):
            ids.add(p.stem)
    return sorted(ids)
