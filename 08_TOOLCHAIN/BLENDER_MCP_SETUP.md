# MCP for Blender — Priority Asset Authoring Setup

v8.2 treats **MCP for Blender** as the priority authoring bridge for Blender-suitable 3D assets. It is intentionally part of the standard creative workstation profile rather than an afterthought, while installation and live mutation remain human-gated.

Pinned reviewed source: `ahujasid/mcp-for-blender` at `60d2a31b4632a7bc178f3dd636f7e68dfb5c8ae4`; package `mcp-for-blender==2.1.3` (MIT).

The bootstrap requires Blender **4.2+** for the bundled game-asset workflow even though the MCP package itself supports older Blender versions. Python **3.10+** is sufficient. Prefer an already-installed `uv`; `pipx` is a supported fallback.

## Safe setup path

Run the read-only dependency report first:

```powershell
python scripts/workstation_doctor.py
```

Review `.local/WORKSTATION_FIX_PLAN.txt`. The bootstrap never silently installs Python, Blender, `uv`, `pipx`, Node, Rokit, paid providers, or system packages.

With explicit approval, install/repair exact pinned isolated CLI capabilities and Rokit-managed Roblox tools:

```powershell
python scripts/workstation_doctor.py --install-recommended
```

To also install/update the Blender addon explicitly:

```powershell
python scripts/workstation_doctor.py --install-recommended --install-blender-addon
```

Then register the server with your active coding runtime using `08_TOOLCHAIN/MCP_RUNTIME_SETUP.md`. After a successful doctor probe, prefer the generated `.local/BLENDER_MCP_RUNTIME_REGISTRATION.md` snippet because it contains this workstation's resolved absolute executable path and avoids common GUI-client PATH mismatches. Enable **Interface: MCP for Blender** if needed, and verify the local addon/server connection. Installation, runtime registration, and a live target handshake are intentionally separate checks.

## Bootstrap runtime defaults

Use these defaults in the MCP client configuration unless a reviewed task requires otherwise:

```text
BLENDER_HOST=localhost
BLENDER_MCP_SAFE_MODE=1
DISABLE_TELEMETRY=true
```

Safe mode is the default bootstrap posture because the bridge can execute Python inside Blender. Normal modeling, materials, rendering, saving, import and export are expected to remain available. If a task genuinely requires disabling safe mode, network access, installing persistent Blender code, or enabling a paid/external generation provider, stop and use the human decision gate first.

Keep the Blender socket on localhost. Run only one writer for the same `.blend` scene/collection area at a time.

## Live authoring handshake

Before mutation verify:

- exact `.blend` file and scene;
- owned collection/object prefix;
- source references and provenance/licensing;
- export directory and format;
- target Roblox scale, axes, pivot and collision plan;
- polygon/material/texture budgets;
- rig/animation requirements;
- current backup/checkpoint and one-writer ownership.

Use `.agents/skills/blender-mcp-production/SKILL.md` for the live-authoring gates and `blender-game-asset` for reference-driven modeling and round-trip acceptance. The expected pipeline is brief → calibration → blockout/silhouette → forms → topology/UV/materials → rig/animation only when required → deterministic export manifest → clean reimport → Roblox Studio acceptance.
