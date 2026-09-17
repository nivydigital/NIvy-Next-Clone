"""Phase 7 knowledge pack and ingest tests."""
from __future__ import annotations

import os
from pathlib import Path

os.environ["KNOWLEDGE_MOCK"] = "1"

from backend.app.runtime.knowledge.ingest import chunk_markdown, extract_pack, ingest_all_packs, ingest_pack, retrieve

ROOT = Path(__file__).resolve().parents[2]


def test_all_packs_present():
    for i in range(1, 9):
        pid = f"KP{i:03d}"
        assert (ROOT / "knowledge" / "packs" / f"{pid}.md").exists()
        assert "Summary" in extract_pack(pid) or pid in extract_pack(pid)


def test_ingest_kp004():
    result = ingest_pack("KP004", actor="test")
    assert result.mock is True
    assert len(result.chunks) >= 1


def test_ingest_all():
    assert len(ingest_all_packs(actor="test")) >= 8
    assert isinstance(retrieve("buyer signals", pack_id="KP004"), list)


def test_chunk_markdown():
    assert len(chunk_markdown("KP999", "## Summary\n\nHello.\n\n### icp\n\nBuyers.\n")) >= 1


def test_memory_files():
    assert (ROOT / "memory" / "policy.yaml").exists()
