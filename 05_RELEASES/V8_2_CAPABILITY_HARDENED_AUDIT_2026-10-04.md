# v8.2 Capability Hardened — Final Audit

**Date:** 2026-10-04  
**Version:** `v8.2-capability-hardened`  
**Baseline:** finalized v8.1 Capability Streamlined bootstrap  
**Disposition:** **APPROVED AS THE CURRENT REUSABLE BOOTSTRAP**, subject to real-workstation live gates described below.

## Executive result

v8.2 keeps the simple v8 human workflow while tightening the agent, memory, creative-tool and workstation layers. The audit focused on four concrete goals: fewer and stronger subagents; Blender MCP as priority 3D authoring infrastructure; Graphify-based repository intelligence without making inferred graph state authoritative; and a setup path that diagnoses dependencies before expensive agent work is spent troubleshooting them.

Final reusable-template inventory:

- **10 canonical capability roles**;
- **hard maximum 3 active subagents**; the Lead does not count as a subagent;
- **37 bundled project-authored/adapted skills**;
- **38 reviewed external skills** resolved from immutable Git refs during maintainer initialization;
- **75 registered skills total** after shared skill resolution;
- **174/174 source unit tests PASS**;
- **174/174 freshly prepared future-game unit tests PASS**;
- fresh prepared `validate_team.py`: **PASS**;
- fresh prepared `validate_repo.py`: **PASS**;
- fresh disposable end-to-end pipeline simulation: **PASS**;
- Python compile, derived-doc check, model-policy structure and static Rojo-layout guard: **PASS**.

No live Blender, Blender MCP, Roblox Studio MCP, native Rojo/StyLua/Selene or real GitHub remote operation was available in this audit container. Those are deliberately reported as **NOT RUN / task-time workstation gates**, not fabricated successes.

## 1. Agent architecture audit

### Finding

The earlier system accumulated too many narrow roles. Adjacent specialties increased delegation overhead, repeated context, tool schema exposure and the chance that several agents would independently reason about the same surface.

### Final architecture

v8.2 consolidates the normal team to:

1. `lead-orchestrator`
2. `design-strategist`
3. `technical-architect`
4. `implementation-worker`
5. `creative-director`
6. `frontend-worker`
7. `content-production-worker`
8. `studio-operator`
9. `assurance-reviewer`
10. `project-initializer`

A dedicated repository-scout is no longer normal. The Lead queries Graphify first, then reads the authoritative files it actually needs. Four narrow review roles are replaced by one **fresh read-only multi-mode** `assurance-reviewer` with `FUNCTIONAL`, `EXPERIENCE`, `RISK` and `RELEASE` modes.

### Three-subagent ceiling

A global ceiling of **3 active delegated contexts** is a deliberate recommendation, not a target to fill:

- LIGHT: normally **0–1**;
- STANDARD: normally **1–2**;
- CRITICAL: up to **3**, with additional specialist/review work in sequential waves.

This provides useful parallelism without turning every feature into an agent swarm. Parallel work is limited to genuinely disjoint/read-only scopes. One writer owns each file/system, Roblox Studio root and Blender scene/collection area at a time.

The Lead must ask whether Graphify + direct reasoning is enough before spawning another agent. Subagents receive compact dispatch packets rather than the full parent chat/tool log.

## 2. Graphify audit

The requested memory/repository tool is **Graphify**, not Graphiti.

Reviewed/pinned default:

- repository: `Graphify-Labs/graphify`;
- reviewed source ref: `e10df08877f8819a625a1afa38c3297a31fda296`;
- published package: `graphifyy==0.9.74`;
- Python: `>=3.10`;
- license: Apache-2.0.

### Final integration decision

Graphify is the preferred **repository-intelligence layer** for topology, dependency, impact and resume questions. Code mapping is local/tree-sitter based and the bootstrap defaults to code-only use.

The default package intentionally omits Graphify's `[mcp]` extra. The reusable bootstrap already calls the Graphify CLI directly, so installing the MCP transport by default would add dependencies and tool-context surface without improving the normal path. `graphifyy[mcp]==0.9.74` remains an opt-in extension when a reviewed runtime specifically needs Graphify as an MCP server.

Graphify remains an index/inference layer. It cannot override Git, repository files, accepted task/design artifacts, GitHub state or live Studio evidence.

## 3. Blender MCP / asset-production audit

3D authoring is no longer treated as an optional afterthought. For Blender-suitable assets, **MCP for Blender is the priority authoring bridge**.

Reviewed/pinned stack:

- repository: `ahujasid/mcp-for-blender`;
- reviewed source ref: `60d2a31b4632a7bc178f3dd636f7e68dfb5c8ae4`;
- package: `mcp-for-blender==2.1.3`;
- Python: `>=3.10`;
- bootstrap Blender floor: **4.2+** because the bundled game-asset workflow targets Blender 4.2+;
- license: MIT.

Default runtime posture:

```text
BLENDER_HOST=localhost
BLENDER_MCP_SAFE_MODE=1
DISABLE_TELEMETRY=true
```

The bridge is high privilege because it can execute Python inside Blender. The pinned release's safe-mode implementation was inspected and includes restrictions around filesystem/process/network primitives and Blender persistence/script-path mechanisms. Safe mode is still treated as defense-in-depth, not as a reason to skip backups, target verification or one-writer ownership.

Installation, runtime registration and live target verification are separate gates. The bootstrap provides reviewed runtime-registration examples but does **not** silently edit a developer's global Claude/Codex/IDE MCP configuration.

`content-production-worker` now handles explicit WORLD / PROP / BLENDER_MODEL / VFX / SFX-AUDIO / ASSET_IMPORT modes, using `blender-mcp-production` plus `blender-game-asset` for measured modeling gates and export/round-trip validation. Disabling safe mode, exposing the Blender socket beyond localhost, enabling paid/network generation providers, or making material dependency changes requires a human decision.

## 4. Frontend / UI capability audit

The reusable bootstrap carries the useful lessons from prior unrelated project experiments **without embedding that project's issue/PR numbers or history**.

Frontend capability combines Roblox-native GUI/HUD guidance with reviewed/adapted hierarchy, taste and motion guidance. Primary skills include:

- `roblox-frontend-systems`
- `ui-production`
- `roblox-ui-polish`
- `roblox-user-interfaces`
- `game-ui-ux`
- `input-systems`
- `accessibility-game`
- `impeccable-ui`
- `interaction-motion`
- `design-taste`

The design guidance explicitly does not force flat/minimal web UI. Dimensional frames, illustrated panels, custom silhouettes, textures, shadows, glow and game-appropriate motion remain valid when supported by the art direction.

The `creative-director` owns cross-surface visual direction; `frontend-worker` owns Roblox GUI/HUD design-to-implementation; `assurance-reviewer` EXPERIENCE mode provides a fresh visual/UX pass without adding another permanent reviewer role.

## 5. Modeling / VFX / SFX capability audit

The creative worker is capability-oriented rather than split into many tiny agents. Bundled production guidance covers:

- reference-driven Blender modeling with measured blockout/forms/topology/UV/export/round-trip gates;
- Roblox VFX readability, layering, performance and gameplay signaling;
- Roblox audio/SFX event design, spatial behavior, mix/readability, provenance and performance;
- asset provenance/licensing and import acceptance;
- world/map and stylized asset-family consistency.

Additional reviewed public Roblox and game-development skill sources were evaluated. The audit intentionally did **not** auto-vendor every overlapping skill found on the web. Capability gaps were adapted into the canonical project skills where useful; external skill count remains bounded and supply-chain reviewed.

## 6. Human-decision behavior

The Lead is expected to proceed autonomously on ordinary reversible implementation decisions inside approved scope, but stop the affected work and ask the human for consequential decisions.

Human gates include:

- material product/design/art direction forks with no canonical answer;
- scope expansion;
- new dependencies, MCPs, addons or permission expansion;
- paid services, APIs or asset purchases;
- licensing/provenance uncertainty;
- destructive operations and migrations;
- Production/shared-place mutation;
- persistence/security/monetization/RNG/trading/compliance changes;
- model/runtime/policy exceptions.

The request format is compact: **Decision needed / Why now / Recommendation / Options / If deferred**. The human answer is recorded in durable task state.

## 7. Dependency and initialization hardening

A major audit goal was avoiding token/agent spend on preventable workstation setup failures.

`scripts/workstation_doctor.py` is now the first dependency diagnostic and is **read-only by default**. It checks:

- usable Python >=3.10 and chooses a compatible interpreter;
- Git;
- Node/npx only when first shared external-skill resolution needs them;
- Rokit and exact Rojo/StyLua/Selene pins;
- GitHub CLI availability with manual fallback;
- Graphify exact pin;
- Blender >=4.2;
- MCP for Blender exact pin;
- isolated installer availability (`uv` preferred, `pipx` fallback);
- separate Blender CLI, runtime-registration and live-addon readiness.

The doctor writes `.local/WORKSTATION_DOCTOR.json` and `.local/WORKSTATION_FIX_PLAN.txt` with concrete remediation commands. It never silently installs Python, Blender, Node, Rokit, uv, pipx, system packages or GUI applications.

Explicit `--install-recommended` uses an already-installed `uv`/`pipx` to provision exact isolated Graphify/MCP-for-Blender CLI pins and uses already-installed Rokit for project Roblox tools. `--install-blender-addon` is a separate explicit mutation flag. Runtime MCP registration remains personal machine state and is documented rather than silently rewritten.

`team.py setup` now runs this preflight **before** expensive first-time shared skill resolution and blocks early when required prerequisites are missing.

## 8. Skill supply chain

External required skills remain sourced from immutable 40-character Git refs. First-time shared resolution is maintainer-only, audited and lock-generating. Normal feature work does not silently refresh third-party skills.

The final registered inventory is:

- 37 bundled project-authored/adapted skills;
- 38 reviewed external skills;
- 75 total registered skills after shared resolution.

The large skill inventory does not mean every task loads 75 skills. Runtime adapters eagerly surface only a very small subset and roles load the relevant skills just in time.

## 9. Model / runtime policy

Runtime adapters remain derived conveniences. They cannot prove the live runtime actually selected the configured model/effort.

Tracked policy keeps normal work on the configured workhorse effort, with deeper reasoning only for eligible/justified classes. Model receipts remain local evidence. A missing receipt does not block writing an idea/design draft, but it blocks claiming a fully validated delegated production/review run.

## 10. Collaboration and task workflow

The human-facing workflow remains:

```text
setup
→ idea/update
→ one GitHub Issue
→ one task branch
→ design checkpoint
→ human scope approval
→ implementation
→ risk-appropriate tests/Studio/Blender/review
→ one draft PR
→ second-human review for substantial work
→ human merge
```

No proposal/promotion PR ceremony was reintroduced. Legacy v7 scripts remain only for migration/backward compatibility.

The system still forbids silent stash/reset/rebase/force-push/push/merge/Production publish. Raw `USER_REQUEST.txt` remains byte-preserved and Git attributes protect it from line-ending rewriting.

## 11. Final validation performed

### Final source tree

- `python -m compileall -q scripts tests` → **PASS**
- `python scripts/sync_derived_docs.py --check` → **PASS**
- `python scripts/validate_model_policy.py --check-config` → **PASS**
- `python scripts/validate_rojo_layout.py` → **PASS**
- `python -m unittest discover -s tests -v` → **174/174 PASS**

The source template is intentionally not bound to a real game repo, so real game initialization/live checks are evaluated on a prepared copy instead of pretending the template itself is initialized.

### Fresh prepared future-game scaffold

A new scaffold was generated with `prepare_new_game.py` using a disposable example repository identity. After local Git initialization with the expected example origin:

- VERSION → `v8.2-capability-hardened`
- roles → **10**
- bundled skills → **37**
- compile → **PASS**
- derived docs → **PASS**
- model-policy structure → **PASS**
- static Rojo layout → **PASS**
- unit suite → **174/174 PASS**
- `validate_team.py` → **PASS**
- `validate_repo.py` → **PASS** and reports **75 registered skills / 10 roles**
- `disposable_pipeline_test.py` → **PASS**
- read-only `team.py setup --developer example-owner --runtime generic` → completed and correctly reported unavailable native/creative/live capabilities as **PENDING/BLOCKED**, not PASS.

### Deliberately not claimed

This audit environment did not provide a real workstation with all target applications/connections, so the following are not reported as passed:

- native pinned Rojo/StyLua/Selene install/build on a developer workstation;
- real GitHub Issue/PR publication against a user repository;
- live Roblox Studio built-in MCP connection/playtest/screenshots/console evidence;
- live Blender 4.2+ plus MCP-for-Blender addon/server connection;
- real Blender asset generation/export/reimport;
- Graphify installed/run as the pinned external CLI in this container.

The bootstrap contains explicit task-time gates for those operations.

## 12. Residual risk and operating recommendations

1. **Three concurrent subagents is a ceiling, not a quota.** Prefer 0–2 on most work and use sequential review waves for critical tasks.
2. **Blender MCP is privileged.** Keep localhost, safe mode and one-writer ownership; checkpoint `.blend` state before mutation.
3. **Graphify is assistive.** Query it first for broad topology, then verify repository files. Do not turn inferred edges into accepted facts without source confirmation.
4. **Do not auto-follow upstream skill HEADs.** Refresh only through explicit supply-chain review and lock update.
5. **Do not enable Graphify MCP/semantic extraction by default.** The lean CLI/code-only path gives most repo-intelligence value with fewer dependencies and less tool context.
6. **Do not install every newly discovered skill.** Add capability only when it closes a measured gap and does not duplicate a stronger existing skill/role.
7. **Keep live tools just-in-time.** Studio and Blender connections should be loaded for tasks that need them, not injected into every subagent context.

## Final decision

`v8.2-capability-hardened` is the recommended finalized reusable bootstrap for the next project iteration. It preserves the v8 simplified human workflow while making the agent team smaller, the creative pipeline materially stronger, memory/repository lookup more efficient, and workstation initialization more deterministic.

## 13. Final reconciliation pass

A final reconciliation pass was run after the capability work was complete.

- Confirmed that prior unrelated game-project Issue/PR identifiers are not encoded as bootstrap history or operating assumptions.
- Re-ran the full source suite: **174/174 PASS**.
- Rechecked the 10-role / 3-concurrent-subagent contract and 75-skill registry (37 bundled + 38 reviewed external).
- Revalidated the Graphify wrapper against the pinned `0.9.74` CLI contract: first build is code-only/local, incremental `update` remains code-only, and query/path/explain are retrieval helpers rather than authority.
- Revalidated the current MCP-for-Blender source/package contract at `2.1.3`, including localhost/safe-mode/telemetry-off defaults and the explicit install/addon/runtime/live-target separation.
- Hardened workstation onboarding further: when the pinned Blender MCP CLI is present, the read-only doctor now emits `.local/BLENDER_MCP_RUNTIME_REGISTRATION.md` with the resolved absolute executable path. This specifically avoids wasting agent turns on GUI-client PATH/`ENOENT` mismatches while still leaving global MCP registration to the human.
- Corrected the release package manifest so it now reflects v8.2 rather than stale v8.1 role/skill/test counts.
- Packaging excludes `.local/`, generated runtime adapters, caches, Python bytecode, worktrees, secrets and native build outputs.

The release remains intentionally pinned to the reviewed Graphify `0.9.74` snapshot rather than automatically following a newer upstream release published during finalization. Upstream refreshes belong in an explicit supply-chain update, not a last-minute release mutation.
