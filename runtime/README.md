# AIOS Runtime

Executable control/runtime boundary for Nivy Next AIOS.

Goals:
- fail closed for undeclared agents/tools
- resolve declared capabilities
- require approval for protected side effects
- use environment-backed credentials only
- emit audit and evaluation records
- support local Ollama plus n8n/Odoo integrations

Registry declaration is not production activation. Runtime activation requires policy, dependencies, evaluation and health gates.