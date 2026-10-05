---
name: codebase-design
description: Design deep, testable Roblox/Luau modules with small interfaces and clean seams. Use when module shape, ownership, adapter boundaries, testability, or architectural locality is the real problem.
---

# Codebase Design — Roblox adaptation

Adapted from `mattpocock/skills` `codebase-design` at pinned commit `24fe0ef7737efae15c87225755e9f6f5965e4888` (MIT).

## Shared vocabulary
- **Module:** code with an interface and implementation; scale-agnostic.
- **Interface:** everything a caller must know: methods/types plus invariants, error modes, ordering, authority and performance expectations.
- **Seam:** a location where behavior can vary without editing the caller.
- **Adapter:** one concrete implementation that occupies a seam.
- **Depth:** useful behavior hidden behind a small interface.
- **Leverage:** capability callers gain per unit of interface they must learn.
- **Locality:** related knowledge/change/debugging concentrates instead of scattering through callers.

## Design rules
- Prefer deep modules over chains of `Manager`/`Service`/`Handler` pass-throughs.
- Apply the **deletion test**: if deleting an abstraction merely removes a file and exposes no concentrated complexity, it may be shallow.
- Server/client authority belongs in the interface contract when it affects correctness or security.
- Prefer dependencies passed across explicit seams over hidden global construction when that improves control/testing.
- Do not invent a seam for hypothetical variation. One adapter may be a local implementation detail; genuine variation or a real isolation boundary earns a seam.
- Tests/evidence should observe behavior at useful interfaces where practical, but do not create extra test infrastructure solely to satisfy this skill.

## Roblox examples of useful seams
Data persistence adapter; matchmaking/teleport boundary; server-authoritative combat module; inventory/economy transaction interface; input-to-action mapping; UI view-model boundary; world-generation plan adapter; Studio authoring bridge.

Use the architecture in the effective approved scope (base `TASK.md` plus approved scope amendments) as the default. If implementation reveals that the interface/seam must materially change, return to the Lead rather than silently widening architecture.
