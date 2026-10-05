# Git workflow — streamlined v8

The normal project path is intentionally small:

`GitHub Issue -> feat/fix/docs task branch -> AI design + human scope approval -> implementation/tests -> one draft PR -> second-human review -> merge`

## Safe defaults

- `main` is accepted shared state. Do not implement directly on it.
- Start or resume work through `python scripts/team.py ...`.
- New work: `python scripts/team.py idea --file <request.txt>` or `python scripts/team.py update --file <request.txt>`.
- Existing work: `python scripts/team.py resume --issue N`.
- `team.py` fetches/fast-forwards a clean `main` when creating a new task; it never auto-stashes, resets, rebases, discards or force-pushes.
- On an existing task branch, fetch first. If `origin/main` moved, inspect the drift and deliberately merge accepted upstream only after the worktree is clean, then retest.
- The human-authored `04_CHANGESETS/GH-.../USER_REQUEST.txt` is immutable provenance and is protected from line-ending normalization.

## Before implementation

The Lead performs repository inspection, design/architecture/impact analysis and selects only relevant skills/subagents. Record risk and gates with the task packet. Substantial implementation waits for explicit human scope approval, normally recorded with:

```powershell
python scripts/team.py approve --issue N --by YOUR_GITHUB_USERNAME
```

If risk/gates materially change after approval, put the change in a revisioned scope amendment and obtain explicit amendment approval. The old revision remains authoritative until then; never mutate gates silently.

## Before a PR

Run the risk-aware checks:

```powershell
python scripts/team.py check --issue N
```

For a local/lightweight iteration you may use `--quick`, but a completed feature must satisfy its full risk gates. Native Rojo/StyLua/Selene and live Studio evidence are required when the task says they are applicable.

Preview remote publication first:

```powershell
python scripts/team.py pr --issue N
```

Only after explicit human approval:

```powershell
python scripts/team.py pr --issue N --confirm-publish
```

This opens a **draft** PR. It does not merge and never publishes Roblox Production.

## Merge and release

A different human reviews substantial work. Merge is performed by an authorized human/integrator after CI and applicable manual gates pass. Production release is a separate explicitly authorized action governed by `TEAM_RELEASE_CHECKLIST.md`.

## Legacy compatibility

`scripts/team_workflow.py`, `submit_proposal.py`, `intake_request.py` and `promote_proposal.py` remain so repositories with v7 proposal/promotion history can still be validated or migrated. They are not the normal v8 entry point.
