# Secrets Policy (Phase 10 / P10.1)

## Rules

1. **Never commit secrets to Git** — passwords, API keys, tokens, private keys, webhook secrets.
2. **Secrets live only in** environment variables or a secret store (production).
3. **Templates only in repo**: `.env.example` with empty or placeholder values.
4. **Default passwords in compose** (e.g. `change-me`) are development defaults only — production must override.
5. **Audit**: tool and workflow logs must redact secret-like keys.

## Production

- Inject secrets via orchestrator (K8s secrets, Docker secrets, or host env).
- Rotate credentials on schedule; revoke leaked keys immediately.
- `scripts/check_no_secrets_in_git.py` must pass in CI.
