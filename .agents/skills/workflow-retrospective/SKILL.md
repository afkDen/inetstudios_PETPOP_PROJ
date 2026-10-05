---
name: workflow-retrospective
description: Review a completed or troubled agent session for improvements to navigation, checks, instructions, tool economy, information access, and workflow guardrails. Use explicitly after meaningful failure/friction; do not run after every task.
---

# Workflow Retrospective — bootstrap adaptation

Adapted from `mattpocock/skills` `retro` at pinned commit `24fe0ef7737efae15c87225755e9f6f5965e4888` (MIT).

This improves the **agent environment**, not the feature code. It is intentionally opt-in/budget-aware; do not spend a retrospective pass on routine successful LIGHT work.

## Review categories
- **Navigation:** did agents waste time locating authoritative information? Prefer better pointers/Graphify coverage over more scout agents.
- **Automated guardrails:** could a deterministic validator have caught the failure? Prefer a check over a reminder for mechanical rules.
- **Judgment standards:** did assurance miss a genuinely non-mechanical quality problem?
- **Instruction design:** is an always-loaded rule stale, duplicated, ambiguous, or a no-op?
- **Tool economy:** were expensive calls/delegations made where a cheaper targeted lookup would suffice?
- **Information access:** was a needed log/source/tool unavailable or poorly surfaced?
- **Evidence:** did the workflow confuse generated/configured state with observed runtime truth?

## Output
Rank recommendations by severity and recurrence likelihood. For each: observed failure/friction, root environmental cause, smallest durable improvement, owner, and whether it belongs in a validator, skill/prompt, tool adapter, or documentation pointer.

Ordinary feature branches must **not** use this skill to rewrite integration-owned bootstrap infrastructure. Record recommendations in the active changeset (for example `RETRO.md`). An integration owner may later accept them through a dedicated bootstrap/infrastructure change.
