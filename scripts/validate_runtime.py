#!/usr/bin/env python3
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--runtime',default='generic'); a=ap.parse_args()
 cfg=json.loads((ROOT/'08_TOOLCHAIN/RUNTIME_PROFILES.json').read_text()); profiles=cfg['profiles']; rid=a.runtime if a.runtime in profiles else cfg['fallback_profile']; p=profiles[rid]
 assert (ROOT/'AGENTS.md').exists(); assert (ROOT/'.agents/skills').exists(); assert (ROOT/'08_TOOLCHAIN/ROLE_CONTRACTS/roles.json').exists()
 skills=[x.parent.name for x in (ROOT/'.agents/skills').glob('*/SKILL.md')]
 if not skills: raise SystemExit('FAIL: no canonical skills discovered')
 print(json.dumps({'requested_runtime':a.runtime,'profile':rid,'mode_hint':p['mode_hint'],'canonical_skill_root':p['skill_source'],'canonical_skill_count':len(skills),'requires_direct_validation':p.get('requires_direct_validation',True),'status':'STATIC_PASS_RUNTIME_EVIDENCE_STILL_REQUIRED'},indent=2))
if __name__=='__main__': main()
