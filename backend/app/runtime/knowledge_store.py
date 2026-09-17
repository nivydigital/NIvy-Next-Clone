"""Knowledge pack store and retrieval (Improvement Plan WP-E / P3).

Default: mock in-memory index over knowledge/packs/*.md.
Live path gated by NIVY_KNOWLEDGE_STORE=live (not used in CI).
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PACKS_DIR = ROOT / "knowledge" / "packs"
REGISTRY_PATH = PACKS_DIR / "registry.yaml"


@dataclass
class PackChunk:
    pack_id: str
    section: str
    text: str
    access_policy: str = "internal"
    freshness: str | None = None


@dataclass
class RetrievalHit:
    pack_id: str
    section: str
    text: str
    score: float
    access_policy: str
    freshness: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "pack_id": self.pack_id,
            "section": self.section,
            "text": self.text[:2000],
            "score": round(self.score, 4),
            "access_policy": self.access_policy,
            "freshness": self.freshness,
        }


def _store_mode() -> str:
    mode = (os.environ.get("NIVY_KNOWLEDGE_STORE") or "mock").strip().lower()
    if mode not in {"mock", "live"}:
        return "mock"
    return mode


def _parse_pack_md(path: Path) -> list[PackChunk]:
    text = path.read_text(encoding="utf-8")
    pack_id = path.stem
    access = "internal"
    freshness = None
    m_access = re.search(r"\*\*Access:\*\*\s*(\S+)", text)
    if m_access:
        access = m_access.group(1).strip()
    m_fresh = re.search(r"\*\*Freshness:\*\*\s*(\S+)", text)
    if m_fresh:
        freshness = m_fresh.group(1).strip()

    chunks: list[PackChunk] = []
    sections = re.split(r"\n(?=### )", text)
    for block in sections:
        block = block.strip()
        if not block:
            continue
        if block.startswith("### "):
            lines = block.splitlines()
            section = lines[0].replace("### ", "", 1).strip()
            body = "\n".join(lines[1:]).strip()
        else:
            section = "summary"
            body = block
        if body:
            chunks.append(
                PackChunk(
                    pack_id=pack_id,
                    section=section,
                    text=body,
                    access_policy=access,
                    freshness=freshness,
                )
            )
    if not chunks:
        chunks.append(
            PackChunk(pack_id=pack_id, section="full", text=text, access_policy=access, freshness=freshness)
        )
    return chunks


class MockKnowledgeStore:
    """Keyword retrieval over committed pack markdown (CI-safe)."""

    def __init__(self) -> None:
        self._chunks: list[PackChunk] = []
        self.reload()

    def reload(self) -> None:
        self._chunks = []
        if not PACKS_DIR.exists():
            return
        for path in sorted(PACKS_DIR.glob("KP*.md")):
            self._chunks.extend(_parse_pack_md(path))

    def list_packs(self) -> list[str]:
        return sorted({c.pack_id for c in self._chunks})

    def retrieve(
        self,
        query: str,
        *,
        pack_ids: list[str] | None = None,
        allow_restricted: bool = False,
        top_k: int = 5,
    ) -> list[RetrievalHit]:
        q = (query or "").strip().lower()
        if not q:
            return []
        tokens = set(re.findall(r"[a-z0-9_]{2,}", q))
        hits: list[RetrievalHit] = []
        for c in self._chunks:
            if pack_ids and c.pack_id not in pack_ids:
                continue
            if c.access_policy == "restricted" and not allow_restricted:
                continue
            body_l = c.text.lower()
            sec_l = c.section.lower()
            score = 0.0
            for t in tokens:
                if t in sec_l:
                    score += 2.0
                if t in body_l:
                    score += 1.0 + min(body_l.count(t), 3) * 0.1
            if score > 0:
                hits.append(
                    RetrievalHit(
                        pack_id=c.pack_id,
                        section=c.section,
                        text=c.text,
                        score=score,
                        access_policy=c.access_policy,
                        freshness=c.freshness,
                    )
                )
        hits.sort(key=lambda h: h.score, reverse=True)
        return hits[: max(1, top_k)]


class LiveKnowledgeStore:
    """Placeholder live path — requires external vector store; falls back to mock behavior with flag check."""

    def __init__(self) -> None:
        # Live integration intentionally not active in default installs.
        self._mock = MockKnowledgeStore()

    def list_packs(self) -> list[str]:
        return self._mock.list_packs()

    def retrieve(self, query: str, **kwargs: Any) -> list[RetrievalHit]:
        # Future: query Qdrant/pgvector when NIVY_KNOWLEDGE_STORE=live and credentials set.
        return self._mock.retrieve(query, **kwargs)


_store: MockKnowledgeStore | LiveKnowledgeStore | None = None


def get_knowledge_store() -> MockKnowledgeStore | LiveKnowledgeStore:
    global _store
    if _store is None:
        if _store_mode() == "live":
            _store = LiveKnowledgeStore()
        else:
            _store = MockKnowledgeStore()
    return _store


def reset_knowledge_store() -> None:
    global _store
    _store = None


def retrieve_for_agent(
    query: str,
    *,
    agent_id: str | None = None,
    pack_ids: list[str] | None = None,
    allow_restricted: bool = False,
    top_k: int = 5,
) -> dict[str, Any]:
    """Single entry used by research/outreach agents."""
    store = get_knowledge_store()
    hits = store.retrieve(
        query,
        pack_ids=pack_ids,
        allow_restricted=allow_restricted,
        top_k=top_k,
    )
    return {
        "mode": _store_mode(),
        "agent_id": agent_id,
        "query": query,
        "hits": [h.to_dict() for h in hits],
        "count": len(hits),
    }
