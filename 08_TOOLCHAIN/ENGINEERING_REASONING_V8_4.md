# Engineering Reasoning Layer — v8.4

v8.4 adds decision-quality and engineering-discipline skills without changing the one-Issue / one-branch / one-PR workflow, the 10 semantic roles, or the three-subagent ceiling. These skills are **capabilities**, not a second process framework.

## What is integrated

- `decision-grilling` — dependency-aware material decision frontier; Lead-controlled and risk-proportional.
- `external-questionnaire` — extracts missing knowledge from the person who actually owns it.
- `domain-modeling` — stable game language and sparse durable decisions.
- `codebase-design` — deep modules, small interfaces, useful seams, locality/leverage.
- `agent-instruction-design` — context pointers, progressive disclosure, completion criteria and anti-drift documentation.
- `workflow-retrospective` — explicit post-failure/environment improvement, not an automatic tax on every task.
- `primary-source-research` — authoritative research notes without mandatory background agents.
- `assurance-two-axis` — separate scope/spec fidelity from engineering/project standards inside the existing assurance reviewer.
- `systematic-debugging` — bundled Roblox/budget-aware synthesis emphasizing the cheapest tight feedback loop.

## Explicit exclusions

The bootstrap does **not** import Matt Pocock's `tdd`, `to-spec`, `to-tickets`, `implement`, `implement-spec`, `triage`, `wayfinder`, `ask-matt`, `setup-matt-pocock-skills`, or their task-graph/integration-branch assumptions. **TDD is intentionally not part of the v8.4 default capability layer.** Existing task/evidence checks remain risk-proportional. New tests are written when they are the cheapest durable verification or the task requires them, not because a global TDD ritual demands them.

## Invocation economy

Do not load or run these skills merely because they exist.

- A single material decision → use the compact `human-decision-gates` format.
- Several dependent material decisions → Lead may use `decision-grilling`.
- Missing fact discoverable by tools/research → agent finds it.
- Missing knowledge owned by another person → `external-questionnaire`.
- Hard technical failure → `systematic-debugging`, starting with existing cheap signals.
- External factual uncertainty that affects a decision → `primary-source-research`.
- Architecture shape/seam problem → `codebase-design`.
- Review → one fresh `assurance-reviewer`, using `assurance-two-axis`; do not spawn two reviewers just for the axes.
- Retrospective → only after meaningful friction/failure or explicit request; record feature-task recommendations rather than silently editing protected bootstrap infrastructure.

## Authority

`AGENTS.md`, `TEAM_PROTOCOL.md`, `TEAM_WORKFLOW.md`, `TASK.*`, Git/Studio evidence, role contracts and integration-owner boundaries remain authoritative. Imported/adapted reasoning techniques cannot create new approval authority or bypass them.
