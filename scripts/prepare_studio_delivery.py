#!/usr/bin/env python3
"""Create, but never auto-approve, an issue-local Studio MCP/Rojo receipt draft."""
from __future__ import annotations
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def prepare(issue:int,root:Path=ROOT):
    if not 1<=issue<=999999:raise ValueError('issue must be 1..999999')
    matches=list((root/'04_CHANGESETS').glob(f'GH-{issue:06d}_*'))
    if len(matches)!=1 or not matches[0].is_dir():
        raise ValueError('expected exactly one existing issue changeset; create/resume it with scripts/team.py first')
    out=matches[0]/'STUDIO_DELIVERY.json'
    if out.exists():
        print('UNCHANGED: existing Studio delivery receipt preserved:',out.relative_to(root));return out
    template=json.loads((root/'templates/STUDIO_DELIVERY_TEMPLATE.json').read_text())
    template['issue']=issue
    task_path=matches[0]/'TASK.json'
    if task_path.is_file():
        task=json.loads(task_path.read_text(encoding='utf-8'))
        template['scope_revision']=int(task.get('scope_revision',0) or 0)
    out.write_text(json.dumps(template,indent=2)+'\n')
    print('DRAFT ONLY:',out.relative_to(root))
    print('Follow 02_TECHNICAL/LIVE_STUDIO_DELIVERY.md; populate from real MCP + Rojo + playtest evidence, never guess PASS.')
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--issue',type=int,required=True);a=ap.parse_args()
    try:prepare(a.issue)
    except ValueError as exc:ap.exit(2,'BLOCKED: '+str(exc)+'\n')
