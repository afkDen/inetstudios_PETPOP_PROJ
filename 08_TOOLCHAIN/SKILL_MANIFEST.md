# SKILL MANIFEST

Canonical inventory: `08_TOOLCHAIN/SKILL_REGISTRY.json`. Canonical storage: `.agents/skills/<name>/SKILL.md`.

## Storage rule
There is one active skill root. Project-native and external skills are not separated into different trees because that creates duplicate discovery and drift. Origin/license/trust are metadata in the registry.

## Installation rule
Project-native skills and project-authored external adaptations ship in the repository. Adaptations retain immutable upstream provenance/license metadata in the registry and notices; they are maintained as project code rather than silently refreshed from upstream. Required upstream skills are installed into the same canonical root during initialization via the pinned universal Agent Skills installer, then statically audited, whole-tree locked in `08_TOOLCHAIN/SKILL_LOCK.json`, and semantically reviewed.

## Runtime compatibility
Runtimes that natively consume `.agents/skills` use it directly. Runtimes that require another path receive a generated mirror/symlink/copy from `scripts/sync_runtime_adapters.py`; those mirrors are never authoritative.

## Update policy
Do not silently update third-party skills during normal game work. Drift is repaired from the exact committed reviewed state. Use `scripts/initialize_project.py --refresh-external-skills` only for a deliberate upstream refresh, then rerun audit + semantic supply-chain review, test, and commit separately.
