#!/usr/bin/env python3
"""Generate agent completeness matrix (Track B1)."""
from __future__ import annotations
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    reg = (ROOT / "agents" / "registry.yaml").read_text()
    skill_impl = {p.stem for p in (ROOT / "skills" / "implementations").glob("SK*.yaml")}
    packs = {p.stem for p in (ROOT / "knowledge" / "packs").glob("KP*.md")}
    lines = ['version: "1.0"', "standard: STD-02/v2", "agents:"]
    for m in re.finditer(r"\{id: (A\d+), name: ([^,]+), version: \"[^\"]+\", status: (\w+),.*?skills: \[([^\]]*)\], prompts: \[([^\]]*)\], knowledge: \[([^\]]*)\]", reg):
        aid, name, status, skills, prompts, knowledge = m.groups()
        sk = [x.strip() for x in skills.split(",") if x.strip()]
        pr = [x.strip() for x in prompts.split(",") if x.strip()]
        kp = [x.strip() for x in knowledge.split(",") if x.strip()]
        folder = (ROOT / "agents" / aid).is_dir()
        runtime = (ROOT / "backend" / "app" / "runtime" / f"{aid.lower()}.py").exists()
        sk_ok = all(s in skill_impl for s in sk) if sk else False
        kp_ok = all(k in packs for k in kp) if kp else True
        depth = "scaffold"
        if folder and runtime and sk_ok:
            depth = "implementation"
        lines += [f"  - id: {aid}", f"    name: {name}", f"    registry_status: {status}", f"    depth: {depth}", f"    folder: {str(folder).lower()}", f"    runtime: {str(runtime).lower()}", f"    skills_resolved: {str(sk_ok).lower()}", f"    knowledge_resolved: {str(kp_ok).lower()}", f"    skills: [{', '.join(sk)}]", f"    prompts: [{', '.join(pr)}]", f"    knowledge: [{', '.join(kp)}]"]
    out = ROOT / "docs" / "complete-automation-plan" / "AGENT-COMPLETENESS-MATRIX.yaml"
    out.write_text("\n".join(lines) + "\n")
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
