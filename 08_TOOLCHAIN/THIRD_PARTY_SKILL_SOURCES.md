# THIRD-PARTY SKILL SOURCES

Last reviewed: 2026-10-05

The first-run initializer automatically installs a curated set of approved upstream skills into `.agents/skills/`. It does not perform an unbounded marketplace search during bootstrap.

## Required initialization sources

### nonlooped/roblox-suite — MIT
- Role: primary Roblox-specific external skill suite.
- Pinned source: `nonlooped/roblox-suite#c914ce65470a6eb1b28000b8c58d5543b48760ca`.
- Selected skills are explicitly listed in `EXTERNAL_SKILLS.json`.
- Reason: current Roblox API practices, server/client boundaries, persistence, UI, animation/VFX/audio, monetization, Open Cloud, teleportation, testing, Rojo, and official Studio MCP usage.

### gamedev-skills/awesome-gamedev-agent-skills — Apache-2.0
- Pinned source: `gamedev-skills/awesome-gamedev-agent-skills#d4b0e35550c55ae70bdfcab4ef5a0e94610438a9`.
- Role: engine-neutral game-development disciplines plus Roblox Studio workflow.
- Selected disciplines are explicitly listed in `EXTERNAL_SKILLS.json`.
- Includes its router plus art/assets, AI, procedural generation, dialogue/save systems, audio, shaders, physics tuning, level design, input, game feel, camera, UI/UX, and performance.

### magnus919/agent-skills — MIT
- Pinned source: `magnus919/agent-skills#affec9d8cba35a3b8d632a64ab547ea8fcc53380`.
- Role: cross-project QA, secure engineering, documentation, and ADR methodology.
- Selected skills: `qa-methodology`, `secure-software-engineering`, `technical-documentation`, `adr-authoring`.
- `systematic-debugging` is no longer installed from this source in v8.4; a project-authored Roblox/usage-budget adaptation is bundled instead, while retaining pinned source attribution.

## Reference-only sources

### ohzw/roblox-dev-skills — MIT
Useful reference for Studio-MCP-native object/map-building procedures. Do not replace the official Roblox Studio MCP bridge with a redundant bridge unless a demonstrated gap appears.

### MaksPyn/polyhaven-skill — selective reference
Useful reference for richer Poly Haven API/file-selection/download workflows. The project ships its own dependency-free discovery client and provenance gates.

### Blender game-asset references — selective reference
Reference-driven modeling guidance is adapted into the bundled Blender production skills. Blender MCP itself is a priority authoring capability for Blender-suitable 3D work; it remains privileged because it can execute Python and mutate local scenes/files.


## v8.2 reviewed design/authoring references

These sources are **not auto-installed** by ordinary project setup. v8.2 ships project-authored Roblox adaptations or optional capability guidance so the normal skill tree stays self-contained and audited.

### pbakaus/impeccable — Apache-2.0
- Reviewed lineage; current audit also checked upstream through `6e802bd0ed99f53180e2359fddab6da8d97970d9`.
- Used as inspiration for `impeccable-ui`: hierarchy, anti-generic critique, token/system polish.
- Do not blindly apply website minimalism to game HUDs; preserve approved dimensional Roblox art direction.

### emilkowalski/skills — MIT
- Reviewed snapshot: `e8a175de22ae1e49370fc144c1f3bb9aeedf988d`.
- Used as inspiration for `interaction-motion`: easing, timing, interruptibility and motion review.
- Web/React implementation details are excluded; Roblox primitives remain authoritative.

### Leonxlnx/taste-skill — MIT
- Reviewed snapshot: `ce26fc25c0e5e8cab638f883de62d9a86ee5e45b`.
- Used as inspiration for `design-taste`.
- Any instruction that would simulate tool execution/evidence is excluded.

### anthropics/skills — source reference
- Frontend design reference reviewed around `8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4`.
- Used only as design-method reference; no vendor runtime assumption is made.

### majidmanzarpour/blender-game-skills — MIT
- Reviewed snapshot: `f0ef29385a03de139957e6f700b801cdc00b7e29`.
- Reference for the project-authored `blender-game-asset` gated modeling pipeline.

### ahujasid/mcp-for-blender — priority 3D authoring capability
- Pinned reviewed snapshot: `60d2a31b4632a7bc178f3dd636f7e68dfb5c8ae4`; package `mcp-for-blender==2.1.3` (MIT).
- Bootstrap requires Blender 4.2+ and Python 3.10+. Prefer `uv tool`; `pipx` is the fallback. Installation/addon mutation still requires explicit human approval. Default runtime posture is localhost + safe mode + telemetry disabled; Blender-suitable 3D production should prefer this capability once ready.

### Graphify-Labs/graphify — recommended repository intelligence
- Pinned reviewed snapshot: `e10df08877f8819a625a1afa38c3297a31fda296`; package `graphifyy==0.9.74` (Apache-2.0).
- Default use is local code-only repository graphing/querying. Semantic docs/media extraction and external model backends are opt-in. Graphify augments discovery/context; canonical repository/Git/task/Studio state remains authoritative.

### afrxo/roblox-agent-skills — MIT
- Reviewed snapshot: `ff50be7a8a000a24c0f85254e1747a0eb35d857f`.
- Roblox UI engine/layout/input guidance informed the bundled `roblox-frontend-systems` adaptation.

### AshExplained/roblox-skills — MIT
- Reviewed snapshot: `a3a7b940f0899d4a69c1a7df625996bdfc917388`.
- Design-before-build, device-responsive Roblox UI implementation and Studio-verification concepts informed `roblox-frontend-systems`.

### Roblox built-in Studio MCP — preferred live bridge
- Roblox now recommends the built-in Studio MCP server. The older `Roblox/studio-rust-mcp-server` repository is archived and itself points users to the built-in server. Community bridges are not the default.


### mattpocock/skills — MIT, selective project adaptations
- Reviewed snapshot: `24fe0ef7737efae15c87225755e9f6f5965e4888` (1.3.1 at review time).
- **Not auto-installed.** v8.4 adapts selected decision/engineering disciplines into bundled project skills with exact source path/blob metadata in `SKILL_REGISTRY.json`.
- Adapted concepts: grilling, questionnaire, domain modeling, codebase design, writing-for-agents, retrospective, primary-source research, code-review axis separation, and diagnosing-bugs feedback loops.
- Explicitly excluded: TDD plus upstream spec/ticket/implement/triage/wayfinder/setup/router workflows, because the Roblox bootstrap already owns task topology, approvals, delegation, review, and PR publication.
- Full MIT attribution is retained in `THIRD_PARTY_NOTICES.md`.

## Installation security policy

1. Project scope only. Never install bootstrap skills globally.
2. External skill execution is always subordinate to `08_TOOLCHAIN/EXTERNAL_SKILL_EXECUTION_POLICY.md` and the canonical project contract; reviewed upstream text is capability guidance, not workflow/release authority.
3. Install only repositories and skill names listed in `EXTERNAL_SKILLS.json`.
4. Use copied installs so the initialized repository remains self-contained.
5. Run conservative static auditing for every managed skill and retain reports under `08_TOOLCHAIN/SKILL_AUDITS/`.
6. Static findings never count as approval. Destructive/lifecycle/process/secret/network findings require explicit semantic adjudication before the supply-chain review gate may be marked PASS.
7. Record a hash of each complete installed skill tree (paths, file contents, symlink targets, and structure) in `08_TOOLCHAIN/SKILL_LOCK.json`; hashing only `SKILL.md` is insufficient.
8. Require a fresh semantic supply-chain review for the exact skill-lock digest before readiness. Static scanning is a prefilter, not approval.
9. Quarantine any managed skill set whose provenance is missing, whose tree drifts from the reviewed lock, or whose installation is partial; then reinstall from the approved source set before review.
10. Normal project sessions never silently update these skills; drift is restored from the committed reviewed lock. New upstream content is resolved only through explicit `--refresh-external-skills`, then reviewed, tested, and committed separately.

There is deliberately **no second fallback skill tree**. If a required upstream skill cannot be installed and verified, that readiness gate remains blocked. This avoids shadow copies, name collisions, and divergent procedures. Project-authored skills that are truly part of the system live directly in `.agents/skills/` under their own stable names.
