# TEAM PROTOCOL — v8.5 Scope Evolution

`AGENTS.md` is master. This file defines the human collaboration boundary.

## Normal task identity

One meaningful request uses:

- one GitHub Issue,
- one branch `feat|fix|docs/<issue>-<slug>`,
- one `04_CHANGESETS/GH-.../` folder,
- one implementation PR.

The original human `.txt` is copied byte-for-byte to `USER_REQUEST.txt`. Any local task reference files are likewise byte-copied into `REFERENCES/` and SHA-256 bound. `.gitattributes` marks both provenance surfaces `-text` so Windows CRLF/LF conversion cannot silently change their bytes. Do not edit them later.

## Human approvals

- Creating a remote Issue is an explicit remote action.
- Before substantial implementation, a human approves the designed scope (`team.py approve`).
- Before push/draft PR, the human explicitly approves publication.
- A different human reviews substantial PRs before merge.
- Merge and Roblox Production publish remain human actions.

Scope approval is not merge approval, and merge approval is not release/publish approval. Initial approval creates revision 1. Later material scope movement uses an explicitly approved `SCOPE_AMENDMENTS/` revision; it does not silently rewrite the prior approval. A DRAFT amendment has no authority yet, and only affected work pauses while it is unresolved. Amendment-specific files/URLs are copied/recorded with provenance rather than rewriting the immutable original intake. Final evidence and scope-aware Studio/full-quality receipts must match the active revision.

## Git safety

Never auto-stash, reset, discard, force-push, rewrite shared history or switch away from dirty work. Fetching is read-only to the working tree. If `origin/main` moved, inspect and deliberately integrate it.

## Studio safety

Use Beta/registered test places for feature development. Before live changes verify the actual Studio window, Universe/Place identity, backup and writer slot, plus separate MCP and Rojo connections. Never treat repo output as proof of live Studio output. Never publish Production automatically.

## Risk proportionality

LIGHT tasks use compact evidence. STANDARD tasks use relevant skills/subagents, native checks and live/review gates when applicable. CRITICAL tasks keep the full quality/security/persistence/economy/release evidence path. The Lead may escalate; it may not silently waive a gate.

## Personal state

`.local/` is per developer/worktree and ignored. Do not copy another developer's receipts or credentials. Shared skills/policy live in Git and are changed only through reviewed infrastructure work.


## v8.5 Human decision gates and lean agents

The Lead uses the capability-consolidated role set in `08_TOOLCHAIN/AGENT_ORCHESTRATION_V8_4.md`. Subagents are not a checklist: delegate only for specialist expertise, independent review, tool isolation or genuinely parallel read-only/disjoint work. Use `human-decision-gates` to stop for material scope, consequential creative direction, installs/MCPs/cost, licensing, destructive state, migrations, Production/shared-place mutation, monetization/compliance, security-boundary or model/policy exceptions. Use a compact decision block by default, `decision-grilling` only for dependent material decisions, and `external-questionnaire` when someone else owns missing knowledge. Routine approved implementation details do not require repeated permission prompts.

For MCP/tool work, use on-demand discovery and `MCP_CAPABILITY_PROFILES.json`. Studio's built-in MCP server is the default live Roblox bridge; Graphify is the recommended repo-intelligence capability; Blender MCP is the priority 3D asset-authoring bridge when relevant. New installs/addons still require explicit approval.
