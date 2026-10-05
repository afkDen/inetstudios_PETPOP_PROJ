# TOOLCHAIN MANIFEST — v8.4

## Canonical core

- Master instructions: `AGENTS.md`
- Human workflow: `scripts/team.py` + `TEAM_WORKFLOW.md`
- Canonical skills: `.agents/skills/`
- Skill provenance/trust: `08_TOOLCHAIN/SKILL_REGISTRY.json` + `SKILL_LOCK.json` after external resolution
- Roles: `08_TOOLCHAIN/ROLE_CONTRACTS/`
- Capabilities: `08_TOOLCHAIN/CAPABILITY_CONTRACT.json`
- Runtime profiles: `08_TOOLCHAIN/RUNTIME_PROFILES.json`
- Shared model restrictions: `08_TOOLCHAIN/TEAM_MODEL_POLICY.json`
- Risk/workflow profile: `08_TOOLCHAIN/WORKFLOW_PROFILE.json`

## Skill runtime

Project-authored and approved external skills share `.agents/skills/`. Runtime-specific mirrors are generated/disposable. Ordinary feature work never refreshes the external supply chain automatically.

## Roblox developer binaries

`rokit.toml` pins Rojo 7.7.0, StyLua 2.5.2 and Selene 0.31.0. `scripts/bootstrap_dev_tools.py --check` verifies local versions. `--install` runs already-installed Rokit only after explicit consent; `--install-plugin` separately consents to Rojo Studio plugin modification.

## Roblox Studio

Live operations route through `studio-operator`. v8 verifies the actual Studio/MCP/Rojo target when a task requires live delivery rather than forcing that session before idea capture. A Rojo build or MCP config file is not a connectivity/playtest proof.

## Optional/no-cost tools

Poly Haven and Openverse helpers are included. Roblox Open Cloud, Blender, glTF-Transform, FFmpeg and other local/remote capabilities are optional and task-dependent. Paid/credit generation APIs are not default dependencies.
- Engineering reasoning layer: `08_TOOLCHAIN/ENGINEERING_REASONING_V8_4.md`
- Bundled adaptation/license notices: `08_TOOLCHAIN/THIRD_PARTY_NOTICES.md`

