---
name: roblox-frontend-systems
description: Roblox-native GUI/HUD implementation and UX systems skill covering GuiObject primitives, responsive layouts, touch/gamepad parity, states, safe areas, server trust boundaries, performance, and design-before-build without flattening the approved art direction.
---

# Roblox Frontend Systems

Use for HUDs, menus, collection/inventory screens, responsive GUI architecture, input/focus, UI state controllers, and visual-to-Roblox implementation mapping.

## Design before broad build

For non-trivial visual work, work from an approved UI/style brief or representative mockup. If a critical visual direction is unresolved, route the choice to the Lead/human rather than improvising an entire style during implementation.

## Roblox-native layout

- Use scale/offset deliberately: scalable outer composition, stable pixel/constraint rules for local controls.
- Use anchors, `UIListLayout` / `UIGridLayout`, `UIPadding`, `UIScale`, aspect/size/text constraints, 9-slice imagery, `UIStroke`, gradients, and `CanvasGroup` intentionally.
- Account for safe areas, topbar/device insets, phone landscape, tablet, 16:9/16:10 and ultrawide where relevant.
- Do not migrate the project's UI framework or architecture unprompted.

## Input and states

Cover mouse, keyboard, gamepad and touch as required. Prefer activation/focus patterns that work across devices. Design and implement relevant default, hover/focus, pressed, selected, disabled, loading, locked, empty, success, warning/error and unread states.

## Visual craft

This skill does **not** mandate flat/minimal web UI. Preserve the approved dimensional/illustrated game art direction: layered frames, textures, shadows, glow, irregular silhouettes, expressive iconography and motion are valid when systematic and performant. Combine with `impeccable-ui`, `design-taste`, `interaction-motion`, `roblox-ui-polish`, and `accessibility-game` as needed.

## Trust and performance

Client UI requests actions; the server remains authoritative for valuable currency, inventory, purchases, rewards and progression. Avoid per-frame expensive layout churn, excessive transparency/compositing, huge textures, and uncontrolled animation loops.

## Acceptance

Verify real game-state binding, responsive recomposition, focus/back behavior, text fit, safe areas, touch targets, loading/error states, no console errors, and live Studio screenshots/playtests where required.
