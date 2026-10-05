# Migration — v8.1 Capability Streamlined → v8.2 Capability Hardened

v8.2 keeps the same public one-Issue/one-branch/one-PR workflow. Migration changes agent/tool infrastructure, not existing task provenance.

## Main changes

- 14 canonical roles → 10.
- remove normal `repository-scout`; use Graphify-first discovery.
- merge functional/experience/risk/release reviewer agents into fresh multi-mode `assurance-reviewer`.
- hard cap: 3 active subagents; extra passes happen in sequential waves.
- Graphify `0.9.74` becomes the recommended local repository-intelligence capability.
- MCP for Blender `2.1.3` becomes priority infrastructure for Blender-suitable 3D asset work.
- add `roblox-frontend-systems`, `graphify-repo-intelligence`, and `blender-mcp-production` bundled skills.
- external skill sources are requested from reviewed immutable Git refs rather than floating repository heads.
- add read-only `team.py doctor` / `workstation_doctor.py` and explicit pinned install flags to reduce setup/debug churn.

## Existing projects

Do not rewrite existing Issues/changesets. Merge the infrastructure update on an `infra/` branch, run runtime-adapter sync, run the doctor, update Graphify after the merge, then continue feature branches normally. Old v8/v8.1 `TASK.json` remains accepted by the validator.
