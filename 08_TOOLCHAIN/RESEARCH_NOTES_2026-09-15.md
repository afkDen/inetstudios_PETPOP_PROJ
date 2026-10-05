# Research Notes — 2026-09-15

Primary/current sources used to shape this bootstrap:

- Google Antigravity overview: https://antigravity.google/docs/overview
- Antigravity models: https://antigravity.google/docs/models
- Antigravity subagents: https://antigravity.google/docs/subagents
- Antigravity skills: https://antigravity.google/docs/ide/skills/
- Antigravity custom agents / CLI: https://antigravity.google/docs/cli/commands/agents/
- Antigravity MCP: https://antigravity.google/docs/mcp
- Antigravity headless/model/effort flags: https://antigravity.google/docs/cli/headless/
- Antigravity permissions: https://antigravity.google/docs/permissions
- Antigravity workflow-to-skills migration: https://antigravity.google/docs/migration/workflows-to-skills
- Roblox AI-accelerated workflows: https://create.roblox.com/docs/ai/accelerated-workflows
- Roblox Studio MCP: https://create.roblox.com/docs/studio/mcp
- Roblox docs agent index: https://create.roblox.com/docs/llms.txt
- Roblox Creator Store: https://create.roblox.com/docs/production/creator-store
- Roblox audio assets: https://create.roblox.com/docs/audio/assets
- nonlooped/roblox-suite: https://github.com/nonlooped/roblox-suite
- gamedev-skills/awesome-gamedev-agent-skills: https://github.com/gamedev-skills/awesome-gamedev-agent-skills
- Meshy API: https://docs.meshy.ai/en/api/quick-start
- Hyper3D Rodin API: https://docs.hyper3d.ai/en
- Tripo API: https://developers.tripo3d.ai/en/docs/introduction
- Poly Haven license: https://polyhaven.com/license
- Quaternius license: https://quaternius.com/license.html

## Architecture corrections made against the original directive

1. Use `.agents/skills/` as the primary workspace skill path.
2. Use `.agents/agents/` for reusable custom agents/subagents.
3. Use `.agents/mcp_config.json` only when manual MCP configuration is needed; Roblox Studio Quick Connect is preferred.
4. Do not invest in legacy Antigravity Workflows; migrate repeatable processes to Skills.
5. Prefer built-in/official Roblox Studio MCP rather than redundant community bridges.
6. Keep paid asset providers disabled until a real need appears.
7. Treat model routing as provisional configuration and use `agy models` / benchmarks rather than assuming a frozen lineup.


## Skill/API expansion pass
- Adopted project-local skill adapters covering the full Roblox Suite domains plus game design, level design, game feel, UI/UX, input, performance, procedural generation, accessibility, world building, QA, security, asset production, and skill supply-chain review.
- Added explicit agent↔skill routing and specialist agents for architecture, world building, assets, playtesting, performance, UI/UX, and persistence review.
- Confirmed Meshy API is credit-based/paid and removed it from the no-cost default path. Hyper3D Rodin is also credit-based.
- Adopted Poly Haven Public API as the primary no-auth commercial-safe asset metadata/search API; assets are CC0 and live API use requires source credit.
- Added Openverse as discovery/reference API with mandatory original-license verification.
- Kept Roblox Open Cloud optional and first-party; enable only when a concrete automation workflow needs a scoped key.
- Added local-tool detection for Blender, glTF-Transform, FFmpeg, Node, and npx.

## Final source verification — 2026-09-15

- Antigravity 2.0/CLI custom agents are workspace-discovered under `.agents/agents/`; current docs list explicit tool allowlists, `flash`/`pro` model tiers, command execution policy, skills, and MCP configuration. The current changelog documents `inheritCustomizations` as the unified ambient inheritance switch.
- Antigravity workspace skills remain under `.agents/skills/`; legacy workflows are being migrated to skills.
- Current Antigravity models include Gemini 3.8 Flash, Gemini 3.1 Pro, Claude Sonnet/Opus 4.6 (thinking), and GPT-OSS-120b; exact availability is still validated at initialization.
- Roblox Studio's official MCP Quick Connect currently lists Antigravity as a supported client.
- Poly Haven's live API is currently free for commercial use with no key for default endpoints; API-service attribution and a unique User-Agent are required, while the assets themselves remain CC0.
- Openverse remains discovery-only in this pipeline: unauthenticated access is supported, but Openverse explicitly does not guarantee license metadata accuracy, so original-source license verification remains mandatory.
- The Agent Skills installer is pinned to `skills@1.5.26` (current reviewed release on 2026-09-15) rather than `skills@latest`; upstream skill content still goes through static audit, whole-tree hashing, and semantic review before readiness.
