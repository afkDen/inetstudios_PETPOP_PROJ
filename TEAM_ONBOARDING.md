# Team Onboarding — v8.5 Scope Evolution

1. Clone the accepted game repository; do not develop from the reusable ZIP.
2. Verify `git remote -v` points to the intended game.
3. Run:

```powershell
python scripts/team.py setup --developer YOUR_GITHUB_USERNAME --runtime claude-code
```

Use the runtime you actually have. Do not copy another person's `.local/` receipts or credentials.

4. For assigned work:

```powershell
python scripts/team.py resume
```

For a genuinely new request:

```powershell
python scripts/team.py update --file .local/ideas/my-update.txt --owner YOUR_GITHUB_USERNAME
```

5. Let the generated task prompt drive skills/subagents internally. You do not manually run every role.
6. Ask before remote Issue creation, pushes/PRs, installs, shared Studio writes, merges or publish/release actions.
7. Different teammates use different branches/worktrees/clones. Never point two active Rojo writers at the same shared Beta place simultaneously.

## Optional task capabilities

For world-generation work, `team.py doctor` reports the pinned BloxMaps adapter. Install it only when needed with `team.py setup ... --install-bloxmaps`. For visual tasks, use whatever approved visual-design capability your runtime actually exposes; no teammate is required to use Claude Design specifically.
