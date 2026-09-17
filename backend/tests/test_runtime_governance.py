from app.runtime.policy import decide
from app.runtime.engine import RuntimeEngine


def test_unknown_tool_is_denied():
    decision = decide(tool_id="not.declared")
    assert decision.allowed is False
    assert "not declared" in decision.reason


def test_protected_tool_requires_approval():
    decision = decide(tool_id="tool.email.send")
    assert decision.allowed is False
    assert decision.requires_approval is True
    assert decide(tool_id="tool.email.send", approved=True).allowed is True


def test_safe_llm_tool_is_allowed():
    assert decide(tool_id="tool.ollama.generate").allowed is True


def test_runtime_registry_binds_seeded_agents():
    engine = RuntimeEngine()
    assert "tool.ollama.generate" in engine._bound_tools(engine._agent("A001"))
    assert "tool.email.send" in engine._bound_tools(engine._agent("A044"))


def test_approval_is_agent_and_tool_scoped():
    engine = RuntimeEngine()
    approval = engine.request_approval("A044", "tool.email.send", "test")
    assert approval["status"] == "pending"
    engine.approve(approval["approval_id"])
    assert engine.approvals[approval["approval_id"]]["status"] == "approved"
