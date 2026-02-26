# Works Playbook

## Core principles
1. **Externalized state**: all progress is written to files; nothing important lives only in chat.
2. **Phase gates**: do not advance phases until the gate checklist is satisfied.
3. **Long-horizon loops**: plan → execute → verify → repair → log.
4. **Adversarial quality**: a dedicated agent attacks the draft to prevent refunds.
5. **Assets > prose**: every major concept gets a checklist/template/worksheet.
6. **Core vs updates**: stable frameworks live in `03-drafts/core/`; fast-changing info lives in `updates/`.

## Phase order (default)
0. Brief
1. Research
2. Architecture
3. Drafting
4. Validation
5. Assets
6. Packaging
7. Launch
8. Updates (ongoing)

## Stop / kill logic
If any of these are true after two full brief+research loops:
- No spending proof
- No differentiation
- Buyer is too broad/unreachable organically
- You cannot produce a materially better artifact pack than alternatives
Then: pivot (narrow buyer/scope/toolkit-first) or kill.

## Works-level learning
After any launch (or kill), add an entry to `FACTORY_POSTMORTEMS.md`.
