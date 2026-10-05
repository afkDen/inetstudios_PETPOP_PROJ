---
name: blender-technical-art
description: Blender technical-art workflow. Use when local Blender is available for topology cleanup, decimation, UV/material consolidation, pivot/scale correction, collision proxies, rig fixes, LODs, deterministic Python automation, or export validation.
---
# Blender technical art

Use Blender only when native Roblox construction/import cleanup needs it. Prefer deterministic `bpy` scripts for repeatable transformations.

Workflow: inspect source → save a reversible milestone → make one bounded change → validate multiple views/metrics → export → fresh-import validation → record transformation in asset provenance.

The official Blender Lab MCP server may be used when installed, but it can execute LLM-generated Python without guards. Treat it as high-trust local code execution: use a workspace without sensitive data, scope commands tightly, and never expose secrets.
