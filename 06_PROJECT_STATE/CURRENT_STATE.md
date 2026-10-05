# CURRENT STATE

- Project Status: **REUSABLE SCAFFOLD v8.5 SCOPE EVOLUTION — NEW GAME PREPARATION REQUIRED**
- Current Version: `v8.5-scope-evolution`
- Current Release: none
- Active Changeset: none
- Current Pipeline Stage: reusable template
- Human-facing workflow: `scripts/team.py` (`setup`, `doctor`, `idea`, `update`, `resume`, `status`, `approve`, `amend`, `withdraw-amendment`, `evidence-scope`, `gates`, `checkpoint`, `check`, `pr`)
- Agent architecture: 10 capability roles; hard maximum 3 active subagents; sequential waves for additional specialist/review passes
- Repository intelligence: Graphify recommended, code-only/local by default, never authoritative
- Creative tooling: MCP for Blender is priority for Blender-suitable 3D assets; localhost + safe mode + telemetry-disabled defaults
- Skills: 49 bundled + 37 reviewed external = 86 registered after maintainer resolution
- Normal collaboration shape: one GitHub Issue + one task branch + one implementation PR
- Preserved deep systems: canonical skills, provider-neutral roles, model policy, risk routing, Studio/Blender safety, independent review, quality gates and release controls
- Legacy compatibility: v7 proposal/promotion scripts remain available but are not the default workflow
- Live Studio/Blender readiness: task-time only; not required merely to capture an idea
- Next Action: prepare a separate game repository with `NEW_GAME_SETUP.md`, then run `python scripts/team.py setup ...`
