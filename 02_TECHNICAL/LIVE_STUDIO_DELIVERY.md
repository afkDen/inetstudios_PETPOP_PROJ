# Task-time note for v8.5

This workflow is invoked **only when an approved task actually needs live Studio evidence**. v8 does not require a disposable Studio/MCP/Rojo session merely to submit an idea or perform repository-only planning. TASK.json controls whether this gate is required for final delivery.

# Live delivery to the **already open** Roblox Studio place

This is the operational guide for teams starting from a Baseplate and expecting work to appear **there**, not just as scripts in Git. It is mandatory for real game-visible tasks. Root `AGENTS.md` remains authoritative. It supplements `ROJO_WORKFLOW.md`, and no step authorizes production publishing.

## Two separate connections — both necessary for this repo-first workflow

**A. Official Studio MCP:** In Studio's Assistant → Manage MCP Servers, enable Studio as MCP server. In **Quick connect**, select the *actual running coding client*, e.g. **Antigravity**. Visual Studio Code is a **different client option**: enabling only VS Code does not prove Antigravity inherited MCP. Studio should show a green connected-client indicator. Restart Studio and your coding runtime if connection/tools do not appear. Do not trust the green indicator alone: directly invoke `list_roblox_studios`, `get_studio_state`, `search_game_tree` and safe read-only `execute_luau` in Edit mode. If multiple Studio windows exist, call `set_active_studio` for the user-confirmed target and repeat the read-only check. The official tools also include `screen_capture`, `start_stop_play`, `get_console_output`, input simulation and `subagent` playtest/explore; discover them in the runtime rather than hallucinating tool access.

**B. Rojo live sync:** From the CURRENT approved issue branch's repository root, run `python scripts/bootstrap_dev_tools.py --check`, then `rojo build default.project.json --output build/dev.rbxlx` and `rojo serve default.project.json`. The pinned Rojo v7 Studio plugin is a **separate** install/connection. In the *same* human-confirmed open Baseplate/test place, open Rojo plugin and **Connect** to the server, preview its managed subtree before authorizing sync. Verify that live Studio contains `ReplicatedStorage/GameShared`, `ServerScriptService/GameServer`, `StarterPlayer/StarterPlayerScripts/GameClient` with a non-destructive read-only tree inspection. The Rojo server is normally localhost port 34872; never point a shared server at the wrong test place.

Enabling MCP without Rojo sync means a repo-only agent can write files but **they won't appear in that open Studio place**. Running `rojo build` creates an output place file, but doesn't modify the already-open Studio window. Opening the built place file in Studio is a separate alternative to live sync, not evidence of changing the intended open Baseplate.

## Target lock before any edits

1. Human specifies intended development place/Studio window and approves any mutations. An unpublished Baseplate can legitimately lack a published place ID; the operator must verify its live instance ID and name. In a published test place prefer a verified `servePlaceIds` allowlist in `default.project.json` after a reviewed infrastructure PR. Back up the original world/terrain first.
2. Pin the issue branch and commit for the test. Never sync an unknown branch, unsaved conflicting Studio scripts or live production place as a default.
3. Use Studio MCP only to **inspect and test managed scripts**; edit them in `src/` and allow Rojo to sync. MCP may own a separate agreed Studio-only world/terrain operation with an explicit asset/backup handoff and human approval. Avoid concurrent dual writers on the same managed subtree.
4. Prove sync with a harmless disposable marker inside one mapped `src/` subtree, confirm its live Instance path with MCP, remove marker and verify it disappears. Capture actual MCP tool responses and operator record. Never use the live production experience for this test.

## Scope limitation of the bundled Rojo project

`default.project.json` initially maps **only three script folders**: `src/server`, `src/shared`, `src/client`. It does not import an environment into Workspace or prebuilt screens into StarterGui. For instance, an `src/client/*.client.luau` screen builder creates its GUI **during a client play session**; it need not show in Studio's Edit-mode Explorer. A hand-built world remains Studio-owned until a reviewed, backed-up migration adds Rojo ownership for a defined subtree. Do not imply new map files appear in the Baseplate from the current mapping.

## Later: reviewed filesystem-owned world (opt in, not automatic)

To share new maps without relying on a single developer's unsynced Studio world, `templates/rojo-world-opt-in.project.json` illustrates a **future**, separately approved `Workspace/VersionedWorld` subtree mapped to `src/world`. Do **not** use this template as the default project yet. First back up the Baseplate/place, agree which instances are allowed to move, create the source folder and convert reviewed native models (`.rbxmx`, `.rbxm` or suitable `.model.json`) into that ownership boundary. Run a disposable-place Rojo build, preview the live plugin sync, inspect unknown-instance preservation and record rollback. Large external FBX/glTF sources need Roblox import, asset IDs and a manifest; not every mesh/terrain property live-syncs via Rojo. Terrain and other Studio-only content keep separate backups/owners until explicitly migrated. A PR that changes the world mapping needs studio delivery and integration-owner approval.

## Actual playtest exit gate

Use `start_stop_play` or the available official playtest subagent on the **locked target Studio instance**, perform the player's intended action (mouse/keyboard/character navigation where available), capture `get_console_output` for the correct client/server contexts and `screen_capture` of actual game pixels. Check real UI state, real gameplay feedback and expected persistence/multiplayer behavior where applicable. Stop play, revert disposable artifacts and record resulting Studio/asset ownership state. A successful Python validator, native Rojo build, image existing on disk or agent's text assertion **is not** proof of an actual playtest.

Start a draft with `python scripts/prepare_studio_delivery.py --issue <ISSUE>` after the issue changeset exists; the draft defaults to PENDING and never supplies fictional evidence. Sanitize runtime logs for usernames, auth tokens, absolute paths and private Studio details before committing evidence; preserve enough non-secret command/result context for independent review. Record actual results using `templates/STUDIO_DELIVERY_TEMPLATE.json` in the issue changeset as `STUDIO_DELIVERY.json`. The draft records the task's active scope revision. If scope later advances, create/refresh Studio evidence for the new revision; `scripts/validate_studio_delivery.py` rejects a v8.5 receipt whose `scope_revision` no longer matches TASK.json. The required `STUDIO_DELIVERY` receipt is checked by `scripts/validate_studio_delivery.py`; PR quality validation requires it for changed game code/assets. It verifies consistency and file evidence, not the truth of arbitrary agent claims: a second human must confirm the intended place, screen results and gameplay before merging. If MCP and/or Rojo cannot be connected, stop with `LIVE_DELIVERY_BLOCKED` or ask to open an **incomplete draft PR**, not a passing feature.

## First workstation initialization (separate from per-feature delivery)

In v8, this same-place handshake is normally performed when the approved task first needs live Studio delivery, not as a prerequisite to idea capture. Historical/full-runtime initialization may still keep ignored `.local/INIT_STUDIO_PREFLIGHT.json` evidence, but every Studio-dependent feature needs its own issue-local `STUDIO_DELIVERY.json` with fresh tests; an old startup test is never a substitute for current feature acceptance.
