---
name: interaction-motion
description: Roblox-adapted motion and microinteraction guidance inspired by Emil Kowalski's design/animation skills. Use for menu transitions, button feedback, cards, HUD state changes, reward reveals, responsive feedback and motion review.
---

# Interaction Motion — Roblox adaptation

Source inspiration: `emilkowalski/skills` (MIT). Adapt concepts to Roblox TweenService/springs/animation constraints; do not import web libraries.

## Motion rules
- Motion communicates cause, hierarchy or state; do not animate merely because an element exists.
- Entering content normally decelerates into place; exiting content can accelerate away. Avoid sluggish ease-in entrances.
- Prefer short interaction feedback over long cinematic UI tweens. Keep frequent controls faster than rare reward reveals.
- Preserve continuity: interruptible/reversible interactions should not snap through stale queued tweens.
- Animate transforms/opacity-like properties where practical; avoid expensive per-frame layout churn.
- Give controls tactile depth: small scale/depth compression, rim/highlight changes and immediate audio/haptic-like feedback where appropriate.
- Use stagger sparingly to express grouping, not to delay information.
- For gameplay HUD events, layer motion by importance: subtle counter response < state transition < danger < reward/ultimate moment.
- Respect reduced-motion/accessibility settings and avoid rapid flashing, excessive camera/UI shake or continuous idle motion.

## Deliverable
For substantial UI, define a motion table: trigger, element, start/end state, duration range, easing/spring intent, interruptibility, sound/VFX pairing, reduced-motion alternative and performance note. Review the implemented result from real Studio capture rather than code alone.
