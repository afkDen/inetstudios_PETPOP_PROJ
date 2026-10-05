# Initialization and Readiness — v8.5 Scope Evolution

v8.5 preserves the separation between **project/developer readiness** from **live Studio task readiness** so a team can capture/design work without performing an unrelated disposable Studio session first.

## Readiness layers

### A. Project/shared readiness

- prepared repository identity and matching origin
- canonical `.agents/skills/` architecture
- reviewed external skill lock when full delegated roles need those skills
- repository/CI contracts
- provider-neutral roles/capabilities

### B. Developer/runtime readiness

- local team profile and generated runtime adapters
- shared model policy structurally valid
- actual model/delegation receipt when delegated execution is needed
- pinned Rojo/StyLua/Selene available when native build/test is needed

### C. Live Studio task readiness

Checked only when an approved task requires Studio:

- intended nonproduction Universe/Place/window confirmed by a human
- official MCP connected to the actual active runtime
- separate Rojo plugin connected to `rojo serve` from the exact task branch
- managed paths verified
- genuine playtest/console/viewport evidence

See `02_TECHNICAL/LIVE_STUDIO_DELIVERY.md`.

## Normal developer command

```powershell
python scripts/team.py setup --developer YOUR_GITHUB_USERNAME --runtime claude-code
```

This is safe to repeat. It reuses valid state and reports PASS/PENDING rather than inventing readiness. It also runs the read-only workstation doctor, which distinguishes core Roblox tools, Graphify repository intelligence, and Blender asset-authoring readiness.

For a standalone report:

```powershell
python scripts/team.py doctor
```

Graphify is recommended but does not block idea capture. Blender MCP is required only when an approved task actually needs Blender-suitable 3D asset authoring. BloxMaps is priority for procedural world/layout tasks but is also task-scoped; pure scripting/UI work does not wait for it.

Recommended isolated CLI capabilities may be installed only after explicit approval and only through already-installed `uv` or `pipx`, plus Rokit:

```powershell
python scripts/team.py setup --developer YOU --runtime claude-code --install-recommended
```

To also modify Blender by installing/updating the MCP addon:

```powershell
python scripts/team.py setup --developer YOU --runtime claude-code --install-recommended --install-blender-addon
```

The bootstrap never silently installs Python, Blender, Node, Rokit, uv or pipx themselves. Those are machine-level prerequisites and the doctor gives exact remediation instead of consuming agent time troubleshooting them.

Missing pinned Roblox project tools may also be installed only after explicit approval:

```powershell
python scripts/team.py setup --developer YOU --runtime claude-code --install-tools
```

Matching Rojo Studio plugin installation is a separate consented option:

```powershell
python scripts/team.py setup --developer YOU --runtime claude-code --install-tools --install-plugin
```

To install the reviewed pinned BloxMaps fork into the ignored external-tool checkout after reviewing the doctor plan:

```powershell
python scripts/team.py setup --developer YOU --runtime YOUR_RUNTIME --install-bloxmaps
```

Then verify deterministic MapGen locally with `python scripts/bloxmaps_adapter.py smoke`. This does not count as live Studio proof. See `08_TOOLCHAIN/BLOXMAPS_SETUP.md`.

## First shared skill bootstrap

Maintainer only, and only when the prepared game's accepted external skill lock is absent:

```powershell
python scripts/team.py setup --developer MAINTAINER --runtime claude-code --initialize-shared-skills --confirm-shared-change
```

The underlying `scripts/initialize_project.py` remains the advanced/compatibility implementation for skill supply-chain auditing, runtime evidence recording and historical full-bootstrap workflows. Ordinary feature work should not call it directly unless the task specifically concerns bootstrap/runtime infrastructure.

## Portability architecture references

The canonical cross-runtime design remains in:

- `08_TOOLCHAIN/PORTABILITY_ARCHITECTURE.md`
- `08_TOOLCHAIN/CAPABILITY_CONTRACT.json`
- `08_TOOLCHAIN/RUNTIME_PROFILES.json`
- `08_TOOLCHAIN/ROLE_CONTRACTS/`
- `08_TOOLCHAIN/TEAM_MODEL_POLICY.json`

## What setup does not authorize

Setup never implies approval to create remote work, push, merge, modify a shared Studio place or publish Roblox Production.
