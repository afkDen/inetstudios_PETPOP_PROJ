# Team collaboration migration — comprehensive review and release record

Date: 2026-09-23. Scope: the local `portable_agentic_roblox_dev_system_FINAL_v2.zip` as input, upgraded for a single shared GitHub repository and independent developer runtimes. This document records **local tests**, not a live GitHub/Studio deployment.

## Audit finding → remediation

| Finding | Risk | Implemented response |
|---|---|---|
| Global runtime validation file keyed only by runtime | Two contributors using Claude Code could overwrite each other's status; tracked personal evidence leaks to other branches | Tracked file is now an empty schema template; evidence lives under ignored `.local/RUNTIME_VALIDATIONS.json`, keyed by `developer::runtime` for team use. Full and planning-only local validation use `--finalize-local` and do not touch main. |
| Shared sequential `U###` allocation on parallel branches | Simultaneous clones may allocate the same update ID | Shared proposals use unique GitHub Issue numbers (`GH-000123`) for raw input and changesets; legacy sequential intake requires explicit `--solo`. |
| Auto-consuming the shared raw input inbox | Agents may process unapproved drafts or the same update twice | Branch-local immutable raw proposals, issue/PR approval, deterministic changeset via `--proposal --issue`; humans promote only approved/merged input on `main`. |
| No distinction between proposal and approved game vision | Unreviewed suggestions could override game scope | Immutable proposal branches + human scope approval + initial one-time accepted idea copy + approved update archive. Original bytes and SHA-256 recorded in sidecars. |
| Project initializer rewrites shared state on each workstation | Local model/machine configuration can dirty Git or falsely claim shared readiness | Per-developer local join script, explicit `--initialize-global` maintainer gate, guarded global finalize/staging on main or approved infra branch, separate honest `--finalize-local` modes. |
| AI Lead assumed single developer | Agent could approve/merge/release another contributor's work | `TEAM_PROTOCOL.md`: AI Lead is branch-scoped; human task owner and second reviewer; integrator controls main and Studio/release; no autonomous merge/publish. |
| No GitHub contribution templates/CI | Inconsistent evidence, missing reviews or accidental untested changes | GitHub Issue forms, PR checklist, advisory CODEOWNERS and limited-permission offline Python CI; live Studio gated by human evidence. |
| Skills/roles could fork per developer | Different AI products might silently load inconsistent procedures | Root AGENTS.md remains master; single locked `.agents/skills/` root; generated vendor adapters ignored; model version and personal configs kept in `.local/`. |
| Ambiguous code-vs-Studio authority | Two agents may overwrite Studio edits or lose non-script changes | Initial scripts-in-Git boundary, one sync scheme per script subtree (Script Sync or Rojo, not both), named Studio integration owner, separate test places. |
| Release/version collisions and ownership ambiguity | Local branches or models could mint competing official versions | Official releases/tags on main by a human release owner; independent personal branch history/experimental test place; release checklist and human governance. |
| Repository URL assumed deployed | Copying ZIP or setting a remote cannot prove repo content or GitHub permissions | `TEAM_IMPORT_GITHUB.md` requires checking existing remote/default branch and reviewed import without force push; GitHub authorization remains a human step. |
| Cost and security blind spots | CI/model/API usage could incur charges or leak secrets | Credential-free Actions with read-only contents permission and timeout; paid external generation disabled by default; private GitHub Free budget and branch-protection limitations documented. |

## Sources of truth

- Shared: `AGENTS.md`, `.agents/skills/`, `08_TOOLCHAIN/TEAM_POLICY.json`, canonical game docs and accepted `main` history.
- Per-issue branch: original proposal `GH-*.txt` plus JSON hash, issue-scoped changeset, tests and review packet.
- Personal per-worktree: ignored `.local/`, `.env.local`, model/runtime versions and workstation Studio evidence. A tracked empty runtime template does not mean any workstation was validated.
- Generated-only: vendor agent adapters, skill mirrors and scratch outputs; never canonical.

## Current validated scope

The migration runs locally with offline static validation, all project/team unit tests, Python compilation and the disposable legacy lifecycle. Team-specific tests exercise byte preservation including CRLF/non-UTF-8, metadata/hash tampering, duplicate IDs, issue-scoped collision avoidance, one-time approval copies, update promotion dependencies, local runtime isolation, partial model modes and idempotent local finalize. Local two-contributor Git simulation passed: Alice/Bob separate proposal branches; independent issue IDs and automated PR checks; clean merge of both proposals; one-time approved game-idea copy; issue-scoped Bob changeset and personal Claude setup with no tracked drift; merged update archive; deliberate unauthorized global-state edit and immutable raw-input tampering both rejected. This was a **local Git simulation**, not proof of real GitHub access, PR approval or Roblox Studio integration. Re-run tests on the exact distributed ZIP as the final release check. No live remote GitHub change, upstream skill acquisition, authentication, shared Studio MCP call or real Roblox multiplayer test was performed here.

## Remaining manual gates

- Real GitHub repository contents and permissions are **unverified in this sandbox**. Import into its existing branch after inspection; invite collaborators and configure rules as allowed by plan. Never force-push this ZIP's `.git` history over existing work.
- The 38 upstream external skill selections remain declared, not physically bundled in this release. The first approved global skill installation/semantic supply-chain review must be completed and committed by the integrator before local full readiness can be claimed by friends.
- Each friend's live runtime/model/agent isolation and Roblox Studio bridge need genuine workstation evidence. A browser chat is planning/review-only unless connected to a capable execution environment.
- GitHub Free private repositories may not enforce required PR reviews/status checks; use human policy and review until technical enforcement is available. GitHub Actions private minutes have a free allowance but are not unlimited. Choose a CI budget and limit secrets exposure.
- Team ownership, asset licensing, experience publish rights, credit and revenue splits require human agreement outside AI chat.

## Acceptance principle

The *team scaffold* can be considered locally release-tested while the *live team workspace* remains `INITIALIZATION_REQUIRED` until these real-world gates succeed. Automated simulation is never described as real GitHub permissions or real Roblox Studio access.
