# Graphify Policy — v8.2

Graphify is the preferred repository-intelligence layer for broad topology, dependency, impact and resume questions. It helps the Lead query a project graph first and then read the authoritative files, reducing repeated whole-repository scans and unnecessary scout delegation.

- Pinned default package: `graphifyy==0.9.74`. The `[mcp]` extra is intentionally not part of default setup because the bootstrap uses the CLI directly; enable `graphifyy[mcp]==0.9.74` only if a reviewed runtime specifically needs Graphify as an MCP server.
- Pinned reviewed source: `Graphify-Labs/graphify@e10df08877f8819a625a1afa38c3297a31fda296`.
- Default bootstrap use is **code-only/local** extraction. Do not enable semantic document/media extraction or a network model backend merely to build the code graph.
- Initial local build: `python scripts/graphify_sync.py build`.
- After pull/merge/structural code changes: `python scripts/graphify_sync.py update`.
- Query the graph before broad file scans, then open the repository files it points to.
- `graphify-out/`, `graph.json`, and transient Graphify state are generated/local and ignored by default.
- Graphify output is an index/inference layer, never authority. Repository files, Git, accepted task/design artifacts, GitHub, and live Studio evidence remain authoritative.
- Optional Graphify work-memory/reflection can summarize repeated outcomes, but accepted facts and human decisions still belong in canonical project artifacts.

Installation is handled by the read-only workstation doctor plus an explicit install flag. `uv tool` is preferred; `pipx` is the fallback. The bootstrap does not install either package manager silently.
