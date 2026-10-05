# v8 Streamlined — Final Bootstrap Audit

Date: 2026-09-24
Source reviewed: `roblox_team_bootstrap_v7_2_reusable(1).zip`
Outcome: `v8.0-streamlined`

## Executive summary

The v7.2 scaffold had strong safety, agent-role, skills, model-policy, Studio/Rojo and review concepts, but the normal human path exposed too many internal lifecycle stages. A simple feature could require an immutable proposal, proposal branch/PR, promotion, promotion branch/PR, implementation branch, multiple evidence packets and then an implementation PR. The result was robust in theory but expensive to operate and created failure modes in the workflow itself.

v8 keeps the deep orchestration but changes the public contract to **simple outside, sophisticated inside**:

`setup -> idea/update -> AI design -> human scope approval -> implementation -> check -> one draft PR -> human review -> merge`

Normal v8 work uses one GitHub Issue, one `feat|fix|docs/<issue>-<slug>` branch and one implementation PR. Legacy v7 proposal/promotion tooling remains only for compatibility/migration.

## Source audit snapshot

The extracted v7.2 package contained roughly 300 files when generated runtime mirrors were included, about 4,000 lines of Python in scripts/tests, dozens of workflow/support documents, 25 bundled canonical project skills, 63 registered skills total and 21 canonical provider-neutral roles. The depth itself was not the main problem; the issue was how much of that depth humans had to drive manually.

The original extracted self-test run also exposed three packaging/test-contract failures: one test assumed a `.git` directory existed in the reusable ZIP, and two toolchain-gate tests were blocked by the unconfigured-template precondition before reaching the condition they intended to test. Those test defects are corrected in v8.

## Findings and disposition

### 1. Excessive GitHub ceremony — HIGH — fixed

**v7.2:** normal idea work could traverse proposal branch/PR -> promotion branch/PR -> implementation branch/PR.

**v8:** one Issue + one task branch + one implementation PR. Human scope approval is recorded inside the issue-local task packet after AI design. Remote push/PR, merge and Roblox publish remain separately gated.

### 2. Raw request line-ending integrity — HIGH — fixed

The reusable v7.2 `.gitattributes` did not protect the normal issue-local raw request path. On Windows, line-ending normalization can change bytes and invalidate a hash/provenance contract.

v8 adds `04_CHANGESETS/**/USER_REQUEST.txt -text` and keeps legacy raw paths protected too. Tests explicitly cover exact byte/hash preservation, including CRLF/mixed/BOM-style input.

### 3. Human scope approval could become stale after design edits — HIGH — fixed

A status flag alone is insufficient if `TASK.md` can change after approval. v8 now records a SHA-256 fingerprint of the approved design/scope portion of `TASK.md`. Delivery-summary notes may evolve, but a post-approval change to interpretation/design/plan/acceptance scope invalidates validation until the task is reopened and approved again.

Risk/gate changes are also frozen after approval unless `team.py gates --reopen-approval ...` explicitly returns the task to design.

### 4. Studio validation was too early in the happy path — MEDIUM — fixed

A developer should not need a live Studio/MCP/Rojo session merely to submit an idea. v8 separates **repository/runtime readiness** from **live Studio readiness**. `team.py setup` can prepare/check a contributor; exact nonproduction Studio/MCP/Rojo verification happens when an approved task actually needs live work.

The low-level Studio validators remain in the system and are still required where the task gate says Studio is required.

### 5. Quality evidence was effectively one-size-fits-all — MEDIUM — fixed

v8 makes the existing risk router meaningful operationally:

- **LIGHT:** compact evidence, relevant checks, live Studio only when necessary.
- **STANDARD:** normal gameplay/UI/content workflow; relevant skills/subagents, native checks, Studio evidence when player-visible/Studio-dependent, independent review for substantial changes.
- **CRITICAL:** persistence, economy/monetization/RNG, networking/security, migrations/shared architecture/release-sensitive work; full quality packet and specialist review.

The heavyweight quality system remains available instead of being deleted.

### 6. Too many human-facing scripts/prompts — MEDIUM — fixed

`scripts/team.py` is now the public workflow surface:

- `setup`
- `idea`
- `update`
- `status`
- `resume`
- `prompt`
- `gates`
- `approve`
- `checkpoint`
- `check`
- `pr`

Deeper scripts remain implementation details or legacy compatibility tools.

### 7. Manual prompt placeholder handling — MEDIUM — fixed

Each task generates a ready-to-paste prompt under `.local/prompts/`. Issue number and known owner are resolved automatically. A new AI session reads the exact task/branch/change-set rather than requiring the human to reconstruct placeholders from memory.

### 8. Remote Issue creation could occur before local checkout reconciliation — MEDIUM — fixed

v8 reconciles a clean/current `main` before creating a new remote GitHub Issue. This avoids leaving a remote Issue behind merely because the local checkout was dirty, on the wrong branch or unable to synchronize.

### 9. Resumability existed but was awkward to invoke — LOW/MEDIUM — fixed

`team.py checkpoint --issue N --note "..."` and `team.py resume` expose the existing checkpoint idea directly. Durable repository state, not chat history, remains the source for resuming work.

### 10. Extracted reusable ZIP tests assumed Git history — LOW — fixed

The canonical-skill-location test now works both inside a Git checkout and in the intentionally Git-less reusable ZIP. Unit tests that target a deep initialization gate now isolate the gate rather than failing at an unrelated template precondition.

## Deep capabilities intentionally preserved

v8 retains:

- `.agents/skills/` as the canonical skill root and existing supply-chain controls;
- provider-neutral role/subagent contracts and runtime adapters;
- model/effort routing and fresh-context reviewer separation;
- full `inspect -> understand -> design -> plan -> specify -> implement -> test -> review -> revise -> verify -> document -> version -> checkpoint` lifecycle;
- server-authoritative Roblox engineering baseline;
- pinned Rojo/StyLua/Selene contract;
- filesystem-first Rojo mapping and Studio-owned world boundary;
- Studio MCP + separate Rojo live-sync verification for tasks that require it;
- independent human review before substantial merge;
- no automatic merge and no automatic Roblox Production publishing;
- legacy proposal/promotion validators for repositories that already contain v7 records.

## New task packet

A normal v8 task creates only:

- `USER_REQUEST.txt` — exact immutable human input;
- `TASK.json` — machine-readable identity/risk/gates/approval;
- `TASK.md` — interpretation, scope, design, plan, acceptance criteria and delivery summary;
- `WORK_STATE.md` — resumable checkpoint;
- `EVIDENCE.json` — compact risk-aware evidence state.

CRITICAL tasks can additionally use the existing `QUALITY_BRIEF.md`, `QUALITY_EVIDENCE.json` and `STUDIO_DELIVERY.json` contracts.

## CI / validation changes

Portable CI now combines:

- derived-document/model-policy/repository/team/Rojo static validation;
- unit tests and disposable pipeline simulation;
- PR immutability/integration-owner checks;
- risk-aware task delivery validation;
- pinned toolchain check + native Rojo build;
- StyLua/Selene when Luau exists.

Infrastructure/integration PRs are not forced to pretend they are gameplay task packets. Feature/source-changing PRs must use the task branch/changeset and satisfy their risk gates.

## Validation performed on this finalized package

Completed successfully in the audit environment:

- Python compile checks for scripts/tests;
- derived documentation check;
- shared model-policy structural validation;
- scoped Rojo layout static validation;
- streamlined team contract validation;
- portable repository contract validation;
- **166 unit tests** in the reusable scaffold;
- **166 unit tests** again in a freshly prepared future-game scaffold;
- disposable intake/plan/implementation/review/revision/checkpoint simulation;
- a functional dry-run of the new public flow: `idea -> gates -> design edit -> approve -> checkpoint -> status -> validate`, including exact raw-request SHA-256 equality and generated-prompt placeholder resolution.

The audit container does **not** have the pinned native Roblox tools installed (`rojo`, `stylua`, `selene` were reported missing), and it has no Roblox Studio/MCP session. Therefore this audit does **not** claim a native Rojo build, live Studio sync, viewport/gameplay evidence or Roblox publish. Those remain real workstation/task-time gates.

## Residual / intentional complexity

1. **First-time external skill supply-chain initialization remains advanced.** This is deliberate because it changes reviewed shared agent dependencies. Ordinary idea/update work does not rerun it.
2. **Legacy v7 scripts remain shipped.** They are useful for migrating/validating existing projects but increase internal file count. They are explicitly non-default.
3. **GitHub Actions use major-version action tags** (for example `actions/checkout@v4`) rather than immutable commit SHAs. Pinning to reviewed SHAs would further harden CI supply-chain reproducibility, but was not changed without externally verifying the intended action commits.
4. **Live Studio truth remains manual/tool-backed.** No static validator can prove that a screenshot/playtest came from the intended live place; human target verification remains required.
5. **The full model/runtime policy is still sophisticated.** It is hidden from normal human workflow, not removed, because the stated requirement was to preserve the existing skill/subagent/model orchestration.

## Final operating recommendation

For new games, use v8 as the bootstrap source. For an existing v7 game, do not interrupt an active issue merely to adopt v8; cut over on a reviewed infrastructure branch at a clean boundary, preserving all historical proposal/raw records. See `MIGRATION_V7_TO_V8.md`.
