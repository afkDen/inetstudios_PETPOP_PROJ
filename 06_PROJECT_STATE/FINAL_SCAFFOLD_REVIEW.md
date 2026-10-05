# Final Scaffold Review — v8.5 Scope Evolution

Status: **FINALIZED REUSABLE TEMPLATE — TARGET GAME CONFIGURATION STILL REQUIRED**

v8.5 builds on the v8.4 reasoning-capability release and introduces the `streamlined-v8.5` revisioned-scope task schema. Existing v8.3/v8.4 task packets remain readable; an already-approved legacy task is lazily upgraded when its first scope amendment is created.

## Architecture decisions

1. `AGENTS.md` remains the master runtime-neutral operating contract.
2. `.agents/skills/<name>/SKILL.md` remains the single canonical active skill root; external skills are pinned, reviewed, copied project-local, audited and whole-tree locked during first maintainer setup.
3. The role catalog is consolidated to **10 capability roles**. The Lead uses at most **3 active subagents**, with LIGHT normally 0–1, STANDARD 1–2 and CRITICAL up to 3; extra specialist/review work uses sequential waves.
4. Graphify is the preferred local repository-intelligence layer before broad scans or discovery-only delegation. Its graph is assistive, never authoritative.
5. MCP for Blender is the priority bridge for Blender-suitable 3D assets. Bootstrap defaults are localhost, safe mode enabled and telemetry disabled; unsafe/network/paid-provider changes require a human decision.
6. Roblox Studio's approved MCP/Rojo path remains the live Roblox execution boundary. One writer owns a Studio root or Blender scene area at a time.
7. `scripts/team.py` is the single normal human-facing workflow surface.
8. The normal task lifecycle is one Issue, one task branch and one implementation PR.
9. Raw human requests, copied task `REFERENCES/**`, and amendment-scoped `SCOPE_AMENDMENTS/**` reference material remain byte-preserved and are protected with `.gitattributes -text`, so CRLF/LF normalization cannot invalidate byte-level SHA-256 provenance.
10. Human scope approval happens on the task branch after AI design and creates revision 1. Later material changes use approved `SCOPE_AMENDMENTS/` revisions; a draft proposal leaves the current approval active and pauses only affected work. Additional human-decision gates cover material design forks, dependencies/MCPs, paid services/assets, licensing, migrations/destructive operations, Production/shared-place mutations and policy exceptions.
11. Quality/evidence requirements are risk-proportional: LIGHT, STANDARD, CRITICAL.
12. Live Studio/Blender verification is task-time, not required merely to capture an idea.
13. The workstation doctor is read-only by default and emits a concrete remediation plan. Explicit install flags use an already-installed `uv` (preferred) or `pipx`, plus Rokit; machine-level package managers/apps are never silently installed.
14. Legacy v7 proposal/promotion tooling remains for migration and regression compatibility, not ordinary new work.
15. No automatic push, merge or Roblox Production publish was introduced.

## Capability inventory

- 10 canonical capability roles.
- 49 bundled project-authored skills in the reusable template.
- 37 reviewed external skills expected after maintainer resolution.
- 86 registered skills total.
- Frontend/UI capability includes Roblox-native GUI implementation plus adapted hierarchy/taste/motion guidance.
- Content production covers world/props, Blender modeling, VFX, SFX/audio and asset import through explicit worker modes.
- One fresh `assurance-reviewer` covers FUNCTIONAL / EXPERIENCE / RISK / RELEASE modes without multiplying reviewer agents.

## Outcome

The system keeps the original agentic depth while reducing normal human ceremony and agent fan-out. The Lead should solve small work itself, query Graphify before broad repository exploration, delegate only the minimum capable specialists, use MCP for Blender as the normal Blender-suitable asset path, and ask the human only when a decision materially changes scope, direction, cost, safety or shared state.


## v8.3 integration note

The scaffold now carries a pinned external BloxMaps production adapter, provider-neutral visual-design routing and repeatable task references without vendoring BloxMaps FSL source into game repositories. The three-subagent hard ceiling remains unchanged.

## v8.3.1 hardening note

The BloxMaps adapter now refuses execution from a dirty checkout, generated-plan output is constrained to approved repository-local roots, asset-only PRs can no longer bypass managed-change delivery gates, v8.3 infrastructure paths are integration-owned, quality evidence follows the canonical branch/role contract, and derived skill inventory counts are checked automatically.

## v8.4 reasoning integration note

The bootstrap now includes project-adapted decision/research/debugging/architecture/agent-writing/review disciplines from the immutable reviewed `mattpocock/skills` snapshot without importing its process-owning ticket/spec/implementation flows. The normal Roblox workflow, approvals, 10 roles, three-subagent ceiling and evidence boundaries remain unchanged. TDD is explicitly not a global requirement.


## v8.5 scope evolution note

Post-approval scope is now intentionally movable without silently mutating the original approval or invalidating unrelated work. Amendment approval history is retained; approved/withdrawn amendment files and their supplemental references are integrity-bound; unresolved draft amendments block final delivery; and compact, Studio, and full-quality evidence are scope-revision aware. Risk/gate changes after approval are part of the same amendment approval rather than a hidden side channel, with stricter notes/substantive-change requirements for de-escalation.
