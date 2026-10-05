# Migration — v8.4 to v8.5 Scope Evolution

v8.5 changes approval semantics, not the one-Issue/one-branch/one-PR topology.

## Existing repositories

Replace bootstrap infrastructure through the normal reviewed integration process. Do not manually copy only `team.py`; the task schema, validators, templates, docs and tests move together.

## Existing in-flight tasks

v8.3/v8.4 task packets remain readable. If an already-approved legacy task needs a post-approval scope change, the first `team.py amend` lazily upgrades its task metadata to revisioned v8.5 scope while preserving the legacy approval hash in history. The task meaning is not changed by this metadata upgrade. Existing task-level evidence is migrated to revision 1 with a metadata-only migration attestation, so merely adopting the v8.5 metadata model does not make unchanged evidence stale.

After upgrade:

- the existing approval is revision 1;
- future changes use `SCOPE_AMENDMENTS/`;
- risk/gate changes after approval are made through an approved amendment;
- final evidence must be current for the active revision; newly created Studio/full-quality receipts use scope-aware schema 2 while schema-1 receipts remain readable for legacy tasks.

## New tasks

New task packets use `schema_version: 4`, `workflow: streamlined-v8.5`, and begin at scope revision 0 until initial approval. Initial approval creates revision 1.

## Removed normal behavior

The normal workflow no longer tells operators to invalidate the entire approval simply because scope needs to move. The old full-reopen helper remains only as a recovery/legacy escape hatch.
