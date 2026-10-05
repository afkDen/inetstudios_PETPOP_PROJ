---
name: bloxmaps-world-production
description: Deterministic Roblox world/layout production through the pinned afkDen/BloxMaps fork, with plan review, asset-manifest bridging, Studio safety and evidence.
---
# BloxMaps World Production

Use this skill for map/world generation, section expansion, procedural layout studies, or feeding Blender-authored asset families into BloxMaps. BloxMaps is a **tool capability, not an extra subagent**.

## Contract
- Canonical integration: `08_TOOLCHAIN/BLOXMAPS_INTEGRATION.json`.
- Use only the pinned fork/ref unless a reviewed supply-chain update intentionally changes it.
- The isolated checkout must be clean before execution. A matching commit with local modifications is not reviewed code and is therefore not MapGen-ready.
- Run from the isolated `.local/tools/bloxmaps` checkout. Never vendor the FSL source into the game repo.
- Default local environment includes `BLOX_NO_OVERLAY=1`. Hosted generation/BYOK is unnecessary.
- Write generated plans only under `.local/bloxmaps/` or the active `04_CHANGESETS/GH-.../` directory.

## WORLD flow
1. Read the approved world/level brief and existing art bible.
2. Decide whether deterministic procedural planning is actually helpful; handcrafted hero spaces may not benefit.
3. Use a fixed prompt + explicit seed and write the resulting plan to task-local ignored evidence first.
4. Inspect `meta.notes`, counts, layout/theme, markers, terrain, paths and obvious composition problems before Studio mutation.
5. If the procedural kit is visually insufficient, produce missing assets through the Content Production Worker + Blender MCP, validate/export them, build a BloxMaps asset manifest, then regenerate the **same seed** so layout comparisons remain meaningful.
6. Treat generated plans as candidate artifacts. Iterate/regenerate or hand-polish; never equate generation with acceptance.
7. Build an accepted plan in a verified nonproduction Studio target through `studio-operator`; collect screenshots/playtest/console evidence.
8. Fresh assurance review judges navigation, readability, scale, gameplay space, art coherence and performance.

## Asset bridge
Blender asset brief → measured model → GLB/OBJ export → provenance/license entry → BloxMaps pack validation/manifest → deterministic regeneration → Studio import/build → round-trip verification.

## Stop / ask
Ask the Lead/human before adopting a new BloxMaps ref, introducing licensed packs that cannot be shared, using hosted/BYOK services, replacing a handcrafted approved area with procedural generation, or changing the game's world architecture materially.
