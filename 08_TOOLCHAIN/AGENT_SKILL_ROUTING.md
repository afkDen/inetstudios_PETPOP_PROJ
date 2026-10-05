# ROLE ↔ SKILL ROUTING

> **GENERATED VIEW.** Canonical role definitions live in `08_TOOLCHAIN/ROLE_CONTRACTS/roles.json`. Regenerate with `python scripts/sync_derived_docs.py`; do not hand-edit this table.

All active skills live in `.agents/skills/`. This file is human-readable only and never overrides the role contracts.

| Role | Model class | Required skills | Write policy |
|---|---|---|---|
| `assurance-reviewer` | `REVIEW_DEEP` | `qa-methodology`, `roblox-testing`, `systematic-debugging`, `playable-vertical-slice`, `game-feel`, `accessibility-game`, `visual-production`, `game-ui-ux`, `roblox-ui-polish`, `roblox-frontend-systems`, `impeccable-ui`, `design-taste`, `interaction-motion`, `secure-software-engineering`, `roblox-networking`, `roblox-datastores`, `performance-optimization`, `economy-progression`, `save-systems`, `release-readiness-review`, `quality-gate`, `skill-use-audit`, `bloxmaps-world-production`, `bloxmaps-ui-accelerator`, `visual-design-orchestration`, `assurance-two-axis` | `read-only` |
| `content-production-worker` | `BALANCED` | `asset-production`, `visual-production`, `building-maps`, `building-3d-objects`, `blender-technical-art`, `blender-game-asset`, `vfx-production`, `audio-production`, `roblox-vfx`, `roblox-audio`, `polyhaven`, `skill-use-audit`, `blender-mcp-production`, `bloxmaps-world-production` | `scoped` |
| `creative-director` | `DEEP` | `visual-production`, `asset-production`, `stylized-asset-families`, `impeccable-ui`, `design-taste`, `game-design-fundamentals`, `accessibility-game`, `roblox-frontend-systems`, `visual-design-orchestration` | `scoped` |
| `design-strategist` | `BALANCED` | `game-design-fundamentals`, `game-feel`, `level-design`, `game-ui-ux`, `accessibility-game`, `economy-progression`, `audio-design`, `domain-modeling` | `scoped` |
| `frontend-worker` | `BALANCED` | `ui-production`, `roblox-ui-polish`, `roblox-user-interfaces`, `game-ui-ux`, `input-systems`, `accessibility-game`, `impeccable-ui`, `interaction-motion`, `design-taste`, `skill-use-audit`, `roblox-frontend-systems`, `visual-design-orchestration`, `bloxmaps-ui-accelerator` | `scoped` |
| `implementation-worker` | `BALANCED` | `roblox`, `roblox-core`, `systematic-debugging`, `playable-vertical-slice`, `skill-use-audit`, `codebase-design` | `scoped` |
| `lead-orchestrator` | `DEEP` | `process-inbox`, `complexity-risk-router`, `context-checkpoint-manager`, `context-memory-curator`, `human-decision-gates`, `mcp-tool-orchestration`, `implementation-package-builder`, `quality-gate`, `team-workflow-orchestrator`, `model-policy-governor`, `skill-use-audit`, `graphify-repo-intelligence`, `decision-grilling`, `external-questionnaire`, `domain-modeling`, `primary-source-research`, `workflow-retrospective` | `scoped` |
| `project-initializer` | `TOOL_RELIABLE` | `project-initializer`, `skill-supply-chain-review`, `model-policy-governor`, `mcp-tool-orchestration`, `agent-instruction-design`, `workflow-retrospective` | `scoped` |
| `studio-operator` | `TOOL_RELIABLE` | `roblox`, `roblox-mcp`, `roblox-testing`, `roblox-studio-workflow`, `studio-place-integration`, `mcp-tool-orchestration` | `studio-only` |
| `technical-architect` | `DEEP` | `roblox`, `roblox-core`, `roblox-networking`, `roblox-datastores`, `secure-software-engineering`, `performance-optimization`, `adr-authoring`, `domain-modeling`, `codebase-design`, `primary-source-research` | `scoped` |

## Policy

- Root `AGENTS.md` owns project-wide rules.
- Skills provide on-demand procedures and domain expertise.
- Role contracts define responsibility/isolation; runtime adapters only translate them.
- Load the minimum relevant skill set. Do not inject every installed skill body into every context.
- Query Graphify before broad repository scans or discovery-only delegation when the local graph is ready.
- Never exceed three active subagents; use sequential waves for additional specialist passes.
- `assurance-reviewer` is the fresh multi-mode independent review boundary.
- `studio-operator` is the semantic live-Studio boundary; the runtime adapter determines how that bridge is granted.
