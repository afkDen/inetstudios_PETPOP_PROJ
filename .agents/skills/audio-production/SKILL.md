---
name: audio-production
description: Roblox SFX/audio production and integration: event intent, layering, sourcing/provenance, trimming/looping, spatial behavior, loudness hierarchy, trigger logic and live Studio verification.
---

# Audio Production

Use with external `audio-design` and `roblox-audio` when installed.

For every sound event define: gameplay intent; source/provenance/license; one-shot/loop; layers; timing; pitch/variation policy; spatial vs non-spatial; rolloff/range; priority/ducking; trigger authority; cooldown/repetition control; mobile/performance implications.

Design an audio hierarchy so UI clicks, pickups, danger, abilities, ambience and reward moments do not compete at equal loudness. Favor variation and restrained layering over constant noise. Avoid copyrighted/unlicensed material and do not assume a discovered sound can be shipped until its license/Roblox asset permissions are verified.

Test actual triggers in Studio, including repeated/overlapping events, distance behavior, respawn/reset, mute/settings and failure states. If no audio authoring/source tool is available, produce the asset brief and integration contract; do not fabricate generated files.
