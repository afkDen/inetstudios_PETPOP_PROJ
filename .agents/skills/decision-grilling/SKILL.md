---
name: decision-grilling
description: Resolve consequential ambiguity with a dependency-aware decision frontier. Use when one material product, design, architecture, or workflow decision depends on other unresolved decisions; keep facts with the agent and decisions with the human.
---

# Decision Grilling — Roblox workflow adaptation

Adapted from `mattpocock/skills` `grilling` at pinned commit `24fe0ef7737efae15c87225755e9f6f5965e4888` (MIT).

This is a **decision-quality discipline**, not a new task workflow. The Lead remains workflow authority. Do not create issues, branches, tickets, specs, approvals, or agent graphs from this skill.

## When to use
Use only when ambiguity is material enough that a single compact `human-decision-gates` request would leave dependent choices unresolved.

- **LIGHT:** normally do not run a multi-round grill unless the human explicitly asks.
- **STANDARD:** use selectively for material product/design/architecture forks.
- **CRITICAL:** use when unresolved choices affect persistence, networking/security, economy/monetization, migrations, release safety, or other high-blast-radius design.

Do not grill routine reversible implementation details already inside approved scope.

## Decision tree and frontier
Model unresolved choices as a dependency tree. The **frontier** is every decision whose prerequisites are already settled. Ask only that frontier; never ask a downstream question whose answer depends on an unresolved upstream choice.

For each frontier decision provide:
- a short title and exact decision;
- the downstream consequence;
- a recommended answer with reasoning;
- 2–4 meaningful options when alternatives exist.

Batch independent frontier questions into one round. After the human answers, recompute the frontier.

## Facts vs decisions
Finding facts is the agent's job. Use Graphify, repository reads, Git/GitHub, approved web research, task evidence, Studio/Blender/tool state, and primary sources before asking the human anything discoverable. The human supplies preferences, priorities, permissions, tradeoffs, acceptance, and choices only they can make.

If the user cannot answer because another person holds the missing knowledge, stop that branch and use `external-questionnaire` instead of repeatedly interrogating the user.

## Completion
Stop when every material branch is either resolved, explicitly deferred/out of scope, or blocked on named external knowledge. Before approval, record resolved material decisions and rationale in `TASK.md` so they are covered by the scope fingerprint. After approval, record non-scope-changing operational decisions/pointers in `WORK_STATE.md` rather than rewriting approved design. Scope-changing answers after approval require a revisioned scope amendment. Keep the current approved revision active until that amendment is explicitly approved; pause only the affected work.
