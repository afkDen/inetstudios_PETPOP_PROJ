# MODEL ROUTING — Portable Classes and Team Caps

`roles.json` defines role responsibilities and one of six **vendor-neutral capability classes**. `TEAM_MODEL_POLICY.json` is the machine-readable, integrator-owned shared model/effort restriction; individual actual model availability and observed execution evidence stay in ignored `.local/`.

| Class | Typical work | Normal effort |
|---|---|---|
| `FAST` | Repository scouting, extraction and tightly bounded repetitive tasks | Low |
| `BALANCED` | Normal implementation, game design, asset work, UI and world building | Medium |
| `DEEP` | Lead, architecture, economy and art direction | Medium |
| `REVIEW` | Ordinary independent QA, playtesting and UI review | Medium |
| `REVIEW_DEEP` | Security, persistence, gameplay and visual quality reviews | Medium |
| `TOOL_RELIABLE` | Studio operator, integration and initializer | Medium |

## Shared profiles

- **Claude Code:** exact approved model `claude-opus-5-5`; Low/Medium only, normal Medium; no High or silently chosen Haiku/Sonnet/Fable substitutes. A deep task is decomposed or escalated to a human if Medium is insufficient.
- **Codex:** exact approved model `gpt-6.1-sol`; Low/Medium/High available if observed; normal Medium. High is restricted to `DEEP`/`REVIEW_DEEP` work with a concrete recorded justification. The normal generated Codex agents remain Medium; use the explicit issue-scoped temporary agent in `scripts/prepare_codex_high.py` after human approval and remove it afterward. Never silently enable `xhigh`, Max or Ultra.
- **Antigravity:** preferred model `gemini-3.8-flash`; Medium workhorse when actually available. The native custom-agent schema has tier/inherit, **not a universal exact-model/per-subagent-effort switch**. Generated agents use `model: inherit` to avoid silently changing the model family. Preflight must inspect actual selectable efforts and delegated agent settings; a FAST role may use Medium if Low is unavailable and that limitation is recorded. High requires the same narrow explicit escalation if available on that selected model.
- **Other/future runtimes:** human approves a real exact model and verifies support for any mapped effort; generic profile is not an endorsement of any model. No inferred equivalence.

## Enforcement and evidence

- Run `python scripts/create_model_preflight.py --runtime RUNTIME [--developer GITHUB_NAME]` to create a blank, Git-ignored, developer/runtime-specific receipt under `.local/model_preflights/` with current policy SHA-256.
- Observe the *actual* main session and delegated FAST/BALANCED workers; collect sanitized local logs under `.local/`; populate your generated receipt, seal its local trace hashes with `create_model_preflight.py --seal`, and set PASS **only after human verification**.
- Run `python scripts/validate_model_policy.py --runtime-key DEVELOPER::RUNTIME` (or just `RUNTIME` during maintainer bootstrap). The initializer refuses `model_policy_validation PASS` without that current evidence; a generated adapter alone is insufficient.
- `scripts/sync_runtime_adapters.py` generates exact `model` + `effort` Claude subagents, exact `model` + `model_reasoning_effort` Codex agent TOMLs, and inheritance-safe Antigravity agent frontmatter. These are *best-effort local configuration*; main-session overrides, environment or invocation settings may take precedence. Inspect the actual delegated run before readiness.
- A policy edit invalidates the receipt automatically. Nobody silently swaps to a newer model or increases effort. Record actual High usage in the issue changeset when explicitly justified and supported.
- Review independence comes from new context and another human for substantial PRs; a different model is optional, **not** a requirement that overrides a teammate's permitted model.

Provider model availability and runtime syntax should be rechecked during local initialization. This project makes **no claim** that changing a static config can enforce provider account restrictions or that this packaged ZIP already tested a live Claude/Codex/Antigravity session.

The bundled `model-policy-governor` skill is assigned to the Lead, project initializer and release reviewer. It is not eagerly injected into every worker.
