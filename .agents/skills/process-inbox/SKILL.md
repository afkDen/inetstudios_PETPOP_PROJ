---
name: process-inbox
description: Convert a rough Roblox idea/update into the streamlined issue-local task state while preserving the human request. Retains legacy inbox compatibility but prefers scripts/team.py.
---
# Process Request / Inbox

For v8 team work:

1. Use one GitHub Issue as the shared request/thread.
2. Use `python scripts/team.py idea|update` to create one issue branch and changeset.
3. Preserve the original bytes in `USER_REQUEST.txt`; do not rewrite them.
4. Put interpretation, design, base approved scope, architecture, plan and acceptance criteria in TASK.md. After initial approval, material scope movement uses revisioned `SCOPE_AMENDMENTS/`; do not silently rewrite approved TASK.md.
5. Classify risk using `complexity-risk-router` and set only necessary gates.
6. Stop substantial implementation while human scope approval is PENDING.
7. After approval, delegate scoped implementation/review and maintain WORK_STATE.md. A DRAFT amendment leaves the prior revision active but pauses affected work; an APPROVED amendment advances the active revision and may require evidence refresh.
8. Use compact EVIDENCE.json by default; expand to the full quality packet only when risk demands it.
9. Publish one draft implementation PR after explicit human approval.

Legacy `00_INPUT/PROPOSALS`, sequential U### inboxes and promotion scripts remain compatibility paths only; do not use them for a new v8 task unless a maintainer explicitly requests legacy migration.
