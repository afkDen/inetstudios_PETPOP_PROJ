---
name: asset-production
description: Game asset production and sourcing. Use for art-direction-controlled sourcing, asset families, specifications, Poly Haven/Openverse/Creator Store search, Blender/glTF cleanup, provenance, licensing, import validation, and approval.
---

# Asset production

Follow: existing project asset → approved free source → Roblox-native/procedural build → local open-source generation/cleanup → only then consider new dependencies.

Every production asset needs provenance and visual/technical review. Prefer cohesive families. Check scale, pivot, collision, geometry, materials/textures, rig/animation suitability, performance, licensing, and Roblox import behavior.

Approved no-cost network sources: Poly Haven API (CC0, API attribution requirement) and Openverse for discovery/reference with per-item license verification. Use `python scripts/polyhaven_search.py <query>` or `python scripts/openverse_search.py <query>` and copy approved results into the asset provenance manifest before import. Approved no-API sources include Kenney and Quaternius subject to current license records.

## Enforced production acceptance
Record limitations of free providers honestly. Real signature-asset needs beyond current sources/local skill must be escalated to human art rather than filled with plain bricks. Validate the generated/imported assets in an actual game camera after lighting and material pass.
