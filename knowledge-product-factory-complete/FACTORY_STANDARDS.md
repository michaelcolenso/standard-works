# Works Standards

## Language standards
- Avoid vagueness. If you must say “it depends”, provide a decision tree.
- Prefer concrete numbers, examples, and scripts over theory.
- Every section must explicitly state a buyer outcome.

## Content standards
Every product must include:
- Quick Start (10-minute activation path)
- Decision support (checklists + if/then rules)
- Examples (at least 3) that show correct usage
- Failure modes (what goes wrong and how to detect it)
- Templates (minimum: one central template + 3 supporting assets)

## Update standards (living products)
- Signals are logged in `updates/signals/`
- Every signal gets a classification:
  - Cosmetic / Tactical / Structural / Invalidating
- Facts change → patches; mental models change → versions
- Changelog must be visible and user-facing

## Required files per product
- STATUS.md, ASSUMPTIONS.md, RISKS.md, METRICS.md
- 00-brief: problem_definition.md, target_buyer.md, pricing_hypothesis.md, kill_criteria.md
- 01-research: source_index.md, summaries.md, contradictions.md, insights.md, open_questions.md
- 02-architecture: product_promise.md, transformation_map.md, outline.md, scope_guardrails.md
- 03-drafts: core/, evergreen/, draft_log.md
- 04-validation: adversarial_review.md, revision_tasks.md, resolved_issues.md
- 05-assets: checklists/, templates/, worksheets/, diagrams/
- 06-packaging: structure.md, quick_start.md, versioning.md, release_notes.md
- 07-launch: landing_copy.md, distribution_plan.md, objections.md, feedback_loop.md
- updates: update_log.md, changelog.md, signals/, digests/, patches/
- versions: v1.0/

## CI / Build standards
- Every PR must pass:
  - scripts/status_check.py (required files/dirs)
  - scripts/quality_gate.py (language + headers)
  - PDF build (Makefile targets)
- A product cannot be marked “Launch ready” unless `dist/` contains:
  - <PRODUCT>_Core_Guide.pdf
  - <PRODUCT>_Quick_Start.pdf
  - <PRODUCT>_Asset_Pack.pdf
  - (living) <PRODUCT>_Update_Digest.pdf

## Minimum Asset Pack (Works Standard: 5-Asset Rule)
Every product ships with at least:
1) Master Tracker (single source of truth)
2) Go/No-Go Gate (binary decision)
3) Sequence Checklist (order enforcement)
4) Worksheet (calculation or trade-off)
5) Verification Sheet (proof of correctness)

Rule:
If a section does not produce or reference one of the above asset types, it does not ship.

## Reuse policy
- Reuse structure freely (works-assets).
- Do not reuse examples, thresholds, or numbers.
- Any reused asset must declare origin and pass adversarial review.
