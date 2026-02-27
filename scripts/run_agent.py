#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "intake"
BACKLOG = INTAKE / "backlog"
ROTATION = INTAKE / "rotation"
STATUS_FILE = ROTATION / "STATUS.md"

IDEAS_FILE = BACKLOG / "ideas.md"
NICHES_FILE = BACKLOG / "niches.md"

SEED_IDEAS = [
    {
        "name": "Freelancer scope-creep containment playbook",
        "source": "r/freelance",
        "keyword": "scope creep fixed bid",
        "type": "Playbook / SOP",
        "niche": "Solo service businesses",
    },
    {
        "name": "Client onboarding template kit for independent consultants",
        "source": "r/consulting",
        "keyword": "client onboarding checklist",
        "type": "Template Library",
        "niche": "Consulting operations",
    },
    {
        "name": "Statement-of-work risk gate for AI implementation projects",
        "source": "r/projectmanagement",
        "keyword": "SOW disputes deliverables",
        "type": "Decision Framework / Calculator",
        "niche": "AI services contracting",
    },
    {
        "name": "First-time manager 90-day feedback system",
        "source": "r/managers",
        "keyword": "new manager feedback cadence",
        "type": "Course / System",
        "niche": "Leadership transitions",
    },
    {
        "name": "Quarterly tax prep workflow for US freelancers",
        "source": "r/smallbusiness",
        "keyword": "quarterly taxes freelancer",
        "type": "Playbook / SOP",
        "niche": "Freelancer finance operations",
    },
]

def parse_kv_args(tokens: list[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for token in tokens:
        if "=" not in token:
            continue
        key, value = token.split("=", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def load_text(path: Path, fallback: str = "") -> str:
    if not path.exists():
        return fallback
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def existing_idea_names(ideas_text: str) -> set[str]:
    names: set[str] = set()
    for raw in ideas_text.splitlines():
        match = re.match(r"^\s*-\s+\[(?: |x|X)\]\s+(.+?)(?:\s+\|\s+.*)?\s*$", raw)
        if match:
            names.add(match.group(1).strip().lower())
    return names


def append_seed_ideas() -> int:
    ideas_text = load_text(
        IDEAS_FILE,
        fallback="# Idea Backlog\n\nUnscored observations only.\nNo analysis.\nNo commitment.\n",
    ).rstrip()
    niches_text = load_text(NICHES_FILE, fallback="# Niche Backlog\n").rstrip()
    if not niches_text:
        niches_text = "# Niche Backlog"
    elif not re.search(r"^#\s+Niche Backlog\b", niches_text, flags=re.MULTILINE):
        niches_text = "# Niche Backlog\n\n" + niches_text.lstrip()

    names = existing_idea_names(ideas_text)
    added = 0

    idea_lines: list[str] = []
    niche_lines: list[str] = []
    for entry in SEED_IDEAS:
        if entry["name"].lower() in names:
            continue
        idea_lines.append(
            f"- [ ] {entry['name']} | source={entry['source']} | "
            f"keyword={entry['keyword']} | type={entry['type']}"
        )
        niche_lines.append(f"- {entry['niche']}")
        added += 1

    if "## Intake Queue" not in ideas_text:
        ideas_text += "\n\n## Intake Queue"
    if idea_lines:
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        ideas_text += f"\n\n### Seeded {stamp}\n" + "\n".join(idea_lines)

    if "## Candidate Niches" not in niches_text:
        niches_text += "\n\n## Candidate Niches"
    known_niches = {line.strip().lower() for line in niches_text.splitlines() if line.startswith("- ")}
    deduped_niches = [line for line in niche_lines if line.strip().lower() not in known_niches]
    if deduped_niches:
        niches_text += "\n" + "\n".join(deduped_niches)

    write_text(IDEAS_FILE, ideas_text.rstrip() + "\n")
    write_text(NICHES_FILE, niches_text.rstrip() + "\n")
    return added


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


def update_slot_status(slot: str, idea_name: str, phase: str, risk: str) -> None:
    original = load_text(
        STATUS_FILE,
        fallback=(
            "# Discovery Rotation Status\n\n"
            "SLOT-1\nIdea:\nPhase:\nDay (X/7):\nRisk:\n\n"
            "SLOT-2\nIdea:\nPhase:\nDay (X/7):\nRisk:\n\n"
            "SLOT-3\nIdea:\nPhase:\nDay (X/7):\nRisk:\n"
        ),
    )
    lines = original.splitlines()
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
                    f"Phase: {phase}",
                    "Day (X/7): 1/7",
                    f"Risk: {risk}",
                ]
            )
            continue
        i += 1
    write_text(STATUS_FILE, "\n".join(out).rstrip() + "\n")


def run_knowledge_discovery(slot: str) -> int:
    slot_dir = ROTATION / slot
    if not slot_dir.exists():
        print(f"Unknown slot: {slot}")
        return 2

    candidate_file = slot_dir / "candidate.md"
    candidate_text = load_text(candidate_file)
    idea_name = field_value(candidate_text, "Idea name")
    source = field_value(candidate_text, "Source (subreddit / keyword)")

    if not idea_name:
        print(f"{slot} has no promoted idea yet. Run: make intake:promote")
        return 1

    money_signals_file = slot_dir / "money_signals.md"
    money_text = load_text(money_signals_file)
    now_stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    today = date.today().isoformat()

    started_value = field_value(money_text, "Started") or now_stamp
    money_text = set_field(money_text, "Started", started_value)
    money_text = set_field(money_text, "Stopped", "")
    money_text = set_field(money_text, "Time spent", "0h 00m")
    subreddit_value = field_value(money_text, "Subreddit")
    if source:
        subreddit_value = source.split(" / ", 1)[0].strip()
    if subreddit_value:
        money_text = set_field(money_text, "Subreddit", subreddit_value)
    write_text(money_signals_file, money_text)

    pain_file = slot_dir / "pain_analysis.md"
    pain_text = load_text(pain_file)
    if not field_value(pain_text, "Started"):
        pain_text = set_field(pain_text, "Started", "")
    if not field_value(pain_text, "Stopped"):
        pain_text = set_field(pain_text, "Stopped", "")
    if not field_value(pain_text, "Time spent"):
        pain_text = set_field(pain_text, "Time spent", "")
    write_text(pain_file, pain_text)

    update_slot_status(
        slot=slot,
        idea_name=idea_name,
        phase="Phase 1 — Money Signals",
        risk="Needs >=3 dollar-denominated spending signals",
    )

    decision_file = slot_dir / "decision.md"
    decision_text = load_text(decision_file)
    decision_text = set_field(decision_text, "Date", today)
    write_text(decision_file, decision_text)

    print(f"Discovery started for {slot}: {idea_name}")
    print("Next: collect >=3 spending signals with dollar amounts in money_signals.md")
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/run_agent.py <agent_name> [KEY=VALUE ...]")
        return 2

    agent_name = sys.argv[1]
    options = parse_kv_args(sys.argv[2:])

    if agent_name == "knowledge_niche_generator":
        added = append_seed_ideas()
        print(f"Seeded intake backlog with {added} new idea(s).")
        print(f"Ideas file: {IDEAS_FILE}")
        print(f"Niches file: {NICHES_FILE}")
        return 0

    if agent_name == "knowledge_discovery":
        slot = options.get("SLOT", "SLOT-1")
        return run_knowledge_discovery(slot)

    print(f"Unknown agent: {agent_name}")
    print("Supported agents: knowledge_niche_generator, knowledge_discovery")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
