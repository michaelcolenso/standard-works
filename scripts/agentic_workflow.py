#!/usr/bin/env python3
"""Long-horizon workflow runner for knowledge products (ideation -> sale)."""
from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Milestone:
    name: str
    done_when: str
    owner_agent: str
    workstream: str
    validation: list[str]


MILESTONES = [
    Milestone(
        name="Ideation lock",
        done_when="A narrow buyer pain with spending proof is recorded in brief and intake notes.",
        owner_agent="market_analyst",
        workstream="00-brief",
        validation=[],
    ),
    Milestone(
        name="Research confidence",
        done_when="Contradictions, open questions, and insights are filled with source citations.",
        owner_agent="research_synthesizer",
        workstream="01-research",
        validation=[],
    ),
    Milestone(
        name="Architecture freeze",
        done_when="Promise, transformation map, outline, and guardrails define the product boundary.",
        owner_agent="knowledge_architect",
        workstream="02-architecture",
        validation=[],
    ),
    Milestone(
        name="Core draft complete",
        done_when="Core draft sections and draft log are complete for v1.0 packaging.",
        owner_agent="primary_author",
        workstream="03-drafts",
        validation=[],
    ),
    Milestone(
        name="Validation pass",
        done_when="Adversarial review findings are resolved or accepted with rationale.",
        owner_agent="adversarial_editor",
        workstream="04-validation",
        validation=[],
    ),
    Milestone(
        name="Asset pack ready",
        done_when="Checklist/template/worksheet/verification artifacts are present and usable.",
        owner_agent="asset_builder",
        workstream="05-assets",
        validation=[],
    ),
    Milestone(
        name="Packaging + sale readiness",
        done_when="Launch copy, objections, and distribution plan are complete and PDFs build cleanly.",
        owner_agent="launch_strategist",
        workstream="06-packaging + 07-launch",
        validation=[
            "python3 scripts/status_check.py {product}",
            "python3 scripts/quality_gate.py {product}",
        ],
    ),
]


def append_update_log(product_dir: Path, line: str) -> None:
    update_log = product_dir / "updates" / "update_log.md"
    update_log.parent.mkdir(parents=True, exist_ok=True)
    existing = update_log.read_text(encoding="utf-8") if update_log.exists() else "# Update Log\n\n"
    if not existing.endswith("\n"):
        existing += "\n"
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    update_log.write_text(existing + f"- {stamp} — {line}\n", encoding="utf-8")


def ensure_workflow_docs(product_dir: Path) -> None:
    docs_dir = product_dir / "workflow"
    docs_dir.mkdir(parents=True, exist_ok=True)

    files = {
        "Prompt.md": "# Prompt\n\nUse this file as the immutable project specification.\n\n## Goals\n- Create a shippable knowledge product from ideation to sale.\n- Keep buyer scope narrow and outcome-focused.\n\n## Non-goals\n- Broad, generic content without proof of buyer spend.\n\n## Hard constraints\n- Work phase-by-phase with no skipping.\n- Keep decisions and status externalized in markdown.\n- Repair validation failures before advancing.\n\n## Deliverables\n- Complete phase folders from 00-brief to 07-launch.\n- Asset pack and packaged PDFs.\n- Launch plan and objection handling docs.\n\n## Done when\n- `scripts/status_check.py` passes.\n- `scripts/quality_gate.py` passes.\n- Launch assets exist and can be used to sell the product.\n",
        "Plan.md": "# Plan\n\nMilestones:\n1. Ideation lock\n2. Research confidence\n3. Architecture freeze\n4. Core draft complete\n5. Validation pass\n6. Asset pack ready\n7. Packaging + sale readiness\n\nRule: stop-and-fix if any gate fails.\n",
        "Implement.md": "# Implement\n\nExecution runbook:\n1. Read `workflow/Prompt.md` and `workflow/Plan.md`.\n2. Plan the current milestone in `workflow/Documentation.md` under orchestrator notes.\n3. Delegate the milestone to the owner agent.\n4. Verify gate commands and quality checks for the milestone.\n5. If a check fails, log a repair loop and do not advance.\n6. On pass, mark milestone complete and update `STATUS.md` + update log.\n",
        "Documentation.md": "# Documentation\n\n## Current milestone\n- Not started\n\n## Milestone checklist\n- [ ] Ideation lock\n- [ ] Research confidence\n- [ ] Architecture freeze\n- [ ] Core draft complete\n- [ ] Validation pass\n- [ ] Asset pack ready\n- [ ] Packaging + sale readiness\n\n## Orchestrator notes\n- (plan + delegation details by loop)\n\n## Decision log\n- (append decisions and rationale)\n\n## Verification log\n- (append command + result each milestone)\n\n## Repair loop log\n- (record failed gate + fix plan + retry result)\n\n## Next actions\n- (append next concrete action)\n",
    }

    for name, content in files.items():
        path = docs_dir / name
        if not path.exists():
            path.write_text(content, encoding="utf-8")


def current_milestone(documentation: str) -> int:
    for idx, milestone in enumerate(MILESTONES):
        if f"[x] {milestone.name}" not in documentation:
            return idx
    return len(MILESTONES)


def mark_milestone(documentation_path: Path, milestone: Milestone) -> None:
    text = documentation_path.read_text(encoding="utf-8")
    if "## Milestone checklist" not in text:
        checklist = "\n## Milestone checklist\n" + "\n".join(f"- [ ] {m.name}" for m in MILESTONES) + "\n"
        text += checklist
    text = text.replace(f"- [ ] {milestone.name}", f"- [x] {milestone.name}")
    text += f"\n- Completed milestone: **{milestone.name}** (owner: `{milestone.owner_agent}`)\n"
    documentation_path.write_text(text, encoding="utf-8")


def append_section_line(documentation_path: Path, section: str, line: str) -> None:
    text = documentation_path.read_text(encoding="utf-8")
    parts = text.splitlines()
    heading = f"## {section}"
    if heading not in text:
        if not text.endswith("\n"):
            text += "\n"
        text += f"\n{heading}\n"
        parts = text.splitlines()

    insert_at = None
    for i, raw in enumerate(parts):
        if raw.strip() == heading:
            insert_at = i + 1
            break
    if insert_at is None:
        return

    while insert_at < len(parts) and parts[insert_at].strip() == "":
        insert_at += 1
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    parts.insert(insert_at, f"- {stamp} — {line}")
    documentation_path.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")


def run_cmd(cmd: str) -> tuple[int, str]:
    result = subprocess.run(cmd, shell=True, check=False, text=True)
    return result.returncode, cmd


def run_validations(commands: Iterable[str], product_dir: Path) -> tuple[bool, list[tuple[str, int]]]:
    results: list[tuple[str, int]] = []
    for cmd in commands:
        rendered = cmd.format(product=str(product_dir))
        print(f"Running: {rendered}")
        code, _ = run_cmd(rendered)
        results.append((rendered, code))
        if code != 0:
            return False, results
    return True, results


def build_delegation_cmd(template: str, milestone: Milestone, product_dir: Path) -> str:
    return template.format(
        agent=milestone.owner_agent,
        milestone=milestone.name,
        product=str(product_dir),
        workstream=milestone.workstream,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run ideation->sale workflow milestones.")
    parser.add_argument("product", help="Product directory path (e.g., products/my-product)")
    parser.add_argument("--advance", action="store_true", help="Mark current milestone complete and run validations.")
    parser.add_argument(
        "--delegate-cmd",
        default="echo Delegated {milestone} to {agent} for {workstream} ({product})",
        help=(
            "Shell command template to execute delegation. Available placeholders: "
            "{agent}, {milestone}, {product}, {workstream}"
        ),
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Run the full orchestrator loop for current milestone (plan, delegate, verify, update logs).",
    )
    args = parser.parse_args()

    product_dir = Path(args.product).resolve()
    if not product_dir.exists():
        raise SystemExit(f"Product not found: {product_dir}")

    ensure_workflow_docs(product_dir)
    documentation_path = product_dir / "workflow" / "Documentation.md"
    doc_text = documentation_path.read_text(encoding="utf-8")
    idx = current_milestone(doc_text)

    if idx >= len(MILESTONES):
        print("All milestones are already complete.")
        return 0

    milestone = MILESTONES[idx]
    print(f"Current milestone: {milestone.name}")
    print(f"Done when: {milestone.done_when}")
    print(f"Owner agent: {milestone.owner_agent}")

    if args.auto:
        append_section_line(
            documentation_path,
            "Orchestrator notes",
            (
                f"Plan milestone '{milestone.name}' with owner `{milestone.owner_agent}` "
                f"over `{milestone.workstream}`."
            ),
        )
        delegate_cmd = build_delegation_cmd(args.delegate_cmd, milestone, product_dir)
        print(f"Delegating: {delegate_cmd}")
        d_code, _ = run_cmd(delegate_cmd)
        append_section_line(
            documentation_path,
            "Orchestrator notes",
            f"Delegation command: `{delegate_cmd}` (exit={d_code})",
        )
        if d_code != 0:
            append_section_line(
                documentation_path,
                "Repair loop log",
                f"Delegation failed for '{milestone.name}'. Retry with corrected command.",
            )
            raise SystemExit(d_code)

        ok, results = run_validations(milestone.validation, product_dir)
        if results:
            for cmd, code in results:
                append_section_line(
                    documentation_path,
                    "Verification log",
                    f"`{cmd}` -> exit={code}",
                )

        if not ok:
            append_section_line(
                documentation_path,
                "Repair loop log",
                (
                    f"Validation failed for '{milestone.name}'. Stop-and-fix before advancing. "
                    f"Owner `{milestone.owner_agent}` retained."
                ),
            )
            raise SystemExit(1)

        mark_milestone(documentation_path, milestone)
        append_update_log(product_dir, f"Milestone completed via --auto: {milestone.name}")
        append_section_line(
            documentation_path,
            "Next actions",
            "Move to next unchecked milestone and repeat orchestrator loop.",
        )
        print(f"Milestone marked complete: {milestone.name}")
        return 0

    if not args.advance:
        print("Use --advance after completing the milestone work.")
        return 0

    ok, results = run_validations(milestone.validation, product_dir)
    for cmd, code in results:
        append_section_line(documentation_path, "Verification log", f"`{cmd}` -> exit={code}")
    if not ok:
        append_section_line(
            documentation_path,
            "Repair loop log",
            f"Validation failed for '{milestone.name}'. Resolve gate failures and retry --advance.",
        )
        raise SystemExit(1)

    mark_milestone(documentation_path, milestone)
    append_update_log(product_dir, f"Milestone completed: {milestone.name}")
    print(f"Milestone marked complete: {milestone.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
