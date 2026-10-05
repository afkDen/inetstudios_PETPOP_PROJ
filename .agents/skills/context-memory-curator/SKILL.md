---
name: context-memory-curator
description: Keep long-running Roblox agent sessions coherent with just-in-time retrieval, structured checkpoint capsules, stale-context pruning and durable repository memory instead of relying on chat history.
---

# Context Memory Curator

Repository artifacts are the default project memory; chat transcripts are not. Prefer precise context pointers to duplicated summaries when the referenced artifact is already durable.

## Memory tiers
1. **Canonical:** GAME_DESIGN.md, accepted technical/design docs, main-branch decisions.
2. **Task:** TASK.json/TASK.md, immutable USER_REQUEST.txt, WORK_STATE.md, evidence.
3. **Session:** temporary logs/tool outputs in `.local/`; never canonical by themselves.

## Context discipline
- Load the minimum authoritative files needed for the current step.
- Prefer search/find then targeted reads over opening whole documentation trees.
- Do not forward raw tool logs to subagents unless they need them.
- At each milestone compact into WORK_STATE with: goal; stage; branch/commit; accepted facts; decisions; changed files/Instances; tests/evidence; blockers; unresolved questions; exact next action.
- Explicitly mark superseded assumptions so fresh sessions do not revive them.
- If context becomes noisy or contradictory, checkpoint and start a fresh context rather than extending stale history.
- A subagent receives a task packet, not the whole parent conversation.

Graphify is the recommended local repository-intelligence/memory augmentation, never source of truth. Query/update it to reduce broad scans and recover relationships, but verify any recalled/inferred graph fact against repository/Git/task/Studio/Blender sources before it changes project state. Semantic model-backed extraction/work-memory is opt-in.
