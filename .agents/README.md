# .agents — Portable Agent Assets

`skills/` is the **only canonical skill root** in this repository. Every active project-authored or approved external skill ultimately lives at `.agents/skills/<name>/SKILL.md`.

Other agent-runtime files (native agent definitions, vendor-specific skill mirrors, MCP client configuration) are generated from `08_TOOLCHAIN/` contracts by `scripts/sync_runtime_adapters.py` and are not authoritative.

Do not create `AGENTS.md` files inside skill folders. Root `AGENTS.md` is the project master contract.
