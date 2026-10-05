# TEAM RELEASE CHECKLIST — v8.5

Use on accepted `main` by the authorized release owner. A feature merge is not a Production publish authorization.

- [ ] Target feature PRs are merged after required human review and CI.
- [ ] Each task has no unresolved DRAFT scope amendment; its merged effective scope revision and approval history are coherent.
- [ ] Each task's risk tier and required evidence were satisfied for the final scope revision; do not require CRITICAL paperwork for LIGHT work or silently waive CRITICAL gates.
- [ ] `GAME_DESIGN.md` and relevant technical docs match merged reality.
- [ ] Pinned native Rojo build passes on merged source.
- [ ] Required integration Studio/device/multiplayer/persistence/security tests are complete on the intended nonproduction target.
- [ ] Assets/licenses/Roblox IDs are approved where applicable.
- [ ] Shared Studio world changes have backup/owner/integration records and no conflicting writers.
- [ ] No `.local/`, credentials, generated runtime adapters or build outputs are tracked.
- [ ] Rollback/migration path is documented for risky changes.
- [ ] Release/version/tag allocation happens only now, from accepted main.
- [ ] Human release owner separately confirms the intended Production Universe/Place and publication action.

Never infer live Roblox correctness from CI alone and never publish Production automatically.
