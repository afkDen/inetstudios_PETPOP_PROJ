# Team model governance v7.1 — reconciliation and final release audit

Date: 2026-09-23. This is a targeted hardening release on top of tagged v7
(`team-model-policy-v7-2026-09-23`). It does not modify the game design or
change the shared team policy approved for v7.

## One canonical operating policy

- `AGENTS.md` remains the master. `.agents/skills/` remains the sole canonical
  tracked skill root. The 21 role contracts remain provider-neutral, and
  `08_TOOLCHAIN/TEAM_MODEL_POLICY.json` remains the sole shared model/effort
  mapping. Vendor-specific agent files are generated locally and ignored.
- Claude Code uses `claude-opus-5-5` with LOW for narrowly scoped FAST work and
  MEDIUM elsewhere; HIGH is forbidden across all team Claude roles.
- Codex uses `gpt-6-sol`, LOW for FAST, MEDIUM for ordinary work, and HIGH
  *only* in separately approved issue-scoped DEEP/REVIEW_DEEP contexts. A
  temporary HIGH agent must be deactivated at task closure.
- Antigravity prefers `gemini-3.8-flash` at MEDIUM if actually selectable and
  verifiable. Its generated agents inherit the validated session model rather
  than silently changing families to satisfy role labels. Unsupported effort
  controls block/limit local readiness or require the documented FAST-only
  fallback; static frontmatter is never evidence of a real delegated run.
- Other runtimes require a human-approved model and direct proof of actual
  main/delegated settings. A policy change invalidates local model receipts.

## Reconciliation fixes in v7.1

1. Claude's `studio-operator` inherits dynamic live MCP tool names without an
   incorrect hardcoded allowlist, but explicitly denies direct `Edit`/`Write`.
   This does not sandbox `Bash` or authorize an MCP server; the workstation's
   live permissions, correct-place Studio connection and Rojo delivery gates
   still apply.
2. The Codex generator checks all owned/unmanaged agent conflicts before
   creating default `.codex/config.toml`, preventing a partial local setup.
   Runtime regeneration preserves a teammate's unmanaged agents and does not
   remove temporary issue-scoped HIGH exceptions.
3. Added `python scripts/validate_model_policy.py --check-config` for explicit
   static policy validation. CI now runs it before unit tests. This mode never
   claims a provider session was verified; full runtime readiness still
   requires hash-bound local execution observations and a human confirmation.
4. Regression coverage includes both the dynamic MCP tool boundary and the
   config-creation conflict path. Existing unit tests cover exact model and
   effort limits, policy-hash invalidation, symlink and local-edit protection,
   missing delegated observations, issue-specific HIGH variants, and
   integration-owned path changes on feature PRs.

## Release-gate evidence and limits

Release candidates must pass repository, team, Rojo layout, static policy,
derived-document and compilation checks; all Python tests; the disposable
request-to-review-to-checkpoint simulation; and `git diff --check`. A clean
clone of the committed release must be tested, and the packaged ZIP must be
re-extracted and verified. The final results for this v7.1 package are recorded
in the accompanying standalone audit and checksum.

**Not performed by this release:** real provider-account model observations,
live Antigravity/Claude/Codex subagent execution on teammates' computers,
native Rokit/Rojo/StyLua/Selene installation, real Studio MCP Quick Connect,
Rojo live sync, a real Studio playtest, or pushing to GitHub. These stay
explicitly blocked until each human operator performs the local bootstrap.
The scaffold remains `INITIALIZATION_REQUIRED` by design; the requested team
model policy is configured and portable but not an account-level enforcement
mechanism.
