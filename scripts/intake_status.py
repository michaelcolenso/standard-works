#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "intake"
ROTATION = INTAKE / "rotation"

SLOTS = ["SLOT-1", "SLOT-2", "SLOT-3"]

def slot_status(slot):
    path = ROTATION / slot
    candidate = path / "candidate.md"
    decision = path / "decision.md"

    if not candidate.exists():
        return "EMPTY"

    text = candidate.read_text()
    if "Idea name:" in text and text.strip().endswith(""):
        return "IN USE"

    if decision.exists():
        d = decision.read_text()
        if "Admit" in d or "Reject" in d or "Park" in d:
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