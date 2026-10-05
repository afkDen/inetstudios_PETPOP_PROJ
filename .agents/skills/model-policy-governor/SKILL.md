---
name: model-policy-governor
description: Apply the team's approved model and reasoning-effort restrictions before selecting/delegating agents, during workstation bootstrap, after a provider/model change, or when authorizing an exceptional high-effort architecture/security review. Enforce exact Claude Code, Codex and evidence-verified Antigravity selections without changing canonical role contracts.
---
# Team model-policy governor

Trigger: initialization, runtime change, new developer onboarding, agent delegation, quota/model fallback, escalation to High, new agent adapter or release readiness.

1. Read `AGENTS.md`, `08_TOOLCHAIN/TEAM_MODEL_POLICY.json` and `08_TOOLCHAIN/MODEL_ROUTING.md`. Canonical `ROLE_CONTRACTS/roles.json` defines capability classes; **never** insert a provider ID into canonical roles.
2. Resolve the role via `scripts/model_policy.py` or `scripts/render_role_packet.py --runtime RUNTIME --role ROLE --task TASK`. Use Low for FAST when actually available; Medium is the normal workhorse. Claude Code stays exact approved Opus 5.5 and never High. Codex stays exact approved GPT-6 Sol; High is available only for DEEP/REVIEW_DEEP when explicit rationale is recorded. On Antigravity, generated agent frontmatter uses `inherit`; inspect the actual selected model and delegated effort rather than inferring support from tiers.
3. Generate runtime adapters with `scripts/sync_runtime_adapters.py --runtime RUNTIME`. Do not directly edit generated files as a source of truth. Preload no more than three installed, relevant skills per generated agent and load additional domain skills on demand.
4. During initialization, use `scripts/create_model_preflight.py`, collect sanitized observed main + delegated FAST/BALANCED traces under ignored `.local/`, verify with `scripts/validate_model_policy.py`, then and only then record `model_policy_validation PASS`. A planning-only runtime without subagents must still supply real main-model evidence; never mislabel it FULL.
5. For High escalation, explain why Medium is insufficient, why the task is DEEP/REVIEW_DEEP, what the actual model supports, and where the justification is recorded in the issue changeset. Do not silently upgrade or change providers on quota exhaustion. If unavailable or disallowed, split the task, ask another human reviewer, or block the affected step.
6. Independent review needs a fresh context and, on substantial team PRs, another human; same approved model in a truly independent context is acceptable. Do not misrepresent static adapter configuration, screenshots, fabricated test traces or CI as proof of real provider settings.

Outputs: approved runtime+role effort plan, local model preflight status, explicit recorded escalations where applicable, and precise blocked capability notes. Do not edit production Studio or approve a release on this skill's authority alone.
