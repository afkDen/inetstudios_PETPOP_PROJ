# Researched art / UI source policy (2026-09-23)

**A skill is a procedure, not an asset generator.** This document separates immediately usable no-cost asset sources, already approved skills, and conditional integrations. Root `AGENTS.md` and `FREE_API_POLICY.md` prevail. Do not auto-install a new provider from this document.

| Source | Verified use | Default decision |
|---|---|---|
| [Kenney individual asset packs](https://kenney.nl/assets) and [UI Pack](https://kenney.nl/assets/ui-pack) | Individual UI/3D packs marked CC0; inspect each actual download/license. Coherent UI primitives and stylized game art. The separate Kenney all-in-one bundle is **paid**, not part of free bootstrap. | Approved per-asset sourcing, not an API |
| [Quaternius](https://quaternius.com/faq.html) | Low-poly 3D asset packs; current FAQ says CC0, including commercial modification. Check each selected pack before ingestion. | Approved per-pack sourcing |
| [Roblox Creator Store](https://create.roblox.com/docs/production/creator-store) | Game-native meshes, models, images and audio, with asset-specific permissions. Search/insert available through official Studio MCP; scan incoming scripts and record rights. | Approved with per-asset inspection |
| [Poly Haven](https://polyhaven.com/license) | CC0 models/materials/HDRIs. Often realistic/PBR, not automatically compatible with a stylized Roblox look. | Conditional art-direction fit |
| [Openverse](https://openverse.org/) | Discovery of openly licensed media with source-level license recheck; not a bespoke 3D model or polished game UI generator. | Reference/discovery |
| [nonlooped Roblox Suite](https://github.com/nonlooped/roblox-suite) | Source-grounded Roblox engineering skills already listed for approved install in EXTERNAL_SKILLS.json. | Keep; test actual installation/discovery |
| [game-dev agent skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) | Existing general game art, UI/UX and studio workflow skills. Broader than Roblox UI art direction. | Keep selectively; add three project-authored focused skills in `.agents/skills/` |
| [Anthropic frontend-design skill](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design) | Web front-end design guidance, **not** an engine-native Roblox UI framework; upstream license/redistribution requires separate approval. | Reference only; do not silently vendor |
| [Google Stitch design skills](https://github.com/google-labs-code/stitch-skills) | Web/app UI design via **Stitch MCP**, separate account/quota/terms, no direct Roblox ScreenGui generation. | Trial only after explicit approval and compatibility benchmark |

Do not promise outputs comparable to a proprietary all-in-one product simply by installing more markdown skills. A reference-driven art director, coherent asset packs, operational tool connections, repeated in-game visual inspection, specialist edits and human aesthetic approval are what close the gap. No paid/credit image/3D API is enabled. Optional local Blender may require extra hardware/time; Studio's `generate_mesh` availability/limits must be probed at runtime instead of presumed unlimited and free.

**Portfolio benchmark:** pick one small vertical slice containing a distinctive lobby corner, one asset family, one complete functional shop/inventory screen and a live Studio playtest. Capture approved targets, actual screenshots from the player's camera, input traces and revision count. Compare execution quality across runtimes on the same scope and quality brief. No marketing screenshots are licensed project assets without express permission.
