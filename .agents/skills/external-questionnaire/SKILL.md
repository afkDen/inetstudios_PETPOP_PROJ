---
name: external-questionnaire
description: Create a focused questionnaire when a task is blocked by knowledge held by another stakeholder, artist, developer, vendor, tester, or domain expert. Use instead of asking the current user to guess information they do not possess.
---

# External Questionnaire — Roblox workflow adaptation

Adapted from `mattpocock/skills` `to-questionnaire` at pinned commit `24fe0ef7737efae15c87225755e9f6f5965e4888` (MIT).

Use this only when the missing input belongs to another human. It does not create a parallel issue/ticket workflow.

## Process
1. Determine **who holds the missing knowledge** and what they are expected to know.
2. Determine **what decisions/facts must come back** before the blocked task branch can continue.
3. Write a concise questionnaire under the active changeset, preferably `QUESTIONNAIRES/<slug>.md`.
4. Order questions by decision value. One question = one idea. Include short context and, only when useful, one line explaining why the answer matters.
5. Mark partial answers and “I don't know” as acceptable. Do not force false certainty.
6. Link the questionnaire from `TASK.md` while still in design. After approval, prefer `WORK_STATE.md` unless the questionnaire changes scope, in which case draft/approve a scope amendment. Mark only the affected work branch blocked.

## Returned answers
Treat returned material as new task evidence/input, not as implicit approval. Preserve any supplied files/answers according to the repository's provenance rules. If the answer changes approved scope, architecture, risk, gates, or a material creative direction, create and explicitly approve a scope amendment before affected implementation continues.

Never fabricate a stakeholder answer and never substitute the agent's opinion for knowledge explicitly owned by an external person.
