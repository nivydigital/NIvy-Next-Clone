"""Phase 7 — knowledge packs, ingest pipeline, memory policy contracts."""
from __future__ import annotations

import os
from pathlib import Path

os.environ["KNOWLEDGE_MOCK"] = "1"

from backend.app.runtime.knowledge.ingest import (
    chunk_markdown,
    extract_pack,
    ingest_all_packs,
    ingest_pack,
    retrieve,
)

ROOT = Path(__file__).resolve().parents[2]


def test_all_packs_present():
    for i in range(1, 9):
        pid = f"KP{i:03d}"
        assert (ROOT / "knowledge" / "packs" / f"{pid}.md").exists()
        text = extract_pack(pid)
        assert "Summary" in text or pid in text


def test_chunk_and_ingest_kp004():
    result = ingest_pack("KP004", actor="test")
    assert result.pack_id == "KP004"
    assert result.mock is True
    assert len(result.chunks) >= 1
    assert result.stored["qdrant"] == len(result.chunks)


def test_ingest_all_and_retrieve():
    results = ingest_all_packs(actor="test")
    assert len(results) >= 8
    hits = retrieve("ideal customer profile buyer signals", pack_id="KP004", limit=3)
    assert isinstance(hits, list)


def test_chunk_markdown_sections():
    text = "# T\n\n## Summary\n\nHello world.\n\n### icp\n\nBuyer signals here.\n"
    chunks = chunk_markdown("KP999", text)
    assert len(chunks) >= 1


def test_memory_policy_file_exists():
    assert (ROOT / "memory" / "policy.yaml").exists()
    assert (ROOT / "memory" / "registry.yaml").exists()
