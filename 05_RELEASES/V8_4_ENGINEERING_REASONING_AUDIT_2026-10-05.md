# v8.4 Engineering Reasoning Integrated — Final Audit

**Version:** `v8.4-engineering-reasoning-integrated`  
**Baseline:** `v8.3.1-bloxmaps-hardened`  
**Task packet compatibility:** existing `streamlined-v8.3` tasks remain supported.

## Source review

Reviewed `mattpocock/skills` at immutable commit `24fe0ef7737efae15c87225755e9f6f5965e4888` (release 1.3.1 at review time, MIT). The integration is selective and adapted rather than installed wholesale. Exact upstream blob provenance is recorded in `SKILL_REGISTRY.json`; the MIT notice is preserved in `THIRD_PARTY_NOTICES.md`.

## Integrated capabilities

- decision frontier / grilling
- external stakeholder questionnaire
- domain modeling/shared language
- deep-module/interface/seam design
- writing/instruction design for agents
- explicit workflow retrospectives
- primary-source research
- two-axis assurance
- budget-aware systematic debugging synthesized with the prior debugging dependency

## Explicit exclusions

No TDD skill is registered or required. The bootstrap also does not import upstream `to-spec`, `to-tickets`, `implement`, `implement-spec`, `triage`, `wayfinder`, `ask-matt`, or setup flows. They conflict with or duplicate the existing one-Issue/one-branch/one-PR authority model.

## Usage-economy decisions

Existing deterministic tests, validators, Rojo/native checks and Studio evidence are preferred before authoring new test infrastructure. Decision grilling is risk-proportional rather than automatic. Research may run in the current context and cannot exceed the Lead's three-subagent budget. Retrospectives are explicit after meaningful friction rather than a post-task tax. Two-axis assurance is performed by the existing fresh reviewer instead of doubling reviewer agents.

## Supply-chain change

The previously external `systematic-debugging` requirement is now a bundled adaptation. This reduces required external skill resolution by one while keeping the same canonical skill name used by roles.

## Validation

Automated source and fresh-scaffold validation on 2026-10-05:

- `pytest -q`: **201 tests passed + 22 subtests passed**.
- `python -m unittest discover -s tests -q`: **201 tests passed**; deliberate fixture gate-failure text is expected test output, not a suite failure.
- Python compile pass for `scripts/` and `tests/`.
- Derived-document check: PASS.
- Shared model-policy structural validation: PASS.
- Static Rojo ownership/layout guard: PASS (not a native Rojo build).
- Disposable intake → planning → implementation → fresh review → revision → checkpoint/resume simulation: PASS.
- All distributable JSON/TOML parsed successfully; no distributable symlinks or high-signal credential/private-key patterns found.
- Fresh `prepare_new_game.py` scaffold: `validate_team.py`, `validate_repo.py`, `validate_rojo_layout.py`, model-policy structural check, disposable pipeline, and the full pytest suite all PASS. The prepared scaffold reports **49 bundled skills, 37 external skills, 86 registered skills, and 10 roles**.
- v8.4 regression coverage enforces the TDD/process-flow exclusion, immutable upstream provenance for Matt-derived adaptations, two-source provenance for bundled `systematic-debugging`, role routing, decision-record placement, approval-fingerprint-safe post-approval decision persistence, and integration ownership of bootstrap test/release surfaces.

Live Roblox Studio MCP/playtest, Blender MCP, Graphify runtime operation, BloxMaps MapGen execution, and a native Rojo binary build were **not** exercised in this packaging environment. The bootstrap continues to require real task-time evidence for those capabilities and does not infer readiness from configuration.
