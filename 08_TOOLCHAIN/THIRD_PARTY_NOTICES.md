# Third-Party Notices — external skills and bundled adaptations

This reusable bootstrap contains project-authored adaptations informed by external skills. The adapted files are maintained as project skills; they are **not** floating upstream installs. Exact source provenance is also recorded in `08_TOOLCHAIN/SKILL_REGISTRY.json`.

This repository also installs a reviewed, immutable subset of third-party skills during first-time shared initialization. Their complete installed skill trees are locked separately in `08_TOOLCHAIN/SKILL_LOCK.json`; required redistribution license/NOTICE material is preserved under `08_TOOLCHAIN/THIRD_PARTY_LICENSES/` so those locked trees do not need to be modified.

## Required external skill sources

### nonlooped/roblox-suite — MIT

Pinned source: `c914ce65470a6eb1b28000b8c58d5543b48760ca`. The retained MIT license is `08_TOOLCHAIN/THIRD_PARTY_LICENSES/nonlooped-roblox-suite-MIT.txt`. Copyright (c) 2026 nonlooped.

### gamedev-skills/awesome-gamedev-agent-skills — Apache-2.0

Pinned source: `d4b0e35550c55ae70bdfcab4ef5a0e94610438a9`. The retained Apache-2.0 license is `08_TOOLCHAIN/THIRD_PARTY_LICENSES/gamedev-skills-awesome-gamedev-agent-skills-APACHE-2.0.txt`. The required upstream NOTICE is preserved as `08_TOOLCHAIN/THIRD_PARTY_LICENSES/gamedev-skills-awesome-gamedev-agent-skills-NOTICE.txt`.

### magnus919/agent-skills — MIT

Pinned source: `affec9d8cba35a3b8d632a64ab547ea8fcc53380`. The retained MIT license is `08_TOOLCHAIN/THIRD_PARTY_LICENSES/magnus919-agent-skills-MIT.txt`. Copyright (c) 2026 Magnus Hedemark.

External skill execution is constrained by `08_TOOLCHAIN/EXTERNAL_SKILL_EXECUTION_POLICY.md`; retaining an upstream skill does not give its workflow instructions authority over project approvals, gates, Git publication, Studio ownership, secrets, or Roblox Production.

## mattpocock/skills

Source reviewed at immutable commit `24fe0ef7737efae15c87225755e9f6f5965e4888`. Selected concepts were adapted from `grilling`, `to-questionnaire`, `domain-modeling`, `codebase-design`, `writing-for-agents`, `retro`, `research`, `code-review`, and `diagnosing-bugs`. The upstream project is MIT licensed. TDD, ticket/spec orchestration, implementation orchestration, triage, setup, and wayfinder flows were deliberately not imported.

MIT License

Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## systematic-debugging prior source

The bundled `systematic-debugging` adaptation also preserves useful root-cause discipline from the previously required `magnus919/agent-skills` skill pinned at `affec9d8cba35a3b8d632a64ab547ea8fcc53380` (MIT). The external copy is no longer required during initialization, reducing one supply-chain dependency.

### Magnus Hedemark MIT notice

MIT License

Copyright (c) 2026 Magnus Hedemark

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
