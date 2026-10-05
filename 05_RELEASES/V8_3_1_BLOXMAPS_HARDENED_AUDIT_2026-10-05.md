# v8.3.1 BloxMaps Hardened — Final Audit

**Version:** `v8.3.1-bloxmaps-hardened`  
**Date:** 2026-10-05  
**Workflow compatibility:** existing `streamlined-v8.3` task packets remain supported; v8.3.1 adds hardening fields/validation without replacing the one-Issue/one-branch/one-PR lifecycle.

## Executive result

This patch finalizes the v8.3 BloxMaps-integrated bootstrap after a second-pass architecture and cross-platform integrity review. The human workflow, 10-role architecture, three-subagent ceiling, provider-neutral model/tool routing, Studio evidence boundary, external-skill supply-chain controls, and isolated BloxMaps design are preserved. The changes below close concrete integrity and policy gaps rather than adding more ceremony.

## Cross-platform byte integrity

The historical Windows failure mode was CRLF/LF normalization changing exact bytes after SHA-256 values had been recorded. Existing protections already covered `USER_REQUEST.txt`, legacy raw-input paths, reviewed skill trees, and the runtime-adapter historical CRLF repair path.

v8.3 introduced byte-hashed task reference copies under `04_CHANGESETS/GH-.../REFERENCES/`, but that tree was not explicitly `-text`. v8.3.1 adds:

```text
04_CHANGESETS/**/REFERENCES/** -text
```

`validate_team.py` now treats removal of that rule as a contract failure. A regression test initializes a real Git repository with `core.autocrlf=true`, commits a CRLF reference, clones/checks it out, and verifies the SHA-256 and bytes are unchanged.

New tasks also carry the `v8.3.1-byte-provenance` integrity profile. Human scope approval records a provenance fingerprint over the request hash plus all file/URL reference metadata. This closes a second-order gap where an approved reference file and its `TASK.json` hash could otherwise be changed together while still satisfying a simple file-vs-metadata hash check. Older v8.3 tasks without this profile remain readable for migration compatibility.

## BloxMaps execution boundary

The BloxMaps adapter previously detected a dirty isolated checkout but did not include cleanliness in `mapgen_ready`. A locally modified `tools/mapgen.py` or `src/MapGen/init.luau` at the same pinned Git commit could therefore still execute.

v8.3.1 requires all of the following before MapGen execution:

- reviewed origin matches;
- HEAD exactly matches the pinned 40-character commit;
- checkout is clean (tracked/untracked non-ignored changes make readiness false);
- Python/Luau prerequisites are present;
- expected MapGen files exist.

`install --confirm` also refuses to call a dirty-but-correct checkout "already pinned correctly". Generated plan output is confined to `.local/bloxmaps/` or `04_CHANGESETS/`, preventing the agent-operated adapter from becoming an arbitrary filesystem write primitive.

## CI managed-change gating

`validate_feature_evidence.changed_src()` already treated these as game-visible managed changes:

- `src/`
- `07_ASSETS/APPROVED/`
- `default.project.json`

`validate_ci_task.py` had independently reimplemented a narrower detector that omitted approved assets. An asset-only feature PR could therefore avoid the normal delivery gate.

v8.3.1 removes that duplicate interpretation: CI calls the canonical managed-change detector. Asset-only PRs now require the same approved task/delivery path as source or Rojo mapping changes.

## Integration-owner boundary

The integration-owner list now protects hardening-sensitive v8.3 infrastructure that ordinary `feat/`, `fix/`, or `docs/` branches should not silently rewrite, including:

- `.gitattributes`;
- BloxMaps pin/setup/adapter files;
- orchestration/context/frontend/MCP capability policy files;
- prepared-game bootstrap logic;
- feature/Studio evidence validators and templates.

This aligns the actual PR ownership boundary with the stated rule that external pins, workflow validators, and evidence contracts are integration-level changes.

## Evidence and documentation consistency

The quality-evidence template now uses the canonical `feat/123-feature` branch form and the canonical `content-production-worker` role. The validator checks that quality-packet branches use `feat|fix|docs/<issue>-<slug>`, match the changeset issue, and match `TASK.json` when present.

Skill inventory counts are now derived from `SKILL_REGISTRY.json` by `sync_derived_docs.py`. Current state is **40 bundled + 38 reviewed external = 78 registered**. `--check` fails if the project-state documentation drifts again.

The retained 72 KB `MASTER_PROJECT_DIRECTIVE.md` is now explicitly labeled historical/non-authoritative so broad-context agents do not confuse its old Antigravity-only assumptions with the current `/AGENTS.md` contract.

## Validation performed

- Full reusable-bootstrap test suite: **190 tests PASS + 20 subtests PASS**.
- Python compileall for scripts/tests: **PASS**.
- Derived documentation check: **PASS**.
- Static Rojo ownership/layout guard: **PASS**.
- Shared model-policy structural validation: **PASS**.
- Disposable local pipeline simulation: **PASS**.
- Prepared-new-game binding into a separate fixture repository: **PASS**.
- Prepared fixture `validate_team.py`: **PASS**.
- Prepared fixture `validate_repo.py`: **PASS** (40 currently bundled canonical skills, 78 registered skills, 10 roles).
- Prepared fixture static Rojo guard and derived-doc check: **PASS**.
- BloxMaps status missing-checkout behavior: correctly reports **PENDING**, without network/install mutation.
- Live BloxMaps MapGen: **not claimed** (isolated checkout/Luau were not installed in this audit environment).
- Native Rojo build: **not claimed** (native pinned toolchain not installed in this audit environment).
- Live Roblox Studio MCP / Blender MCP: **not claimed** (no live Studio/Blender session in this audit environment).

## Final recommendation

Use `v8.3.1-bloxmaps-hardened` as the finalized reusable bootstrap baseline. Future development should favor a smaller number of canonical machine-readable contracts and shared validator functions over adding new agents or parallel policy representations. The next meaningful architectural work should reduce duplication further, not increase workflow ceremony.
