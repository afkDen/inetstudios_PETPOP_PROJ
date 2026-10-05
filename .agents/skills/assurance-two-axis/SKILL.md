---
name: assurance-two-axis
description: Keep spec/scope fidelity separate from engineering/project-standard quality during independent review so polished wrong-scope code cannot mask a product miss and spec-correct code cannot hide unsafe implementation.
---

# Two-Axis Assurance — Roblox workflow adaptation

Adapted from `mattpocock/skills` `code-review` at pinned commit `24fe0ef7737efae15c87225755e9f6f5965e4888` (MIT).

This augments the existing fresh `assurance-reviewer`; it does not create additional reviewer agents.

## Axis A — Scope / spec fidelity
Compare the actual diff/runtime evidence with the **effective approved scope**: base `TASK.md` plus every APPROVED `SCOPE_AMENDMENTS/AMENDMENT-*.md` through the active revision, and its acceptance criteria:
- missing or partial requested behavior;
- behavior outside the active approved scope revision;
- implemented behavior that contradicts the approved design;
- evidence that proves a different scenario than the one requested.

## Axis B — Engineering / project standards
Evaluate correctness and maintainability against repository rules and task risk:
- authority/security/persistence/networking correctness;
- failure/cleanup/race behavior;
- module/interface quality and unjustified complexity;
- performance and platform constraints;
- UI/accessibility/experience rules where relevant;
- evidence/provenance/Git-task coherence.

Treat code smells as judgment signals, not automatic violations. Deterministic lint/format/schema rules belong to automated checks rather than reviewer prose.

## Reporting
Keep findings grouped by axis even if one issue touches both. Within each axis, rank by severity and cite direct evidence. Then apply the existing FUNCTIONAL / EXPERIENCE / RISK / RELEASE mode verdict. Do not double the reviewer count just to separate axes; one fresh reviewer may perform two explicit passes.
