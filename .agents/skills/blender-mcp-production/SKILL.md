---
name: blender-mcp-production
description: Priority Blender MCP authoring workflow for Roblox-ready 3D models, props, modular environment assets, rigs, materials, and exports with target verification, measured gates, provenance, and round-trip validation.
---

# Blender MCP Production

Use for Blender-suitable 3D asset work. In this bootstrap Blender MCP is a **priority authoring capability**, not a last-resort optional extra.

## Safety and ownership handshake

Before any mutation, record/verify:

- exact `.blend` file and scene;
- owned collection/object prefix;
- reference assets and license/provenance;
- target Roblox scale and orientation;
- export directory and format;
- polygon/material/texture budget;
- whether rigging/animation is required;
- one active writer for the owned Blender scene area.

Blender MCP can execute Python inside Blender. Treat it as privileged local authoring. Never install/upgrade the MCP/addon, fetch paid/licensed assets, change unrelated files, or connect external services without the required human decision gate.

Bootstrap defaults: keep the bridge on `localhost`, set `BLENDER_MCP_SAFE_MODE=1`, and set `DISABLE_TELEMETRY=true`. Do not disable safe mode, expose the socket remotely, or enable paid/network model-generation providers without a named human decision.

## Production loop

1. **Brief** — category, references, target dimensions, camera/gameplay size, budgets, inferred details.
2. **Calibration** — units, origin/pivot, axes, reference planes, collection ownership.
3. **Blockout** — primary masses only. Compare silhouette/proportions before detail.
4. **Forms** — secondary forms; render fixed review views and correct measurable deviations.
5. **Topology + UV/materials** — game-ready geometry, material consolidation, texel strategy.
6. **Rig/animation** — only when required; verify deformation and sockets/pivots.
7. **Export** — deterministic naming, manifest, scale/pivot/collider notes.
8. **Round-trip** — reimport into clean Blender/Roblox staging context and verify what actually arrives.
9. **Roblox acceptance** — size, pivot, collision, material appearance, draw/triangle/texture budget, animation behavior, LOD where relevant.

Prefer reproducible scripts/operations for complex repeated edits. Save source `.blend` and build/export notes under the project asset-production structure.

## Evidence

Return review renders/screenshots, measured mismatches/fixes, final source/export paths, manifest, provenance/licenses, budget summary, and Roblox import/live evidence when acceptance requires Studio.
