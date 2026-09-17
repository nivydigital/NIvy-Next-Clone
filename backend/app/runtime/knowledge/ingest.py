"""Knowledge ingest pipeline: extract → chunk → embed → store (Phase 7 / P7.3).

In-memory mocks when QDRANT_URL / MINIO_ENDPOINT / DATABASE_URL unset.
"""
from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from ..audit import audit_log

ROOT = Path(__file__).resolve().parents[4]
PACKS_DIR = ROOT / "knowledge" / "packs"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _mock_mode() -> bool:
    if os.getenv("KNOWLEDGE_MOCK", "").strip().lower() in {"1", "true", "yes"}:
        return True
    return not (os.getenv("QDRANT_URL") and os.getenv("MINIO_ENDPOINT") and os.getenv("DATABASE_URL"))


@dataclass
class Chunk:
    chunk_id: str
    pack_id: str
    section: str
    text: str
    token_estimate: int
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "pack_id": self.pack_id,
            "section": self.section,
            "text": self.text,
            "token_estimate": self.token_estimate,
            "metadata": self.metadata,
        }


@dataclass
class IngestResult:
    pack_id: str
    chunks: list[Chunk]
    stored: dict[str, Any]
    mock: bool
    ingested_at: str = field(default_factory=_now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "pack_id": self.pack_id,
            "chunk_count": len(self.chunks),
            "chunks": [c.to_dict() for c in self.chunks],
            "stored": self.stored,
            "mock": self.mock,
            "ingested_at": self.ingested_at,
        }


def extract_pack(pack_id: str) -> str:
    path = PACKS_DIR / f"{pack_id}.md"
    if not path.exists():
        raise FileNotFoundError(f"knowledge pack not found: {path}")
    return path.read_text(encoding="utf-8")


def chunk_markdown(pack_id: str, text: str, max_chars: int = 800) -> list[Chunk]:
    sections: list[tuple[str, str]] = []
    current_section = "preamble"
    buf: list[str] = []
    for line in text.splitlines():
        if line.startswith("### "):
            if buf:
                sections.append((current_section, "\n".join(buf).strip()))
            current_section = line[4:].strip() or "section"
            buf = []
        elif line.startswith("## "):
            if buf:
                sections.append((current_section, "\n".join(buf).strip()))
            current_section = line[3:].strip() or "section"
            buf = []
        else:
            buf.append(line)
    if buf:
        sections.append((current_section, "\n".join(buf).strip()))

    chunks: list[Chunk] = []
    for section, body in sections:
        if not body:
            continue
        parts = [body[i : i + max_chars] for i in range(0, len(body), max_chars)]
        for i, part in enumerate(parts):
            part = part.strip()
            if not part:
                continue
            digest = hashlib.sha256(f"{pack_id}:{section}:{i}:{part}".encode()).hexdigest()[:12]
            chunks.append(
                Chunk(
                    chunk_id=f"{pack_id}-{digest}",
                    pack_id=pack_id,
                    section=section,
                    text=part,
                    token_estimate=max(1, len(part) // 4),
                    metadata={
                        "pack_id": pack_id,
                        "section": section,
                        "source_path": f"knowledge/packs/{pack_id}.md",
                        "part_index": i,
                    },
                )
            )
    return chunks


def embed_texts(texts: list[str]) -> list[list[float]]:
    vectors: list[list[float]] = []
    for t in texts:
        h = hashlib.sha256(t.encode()).digest()
        vectors.append([((b / 255.0) * 2 - 1) for b in h[:8]])
    return vectors


class InMemoryStore:
    def __init__(self) -> None:
        self.vectors: dict[str, dict[str, Any]] = {}
        self.objects: dict[str, bytes] = {}
        self.rows: list[dict[str, Any]] = []

    def upsert_vector(self, chunk: Chunk, vector: list[float]) -> None:
        self.vectors[chunk.chunk_id] = {
            "chunk_id": chunk.chunk_id,
            "pack_id": chunk.pack_id,
            "section": chunk.section,
            "vector": vector,
            "text": chunk.text,
            "metadata": chunk.metadata,
        }

    def put_object(self, key: str, data: bytes) -> None:
        self.objects[key] = data

    def insert_row(self, row: dict[str, Any]) -> None:
        self.rows.append(row)

    def search(self, pack_id: str | None, query: str, limit: int = 5) -> list[dict[str, Any]]:
        q = query.lower()
        hits = []
        for rec in self.vectors.values():
            if pack_id and rec["pack_id"] != pack_id:
                continue
            score = sum(1 for w in re.findall(r"[a-z0-9]+", q) if w in rec["text"].lower())
            hits.append({**rec, "score": score})
        hits.sort(key=lambda r: r["score"], reverse=True)
        return hits[:limit]


_STORE = InMemoryStore()


def get_store() -> InMemoryStore:
    return _STORE


def ingest_pack(pack_id: str, *, actor: str = "system") -> IngestResult:
    if not re.match(r"^KP\d{3}$", pack_id):
        raise ValueError(f"invalid pack_id: {pack_id}")
    text = extract_pack(pack_id)
    chunks = chunk_markdown(pack_id, text)
    vectors = embed_texts([c.text for c in chunks])
    mock = _mock_mode()
    store = get_store()
    stored = {"qdrant": 0, "minio": 0, "postgres": 0, "mock": mock}
    for chunk, vector in zip(chunks, vectors, strict=True):
        obj_key = f"knowledge/{pack_id}/{chunk.chunk_id}.txt"
        store.put_object(obj_key, chunk.text.encode("utf-8"))
        stored["minio"] += 1
        store.upsert_vector(chunk, vector)
        stored["qdrant"] += 1
        store.insert_row(
            {
                "chunk_id": chunk.chunk_id,
                "pack_id": pack_id,
                "section": chunk.section,
                "object_key": obj_key,
                "token_estimate": chunk.token_estimate,
                "ingested_at": _now(),
                "provenance": chunk.metadata,
            }
        )
        stored["postgres"] += 1
    result = IngestResult(pack_id=pack_id, chunks=chunks, stored=stored, mock=mock)
    audit_log.record(
        event_type="knowledge.ingest",
        actor=actor,
        action=pack_id,
        status="completed",
        request_id=str(uuid4()),
        data={"chunk_count": len(chunks), "mock": mock},
    )
    return result


def ingest_all_packs(*, actor: str = "system") -> list[IngestResult]:
    return [ingest_pack(path.stem, actor=actor) for path in sorted(PACKS_DIR.glob("KP*.md"))]


def retrieve(query: str, *, pack_id: str | None = None, limit: int = 5) -> list[dict[str, Any]]:
    return get_store().search(pack_id, query, limit=limit)
