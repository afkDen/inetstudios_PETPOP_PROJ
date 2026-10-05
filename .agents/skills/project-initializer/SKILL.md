---
name: project-initializer
description: Prepare or repair the streamlined v8 Roblox team checkout, shared skills and local developer runtime without forcing live Studio validation before idea capture.
---
# Project Initializer

1. Read `AGENTS.md`, `INITIALIZE_PROJECT.md`, TEAM_POLICY and current initialization state.
2. Verify this is a prepared/cloned game checkout with the expected origin. Never treat the reusable template as a live game.
3. Normal developer entry: `python scripts/team.py setup --developer <user> --runtime <runtime>`.
4. Reuse accepted shared skills and valid local tools. Generate only the runtime adapters/personal profile needed for the current developer.
5. If the shared external skill lock is genuinely absent, only the maintainer may use `team.py setup --initialize-shared-skills --confirm-shared-change`; review the resulting lock/audits before shared acceptance.
6. Ask before installing project tools or the Rojo Studio plugin.
7. Do not require live Studio just to capture an idea. When an approved task later needs Studio, use `LIVE_STUDIO_DELIVERY.md` for fresh exact-place MCP/Rojo/playtest evidence.
8. Before actual delegated implementation/review, validate the runtime/model policy required by the roles being used. Do not fake readiness from static adapter files.

Never process a real game idea as part of shared skill installation, never copy another developer's `.local/`, and never publish/merge automatically.
