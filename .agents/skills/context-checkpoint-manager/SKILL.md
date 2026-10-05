---
name: context-checkpoint-manager
description: Creates or repairs durable continuation checkpoints so a fresh agent/runtime session can resume from repository state after interruption, usage exhaustion, restart, or intentional rollover.
---

# Context Checkpoint Manager

Update:
- active issue changeset `WORK_STATE.md` (every assignee can update their own)
- active issue changeset `NEXT_ACTION.md` (every assignee can update their own)
- shared `06_PROJECT_STATE/CURRENT_STATE.md` **only** by the main-branch human integrator after merging accepted work
- shared `06_PROJECT_STATE/NEXT_ACTION.md` **only** when the integration owner updates the canonical next action

Record:
- current stage;
- completed/partial/remaining work;
- exact changed files and Studio Instances;
- tests/failures;
- decisions/deviations and unresolved decision frontier;
- blockers / external knowledge dependencies;
- current owner;
- exact next action.

Before ending, inspect actual repository/Studio state. If checkpoint notes conflict with reality, trust reality, document the mismatch, and repair the checkpoint.

Prefer **context pointers** to duplicate content: link TASK/design/research/evidence paths instead of copying large bodies into WORK_STATE. A checkpoint should contain only the state required to resume.
