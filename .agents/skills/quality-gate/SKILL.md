---
name: quality-gate
description: Apply risk-proportional Definition-of-Done gates to Roblox work. LIGHT uses compact checks, STANDARD adds relevant live/review evidence, CRITICAL uses the full quality packet and specialist review.
---
# Quality Gate

1. Read TASK.json risk/gates and TASK.md acceptance criteria.
2. Check specification compliance and relevant regression/acceptance evidence.
3. Verify server/client authority, console/runtime errors, and affected risk domains.
4. Activate only reviewers relevant to actual risk.
5. Require revision for material failures and retest after fixes.
6. Use a fresh independent reviewer when required; the implementer cannot be the sole substantial-work reviewer.
7. Lead adjudicates: APPROVED / APPROVED WITH FOLLOWUPS / REVISION REQUIRED / BLOCKED / ARCHITECTURAL REWORK REQUIRED.

## Risk mapping

- LIGHT: compact EVIDENCE.json + relevant static/native checks; live Studio/reviewer only if the task requires them.
- STANDARD: real Studio evidence for player-visible/Studio-dependent work and fresh independent review for substantial changes.
- CRITICAL: QUALITY_BRIEF + QUALITY_EVIDENCE + relevant specialist reviews; Studio receipt when applicable.

A build, parser-valid packet or agent self-report never substitutes for evidence the task actually requires. Missing capability -> BLOCKED/PENDING.
