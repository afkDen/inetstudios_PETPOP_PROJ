# Migration: v7.2 proposal/promotion workflow -> v8 streamlined

v8 is designed primarily for **future games and cleanly planned cutovers**. Do not replace workflow infrastructure in the middle of an uncheckpointed feature.

## What changes

Normal new work becomes:

`Issue -> task branch -> AI design -> human scope approval -> implementation -> one draft PR -> human review -> merge`

The v7 proposal branch/PR and promotion branch/PR are not required for new v8 tasks. Existing v7 proposal, approval and changeset records remain valid and are still checked by the compatibility validators.

## Safe cutover for an existing game

1. Finish or checkpoint all active work. Do not switch away from a dirty branch.
2. Merge/close the currently active v7 proposal/promotion/feature PRs according to that repository's accepted rules.
3. Create an `infra/` migration branch from current `main`.
4. Apply/review the v8 workflow files, policy, CLI and validators as one infrastructure change.
5. Preserve existing `00_INPUT/PROPOSALS`, promoted raw inputs and historical `04_CHANGESETS`; do not rewrite their bytes or hashes.
6. Run the complete portable test/validator suite and the repository's native checks.
7. Merge the migration only through the authorized human/integration process.
8. Start the **next genuinely new Issue** with `python scripts/team.py idea` or `update`.

Do not convert old accepted records into fake v8 tasks merely for consistency. Historical v7 records are history; new v8 work uses `TASK.json` + `USER_REQUEST.txt`.

## Existing active v7 issue

If an issue already has a v7 feature branch/changeset, finish it with its current accepted workflow. A new AI conversation does not justify creating a duplicate v8 Issue or branch.

## Rollback

Because v8 workflow changes should arrive through a focused infrastructure PR, rollback is a normal reviewed Git revert of that infrastructure change. Never reset/force-push shared history to undo a workflow migration.
