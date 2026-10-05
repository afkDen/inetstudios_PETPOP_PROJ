#!/usr/bin/env python3
"""Join existing team repository without mutating tracked bootstrap/global state."""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LOCAL=ROOT/'.local'

def local_profile(developer, runtime, runtime_version='', model_label=''):
    if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?',developer):
        raise ValueError('use your GitHub username, not an email, path or token')
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}',runtime):
        raise ValueError('runtime id must be lowercase letters/digits/hyphens')
    for label,value in [('runtime-version',runtime_version),('model-label',model_label)]:
        if len(value)>120 or any(c in value for c in ('\n','\r','\0')): raise ValueError(label+' is invalid')
    return {'schema_version':1,'developer':developer,'runtime':runtime,'runtime_version':runtime_version or 'unspecified','model_label':model_label or 'configured locally','runtime_validation_path':'.local/RUNTIME_VALIDATIONS.json','shared_main_is_not_local_state':True}

def load_profile(developer, runtime, runtime_version='', model_label=''):
    p=local_profile(developer,runtime,runtime_version,model_label)
    pth=LOCAL/'developers'/f'{developer.lower()}__{runtime}.json'
    pth.parent.mkdir(parents=True,exist_ok=True)
    # Do not overwrite an unchanged personal profile (idempotent).
    if not pth.exists() or json.loads(pth.read_text())!=p: pth.write_text(json.dumps(p,indent=2)+'\n')
    return pth

def check(root=ROOT):
    issues=[]
    for path in ['AGENTS.md','TEAM_PROTOCOL.md','08_TOOLCHAIN/SKILL_REGISTRY.json','08_TOOLCHAIN/TEAM_POLICY.json']:
        if not (root/path).exists():issues.append('missing '+path)
    lock=root/'08_TOOLCHAIN/SKILL_LOCK.json'
    if not lock.exists(): issues.append('no committed approved SKILL_LOCK.json: shared first-time skill bootstrap still required')
    else:
        from initialize_project import expected_external,lock_current,audits_current
        _,expected=expected_external()
        if not lock_current(expected) or not audits_current(expected):issues.append('shared external skills missing or changed: do not silently upgrade; ask integrator to repair from reviewed Git state')
    # Shared state intentionally not touched by checks or local joins.
    return issues

def main():
    ap=argparse.ArgumentParser(description='Initialize personal runtime setup only; never reset global project or change shared skill versions.')
    ap.add_argument('--developer',required=True,help='GitHub username')
    ap.add_argument('--runtime',required=True)
    ap.add_argument('--runtime-version',default='')
    ap.add_argument('--model-label',default='',help='Descriptive local model binding (not credentials)')
    ap.add_argument('--check-only',action='store_true')
    a=ap.parse_args()
    policy=json.loads((ROOT/'08_TOOLCHAIN/TEAM_POLICY.json').read_text(encoding='utf-8'))
    if policy.get('template_unconfigured') is not False:
        raise SystemExit('BLOCKED: reusable bootstrap is not bound to a game; use NEW_GAME_SETUP.md first')
    p=local_profile(a.developer,a.runtime,a.runtime_version,a.model_label)
    if not a.check_only:
        path=load_profile(a.developer,a.runtime,a.runtime_version,a.model_label)
        cp=subprocess.run([sys.executable,'scripts/sync_runtime_adapters.py','--runtime',a.runtime],cwd=ROOT,check=False)
        if cp.returncode:raise SystemExit('runtime adapter failed: inspect your toolchain')
        # Create local runtime registry from the shared template, never write the tracked template.
        local=LOCAL/'RUNTIME_VALIDATIONS.json'
        if not local.exists():
            template=json.loads((ROOT/'06_PROJECT_STATE/RUNTIME_VALIDATIONS.json').read_text())
            local.parent.mkdir(parents=True,exist_ok=True)
            local.write_text(json.dumps(template,indent=2)+'\n')
        print('Personal profile:',path.relative_to(ROOT))
    issues=check()
    if issues:
        print('PERSONAL SETUP: PARTIAL — '+ '; '.join(issues))
        print('Personal runtime must independently validate skill discovery, context isolation, models and real Studio bridge.')
        return 0 # Missing shared bootstrap is reported, not silently fabricated or destructive.
    print('PERSONAL SETUP: CORE CHECKS PASS; live runtime and Studio direct-evidence gates remain separate.')
    return 0
if __name__=='__main__':raise SystemExit(main())
