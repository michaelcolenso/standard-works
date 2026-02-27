#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "intake"
ROTATION = INTAKE / "rotation"

SLOTS = ["SLOT-1", "SLOT-2", "SLOT-3"]

def field_value(text: str, field: str) -> str:
    match = re.search(rf"^{re.escape(field)}:[ \t]*(.*)$", text, flags=re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip()

def slot_status(slot):
    path = ROTATION / slot
    candidate = path / "candidate.md"
    decision = path / "decision.md"

    if not path.exists() or not candidate.exists():
        return "EMPTY"

    text = candidate.read_text(encoding="utf-8", errors="ignore")
    idea_name = field_value(text, "Idea name")
    if not idea_name:
        return "EMPTY"

    if decision.exists():
        d = decision.read_text(encoding="utf-8", errors="ignore")
        decision_value = field_value(d, "Decision").lower()
        if decision_value in {"admit", "reject", "park"}:
            return "DECIDED"

    return "IN PROGRESS"

def main():
    print("\nDiscovery Slots:\n")
    open_slots = 0

    for s in SLOTS:
        status = slot_status(s)
        print(f"  {s}: {status}")
        if status == "EMPTY":
            open_slots += 1

    print("\nNext Actions:\n")

    if open_slots > 0:
        print("• Promote an idea from intake/backlog/ideas.md into an open slot")
        print("• Or run Phase 0 niche discovery")
        print("\nSuggested commands:")
        print("  make intake:seed")
        print("  make intake:promote")
    else:
        print("• No open discovery slots")
        print("• Complete or terminate an active slot")

if __name__ == "__main__":
    main()
