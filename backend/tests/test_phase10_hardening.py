"""Phase 10 hardening contracts."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_env_example_exists():
    p = ROOT / ".env.example"
    assert p.exists()
    text = p.read_text()
    assert "POSTGRES_PASSWORD" in text
    assert "sk-" not in text


def test_ops_artifacts_exist():
    assert (ROOT / "ops" / "secrets" / "SECRETS-POLICY.md").exists()
    assert (ROOT / "scripts" / "check_no_secrets_in_git.py").exists()
    assert (ROOT / "scripts" / "backup_postgres.sh").exists()
    assert (ROOT / "scripts" / "restore_postgres.sh").exists()
    assert (ROOT / "ops" / "checklists" / "PRODUCTION-ACTIVATION.md").exists()
    assert (ROOT / "ops" / "observability" / "dashboard-spec.yaml").exists()


def test_secret_scanner_runs_clean():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_no_secrets_in_git.py")],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "OK" in proc.stdout


def test_observability_summary():
    from backend.app.runtime.observability import audit_summary, health_snapshot
    from backend.app.runtime.audit import audit_log

    audit_log.record(event_type="tool.execution", actor="test", action="phase10", status="completed", data={})
    assert audit_summary()["total_events"] >= 1
    assert health_snapshot(checks={"postgres": True})["ok"] is True
