---
name: agent-instruction-design
description: Design and prune AGENTS.md files, role prompts, skills, and agent-facing documentation using context pointers, progressive disclosure, explicit completion criteria, and single-source-of-truth rules.
---

# Agent Instruction Design — bootstrap adaptation

Adapted from `mattpocock/skills` `writing-for-agents` at pinned commit `24fe0ef7737efae15c87225755e9f6f5965e4888` (MIT).

Use primarily for bootstrap/integration work, not ordinary gameplay implementation.

## Context pointers
An always-loaded line should say **what** out-of-context material contains and **when** to reach it. Strong pointers reduce the need to inline whole policies. Front-load the trigger; avoid synonym lists that describe the same branch twice.

## Information hierarchy
1. In-file steps the agent must execute every run.
2. In-file reference needed often enough to stay nearby.
3. Disclosed reference behind a precise pointer for branch-specific detail.

Push branch-specific reference down; keep required ordered actions visible. Optimize reliability first, token count second.

## Completion criteria
Every procedural step should end on a checkable completion condition. Prefer exhaustive, observable criteria over “understand” or “be thorough.” If a fuzzy step is repeatedly rushed, sharpen its completion bound before adding more prose.

## Single source of truth
Do not restate facts that are cheap to discover from canonical JSON/config/scripts. Generated docs should identify their source and be mechanically synchronized. Duplication that can drift is a bug.

## Context and cognitive load
Always-loaded rules spend context every turn. User-invoked/maintainer workflows spend human attention. Keep frequent autonomous disciplines small and composable; keep consequential or expensive workflows explicit.

## Pruning
Delete stale claims, no-op instructions, redundant warnings, and environment facts that are only cached copies of configuration. Use concise leading terms only when they genuinely improve consistent behavior.

Never use this skill to weaken safety, approval, provenance, evidence, or integration-owner boundaries for token savings.
