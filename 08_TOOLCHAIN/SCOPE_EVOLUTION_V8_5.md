# Scope Evolution — v8.5

v8.5 keeps human approval meaningful **without pretending an approved feature can never evolve**.

## Core model

Initial design is approved as **scope revision 1**. `TASK.md` remains the immutable base scope after that approval. Material post-approval changes are written as ordered files under:

```text
04_CHANGESETS/GH-.../SCOPE_AMENDMENTS/AMENDMENT-0001.md
```

The effective scope is:

```text
approved TASK.md base
+ approved amendment 1
+ approved amendment 2
+ ...
```

Later approved amendment text supersedes conflicting earlier scope. A DRAFT amendment has **no authority** yet.

## Why amendments instead of reopening everything

A proposed change should not erase a valid prior approval. While an amendment is DRAFT:

- the current approved scope revision remains active;
- unaffected implementation may continue;
- work directly affected by the proposed change pauses;
- the amendment may be edited freely;
- final delivery is blocked until the amendment is either approved or explicitly withdrawn.

When approved, the amendment receives an immutable fingerprint and the task advances by one scope revision. Prior approval records stay in `TASK.json.scope_history`.

## Public commands

Draft a material change after initial approval:

```powershell
python scripts/team.py amend --issue N --reason "Add ranked matchmaking" --by YOU
```

If the revised scope depends on new source material, attach it to the amendment rather than altering original intake provenance:

```powershell
python scripts/team.py amend --issue N --reason "Adopt revised HUD brief" --by YOU `
  --reference .local/ideas/revised-hud.md `
  --reference https://example.com/approved-reference
```

Local amendment references are byte-copied and SHA-256 bound under `SCOPE_AMENDMENTS/REFERENCES/AMENDMENT-####/`. Their bytes/metadata become part of the finalized amendment provenance. To replace a copied reference, withdraw/redraft the proposal rather than editing the provenance record.

Edit the generated amendment, including what is added/changed/removed, acceptance impact, architecture impact, existing-work impact and evidence impact.

Approve it:

```powershell
python scripts/team.py approve --issue N --amendment 1 --by YOU --note "Approved revised matchmaking slice"
```

Risk/gate changes that belong to the amendment are approved atomically:

```powershell
python scripts/team.py approve --issue N --amendment 1 --by YOU `
  --risk CRITICAL `
  --studio-required yes `
  --independent-review yes `
  --full-quality-packet yes
```

Withdraw a proposal without changing the active revision:

```powershell
python scripts/team.py withdraw-amendment --issue N --amendment 1 --by YOU --note "No longer wanted"
```

## What requires an amendment

Use an amendment for a material change to any of these after approval:

- requested player behavior or acceptance criteria;
- meaningful feature addition/removal/deferment;
- architecture or authority model;
- persistence, networking, security, economy or monetization behavior;
- material art/UX direction that changes the accepted product;
- risk tier or delivery/review gates.

Do **not** create an amendment for ordinary reversible implementation choices already inside the approved behavior. Record those in `WORK_STATE.md`.

## Evidence continuity

Approval history and implementation evidence are separate concerns. An amendment chooses one evidence-impact mode:

- `refresh-affected` (default): preserve existing evidence, but mark it stale for final delivery until the affected evidence is reviewed/refreshed;
- `retain`: the human explicitly approves the amendment while affirming existing evidence remains applicable;
- `reset`: reset task-level evidence when the change invalidates the prior verification basis.

For the default mode, after the implementation/review work has made the evidence applicable to the new scope revision, record that explicitly:

```powershell
python scripts/team.py evidence-scope --issue N --by REVIEWER --note "Re-ran affected Studio scenario and reviewed unchanged backend evidence"
```

This command only attests scope applicability. It does not manufacture PASS results, screenshots, reviewer separation, or Studio evidence. If existing `STUDIO_DELIVERY.json` / `QUALITY_EVIDENCE.json` receipts are present, the explicit attestation rebinds their `scope_revision` with a `scope_rebind` audit record; it does not change their PASS/PENDING status or other evidence fields. The same controlled rebind happens for `--evidence-impact retain`. `reset` never rebinds old receipts.

## Integrity rules

- Direct edits to the approved base `TASK.md` remain blocked.
- Approved and withdrawn amendment files become immutable decision records.
- DRAFT amendment files may change until a decision is recorded.
- Unregistered amendment files fail validation.
- Amendment files are `-text` in `.gitattributes` to avoid cross-platform CRLF/LF surprises.
- Final delivery cannot proceed with an unresolved DRAFT amendment.
- Final delivery evidence must explicitly target the active scope revision; v8.5 Studio and full-quality receipts also carry that revision.
- Risk/review gates cannot be silently weakened. Lowering a CRITICAL risk classification requires a substantive scope change that removes the critical behavior plus a human approval note. Other gate de-escalations also require an explanatory approval note.
- `retain` evidence impact requires a human note explaining why prior evidence remains valid.

## Legacy full reopen

`scripts/streamlined_task.py` retains a legacy full-reopen helper for recovery/migration when the **base TASK.md itself** genuinely must be replaced. Normal v8.5 work should use revisioned amendments. A base reapproval increments the revision and preserves history; it never silently resets the task back to revision 1.
