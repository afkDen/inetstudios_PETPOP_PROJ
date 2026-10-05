---
name: domain-modeling
description: Sharpen the game's shared language and durable domain concepts. Use when terms are overloaded, code/design vocabulary conflicts, or a hard-to-reverse surprising tradeoff needs a durable decision record.
---

# Domain Modeling — Roblox workflow adaptation

Adapted from `mattpocock/skills` `domain-modeling` at pinned commit `24fe0ef7737efae15c87225755e9f6f5965e4888` (MIT).

A shared language reduces ambiguity across design docs, Luau APIs, Remote names, state machines, tests, Graphify queries, task packets, and reviews.

## Discipline
- When two terms are used for the same concept, choose one canonical term.
- When one term is doing several jobs, split it into precise concepts.
- Stress-test definitions with concrete player/server/session/round/item/economy scenarios and edge cases.
- Compare claimed behavior with current repository/Studio truth; surface contradictions instead of silently choosing one.
- Prefer game/player language over implementation jargon when naming domain concepts.

## Glossary
Use root `GLOSSARY.md` when present. Keep it implementation-free: canonical term, concise definition, and useful contrast/alias only. Do not turn the glossary into a spec, task log, API reference, or architecture document.

During **pre-approval design**, proposed glossary changes belong in `TASK.md` first. A specialist without repository write authority returns the proposed terms/definitions to the Lead rather than mutating canonical docs. After the human approves the underlying meaning, the implementing task may update `GLOSSARY.md` inside its approved scope. A post-approval semantic change that alters scope must be captured in a revisioned scope amendment and explicitly approved before affected implementation proceeds.

## Durable decisions
Use ADRs sparingly. A durable architecture decision is warranted only when all are true:
1. expensive or risky to reverse;
2. surprising without context;
3. a real tradeoff among alternatives.

If the project has an accepted ADR location, use it. Otherwise capture the proposed decision/rationale in the task and let the Lead/integrator establish the durable location rather than inventing a parallel documentation tree.
