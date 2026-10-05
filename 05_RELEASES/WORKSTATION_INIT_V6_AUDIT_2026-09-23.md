# Workstation initialization v6 — finalization and evidence boundaries

## Why v6 exists

v5 contained a Studio disposable-test phase in `INITIALIZE_PROJECT.md`, but individual dependency installation and real Rojo plugin-to-open-Baseplate synchronization were not part of one enforced full-runtime initialization sequence. Consequently, a teammate could mistake a repository-only Rojo build or an MCP config file for proof that work appeared in their open place.

## Changes

- `TEAM_BOOTSTRAP_PROMPT.txt` is the single first-use entrypoint for each person, regardless of AI model/runtime. Global shared skill bootstrap still belongs only to the integration owner; joining teammates validate locally, never rewrite tracked global state.
- `scripts/workstation_preflight.py` checks the pinned Rojo, StyLua and Selene versions and **runs a native Rojo build**. After explicit user approval, it can run already-installed Rokit and optionally install the Rojo Studio plugin; it never silently downloads a system-wide installer. Hash receipts go only under ignored `.local/`.
- `templates/INIT_STUDIO_PREFLIGHT_TEMPLATE.json` and `scripts/validate_initialization_studio.py` define staged, local-only MCP, same-place Rojo marker appearance/removal, and disposable real playtest/console/viewport/human-confirmation evidence.
- Full local readiness now requires `developer_toolchain`, `roblox_studio_bridge`, `rojo_live_sync` and `studio_disposable_test`. Recording a live gate PASS validates the relevant local receipt stage. Revalidating full readiness checks the complete receipt again.
- The startup playtest is explicitly **not** reused as acceptance evidence for later gameplay, UI or world features. Each issue still needs new `STUDIO_DELIVERY.json`, quality evidence and independent review.

## Tests and limitations

Portable static repository/team/Rojo checks, Python unit/negative tests and the disposable *repository* development simulation were rerun before packaging. The new tests include negative cases for wrong runtime, missing actual MCP probe files, missing either Rojo marker phase, missing playtest/human verification, missing binaries and a native build that reports success without creating an artifact. Their fake images and tool outputs are clearly test fixtures and make no claim to authenticate real MCP activity.

**A real native Rojo build and real Studio connection could not be run in this packaging environment.** Only the actual human-confirmed workstation can complete the live gates. The package remains `INITIALIZATION_REQUIRED` until legitimate direct tests pass there. A genuine runtime Studio operator plus human verification is necessary; a receipt validator alone cannot prove that a screenshot or a text file came from Studio. On new coding sessions, recheck read-only active Studio target and branch-specific Rojo connection; redo full initialization if relevant tool/runtime/target state changes.

## Operational entrypoint

Paste the complete `TEAM_BOOTSTRAP_PROMPT.txt` in the **active coding runtime** before the first game idea. It should stop for permission only when Rokit/plugin installation or selection of a safe open Studio place is required. When all shared and local gates pass, use `TEAM_PROPOSAL_PROMPT.txt` or `TEAM_TASK_PROMPT.txt` for normal tasks.
