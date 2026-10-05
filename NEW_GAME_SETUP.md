# New Game Setup — v8.5 Scope Evolution

This ZIP is an unconfigured reusable template. Do not develop inside the extracted template itself.

## 1. Create an empty private GitHub repository

Create a new repository with no README/license/gitignore so the scaffold can be copied without overwriting existing work.

## 2. Prepare the game checkout

From the extracted bootstrap root:

```powershell
python scripts/prepare_new_game.py `
  --repo-url https://github.com/OWNER/NEW-GAME.git `
  --destination C:\RobloxProjects\NEW-GAME `
  --maintainer OWNER
```

The helper refuses nonempty/conflicting destinations, token-bearing URLs, source/destination overlap and mismatched existing origins. It copies the scaffold and binds policy/configuration only; it does not commit, push, install tools/skills or touch Studio.

## 3. Review and create the first Git commit

Inside the prepared checkout, verify policy/CODEOWNERS/remote yourself. For a truly empty clone:

```powershell
git status --short
git remote -v
# after human review only:
git add .
git diff --cached --check
git commit -m "Add streamlined Roblox team scaffold"
git push -u origin main
```

## 4. Run streamlined developer setup

```powershell
python scripts/team.py setup --developer OWNER --runtime claude-code
```

This checks repository contracts, runtime adapters/model-policy config and pinned local tools. It deliberately does **not** force live Studio/MCP/Rojo validation before an idea can be captured.

### First shared external-skill resolution

The reusable ZIP contains project-authored skills and the reviewed installer/registry for external skills, but not the resolved external skill trees. The first maintainer may explicitly run:

```powershell
python scripts/team.py setup `
  --developer OWNER `
  --runtime claude-code `
  --initialize-shared-skills `
  --confirm-shared-change
```

Review the resulting skill lock/audits and use the existing supply-chain review process before merging shared bootstrap changes. Teammates later reuse the accepted lock; they do not refresh it during normal work.

## 5. Submit the game idea

Write a plain human `.txt`, then:

```powershell
python scripts/team.py idea --file .local/ideas/game.txt --owner OWNER
```

This is the normal v8 entry point. No separate proposal PR or promotion PR is required.

## Existing nonempty repository

Do not point `prepare_new_game.py` at it. Import the scaffold through a reviewed infrastructure branch/PR and resolve collisions deliberately.
