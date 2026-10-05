---
name: blender-game-asset
description: Reference-driven Blender game-asset production for Roblox: measured blockout, modeling, topology, UV/materials, rig/animation when needed, export and round-trip validation. Use with the priority Blender MCP path when Blender-suitable asset work is approved.
---

# Blender Game Asset Production

Inspired by `majidmanzarpour/blender-game-skills` (MIT) plus the project's existing `blender-technical-art` rules.

## Gated pipeline
1. **Brief** — references, target dimensions, camera/read distance, style bible, triangle/material/texture budgets, pivot/collision/rig needs.
2. **Calibration/blockout** — correct scale and silhouette before detail. Capture measured renders.
3. **Primary/secondary forms** — preserve readable silhouette and modularity.
4. **Topology** — game-ready topology, normals, smoothing, naming and transform hygiene.
5. **UV/materials** — minimize material slots, texture memory and unnecessary unique maps; define Roblox-compatible PBR output.
6. **Rig/animation** — only if required; validate deformation and export conventions.
7. **Export** — deterministic FBX/glTF settings as appropriate, explicit units, pivots and manifests.
8. **Round trip** — reimport/check dimensions, orientation, materials, collisions, rig/animations and gameplay-camera appearance.

Blender MCP is the priority authoring path for Blender-suitable 3D asset work. Never install/connect it silently: the workstation/addon setup is a human decision gate. If the priority capability is unavailable, stop and report the missing readiness; use Roblox-native Parts/CSG or a manual Blender fallback only when the Lead/human explicitly chooses that alternative. Never pretend a mesh was created.
