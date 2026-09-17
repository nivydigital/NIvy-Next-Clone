from pathlib import Path

import yaml

from app.runtime.engine import RuntimeEngine

ROOT = Path(__file__).resolve().parents[2]


def test_executable_prompt_library_is_complete():
    data = yaml.safe_load((ROOT / "prompts" / "executable.yaml").read_text(encoding="utf-8"))
    assert set(data["prompts"]) >= {f"PR{i:03d}" for i in range(1, 9)}
    for prompt in data["prompts"].values():
        assert prompt.get("body", "").strip()
        assert prompt.get("variables")


def test_bound_agent_resolves_its_registered_prompt():
    engine = RuntimeEngine()
    prompt = engine.build_prompt("A044", "PR004", {"company": "Example", "offer": "Audit"}, None)
    assert "Email Outreach" in prompt
    assert "Example" in prompt


def test_wrong_prompt_is_denied():
    engine = RuntimeEngine()
    try:
        engine.build_prompt("A001", "PR004", {}, None)
    except Exception as exc:
        assert "not bound" in str(exc)
    else:
        raise AssertionError("unbound prompt was accepted")


def test_agent_without_raw_prompt_cannot_execute_without_registered_prompt():
    engine = RuntimeEngine()
    engine.prompt_library = {"common": {}, "prompts": {}}
    try:
        engine.build_prompt("A001", None, {}, None)
    except Exception as exc:
        assert "executable prompt" in str(exc)
    else:
        raise AssertionError("missing executable prompt was accepted")
