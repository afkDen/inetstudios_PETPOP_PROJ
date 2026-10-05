#!/usr/bin/env python3
"""Human-invoked, integration-owner acceptance copy for immutable input; does not approve GitHub issue itself."""
from __future__ import annotations
import argparse, json, hashlib, re, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def promote(issue:int, kind:str, approved_by:str, root=ROOT, allow_test_branch=False):
    if kind not in {'idea','update'}:raise ValueError('invalid kind')
    if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?',approved_by):raise ValueError('invalid approving GitHub username')
    if issue<1 or issue>999999:raise ValueError('invalid issue')
    if not allow_test_branch:
        cp=subprocess.run(['git','branch','--show-current'],cwd=root,text=True,stdout=subprocess.PIPE,check=False)
        if cp.stdout.strip()!='main':raise PermissionError('acceptance may only be recorded by an integrator on main')
    key=f'GH-{issue:06d}'
    folder=root/'00_INPUT/PROPOSALS'/('IDEAS' if kind=='idea' else 'UPDATES')
    proposals=list(folder.glob(key+'_*.txt'))
    if len(proposals)!=1:raise ValueError('exactly one accepted proposal with this GH issue key required')
    src=proposals[0]; meta=json.loads(src.with_suffix('.json').read_text()); raw=src.read_bytes()
    if meta.get('issue')!=issue or meta.get('kind')!=kind or meta.get('sha256')!=hashlib.sha256(raw).hexdigest():raise ValueError('source metadata/hash mismatch')
    if kind=='idea':
        dest=root/'00_INPUT/GAME_IDEA/rough_game_idea.txt'
        if dest.exists():raise FileExistsError('canonical game idea already accepted; changes must be updates')
        log=root/'00_INPUT/GAME_IDEA/APPROVAL.json'
    else:
        cs=list((root/'04_CHANGESETS').glob(key+'_*'))
        if len(cs)!=1 or not (cs[0]/'USER_REQUEST.txt').is_file() or (cs[0]/'USER_REQUEST.txt').read_bytes()!=raw:
            raise ValueError('update promotion requires an integrated issue changeset preserving original raw input')
        dest=root/'00_INPUT/UPDATES/PROCESSED'/src.name
        if dest.exists():raise FileExistsError('update already archived')
        log=dest.with_suffix('.json')
    dest.parent.mkdir(parents=True,exist_ok=True)
    # Recorded approver is a declaration only, not a verified GitHub PR approval.
    policy_file=root/'08_TOOLCHAIN/TEAM_POLICY.json'
    if policy_file.is_file():
        policy=json.loads(policy_file.read_text(encoding='utf-8'))
        if policy.get('template_unconfigured') is not False:
            raise ValueError('cannot approve an idea in an unconfigured template')
        issue_url=policy['remote_url'].removesuffix('.git')+f'/issues/{issue}'
    elif allow_test_branch: issue_url='' # Isolated unit fixture, never real acceptance.
    else: raise FileNotFoundError('TEAM_POLICY.json is required for a real game')
    record={'schema_version':1,'issue':issue,'proposal':src.relative_to(root).as_posix(),'sha256':meta['sha256'],'approved_by_declared':approved_by,'github_issue_url':issue_url,'github_review_verified_by_script':False}
    if log.exists():raise FileExistsError('acceptance metadata exists, review before updating')
    with dest.open('xb') as f:f.write(raw)
    try:log.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    except Exception:dest.unlink(missing_ok=True);raise
    return dest

def main():
    p=argparse.ArgumentParser(description='Record a human-approved proposal in immutable main-branch input. Does not independently verify PR approval.')
    p.add_argument('--issue',type=int,required=True);p.add_argument('--kind',choices=['idea','update'],required=True)
    p.add_argument('--approved-by',required=True,help='username of actual human integrator; CLI does not verify identity or GitHub approval')
    a=p.parse_args()
    try:d=promote(a.issue,a.kind,a.approved_by)
    except (ValueError,FileExistsError,PermissionError) as e:p.error(str(e))
    print(d.relative_to(ROOT).as_posix())
if __name__=='__main__':main()
