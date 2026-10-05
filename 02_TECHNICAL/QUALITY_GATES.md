# Quality Gates

## Tier 0 — Trivial
Minimal verification; no specialist overhead unless risk appears.

## Tier 1 — Small
Targeted implementation + focused verification + Lead check.

## Tier 2 — Normal Feature
Design/technical analysis, implementation package, acceptance tests, implementation report, independent QA review, Lead adjudication.

## Tier 3 — Complex Feature
Multiple relevant specialists, explicit integration plan, stronger QA/playtest coverage, performance/security review as applicable, fresh final review.

## Tier 4 — High-Risk / Foundational
Architecture, persistence, networking/security, regression, migration/rollback, fresh independent review, Lead adjudication, and explicit release readiness.

## Universal release gates
- approved scope complete;
- acceptance tests pass;
- relevant console errors resolved;
- server/client boundaries correct;
- exploit-sensitive paths validated;
- persistence safe where applicable;
- multiplayer/device behavior checked where relevant;
- performance reasonable;
- documentation updated;
- Git clean;
- rollback path exists.

## Visible game features: no-placeholder completion gate

For every Tier 2+ visible feature follow `PRODUCTION_QUALITY_CONTRACT.md`. Pre-approved art brief and art-direction signoff are required for substantial visuals; an actual playable slice, meaningful UI states if relevant, approved asset families, real Studio screenshots/playtest/console evidence, and fresh role-separated visual/gameplay review are required. `scripts/validate_feature_evidence.py` enforces issue evidence schema, file existence and independent reviewer IDs. The script cannot certify real aesthetics or test truth; the second human reviewer must inspect evidence. A brick blockout is a valuable milestone but must remain BLOCKOUT, not APPROVED. If no live Studio/asset capability exists, record BLOCKED / manual owner rather than claiming PASS.
