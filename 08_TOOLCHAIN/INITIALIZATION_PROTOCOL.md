# INITIALIZATION PROTOCOL — v8

Root `AGENTS.md` is authoritative. v8 separates durable/project readiness, developer/runtime readiness, and task-time live Studio readiness.

## Project-level gates

Durable, normally completed once per game: repository identity/structure, Git, canonical project skills, reviewed external skills/lock, skill supply-chain review, repository tests, credential policy and CI/toolchain configuration.

## Developer/runtime gates

Validated per developer/runtime when needed: local profile, actual model policy evidence for delegated work, skill discovery, role/context isolation, and pinned developer binaries for native implementation.

These remain personal under `.local/`; switching runtimes does not rewrite shared project state.

## Task-time Studio gates

Studio MCP, same-branch Rojo live sync and playtest evidence are required only when the approved task needs live Studio acceptance. They are fresh task evidence, not a permanent blanket initialization claim.

A developer may capture an idea, inspect code and perform planning without a live Studio session. They may not claim a Studio-dependent feature complete until the issue-local live gate passes.

## Canonical skills

All active skills resolve to `.agents/skills/<name>/SKILL.md`. External installation uses the reviewed project-scoped installer/lock. Runtime mirrors are generated adapters and do not prove provenance/execution.

## Runtime execution modes

- `FULL_NATIVE`
- `FULL_EMULATED`
- `PLANNING_ONLY`
- `READ_ONLY`

Use the mode honestly for the operation at hand; do not convert missing live tooling into fake PASS.
