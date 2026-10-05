# Agent Orchestration v8.4 — Three-Thread Capability Team + Reasoning Layer

v8.4 retains the normal role catalog to **10 roles** and imposes a **hard maximum of three active subagents**. The Lead is not counted as a subagent. More total specialist passes may occur in sequential waves, but never more than three delegated contexts run at once.

## Canonical roles

- `lead-orchestrator` — routing, Graphify-first discovery, synthesis, human gates and checkpoints.
- `design-strategist` — game/product/UX/economy design when relevant.
- `technical-architect` — architecture, networking, persistence and high-risk contracts.
- `implementation-worker` — scoped Luau/system implementation.
- `creative-director` — art/UI/world/VFX direction and visual-system approval package.
- `frontend-worker` — Roblox GUI/HUD design-to-implementation specialist.
- `content-production-worker` — world/assets/Blender/VFX/SFX; Blender MCP is priority for Blender-suitable 3D authoring.
- `studio-operator` — narrow live Roblox Studio execution bridge.
- `assurance-reviewer` — fresh read-only `FUNCTIONAL`, `EXPERIENCE`, `RISK`, and `RELEASE` review modes.
- `project-initializer` — setup/repair only; not normal feature delegation.

A dedicated repository-scout agent is no longer normal. The Lead queries Graphify first, then reads only the authoritative files required. The four v8.1 reviewer roles are consolidated into one fresh multi-mode assurance reviewer.

## Concurrency recommendation

Three is a strong ceiling for this workflow: it permits useful parallelism while keeping tool/context overhead and write conflicts bounded.

- **LIGHT:** normally 0–1 active subagent.
- **STANDARD:** normally 1–2. A third is allowed only for genuinely disjoint work.
- **CRITICAL:** up to 3 active. Additional specialist/review work uses sequential waves.

One writer owns each file/system/Studio root/Blender scene area at a time. A reviewer should normally start after the relevant writer reaches a stable checkpoint.

## Dispatch packet

Send only objective, owned scope, authoritative files/facts, relevant skills/tools, deliverable/evidence, stop conditions, and unresolved human decisions. Include Graphify query/path output only when it materially narrows the work. Never dump the full parent chat or raw tool logs into workers.

## Human gates

Proceed autonomously on ordinary reversible implementation details inside approved scope. Stop and ask for material creative/design forks, scope expansion, installations/MCPs/paid services, licensing uncertainty, migrations/destructive state changes, Production/shared-place mutation, monetization/compliance changes, security/persistence policy exceptions, or anything else that materially constrains the product.

## External production capabilities

BloxMaps and Blender MCP are **tools**, not extra agents. A WORLD task can therefore remain `Lead + content-production-worker (+ creative-director when needed)` while the worker calls deterministic MapGen and Blender authoring capabilities. UI tasks remain `Lead + creative-director/frontend-worker` and may use provider-neutral visual tools or optional BloxUI blueprints without spawning tool-specific agents.

`design.visual` is semantic and vendor-neutral. A runtime may bind it to Claude Design, another visual workspace, image tools, Studio prototypes or equivalent capabilities. The workflow/evidence requirements stay the same.

## v8.4 reasoning layer

Reasoning skills do not add roles or task lifecycles. The Lead uses compact human decisions by default, `decision-grilling` only for dependent consequential choices, and `external-questionnaire` when another person owns missing knowledge. `domain-modeling`, `codebase-design`, `primary-source-research`, and the bundled budget-aware `systematic-debugging` are loaded on demand. The fresh `assurance-reviewer` uses `assurance-two-axis` inside its existing modes. `workflow-retrospective` is explicit after meaningful friction, not a mandatory post-task pass. TDD is intentionally not part of the v8.4 default capability layer.
