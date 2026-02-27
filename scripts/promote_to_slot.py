#!/usr/bin/env python3
from __future__ import annotations

import re
import os
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "intake"
BACKLOG = INTAKE / "backlog"
ROTATION = INTAKE / "rotation"
STATUS_FILE = ROTATION / "STATUS.md"
IDEAS_FILE = BACKLOG / "ideas.md"

SLOTS = ["SLOT-1", "SLOT-2", "SLOT-3"]
PRODUCT_TYPES = [
    "Playbook / SOP",
    "Template Library",
    "Decision Framework / Calculator",
    "Research Digest",
    "Course / System",
]


def load_text(path: Path, fallback: str = "") -> str:
    if not path.exists():
        return fallback
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def field_value(text: str, field: str) -> str:
    match = re.search(rf"^{re.escape(field)}:[ \t]*(.*)$", text, flags=re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip()


def set_field(text: str, field: str, value: str) -> str:
    pattern = rf"^{re.escape(field)}:[ \t]*.*$"
    replacement = f"{field}: {value}"
    if re.search(pattern, text, flags=re.MULTILINE):
        return re.sub(pattern, replacement, text, count=1, flags=re.MULTILINE)
    trailer = "" if text.endswith("\n") else "\n"
    return f"{text}{trailer}{field}: {value}\n"


def parse_metadata(raw_line: str) -> tuple[str, dict[str, str]]:
    body = re.sub(r"^\s*-\s+\[(?: |x|X)\]\s+", "", raw_line.strip())
    parts = [part.strip() for part in body.split("|")]
    idea_name = parts[0].strip()
    metadata: dict[str, str] = {}
    for part in parts[1:]:
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        metadata[key.strip().lower()] = value.strip()
    return idea_name, metadata


def find_open_slot() -> str | None:
    for slot in SLOTS:
        candidate_file = ROTATION / slot / "candidate.md"
        candidate_text = load_text(candidate_file)
        if not field_value(candidate_text, "Idea name"):
            return slot
    return None


def mark_line_done(line: str) -> str:
    return re.sub(r"^(\s*-\s+\[)\s(\]\s+)", r"\1x\2", line, count=1)


def toggle_type_checks(candidate_text: str, chosen_type: str) -> str:
    out = candidate_text
    for product_type in PRODUCT_TYPES:
        checked = "[x]" if product_type == chosen_type else "[ ]"
        out = re.sub(
            rf"^- \[(?: |x|X)\] {re.escape(product_type)}$",
            f"- {checked} {product_type}",
            out,
            flags=re.MULTILINE,
        )
    return out


def update_status(slot: str, idea_name: str) -> None:
    status_text = load_text(
        STATUS_FILE,
        fallback=(
            "# Discovery Rotation Status\n\n"
            "SLOT-1\nIdea:\nPhase:\nDay (X/7):\nRisk:\n\n"
            "SLOT-2\nIdea:\nPhase:\nDay (X/7):\nRisk:\n\n"
            "SLOT-3\nIdea:\nPhase:\nDay (X/7):\nRisk:\n"
        ),
    )
    lines = status_text.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        out.append(lines[i])
        if lines[i].strip() == slot:
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r"^SLOT-\d+$", lines[i].strip()):
                i += 1
            out.extend(
                [
                    f"Idea: {idea_name}",
                    "Phase: Phase 0 — Promoted",
                    "Day (X/7): 0/7",
                    "Risk: Awaiting money signal validation",
                ]
            )
            continue
        i += 1
    write_text(STATUS_FILE, "\n".join(out).rstrip() + "\n")


def main() -> int:
    open_slot = find_open_slot()
    if not open_slot:
        print("No open discovery slots. Resolve an active slot before promoting a new idea.")
        return 1

    ideas_text = load_text(IDEAS_FILE)
    if not ideas_text:
        print(f"No ideas file found at {IDEAS_FILE}.")
        return 1

    lines = ideas_text.splitlines()
    target_index = -1
    idea_name = ""
    metadata: dict[str, str] = {}
    for idx, line in enumerate(lines):
        if re.match(r"^\s*-\s+\[ \]\s+.+", line):
            target_index = idx
            idea_name, metadata = parse_metadata(line)
            break

    if target_index < 0 or not idea_name:
        print("No unchecked ideas to promote. Run: make intake:seed")
        return 1

    source = metadata.get("source", "Unknown")
    keyword = metadata.get("keyword", "")
    source_field = source if not keyword else f"{source} / {keyword}"
    product_type = metadata.get("type", "Playbook / SOP")
    if product_type not in PRODUCT_TYPES:
        product_type = "Playbook / SOP"

    today = date.today()
    deadline = today + timedelta(days=7)
    owner = os.getenv("USER", Path.home().name)

    candidate_file = ROTATION / open_slot / "candidate.md"
    candidate_text = load_text(candidate_file)
    candidate_text = set_field(candidate_text, "Idea name", idea_name)
    candidate_text = set_field(candidate_text, "Source (subreddit / keyword)", source_field)
    candidate_text = set_field(candidate_text, "Entered slot", today.isoformat())
    candidate_text = set_field(candidate_text, "Slot deadline (7 days max)", deadline.isoformat())
    candidate_text = set_field(candidate_text, "Owner", owner)
    candidate_text = toggle_type_checks(candidate_text, product_type)
    write_text(candidate_file, candidate_text)

    lines[target_index] = mark_line_done(lines[target_index])
    write_text(IDEAS_FILE, "\n".join(lines).rstrip() + "\n")

    update_status(open_slot, idea_name)

    print(f"Promoted idea to {open_slot}: {idea_name}")
    print(f"Type: {product_type}")
    print("Next: run `make intake:run SLOT=<slot>` to start discovery logs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
