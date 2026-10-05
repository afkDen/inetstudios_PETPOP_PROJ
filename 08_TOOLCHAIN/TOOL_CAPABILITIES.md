# Tool capabilities — v8.2

Tools are discovered and loaded on demand. Do not give every subagent every MCP/tool definition. Use the minimum capability group needed for the owned scope, verify the target before mutation, and preserve real evidence for writes.

## Roblox Studio MCP

Primary live Roblox bridge for `studio-operator`. Verify the exact nonproduction universe/place, open Studio window, branch/task ownership and writer slot before mutation. Studio evidence remains task-local and cannot be replaced by static reasoning.

## Graphify

- Pinned published package: `graphifyy==0.9.74`.
- Reviewed source: `Graphify-Labs/graphify@e10df08877f8819a625a1afa38c3297a31fda296`.
- Default use: local code graph and query/update workflow; semantic document/media extraction is opt-in.
- Intended user: Lead/orchestrator before broad repository scans.
- Graph output is assistive, not canonical memory.

## MCP for Blender

- Priority 3D authoring capability for `content-production-worker`.
- Pinned package: `mcp-for-blender==2.1.3`.
- Reviewed source: `ahujasid/mcp-for-blender@60d2a31b4632a7bc178f3dd636f7e68dfb5c8ae4`.
- Bootstrap prerequisites: Blender 4.2+ and Python 3.10+; `uv tool` preferred, `pipx` fallback.
- Default connection posture: localhost, `BLENDER_MCP_SAFE_MODE=1`, `DISABLE_TELEMETRY=true`.
- It can execute Python inside Blender, so target verification, one-writer ownership, backups and human gates for unsafe/network/paid-provider changes are mandatory.

See `MCP_CAPABILITY_PROFILES.json` and the matching skill files for role-specific policies.

## BloxMaps external production capability

The pinned `afkDen/bloxmaps` fork is an isolated local tool capability, not an MCP and not an AI vendor dependency. `content-production-worker` may use it for deterministic world plans and the asset-manifest bridge. `frontend-worker` may use BloxUI blueprints only as an optional accelerator. See `BLOXMAPS_INTEGRATION.json` and `BLOXMAPS_SETUP.md`.
