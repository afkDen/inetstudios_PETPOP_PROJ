---
name: primary-source-research
description: Investigate a task question using authoritative primary sources and leave a concise cited research note. Use when repository/tool evidence is insufficient and external facts materially affect a decision or implementation.
---

# Primary-Source Research — workflow adaptation

Adapted from `mattpocock/skills` `research` at pinned commit `24fe0ef7737efae15c87225755e9f6f5965e4888` (MIT).

## Rules
1. Search primary sources first: official Roblox/API/tool documentation, source repositories at the relevant pinned ref, specifications, vendor docs, or first-party APIs.
2. Use secondary/community sources only to discover leads or when firsthand operational experience is specifically relevant; label uncertainty.
3. Follow important claims back to the source that owns the fact. Record source/version/date when freshness matters.
4. Prefer the cheapest sufficient research path. Do **not** spawn a background/subagent merely because research is needed; the Lead's three-subagent budget still applies.
5. Save durable task-specific findings under the active changeset, preferably `RESEARCH/<slug>.md`. A read-only/non-writing specialist returns the cited note to the Lead for persistence. After scope approval, prefer a `WORK_STATE.md` pointer unless the research changes the approved plan, in which case draft/approve a scope amendment rather than silently editing the approved base scope.
6. Research informs decisions; it does not silently change approved scope, external pins, dependencies, or policy.

Return a short answer first, then evidence/links, uncertainties, and what decision the research affects.
