# v5 final audit — live Studio delivery, source discovery and art/UI quality

Date: 2026-09-23. Basis: prior v4 packaged repository, its local source/role/config/tests and publicly checked official Roblox/Rojo documentation and asset/license sources. This is a **scaffold** release audit, not a claim that a live Roblox place was playtested.

## Root causes and corrective decisions

1. **Repo-only output vs the user's already-open Baseplate.** The prior default Rojo mapping owns only `src/server`, `src/shared`, `src/client`. MCP quick connect does not automatically connect Rojo or transfer repo scripts to the user's current place. `rojo build` creates a place file; live updates to the open Baseplate require `rojo serve` and the separately installed Rojo Studio plugin, plus inspection of the exact live Studio target. Selecting Visual Studio Code in MCP quick connect is not proof that Antigravity is connected. **Action:** mandatory separate MCP+Rojo two-connection preflight, actual tool probes, human target lock, reversible sync marker and receipt.
2. **Studio verification at end only.** v4 requests console/screenshots for completion but doesn't operationalize the initial target/bridge handshake. An agent can write lots of source files without touching the user's open Studio window. **Action:** `studio-place-integration` skill and `LIVE_STUDIO_DELIVERY.md` before implementation; issue-local `STUDIO_DELIVERY.json` required for accepted managed game code, approved asset or Rojo-mapping changes.
3. **Visual reference and asset supply gaps.** Existing general game/Roblox skills guide engineering but are not bespoke high-quality 3D/UI engines. More agent roles don't automatically provide finished icons, textured meshes, reference mockups or compatible client/server UI. **Action:** targeted `roblox-ui-polish` and `stylized-asset-families` skills, stronger art/UI role contracts, human-approved reference comparison and real in-game iteration. Verified CC0 Kenney individual packs and Quaternius packs are explicit curated starting points. Commercial product galleries may guide acceptance quality but do not grant redistribution or product parity.
4. **Cross-team world source gap.** v4 uses filesystem-authoritative scripts but leaves hand-built Workspace worlds in Studio. The team's long-term desire for shareable source-controlled maps requires a safe opt-in migration rather than silently expanding Rojo's mapping over an existing world. **Action:** reviewed `templates/rojo-world-opt-in.project.json` only; source authority changes require backup, disposable test, visual diff and integration-owner approval.
5. **Quality gate coverage gap.** Earlier `--compare` checked only changed `src/`, so art-only changes could bypass accepted issue quality packets. **Action:** compare managed `src/`, `07_ASSETS/APPROVED/`, `default.project.json`, including uncommitted local changes and untracked files; require complete issue-local Studio delivery and independent quality packet on accepted work.
6. **External skill install assumptions.** The previous ZIP bundles project skills but declares 38 external skills to be installed/audited by project initialization. If that initial installation hasn't run on the team main branch, agents cannot truthfully claim those skills were available. **Action:** retain the reviewed 38-skill upstream policy and make targeted project-native additions. Do not blindly vendor web-only design skills as Roblox GUI frameworks, nor automatically enable paid/credit generation services.

## New/changed assets

- Three canonical project-authored skills: `.agents/skills/studio-place-integration`, `roblox-ui-polish`, `stylized-asset-families`.
- New target-specific SOP: `02_TECHNICAL/LIVE_STUDIO_DELIVERY.md`, with distinct official MCP quick-connect and Rojo Studio plugin checks.
- New candidate/license distinctions: `08_TOOLCHAIN/QUALITY_SOURCE_CANDIDATES.md`.
- New opt-in world migration illustration: `templates/rojo-world-opt-in.project.json` (not enabled by default).
- New receipt template and helpers: `templates/STUDIO_DELIVERY_TEMPLATE.json`, `scripts/prepare_studio_delivery.py`, `scripts/validate_studio_delivery.py`, with `QUALITY_EVIDENCE.json` integration.
- Updated root master contract, standard team prompt, quality contracts, role/skill registry and regenerated routing documentation.

## Real-world requirements and honest limitations

- No tool connection was made to the user's own Roblox Studio, Baseplate or GitHub remote in this release. Local fixture tests exercise the validation contract but cannot authenticate screenshots or prove Studio tool calls. Actual place targeting, MCP availability, Rojo plugin sync, viewport inspection, visual approval and playtesting **must be done on the teammates' workstations**.
- This execution environment lacks the pinned Rojo, StyLua and Selene binaries; a native build/real Studio playtest is PENDING, not PASS. The existing `python scripts/bootstrap_dev_tools.py --install --install-plugin` path remains explicitly consented after Rokit is installed.
- Neither the new skills nor existing free APIs promise proprietary all-in-one game-generation parity. No new paid/credit API dependency or unchecked external skill was installed.
- The base project's world/terrain remain Studio-owned until an authorized migration. For an unregistered Baseplate with no published place ID, verify open Studio instance name and instance ID with human confirmation rather than fabricating a place ID.
- Evidence validators confirm shape, paths and consistency; second-human reviewers must inspect original tool evidence, actual gameplay and actual screenshot quality. Never use generated images as fake Studio captures.

## Reviewed primary sources

- Official Roblox Studio MCP: https://create.roblox.com/docs/studio/mcp
- Rojo CLI + plugin setup: https://rojo.space/docs/v7/getting-started/installation/
- Rojo serve/live sync: https://rojo.space/docs/v7/getting-started/new-game/
- Rojo mapping limitations: https://rojo.space/docs/v7/sync-details/
- Individual Kenney UI Pack CC0: https://kenney.nl/assets/ui-pack
- Quaternius licensing FAQ: https://quaternius.com/faq.html
- Official Creator Store: https://create.roblox.com/docs/production/creator-store
- Existing skill families: https://github.com/nonlooped/roblox-suite and https://github.com/gamedev-skills/awesome-gamedev-agent-skills
- Conditional web-focused references, not enabled: https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design and https://github.com/google-labs-code/stitch-skills

## Release test classification

Portable static validation, Python tests, syntax compilation, derived docs, team policy and disposable pipeline: tested locally and must be rerun on the **packaged ZIP** before distribution. Studio real-world connections/native binaries: pending workstation verification. The released project stays INITIALIZATION_REQUIRED until those live gates are genuinely satisfied.
