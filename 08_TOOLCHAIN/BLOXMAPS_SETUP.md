# BloxMaps Production Adapter — v8.3.1 hardening

The bootstrap integrates the team fork `afkDen/bloxmaps` as a **pinned external capability**, not vendored source. This preserves the simple idea/update workflow, isolates its FSL-1.1-ALv2 license/dependencies, and keeps every AI runtime/model usable.

## Default boundary

- Priority: deterministic MapGen, Studio map builder, model/icon asset manifests, multi-section worlds.
- Optional: BloxUI blueprints/prototypes and quality/lint ideas.
- Human architecture gate: adopting Fusion/BloxUI runtime as a project's real frontend framework.
- Excluded from normal bootstrap: hosted BloxMaps website/cloud/account stack.
- No hosted AI key is required. Claude Design is **not** required. Visual work binds to the strongest real visual capability exposed by the active runtime.

Canonical pin and policy: `08_TOOLCHAIN/BLOXMAPS_INTEGRATION.json`.

## Install the isolated fork checkout

Readiness is always safe/read-only:

```powershell
python scripts/bloxmaps_adapter.py status
python scripts/team.py doctor
```

`READY` now requires the isolated checkout to be **clean**, in addition to matching the reviewed origin/ref and local MapGen prerequisites. A checkout with local edits is intentionally blocked from `smoke`/`generate`; reconcile it manually instead of executing code that no longer matches the reviewed pin.

After reviewing the fix plan, explicitly install the pinned fork:

```powershell
python scripts/team.py setup --developer YOU --runtime YOUR_RUNTIME --install-bloxmaps
```

Equivalent direct command:

```powershell
python scripts/bloxmaps_adapter.py install --confirm
```

The checkout goes under `.local/tools/bloxmaps/` and is ignored. It does **not** replace the game repo's Rojo 7.7.0 pin. BloxMaps keeps its own isolated toolchain expectations.

## Smoke test

```powershell
python scripts/bloxmaps_adapter.py smoke
```

This generates a deterministic no-library plan and writes ignored evidence under `.local/bloxmaps/`. It is not Studio proof.

Direct `generate` output is confined to `.local/bloxmaps/` or `04_CHANGESETS/`. This keeps agent-operated generation from becoming an arbitrary filesystem write primitive while still supporting ignored experiments and issue-local evidence.

## Agent workflow

For a world task, the Lead routes WORLD work to `content-production-worker` using `bloxmaps-world-production`. The worker first produces/reviews a deterministic plan, then uses Blender MCP for missing bespoke assets when appropriate, regenerates with the validated asset manifest, and only then asks `studio-operator` to build the accepted plan in a verified nonproduction place.

For UI, `frontend-worker` may use `bloxmaps-ui-accelerator` for blueprints/prototypes, but BloxUI/Fusion adoption is never automatic. Signature visual direction remains controlled by the project art/UI bible and provider-neutral `visual-design-orchestration`.

## Upgrade the pin

Never `git pull` the isolated checkout as an upgrade strategy. Review upstream/fork changes and licensing/dependencies first, run BloxMaps tests plus this adapter smoke test, then intentionally update the pinned commit in `BLOXMAPS_INTEGRATION.json` and corresponding tests/docs.
