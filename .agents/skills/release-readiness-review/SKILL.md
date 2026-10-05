---
name: release-readiness-review
description: Performs final independent readiness review before merge/tag/release. Use for substantial changesets and all release candidates.
---

# Release Readiness Review

Verify:
- current approved scope revision complete, with no DRAFT scope amendment still open;
- all required reviews closed;
- acceptance/regression tests pass;
- exploit-sensitive paths validated;
- persistence/migrations safe;
- performance/device/multiplayer checks complete where relevant;
- docs, TASK.json scope history, approved amendment overlays and state match reality;
- asset provenance complete;
- temporary debug artifacts removed;
- rollback path known;
- Git diff reviewed and unrelated changes absent;
- version/tag plan correct.

Return one outcome with evidence:
APPROVED / APPROVED WITH FOLLOWUPS / REVISION REQUIRED / BLOCKED.

In team mode, verify another human has reviewed substantial PRs and the integration owner has updated canonical state on main. Personal branch tags are not official releases; CI/mocks are not live Roblox Studio evidence. Use `TEAM_RELEASE_CHECKLIST.md`.
