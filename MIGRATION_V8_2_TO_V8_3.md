# Migration — v8.2 Capability Hardened → v8.3 BloxMaps Integrated

v8.3 keeps the public `team.py` workflow and task provenance model intact. The migration primarily adds production capabilities and intake references.

## What changes

- workflow metadata advances to `streamlined-v8.3`; v8/v8.1/v8.2 task records remain readable;
- `afkDen/bloxmaps` is pinned as an **external ignored checkout**, never vendored into generated games;
- `content-production-worker` gains deterministic BloxMaps WORLD mode and Blender→asset-manifest bridging;
- `frontend-worker` gains optional BloxUI blueprint acceleration without automatic Fusion/BloxUI adoption;
- visual design becomes provider-neutral (`design.visual`), so Claude Design is optional rather than required;
- `team.py idea/update --reference ...` can preserve URLs and copy local reference files into the issue changeset for collaboration;
- workstation doctor reports BloxMaps readiness and setup provides an explicit `--install-bloxmaps` action.

## Existing games

Do not rewrite existing `USER_REQUEST.txt` or task histories. Merge the bootstrap/toolchain update through a reviewed integration branch, run the full repository tests, then each developer reruns `team.py setup`. BloxMaps is installed per workstation only when world-generation work needs it.

## Existing UI code

No UI framework migration is implied. BloxUI runtime adoption requires a separate human-approved architecture decision. Existing custom Roblox UI remains valid and preferred for signature surfaces when that matches the project's direction.
