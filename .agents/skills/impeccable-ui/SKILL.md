---
name: impeccable-ui
description: Roblox-adapted interface craft guidance inspired by Impeccable and Anthropic frontend-design. Use for shaping, critiquing, auditing and polishing HUDs/menus/components so they are distinctive, coherent and not generic template output.
---

# Impeccable UI — Roblox adaptation

Source inspiration: `pbakaus/impeccable` (Apache-2.0) and Anthropic `frontend-design` skill. This project-authored adaptation is not a verbatim vendor bundle and must be used with Roblox-native UI skills.

## Method
1. Ground the interface in the game's subject, audience, play context and approved art direction before touching components.
2. Define the hierarchy first: primary action/state, secondary information, ambient/decorative material. Remove equal-weight boxes.
3. Establish a small token system for type, spacing, color, stroke, depth, shape families and motion. Reuse it consistently.
4. Avoid AI-default tells unless deliberately justified: repeated rounded cards, same-radius nesting, generic gradient glows, arbitrary icon tiles, excessive centered composition, weak gray-on-color text, over-boxing and unmotivated purple/blue palettes.
5. Preserve game dimensionality: layered artwork, texture, irregular silhouettes, illustrated frames, shadows, glow and playful motion are valid when they serve the approved style. Do **not** flatten Roblox GUI to imitate a minimalist website.
6. Design complete states: default, hover/focus, pressed, selected, disabled, loading, empty, locked, success, warning/error, new/unread.
7. Stress-test long text, large numbers, missing images, low-resolution screens, phone safe areas, controller focus and high-action gameplay backgrounds.
8. Critique at normal gameplay viewing distance. Ask: can the player identify priority in under a second? Does the screen still look like this game with labels removed?
9. Before final approval, compare against references and anti-references, then do a dedicated polish pass for spacing, alignment, border consistency, icon family, visual tangencies and hierarchy.

Use `roblox-ui-polish`, `game-ui-ux`, `roblox-user-interfaces`, and `accessibility-game` for implementation specifics.
