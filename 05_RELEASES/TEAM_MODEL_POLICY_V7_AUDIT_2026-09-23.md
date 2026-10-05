# Team model-policy v7 — release audit

Date: 2026-09-23. Scope: portable team workflow / runtime model routing / generated subagents. Supersedes v6 model-routing defaults only; does not overwrite current game design or earlier history.

## What is canonical

- `AGENTS.md` remains the single master project contract. `.agents/skills/` remains the only tracked active skill tree. The project maintains 21 vendor-neutral role contracts and 63 curated skill entries (25 bundled, 38 external pending per-project approved installation on a new clone).
- `08_TOOLCHAIN/TEAM_MODEL_POLICY.json` governs allowed models and reasoning; `scripts/model_policy.py` resolves all six model classes without changing roles or game state.
- Shared team model policy: Claude Code uses exact configured `claude-opus-5-5` with Low or Medium only; Codex uses exact `gpt-6-sol`, Low/Medium and exceptional issue-specific High limited to DEEP/REVIEW_DEEP; Antigravity prefers an observed available `gemini-3.8-flash`, defaults Medium and must directly verify supported effort controls. Other runtimes must establish human-approved bindings. Medium is the default for all but narrowly scoped FAST work.
- Model policy is a project preference and runtime validation requirement, NOT an organization-wide provider account restriction. Missing/unselectable model or effort blocks the corresponding local runtime gate instead of silently substituting another model. An active model and separate delegated execution traces, plus operator confirmation, are required for local readiness; static adapter files alone cannot certify a runtime.

## Reconciliation fixes and conflict prevention

1. Generated Claude agents specify model and effort. The Studio operator does *not* use a fixed built-in tool allowlist, which could otherwise hide dynamic Roblox MCP tools. Other specialists receive narrower tool selections and bounded eager skill loading.
2. Generated Codex agents explicitly select GPT-6 Sol with Medium baseline and Low for FAST. High requires `scripts/prepare_codex_high.py` with a GH issue, eligible DEEP/REVIEW_DEEP role, meaningful justification and a named human approver. The generated temporary agent is ignored and survives normal adapter sync; close the exception when the issue ends.
3. Antigravity agents inherit a locally verified session model. Static custom-agent format cannot prove their actual effort setting. Initialization requires observations from the active workspace and a delegated agent; missing evidence leaves the runtime unvalidated.
4. Runtime adapter regeneration tracks full hashes of its own output and refuses to overwrite changed or conflicting local files, custom agents or Codex settings. It rejects symlinked output paths and symlinks within skill mirrors. Regeneration does not remove unrelated user agents or approved temporary High variants.
5. `scripts/validate_team.py` derives protected infrastructure paths from the shared `TEAM_POLICY.json` rather than maintaining a contradictory second master list. Model configuration, generated adapter infrastructure and initialization scripts are owned by integration review.
6. Team global initialization uses per-developer local runtime receipts. The shared project is initialized once; subsequent developer runtimes are validated separately. A global finalization now reports Git staging/commit errors instead of falsely reporting a successful checkpoint.
7. The existing GitHub Issue-linked immutable proposals, branch/PR controls, Rojo filesystem ownership, Studio MCP + separate live Rojo sync checks, disposable Studio playtests and visual/gameplay evidence requirements remain required. No automatic merges or live publishing have been added.

## Portable test evidence

- Repository, team and Rojo layout static validation, derived document check, Python compilation, model-policy unit checks and disposable request-to-review-to-checkpoint simulation: run as release gates.
- Negative checks include Claude model/effort mismatch and missing delegated traces; Codex invalid High escalation; generated agent YAML validity; regenerated adapter conflicts; symlink containment; integration-owned path edits on a feature branch; and global initialization refusing false successful Git commits.
- All executable test results recorded during release packaging must be rechecked from the extracted final ZIP. No simulated local test is evidence of real provider access, successful real upstream skill installation or connectivity to the user's Roblox Studio Baseplate.

## Remaining real-world gates

The portable scaffold remains `INITIALIZATION_REQUIRED`. The repository has **not** been pushed to a specific game repository in this release. On each developer workstation, the runtime must verify selected main and delegated models, install or verify pinned Rokit/Rojo/StyLua/Selene, connect to the *correct* open Roblox Studio place through the selected MCP client, independently connect its Rojo Studio plugin, and complete the reversible sync/playtest/screenshot test. The actual game's features must still pass their separate functional and visual reviews and the team's human PR/merge approvals.

Use `TEAM_BOOTSTRAP_PROMPT.txt` first; then `TEAM_TASK_PROMPT.txt` with an approved GitHub Issue-linked update. Use `08_TOOLCHAIN/MODEL_POLICY_SETUP.md` for model policy and exception commands.
