---
name: graphify-repo-intelligence
description: Use Graphify as a local-first repository knowledge graph to answer topology, dependency, impact, path, and prior-work questions before broad scans or extra scout agents. Repository/Git/task/Studio state remains authoritative.
---

# Graphify Repository Intelligence

Use this skill when the Lead needs broad repository understanding, change-impact discovery, subsystem relationships, or a compact context slice for delegation.

## Policy

- Prefer Graphify before spawning a dedicated discovery/scout agent.
- Prefer local code-only extraction first: deterministic tree-sitter parsing, no semantic provider required.
- The graph is an index, never the source of truth. Verify any state-changing claim against current files, Git, task metadata, or Studio.
- Refresh after pulls, merges, large branch switches, or structural refactors.
- Do not enable semantic extraction of docs/media or external model backends without explicit project/human approval when it adds credentials/cost/network transfer.
- Keep graph output out of prompt-cache/tracked-state hot paths (`graphify-out/`, `graph.json`).

## Fast workflow

1. `python scripts/graphify_sync.py status`
2. If missing/stale and Graphify is installed: `python scripts/graphify_sync.py update` (builds code-only when no graph exists).
3. Query the graph for the exact question before broad reads.
4. Read only the authoritative files returned by the query/path/explain result.
5. Put only the relevant facts/paths into the specialist dispatch packet.

## Good questions

- What connects this controller to persistence/networking?
- Which modules are likely affected by this feature?
- Where is this UI state produced and consumed?
- What subsystem owns this concept?
- What recent changed files are in the same graph community?

## Work memory

Graphify work-memory/reflection features are optional augmentation. Useful/corrected outcomes may be recorded locally, but accepted product decisions still belong in `GAME_DESIGN.md`, pre-approval `TASK.md` or approved scope amendments, ADRs, issue/PR history, and other canonical repo artifacts.

## Stop conditions

Stop and verify directly when the graph is stale, a queried edge is inferred/low-confidence, a destructive change depends on the answer, or Git/Studio/task state disagrees with the graph.
