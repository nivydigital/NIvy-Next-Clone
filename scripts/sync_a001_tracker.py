from pathlib import Path

TRACKER = Path("docs/agent-implementation-plan/AGENT-PROGRESS-TRACKER.md")

# A001 remains blocked only by live G12/G19 evidence; this row must never mark G20 complete early.
NEW_ROW = "| A001 | Market Research | INTEGRATION | ☑ | ☑ | ☑ | ☑ | ☑ | ☑ | ☑ | ☑ | ☑ | ☑ | ☑ | ☑ | ◐ | ☑ | ☑ | ☑ | ☑ | ☑ | ☑ | ◐ | ☐ | CI #72 passed; deterministic evaluation 5/5 (100%); G12/G19 live runtime evidence pending; A002 remains BLOCKED. |"


def main() -> None:
    text = TRACKER.read_text(encoding="utf-8")
    lines = text.splitlines()
    matches = [i for i, line in enumerate(lines) if line.startswith("| A001 |")]
    if len(matches) != 1:
        raise SystemExit(f"Expected exactly one A001 row, found {len(matches)}")
    lines[matches[0]] = NEW_ROW
    updated = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    if updated != text:
        TRACKER.write_text(updated, encoding="utf-8")
        print("A001 tracker row updated")
    else:
        print("A001 tracker row already current")


if __name__ == "__main__":
    main()
