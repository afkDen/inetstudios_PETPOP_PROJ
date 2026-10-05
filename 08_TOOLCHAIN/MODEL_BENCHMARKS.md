# MODEL BENCHMARKS

No project-specific model benchmark has been run yet.

## Required before changing a major role mapping

Compare candidates on:
- Roblox/Luau correctness;
- architecture;
- instruction following;
- MCP/tool use;
- debugging;
- long-task reliability;
- structured outputs;
- context handling;
- subagent behavior;
- security review;
- test/review quality;
- speed and quota/cost pressure.

## Initial benchmark set

1. Implement a small server-authoritative interaction with a validated RemoteEvent.
2. Review a deliberately vulnerable RemoteEvent handler.
3. Diagnose a synthetic persistence race/migration issue.
4. Create a deterministic implementation package from a rough request.
5. Inspect a medium repository and return only evidence-backed dependency findings.

Record: candidate, role tested, tasks, compared-against, quality, tool use, reliability, speed, cost posture, decision (`TRIAL / ADOPT / REJECT / DEFER`).
