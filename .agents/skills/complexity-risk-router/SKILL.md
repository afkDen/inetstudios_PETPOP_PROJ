---
name: complexity-risk-router
description: Classify Roblox changes by technical/product risk and map them to v8 LIGHT, STANDARD or CRITICAL workflow gates, selecting only the planning, implementation, Studio and review work actually needed.
---
# Complexity / Risk Router

## LIGHT

Tiny wording/property/cosmetic fixes, narrow reversible tuning, small low-risk bug fixes. Compact checks/evidence. Independent AI review optional. Live Studio only when honest acceptance requires it.

## STANDARD

Normal gameplay, UI, content, enemy, quest, progression, ordinary system feature or substantial visual work. Require scoped design/impact analysis, relevant skills/roles, acceptance tests, native build, live Studio evidence when player-visible/Studio-dependent, and fresh independent review for substantial changes.

## CRITICAL

Trading/economy rewrite, purchases/monetization/RNG, DataStore/schema migration, exploit-sensitive networking/security, shared architecture migration, cross-place/release-critical systems. Require full quality packet, architecture/security/persistence/economy reviews as relevant, migration/rollback and explicit human gates.

Escalate when a lower-looking request touches irreversible player data, money, exploit-sensitive authority, or large migrations. Never silently downgrade to reduce paperwork.
