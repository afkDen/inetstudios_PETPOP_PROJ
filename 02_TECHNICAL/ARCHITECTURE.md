# TECHNICAL ARCHITECTURE — Development Operating System

## Core invariant

`repository state > session history`.

The development operating system is runtime- and model-neutral. Stable project primitives are root `AGENTS.md`, canonical `.agents/skills/`, semantic role/capability contracts, changesets, acceptance tests, review evidence, project/runtime state, and Git history.

## Execution architecture

```text
Human rough .txt request
        ↓
Lead role
        ↓
interpret / research / design / risk routing
        ↓
implementation package + acceptance tests
        ↓
isolated implementation worker(s)
        ↓
Studio operator for live Roblox operations when needed
        ↓
tests / evidence
        ↓
fresh independent reviewer(s)
        ↓
Lead adjudication / revision loop
        ↓
canonical docs + Git + checkpoint
```

A runtime is an execution host, not project identity. Native subagents are preferred when reliable; otherwise role isolation may be emulated with fresh sessions/worktrees/remote workers. Exact models are replaceable runtime bindings to capability classes.
