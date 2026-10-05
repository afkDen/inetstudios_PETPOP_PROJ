# MCP Runtime Registration — v8.2

Installing an MCP server is not the same as making it available to the active coding runtime. The bootstrap therefore treats **CLI readiness**, **runtime registration**, and **live target verification** as separate gates.

For Blender authoring the pinned executable is `mcp-for-blender` from `mcp-for-blender==2.1.3`. Keep these defaults unless a human explicitly approves an exception:

```text
BLENDER_HOST=localhost
BLENDER_MCP_SAFE_MODE=1
DISABLE_TELEMETRY=true
```

The workstation doctor never edits a user's global Claude/Codex/IDE configuration automatically. Runtime configuration is personal machine state, can contain unrelated servers/secrets, and differs across clients. After the pinned CLI is actually installed, the doctor also writes `.local/BLENDER_MCP_RUNTIME_REGISTRATION.md` using the resolved **absolute executable path** on that workstation; prefer that local snippet for GUI-launched clients because they may not inherit the same PATH as the terminal. Static examples remain under `08_TOOLCHAIN/MCP_CONFIG_EXAMPLES/`. Register the server once, restart/reload the runtime if required, and then let the task-time capability probe verify that the Blender tools are actually exposed.

## Claude Code

The upstream MCP-for-Blender project documents command registration in the form:

```text
claude mcp add blender mcp-for-blender
```

If your Claude configuration supports per-server environment variables, add the three bootstrap defaults above to the `blender` server. Otherwise launch/configure the runtime with those variables set. Do not disable safe mode just to make an operation easier; use the human decision gate if a required Blender operation is blocked.

## Codex

The upstream project documents:

```text
codex mcp add blender -- mcp-for-blender
```

A direct TOML example with the bootstrap defaults is provided in `08_TOOLCHAIN/MCP_CONFIG_EXAMPLES/codex-blender.toml`.

## Antigravity / JSON-style clients

Use the JSON example in `08_TOOLCHAIN/MCP_CONFIG_EXAMPLES/blender-mcp.json`, adapting only the surrounding client-specific location/shape when necessary. Keep the command and safety defaults intact.

## Verification

Registration is not considered proven because a config file exists. At task time the Lead/content worker must probe the active runtime, verify the expected Blender MCP tool group is visible, verify the exact `.blend`/scene/collection ownership, and then perform a reversible inspection before mutation.

For installation/addon details, see `08_TOOLCHAIN/BLENDER_MCP_SETUP.md`.
