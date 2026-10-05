# v8.5 Scope Evolution — Final Audit

**Version:** `v8.5-scope-evolution`  
**Date:** 2026-10-05  
**Baseline:** v8.4 Engineering Reasoning Integrated

## Purpose

v8.5 corrects the overly rigid post-approval model. Initial human approval remains a meaningful authorization boundary, but it no longer means the feature can never evolve. Material changes after approval use explicit, revisioned scope amendments so prior valid approvals/work/evidence are preserved where appropriate and silent scope drift remains blocked.

The normal topology is unchanged: **one GitHub Issue → one task branch → one issue-local changeset → one draft PR → human merge/release**. The 10-role capability architecture, three-active-subagent ceiling, reasoning layer, no-global-TDD policy, Studio/Blender/BloxMaps boundaries, and human-only push/merge/Production authority remain intact.

## Scope model

- New tasks use task schema 4 / `streamlined-v8.5`.
- Initial approval creates **scope revision 1**.
- `TASK.md` becomes the immutable base approved scope.
- Material post-approval changes are DRAFT/APPROVED/WITHDRAWN files under `SCOPE_AMENDMENTS/`.
- DRAFT amendments do not replace the current approved scope. Unaffected work may continue; affected work pauses.
- APPROVED amendments advance the revision and preserve the complete approval history.
- WITHDRAWN amendments remain immutable audit records without advancing the revision.
- Direct edits to approved base scope remain invalid.
- The legacy full-reopen path remains only for base-task repair/migration, preserves history, and refuses to run while a DRAFT amendment exists.

## Additional hardening found during audit

### Amendment source provenance

Post-approval scope can depend on new source material. `team.py amend` therefore supports repeatable `--reference` values. Local files are copied beneath `SCOPE_AMENDMENTS/REFERENCES/AMENDMENT-####/`, SHA-256 recorded, byte-preserved by `.gitattributes -text`, and included in finalized amendment provenance. URLs are recorded verbatim. Finalized reference metadata and bytes are tamper-checked.

A real Git regression test uses `core.autocrlf=true` and verifies CRLF amendment-reference bytes survive add → commit → clone → checkout exactly. This covers the same historical line-ending/SHA failure class as original task references.

### Evidence continuity without false invalidation

- Existing v8.3/v8.4 approved tasks lazily migrate to revision 1 when first amended.
- A metadata-only legacy upgrade carries existing compact evidence into revision 1 with an explicit migration attestation instead of needlessly making unchanged evidence stale.
- An approved amendment selects `refresh-affected` (default), `retain`, or `reset` evidence impact.
- `retain` requires a nonblank human note explaining why existing evidence remains applicable.
- `refresh-affected` preserves old evidence but blocks final delivery until `team.py evidence-scope` explicitly reviews/re-attests applicability.
- `reset` never rebinds old heavy evidence.
- Existing Studio/full-quality receipts can be rebound only by explicit `retain` approval or `evidence-scope`; this adds a `scope_rebind` audit record and never changes PASS/PENDING results or manufactures observations.

### Scope-aware heavy evidence

New `STUDIO_DELIVERY.json` and `QUALITY_EVIDENCE.json` templates are schema 2 and carry `scope_revision`. For v8.5 tasks their validators require that revision to match `TASK.json`. Legacy schema-1 receipts remain readable for legacy tasks.

### Risk/gate de-escalation

Post-approval risk/gate changes must go through the same approved amendment rather than a side channel. De-escalation is intentionally asymmetric:

- lowering CRITICAL risk requires a substantive scope change that removes the critical behavior plus a nonblank human approval note;
- turning previously-required gates off requires a nonblank approval note;
- CRITICAL tasks still force independent review/full-quality gates while they remain CRITICAL.

This allows legitimate scope reduction without making safety gates silently disappear.

### Review / agent instruction coherence

The assurance, release-readiness, process-inbox, team-orchestrator, codebase-design, Graphify, human-decision, and Lead instructions now treat effective scope as **base TASK.md + approved amendments**. Post-approval in-scope operational decisions belong in `WORK_STATE.md`; material scope/architecture/risk/gate changes belong in amendments. This avoids accidentally churning the immutable base fingerprint.

### PR/release coherence

Draft PR bodies now include active scope revision and approved-amendment count, ask reviewers to inspect effective scope rather than base TASK.md alone, and require no unresolved DRAFT amendment. The release checklist likewise checks the final merged scope revision/evidence.

## CLI additions / semantics

Normal human-facing commands now include:

- `team.py amend --issue N --reason ... [--reference ...]`
- `team.py approve --issue N --amendment A ...`
- `team.py withdraw-amendment --issue N --amendment A ...`
- `team.py evidence-scope --issue N ...`

`team.py gates` remains a pre-approval design command. Once initial scope is approved, risk/gate movement belongs to an amendment.

## Compatibility

- v8.3/v8.4 task packets remain readable.
- Existing approved legacy tasks are upgraded lazily only when revisioned scope is needed.
- Existing task/request/reference provenance is not rewritten.
- v7 proposal/promotion compatibility remains unchanged and non-default.
- v8.4 reasoning skills, 49 bundled + 37 reviewed external = 86 registered skills, 10 roles, and the three-subagent cap are unchanged.

## Validation performed

From the reusable source tree:

- pytest: **226 passed + 22 subtests passed**;
- unittest: **226 tests passed**;
- derived documentation: PASS;
- model-policy structural validation: PASS;
- static Rojo ownership/layout guard: PASS;
- Python compilation for modified workflow/validators: PASS.

A freshly prepared game repository from this bootstrap was initialized with a matching Git origin and committed, then passed:

- `validate_team.py`;
- `validate_repo.py` — reporting 49 canonical skills present, 86 registered skills, 10 roles;
- `validate_rojo_layout.py`;
- `validate_model_policy.py --check-config`;
- `disposable_pipeline_test.py`;
- `sync_derived_docs.py --check`.

The final packaging process also excludes generated runtime adapters, `.local`, caches, build outputs and Git metadata. The package manifest hashes every distributable file except the manifest itself; the ZIP checksum covers the manifest too. A clean extraction of the packaged ZIP passed ZIP CRC, every manifest hash, the full pytest suite, derived-doc/model-policy/Rojo static checks, and a **second fresh game preparation from the extracted archive** whose team/repository/model/Rojo/disposable-pipeline validators all passed.

## Boundaries not falsely claimed

This audit does **not** claim live Roblox Studio MCP/playtest, Blender MCP, Graphify runtime operation, BloxMaps MapGen execution, or a native Rojo binary build in the packaging environment. Those remain task-time evidence requirements when applicable.

## Final assessment

v8.5 makes approval **revisioned rather than brittle**. A human can deliberately move the requested product after approval without erasing valid prior decisions, while the workflow still prevents silent scope drift, stale evidence reuse, line-ending/hash provenance failures, and hidden risk/gate weakening.
