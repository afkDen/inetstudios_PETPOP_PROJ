# Context, Repository Intelligence and Memory — v8.4

The repository remains durable project memory. The current workflow uses **Graphify** as a recommended local repository-intelligence layer so agents can query project structure instead of repeatedly rereading the whole tree.

## Authority order

1. Current repository files + accepted `GAME_DESIGN.md` / ADRs / technical docs.
2. Active task `TASK.*`, `WORK_STATE.md`, evidence and human decisions.
3. Git/GitHub history.
4. Actual Studio/Blender source state and measured evidence.
5. Graphify index/work-memory as retrieval augmentation.
6. `.local/` temporary/session evidence.

Graphify is never authority for a mutation. Inferred or stale graph edges must be verified against current sources.

## Graphify workflow

- Build code-only locally after initial setup when Graphify is available.
- Update after pulls, merges and structural refactors.
- Query/path/explain before broad repository scans or spawning discovery-only agents.
- Read only the authoritative files returned by the query.
- Keep `graphify-out/`, `graph.json`, `.graphify/` local/ignored.
- Semantic extraction over docs/media and Graphify work-memory/reflection are opt-in augmentations; they may involve configured model backends and must not silently introduce cost/network data transfer.

## Task checkpoint capsule

At meaningful checkpoints record: goal/stage, branch/commit, accepted facts/decisions, changed files/Studio/Blender assets, tests/evidence, blockers/unresolved questions, and exact next action. This capsule is what a fresh conversation resumes from.
