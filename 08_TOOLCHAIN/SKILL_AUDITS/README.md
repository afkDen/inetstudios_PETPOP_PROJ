# Third-party skill audit reports

The initializer writes one JSON static-audit report per managed external skill here. Reports are deterministic evidence for semantic supply-chain review; they are **not security approval by themselves**.

A runtime may mark `skill_supply_chain_review` PASS only when:

1. `08_TOOLCHAIN/SKILL_LOCK.json` exists and matches every managed skill tree;
2. every managed skill has a current audit report in this directory; and
3. a fresh semantic reviewer has adjudicated the exact locked content and recorded the lock digest in initialization evidence.
