# Decision Log

## D001 — Repository is authoritative memory
Chat history is not required for continuation.

## D002 — Official Roblox Studio integration is the primary live bridge
Prefer Roblox's official Studio MCP or an equivalent first-party bridge supported by the active runtime. Product-specific connection UX is adapter configuration, not project architecture; redundant community bridges require a demonstrated capability gap.

## D003 — Open Agent Skills are canonical reusable procedures
New reusable procedures live in `.agents/skills/` using portable `SKILL.md` packages. Vendor-specific workflow systems may be used only as generated adapters when necessary; they are never canonical project memory.

## D004 — Small initial toolchain
No paid external 3D/audio provider is enabled until a concrete project need justifies cost, dependency, and quality tradeoffs.

## D005 — Runtime model mappings are configuration
Stable role definitions survive model changes. Model changes update toolchain documents, not project history or IDs.

## 2026-09-17 — Canonical instruction and skill layout

- Root `AGENTS.md` is the master project operating contract.
- `.agents/skills/` is the single canonical active skill root for both project-authored and approved external skills.
- Project vs external origin is metadata in `08_TOOLCHAIN/SKILL_REGISTRY.json`, not a separate directory tree.
- Runtime-specific skill mirrors/custom-agent files are generated adapters and are not authoritative.
- Canonical roles and model classes are provider-neutral; runtime/model changes update runtime validation, not project state.
