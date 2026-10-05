---
name: studio-place-integration
description: Bind a specific open Roblox Studio test place to a filesystem-first Rojo working branch and a real Studio MCP client; verify two separate connections, run visible synced code and real playtests, and return an issue-local delivery receipt. Use at the start of any game-code task that expects edits to appear in an already-open Baseplate or development place.
---

# Studio Place Integration — Mandatory live-task preflight

Read `AGENTS.md` and `02_TECHNICAL/LIVE_STUDIO_DELIVERY.md`. Before game-visible implementation, ask the Studio operator to confirm **the correct open Studio window**, whether the client connected is the **current coding runtime** (Antigravity, not just Visual Studio Code), and whether the **separate Rojo plugin** is connected to `rojo serve default.project.json` from the CURRENT issue branch. No connected bridge or wrong place means `LIVE_DELIVERY_BLOCKED`, not a repository-only claim of completion.

1. Record the intended human-approved test place and its actual `list_roblox_studios` result. Where several windows are open, call `set_active_studio` and re-inspect. For an unpublished Baseplate, a blank place ID can be legitimate; require explicit confirmation by place name and Studio instance ID instead. Never infer place identity from a repository URL.
2. MCP health check: `get_studio_state`, `search_game_tree` and safe read-only `execute_luau` (Edit). Save actual tool results, not invented notes. The Studio MCP quick-connect client and Rojo plugin are different connections.
3. Rojo live-sync check: run native Rojo build, then `rojo serve default.project.json`. Connect the matching plugin to the chosen Studio place, preview sync, and confirm `ReplicatedStorage/GameShared`, `ServerScriptService/GameServer` and `StarterPlayer/StarterPlayerScripts/GameClient` in the live data model. Use one disposable marker in a managed subtree only after human consent; delete it and verify the change reversed. Do not have Studio MCP and Rojo simultaneously author the same managed script.
4. The starter project does **not** map Workspace, StarterGui or a persistent map. UI under `src/client` must actually create/wire UI on the client at play time; 3D worlds not migrated to Rojo remain Studio-owned with an assigned owner and a backup. If the request expects a map persisted in Git, produce a reviewed new asset/ownership plan first.
5. On the exact target place, run the gameplay scenario through `start_stop_play` or the available playtest subagent, simulate required character/UI inputs when available, capture `get_console_output`, and take real `screen_capture` images. Test more than a no-op script.
6. Record a `STUDIO_DELIVERY.json` from the issue-local template, the git commit, instance name/ID, intended place, MCP tool receipt, Rojo sync receipt, actual run evidence and human acknowledgement. The validator checks evidence shape; a human verifies authenticity and visual quality. Report `BLOCKED` without the actual capabilities.

Do not use `rojo build` alone as evidence that a developer's open place was modified. Do not publish a live production place during ordinary testing.
