# Migration: v8.0 Streamlined → v8.1 Capability Streamlined

v8.1 keeps the **same simple human workflow** (`setup → idea/update → approve → implement → check → one PR`) while replacing the overly granular agent layer with a smaller capability-oriented system.

## What changes

- Canonical roles: **21 → 14**.
- Bundled project skills: **25 → 34**.
- Registered skills: **63 → 72**.
- Codex team policy: GPT-6.1 Sol, Medium workhorse; High remains a narrow justified exception for eligible deep/review roles.
- Frontend design: Roblox-adapted Impeccable + Emil motion + Taste guidance, routed to the creative/frontend/review roles.
- Content production: one capability worker handles world/level, 3D/Blender, VFX, SFX/audio and approved asset-source/import modes.
- Human decisions: consequential scope, creative forks, installs/MCPs, costs, licenses, migrations, Production/shared-place mutation and policy/security exceptions explicitly stop for human approval.
- Context/memory: repository/task artifacts remain the source of truth; compact checkpoint capsules and subagent dispatch packets reduce stale-context/token waste. Graph memory is optional only.
- MCPs: discover just-in-time, official-first, least-privilege. Roblox Studio's built-in MCP is the default Studio bridge. Blender MCP is optional and requires approval/review.

## Role mapping

| v8.0 roles | v8.1 role |
| --- | --- |
| `game-design-analyst`, `economy-progression-analyst` | `design-strategist` |
| `art-director` | `creative-director` |
| `ui-implementation-worker` | `frontend-worker` |
| `world-builder`, `asset-worker` | `content-production-worker` |
| `qa-reviewer`, `gameplay-reviewer`, `playtest-reviewer` | `quality-reviewer` |
| `ui-ux-reviewer`, `visual-reviewer` | `experience-reviewer` |
| `security-reviewer`, `persistence-reviewer`, `performance-reviewer` | `risk-reviewer` with explicit review mode |
| `lead-orchestrator`, `repository-scout`, `technical-architect`, `implementation-worker`, `studio-operator`, `release-reviewer`, `project-initializer` | retained |

The consolidation is deliberate: **mode/skill selection replaces role proliferation**. Do not recreate a narrow role merely because one task needs a specialist lens.

## Upgrade an existing v8 project

Do this on an integration-owned branch, not in the middle of another developer's feature branch.

1. **Checkpoint active feature work.** Keep local/uncommitted work isolated.
2. Bring the reviewed v8.1 toolchain files into the integration branch.
3. Regenerate runtime adapters for each runtime actually used by the team:

```powershell
python scripts/sync_runtime_adapters.py --runtime claude-code
python scripts/sync_runtime_adapters.py --runtime codex
# only when used:
python scripts/sync_runtime_adapters.py --runtime antigravity
```

4. Because `TEAM_MODEL_POLICY.json` changes, refresh each developer/runtime's ignored local model receipt through the normal setup/preflight path. Do **not** fake or copy another person's receipt.
5. Run:

```powershell
python -m unittest discover -s tests
python scripts/sync_derived_docs.py --check
python scripts/validate_model_policy.py --check-config
python scripts/validate_team.py
python scripts/validate_repo.py
```

6. Review and merge the toolchain PR with a different human reviewer.
7. Existing v8 task metadata remains readable: v8.1 validators accept both `streamlined-v8` and `streamlined-v8.1`, while new tasks are written as `streamlined-v8.1`.

## Projects that already adopted earlier frontend capability adaptations

Do not duplicate the same skill source under a second name. Reconcile by behavior:

- map Impeccable-derived guidance to `impeccable-ui`;
- map Emil motion guidance to `interaction-motion`;
- map Taste-derived critique to `design-taste`;
- route them through `creative-director`, `frontend-worker`, and fresh `experience-reviewer`;
- keep real Studio screenshot/state evidence for acceptance;
- preserve dimensional, illustrated, textured Roblox UI instead of interpreting web guidance as a mandate for flat minimalism.

## MCP / optional capability migration

No new MCP server is silently installed by this upgrade.

- Roblox Studio: prefer the **built-in Studio MCP** and verify the exact Studio target before mutation.
- Blender: optional; installation/addon/server connection needs human approval and a pinned/reviewed version.
- Basic/graph memory: optional augmentation only. Never let an external graph override repository/GitHub/Studio truth.

## Removed assumptions

v8.1 does **not** assume:

- more subagents means better output;
- every task needs a reviewer swarm;
- the Lead should eagerly load every skill/tool;
- chat history is reliable long-term memory;
- an MCP configured on disk was actually connected or used;
- an external design skill should be copied wholesale into Roblox workflows.

## Rollback

If a v8.1 integration has not been merged, abandon the integration branch normally. Do not rewrite another developer's feature branch. If already merged, use a reviewed revert PR for the specific integration commits rather than `reset --hard` or force-pushing shared history.
