---
name: systematic-debugging
description: Diagnose Roblox/code/tool failures with the cheapest tight feedback loop, evidence-first root-cause analysis, minimal hypotheses, and verified cleanup. Use for bugs, regressions, build/integration failures, performance issues, and flaky Studio behavior.
---

# Systematic Debugging — Roblox + usage-budget adaptation

Synthesized from `mattpocock/skills` `diagnosing-bugs` at commit `24fe0ef7737efae15c87225755e9f6f5965e4888` (MIT) and the previously pinned `magnus919/agent-skills` `systematic-debugging` at `affec9d8cba35a3b8d632a64ab547ea8fcc53380` (MIT).

## Principle
**No fix before a trustworthy signal for the actual symptom.** Do not guess-edit until you can observe the failure closely enough to falsify a cause.

The signal does **not** have to be a newly written test. Preserve usage budget: prefer existing, cheap, deterministic feedback before authoring new infrastructure.

## 1. Build the cheapest tight feedback loop
Prefer roughly in this order, choosing what matches the bug:
1. existing focused test/validator/check;
2. existing CLI/build/Rojo command with a fixture or known output;
3. focused Luau harness or existing test place;
4. Studio MCP probe/playtest with exact console/Instance/state evidence (when the current role lacks Studio authority, return the exact probe to the Lead/`studio-operator`);
5. captured/replayable event, Remote payload, save fixture, trace, or differential old-vs-new comparison;
6. temporary targeted instrumentation with a unique removable prefix;
7. human-in-the-loop reproduction only when automation is genuinely unavailable.

A good loop catches **this bug**, is repeatable enough to compare hypotheses, and is as fast as practical. For flaky bugs, raise reproduction probability instead of pretending determinism.

If no trustworthy loop can be built, state what was tried and what missing access/artifact is required. Do not manufacture a theory from absence of evidence.

## 2. Reproduce and minimize
Confirm the observed symptom matches the user's report. Shrink the scenario one element at a time while re-running the loop. Keep only load-bearing inputs/state/steps.

## 3. Investigate root cause
Read complete errors/stacks/console lines; inspect recent relevant changes; trace data across client/server/module/tool boundaries; compare working and broken examples; verify dependency/source/pin/dirty state before blaming library behavior. Redact secrets from any captured output.

For a hard bug, write 2–4 ranked falsifiable hypotheses. For a simple bug with direct evidence, one hypothesis is enough. Test one variable at a time; do not bundle speculative fixes.

## 4. Fix minimally and verify
Apply the smallest root-cause fix. Re-run the minimized loop and the original scenario, then the task's already-required broader checks. Add a regression test only when it is a cheap durable guard at a correct seam or the task/risk explicitly requires one; **do not introduce TDD ceremony solely to satisfy this skill**.

After three failed fix attempts that expose new coupling, stop and escalate the architecture to the Lead/`codebase-design` rather than stacking Fix #4.

## 5. Cleanup
Remove tagged debug instrumentation/throwaway harnesses unless intentionally retained as documented tooling. Record root cause, verification evidence, and any remaining uncertainty in the task state.
