---
name: implementation-package-builder
description: Builds deterministic implementation contracts for Roblox feature workers. Use before delegating Tier 2–4 implementation.
---

# Implementation Package Builder

Include only relevant sections, but make ownership deterministic:

- Goal
- Required Reading
- User-requested vs inferred scope
- Affected Feature IDs
- Existing Systems
- Expected Change Locations
- File/Instance Ownership
- Architecture Constraints
- Server/Client Ownership
- Networking Contract
- Persistence/Data Migration Impact
- UI Requirements
- Asset Requirements
- Ordered Tasks
- Security Requirements
- Performance Requirements
- Acceptance Tests
- Completion/Reporting Requirements

If live Studio/repository reality invalidates the package, the worker must stop only the affected step and return the mismatch to the Lead rather than improvising a broad migration.
