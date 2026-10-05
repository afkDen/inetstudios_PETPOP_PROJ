# FREE / NO-COST API POLICY

Last reviewed: 2026-09-15

Default production automation must not depend on per-call paid APIs. A "free account" or trial credit is not considered a no-cost API.

## ADOPT

### Poly Haven Public API
- Cost: free for personal and commercial use.
- Auth: none.
- Assets: CC0.
- Live-API requirement: include a visible "Powered by Poly Haven" credit when building on the live API.
- Project use: texture/model/HDRI discovery and metadata; record provenance.
- Client: `scripts/polyhaven_search.py`.

### Openverse API
- Cost posture: currently usable without authentication for standard throttled access, but its terms reserve the right to introduce fees for commercial/heavy use; therefore it is discovery/reference only, never a hard production dependency.
- Auth: optional for higher limits.
- Project use: reference/discovery of openly licensed images/audio.
- Critical gates: re-check current API terms before material automation use, and independently verify the original source license before production use because Openverse warns its license metadata may be inaccurate.
- Client: `scripts/openverse_search.py`.

### Roblox Open Cloud
- Cost policy: first-party Roblox API; no third-party generation fee is part of this scaffold.
- Auth: API key/OAuth with scoped permissions.
- Project use: optional external automation for supported Roblox resources.
- Enable only when a concrete workflow needs it; key remains local.

## LOCAL / OPEN-SOURCE, NO PER-CALL FEE
- Blender + Python API — optional technical-art automation.
- Official Blender Lab MCP Server — optional local open-source bridge; no per-call fee, but executes LLM-generated Blender Python without guards, so use only under sandbox/reversibility policy.
- glTF-Transform CLI — GLB/glTF inspection/optimization.
- FFmpeg — audio/video conversion/analysis where installed.
- TRELLIS/local 3D generation — RESEARCH/OPTIONAL only; requires capable local GPU and license/dependency review before adoption.

## APPROVED FREE ASSET SOURCES WITHOUT REQUIRED API
- Kenney: CC0 assets.
- Quaternius: free commercial-use assets under the current Quaternius Asset License; no standalone redistribution.
- Roblox Creator Store/Toolbox: inspect every imported asset and its scripts/rights.

## REJECT FROM DEFAULT NO-COST PATH
- Meshy API: paid API credits / paid API access.
- Hyper3D Rodin API: credit-based and API access tied to paid tier.
- Freesound API: free API use is limited to non-commercial use unless separately licensed.
- Any provider whose "free" status is temporary trial credit or requires payment for commercial/API usage.

## DURABILITY RULE

Before relying on any network service in a production workflow, re-check its current pricing/terms and licensing. A provider becoming paid, trial-only, commercially restricted, or materially less reliable automatically removes it from the no-cost default path until the Lead reviews it again.
