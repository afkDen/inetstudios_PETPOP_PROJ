---
name: team-workflow-orchestrator
description: Run the streamlined v8 issue-scoped workflow: one Issue, one task branch, byte-preserved request, risk-proportional agentic implementation, approval-gated draft PR, and human-controlled merge/release.
---
# Team workflow orchestrator

Trigger: the user supplies a new idea/update `.txt`, asks to resume a task, or wants to check/publish/review team work.

1. Read `AGENTS.md`, `TEAM_PROTOCOL.md`, `TEAM_WORKFLOW.md`, actual Git state and the relevant Issue/task changeset.
2. For new work use `python scripts/team.py idea|update`; for existing work use `team.py resume`. Do not create a separate proposal/promotion lifecycle for a v8 task.
3. Preserve `USER_REQUEST.txt` byte-for-byte. Use TASK.md for interpretation/design and WORK_STATE.md for resumability.
4. Route risk/skills/roles proportionally. Do not run every agent. Resolve material decision dependencies with the smallest mechanism (`human-decision-gates` → `decision-grilling` only when needed; `external-questionnaire` for knowledge held elsewhere). Complete design/plan first and stop for human scope approval when TASK.json says PENDING.
5. After initial approval, execute within the active approved scope revision. When the human wants material scope to move, create a revisioned scope amendment; keep the prior revision authoritative until explicit amendment approval, then refresh/attest affected evidence before delivery. Execute the design→implementation→test/evidence→fresh review→revision→checkpoint lifecycle on the task branch. Tests are risk/evidence-driven; TDD is not a global requirement. Use Studio/Rojo live evidence only when the task requires it.
6. Run `python scripts/team.py check --issue N` before final delivery. LIGHT/STANDARD/CRITICAL gates differ; CRITICAL retains the full quality packet.
7. Ask before remote publication. `team.py pr` is preview-only until `--confirm-publish`. Human review controls merge; Production publish is separate.
8. Stop on dirty/divergent/wrong-origin state rather than auto-stash/reset/rebase/force-push.

Return: exact issue/branch/changeset, risk/gates, selected skills/roles, files changed, tests/native build/Studio evidence, independent review, blockers and next action.
