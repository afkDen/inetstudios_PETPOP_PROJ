# v7.2 reusable bootstrap port — 2026-09-24

Source basis: user-provided v7.1 reusable ZIP, an earlier game archive and historical agent session log. This is a **template revision**, not a new Roblox place deployment or GitHub PR.

- Ported source changes from archived earlier-game: Windows npx launcher resolution (`npx.cmd`), CRLF-safe owned runtime adapter migrations / LF-precise writes, relocatable skill-audit root, lock/provenance validation after first bootstrap, and Windows-compatible symlink tests.
- Ported the CI fixture change to isolate `GITHUB_HEAD_REF` (both absent and present) without changing production branch detection.
- `NEW_GAME_START_PROMPT.txt` provides a consent-gated, single-session path from an empty new repository through the authorized shared-initialization PR, with mandatory direct-evidence stops.
- New-game safe binding helper: no bundled Git history, never reset/push/commit or overwrite a populated destination; project remote identity, human integrator, CODEOWNERS, onboarding, Rojo name and proposal issue URL are configured per game.
- Deliberately absent: earlier-game external skill trees/lock/semantic approval, personal runtime receipts, Baseplate screenshots, local credentials and earlier-game branch history. Exact 38 required skills still come from the new game's approved bootstrap process.
- Historical scaffold audits bundled in `05_RELEASES/` describe the template architecture; they are **not** fresh CI, model, Rojo or Studio proof for another game.
- Local automated tests on the prepared package can verify its structural contracts. Native Windows Rokit/Rojo, upstream skill access, GitHub CI and same-place Studio MCP/live sync/playtest all require direct revalidation in the target new game.
