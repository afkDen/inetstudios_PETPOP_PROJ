# Manual workstation prerequisites

Run `python scripts/team.py doctor` first. It is read-only and writes a concrete fix plan under `.local/`.

The bootstrap may use an already-installed `uv` (preferred) or `pipx`, plus Rokit, only after explicit install flags. It does **not** silently install Python, Blender, Node, uv, pipx, Rokit, GUI applications, paid providers, or system packages.

Manual machine-level prerequisites when relevant:

- Python 3.10+;
- Git;
- Node/npx for first or explicit external-skill resolution;
- Rokit, which provisions the project-pinned Rojo/StyLua/Selene versions;
- `uv` (preferred) or `pipx` for isolated Graphify and MCP-for-Blender CLI tools;
- Blender 4.2+ for the bundled reference-driven game-asset workflow;
- Roblox Studio and the project-approved Studio MCP/Rojo setup when a task reaches live Studio validation.

For Blender authoring, the bootstrap defaults to `BLENDER_HOST=localhost`, `BLENDER_MCP_SAFE_MODE=1`, and `DISABLE_TELEMETRY=true`. Disabling safe mode, exposing the Blender socket remotely, or enabling paid/network asset-generation providers requires a human decision gate.
