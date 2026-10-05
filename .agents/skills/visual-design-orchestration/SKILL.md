---
name: visual-design-orchestration
description: Provider-neutral visual-design workflow that binds to whichever real design/image/prototyping capability the active AI runtime exposes while preserving equivalent approval and evidence gates.
---
# Provider-Neutral Visual Design Orchestration

The project must not depend on a named vendor feature such as Claude Design. A named vendor feature is never required; `design.visual` is a **semantic capability**.

## Capability ladder
Use the strongest genuinely available option:
1. native visual-design workspace/canvas from the active runtime;
2. image generation/editing + image inspection;
3. interactive Roblox Studio/BloxUI or equivalent prototype;
4. structured wireframe/component spec plus screenshots/renders from the implementation environment.

A named tool is a runtime binding, not canonical workflow truth. Never claim a visual tool was used if unavailable.

## Required outputs for substantial visual work
- reference synthesis and anti-copy transformation notes;
- visual thesis + anti-goals;
- representative composition/mockup/prototype before broad rollout;
- tokens/component/state/responsive/input direction;
- human approval for material visual forks;
- implementation handoff tied to real Roblox constraints;
- actual Studio screenshots/playtest evidence after implementation where acceptance requires it.

If the runtime lacks rich visual tooling, continue with the best available equivalent rather than blocking solely because a specific vendor feature is missing. Escalate only when the requested outcome truly cannot be evidenced with the available capability.
