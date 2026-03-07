# Implement

Execution runbook:
1. Read `workflow/Prompt.md` and `workflow/Plan.md`.
2. Plan the current milestone in `workflow/Documentation.md` under orchestrator notes.
3. Delegate the milestone to the owner agent.
4. Verify gate commands and quality checks for the milestone.
5. If a check fails, log a repair loop and do not advance.
6. On pass, mark milestone complete and update `STATUS.md` + update log.
