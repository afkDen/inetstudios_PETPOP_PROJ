# First Import — Prepared New-Game Checkout (v8)

Target remote: `https://github.com/afkDen/inetstudios_PETPOP_PROJ.git` (replaced by `scripts/prepare_new_game.py`). The ZIP ships without Git history, personal runtime state, resolved third-party skill lock or deployment rights.

1. Create a genuinely new empty GitHub repository, clone it, and use `scripts/prepare_new_game.py` to fill that empty clone.
2. Inspect origin, TEAM_POLICY, PREPARED_GAME.json, CODEOWNERS and the working tree. Review before the first commit/push.
3. After the scaffold is accepted on main, run `python scripts/team.py setup --developer YOU --runtime <runtime>`.
4. The first maintainer resolves the shared external-skill lock only when absent, using the explicit `--initialize-shared-skills --confirm-shared-change` path and a reviewed infrastructure change. Teammates reuse accepted shared state.
5. Invite collaborators and use `TEAM_ONBOARDING.md`.
6. Start the first real game request with `python scripts/team.py idea --file ...`. No separate proposal/promotion PR is required.

For a nonempty existing repository, do not use `prepare_new_game.py`; import through a reviewed infrastructure branch while preserving existing files/history.
