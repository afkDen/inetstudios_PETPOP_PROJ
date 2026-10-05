#!/usr/bin/env python3
from pathlib import Path
import json
import re
ROOT=Path(__file__).resolve().parents[1]
ROLES=json.loads((ROOT/'08_TOOLCHAIN/ROLE_CONTRACTS/roles.json').read_text())['roles']
SKILLS=json.loads((ROOT/'08_TOOLCHAIN/SKILL_REGISTRY.json').read_text())['skills']


def skill_counts():
    bundled=sum(1 for s in SKILLS if s.get('origin')=='project' and s.get('state')=='bundled')
    external=sum(1 for s in SKILLS if s.get('origin')=='external')
    return bundled,external,len(SKILLS)


def skill_count_doc_updates():
    bundled,external,total=skill_counts()
    return {
        ROOT/'06_PROJECT_STATE/CURRENT_STATE.md': [
            (r'- Skills: \d+ bundled \+ \d+ reviewed external = \d+ registered after maintainer resolution',
             f'- Skills: {bundled} bundled + {external} reviewed external = {total} registered after maintainer resolution'),
        ],
        ROOT/'06_PROJECT_STATE/FINAL_SCAFFOLD_REVIEW.md': [
            (r'- \d+ bundled project-authored skills in the reusable template\.',
             f'- {bundled} bundled project-authored skills in the reusable template.'),
            (r'- \d+ reviewed external skills expected after maintainer resolution\.',
             f'- {external} reviewed external skills expected after maintainer resolution.'),
            (r'- \d+ registered skills total\.',
             f'- {total} registered skills total.'),
        ],
    }


def sync_skill_count_docs(*, check=False):
    stale=[]
    for path,replacements in skill_count_doc_updates().items():
        current=path.read_text(encoding='utf-8')
        expected=current
        for pattern,replacement in replacements:
            expected,n=re.subn(pattern,replacement,expected,count=1)
            if n!=1:
                raise RuntimeError(f'cannot locate derived skill-count line in {path.relative_to(ROOT)}')
        if current!=expected:
            if check:
                stale.append(path.relative_to(ROOT).as_posix())
            else:
                path.write_text(expected,encoding='utf-8')
    return stale

def routing_view():
    lines=[
        '# ROLE ↔ SKILL ROUTING',
        '',
        '> **GENERATED VIEW.** Canonical role definitions live in `08_TOOLCHAIN/ROLE_CONTRACTS/roles.json`. Regenerate with `python scripts/sync_derived_docs.py`; do not hand-edit this table.',
        '',
        'All active skills live in `.agents/skills/`. This file is human-readable only and never overrides the role contracts.',
        '',
        '| Role | Model class | Required skills | Write policy |',
        '|---|---|---|---|',
    ]
    for r in sorted(ROLES,key=lambda x:x['id']):
        skills=', '.join(f'`{s}`' for s in r.get('required_skills',[])) or '—'
        lines.append(f"| `{r['id']}` | `{r['model_class']}` | {skills} | `{r['write_policy']}` |")
    lines += [
        '',
        '## Policy',
        '',
        '- Root `AGENTS.md` owns project-wide rules.',
        '- Skills provide on-demand procedures and domain expertise.',
        '- Role contracts define responsibility/isolation; runtime adapters only translate them.',
        '- Load the minimum relevant skill set. Do not inject every installed skill body into every context.',
        '- Query Graphify before broad repository scans or discovery-only delegation when the local graph is ready.',
        '- Never exceed three active subagents; use sequential waves for additional specialist passes.',
        '- `assurance-reviewer` is the fresh multi-mode independent review boundary.',
        '- `studio-operator` is the semantic live-Studio boundary; the runtime adapter determines how that bridge is granted.',
        '',
    ]
    return '\n'.join(lines)

def main():
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('--check',action='store_true'); a=ap.parse_args()
    out=ROOT/'08_TOOLCHAIN/AGENT_SKILL_ROUTING.md'; expected=routing_view()
    if a.check:
        stale=[]
        if not out.exists() or out.read_text(encoding='utf-8')!=expected: stale.append(out.relative_to(ROOT).as_posix())
        stale+=sync_skill_count_docs(check=True)
        if stale:
            raise SystemExit('FAIL: derived documentation is stale ('+', '.join(stale)+'); run python scripts/sync_derived_docs.py')
        print('PASS: derived documentation current'); return
    out.write_text(expected,encoding='utf-8')
    sync_skill_count_docs(check=False)
    print('PASS: synchronized derived documentation')
if __name__=='__main__': main()
