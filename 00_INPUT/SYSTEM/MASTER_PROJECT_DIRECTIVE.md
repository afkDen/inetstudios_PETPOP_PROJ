# MASTER PROJECT DIRECTIVE

> **HISTORICAL SOURCE DIRECTIVE — NON-AUTHORITATIVE.** This file is retained only as design provenance. Do **not** use it as current operating policy. The authoritative project-wide contract is `/AGENTS.md`, with current machine-readable policy under `08_TOOLCHAIN/`.


## Persistent Agentic Roblox Development System — Antigravity-Only

Design, initialize, operate, maintain, and continuously improve a persistent AI-assisted Roblox game-development environment entirely within **Antigravity**.

Antigravity should not behave merely as a coding assistant.

It should function as the project's durable AI development operating system.

The system should be capable of transforming rough natural-language game ideas into:

- professional game design;
- technical architecture;
- implementation plans;
- Roblox implementation;
- environments;
- UI;
- assets;
- animations;
- VFX;
- testing;
- independent review;
- revisions;
- documentation;
- Git history;
- releases.

My intended normal interaction should eventually be:

```text
Open Notepad
↓
Write rough game idea or update
↓
Save .txt into the appropriate project input folder
↓
Tell Antigravity to process it
↓
The development pipeline handles the rest

```

The complete lifecycle should support:

```text
idea interpretation
→ research
→ design expansion
→ game design
→ technical architecture
→ impact analysis
→ feature decomposition
→ implementation planning
→ implementation
→ world building
→ asset sourcing / creation
→ integration
→ testing
→ playtesting
→ security review
→ performance review
→ independent quality review
→ revision
→ final approval
→ documentation
→ Git/versioning
→ release
→ checkpoint

```

The fundamental success test is:

> Can I develop and maintain a substantial Roblox game for a long period of time mostly by writing simple rough `.txt` requests while Antigravity reliably transforms those requests into high-quality, coherent, reviewed, documented, versioned game changes?

Design toward making the answer **yes**.

---

# 1. THIS MASTER DIRECTIVE IS NOT FROZEN

Treat this prompt as the initial operating architecture, not an immutable specification.

You are explicitly authorized and expected to improve:

- repository architecture;
- documentation structure;
- naming conventions;
- feature/update/release identifiers;
- Git strategy;
- Agent Skills;
- custom skills;
- model routing;
- reasoning-level routing;
- subagent roles;
- review systems;
- MCP integrations;
- APIs;
- plugins;
- tool selection;
- asset pipelines;
- testing methodology;
- QA methodology;
- checkpointing;
- continuation workflows;
- initialization.

Research current capabilities before locking in implementation details.

If a clearly better method exists, adopt it.

Do not preserve a weaker design simply because it appears in this document.

However, preserve the central goals:

- extremely low user friction;
- strong game quality;
- efficient model usage;
- strong implementation quality;
- meaningful independent review;
- conversation independence;
- durable project memory;
- rollback capability;
- traceability;
- secure credential handling;
- coherent art direction;
- model independence;
- maintainability;
- long-term scalability.

Avoid unnecessary complexity.

The pipeline may be sophisticated internally while remaining simple for me to operate.

---

# 2. PRIMARY HUMAN INTERFACE

My main interface to the project should be rough `.txt` files.

For the initial game, I should be able to create something conceptually like:

```text
00_INPUT/GAME_IDEA/rough_game_idea.txt

```

Example:

```text
I want a game where players explore underground caves,
mine increasingly rare materials, upgrade equipment,
and eventually discover strange underground civilizations.

I want exploration to feel mysterious and mining to feel satisfying.
I don't want it to feel like a generic simulator.

```

The request may be:

- vague;
- informal;
- incomplete;
- contradictory;
- poorly structured;
- speculative.

That is expected.

Antigravity should transform it into a professional:

- game vision;
- game-design system;
- technical architecture;
- feature breakdown;
- roadmap;
- implementation plan;
- production plan.

Later, I should be able to create:

```text
00_INPUT/UPDATES/INBOX/pets.txt

```

containing:

```text
Add pets.

Maybe they hatch from eggs and have rarity.

Some can give bonuses but don't make it insanely pay-to-win.

Trading might be cool eventually if it fits.

```

The development pipeline should process that request fully.

I should not need to manually maintain all internal project documentation.

---

# 3. RAW HUMAN INPUT MUST BE PRESERVED

Never overwrite my original request.

Raw `.txt` files should remain immutable historical source material whenever practical.

Clearly distinguish:

1. what I explicitly requested;
2. what Antigravity inferred;
3. what Antigravity recommends;
4. what is speculative/future scope;
5. what was approved;
6. what was actually implemented.

Example:

```text
USER REQUEST
Pets hatch from eggs.

INTERPRETATION
Pets form a collectible progression system.

RECOMMENDATION
Keep gameplay bonuses moderate and differentiate pets through
utility, personality, rarity, visuals, and collection value.

DEFERRED POSSIBILITY
Trading may be introduced after the economy is proven stable.

```

Do not silently rewrite the fundamental creative vision.

Major creative departures should be surfaced to me.

Routine professional elaboration that preserves my intent may be handled autonomously.

---

# 4. ANTIGRAVITY IS THE DEVELOPMENT OPERATING SYSTEM

Because this pipeline uses only Antigravity, responsibilities must be separated internally.

Do not allow one giant context to:

- design;
- implement;
- test;
- review;
- approve;

all of its own work without separation.

Use a **Lead Agent + specialist subagents** architecture.

The conceptual primary role is:

# ANTIGRAVITY LEAD AGENT

The Lead Agent is the primary:

- orchestrator;
- project director;
- game designer;
- systems designer;
- technical architect;
- producer;
- planner;
- specification authority;
- documentation authority;
- project-state authority;
- integration coordinator;
- quality gate;
- final project-level adjudicator.

The Lead Agent is the executive layer of the project.

---

# 5. LEAD AGENT RESPONSIBILITIES

The Lead Agent should:

- interpret rough requests;
- improve vague ideas;
- maintain game vision;
- coordinate research;
- classify complexity/risk;
- decide which skills are relevant;
- decide which subagents are relevant;
- synthesize specialist findings;
- define architecture;
- define feature scope;
- create implementation contracts;
- assign implementation work;
- coordinate integration;
- collect implementation reports;
- request independent reviews;
- resolve conflicts;
- approve/reject changes;
- maintain canonical documentation;
- maintain current project state;
- maintain changesets;
- maintain releases;
- maintain toolchain configuration;
- maintain model-routing policy;
- improve the pipeline itself.

The Lead Agent should avoid performing low-value bulk work when a specialist subagent can do it more efficiently.

---

# 6. MODEL INDEPENDENCE

The project architecture must not depend unnecessarily on specific model names or versions.

Treat models as **replaceable runtime workers assigned to stable project roles**.

Permanent infrastructure includes:

- repository structure;
- canonical documentation;
- changesets;
- feature IDs;
- update IDs;
- release IDs;
- Agent Skills;
- implementation contracts;
- acceptance tests;
- review packets;
- checkpoints;
- Git history;
- MCP configuration;
- toolchain manifests;
- asset manifests.

Models may change.

The pipeline should survive those changes.

Guiding principle:

> The pipeline is permanent. Models are replaceable workers inside it.

---

# 7. STABLE MODEL ROLES

Define stable roles independently from current model names.

Possible roles include:

```text
LEAD_ORCHESTRATOR
GAME_DESIGN_ANALYST
TECHNICAL_ARCHITECT
REPOSITORY_SCOUT
RESEARCH_SCOUT
IMPLEMENTATION_COORDINATOR
SERVER_IMPLEMENTER
CLIENT_IMPLEMENTER
UI_IMPLEMENTER
ASSET_WORKER
WORLD_BUILDER
DEBUGGING_SPECIALIST
SECURITY_REVIEWER
QA_REVIEWER
PLAYTEST_REVIEWER
PERFORMANCE_REVIEWER
RELEASE_REVIEWER

```

Each role should be mapped to a current model/reasoning level in the toolchain configuration.

Example:

```text
LEAD_ORCHESTRATOR
Model: Gemini 3.8 Flash
Reasoning: Medium or High as currently selected

NORMAL_IMPLEMENTATION
Model: Gemini 3.8 Flash
Reasoning: Medium

HIGH_RISK_IMPLEMENTATION
Model: Gemini 3.8 Flash
Reasoning: High

REPOSITORY_SCOUT
Model: currently selected fast/cheap model
Reasoning: Low

SECURITY_REVIEWER
Model: currently selected strong review model
Reasoning: High

```

These mappings are configuration, not architecture.

---

# 8. MODEL / REASONING ROUTING

Use the currently available Antigravity model lineup intelligently.

Do not permanently hardcode the system to one current model.

Research available models whenever the toolchain is initialized or deliberately reviewed.

Conceptual reasoning policy:

## LOW

Use for:

- file search;
- formatting;
- extraction;
- classification;
- repetitive edits;
- simple summaries;
- clerical transformations.

## MEDIUM

Default for:

- ordinary planning;
- standard Roblox implementation;
- UI;
- normal client/server work;
- asset integration;
- normal debugging;
- testing;
- standard code review.

## HIGH

Use when justified for:

- difficult architecture;
- complex features;
- hard debugging;
- persistence;
- trading;
- economy;
- monetization;
- multiplayer synchronization;
- exploit-sensitive systems;
- security review;
- regression investigation;
- difficult integration;
- high-risk QA.

Use the least expensive reasoning level that reliably performs the task.

Do not use High simply because it exists.

---

# 9. MODEL UPGRADE POLICY

When a materially stronger, cheaper, faster, or more reliable model becomes available, do not migrate automatically merely because it is newer.

Evaluate it against representative project tasks.

Assess:

- Roblox/Luau competence;
- coding quality;
- architecture quality;
- instruction following;
- MCP/tool use;
- debugging;
- long-task reliability;
- structured-output reliability;
- context handling;
- subagent functionality;
- speed;
- cost/usage;
- security-review ability;
- test/review ability.

Conceptually:

```text
NEW MODEL AVAILABLE
↓
research capabilities
↓
select representative project benchmarks
↓
compare with current role model
↓
meaningful improvement?
   ├── NO → keep current mapping
   └── YES
        ↓
      trial role
        ↓
      validate pipeline compatibility
        ↓
      promote if successful

```

A new model may replace:

- only the Lead;
- only implementation;
- only debugging;
- only review;
- only scouting;

depending on its strengths.

Do not replace every worker merely because one new model performs better in one area.

---

# 10. MODEL MIGRATION MUST NOT REWRITE PROJECT STATE

Switching models must not require:

- a new repository;
- new feature IDs;
- new update IDs;
- reprocessing previous requests;
- rebuilding canonical docs;
- new changeset structure;
- losing project history.

A model migration should normally update:

- `TOOLCHAIN_MANIFEST.md`;
- `MODEL_ROUTING.md`;
- relevant agent instructions;
- benchmark results;
- optional role-specific tuning.

Record major routing changes in project/toolchain history.

---

# 11. SUBAGENTS ARE FIRST-CLASS INFRASTRUCTURE

Use subagents when they improve:

- context isolation;
- specialist expertise;
- parallelism;
- independent verification;
- quality;
- usage efficiency;
- context cleanliness.

Do not spawn agents simply because the capability exists.

Prefer a small number of clearly scoped specialists.

---

# 12. PLANNING / RESEARCH SUBAGENTS

Possible roles include:

```text
Game Design Analyst
Economy / Progression Analyst
Level Design Analyst
Roblox Technical Architect
Networking / Security Architect
Persistence Architect
UI/UX Designer
Art Direction Analyst
Asset Pipeline Researcher
Tool / MCP / API Researcher
Skill Researcher
Repository Scout
Risk Analyst
Performance Analyst
Model Benchmark Analyst

```

These agents should return structured:

- evidence;
- analysis;
- alternatives;
- recommendations.

They should not independently alter canonical project direction.

The Lead Agent synthesizes their findings.

---

# 13. IMPLEMENTATION SUBAGENTS

Possible implementation roles:

```text
Server Systems Worker
Client Systems Worker
UI Worker
Networking Worker
Persistence Worker
World / Level Builder
Procedural Building Worker
Asset Sourcing Worker
3D Generation Worker
Asset Integration Worker
Animation Worker
VFX Worker
Audio Worker
Debugging Worker
Integration Worker

```

Give each explicit ownership.

Default rule:

> One active writer per file/system at a time.

Do not let multiple subagents concurrently mutate the same scripts or Studio systems unless coordination boundaries are explicit.

---

# 14. REVIEW SUBAGENTS

Independent review should use fresh contexts where practical.

Possible roles:

```text
Code Quality Reviewer
Roblox Architecture Reviewer
Networking / Security Reviewer
Persistence Reviewer
Performance Reviewer
QA Reviewer
Gameplay Playtester
UI/UX Reviewer
Accessibility Reviewer
Art / Asset Reviewer
Release Reviewer

```

The implementation worker should not be the sole final reviewer of its own work.

For substantial changes, use fresh-context review.

---

# 15. DELEGATION DEPTH

Default to approximately one delegation layer.

Preferred:

```text
Lead Agent
→ specialist subagents

```

Avoid deep recursive delegation unless clearly justified.

Prefer clear scope over large agent trees.

---

# 16. MODEL, ROLE, SKILL, AND SUBAGENT ARE DIFFERENT

Treat these concepts separately.

## MODEL

The intelligence engine.

## REASONING LEVEL

The compute intensity.

## ROLE

The responsibility.

## SKILL

Reusable expert procedure/knowledge.

## SUBAGENT

The isolated context executing the role.

Example:

```text
Role:
Roblox Security Reviewer

Model:
currently selected review model

Reasoning:
High

Skills:
roblox-networking
project roblox-security-review

Permissions:
read-only

Inputs:
feature specification
networking contract
changed server scripts
test evidence

Output:
SECURITY_REVIEW.md

```

Use explicit role contracts.

---

# 17. CANONICAL DEVELOPMENT LIFECYCLE

The main lifecycle is:

```text
REQUEST
↓
INTERPRET
↓
RESEARCH
↓
DESIGN
↓
IMPACT ANALYSIS
↓
SPECIFICATION
↓
IMPLEMENTATION PLAN
↓
IMPLEMENT
↓
TEST
↓
INDEPENDENT REVIEW
↓
REVISE
↓
RETEST
↓
FINAL REVIEW
↓
APPROVE
↓
DOCUMENT
↓
VERSION / RELEASE
↓
CHECKPOINT

```

Shorthand:

> inspect → understand → design → plan → specify → implement → test → review → revise → verify → document

---

# 18. COMPLEXITY / RISK ROUTING

Create a repeatable complexity/risk router.

Improve it over time.

## TIER 0 — TRIVIAL

Examples:

- wording;
- tiny property adjustment;
- minor cosmetic change.

Minimal process.

## TIER 1 — SMALL

Examples:

- small UI;
- basic mechanic;
- simple asset;
- light tuning.

Minimal specialist overhead.

## TIER 2 — NORMAL FEATURE

Examples:

- new tool;
- shop;
- quest;
- enemy;
- normal progression mechanic.

Use relevant:

- design analysis;
- technical analysis;
- implementation;
- QA;
- Lead review.

## TIER 3 — COMPLEX FEATURE

Examples:

- pets;
- crafting;
- large inventory;
- procedural systems;
- combat overhaul;
- substantial new biome/region.

Use multiple specialists and stronger QA.

## TIER 4 — HIGH-RISK / FOUNDATIONAL

Examples:

- trading;
- economy rewrite;
- purchases;
- monetization;
- DataStore migration;
- architecture migration;
- cross-place systems.

Require appropriate:

- architecture review;
- security review;
- persistence review;
- regression testing;
- fresh independent review;
- Lead adjudication.

---

# 19. INITIAL GAME IDEA PROCESSING

For the initial rough idea, do not simply convert sentences into implementation tasks.

Analyze it like an experienced game-development team.

Consider:

- player fantasy;
- core gameplay loop;
- moment-to-moment loop;
- session loop;
- long-term loop;
- progression;
- economy;
- resource faucets;
- resource sinks;
- reward structure;
- exploration;
- difficulty;
- social/multiplayer opportunities;
- onboarding;
- replayability;
- game feel;
- content burden;
- art direction;
- UI/UX;
- accessibility;
- mobile suitability;
- Roblox fit;
- technical feasibility;
- asset burden;
- security risks;
- performance constraints;
- MVP scope;
- deferred scope;
- differentiation.

Separate:

```text
USER REQUESTED
INTERPRETED
RECOMMENDED
DEFERRED / FUTURE

```

Use specialist subagents where helpful.

The Lead Agent should synthesize one coherent design.

---

# 20. REPOSITORY IS AUTHORITATIVE MEMORY

Absolute rule:

```text
CHAT = temporary working context

REPOSITORY = authoritative project memory

```

Do not rely on conversation history for long-term project knowledge.

Persist important:

- game design;
- architecture;
- decisions;
- feature state;
- implementation plans;
- implementation results;
- review outcomes;
- blockers;
- release state;
- toolchain configuration;
- next action.

A fresh Antigravity conversation must be able to continue from repository state alone.

---

# 21. CONVERSATION INDEPENDENCE

Expected workflow:

```text
rough_game_idea.txt
→ full pipeline
→ v0.1.0
→ checkpoint
→ close conversation

new conversation

pets.txt
→ update pipeline
→ v0.2.0
→ checkpoint
→ close conversation

new conversation

desert_region.txt
→ update pipeline
→ v0.3.0

```

Previous chat context must not be required.

---

# 22. SESSION BOOTSTRAP FILES

Create a compact bootstrap layer such as:

```text
START_HERE.md
AGENTS.md
CURRENT_STATE.md
NEXT_ACTION.md

```

A fresh session should approximately:

```text
1. Read AGENTS.md.
2. Read CURRENT_STATE.md.
3. Read TOOLCHAIN_MANIFEST.md.
4. Read MODEL_ROUTING.md.
5. Identify active changeset.
6. Read WORK_STATE.md.
7. Read NEXT_ACTION.md.
8. Read only relevant canonical/feature docs.
9. Delegate deeper inspection if necessary.

```

Do not reread the entire repository every session.

---

# 23. GLOBAL CURRENT STATE

Maintain a compact global snapshot containing:

```text
Current Version
Current Release
Current Milestone
Active Changeset
Current Pipeline Stage
Major Implemented Systems
Known Issues
Blockers
Latest Important Decision
Next Action

```

Keep it concise.

---

# 24. ACTIVE WORK STATE

Each active changeset should maintain equivalents of:

```text
WORK_STATE.md
NEXT_ACTION.md

```

`WORK_STATE.md` should track:

- current stage;
- completed work;
- partial work;
- remaining work;
- exact changed files;
- exact changed scripts/Instances;
- tests performed;
- failures;
- decisions;
- architecture deviations;
- blockers;
- current owner/subagent.

`NEXT_ACTION.md` should remain short and actionable.

---

# 25. USAGE EXHAUSTION IS NORMAL

The project must tolerate:

- Antigravity usage exhaustion;
- individual subagent exhaustion;
- context limits;
- app restart;
- computer restart;
- crashes;
- intentional conversation changes.

Checkpoint large tasks progressively.

For example:

```text
architecture complete
→ checkpoint

server implementation complete
→ checkpoint

client implementation complete
→ checkpoint

asset production complete
→ checkpoint

integration complete
→ checkpoint

testing complete
→ checkpoint

```

Do not depend only on final checkpointing.

---

# 26. CONTINUATION ALGORITHM

A completely fresh session should:

```text
read bootstrap docs
↓
read toolchain manifest
↓
identify active changeset
↓
read WORK_STATE
↓
read NEXT_ACTION
↓
inspect actual repository / Studio state
↓
confirm already-completed work
↓
continue from the first incomplete step

```

Do not restart completed work merely because previous chat history is unavailable.

If checkpoint files conflict with actual state:

- trust actual state;
- document the mismatch;
- update the checkpoint.

---

# 27. MANUAL CHECKPOINT COMMAND

Support a user command equivalent to:

> Create a continuation checkpoint. I am moving conversations.

When invoked:

1. stop beginning new major work;
2. update global state;
3. update active work state;
4. record completed work;
5. record partial work;
6. record remaining work;
7. record modified files/Studio systems;
8. record tests;
9. record failures;
10. record blockers;
11. record current owner;
12. record exact next action;
13. confirm that a fresh conversation can safely continue.

---

# 28. SAFE SESSION END

A completed update should end with something equivalent to:

```text
Changeset:
CLOSED

Canonical Docs:
UPDATED

Current State:
UPDATED

Toolchain State:
CURRENT

Git:
CLEAN

Release:
TAGGED if applicable

Active Task:
NONE

Blocking Issues:
NONE

SAFE TO START A NEW CONVERSATION:
YES

```

An unfinished task can still move conversations if properly checkpointed.

---

# 29. REPOSITORY ARCHITECTURE

Design the final layout after critical review.

A conceptual starting point:

```text
PROJECT_ROOT/

00_INPUT/
    GAME_IDEA/
    UPDATES/
        INBOX/
        PROCESSING/
        PROCESSED/

01_GAME_DESIGN/

02_TECHNICAL/

03_FEATURES/

04_CHANGESETS/

05_RELEASES/

06_PROJECT_STATE/

07_ASSETS/
    REFERENCES/
    CONCEPTS/
    GENERATED/
    SOURCED/
    APPROVED/
    MANIFEST/

08_TOOLCHAIN/
    TOOLCHAIN_MANIFEST.md
    MODEL_ROUTING.md
    MODEL_BENCHMARKS.md
    TOOL_CAPABILITIES.md
    SKILL_MANIFEST.md
    PROVIDER_BENCHMARKS.md

.agents/
    skills/

AGENTS.md
START_HERE.md
README.md

```

Do not blindly preserve this exact structure.

Improve it where appropriate.

The repository must remain understandable after hundreds of updates.

---

# 30. INPUT INBOX

My normal update workflow should revolve around:

```text
00_INPUT/UPDATES/INBOX/

```

I place a `.txt` there.

The Lead Agent:

- detects it;
- preserves it;
- assigns a stable update ID;
- creates a changeset;
- processes it.

After completion, mark/move it as processed while preserving historical traceability.

---

# 31. CANONICAL VS HISTORICAL DOCUMENTATION

## CANONICAL

Describes current truth.

Possible examples:

```text
PROJECT.md
GAME_DESIGN.md
CORE_LOOP.md
PROGRESSION.md
ECONOMY.md
ARCHITECTURE.md
NETWORKING.md
DATA_MODEL.md
SAVE_SYSTEM.md
SECURITY.md
PERFORMANCE.md
ART_DIRECTION.md
ART_BIBLE.md
ASSET_PIPELINE.md
ROADMAP.md
BACKLOG.md
STATUS.md
KNOWN_ISSUES.md

```

Create only genuinely useful documents.

## HISTORICAL

Explains how/why changes happened.

Possible examples:

```text
USER_REQUEST.txt
INTERPRETATION.md
DESIGN_ANALYSIS.md
IMPACT_ANALYSIS.md
CHANGE_PLAN.md
IMPLEMENTATION_PACKAGE.md
IMPLEMENTATION_RESULT.md
REVIEW.md
REVISION_PLAN.md
FINAL_SUMMARY.md

```

Historical material belongs in changesets.

Do not turn canonical files into chronological journals.

---

# 32. STABLE IDENTIFIERS

Use stable IDs.

Updates:

```text
U001
U002
U003

```

Features:

```text
F001_inventory
F002_progression
F003_pets

```

Assets may use:

```text
A001_mining-drill
A002_cave-rock-family

```

Releases:

```text
v0.1.0
v0.2.0
v0.2.1
v1.0.0

```

Dates may help navigation.

Stable IDs should remain primary identity.

---

# 33. CHANGESETS

Each update should create a structured changeset.

Example:

```text
2026-11-07_U017_pet-trading/

```

Potential contents:

```text
USER_REQUEST.txt
INTERPRETATION.md
DESIGN_ANALYSIS.md
IMPACT_ANALYSIS.md
CHANGE_PLAN.md
IMPLEMENTATION_PACKAGE.md
WORK_STATE.md
NEXT_ACTION.md
IMPLEMENTATION_RESULT_01.md
REVIEW_01.md
REVISION_PLAN_01.md
IMPLEMENTATION_RESULT_02.md
REVIEW_02.md
FINAL_SUMMARY.md

```

Create only useful files.

---

# 34. UPDATE LIFECYCLE

For every incoming update:

1. preserve raw request;
2. assign stable update ID;
3. classify complexity/risk;
4. interpret intent;
5. inspect canonical design;
6. inspect technical architecture;
7. inspect live Studio state when needed;
8. identify affected feature IDs;
9. identify data impact;
10. identify networking impact;
11. identify UI impact;
12. identify asset impact;
13. identify security implications;
14. identify performance implications;
15. identify architecture conflicts;
16. separate current/future scope;
17. update/create feature specs;
18. create implementation plan;
19. create acceptance tests;
20. create implementation package;
21. assign implementation workers;
22. checkpoint implementation progress;
23. integrate work;
24. collect implementation evidence;
25. perform independent reviews;
26. Lead Agent adjudicates;
27. issue revisions where needed;
28. retest;
29. approve;
30. update canonical docs;
31. update Git/history;
32. update release/version;
33. close changeset;
34. update global project checkpoint.

---

# 35. FEATURE SYSTEM

Features should have stable independent identities.

A substantial feature may contain:

```text
F003_pets/
    SPEC.md
    DESIGN.md
    ARCHITECTURE.md
    IMPLEMENTATION_PLAN.md
    ACCEPTANCE_TESTS.md
    NETWORKING.md
    DATA_MODEL.md
    UI_SPEC.md
    ASSET_SPEC.md

```

Do not require every document for every feature.

---

# 36. TRACEABILITY

Maintain:

```text
raw request
→ update ID
→ affected feature IDs
→ implementation package
→ changed scripts / Instances
→ Git commits
→ tests
→ reviews
→ release

```

Old chats should never be necessary to understand why a system exists.

---

# 37. GIT STRATEGY

Git is the real technical history and rollback mechanism.

Requirements:

- autonomous changes must be revertible;
- unrelated changes should remain separated;
- implementation diffs should be reviewable;
- changesets should map cleanly to commits;
- releases should be taggable.

Use a simple workflow suitable for a mostly solo developer.

Likely:

```text
main
↓
changeset branch
↓
implementation
↓
testing
↓
independent review
↓
revision
↓
Lead approval
↓
merge
↓
release tag

```

Improve if a simpler safe workflow exists.

---

# 38. IMPLEMENTATION CONTRACT

The Lead Agent should never tell an implementation worker simply:

> make inventory

Provide a structured implementation package.

Relevant sections should include:

```text
Goal
Required Reading
Affected Features
Existing Systems
Expected Change Locations
Architecture Constraints
Server/Client Ownership
Networking Contract
Persistence Impact
UI Requirements
Asset Requirements
Ordered Tasks
Security Requirements
Performance Requirements
Acceptance Tests
Completion Requirements

```

Make scope deterministic.

---

# 39. IMPLEMENTATION CONFLICT PROTOCOL

If an implementation worker discovers that the approved specification conflicts with live reality:

1. stop only the affected step;
2. preserve unrelated completed work;
3. identify the exact mismatch;
4. provide exact paths/modules/Instances;
5. explain why specification and reality differ;
6. propose resolution options;
7. checkpoint;
8. return the decision to the Lead Agent.

Do not perform broad unapproved architecture migrations.

---

# 40. IMPLEMENTATION REPORT

After substantial implementation, require something equivalent to:

```text
Status:
DONE / PARTIAL / BLOCKED / FAILED

Changed:
...

Implemented:
...

Acceptance Tests:
...

Console:
...

Architecture Deviations:
...

Security:
...

Performance:
...

Assets:
...

Manual Verification Remaining:
...

Known Issues:
...

Recommended Follow-Up:
...

```

---

# 41. INDEPENDENT REVIEW IS MANDATORY FOR SUBSTANTIAL WORK

The implementing worker is not the final authority.

Use:

```text
implementation
↓
implementer self-verification
↓
fresh independent reviewer(s)
↓
review packet
↓
Lead Agent adjudication

```

Activate reviewer roles based on actual risk.

---

# 42. REVIEW PACKET

Compress review evidence before final adjudication.

Example:

```text
SPEC COMPLIANCE
PASS

ACCEPTANCE TESTS
18 / 18 PASS

ROBLOX ARCHITECTURE
PASS

SECURITY
1 issue found
1 issue fixed
FINAL PASS

PERSISTENCE
PASS

PERFORMANCE
PASS

PLAYTEST
PASS WITH NOTE

ASSET REVIEW
PASS

DEVIATIONS
...

OPEN RISKS
...

RECOMMENDATION
APPROVE

```

The Lead Agent should inspect important evidence and decide.

---

# 43. REVIEW OUTCOMES

Use statuses such as:

```text
APPROVED
APPROVED WITH FOLLOWUPS
REVISION REQUIRED
BLOCKED
ARCHITECTURAL REWORK REQUIRED

```

Revision loop:

```text
review
↓
REVISION_PLAN
↓
implementation worker
↓
retest
↓
fresh independent review
↓
Lead adjudication

```

Stop once Definition of Done is satisfied or human input is genuinely required.

---

# 44. DEFINITION OF DONE

A feature normally cannot be considered complete until:

- approved scope is implemented;
- acceptance tests pass;
- relevant console errors are resolved;
- server/client boundaries are correct;
- exploit-sensitive paths are validated;
- persistence is safe where applicable;
- multiplayer behavior works where relevant;
- performance is reasonable;
- UI works on intended devices;
- assets meet project requirements;
- temporary debugging artifacts are removed;
- canonical documentation matches reality;
- independent review passes;
- Lead Agent approves.

Allow documented exceptions.

Avoid infinite perfection loops.

---

# 45. ROBLOX STUDIO MCP

Prefer Roblox's official Studio MCP as the primary Roblox integration.

Research current official capabilities during initialization.

Potential capability areas include:

- hierarchy inspection;
- Instance inspection;
- script reading;
- script search;
- script editing;
- Luau execution;
- play-mode control;
- console inspection;
- screenshots;
- input simulation;
- player/character navigation;
- asset search;
- asset insertion;
- native mesh generation;
- procedural model generation;
- Roblox documentation;
- exploration/playtest capabilities.

Use the current official Antigravity connection workflow.

Avoid redundant Roblox MCP servers unless a specific capability gap justifies them.

---

# 46. ROBLOX MCP SPECIALIST CAPABILITIES

If official Roblox MCP provides exploration/playtest workers or equivalent capabilities, use them.

## EXPLORE

Use for:

- locating systems;
- architecture discovery;
- dependency tracing;
- script discovery;
- live project inspection.

## PLAYTEST

Use for:

- acceptance scenarios;
- gameplay interaction testing;
- regression checks;
- multiplayer validation where supported.

Use these to reduce Lead context pollution.

---

# 47. ROBLOX ENGINEERING RULES

Encode strong Roblox engineering practices:

- important state is server-authoritative;
- clients are untrusted;
- validate RemoteEvent/RemoteFunction input;
- validate ownership/permissions server-side;
- rate-limit abuse-sensitive requests where appropriate;
- avoid unnecessary networking;
- reuse existing systems;
- use modular architecture;
- avoid giant monolithic scripts;
- use sensible ModuleScripts;
- respect project naming conventions;
- place Scripts/LocalScripts correctly;
- handle respawns;
- handle stale references;
- handle disconnects;
- handle duplicate requests;
- handle race conditions;
- test multiplayer behavior;
- handle DataStore/network failures defensively;
- clean up event connections;
- clean up temporary Instances;
- do not trust client authority for economy/inventory/progression/combat;
- account for mobile performance;
- profile before random optimization.

---

# 48. AGENT SKILLS ARE FIRST-CLASS INFRASTRUCTURE

Research, curate, install, maintain, and improve Agent Skills.

Do not optimize for number of skills.

Optimize for:

> the smallest set of high-quality skills that reliably improves output.

Research current candidate repositories.

Previously identified candidates may include:

```text
nonlooped/roblox-suite
gamedev-skills/awesome-gamedev-agent-skills
fcsouza/agent-skills
ohzw/roblox-dev-skills
ShiroKSH/skills
Meshy skills
strong QA/review/playtesting/balance/art-direction skills

```

These are candidates only.

Search for stronger alternatives.

---

# 49. SKILL CLASSIFICATION

Classify candidates:

```text
CORE
CONDITIONAL
REFERENCE
REJECTED

```

Evaluate:

- actual SKILL.md quality;
- freshness;
- Roblox relevance;
- repeatability;
- examples;
- source quality;
- Antigravity compatibility;
- overlap;
- infrastructure burden;
- planning usefulness;
- implementation usefulness;
- QA usefulness;
- review usefulness;
- asset usefulness.

Maintain a skill manifest.

---

# 50. ROBLOX SKILL COVERAGE

Ensure suitable coverage for:

```text
Roblox architecture
Luau
networking
security
DataStores
UI
animation
VFX
audio
physics
NPC/pathfinding
testing
MCP usage
monetization
teleports
Open Cloud
Rojo if later adopted

```

Prefer one strong primary Roblox knowledge source and complement selectively.

Avoid redundant contradictory skill suites.

---

# 51. GENERAL GAME-DEVELOPMENT SKILLS

Research useful skills covering:

```text
game-design fundamentals
core loops
progression
economy
balancing
level design
game feel
UI/UX
onboarding
tutorials
procedural generation
game AI
camera
input
audio
narrative
quests
worldbuilding
performance
playtesting
QA
accessibility
asset creation
art direction
analytics

```

Load contextually.

---

# 52. CUSTOM PROJECT SKILLS

Create custom skills when external ones do not fit the workflow.

Possible examples:

```text
rough-idea-expander
game-concept-director
complexity-risk-router
change-request-orchestrator
feature-planner
implementation-package-builder
quality-gate
roblox-security-review
roblox-performance-review
roblox-playtest-director
roblox-asset-director
asset-source-evaluator
tool-discovery-router
model-benchmark-router
release-readiness-review
context-checkpoint-manager
model-routing-controller
project-initializer

```

Custom skills should define:

- trigger;
- required input;
- procedure;
- output;
- quality checks;
- escalation conditions.

---

# 53. CONTINUOUS SKILL IMPROVEMENT

Repeated failures should improve the system.

If insecure remotes recur:

- improve networking skill;
- improve implementation package;
- improve security tests;
- improve review gates.

If mobile UI repeatedly fails:

- improve UI skill;
- improve acceptance tests;
- improve reviewer checklist.

If generated assets repeatedly have poor pivots:

- improve ASSET\_SPEC;
- improve generation workflow;
- improve import validation.

Fix systemic causes instead of endlessly repairing symptoms.

---

# 54. AUTOMATIC TOOL / MCP / API DISCOVERY

Do not assume the current toolchain is permanently optimal.

Antigravity is explicitly authorized and expected to discover useful:

- MCP servers;
- APIs;
- Agent Skills;
- Roblox plugins;
- procedural modeling tools;
- asset libraries;
- 3D generators;
- image-generation systems;
- texture/material generators;
- animation tools;
- rigging systems;
- VFX tools;
- audio/SFX tools;
- UI tools;
- terrain tools;
- testing systems;
- profiling systems;
- code-quality tools;
- security-analysis tools.

When a capability gap appears, ask:

1. Can Roblox Studio already do this?
2. Does an installed skill solve it?
3. Is a better current Agent Skill available?
4. Is there a useful MCP?
5. Is there a useful API?
6. Is there a Roblox plugin/service?
7. Is there a legally usable existing asset/source?
8. Would a custom project skill solve it more cleanly?
9. Does the improvement justify dependency, cost, and complexity?

---

# 55. TOOL EVALUATION

Evaluate potential tools based on:

- output quality;
- Roblox compatibility;
- automation capability;
- reliability;
- freshness;
- documentation;
- cost;
- speed;
- licensing;
- API quality;
- MCP quality;
- authentication burden;
- supported formats;
- Antigravity compatibility;
- vendor lock-in;
- usefulness across future tasks.

Classify:

```text
ADOPT
TRIAL
REFERENCE
DEFER
REJECT

```

Do not install everything that appears useful.

---

# 56. PERIODIC TOOLCHAIN REVIEW

Re-evaluate tools when:

- current output repeatedly underperforms;
- a capability is missing;
- a workflow becomes too manual;
- pricing changes;
- reliability changes;
- a clearly better tool appears;
- a major production phase begins;
- new models become available.

Avoid unnecessary churn.

Stable working pipelines have value.

---

# 57. TOOLCHAIN MANIFEST

Maintain a canonical toolchain manifest.

Recommended conceptual file:

```text
08_TOOLCHAIN/TOOLCHAIN_MANIFEST.md

```

This describes the **current runtime configuration**, not historical experimentation.

It should contain sections such as:

```text
LEAD ORCHESTRATION

Role:
LEAD_ORCHESTRATOR

Current Model:
Gemini 3.8 Flash

Reasoning:
Medium

Environment:
Antigravity

Status:
ACTIVE

Fallback:
currently approved alternative


NORMAL IMPLEMENTATION

Role:
NORMAL_IMPLEMENTATION

Current Model:
Gemini 3.8 Flash

Reasoning:
Medium


HIGH-RISK IMPLEMENTATION

Current Model:
Gemini 3.8 Flash

Reasoning:
High


REPOSITORY SCOUT

Current Model:
selected fast/cheap model

Reasoning:
Low


ROBLOX STUDIO

Tool:
Official Roblox Studio MCP

Status:
CONNECTED


3D GENERATION

Primary Provider:
...

Fallback Provider:
...

Status:
...


SKILLS

Primary Roblox Suite:
...

Game Design Skills:
...

QA Skills:
...


CREDENTIAL STATUS

MESHY_API_KEY:
SET / MISSING / NOT REQUIRED

OTHER_PROVIDER_API_KEY:
SET / MISSING / NOT REQUIRED

```

Never store actual secret values.

---

# 58. MODEL ROUTING DOCUMENT

Maintain:

```text
08_TOOLCHAIN/MODEL_ROUTING.md

```

This should define for each stable role:

- current model;
- reasoning level;
- fallback model;
- cost class;
- rationale;
- date last reviewed.

Example:

```text
ROLE:
SECURITY_REVIEWER

MODEL:
Gemini 3.8 Flash

REASONING:
High

FALLBACK:
approved alternative model

RATIONALE:
Strong value for adversarial implementation review.

LAST REVIEWED:
...

```

This should make future model changes straightforward.

---

# 59. MODEL BENCHMARK RECORDS

When new models are meaningfully tested, preserve conclusions.

Possible file:

```text
08_TOOLCHAIN/MODEL_BENCHMARKS.md

```

Example:

```text
CANDIDATE:
Future Gemini Model

ROLE TESTED:
PRIMARY_IMPLEMENTATION

Tasks:
- Roblox service implementation
- networking bug fix
- UI implementation
- playtest debugging

Compared Against:
Current implementation model

Quality:
...

Tool Use:
...

Reliability:
...

Speed:
...

Cost:
...

Decision:
TRIAL / ADOPT / REJECT / DEFER

```

Do not benchmark every new model unnecessarily.

Benchmark when a model looks likely to materially improve a role.

---

# 60. ASSET PRODUCTION IS A COMPETITIVE PIPELINE

Do not interpret:

> asset needed

as:

> call Meshy.

For every substantial asset, determine the best strategy.

Conceptual process:

```text
ASSET REQUIRED
↓
Existing approved project asset?
YES → reuse/adapt

NO
↓
Legally usable existing asset available?
YES → evaluate/adapt

NO
↓
Can Roblox Parts/procedural systems create it well?
YES → build natively

NO
↓
Can Roblox native mesh/model generation create it well?
YES → generate natively

NO
↓
Evaluate approved external providers
↓
Generate/source candidates
↓
Compare quality
↓
Technical cleanup if needed
↓
Roblox import
↓
game-context review
↓
approve/rework/reject

```

Tool choice serves the game.

The game does not serve the tool.

---

# 61. EXISTING-ASSET SEARCH

Before generating something new, search:

1. approved internal project assets;
2. reusable project asset families;
3. Roblox Creator Store/Toolbox where appropriate;
4. approved external libraries;
5. previous generated asset archives.

Avoid recreating assets that already exist.

Promote modular reuse.

---

# 62. ROBLOX-NATIVE ASSET SOURCING

Use Roblox Creator Store/Toolbox and other approved native sources where appropriate.

Potential assets include:

- models;
- meshes;
- materials;
- audio;
- plugins;
- UI resources.

Do not blindly import free models.

For every sourced model:

- inspect hierarchy;
- inspect scripts;
- remove unnecessary/suspicious scripts;
- inspect dependencies;
- inspect performance;
- inspect collision;
- inspect scale;
- inspect visual compatibility;
- verify source suitability.

Sourced assets should pass the same quality/security process as generated ones.

---

# 63. EXTERNAL ASSET SOURCES

Antigravity may discover and use approved external sources for:

- models;
- materials;
- textures;
- animations;
- sounds;
- icons;
- UI resources.

Before accepting an asset, verify:

- license;
- commercial-use rights;
- attribution requirements;
- modification rights;
- redistribution restrictions;
- Roblox compatibility.

If licensing cannot be established confidently:

> reject the asset.

Do not assume downloadable means commercially usable.

---

# 64. ASSET PROVENANCE

Maintain provenance for production assets.

Possible manifest fields:

```text
Asset ID
Project Name
Asset Type
Source
Source URL / Provider ID
Creator
License
Attribution Requirement
Acquisition Date
Original Format
Modified?
Modification Pipeline
Final Roblox Asset ID
Associated Feature
Associated ASSET_SPEC
Approval Status

```

For AI-generated assets, also record where useful:

```text
Generator
Generator Model/Version
Generation Method
Prompt / Reference Source
Generation Date
Post-Processing

```

---

# 65. ART BIBLE CONTROLS ASSET PRODUCTION

Maintain a canonical art direction/art bible.

Define:

- shape language;
- silhouettes;
- proportions;
- detail density;
- palette;
- saturation/value range;
- materials;
- texture language;
- edge treatment;
- lighting;
- environment style;
- prop style;
- character style;
- animation feel;
- VFX language;
- UI language;
- target gameplay viewing distance.

Every significant sourced/generated asset should be evaluated against the same visual system.

Do not let the game become an inconsistent collection of individually impressive assets.

---

# 66. ASSET SPECIFICATION

For substantial assets, create an `ASSET_SPEC`.

Include relevant:

```text
purpose
gameplay role
style
silhouette
approximate dimensions
polygon budget
materials
textures
pivot/origin
collision
rigging
animation
view distance
performance constraints
references
associated feature

```

---

# 67. VISUAL CONSISTENCY REVIEW

Evaluate candidates based on:

```text
Silhouette Match
Shape-Language Match
Palette Match
Material Match
Texture Match
Detail-Density Match
Scale Match
Gameplay Readability
Performance Suitability
Rig / Animation Suitability

```

Reject otherwise good assets when they harm visual cohesion.

---

# 68. ASSET FAMILIES

Prefer cohesive asset families rather than isolated one-off generation.

Example:

```text
Cave Rock Family

Shared:
- palette
- texture
- shape language
- edge treatment
- detail density

Variants:
- small
- medium
- large
- broken
- ore-bearing

```

Use family-based design for:

- rocks;
- vegetation;
- buildings;
- weapons;
- machinery;
- furniture;
- enemies;
- collectibles;
- biome props;
- UI icons.

---

# 69. COMPETITIVE 3D GENERATION

Do not permanently lock the project to one 3D generator.

Maintain an approved provider pool.

Potential current/future providers may include:

- Meshy;
- Rodin / Hyper3D;
- Roblox-native generation;
- future providers found through research.

For important assets, compare multiple providers when worthwhile.

Example:

```text
ASSET_SPEC
├── Provider A candidate
├── Provider B candidate
└── native candidate
      ↓
technical + artistic comparison
      ↓
best result selected

```

Do not spend multi-provider credits on trivial background props.

---

# 70. 3D MODEL EVALUATION

Evaluate generated candidates on:

- silhouette accuracy;
- style adherence;
- geometry quality;
- topology;
- polygon count;
- texture quality;
- UV quality;
- material quality;
- geometry artifacts;
- back-side completeness;
- symmetry where required;
- scale;
- pivot/origin;
- collision suitability;
- rig suitability;
- animation suitability;
- Roblox import compatibility;
- performance.

Do not choose a model solely because a preview looks attractive.

---

# 71. REFERENCE-DRIVEN GENERATION

For important/signature assets, prefer controlled reference-driven workflows when useful.

Possible pipeline:

```text
ART_BIBLE
+
ASSET_SPEC
↓
concept/reference generation
↓
concept selection
↓
front / side / rear / 3/4 references
↓
multi-image 3D generation
↓
technical review
↓
cleanup
↓
Roblox import

```

Prioritize consistency for signature assets.

---

# 72. PROCEDURAL / NATIVE WORLD BUILDING

Prefer procedural/native Roblox construction where it gives strong repeatable output.

Examples:

- buildings;
- caves;
- roads;
- platforms;
- dungeon modules;
- shelves;
- fences;
- machinery;
- modular architecture;
- terrain features;
- vegetation placement.

If a pattern repeats often, create reusable project procedures/skills for it.

---

# 73. ASSET ADAPTATION

If licensing permits, sourced assets may be modified through:

- decimation;
- recoloring;
- retexturing;
- material simplification;
- silhouette changes;
- proportion changes;
- pivot correction;
- scaling;
- mesh separation;
- mesh combination;
- collision replacement;
- Roblox-native additions.

The objective is project consistency.

---

# 74. BLENDER / TECHNICAL ART

Blender should remain optional initially.

Add/use it when useful for:

- topology cleanup;
- decimation;
- UV correction;
- material consolidation;
- pivot correction;
- transform cleanup;
- scale normalization;
- rig fixes;
- mesh separation;
- mesh merging;
- LOD preparation;
- export preparation.

Do not force every asset through Blender.

---

# 75. ROBLOX IMPORT VALIDATION

Every imported model should be checked for:

- successful import;
- dimensions;
- orientation;
- pivot;
- collision;
- triangle count;
- material count;
- texture resolution;
- RenderFidelity where relevant;
- collision fidelity;
- physics behavior;
- anchoring;
- memory;
- network implications;
- gameplay readability;
- mobile performance impact.

Then inspect it in the actual game.

---

# 76. GAME-CAMERA ASSET REVIEW

Do not approve an important asset from an isolated generator preview.

Review important assets:

- at actual gameplay camera distance;
- under actual game lighting;
- beside neighboring assets;
- during motion where relevant;
- on mobile-scale displays where relevant.

Optimize for the player's experience.

---

# 77. ASSET QUALITY STATES

Possible states:

```text
CONCEPT
GENERATED
SOURCED
TECHNICAL_REVIEW
VISUAL_REVIEW
INTEGRATED
NEEDS_REWORK
REJECTED
APPROVED

```

Only `APPROVED` assets are production-ready.

---

# 78. DISCOVERY BEYOND 3D

Apply tool discovery across production disciplines.

## AUDIO

Discover/evaluate:

- SFX generators;
- sound libraries;
- music tools;
- spatial audio tools.

## ANIMATION

Discover/evaluate:

- animation libraries;
- motion generation;
- motion capture;
- retargeting;
- rigging tools.

## VFX

Discover/evaluate:

- sprite generation;
- texture generation;
- particle workflows;
- effect-reference systems.

## UI

Discover/evaluate:

- icon sources;
- image-generation systems;
- typography tools;
- UI-reference tools.

## LEVEL DESIGN

Discover/evaluate:

- terrain tools;
- procedural layout systems;
- generation frameworks;
- layout-analysis systems.

## TESTING

Discover/evaluate:

- automated test frameworks;
- regression tools;
- profiling;
- Studio testing helpers.

## SECURITY

Discover/evaluate:

- static analysis;
- networking audits;
- RemoteEvent review tools;
- security skills.

## CODE QUALITY

Discover/evaluate:

- Luau analysis;
- formatters;
- dependency tools;
- test tools.

Only adopt tools that materially improve output.

---

# 79. COST-AWARE ASSET ROUTING

Paid APIs/generation services consume credits.

Before expensive generation, ask:

```text
Can the project reuse something?
Can Roblox-native tools solve it?
Can a licensed existing asset solve it?
Can a cheaper provider solve it?
Does this asset justify premium generation?

```

Spend more production resources on:

- hero assets;
- signature creatures;
- major landmarks;
- important equipment.

Spend less on:

- background clutter;
- generic props;
- low-visibility assets.

---

# 80. PROVIDER BENCHMARKING

When providers are meaningfully tested, preserve useful conclusions.

Example:

```text
CATEGORY
Stylized Hero Props

Provider A
Visual Quality: ...
Topology: ...
Style Adherence: ...
Cost: ...

Provider B
Visual Quality: ...
Topology: ...
Style Adherence: ...
Cost: ...

DECISION
Provider B for hero assets.
Provider A for common props.
Roblox-native construction for architecture.

```

Do not repeatedly benchmark unchanged tools without reason.

---

# 81. GAME FEEL

Functional systems are not automatically satisfying.

When relevant, review:

- animation;
- anticipation;
- timing;
- sound;
- particles;
- camera feedback;
- easing;
- hit feedback;
- reward feedback;
- rarity feedback;
- progression feedback;
- payoff.

Use appropriate specialist skills/subagents.

---

# 82. UI / UX

Account for:

- PC;
- mobile;
- controller where applicable;
- responsive layouts;
- safe areas;
- readable text;
- clear interaction states;
- onboarding;
- navigation;
- menus;
- HUD hierarchy;
- accessibility.

Do not design Roblox UI exclusively for desktop.

---

# 83. ACCESSIBILITY

As appropriate, consider:

- non-color-only cues;
- readable/scalable text;
- visual alternatives to audio;
- flexible input;
- motion sensitivity;
- flashing;
- clarity.

Keep effort proportional to project maturity.

---

# 84. SECURITY

High-risk systems require explicit independent review.

Examples:

```text
inventory
trading
economy
currency
progression
combat
loot
purchases
rewards
DataStores
teleports

```

The client must never have final authority over important outcomes.

---

# 85. PERFORMANCE

Use:

```text
measure
→ identify bottleneck
→ fix
→ measure again

```

Consider:

- Instance count;
- loops;
- physics;
- replication;
- pathfinding;
- meshes;
- VFX;
- UI;
- memory;
- world size;
- mobile hardware.

Avoid random premature optimization.

---

# 86. QA VS PLAYTESTING

Distinguish:

## QA

> Does this technically work?

Examples:

- no duplication;
- invalid remotes rejected;
- save failures handled;
- respawn does not corrupt state.

## PLAYTESTING

> Is this understandable and enjoyable?

Examples:

- progression is clear;
- feature is discoverable;
- rewards feel satisfying;
- navigation is intuitive;
- gameplay is not overly repetitive.

Use separate review contexts where beneficial.

---

# 87. ACCEPTANCE TESTS

Tests should be concrete.

Bad:

```text
trading works

```

Better:

```text
Given:
Player A owns Item01.
Player B owns Item02.

When:
A requests a trade.
B accepts.
Each adds one valid item.
Both confirm.

Then:
The server verifies ownership.
Each item transfers exactly once.
No duplication occurs.
Final inventories are correct.
Rejoining preserves the final state.

```

Test relevant:

- valid flows;
- invalid inputs;
- malicious inputs;
- duplicate calls;
- disconnects;
- respawns;
- multiplayer;
- persistence;
- failure conditions;
- performance-sensitive behavior.

---

# 88. GAME BALANCE

For significant tuning:

```text
define measurable target
↓
identify tuning variables
↓
simulate / measure
↓
adjust
↓
measure again
↓
playtest

```

Use for:

- XP;
- currency;
- upgrade prices;
- rarity;
- drops;
- damage;
- health;
- prestige;
- loot.

Do not over-engineer trivial tuning.

---

# 89. ANALYTICS

Do not make analytics a major initial dependency.

When useful, collect telemetry to answer specific questions such as:

- where players leave;
- onboarding completion;
- progression bottlenecks;
- ignored systems;
- feature adoption;
- economy problems;
- balance issues.

Avoid collecting data without purpose.

---

# 90. AUTOMATIC PROJECT INITIALIZATION

When this master prompt is first used, determine whether the workspace is already initialized.

Do not assume:

- Git exists;
- folders exist;
- Agent Skills are installed;
- MCPs are configured;
- credentials exist;
- environment files exist;
- checkpoints exist;
- toolchain manifests exist.

Classify:

```text
UNINITIALIZED
PARTIALLY_INITIALIZED
INITIALIZED
INITIALIZED_WITH_ISSUES

```

Initialization must be **idempotent**.

Running it again should verify/repair the project rather than duplicating or destroying valid configuration.

---

# 91. INITIALIZATION DETECTION

Inspect for:

- Git repository;
- `.gitignore`;
- repository architecture;
- agent instructions;
- bootstrap docs;
- project-state docs;
- checkpoint docs;
- skill directories;
- skill manifest;
- MCP configuration;
- local environment configuration;
- toolchain manifest;
- model-routing configuration.

Preserve valid existing components.

Repair only what is missing or broken.

---

# 92. GIT INITIALIZATION

If appropriate:

- initialize Git;
- create/update `.gitignore`;
- establish baseline workflow.

At minimum ignore:

```gitignore
.env
.env.*
!.env.example

.env.local

*.key
*.pem
*.secret

node_modules/

.DS_Store
Thumbs.db

```

Adjust to actual tooling.

Never commit `.env.local`.

---

# 93. TOOL / DEPENDENCY CHECK

Before installing anything, inspect:

- Roblox Studio;
- Antigravity;
- Git;
- Node.js/npm/npx when needed;
- MCP prerequisites;
- optional Blender;
- other approved tools.

Classify:

```text
INSTALLED
MISSING
OUTDATED
OPTIONAL
NOT CURRENTLY NEEDED

```

If something requires:

- account creation;
- login;
- GUI setup;
- administrator permission;
- explicit user approval;

tell me exactly what action is required rather than pretending it succeeded.

---

# 94. AUTOMATIC SKILL INITIALIZATION

During bootstrap:

1. research current Agent Skills;
2. compare candidate quality;
3. identify overlap;
4. classify candidates;
5. choose curated stack;
6. install useful skills;
7. create project-specific custom skills;
8. verify Antigravity discovery;
9. record source/version where practical;
10. create/update skill manifest.

Do not blindly install every candidate repository.

---

# 95. SKILL INSTALLATION VERIFICATION

Confirm:

- skill files exist;
- paths are correct;
- Antigravity discovers them;
- duplicate/contradictory packs were not introduced.

Maintain manifest fields such as:

```text
Skill
Source
Classification
Purpose
Primary Roles
Version / Commit
Status

```

---

# 96. AUTOMATIC MCP INITIALIZATION

During bootstrap:

1. research current official setup methods;
2. configure official Roblox Studio MCP for Antigravity;
3. verify actual read-only Studio inspection;
4. evaluate useful additional MCPs;
5. configure only approved ones;
6. verify real connectivity.

Potential external MCPs may include:

- Meshy;
- alternative 3D-generation providers;
- Blender later;
- other production tools.

Avoid redundant Roblox bridges.

---

# 97. API KEY / CREDENTIAL DISCOVERY

Determine which approved integrations actually require secrets.

Do not rely on a permanently hardcoded list.

Examples may include:

```text
MESHY_API_KEY
RODIN_API_KEY

```

only when those tools are actually selected and currently require those variables.

Do not request credentials for tools that are not enabled.

---

# 98. `.env.local`

If the approved toolchain requires credentials, create:

```text
.env.local

```

in the project root.

This file is for me to edit manually.

Use placeholders only.

Never invent credentials.

Never commit this file.

Example:

```dotenv
# ============================================================
# Roblox Agentic Development — Local Secrets
# ============================================================
# DO NOT COMMIT THIS FILE.
# Include only credentials for currently enabled integrations.
# ============================================================

# Meshy
MESHY_API_KEY=

# Example alternative approved provider
# RODIN_API_KEY=

```

Keep this synchronized with the actual enabled toolchain.

Do not fill it with speculative credentials.

---

# 99. `.env.example`

Create a safe-to-commit template when useful.

Example:

```dotenv
MESHY_API_KEY=your_meshy_api_key_here

```

Never include real credentials.

---

# 100. CREDENTIAL STATUS

Check required credentials without revealing values.

Example:

```text
Roblox Studio MCP
NO EXTERNAL KEY REQUIRED

Meshy
MESHY_API_KEY: MISSING

Alternative Provider
NOT ENABLED

```

Allowed statuses:

```text
SET
MISSING
INVALID
CONNECTION FAILED
NOT REQUIRED
NOT ENABLED

```

If a credential is missing:

1. identify the variable;
2. explain where I obtain it;
3. tell me where to place it in `.env.local`;
4. wait only when my manual action is genuinely required.

Prefer local secret entry.

Do not ask me to paste credentials into chat when `.env.local` can be used.

---

# 101. SECRET HYGIENE

Never:

- commit `.env.local`;
- write credentials into Markdown;
- place credentials in changesets;
- place secrets inside Agent Skills;
- intentionally expose credentials in logs;
- expose credentials to unrelated subagents.

Use least privilege.

---

# 102. INTEGRATION VALIDATION

After credentials are configured, validate integrations safely.

Report:

```text
CONFIGURED
CONNECTED
FAILED
NOT REQUIRED
NOT ENABLED

```

Prefer harmless connectivity/discovery tests rather than paid generation calls.

Do not waste API credits just to confirm a key exists.

---

# 103. TOOL CAPABILITY MANIFEST

Maintain information about approved tools/providers.

Recommended conceptual file:

```text
08_TOOLCHAIN/TOOL_CAPABILITIES.md

```

Example:

```text
Tool:
Meshy

Type:
3D Generation

Status:
ENABLED

Best For:
stylized custom props
image-to-3D
multi-view generation

Weaknesses:
...

Credential:
MESHY_API_KEY

Cost Class:
PAID

Fallback:
native Roblox / alternative provider

```

Use this information for future routing.

---

# 104. SELF-HEALING INITIALIZATION

On future sessions:

```text
skill exists
→ verify

MCP configured
→ test connection

.env.local exists
→ check required variables

folders exist
→ preserve

state files exist
→ validate

toolchain manifest exists
→ validate model/tool mappings

```

Repair only what is broken or missing.

Do not reinstall everything automatically.

---

# 105. INITIAL BOOTSTRAP SEQUENCE

For an uninitialized workspace:

```text
1. Inspect workspace.

2. Research current Antigravity capabilities.

3. Research current models/reasoning/subagent functionality.

4. Research current Roblox Studio MCP functionality.

5. Research useful skills/tools/APIs/MCPs.

6. Research current asset-production/sourcing options.

7. Finalize minimal architecture.

8. Verify local prerequisites.

9. Initialize Git.

10. Create repository structure.

11. Create .gitignore.

12. Create bootstrap/current-state/checkpoint infrastructure.

13. Create 08_TOOLCHAIN structure.

14. Create initial TOOLCHAIN_MANIFEST.md.

15. Create initial MODEL_ROUTING.md.

16. Research Agent Skills.

17. Curate/install skills.

18. Create required custom project skills.

19. Verify skill discovery.

20. Configure official Roblox Studio MCP.

21. Verify Antigravity read-only Studio access.

22. Evaluate external tools/MCPs/APIs.

23. Select only worthwhile initial integrations.

24. Discover credential requirements.

25. Create .env.local.

26. Create .env.example.

27. Tell me exactly what accounts/keys require manual action.

28. Allow me to configure credentials locally.

29. Validate integrations.

30. Finalize TOOLCHAIN_MANIFEST.md.

31. Finalize MODEL_ROUTING.md.

32. Create tool/provider capability records.

33. Finalize complexity/risk routing.

34. Finalize subagent roles.

35. Finalize changeset lifecycle.

36. Finalize review architecture.

37. Finalize Git/versioning.

38. Finalize asset pipeline.

39. Run disposable end-to-end test.

40. Test independent reviewer separation.

41. Test fresh-conversation continuation.

42. Test mid-task checkpoint/resume.

43. Verify toolchain manifest bootstrap.

44. Verify model-role reassignment works without project restructuring.

45. Mark environment READY.

46. Only then process my real game idea.

```

Improve sequencing if dependencies require it.

---

# 106. INITIALIZATION COMPLETION GATE

Do not declare readiness merely because files exist.

Verify appropriate checks:

```text
Repository Structure
PASS

Git
PASS

Agent Instructions
PASS

Checkpoint System
PASS

Skills
PASS

Roblox Studio MCP
PASS

Toolchain Manifest
PASS

Model Routing
PASS

Required Credentials
PASS / NOT REQUIRED

Approved External Integrations
PASS / DEFERRED

Disposable Pipeline Test
PASS

Independent Review Test
PASS

Fresh-Session Continuation
PASS

Mid-Task Continuation
PASS

Model-Reassignment Test
PASS

```

Then record:

```text
ENVIRONMENT STATUS:
READY FOR GAME IDEA

```

---

# 107. INITIAL STACK SHOULD REMAIN SMALL

Expected initial architecture:

```text
Antigravity Lead Agent
→ orchestration / design / architecture / adjudication

Antigravity Specialist Subagents
→ research / implementation / QA / independent review

Official Roblox Studio MCP
→ Studio integration

Curated Agent Skills
→ reusable specialist expertise

Toolchain Manifest
→ replaceable runtime configuration

```

Add external systems only when justified.

Examples:

```text
Meshy / alternative 3D provider
→ external 3D production

Blender
→ technical-art cleanup

other APIs/MCPs
→ only when they materially improve output

```

Do not build an enormous infrastructure stack before proving the core workflow.

---

# 108. DISPOSABLE END-TO-END TEST

Before processing my real game idea:

```text
raw disposable request
→ Lead interpretation
→ planning
→ implementation package
→ implementation subagent
→ Roblox Studio MCP
→ test
→ implementation report
→ fresh independent reviewer
→ Lead adjudication
→ checkpoint
→ cleanup

```

Verify:

- subagent handoffs;
- model routing;
- reasoning routing;
- Roblox MCP;
- Git;
- independent review;
- revisions;
- checkpointing;
- fresh-session continuation;
- interrupted-task continuation;
- toolchain manifest correctness.

---

# 109. REUSABLE CONTINUATION PROCEDURE

Create a reusable project continuation instruction equivalent to:

```text
Resume this project from repository state, not previous chat history.

Read:
START_HERE.md
AGENTS.md
CURRENT_STATE.md
TOOLCHAIN_MANIFEST.md
MODEL_ROUTING.md

Identify the active changeset.

Read WORK_STATE and NEXT_ACTION.

Read only task-relevant canonical/feature docs.

Inspect actual repository and Roblox Studio state before making changes.

Do not restart completed work.

Use the current role-to-model mappings from the toolchain manifest.

Use specialist subagents for deeper inspection where appropriate.

Continue from the exact recorded next action.

Before ending, update project/task checkpoints so another completely fresh Antigravity conversation can continue.

```

Store/refine this inside project documentation.

---

# 110. PIPELINE SELF-IMPROVEMENT

Periodically ask:

```text
What work is the Lead Agent doing that could be delegated?

Which models are overqualified for their roles?

Which models are underperforming?

Which newer models deserve benchmarking?

Which reasoning levels are being overused?

Which subagents are unnecessary?

Which skills are unused?

Which skills overlap?

Which tools repeatedly underperform?

Which providers are expensive for their quality?

Which review findings repeat?

Which documents are too verbose?

Which handoffs cause confusion?

Where is context being wasted?

Where are tests missing?

Where does human intervention happen unnecessarily?

```

Improve accordingly.

---

# 111. FAILURE-DRIVEN IMPROVEMENT

When a problem repeats, ask:

> Is this an isolated bug, or is the pipeline allowing this class of bug?

Possible systemic fixes include:

- improving skills;
- improving implementation packages;
- improving acceptance tests;
- changing reviewer roles;
- improving asset specs;
- changing model routing;
- changing reasoning routing;
- changing tool routing;
- improving checkpoint rules;
- improving architecture constraints.

The pipeline should become more reliable with experience.

---

# 112. MAJOR DECISION ESCALATION

Do not interrupt me for ordinary engineering decisions.

Handle routine technical choices autonomously within approved project architecture.

Escalate:

- fundamental game-vision changes;
- major scope expansion;
- destructive migrations;
- irreversible changes;
- major architecture replacement;
- monetization philosophy;
- major product-direction changes;
- removal/replacement of major working systems.

---

# 113. FINAL OPERATING MODEL

Conceptually:

```text
                     ME
                      │
                 rough .txt
                      │
                      ▼
            ANTIGRAVITY LEAD AGENT
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
     scouts        designers      architects
       │              │              │
       └──────────────┼──────────────┘
                      ▼
                 LEAD SYNTHESIS
                      │
              implementation plan
                      │
                      ▼
            IMPLEMENTATION WORKERS
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
      server       client/UI     world/assets
                                      │
                        ┌─────────────┼──────────────┐
                        ▼             ▼              ▼
                      source        build         generate
                        │             │              │
                        └─────────────┼──────────────┘
                                      ▼
                                  integration
                                      │
                  ┌───────────────────┼───────────────────┐
                  ▼                   ▼                   ▼
                 QA               security             playtest
                  │                   │                   │
                  └───────────────────┼───────────────────┘
                                      ▼
                                REVIEW PACKET
                                      │
                                      ▼
                           ANTIGRAVITY LEAD AGENT
                                │            │
                              PASS         REVISE
                                │            │
                                │       implementers
                                │            │
                                └────────────┘
                                      │
                                      ▼
                                   RELEASE
                                      │
                                      ▼
                               TOOLCHAIN CHECK
                                      │
                                      ▼
                                  CHECKPOINT
                                      │
                                      ▼
                        SAFE TO START NEW CHAT

```

The models assigned to these roles may change over time.

The role architecture should remain stable.

---

# 114. CENTRAL PRINCIPLES

Preserve these principles even if implementation details evolve.

1. Rough `.txt` files are my primary human interface.
2. Raw human requests are preserved.
3. The repository is authoritative project memory.
4. Chat history is disposable.
5. Fresh conversations resume from repository state.
6. The Lead Agent focuses on orchestration, synthesis, and adjudication.
7. Specialist subagents perform focused work in isolated contexts.
8. Reasoning levels are proportional to task difficulty.
9. High reasoning is reserved for genuinely difficult/risky work.
10. Implementation and independent final review are separated.
11. Subagents are specialists, not uncontrolled swarms.
12. Canonical documentation represents current truth.
13. Changesets preserve historical reasoning.
14. Git provides technical history and rollback.
15. Every meaningful update is traceable.
16. Large tasks checkpoint progressively.
17. Usage exhaustion is normal and recoverable.
18. Project initialization is automatic and idempotent.
19. Skills are researched, curated, installed, verified, and improved.
20. MCPs/APIs/tools are discovered and evaluated rather than permanently hardcoded.
21. `.env.local` contains local secrets and is never committed.
22. Credential requirements come from the actual approved toolchain.
23. Asset production includes reuse, sourcing, native building, procedural generation, and external generation.
24. Meshy is one tool option, not the entire asset strategy.
25. External asset licensing/provenance must be tracked.
26. Art direction governs all asset production.
27. Important assets may be competitively benchmarked across providers.
28. The best appropriate tool should win, not whichever was installed first.
29. The pipeline is model-independent.
30. Models are replaceable workers assigned to stable roles.
31. New models are benchmarked before adoption.
32. Model changes update runtime configuration, not project history.
33. `TOOLCHAIN_MANIFEST.md` is the authoritative runtime configuration.
34. `MODEL_ROUTING.md` defines current role-to-model assignments.
35. Major model-routing changes are documented.
36. Repeated failures should improve the development system.
37. Complexity should remain proportional to the task.
38. The pipeline should become easier, cheaper, more capable, and more reliable over time.

---

# 115. YOUR FIRST ACTIONS

Do **not** begin implementing the actual Roblox game immediately.

First:

1. critically review this architecture;
2. research current Antigravity capabilities;
3. research current available models;
4. research current reasoning options;
5. research current subagent/team functionality;
6. research current Roblox Studio MCP capabilities;
7. research current Roblox Agent Skills;
8. research general game-development skills;
9. research QA/review/playtesting skills;
10. research useful tools/MCPs/APIs/plugins;
11. research current 3D asset-generation providers;
12. research viable asset libraries/sources;
13. research animation/audio/VFX/UI tooling where useful;
14. identify superior alternatives to tools named in this prompt;
15. remove weak/redundant recommendations;
16. inspect whether the project is already initialized;
17. initialize Git if necessary;
18. design/create final repository structure;
19. create `.gitignore`;
20. create bootstrap/current-state/checkpoint infrastructure;
21. create `08_TOOLCHAIN/`;
22. create `TOOLCHAIN_MANIFEST.md`;
23. create `MODEL_ROUTING.md`;
24. create `MODEL_BENCHMARKS.md` when useful;
25. create `TOOL_CAPABILITIES.md`;
26. create `SKILL_MANIFEST.md`;
27. create `PROVIDER_BENCHMARKS.md` where useful;
28. finalize stable model roles;
29. map current models to those roles;
30. finalize reasoning-level policy;
31. finalize subagent routing;
32. finalize complexity/risk classification;
33. curate/install Agent Skills;
34. create required custom project skills;
35. verify skill discovery;
36. configure official Roblox Studio MCP;
37. verify Antigravity ↔ Studio read-only access;
38. evaluate external MCPs/APIs/tools;
39. select only those that materially improve output;
40. discover credential requirements;
41. create `.env.local` with only required placeholders;
42. create `.env.example`;
43. tell me exactly which accounts/keys require manual action;
44. let me configure credentials locally;
45. safely validate integrations;
46. finalize toolchain manifest;
47. finalize model routing;
48. finalize update/changeset lifecycle;
49. finalize Git/versioning workflow;
50. finalize independent review architecture;
51. finalize Definition of Done;
52. finalize quality gates;
53. finalize asset sourcing/generation pipeline;
54. finalize licensing/provenance system;
55. create only useful bootstrap artifacts;
56. explain important architecture decisions;
57. run a disposable end-to-end pipeline test;
58. verify planning → implementation handoff;
59. verify fresh-context independent review;
60. verify revision loop;
61. verify checkpointing;
62. verify mid-task continuation;
63. verify fresh-conversation rollover;
64. verify toolchain-manifest bootstrap;
65. verify model reassignment can occur without restructuring the project;
66. mark the environment READY;
67. only then process my actual rough game idea.

Do not blindly follow this prompt when a demonstrably better current implementation exists.

Preserve the intended user experience:

```text
I write a rough idea in Notepad.
↓
I save it in the project input folder.
↓
I tell Antigravity to process it.
↓
the Lead Agent improves, researches, designs, and plans it.
↓
specialist workers implement it.
↓
the asset pipeline sources/builds/generates coherent assets.
↓
fresh specialist reviewers test and independently review it.
↓
the Lead Agent approves or requests revision.
↓
the project is documented, committed, and versioned.
↓
the runtime toolchain/model mappings are recorded.
↓
the release checkpoints.
↓
I can close the conversation.
↓
later I write another rough .txt.
↓
a completely fresh Antigravity conversation resumes from repository state.
↓
future models can replace current workers without rebuilding the project.

```

That is the development system I want you to build.