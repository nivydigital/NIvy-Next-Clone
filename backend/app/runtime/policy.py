from __future__ import annotations
from dataclasses import dataclass

class PolicyDenied(PermissionError):
    pass

@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    requires_approval: bool
    reason: str

PROTECTED_TOOLS = {
    "email.send",
    "tool.email.send",
    "odoo.write",
    "tool.odoo.write",
    "crm.update",
    "tool.crm.update",
    "proposal.send",
    "tool.proposal.send",
    "lead.create",
    "tool.lead.create",
}

SAFE_TOOLS = {
    "ollama.generate",
    "tool.ollama.generate",
    "ollama",
    "lead.read",
    "tool.lead.read",
    "lead.qualify",
    "tool.lead.qualify",
    "audit.write",
    "tool.audit.write",
    "web.fetch",
    "tool.web.fetch",
    "browser.fetch",
    "web.crawl",
    "tool.web.crawl",
    "email.verify",
    "tool.email.verify",
    "reacher.verify",
    "verification.email",
}

def decide(*, tool_id: str, approved: bool = False, autonomous: bool = False) -> PolicyDecision:
    if tool_id in SAFE_TOOLS:
        return PolicyDecision(True, False, "safe tool")
    if tool_id in PROTECTED_TOOLS:
        if approved:
            return PolicyDecision(True, True, "explicit approval present")
        return PolicyDecision(False, True, "protected side effect requires approval")
    return PolicyDecision(False, False, "tool is not declared by runtime policy")

def enforce(*, tool_id: str, approved: bool = False, autonomous: bool = False) -> PolicyDecision:
    decision = decide(tool_id=tool_id, approved=approved, autonomous=autonomous)
    if not decision.allowed:
        raise PolicyDenied(decision.reason)
    return decision
