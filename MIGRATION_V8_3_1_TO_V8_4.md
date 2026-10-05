# Migration — v8.3.1 BloxMaps Hardened → v8.4 Engineering Reasoning Integrated

v8.4 is intentionally compatible with the existing `streamlined-v8.3` task packet schema. No existing task must be rewritten. The release changes reasoning capability/routing, not task topology.

## Changes
- Eight new bundled project adaptations derived from the pinned `mattpocock/skills` snapshot.
- `systematic-debugging` becomes a bundled Roblox/budget-aware project adaptation and is removed from the required external-skill installer.
- Root `GLOSSARY.md` becomes the optional canonical game/domain vocabulary surface.
- `TASK.md` adds a decision record section for decision frontier, external knowledge blockers, and research pointers.
- Fresh assurance explicitly separates scope/spec fidelity from engineering/project standards.
- TDD and Matt's ticket/spec/implementation orchestration are explicitly excluded.

Existing v8.3/v8.3.1 tasks remain readable and approvable.

## Existing external-skill locks

An already-initialized v8.3.1 game may have `systematic-debugging` recorded in `08_TOOLCHAIN/SKILL_LOCK.json` as an external skill. v8.4 replaces that copy with the bundled reviewed adaptation and expects 37 external skills instead of 38. After applying the v8.4 bootstrap changes, the integration owner should run the normal maintainer initialization/explicit external-skill refresh so the lock and static audits are regenerated for the 37-skill external set, then perform the existing semantic-review/finalization gate before committing the refreshed lock. Do not hand-edit hashes to make the old lock appear current.
