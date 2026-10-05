# Team/Rojo production-quality release audit — 2026-09-23

Scope: review the actual v3 ZIP and correct false dependency readiness, overly broad subagent instructions, missing skill execution evidence and weak gameplay/visual acceptance. Source project is a bootstrap with **no actual game code yet**. Nothing in this audit can validate an unrelated Roblox game previously generated on a teammate's computer.

## Source-derived baseline defects

1. `rokit.toml` pinned Rojo but `initialize_project.py`/local teammate onboarding did **not** install or version-check local CLI binaries; the Studio plugin was explicitly separate. CI could install Rokit/Rojo, but that did not mean a teammate had installed them.
2. Role contracts supplied a general implementation worker with ~15 required skills, increasing context noise without enforcing task-specific activation or measured results. No separated art director, dedicated UI production worker, independent in-game visual reviewer or independent gameplay reviewer existed.
3. Quality gates tested architecture/security/scaffold and loosely required assets/UI. They had no issue-local, structurally enforced playable-and-visual evidence packet. Blank art bible templates had no mandatory preproduction signoff; blockouts could be falsely reported as complete.
4. The CI Rojo native build checked assembly only. It did not run real Studio playtests, genuine Luau tests, screenshot inspection or actual UI interactions.

## Implemented corrective controls

- Added verified local tool onboarding: `bootstrap_dev_tools.py --check/--install/--install-plugin`. Existing Rokit must be installed deliberately by the human; it installs pinned Rojo/StyLua/Selene only on explicit `--install`. Studio plugin install separately requires explicit `--install-plugin` and subsequent real verification. FULL per-developer runtime gating includes `developer_toolchain` and rejects a false PASS if binaries/versions are missing; PLANNING_ONLY is not falsely blocked by developer tools.
- Four project-native skills (visual production, UI production, playable vertical slice, skill-use audit) under the sole canonical `.agents/skills/` root; role-specific prompts and 4 additional semantic agents (art director, UI implementer, independent visual and gameplay reviewers). Lead/implementation scopes made more deliberate; image.inspect added as a real visual-review capability requirement. Generic image generation no longer falsely required for free-asset worker.
- Mandatory pre-implementation quality brief/art direction, separate labeled blockout vs production stages, realistic no-cost asset sourcing and escalation if a required signature asset is unavailable. Significant UI requires approved interaction map, real binding/states, responsive on-device proof. Playable vertical slices require real Studio and console evidence. Human aesthetic signoff is a separate release gate, not a text-only AI self-review.
- `validate_feature_evidence.py` verifies issue-local receipt/output paths, functional logs, screenshot file structure/dimensions, live Studio evidence fields, no unresolved placeholders, role separation and human merge still pending. It allows documented NOT_APPLICABLE visuals/UI for backend-only work without allowing art-heavy features to waive visual review. This is an honesty/shape check; humans inspect actual proof.
- Feature PR CI and `team_workflow.py check --test` now require structurally valid evidence for committed source changes. Team members lacking Studio can request an explicitly INCOMPLETE draft PR after portable checks with user consent; CI keeps it red until real evidence, peer review and live testing arrive. The human-controlled merge flow is preserved.
- CI now checks pinned binary versions; formats/lints any actual Luau files (skipping an empty code tree rather than pretending Luau tests ran); the native Rojo build is separately reported. Exact model/tool/skill root and reproducible asset/UI/gameplay quality are defined in `08_TOOLCHAIN/PRODUCTION_MODEL_BENCHMARK.md` for future comparative trials.

## Verification performed locally on this release candidate

- Portable validators (repository, shared team, Rojo mapping, derived role/skill docs), Python compilation, complete Python unit suite including negative readiness/evidence cases, disposable scaffold lifecycle, CI YAML structural parsing, `git diff --check` and tracked-path secret scan.
- Direct local `bootstrap_dev_tools.py --check` intentionally reports missing Rojo/StyLua/Selene here because those binaries and Roblox Studio are not installed in this sandbox. It therefore correctly returns a nonzero exit status. We did not claim or fabricate native Rojo, native Luau or live Studio test results.
- Actual skill registry and role counts refer only to project-authored bundled skills + expected externally installed skills. The external skill lock remains an approved maintainer bootstrap prerequisite; no external skill installation was fabricated during release validation.

## Residual limitations and mandatory workstation/production gates

- On each teammate's real machine, install/review Rokit then explicitly run `bootstrap_dev_tools.py --install` and (if needed) `--install-plugin`. Verify Rojo 7.7.0, StyLua 2.5.2, Selene 0.31.0, matching plugin, accepted official Studio MCP and a disposable real `rojo build`/`serve`/playtest. GitHub Actions was **not executed in the live project repository** during this local review.
- The bootstrap contains only an empty `src/` tree. Consequently no native Luau gameplay-unit framework/test cases can be honestly reported as passing. Add a reviewed/pinned game test runner after the initial slice and run it in Studio; Python infrastructure unit tests do not substitute.
- The source-to-Studio mapping is still deliberately limited to the three script subtrees; non-Rojo terrain/world is separately owned by the team. Visual asset quality cannot be ensured by empty skill definitions or free API calls; a human-approved aesthetic and appropriate art-capable tools/assets are essential. A static validator cannot know whether a screenshot was genuinely captured in Studio or genuinely looks good.
- Current CI third-party GitHub Action tags are not full commit-SHA pinned; the owner should review/pin them before handling untrusted public PRs or introducing secrets. CI currently runs without credentials. Production publishing, GitHub repo import, actual team permissions and live Studio integration remain strictly human authorized.

Release criterion: this ZIP is a **reviewed, ready-to-initialize scaffold**, not proof that your live game is polished or the real team workstation is ready. No push or force-update to the supplied GitHub remote was performed.
