# v8.1 Capability Streamlined — Final Audit

**Date:** 2026-10-04  
**Version:** `v8.1-capability-streamlined`  
**Baseline:** finalized v8.0 Streamlined bootstrap

## Executive result

v8.1 preserves v8.0's simplified human workflow while substantially upgrading the agent/tool layer. The central change is a shift from **many narrow subagents** to **fewer capability-oriented roles with just-in-time skills/tools and explicit modes**.

Measured bootstrap changes:

- roles: **21 → 14** (33% fewer canonical roles);
- bundled project skills: **25 → 34**;
- registered skills: **63 → 72**;
- source unit tests: **173/173 PASS**;
- freshly prepared future-game scaffold: **173/173 PASS**;
- prepared `validate_team.py`: **PASS**;
- prepared `validate_repo.py`: **PASS**;
- derived docs: **PASS**;
- static model-policy structure: **PASS**;
- disposable workflow simulation: **PASS**.

Live Roblox Studio/MCP and native workstation tools were not available in this audit container and are intentionally **not** reported as passed.

## Research incorporated

The redesign reviewed public primary/near-primary sources for:

- Impeccable UI/design guidance;
- Emil Kowalski interaction/motion skills;
- Taste visual-direction guidance;
- Anthropic frontend-design;
- game-development skill catalogs and Roblox-specific skill suites;
- reference-driven Blender game-asset skills;
- Blender MCP implementations;
- Roblox Studio's built-in MCP direction;
- repository-intelligence and graph-memory candidates;
- agent architecture guidance emphasizing simple composable workflows, context curation, fresh-context evaluation, on-demand tool discovery and long-running checkpoints.

The v8.1 review incorporated reusable lessons from earlier project experiments without importing unrelated project issue/PR history into the scaffold.

## Agent architecture

### Before: 21 roles

The prior role set separated many adjacent concerns: art/asset/world; UI implementation/UI review/visual review; QA/gameplay/playtest; security/persistence/performance; game design/economy.

### After: 14 roles

- `lead-orchestrator`
- `repository-scout`
- `design-strategist`
- `technical-architect`
- `implementation-worker`
- `creative-director`
- `frontend-worker`
- `content-production-worker`
- `studio-operator`
- `quality-reviewer`
- `experience-reviewer`
- `risk-reviewer`
- `release-reviewer`
- `project-initializer`

Specialization now comes from **skills + modes + evidence requirements**, not a new role for every concern.

### Delegation budget

- LIGHT: 0–1 production/analysis specialist; reviewer optional.
- STANDARD: normally max 2 production/analysis specialists + 1 fresh reviewer.
- CRITICAL: normally max 4 production/analysis specialists + up to 2 fresh reviewers; exceeding the budget requires explicit human justification.

Read-only/disjoint scopes may run in parallel. A file/system/Studio root has one writer at a time.

## Frontend/UI capability upgrade

Added Roblox-adapted project skills:

- `impeccable-ui` — hierarchy, visual systems, anti-template critique and polish; explicitly preserves dimensional/illustrated/textured game interfaces;
- `interaction-motion` — interaction timing, easing/spring intent, interruptibility, tactile feedback and reduced-motion alternatives;
- `design-taste` — controlled visual alternatives, anti-generic critique, reference transformation; fabricated/mock execution evidence is explicitly forbidden.

These are mapped primarily to `creative-director`, `frontend-worker`, and fresh `experience-reviewer`, alongside existing native Roblox UI/input/accessibility skills.

## Modeling / VFX / SFX / content capability

`content-production-worker` replaces separate world/asset workers and supports explicit capability modes:

- WORLD / LEVEL
- PROP / 3D
- BLENDER_MODEL
- VFX
- SFX / AUDIO
- ASSET_SOURCE / IMPORT

New supporting skills:

- `blender-game-asset`
- `vfx-production`
- `audio-production`

The worker may use approved MCP/tool capability when genuinely connected, but must produce a deterministic manual/operator packet instead of faking output when the tool is unavailable.

## Human decision gates

`human-decision-gates` is first-class and routed to the Lead. The agent continues routine reversible work but asks/stops the affected work for:

- material scope expansion;
- consequential creative/art/UX forks without a canonical answer;
- new packages/tools/system managers/MCP servers/addons or permission expansion;
- paid APIs/services/asset purchases/recurring costs;
- license/provenance uncertainty;
- destructive state operations/migrations;
- Production/shared-place mutation outside approved windows;
- persistence/security/monetization/RNG/trading/policy changes;
- model/runtime/policy exceptions;
- unresolved requirement conflicts.

Decision requests are intentionally compact: decision, why now, recommendation, options/tradeoffs, and safe work that can continue if deferred.

## Context and memory

`context-memory-curator` formalizes three tiers:

1. canonical repo/design state;
2. issue/task state and evidence;
3. temporary local/session traces.

Subagents receive compact dispatch packets rather than entire chat histories/tool logs. `WORK_STATE.md` is the long-running checkpoint capsule. Fresh sessions retrieve authoritative slices just in time.

Graph-memory experimentation was **not enabled by default** in v8.1. v8.2 later standardized repository intelligence on Graphify while keeping repository/Git/accepted task artifacts/GitHub/live Studio authoritative.

## MCP/tool strategy

Added `mcp-tool-orchestration` and `08_TOOLCHAIN/MCP_CAPABILITY_PROFILES.json`.

Policy:

- discover tools only when needed;
- official-first;
- no silent installation/connection;
- least privilege;
- separate inspection from mutation;
- prefer deferred/tool-search/programmatic orchestration where the active runtime supports it;
- record evidence for mutations;
- deterministic fallback if capability is unavailable.

Roblox Studio's built-in MCP is preferred. Blender MCP is optional and gated. Repository graph tooling is assistive, not canonical.

## Model policy

Codex profile is updated to **GPT-6.1 Sol** with Medium as the normal workhorse. High remains an explicit justified exception only for eligible deep/review classes. Claude remains Opus 5.5 Low/Medium only in the tracked team policy.

Static adapters never count as proof that the live runtime actually used a model/effort.

## Compatibility

- New task metadata writes `streamlined-v8.1`.
- Task validation accepts existing `streamlined-v8` metadata as well, avoiding unnecessary breakage in migrated projects.
- v7 proposal/promotion tools remain for migration/history; the normal v8/v8.1 path is still one Issue → one task branch → one PR.

## Validation performed

### Final source tree

- `python -m unittest discover -s tests` → **173 PASS**
- `python -m py_compile scripts/*.py tests/*.py` → **PASS**
- `python scripts/sync_derived_docs.py --check` → **PASS**
- `python scripts/validate_model_policy.py --check-config` → **PASS**

The reusable source intentionally remains unbound to a real game repository, so `validate_team.py` correctly refuses to claim an initialized project there.

### Fresh prepared future-game scaffold

Created through `prepare_new_game.py` using a disposable example repository identity, then ran:

- unit suite → **173 PASS**
- Python compile → **PASS**
- derived docs → **PASS**
- model-policy structure → **PASS**
- `validate_team.py` → **PASS**
- `validate_repo.py` → **PASS**
- disposable pipeline simulation → **PASS**

### Deliberately not claimed

- native Rojo/StyLua/Selene executable validation in this audit environment;
- real Roblox Studio MCP connection;
- live Studio playtest/viewport/console evidence;
- Blender MCP installation or authoring run;
- repository-graph experimentation beyond the scaffold defaults.

Those remain workstation/task-time gates.

## Residual risks / recommendations

1. Third-party/adapted skills should remain pinned and reviewed before refresh; do not auto-follow upstream HEAD.
2. MCP bridges/addons are code execution surfaces. Treat optional Blender/memory connections as explicit installation/security decisions.
3. More tool capability can increase context and attack surface; keep just-in-time discovery and least-privilege routing.
4. Graph memory should be adopted only after measuring a real retrieval problem that repo-native checkpoints do not solve.
5. Role consolidation should be evaluated by output quality/cost over several real tasks. Split a role again only if evidence shows a persistent quality boundary—not merely because a skill exists.
6. Earlier project-specific frontend experiments remain external provenance only; reusable bootstrap behavior is documented generically.
