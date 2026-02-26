#!/usr/bin/env python3
import sys, pathlib

REQUIRED_FILES = [
  "STATUS.md","ASSUMPTIONS.md","RISKS.md","METRICS.md",
  "00-brief/problem_definition.md","00-brief/target_buyer.md","00-brief/pricing_hypothesis.md","00-brief/kill_criteria.md",
  "01-research/source_index.md","01-research/summaries.md","01-research/contradictions.md","01-research/insights.md","01-research/open_questions.md",
  "02-architecture/product_promise.md","02-architecture/transformation_map.md","02-architecture/outline.md","02-architecture/scope_guardrails.md",
  "03-drafts/draft_log.md",
  "04-validation/adversarial_review.md","04-validation/revision_tasks.md","04-validation/resolved_issues.md",
  "06-packaging/structure.md","06-packaging/quick_start.md","06-packaging/versioning.md","06-packaging/release_notes.md",
  "07-launch/landing_copy.md","07-launch/distribution_plan.md","07-launch/objections.md","07-launch/feedback_loop.md",
  "updates/update_log.md","updates/changelog.md",
]

REQUIRED_DIRS = [
  "05-assets/checklists","05-assets/templates","05-assets/worksheets","05-assets/diagrams",
  "updates/signals","updates/digests","updates/patches",
  "versions/v1.0"
]

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/status_check.py <product_dir>")
        return 2
    root = pathlib.Path(sys.argv[1]).resolve()
    if not root.exists():
        print(f"Not found: {root}")
        return 2

    missing_files=[f for f in REQUIRED_FILES if not (root/f).exists()]
    missing_dirs=[d for d in REQUIRED_DIRS if not (root/d).exists()]

    status_ok = (root/"STATUS.md").exists() and "Current Phase:" in (root/"STATUS.md").read_text(encoding="utf-8", errors="ignore")

    ok=True
    if missing_files:
        ok=False
        print("Missing required files:")
        for m in missing_files:
            print(" -", m)
    if missing_dirs:
        ok=False
        print("Missing required directories:")
        for d in missing_dirs:
            print(" -", d)
    if not status_ok:
        ok=False
        print("STATUS.md missing or malformed (must include 'Current Phase:').")

    if ok:
        print("STATUS CHECK: OK ✅")
        return 0
    print("STATUS CHECK: FAIL ❌")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
