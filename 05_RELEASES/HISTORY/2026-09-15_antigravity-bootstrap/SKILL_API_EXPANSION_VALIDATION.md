> **HISTORICAL / SUPERSEDED.** This record describes the 2026-09-15 Antigravity-oriented bootstrap and is retained only for traceability. Current authority is root `AGENTS.md`, `06_PROJECT_STATE/CURRENT_STATE.md`, `06_PROJECT_STATE/FINAL_SCAFFOLD_REVIEW.md`, and `08_TOOLCHAIN/PORTABILITY_ARCHITECTURE.md`.

# Skill / API Expansion Validation — 2026-09-15

Status: PORTABLE BOOTSTRAP PASS; WORKSTATION INITIALIZATION REQUIRED

## Packaged skill architecture
- Project-native active skills before initialization: 16
- Approved upstream skills selected for automatic installation: 38
- Expected active workspace skills after successful initialization: 54
- Project-authored fallback adapters retained outside the active skills directory: 26
- Custom agents: 17 (including the narrow live-MCP `studio-operator`)
- Agent↔skill routing manifest: PASS
- Custom-agent frontmatter scopes (tools/skills/rules/model/policy): PASS
- Reviewer direct-write capability isolation: PASS
- Project-native skill frontmatter/static checks: PASS
- Python initializer/client compile: PASS
- Intake/unit tests: PASS
- Repository static validator: PASS
- Disposable local pipeline simulation: PASS
- Full initialization state-machine simulation with a fake `npx` installer: PASS, including automatic install → discovery-gate recording → final READY commit → clean Git verification

## No-cost integrations
- Poly Haven API client: packaged; no authentication required.
- Openverse API client: packaged for discovery/reference; original asset license must still be verified.
- Roblox Open Cloud skill: conditional; credentials intentionally not configured until a concrete workflow needs them.
- Blender / glTF-Transform / FFmpeg: optional local tools detected during initialization.

## Paid API policy
Meshy and Hyper3D/Rodin are not approved as default bootstrap integrations because API use is credit-metered. No paid generation API is required to reach `READY FOR GAME IDEA`.

## Upstream skill installation
Approved upstream packs are now a **required first-run initialization gate**, not an optional manual sync. `scripts/initialize_project.py` invokes the pinned Agent Skills CLI `skills@1.5.26` through `npx`, explicitly targets the Antigravity agent, and installs approved skill names at project scope with copied files, audits the resulting trees, hashes each complete installed skill tree, quarantines provenance/hash drift or blocking executable findings, and requires a separate semantic review bound to the exact install-manifest hash before readiness.

The packaging sandbox cannot reach GitHub from the container, so real upstream downloads are intentionally deferred to the user's workstation. The installer logic was exercised end-to-end with a deterministic local `npx` test double; real network installation must still succeed during workstation initialization.

## Remaining real-environment gate
The official Roblox Studio MCP and Antigravity-native discovery checks can only be honestly verified on the development workstation. `INITIALIZE_PROJECT.md` handles those gates and refuses readiness without direct evidence.
