---
name: roblox-ui-polish
description: Produce complete Roblox in-game UI from approved visual references, cohesive design tokens, real client/server state, touch/gamepad navigation and actual Studio screenshots. Use alongside ui-production for visual-heavy HUD, menus, shops and inventories; prevent static skeleton GUI acceptance.
---

# Reference-Driven Roblox UI

Read `02_TECHNICAL/PRODUCTION_QUALITY_CONTRACT.md` and the approved `QUALITY_BRIEF.md`. A visually polished external product is a reference for *quality/coverage*, not permission to copy its exact graphics, art or proprietary source. Collect licensed or project-authored reference screens; approve a **single cohesive in-game UI direction** with the human owner before final implementation.

Deliver a screen inventory and an actual visual mockup at the target gameplay camera, including typography, spacing scale, icon family, corner radii, color/contrast and art direction. Supply normal, pressed, disabled, loading, empty, error and success states for controls. Prefer a consistently licensed project-approved icon/GUI asset family (for example, a verified CC0 Kenney UI pack), not randomly mixed visual kits. Any asset import must update provenance.

Implement via `src/client` under Rojo unless a reviewed mapping explicitly owns `StarterGui`. Bind each button to real stateful behavior. Specify each action's server validation and error handling; a fake balance or decorative button is a BLOCKOUT. Optional reactive UI frameworks require a version-pinned, separately reviewed dependency and an implementation benchmark; do not install a web-only design skill as though it outputs working Roblox ScreenGui instances.

On the exact Studio test place, test normal mouse, narrow phone viewport, touch and controller where supported, safe areas and clipping, dynamic data and failure states. Capture real screenshots and input traces using the Studio operator, compare them against the approved reference at normal playing distance, revise until a distinct read-only UI reviewer and human visual approver sign off. Record SKILL_USE_RECEIPT and quality evidence. If no image-inspection-capable reviewer is available, block visual approval.
