# Dependency Bootstrap — v8.2

The dependency layer is designed to fail early with actionable remediation instead of consuming agent turns debugging machine setup.

Run:

```powershell
python scripts/team.py doctor
```

The doctor is read-only by default and records:

- `CORE_READY` — Git, Python 3.10+ and exact project-pinned Rojo/StyLua/Selene;
- `GRAPH_READY` — published pinned Graphify CLI (`graphifyy==0.9.74`);
- `CREATIVE_CLI_READY` — Blender 4.2+, Python 3.10+ and pinned `mcp-for-blender==2.1.3`;
- Blender-addon live verification separately from CLI readiness;
- Roblox Studio live verification as just-in-time task readiness.

The local remediation plan is written to `.local/WORKSTATION_FIX_PLAN.txt`. When the pinned Blender MCP CLI is present, the doctor also writes `.local/BLENDER_MCP_RUNTIME_REGISTRATION.md` with the resolved absolute executable path so GUI-launched runtimes do not waste time on PATH/ENOENT troubleshooting.

With human approval and an already-installed `uv` (preferred) or `pipx`, plus Rokit:

```powershell
python scripts/team.py setup --developer YOU --runtime claude-code --install-recommended
```

This may run exact pinned isolated CLI installs (`graphifyy==0.9.74`, `mcp-for-blender==2.1.3`) and `rokit install`. It never bootstraps Python, Blender, Node, uv, pipx or Rokit themselves.

Addon mutation is separate:

```powershell
python scripts/team.py setup --developer YOU --runtime claude-code --install-recommended --install-blender-addon
```

After install, use localhost + Blender MCP safe mode by default. A task that needs a capability not currently ready should stop once with the doctor's specific fix plan rather than repeatedly attempting ad-hoc installations.
