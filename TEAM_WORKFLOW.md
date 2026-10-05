# TEAM WORKFLOW — v8.5 Scope Evolution

The public interface is `python scripts/team.py ...`. The deep skills/roles lifecycle remains; humans no longer manually drive separate proposal and promotion PRs.

## 1. Developer readiness

```powershell
python scripts/team.py setup --developer YOU --runtime claude-code
```

Reuse valid tools/skills. Do not silently install anything. Live Studio validation is deferred until a task requires it.

## 2. Capture an idea or update

```powershell
python scripts/team.py idea --file .local/ideas/game.txt --owner YOU
# later
python scripts/team.py update --file .local/ideas/pets.txt --owner YOU
```

You may pass `--issue N` when the Issue already exists. Otherwise the CLI asks before creating one with `gh`.

The command synchronizes clean `main`, creates one issue branch, preserves the raw request, creates `TASK.json`, `TASK.md`, `WORK_STATE.md`, compact `EVIDENCE.json`, and generates `.local/prompts/GH-...txt`.

## 3. AI design checkpoint

Paste the generated prompt into the approved runtime on the same checkout/branch. The Lead must inspect/understand/design/plan/specify first, use the risk router, select only relevant skills/subagents, fill the task plan and decide whether Studio/full quality evidence is required.

If scope approval is still PENDING, substantial implementation stops here.

## 4. Human scope approval

```powershell
python scripts/team.py approve --issue N --by YOU --note "Approved scope"
```

If design discovered higher risk, record it at approval with `--risk CRITICAL` or resolve gates before approval, for example `python scripts/team.py gates --issue N --studio-required yes`. This approval creates **scope revision 1** and does not authorize remote publication.

### 4a. Move approved scope deliberately

Approval is a safe checkpoint, not a promise that the feature can never evolve. For a material post-approval change, draft a revisioned amendment instead of silently editing `TASK.md` or invalidating the whole prior approval:

```powershell
python scripts/team.py amend --issue N --reason "Add another accepted behavior" --by YOU
```

New files/URLs that justify the change can be supplied with repeatable `--reference`; they are stored and hashed inside the amendment rather than mutating original intake references.

Edit the generated `SCOPE_AMENDMENTS/AMENDMENT-....md`. While it is DRAFT, the previous approved revision remains authoritative; unaffected work may continue, but work affected by the proposal pauses. Then explicitly approve it:

```powershell
python scripts/team.py approve --issue N --amendment 1 --by YOU --note "Approved revision"
```

Risk/gate changes can be included on that approval command. Gate de-escalation requires an explanatory approval note; lowering CRITICAL risk additionally requires a substantive scope change. A DRAFT amendment may instead be explicitly withdrawn. Final delivery blocks on unresolved amendments. By default, prior evidence is preserved but must be reviewed/refreshed for the new revision; after that review use `team.py evidence-scope` to attest applicability. Studio/full-quality receipts are also bound to the active scope revision. Explicit `retain` approval or `evidence-scope` can rebind existing receipts after human review of applicability; this writes an audit record and never changes their PASS/PENDING result. See `08_TOOLCHAIN/SCOPE_EVOLUTION_V8_5.md`.

## 5. Implement and test

The Lead follows:

`inspect → understand → design → plan → specify → implement → test → independent review → revise → verify → document → checkpoint`

For live Studio work follow `LIVE_STUDIO_DELIVERY.md`; for CRITICAL work use the full production quality contract. Keep `WORK_STATE.md` resumable.

## 6. Check

```powershell
python scripts/team.py check --issue N
```

This runs task integrity/risk gates, repository validators, unit tests, the disposable pipeline, pinned native build, formatting/lint where source exists, and any required Studio/full-quality packet validation.

During development, `--quick` skips heavyweight final checks but never implies completion.

## 7. Draft PR

```powershell
python scripts/team.py pr --issue N
```

Preview only. After explicit approval:

```powershell
python scripts/team.py pr --issue N --confirm-publish
```

An explicitly incomplete collaboration PR may use `--allow-incomplete`; it must stay draft and cannot be called accepted.

## 8. Review and merge

A different human reviews substantial work. CI and required manual/live gates must pass. Merge in GitHub through the authorized human process. Production publish/release is separate.

## Resume

```powershell
python scripts/team.py resume
```

Never create a duplicate task just because the AI conversation or computer session changed.

## Legacy v7 compatibility

`team_workflow.py propose/start`, `submit_proposal.py`, and `promote_proposal.py` remain for existing v7 history/migration. They are not the default v8 workflow.


## v8.5 orchestration note

Normal task steps remain unchanged, but the internal team is now capability-consolidated. The Lead normally uses 0–1 subagent for LIGHT work, 1–2 for STANDARD work, and never more than 3 active subagents for CRITICAL work. Additional specialists/reviewers run in sequential waves, not wider fan-out. Use `creative-director` + `frontend-worker` for substantial GUI/HUD design/implementation and `content-production-worker` modes for world/3D/VFX/SFX. One fresh `assurance-reviewer` uses FUNCTIONAL, EXPERIENCE, RISK and/or RELEASE modes only when those dimensions are material; combine related modes in one review context when efficient.

At any stage, a material decision matching `human-decision-gates` pauses the affected work for a concise human question. Approved routine implementation proceeds without ceremony.

## v8.5 references and external production tools

Idea/update intake can include repeatable references without changing the one-Issue/one-branch flow:

```powershell
python scripts/team.py update `
  --file .local/ideas/update.txt `
  --reference .local/references/hud.png `
  --reference https://example.com/inspiration `
  --owner YOU
```

Local reference files are copied into the changeset with hashes so teammates and fresh AI sessions can inspect the same source material. URLs are recorded verbatim. The Lead still decides which references are authoritative and how they may be transformed without copying protected work.

BloxMaps and Blender MCP are capabilities used *inside* the same task. They do not create extra Issues, branches, PRs, or permanent agents. Procedural world plans remain reviewable candidate artifacts before live Studio mutation.

## v8.5 decision/reasoning note

The workflow is unchanged structurally. During design, use the smallest decision mechanism: direct gate for one decision, Lead-controlled `decision-grilling` for a dependency frontier, and `external-questionnaire` for knowledge held by another human. Research and debugging must prefer existing cheap signals. TDD is not a bootstrap-wide requirement. Fresh review separates scope/spec fidelity from engineering/project standards inside the same assurance boundary.
