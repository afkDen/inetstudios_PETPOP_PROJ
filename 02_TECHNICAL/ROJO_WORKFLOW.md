# Filesystem-first Roblox source authority (Rojo v7)

`AGENTS.md` controls behavior; `TEAM_PROTOCOL.md` controls collaboration. This file defines **which tool owns which game subtree**. Keep a single writer and a single sync authority per managed subtree. If the existing live place uses a different hierarchy, reconcile it in a reviewed infrastructure PR and a disposable Studio place **before** the first real sync.

## Source of truth

- **Git/Rojo** owns `src/server/**` → `ServerScriptService/GameServer`, `src/client/**` → `StarterPlayer/StarterPlayerScripts/GameClient`, and `src/shared/**` → `ReplicatedStorage/GameShared`. `default.project.json` is the only default project mapping. Every developer builds/syncs only their own working branch and development place. Do not edit the same managed script via Studio MCP/Script Sync and Rojo concurrently; back-port deliberate Studio edits into source files via reviewed Git changes.
- **Git** owns game design, approved proposal text, Lua/Luau tests, project config, skills and manifests. GitHub `main` is the only accepted integrated state; branch-local changesets hold work-in-progress.
- **Studio, under human ownership**, initially owns manually sculpted terrain, hand-built Workspace scenery, visual/animation editing and experience settings not yet converted into source assets. Those edits need a clear owner, separate development place, backup and integration record. Do not claim this starter Rojo layout versions the whole experience.
- **Asset manifests + Git LFS when needed** record source/approved binaries, licenses, content hashes, Roblox IDs and import status. Never commit API keys, DataStore data or a live production place full of secrets.

## Toolchain and checks

- `rokit.toml` pins Rojo 7.7.0, StyLua 2.5.2, Selene 0.31.0. Follow `02_TECHNICAL/DEPENDENCY_BOOTSTRAP.md`: manually review/install Rokit, run `python scripts/bootstrap_dev_tools.py --install`, and explicitly opt in to `--install-plugin` for the matching Rojo Studio plugin. Run `--check` to verify versions; never claim manifest=installed. Do not silently install a newer Rojo/plugin version on each workstation.
- Static: `python scripts/validate_rojo_layout.py`. This catches unauthorized new filesystem-to-Studio mappings and folder ownership drift; it is **not** an actual Rojo build.
- Native: `rojo build default.project.json --output build/dev.rbxlx`. Run locally and in CI where the pinned CLI exists. If native build fails or is unavailable, mark it PENDING/FAILED rather than claiming PASS.
- Live: `rojo serve default.project.json`, connect the matching Rojo plugin to a **personal test place**, inspect the patch preview, then run relevant Studio/playtest/console/multiplayer checks. Use the studio-operator for inspection and tests; shared experience edits are a separately authorized integration step.
- `servePlaceIds` can be set after the team has verified its intended test place IDs, to guard against syncing the wrong place. Do not guess or hardcode production IDs into a scaffold.

## Add more filesystem coverage gradually

Only after the team proves the three initial script subtrees should it expand to Rojo `.model.json` files, generated UI, place templates, text-based assets or reviewed binary place snapshots. Every expanded subtree needs a named Git/Studio owner, a rollback plan and a CI build check. Existing visual content should first be backed up and compared in a disposable place; avoid blanket sync to an unknown production universe.

Rojo 7.7 also introduces experimental syncback functionality. Do not make automated syncback part of the default workflow until the team has reviewed its actual effects and loss/conflict behavior on the game's own test place.

## Existing open Baseplate is not automatically synchronized

For the official Studio MCP and **separately installed Rojo plugin** two-connection workflow, target lock, live sync marker, run-time-generated GUI and real Studio test evidence, see `02_TECHNICAL/LIVE_STUDIO_DELIVERY.md`. This is mandatory for game-code features expected to appear in an already-open Baseplate; `rojo build` emits a file but does not live-modify that Studio window.

## Game quality is separate from source sync

A successful Rojo build only checks assembly. Read `02_TECHNICAL/PRODUCTION_QUALITY_CONTRACT.md`: visual prototypes are stage-labeled and require distinct art, playable Studio and UI interaction proof before PR acceptance.
