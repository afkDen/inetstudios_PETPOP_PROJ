# PORTABILITY ARCHITECTURE

## Canonical vs adapter state

Canonical project truth is runtime-neutral: root `AGENTS.md`, `.agents/skills/`, role/capability contracts, project/change state, tests, review evidence, and Git. Runtime-specific files are generated adapters.

### Canonical instruction hierarchy
1. `AGENTS.md` — always-on master contract.
2. Canonical/state docs — loaded only as needed.
3. `.agents/skills/<name>/SKILL.md` — on-demand expert procedures.
4. `ROLE_CONTRACTS` — semantic responsibilities and isolation requirements.
5. Runtime adapters — translate, never redefine, canonical rules.

### Skill layout decision
All active skills use one flat canonical root `.agents/skills/<name>/`. Project vs vendor is metadata, not path. This maximizes compatibility with runtimes that support `.agents/skills` but may differ in nested-folder traversal.

### Runtime replacement
A runtime binds semantic capabilities and model classes. If native custom agents are unavailable, roles can be executed through fresh sessions/worktrees/remote/API workers while preserving independent review.

## Visual and production capability portability

`design.visual` is provider-neutral. Runtime adapters may bind it to Claude Design, another native visual workspace, image generation/editing, Roblox Studio prototypes, or structured mockup tooling. Canonical roles and acceptance evidence do not depend on one vendor.

BloxMaps is a pinned external tool capability and Blender MCP is an approved authoring bridge; neither is an AI model. They can therefore be used by any runtime that can execute approved local tools, preserving comparable production capability across agent vendors.
