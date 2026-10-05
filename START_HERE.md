# START HERE — v8.5 Scope Evolution

## If this is the reusable ZIP

Prepare a separate game repository first with `NEW_GAME_SETUP.md` / `scripts/prepare_new_game.py`. Do not develop directly inside the template.

## If this is already a prepared game checkout

Run once per developer/runtime as needed:

```powershell
python scripts/team.py setup --developer YOUR_GITHUB_USERNAME --runtime claude-code
python scripts/team.py doctor
```

The doctor is read-only and reports core tools, GitHub CLI automation, first-time skill-resolution prerequisites, Graphify readiness and creative/Blender readiness. Graphify is recommended for repository intelligence; MCP for Blender is priority infrastructure when the task needs Blender-suitable 3D assets. Review `.local/WORKSTATION_FIX_PLAN.txt` before any install flags.

Use `codex`, `antigravity`, or `generic` when appropriate. Setup checks the repository, runtime adapters, model-policy config and pinned local tools. **It does not force a disposable Studio playtest before you can even write an idea.** Live Studio validation occurs when an approved task actually needs Studio.

Then use exactly one of:

```powershell
python scripts/team.py idea --file .local/ideas/game.txt --owner YOU
python scripts/team.py update --file .local/ideas/update.txt --owner YOU
python scripts/team.py resume
python scripts/team.py status
```

The generated `.local/prompts/GH-...txt` is the normal prompt to paste into Claude Code/Codex. The Lead keeps the full inspect/design/skills/subagents/test/review pipeline internally.

Legacy v7 proposal/promotion commands are supported for old repositories only; do not use them for a new v8 task unless a maintainer explicitly chooses migration mode.


## v8.5 agent behavior in one minute

The Lead should not spawn every specialist. LIGHT work normally uses 0–1 subagent; STANDARD normally 1–2; CRITICAL may use up to 3. **Never run more than three subagents at once.** Additional specialist/review passes happen in sequential waves. One fresh `assurance-reviewer` can cover FUNCTIONAL / EXPERIENCE / RISK / RELEASE modes as relevant. Subagents get compact task packets, not the whole conversation.

If a consequential choice has no canonical answer, the Lead should ask you with a recommendation/options and stop only the affected work. New MCPs/packages/addons, paid/external services, Production/shared-place mutation, destructive state changes and significant scope/creative forks all require explicit approval.

For player-facing production, route through the consolidated specialists: `creative-director`, `frontend-worker`, `content-production-worker`, `studio-operator`, then a fresh `assurance-reviewer` in EXPERIENCE mode and/or `assurance-reviewer` in FUNCTIONAL mode when justified.


## Moving scope after approval

Approval is revisioned, not permanent lock-in. If you want a material change after initial approval, use `python scripts/team.py amend --issue N --reason "..."`, edit the generated amendment, then approve that numbered amendment. The previous approved revision stays active until the new one is approved; unaffected work may continue. See `08_TOOLCHAIN/SCOPE_EVOLUTION_V8_5.md`.
