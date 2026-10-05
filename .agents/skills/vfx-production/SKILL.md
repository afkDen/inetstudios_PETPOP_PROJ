---
name: vfx-production
description: Roblox VFX production for readable, performant particles/beams/trails/lights/UI-world feedback. Use for abilities, pickups, scares, hits, rewards, ambience and state transitions with mobile budgets and real Studio validation.
---

# VFX Production

Use with `roblox-vfx`, `game-feel`, the style bible and `performance-optimization` when available.

## Layer by function
- anticipation / telegraph
- action / impact
- directional motion
- residue / decay
- gameplay-state confirmation
- optional camera/UI response
- paired audio cue

Define color/value, silhouette, timing, spatial scale, emitter count, lifetime, rate/burst, texture provenance, light usage and LOD/mobile fallback. Effects must clarify gameplay before they decorate it. Preserve contrast against likely backgrounds and avoid obscuring targets or HUD.

Prefer a small reusable effect language over one-off emitters. Pool/reuse where justified. Limit transparency overdraw, long-lived particles, excessive lights and full-screen flashes. Validate in the exact Studio place from player camera on representative device/performance settings. Capture before/after and console/performance notes.
