---
name: human-decision-gates
description: Decide when an agent must ask the human before proceeding, choosing a compact decision request, dependency-aware grilling, or an external questionnaire without interrupting for routine reversible work.
---

# Human Decision Gates

Do not interrupt for routine reversible implementation details already determined by accepted design. **Ask and stop the affected work** when any of these is true:
- material scope expansion or new feature/system;
- high-impact creative/art/UX fork with significant downstream cost and no canonical answer;
- new package/tool/system-manager/MCP server installation or permission expansion;
- external account, paid API, subscription, asset purchase or recurring cost;
- unclear asset/license/provenance permission;
- destructive Git/state operation, force update, migration or irreversible data transformation;
- Production publish, shared-place mutation outside the approved writer window, or release action;
- persistence schema migration, security/trust-boundary change, monetization/RNG/trading policy change;
- model/runtime/policy exception;
- a requirement conflict that cannot be resolved from canonical sources.

## Choose the smallest decision mechanism
Facts are the agent's job: inspect repository/Graphify/Git/Studio/tool state and primary sources before asking the human.

1. **One material decision, dependencies already settled:** use one compact block:
   **Decision needed:** <one sentence>  
   **Why now:** <downstream consequence>  
   **Recommendation:** <preferred option + reason>  
   **Options:** A / B / C with material tradeoff  
   **If deferred:** <what can safely continue>
2. **Several material decisions whose answers depend on one another:** the Lead may use `decision-grilling`. Keep it risk-proportional; LIGHT tasks normally do not need a multi-round interview.
3. **The current user cannot answer because another person owns the missing knowledge:** use `external-questionnaire` and mark that branch blocked instead of asking the user to guess.

Specialists should surface unresolved material choices to the Lead; they should not start independent interview workflows that fragment task authority.

Before initial approval, record material design/scope decisions in `TASK.md`. After approval, record ordinary in-scope operational decisions in `WORK_STATE.md` so the immutable base scope is not churned. If an answer changes approved scope, architecture, risk, or gates, draft a revisioned scope amendment and obtain explicit amendment approval before affected implementation continues; leave unaffected work on the existing approved revision.
