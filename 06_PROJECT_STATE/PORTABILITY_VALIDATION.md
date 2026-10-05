# Portability / Master-Skill Architecture Validation — 2026-09-17

## Scope

Validated the runtime-neutral refactor in which root `AGENTS.md` is the master contract and `.agents/skills/` is the only canonical active skill root.

## Invariants

- one canonical instruction authority: `AGENTS.md`;
- one canonical skill authority: `.agents/skills/`;
- skill provenance/lock/audit metadata stays under `08_TOOLCHAIN/`;
- project state and runtime-validation state remain separate;
- canonical roles/model classes are provider-neutral;
- generated vendor/runtime adapters are disposable and ignored;
- historical provider-specific bootstrap records are explicitly archived/superseded;
- local secret values are neither committed nor inspected/logged by initialization;
- external skill approval is bound to exact whole-tree hashes plus static and semantic review.

## Conclusion

The repository has a durable vendor-neutral core and replaceable runtime/model bindings. Final release verification evidence is recorded in `05_RELEASES/FINALIZATION_AUDIT_2026-09-17.md`.
