#!/usr/bin/env python3
"""Phase 2 / P2.4 — Align prompt variables to registry and agent references.

Exit codes:
  0 = all checks passed
  1 = one or more alignment failures
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_registry_prompts() -> dict[str, set[str]]:
    text = (ROOT / "prompts" / "registry.yaml").read_text()
    out: dict[str, set[str]] = {}
    for m in re.finditer(
        r'\{id: (PR\d+), name: [^,]+, version: "[^"]+", status: \w+, owner: [^,]+, category: \w+, model_compatibility: \[[^\]]*\], variables: \[([^\]]*)\]',
        text,
    ):
        pid = m.group(1)
        vars_ = {v.strip() for v in m.group(2).split(",") if v.strip()}
        out[pid] = vars_
    return out


def load_executable_variables() -> dict[str, set[str]]:
    text = (ROOT / "prompts" / "executable.yaml").read_text()
    out: dict[str, set[str]] = {}
    current = None
    for line in text.splitlines():
        m = re.match(r"  (PR\d+):", line)
        if m:
            current = m.group(1)
            out.setdefault(current, set())
            continue
        if current and "variables:" in line:
            vm = re.search(r"variables: \[([^\]]*)\]", line)
            if vm:
                out[current] |= {v.strip() for v in vm.group(1).split(",") if v.strip()}
    return out


def load_agent_prompt_refs() -> dict[str, list[str]]:
    text = (ROOT / "agents" / "registry.yaml").read_text()
    refs: dict[str, list[str]] = {}
    for m in re.finditer(r"\{id: (A\d+),.*?prompts: \[([^\]]*)\]", text):
        aid = m.group(1)
        plist = [p.strip() for p in m.group(2).split(",") if p.strip()]
        refs[aid] = plist
    return refs


def main() -> int:
    errors: list[str] = []
    reg = load_registry_prompts()
    exe = load_executable_variables()
    agents = load_agent_prompt_refs()

    for i in range(1, 9):
        pid = f"PR{i:03d}"
        body = ROOT / "prompts" / "bodies" / f"{pid}.md"
        if not body.exists():
            errors.append(f"missing body file: prompts/bodies/{pid}.md")
        if pid not in exe:
            errors.append(f"missing executable entry: {pid}")
        if pid not in reg:
            errors.append(f"missing registry entry: {pid}")
        elif pid in exe:
            if reg[pid] - exe[pid]:
                errors.append(f"{pid}: registry vars not in executable: {sorted(reg[pid] - exe[pid])}")

    known = set(reg) | set(exe) | {f"PR{i:03d}" for i in range(1, 12)}
    for aid, plist in agents.items():
        if not plist:
            errors.append(f"{aid}: no prompts declared")
            continue
        for p in plist:
            if p not in known:
                errors.append(f"{aid}: references unknown prompt {p}")

    for i in range(1, 9):
        if not (ROOT / "prompts" / "bodies" / f"PR{i:03d}.md").exists():
            errors.append(f"body missing PR{i:03d}.md")

    if errors:
        print("FAIL — prompt schema alignment issues:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("OK — prompt schema alignment")
    print(f"  registry prompts: {len(reg)}")
    print(f"  executable prompts: {len(exe)}")
    print(f"  agents mapped: {len(agents)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
