# Production Quality Contract — Risk-Proportional v8

The quality system exists to prevent fake completion, not to make every tiny change produce a dossier. `08_TOOLCHAIN/WORKFLOW_PROFILE.json` defines LIGHT / STANDARD / CRITICAL tiers.

## Universal truth rules

For every tier:

1. Never claim Studio, screenshots, playtests, device checks, subagent reviews or model/tool execution that did not actually happen.
2. `USER_REQUEST.txt` is provenance, not a design specification. Effective approved scope is the base TASK.md plus APPROVED scope amendments in revision order; DRAFT amendments have no authority.
3. A build/lint/unit test is not a live gameplay test.
4. Blockouts, skeleton UI and stub interactions must be labeled `BLOCKOUT` / `PARTIAL`, not complete.
5. Human aesthetic approval and human PR review cannot be replaced by an AI self-report.

## LIGHT

Use for a small, contained, reversible change with no persistence/economy/security/release impact.

Required by default:
- task integrity and human approval of the active scope revision,
- relevant static/unit/native checks,
- compact `EVIDENCE.json`,
- quick Studio verification only when the actual behavior/visuals cannot be validated honestly without it.

Fresh independent AI review is optional unless the Lead finds meaningful risk.

## STANDARD

Use for ordinary gameplay, UI, content and system work.

Required as applicable:
- relevant canonical skills and scoped specialist roles/subagents,
- clear effective-scope design/architecture/acceptance criteria (TASK.md plus approved amendments),
- native Rojo build + formatting/lint,
- real Studio delivery evidence for player-visible or Studio-dependent behavior,
- fresh independent review for substantial changes,
- real UI/device/visual evidence when those areas changed.

`EVIDENCE.json` is the default compact packet. `QUALITY_BRIEF.md` may be used for substantial visual/UI work even when the task is not CRITICAL.

## CRITICAL

Use for persistence/DataStores, economy/monetization/RNG, security/networking authority, schema migration, shared architecture, or release-sensitive work.

Required:
- full `QUALITY_BRIEF.md` before implementation,
- issue-local `QUALITY_EVIDENCE.json`,
- `STUDIO_DELIVERY.json` whenever the feature has a live Studio acceptance path,
- relevant security/persistence/performance/economy specialist review,
- fresh independent review with implementer/reviewer separation,
- rollback/migration considerations,
- explicit human verification of manual/live gates.

The v8.5 full packet also binds to the active scope revision. Validate it with `scripts/validate_feature_evidence.py`; that validator checks structure/path separation, not whether a screenshot is beautiful or a claim is truthful.

## Art / UX

For substantial visuals define art direction before final production: silhouette family, scale, materials/palette, lighting, camera distance, references/anti-goals and performance budget. Use coherent sourced/licensed assets or creator-authored work. Do not use unrelated asset piles merely to avoid an art decision.

For substantial UI define screen/interaction behavior and real state bindings, including loading/error/empty/disabled states and relevant mouse/touch/controller/keyboard paths. Test intended form factors when they matter.

## Studio delivery

When TASK.json says `studio_required: true`, follow `LIVE_STUDIO_DELIVERY.md`. v8.5 Studio receipts bind to the active scope revision; a receipt from an older revision is structurally stale even if its underlying observations may later be reviewed and re-established. Verify the actual nonproduction place/window, separate MCP and Rojo connections, managed-tree sync, real input/run/console/viewport evidence and a human target check.

A disconnected runtime can still design or produce an explicitly incomplete draft, but it must report the live gate as BLOCKED/PENDING.

## Skill/subagent evidence

Do not run every skill or every agent. The Lead selects only relevant skills/roles. For CRITICAL work and substantial visual/UI production, retain skill-use/reviewer evidence sufficient to show what was actually used and that the final reviewer was independent.

## Merge boundary

CI can verify repository structure, task integrity and evidence shape. Humans remain responsible for scope, aesthetics, real-world Studio truth and final merge/release decisions.
