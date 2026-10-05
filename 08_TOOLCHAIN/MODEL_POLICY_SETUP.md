# Team model policy — local operator instructions

Follow `AGENTS.md` and the shared machine-readable `TEAM_MODEL_POLICY.json`. No developer should change the canonical `roles.json` to select a provider model. Runtime adapter files are derived and ignored by Git.

1. **Claude Code teammate:** configure the main session with **Claude Opus 5.5** at **Medium**. Generate `.claude/agents` via `python scripts/sync_runtime_adapters.py --runtime claude-code`; the generated agents explicitly set `model: claude-opus-5-5`, FAST `effort: low` and other agents `effort: medium`. A high setting, alias substitution or inherited override violates the shared policy. Check Claude Code environment/model-allowlist precedence rather than trusting frontmatter alone.
2. **Codex teammate:** choose **GPT-6.1 Sol** at **Medium**. Generate `.codex/config.toml` and `.codex/agents/*.toml` with `python scripts/sync_runtime_adapters.py --runtime codex`. Normal workers and reviewers are Medium; FAST uses Low. For narrowly scoped DEEP or REVIEW_DEEP work only, request High explicitly with the issue-specific justification and confirm actual active settings. Project TOML can be overridden at runtime: inspect live threads.
3. **Antigravity teammate:** confirm that **Gemini 3.8 Flash** and Medium are selectable on your plan, or request human approval for a policy change if unavailable. Generate agents with `--runtime antigravity`; all use `model: inherit` because the native schema only supports `inherit`, `flash` or `pro` rather than a guaranteed exact ID. Test the model/effort seen by delegated agents. If Low for FAST is unavailable, document Medium fallback; do not pretend it ran Low. If native delegation cannot honor the restriction, use isolated portable role packets / FULL_EMULATED or remain PLANNING_ONLY.
4. **Other runtime:** a human documents an approved exact model and verified effort settings. Do not claim universal Low/Medium/High equivalence across vendors.

Create ignored preflight: `python scripts/create_model_preflight.py --runtime RUNTIME --developer GITHUB_NAME`. For first maintainer initialization omit `--developer`. Collect sanitized actual CLI/IDE traces showing the main model/effort and two *delegated* test workers (implementation-worker BALANCED; assurance-reviewer REVIEW_DEEP). Store them under `.local/` and edit only the ignored per-developer/runtime receipt under `.local/model_preflights/`, never the tracked template or team policy. Complete human verification only after observing real settings; then run `python scripts/validate_model_policy.py --runtime-key GITHUB_NAME::RUNTIME`.

Do not enable high effort automatically, silently substitute models on quota exhaustion, leak model provider tokens into logs, or treat an unverified local model receipt as proof of Studio connectivity. Each future feature still requires its own acceptance and real Studio evidence.

## Seal and validate actual evidence

The initializer prints the exact receipt path from `scripts/create_model_preflight.py`. Capture **real**, sanitized CLI/IDE observations as separate `.local/*.txt` files and fill their paths/model/effort in that JSON. To bind those files against later accidental edits, run:

```bash
python scripts/create_model_preflight.py --runtime claude-code --developer YOUR_GITHUB_NAME --seal
python scripts/validate_model_policy.py --runtime-key YOUR_GITHUB_NAME::claude-code
```

Do not mark `status: PASS` until a human has checked the **actual** main session and FAST/BALANCED delegated runs and completed the `human_verification` fields. The validator verifies local receipt consistency and hashes; it cannot authenticate your model provider or prove a transcript is genuine. One receipt per developer/runtime avoids overwriting previous local test records. `--force` archives an existing receipt under ignored `.local/model_preflights/history/` before replacing it.

## Codex — explicit High exception

Do not change the default Medium Codex agents. If an assigned `DEEP` / `REVIEW_DEEP` role genuinely needs High, obtain explicit human approval for a specific issue and create a **temporary, ignored issue-scoped** variant. Adapter regeneration preserves the variant; deactivate it after the issue closes:

```bash
python scripts/prepare_codex_high.py --role assurance-reviewer --issue GH-000123 \
  --justification "Adversarial review of a new trading trust boundary" --approved-by YOUR_GITHUB_NAME
# Preview only above; after human approval, repeat with --activate.
# Refresh Codex agent discovery, verify the actual selected GPT-6.1 Sol High,
# and remove after issue closure:
python scripts/prepare_codex_high.py --role assurance-reviewer --issue GH-000123 --deactivate
```

Generated variants are local and never committed. `--activate` records a *claim of operator approval*, not proof of GitHub authorization; a real human review remains required. Do not use this facility for `BALANCED`, `FAST`, or ordinary implementation. If you just need a one-off externally managed High context, use `render_role_packet.py --runtime codex --effort high --escalate --justification ...` instead and verify that runtime.

## Adapter integrity and generated-file boundaries

- Regeneration preserves personal/unmanaged agents and temporary issue-scoped Codex High variants; edited generated files are blocked instead of silently overwritten.
- Claude Studio operator inherits discovered MCP tools without an unsafe fixed allowlist but denies direct Edit/Write tools; the live operator must validate the actual MCP connection and permissions. This is best-effort tooling scope, not a security sandbox for terminal commands.
- Codex local agent files are generated first and the default `.codex/config.toml` only after ownership checks pass. Local customized config must be explicitly reconciled, never overwritten automatically.
- To validate shared static model policy without pretending to verify an account, run `python scripts/validate_model_policy.py --check-config`.
