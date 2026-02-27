#!/usr/bin/env python3
"""Long-horizon workflow runner for knowledge products (ideation -> sale)."""
from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class Milestone:
    name: str
    done_when: str
    validation: list[str]


MILESTONES = [
    Milestone(
        name="Ideation lock",
        done_when="A narrow buyer pain with spending proof is recorded in brief and intake notes.",
        validation=[],
    ),
    Milestone(
        name="Research confidence",
        done_when="Contradictions, open questions, and insights are filled with source citations.",
        validation=[],
    ),
    Milestone(
        name="Architecture freeze",
        done_when="Promise, transformation map, outline, and guardrails define the product boundary.",
        validation=[],
    ),
    Milestone(
        name="Core draft complete",
        done_when="Core draft sections and draft log are complete for v1.0 packaging.",
        validation=[],
    ),
    Milestone(
        name="Validation pass",
        done_when="Adversarial review findings are resolved or accepted with rationale.",
        validation=[],
    ),
    Milestone(
        name="Asset pack ready",
        done_when="Checklist/template/worksheet/verification artifacts are present and usable.",
        validation=[],
    ),
    Milestone(
        name="Packaging + sale readiness",
        done_when="Launch copy, objections, and distribution plan are complete and PDFs build cleanly.",
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
        "Implement.md": "# Implement\n\nExecution runbook:\n1. Read `workflow/Prompt.md` and `workflow/Plan.md`.\n2. Execute only the current milestone scope.\n3. Run validations for the milestone.\n4. If a check fails, fix and rerun before moving ahead.\n5. Update `workflow/Documentation.md` and `STATUS.md` every loop.\n",
        "Documentation.md": "# Documentation\n\n## Current milestone\n- Not started\n\n## Decision log\n- (append decisions and rationale)\n\n## Verification log\n- (append command + result each milestone)\n\n## Next actions\n- (append next concrete action)\n",
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
    text += f"\n- Completed milestone: **{milestone.name}**\n"
    documentation_path.write_text(text, encoding="utf-8")


def run_cmd(cmd: str) -> None:
    result = subprocess.run(cmd, shell=True, check=False, text=True)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run ideation->sale workflow milestones.")
    parser.add_argument("product", help="Product directory path (e.g., products/my-product)")
    parser.add_argument("--advance", action="store_true", help="Mark current milestone complete and run validations.")
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

    if not args.advance:
        print("Use --advance after completing the milestone work.")
        return 0

    for cmd in milestone.validation:
        rendered = cmd.format(product=str(product_dir))
        print(f"Running: {rendered}")
        run_cmd(rendered)

    mark_milestone(documentation_path, milestone)
    append_update_log(product_dir, f"Milestone completed: {milestone.name}")
    print(f"Milestone marked complete: {milestone.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
