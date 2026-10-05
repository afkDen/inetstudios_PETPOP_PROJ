# v8.3 BloxMaps Integrated — Final Audit

**Version:** `v8.3-bloxmaps-integrated`  
**Date:** 2026-10-04

## Executive result

v8.3 preserves the simple v8 human path — setup → idea/update → one Issue → one branch → design → human approval → implementation/evidence → one draft PR → second-human review → merge — while adding BloxMaps as a pinned external production capability and removing any canonical dependence on Claude Design or another named visual vendor feature.

## BloxMaps review and integration boundary

Reviewed public source/fork: `afkDen/bloxmaps` pinned to commit `40917c59954a3586634641306482031ab128a007`, matching the initial public BloxMaps release reviewed in this task. The source is FSL-1.1-ALv2/Fair Source, so v8.3 deliberately does **not** vendor it into the reusable bootstrap or generated game repositories. The adapter clones it only into ignored `.local/tools/bloxmaps/` after explicit approval.

Priority components are MapGen, the Studio map builder, model/icon asset manifests and multi-section worlds. BloxUI blueprints are optional acceleration. Full BloxUI/Fusion runtime adoption is a project architecture decision, not a bootstrap default. The hosted website/cloud/account stack is excluded from the normal workflow.

## Model/runtime portability

`design.visual` is semantic. A capable runtime may satisfy it with Claude Design, another native visual workspace, image generation/editing plus inspection, Roblox Studio prototypes, BloxUI blueprints, or a structured mockup/render loop. The workflow retains the same approval and evidence requirements regardless of provider. Canonical role contracts remain provider/model-neutral.

## Agent efficiency

The role catalog remains 10 roles with a hard maximum of 3 active subagents. BloxMaps and Blender MCP are tools used by existing workers, not new agents. Typical world work remains Lead + Content Production Worker (+ Creative Director if needed), followed by a sequential fresh Assurance Reviewer.

## Collaboration improvements

`team.py idea/update` now accepts repeatable `--reference` arguments. URL references are recorded verbatim. Local regular files up to 20 MiB are byte-copied into the issue changeset with SHA-256 provenance and a `REFERENCES.md`, making visual/design references shareable with teammates without relying on chat history.

## Setup/dependency hardening

The workstation doctor now reports BloxMaps readiness separately from core project readiness. `team.py setup --install-bloxmaps` explicitly installs the pinned fork checkout; it never silently installs it. BloxMaps' own Rojo/toolchain stays isolated and cannot downgrade the game's pinned Rojo 7.7.0. Python >=3.11 and Luau are required for local MapGen; Lune is only needed for BloxUI-server paths.

## Validation performed

- Python compilation for modified scripts: PASS.
- Derived role/skill routing regeneration/check: PASS.
- Full reusable-bootstrap unit suite: **180 tests PASS** after integration.
- Provider-neutral role/skill registry validation is included in that suite.
- BloxMaps adapter status/doctor behavior tested in missing-checkout mode: PASS.
- Live BloxMaps MapGen execution was **not** claimed in this environment because outbound DNS to GitHub is unavailable and Luau/BloxMaps were not installed here. Workstation smoke remains a real setup gate (`python scripts/bloxmaps_adapter.py smoke`).
- Live Roblox Studio / Blender MCP evidence was not claimed.

## GitHub fork write limitation during this task

The connected GitHub integration could read `afkDen/bloxmaps` and reported repository admin metadata, but write endpoints returned `403 Resource not accessible by integration` for both Issue creation and branch creation. Therefore this task did not claim any fork-side commit/PR. The v8.3 integration is intentionally compatible with the current pinned fork without requiring fork modifications.

## Release recommendation

Use v8.3 as the next reusable bootstrap. Keep BloxMaps source isolated and pinned, upgrade it only after explicit upstream/fork review, and keep visual-design execution provider-neutral.
