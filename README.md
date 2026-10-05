# Portable Agentic Roblox Development System — v8.5 Scope Evolution

A Roblox team scaffold that keeps the deep agent workflow, skills, role isolation, Studio safety and review gates while making normal human use much simpler.

## What v8.5 changes

v8.5 keeps the v8.4 reasoning/capability layer and changes the approval model so approved work can evolve deliberately. Initial human approval creates **scope revision 1**. Material post-approval changes are drafted under `SCOPE_AMENDMENTS/`, then explicitly approved as later revisions. A draft amendment does not erase the current approval: unaffected work can continue, while affected work pauses until the proposal is approved or withdrawn. Final delivery requires evidence to be current for the active revision, including scope-aware Studio/full-quality receipts. Amendments can carry new byte-hashed files/URLs without mutating original intake provenance, and risk/gate de-escalation is explicitly guarded.

This fixes the overly rigid “reopen the whole task” behavior without allowing silent scope drift. See `08_TOOLCHAIN/SCOPE_EVOLUTION_V8_5.md` and `MIGRATION_V8_4_TO_V8_5.md`.

## What v8.4 adds

v8.4 keeps the hardened v8.3 task/provenance schema and the 10-role/three-subagent architecture, then adds a selective engineering-reasoning layer adapted from the reviewed `mattpocock/skills` repository. The bootstrap gains dependency-aware decision grilling, external stakeholder questionnaires, domain-language discipline, deep-module/seam design, agent-instruction design, explicit workflow retrospectives, primary-source research, two-axis assurance, and a bundled budget-aware debugging discipline.

It deliberately **does not import TDD or Matt's spec/ticket/implementation/triage orchestration**. Existing risk-proportional tests and Studio evidence remain authoritative, and new test authoring is used only when it is the cheapest durable guard or the task requires it. See `08_TOOLCHAIN/ENGINEERING_REASONING_V8_4.md` and `05_RELEASES/V8_4_ENGINEERING_REASONING_AUDIT_2026-10-05.md`.

## What v8.3.1 hardens

v8.3.1 is a backwards-compatible hardening release over the v8.3 workflow schema. It preserves `streamlined-v8.3` task compatibility while closing cross-platform and boundary gaps found in final review:

- task-local `REFERENCES/**` are now Git `-text` byte-preserved, preventing Windows CRLF/LF normalization from invalidating recorded SHA-256 provenance;
- BloxMaps MapGen execution now requires a **clean** isolated checkout as well as the exact reviewed origin/ref, and generated-plan writes are confined to `.local/bloxmaps/` or `04_CHANGESETS/`;
- approved assets under `07_ASSETS/APPROVED/` use the same managed-change detection in CI as source/Rojo mapping changes, closing the asset-only evidence bypass;
- v8.3 workflow/BloxMaps policy files are included in the integration-owner boundary;
- quality evidence uses the canonical `feat|fix|docs/<issue>-<slug>` branch contract and canonical consolidated roles;
- skill inventory numbers in project-state docs are derived from `SKILL_REGISTRY.json`, and the retained legacy master directive is explicitly marked historical/non-authoritative.

## What v8.3 adds

v8.3 keeps the v8 streamlined human workflow and v8.2 capability hardening, then adds a reviewed BloxMaps production adapter and provider-neutral visual design layer:

- **10 consolidated capability roles instead of 21 narrow roles** to reduce duplicate delegation and token/tool overhead.
- **Roblox-adapted frontend design stack** inspired by Impeccable, Emil Kowalski motion guidance, Taste, and Anthropic frontend-design, while preserving dimensional/illustrated game UI.
- A single **content-production worker** with explicit modes for Roblox world building, 3D/Blender modeling, VFX and SFX/audio production.
- **Human-decision gates** for consequential creative forks, scope expansion, installations/MCPs, costs, licensing, migrations, Production and other irreversible/high-impact choices.
- **Just-in-time MCP/tool orchestration**: official Roblox Studio MCP for live Roblox work; **MCP for Blender is the priority authoring path for Blender-suitable 3D assets**; **Graphify is the recommended local repository-intelligence layer**. Canonical repo/Git/task/Studio state remains source of truth.
- **Graphify-first repository intelligence + context-memory curation** and compact subagent dispatch packets so long-running work survives fresh sessions without forwarding entire chats/tool logs.
- **Hard three-subagent concurrency cap** with sequential waves and one multi-mode fresh assurance reviewer to prevent unnecessary fan-out while preserving independent review.
- **Pinned BloxMaps production adapter** using your `afkDen/bloxmaps` fork for deterministic map/world plans, Studio map building, asset manifests and multi-section worlds without vendoring FSL source into game repositories.
- **Provider-neutral visual design**: Claude Design is one optional runtime binding, not a canonical dependency. Claude, OpenAI/Codex, Gemini, Cursor, Copilot and other capable agents use the same semantic roles/skills/evidence gates.
- **Optional BloxUI acceleration** for declarative blueprints/prototypes; adopting Fusion/BloxUI as the actual frontend framework requires a human architecture decision.

See `08_TOOLCHAIN/AGENT_ORCHESTRATION_V8_3.md`, `08_TOOLCHAIN/BLOXMAPS_SETUP.md`, `08_TOOLCHAIN/FRONTEND_SKILLS.md`, `08_TOOLCHAIN/MCP_CAPABILITY_PROFILES.json`, and `08_TOOLCHAIN/CONTEXT_AND_MEMORY.md`.

## The normal workflow

```text
setup
  ↓
idea / update
  ↓
AI designs + selects relevant skills/subagents
  ↓
human approves scope revision 1
  ↓
implementation ↔ approved scope amendments as needed
  ↓
tests + Studio evidence as needed
  ↓
check
  ↓
one draft PR
  ↓
human review + merge
```

Normal work is **one GitHub Issue + one task branch + one implementation PR**. v7 proposal/promotion scripts remain only for migration/backward compatibility.

## New game

1. Create an empty private GitHub repository.
2. From this extracted reusable ZIP run:

```powershell
python scripts/prepare_new_game.py `
  --repo-url https://github.com/OWNER/MY-GAME.git `
  --destination C:\RobloxProjects\MY-GAME `
  --maintainer OWNER
```

3. Review/commit/push the scaffold manually.
4. In the prepared checkout:

```powershell
python scripts/team.py setup --developer OWNER --runtime claude-code
```

Run the read-only workstation doctor any time setup looks suspicious:

```powershell
python scripts/team.py doctor
```

It writes a concrete local fix plan for pinned Roblox tools, Graphify, Blender/MCP for Blender, and the isolated BloxMaps world-generation checkout. When the Blender MCP CLI is ready it also writes a local runtime-registration snippet with the resolved absolute executable path, avoiding a common GUI-client PATH/ENOENT failure. No system dependency is installed by default. After reviewing the plan, `team.py setup ... --install-recommended` can use an already-installed `uv` or `pipx`, plus Rokit for exact pinned CLI installs; `--install-blender-addon` is a separate explicit mutation.

The first maintainer may use `--initialize-shared-skills --confirm-shared-change` when the reviewed external skill set has not yet been resolved. Live Studio/MCP/Rojo validation is deliberately deferred until an approved task actually needs Studio.

## First game idea

Write the idea in a plain `.txt` (for example `.local/ideas/game.txt`) and run:

```powershell
python scripts/team.py idea `
  --file .local/ideas/game.txt `
  --reference .local/references/moodboard.png `
  --reference https://example.com/reference `
  --owner OWNER
```

If no `--issue` is supplied, the CLI asks before creating one through authenticated `gh`. It then creates the single task branch, byte-preserves the original request, creates the issue changeset and generates a ready-to-paste AI prompt under `.local/prompts/`.

The AI designs first. When you accept its proposed scope:

```powershell
python scripts/team.py approve --issue 6 --by OWNER --note "Approved first vertical slice"
```

If you later want to change that approved scope, do not silently rewrite `TASK.md` and do not throw away the valid approval. Draft and approve an amendment:

```powershell
python scripts/team.py amend --issue 6 --reason "Add another accepted behavior" --by OWNER
python scripts/team.py approve --issue 6 --amendment 1 --by OWNER --note "Approved scope revision 2"
```

## Future update

```powershell
python scripts/team.py update --file .local/ideas/fear-combos.txt --owner OWNER
```

Same flow. No proposal PR and no promotion PR.

## Checkpoint / resume tomorrow

```powershell
python scripts/team.py checkpoint --issue 6 --note "Core loop implemented; Studio playtest next"
python scripts/team.py resume
```

## Before a PR

```powershell
python scripts/team.py check --issue 6
python scripts/team.py pr --issue 6
```

The second command is preview-only. With explicit approval:

```powershell
python scripts/team.py pr --issue 6 --confirm-publish
```

Merge remains a human GitHub action. Roblox Production publish remains a separate release action.

## What was preserved from v7

- canonical `.agents/skills/` skill system and supply-chain controls
- provider-neutral role/subagent contracts
- runtime/model policy and fresh-context independent review
- Rojo/Studio separation and nonproduction live verification
- server-authoritative Roblox engineering rules
- pinned development tools and CI
- checkpoints and resumable issue-local state
- full quality evidence path for critical/high-risk work

Read `START_HERE.md`, `AGENTS.md`, and `TEAM_WORKFLOW.md` for the operating contract.

## Migration / audit

- `MIGRATION_V7_TO_V8.md` — safe cutover guidance for an existing v7 game.
- `MIGRATION_V8_TO_V8_1.md` — historical v8 → v8.1 guidance.
- `MIGRATION_V8_1_TO_V8_2.md` — historical capability-hardening migration guidance.
- `MIGRATION_V8_2_TO_V8_3.md` — historical BloxMaps/provider-neutral visual integration guidance.
- `MIGRATION_V8_3_1_TO_V8_4.md` — historical engineering-reasoning integration guidance.
- `MIGRATION_V8_4_TO_V8_5.md` — current revisioned-scope migration guidance.
- `05_RELEASES/V8_5_SCOPE_EVOLUTION_AUDIT_2026-10-05.md` — current scope-evolution audit and validation.
- `05_RELEASES/V8_4_ENGINEERING_REASONING_AUDIT_2026-10-05.md` — historical reasoning integration audit.
- `05_RELEASES/V8_3_1_BLOXMAPS_HARDENED_AUDIT_2026-10-05.md` — historical v8.3.1 hardening audit.
- `05_RELEASES/V8_3_BLOXMAPS_INTEGRATED_AUDIT_2026-10-04.md` — historical v8.3 integration audit.
- `05_RELEASES/V8_2_CAPABILITY_HARDENED_AUDIT_2026-10-04.md` — historical v8.2 audit.
- `05_RELEASES/V8_1_CAPABILITY_STREAMLINED_AUDIT_2026-10-04.md` — historical v8.1 audit.
- The v8.0 audit remains in release history as the baseline.
