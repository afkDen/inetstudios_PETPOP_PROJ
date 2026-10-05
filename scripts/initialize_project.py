#!/usr/bin/env python3
from __future__ import annotations
import argparse,datetime as dt,hashlib,json,os,re,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STATUS=ROOT/'06_PROJECT_STATE/INITIALIZATION_STATUS.json'
RUNTIME_TEMPLATE=ROOT/'06_PROJECT_STATE/RUNTIME_VALIDATIONS.json'
RUNTIMES=ROOT/'.local/RUNTIME_VALIDATIONS.json'
CFG=ROOT/'08_TOOLCHAIN/EXTERNAL_SKILLS.json'
SKILLS=ROOT/'.agents/skills'
LOCK=ROOT/'08_TOOLCHAIN/SKILL_LOCK.json'
AUDITS=ROOT/'08_TOOLCHAIN/SKILL_AUDITS'
QUARANTINE=ROOT/'08_TOOLCHAIN/SKILL_QUARANTINE'
GLOBAL={'repository_structure','git','canonical_skills','external_skills','skill_supply_chain_review','local_tests','free_tool_probe','credential_policy'}
RUNTIME={'capability_validation','model_policy_validation','skill_discovery','role_execution_validation','developer_toolchain','roblox_studio_bridge','rojo_live_sync','studio_disposable_test'}

def now(): return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()

def authorized_global_branch():
 """The human must additionally be an authorized maintainer; a branch name alone cannot prove that."""
 branch=run(['git','branch','--show-current'],check=False).stdout.strip()
 return branch=='main' or branch.startswith('infra/')
def load(p): return json.loads(p.read_text())
def save(p,o): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2)+'\n')
def run(c,check=True,env=None):
 e=os.environ.copy(); e.update(env or {}); print('+',' '.join(c)); return subprocess.run(c,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=check,env=e)

def treehash(root: Path):
 """Hash paths, object types, symlink targets, and file bytes for the complete skill tree."""
 h=hashlib.sha256()
 for p in sorted(root.rglob('*'), key=lambda x:x.relative_to(root).as_posix()):
  rel=p.relative_to(root).as_posix(); h.update(rel.encode()+b'\0')
  if p.is_symlink(): h.update(b'L\0'+os.readlink(p).encode()+b'\0')
  elif p.is_dir(): h.update(b'D\0')
  elif p.is_file(): h.update(b'F\0'); h.update(p.read_bytes()); h.update(b'\0')
  else: h.update(b'O\0')
 return h.hexdigest()

def setg(g,s,e=''):
 x=load(STATUS); x['checks'][g]={'status':s,'evidence':e}; x['last_updated']=now()
 if s!='PASS' and x.get('project_status')=='READY_FOR_GAME_IDEA': x['project_status']='INITIALIZATION_REQUIRED'
 save(STATUS,x)

def runtime_entry(rid):
 x=load(RUNTIMES if RUNTIMES.exists() else RUNTIME_TEMPLATE); return x,x['runtimes'].setdefault(rid,{'mode':'UNVALIDATED','status':'VALIDATION_REQUIRED','checks':{k:{'status':'NOT_RUN','evidence':''} for k in sorted(RUNTIME)}})

def setr(rid,g,s,e='',mode=None):
 x,r=runtime_entry(rid); r['checks'][g]={'status':s,'evidence':e}; r['last_updated']=now()
 if mode: r['mode']=mode
 if s!='PASS' and r.get('status')=='READY': r['status']='VALIDATION_REQUIRED'
 save(RUNTIMES,x)

def expected_external():
 cfg=load(CFG); return cfg,[n for src in cfg['sources'] if src.get('install')=='required' for n in src['skills']]

def lock_current(expected):
 if not LOCK.exists(): return False
 try:
  m=load(LOCK); hashes=m.get('skill_tree_sha256',{})
  return set(hashes)==set(expected) and all((SKILLS/n/'SKILL.md').exists() and treehash(SKILLS/n)==hashes[n] for n in expected)
 except Exception: return False

def audits_current(expected):
 return all((AUDITS/f'{n}.json').exists() for n in expected)

def quarantine_existing(expected):
 existing=[n for n in expected if (SKILLS/n).exists()]
 if not existing: return None
 stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ'); q=QUARANTINE/stamp; q.mkdir(parents=True,exist_ok=True)
 for n in existing: shutil.move(str(SKILLS/n),str(q/n))
 return q

def restore_quarantine(q,expected):
 if not q: return
 for n in expected:
  cur=SKILLS/n
  if cur.exists(): shutil.rmtree(cur) if cur.is_dir() and not cur.is_symlink() else cur.unlink()
  old=q/n
  if old.exists(): shutil.move(str(old),str(cur))

def git_has(path: str):
 if not (ROOT/'.git').exists(): return False
 return run(['git','cat-file','-e',f'HEAD:{path}'],check=False).returncode==0

def restore_reviewed_external_from_git(expected):
 """Repair drift from the exact reviewed/committed state before considering network resolution."""
 if not git_has('08_TOOLCHAIN/SKILL_LOCK.json'): return False,None
 tracked=[f'.agents/skills/{n}' for n in expected]
 if not all(git_has(f'{x}/SKILL.md') for x in tracked): return False,None
 q=quarantine_existing(expected)
 paths=['08_TOOLCHAIN/SKILL_LOCK.json','08_TOOLCHAIN/SKILL_AUDITS']+tracked
 cp=run(['git','restore','--source=HEAD','--']+paths,check=False)
 if cp.returncode or not lock_current(expected) or not audits_current(expected):
  restore_quarantine(q,expected); return False,None
 return True,q

def run_static_audits(expected):
 AUDITS.mkdir(parents=True,exist_ok=True)
 for old in AUDITS.glob('*.json'): old.unlink()
 for n in expected:
  cp=run([sys.executable,'scripts/audit_skill_tree.py',str(SKILLS/n),'--output',str(AUDITS/f'{n}.json')],check=False)
  if cp.returncode: return False, f'static audit failed for {n}: {cp.stdout[-1000:]}'
 return True, f'{len(expected)} static audit reports generated; semantic review still required'

def install_external(offline=False,refresh=False):
 cfg,expected=expected_external()
 if not refresh and lock_current(expected) and audits_current(expected):
  setg('external_skills','PASS','managed skills verified by whole-tree lock and static audit reports'); return
 if not refresh:
  repaired,q=restore_reviewed_external_from_git(expected)
  if repaired:
   setg('external_skills','PASS','drift repaired from exact committed reviewed skill lock; prior working copy quarantined')
   return
 if offline:
  setg('external_skills','BLOCKED','offline and no current reviewed external skill state can be restored'); return
 if not shutil.which('npx'):
  setg('external_skills','BLOCKED','npx required for initial/explicit upstream skill resolution'); return
 q=quarantine_existing(expected)
 inst=cfg['installer']; pkg=f"{inst['package']}@{inst['version']}"
 try:
  for src in cfg['sources']:
   if src.get('install')!='required': continue
   # Windows CreateProcess needs the resolved npx.cmd launcher, not bare npx.
   source_spec=src['repository']+(('#'+src['ref']) if src.get('ref') else '')
   cmd=[shutil.which('npx'),'--yes',pkg,'add',source_spec,'--agent','universal']
   for n in src['skills']: cmd += ['--skill',n]
   cmd += ['--yes','--copy']
   cp=run(cmd,check=False,env={'DO_NOT_TRACK':'1','DISABLE_TELEMETRY':'1'})
   if cp.returncode: raise RuntimeError(cp.stdout[-3000:])
  missing=[n for n in expected if not (SKILLS/n/'SKILL.md').exists()]
  if missing: raise RuntimeError('missing after install: '+', '.join(missing))
  ok,msg=run_static_audits(expected)
  if not ok: raise RuntimeError(msg)
  lock={'schema_version':2,'status':'RESOLVED','resolved_at':now(),'installer_spec':inst,'sources':[{'repository':s['repository'],'ref':s.get('ref'),'declared_license':s.get('license'),'skills':s['skills']} for s in cfg['sources'] if s.get('install')=='required'],'skill_tree_sha256':{n:treehash(SKILLS/n) for n in expected},'static_audit_reports':'08_TOOLCHAIN/SKILL_AUDITS/*.json'}
  save(LOCK,lock)
  setg('external_skills','PASS',f'{len(expected)} external skills installed into canonical .agents/skills, statically audited, and whole-tree locked')
  setg('skill_supply_chain_review','NOT_RUN','new/changed external skill lock requires semantic review')
 except Exception as e:
  restore_quarantine(q,expected); setg('external_skills','BLOCKED',str(e)); return

def credential_policy_check(root=ROOT):
 """Validate secret-storage policy without reading/logging legitimate local secret values."""
 gi=(root/'.gitignore').read_text(errors='ignore') if (root/'.gitignore').exists() else ''
 problems=[]
 if '.env.local' not in gi: problems.append('.env.local is not gitignored')
 if (root/'.git').exists():
  cp=subprocess.run(['git','ls-files','--error-unmatch','.env.local'],cwd=root,text=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  if cp.returncode==0: problems.append('.env.local is tracked by Git')
 ex=root/'.env.example'
 if ex.exists():
  for i,line in enumerate(ex.read_text(errors='ignore').splitlines(),1):
   m=re.match(r'^([A-Z][A-Z0-9_]*)=(.*)$',line.strip())
   if not m: continue
   val=m.group(2).strip()
   if val and not re.search(r'(^your_|placeholder|example|changeme|<.*>|^$)',val,re.I): problems.append(f'.env.example line {i} contains a non-placeholder value')
 return (not problems, '; '.join(problems) if problems else 'local secret file is ignored/untracked; local values intentionally not inspected')

def initialize(rid,offline=False,refresh_external=False,runtime_id=None):
 env_local=ROOT/'.env.local'
 if not env_local.exists(): env_local.write_text('# Local secrets only. DO NOT COMMIT. Add only credentials for deliberately enabled integrations.\n')
 run([sys.executable,'scripts/sync_derived_docs.py'],check=False)
 cp=run([sys.executable,'scripts/validate_repo.py'],check=False); setg('repository_structure','PASS' if cp.returncode==0 else 'FAIL',cp.stdout[-2000:])
 if not (ROOT/'.git').exists(): run(['git','init'])
 setg('git','PASS','Git repository present')
 bundled=list(SKILLS.glob('*/SKILL.md')); setg('canonical_skills','PASS' if bundled else 'FAIL',f'{len(bundled)} skills currently present under canonical root')
 ok,msg=credential_policy_check(); setg('credential_policy','PASS' if ok else 'FAIL',msg)
 install_external(offline,refresh_external)
 cp=run([sys.executable,'scripts/check_free_tools.py'],check=False); setg('free_tool_probe','PASS' if cp.returncode==0 else 'FAIL',cp.stdout[-2000:])
 adapter=run([sys.executable,'scripts/sync_runtime_adapters.py','--runtime',runtime_id or rid.split('::')[-1]],check=False)
 if adapter.returncode:
  raise SystemExit('LOCAL ADAPTER GENERATION BLOCKED: '+adapter.stdout[-2000:])
 tests=[run([sys.executable,'scripts/validate_repo.py'],check=False),run([sys.executable,'-m','unittest','discover','-s','tests','-v'],check=False),run([sys.executable,'scripts/disposable_pipeline_test.py'],check=False)]
 ok=all(c.returncode==0 for c in tests); setg('local_tests','PASS' if ok else 'FAIL','portable static/unit/disposable tests '+('passed' if ok else 'failed'))
 x,_=runtime_entry(rid); save(RUNTIMES,x); print('Local initialization complete; runtime direct-evidence gates may remain.')

def current_lock_digest(): return hashlib.sha256(LOCK.read_bytes()).hexdigest() if LOCK.exists() else ''

def semantic_review_can_pass():
 _,expected=expected_external(); return lock_current(expected) and audits_current(expected)

def finalize(rid):
 if (ROOT/'08_TOOLCHAIN/TEAM_POLICY.json').exists() and not authorized_global_branch():
  raise SystemExit('GLOBAL FINALIZE requires an authorized integration owner on main or an infrastructure PR branch; teammates use team_setup.py')
 s=load(STATUS); x,r=runtime_entry(rid); lock_sha=current_lock_digest()
 review=s['checks'].get('skill_supply_chain_review',{})
 review_current=review.get('status')=='PASS' and lock_sha and f'skill_lock_sha256={lock_sha}' in review.get('evidence','')
 all_global=all(s['checks'].get(k,{}).get('status')=='PASS' for k in GLOBAL)
 all_runtime=all(r['checks'].get(k,{}).get('status')=='PASS' for k in RUNTIME)
 mode_ok=r.get('mode') in {'FULL_NATIVE','FULL_EMULATED'}
 if s.get('project_status')=='READY_FOR_GAME_IDEA' and r.get('status')=='READY' and all_global and all_runtime and mode_ok and review_current:
  from validate_initialization_studio import validate,RECEIPT
  live_errors=validate(RECEIPT,ROOT,'full',rid)
  if live_errors:raise SystemExit('NOT READY: local Studio preflight missing or stale: '+'; '.join(live_errors))
  from validate_model_policy import validate as validate_models,receipt_path as model_receipt_path
  model_errors=validate_models(model_receipt_path(rid),ROOT,rid)
  if model_errors:raise SystemExit('NOT READY: local model preflight missing or stale: '+'; '.join(model_errors))
  from workstation_preflight import current_preflight
  if not current_preflight(ROOT):raise SystemExit('NOT READY: native developer preflight stale/missing')
  print('PASS: project and runtime already READY; no files or commits changed'); return
 missing=[k for k in GLOBAL if s['checks'].get(k,{}).get('status')!='PASS']+[f'runtime:{k}' for k in RUNTIME if r['checks'].get(k,{}).get('status')!='PASS']
 if not review_current: missing.append('skill_supply_chain_review=STALE_FOR_CURRENT_LOCK')
 if not mode_ok: missing.append('runtime:mode')
 if missing: print('NOT READY:',', '.join(sorted(set(missing)))); raise SystemExit(2)
 from validate_initialization_studio import validate as validate_studio,RECEIPT
 from validate_model_policy import validate as validate_models, receipt_path as model_receipt_path
 live_errors=validate_studio(RECEIPT,ROOT,'full',rid)
 model_errors=validate_models(model_receipt_path(rid),ROOT,rid)
 if live_errors or model_errors:
  raise SystemExit('NOT READY: real evidence stale/missing: '+'; '.join(live_errors+model_errors))
 from workstation_preflight import current_preflight
 if not current_preflight(ROOT):raise SystemExit('NOT READY: native developer preflight stale/missing')
 s['project_status']='READY_FOR_GAME_IDEA'; s['last_updated']=now(); save(STATUS,s); r['status']='READY'; r['last_updated']=now(); save(RUNTIMES,x)
 (ROOT/'06_PROJECT_STATE/CURRENT_STATE.md').write_text('# CURRENT STATE\n\n- Project Status: **SHARED SKILLS/BOOTSTRAP READY**\n- Example locally validated runtime: see ignored `.local/RUNTIME_VALIDATIONS.json` on this workstation\n- Active Changeset: none\n- Current Pipeline Stage: ready for streamlined issue tasks\n- Next Action: use `python scripts/team.py idea` or `update`; use `team.py resume` for existing work\n')
 (ROOT/'06_PROJECT_STATE/NEXT_ACTION.md').write_text('# NEXT ACTION\n\nUse `python scripts/team.py idea --file ...` for a new game idea, `team.py update` for recurring work, or `team.py resume` for an existing issue. Do not process the real game idea during shared skill bootstrap itself.\n')
 # Stage only project bootstrap evidence, not the entire developer workspace.
 staged=run(['git','add','-A','--','.agents/skills','08_TOOLCHAIN/SKILL_LOCK.json','08_TOOLCHAIN/SKILL_AUDITS','06_PROJECT_STATE/INITIALIZATION_STATUS.json','06_PROJECT_STATE/CURRENT_STATE.md','06_PROJECT_STATE/NEXT_ACTION.md'],check=False)
 if staged.returncode:
  raise SystemExit('NOT FINALIZED: could not stage shared bootstrap checkpoint: '+staged.stdout[-1000:])
 d=run(['git','diff','--cached','--quiet'],check=False)
 if d.returncode not in {0,1}:raise SystemExit('NOT FINALIZED: could not inspect staged bootstrap checkpoint: '+d.stdout[-1000:])
 if d.returncode:
  commit=run(['git','commit','-m',f'Validate portable project runtime: {rid}'],check=False)
  if commit.returncode:raise SystemExit('NOT FINALIZED: Git checkpoint commit failed: '+commit.stdout[-1000:])
 print('PASS: shared bootstrap ready for streamlined tasks; runtime',rid,'READY',r['mode'])


def finalize_local(rid):
 """Finalize workstation/runtime evidence without changing any tracked project state."""
 shared=load(STATUS)
 x,r=runtime_entry(rid)
 mode=r.get('mode')
 required=RUNTIME if mode in {'FULL_NATIVE','FULL_EMULATED'} else (RUNTIME-{'developer_toolchain','roblox_studio_bridge','rojo_live_sync','studio_disposable_test'})
 missing=[k for k in required if r['checks'].get(k,{}).get('status')!='PASS']
 if mode not in {'FULL_NATIVE','FULL_EMULATED','PLANNING_ONLY','READ_ONLY'}:missing.append('validated runtime mode')
 if missing: raise SystemExit('LOCAL RUNTIME NOT READY: '+', '.join(sorted(missing)))
 if mode in {'FULL_NATIVE','FULL_EMULATED'}:
  from validate_model_policy import validate as validate_models,receipt_path as model_receipt_path
  model_errors=validate_models(model_receipt_path(rid),ROOT,rid)
  if model_errors:raise SystemExit('LOCAL RUNTIME NOT READY: model evidence stale/incomplete: '+'; '.join(model_errors))
  from validate_initialization_studio import validate,RECEIPT
  live_errors=validate(RECEIPT,ROOT,'full',rid)
  if live_errors:raise SystemExit('LOCAL RUNTIME NOT READY: local Studio preflight stale/incomplete: '+'; '.join(live_errors))
  from workstation_preflight import current_preflight
  if not current_preflight(ROOT):raise SystemExit('LOCAL RUNTIME NOT READY: native developer preflight stale/missing')
  _,expected=expected_external()
  if shared.get('project_status')!='READY_FOR_GAME_IDEA' or not lock_current(expected) or not audits_current(expected):
   r['status']='VALIDATED_RUNTIME_SHARED_BOOTSTRAP_PENDING'
  else:r['status']='READY'
 else:
  from validate_model_policy import validate as validate_models,receipt_path as model_receipt_path
  model_errors=validate_models(model_receipt_path(rid),ROOT,rid,require_delegates=False)
  if model_errors:raise SystemExit('LOCAL RUNTIME NOT READY: planning/read-only model evidence missing: '+'; '.join(model_errors))
  r['status']='VALIDATED_'+mode
 # Prevent no-op timestamp churn in personal state too.
 if RUNTIMES.exists():
  previous=load(RUNTIMES).get('runtimes',{}).get(rid,{})
  if previous.get('status')==r['status'] and previous.get('checks')==r['checks'] and previous.get('mode')==mode:
   print('LOCAL RUNTIME ALREADY VALIDATED:',rid,r['status']); return
 r['last_updated']=now();save(RUNTIMES,x)
 print('LOCAL RUNTIME:',rid,r['status'],'(personal ignored state; shared main unchanged)')

def require_correct_repository():
 """Prevent a template or wrong checkout from changing shared project state."""
 policy=load(ROOT/'08_TOOLCHAIN/TEAM_POLICY.json')
 if policy.get('template_unconfigured') is not False:
  raise SystemExit('BLOCKED: reusable template is unconfigured; run scripts/prepare_new_game.py from extracted bootstrap first')
 actual=run(['git','remote','get-url','origin'],check=False)
 if actual.returncode:
  raise SystemExit('BLOCKED: no origin remote. Clone the intended NEW GitHub repository before initializing')
 def normalize(u):
  u=u.strip()
  if u.startswith('git@github.com:'):u='https://github.com/'+u.split(':',1)[1]
  if u.startswith('ssh://git@github.com/'):u='https://github.com/'+u.split('ssh://git@github.com/',1)[1]
  return u.removesuffix('.git').rstrip('/').lower()
 if normalize(actual.stdout)!=normalize(policy['remote_url']):
  raise SystemExit('BLOCKED: origin differs from configured TEAM_POLICY.json; inspect repository URL, no files changed')

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--runtime',default='generic'); ap.add_argument('--offline',action='store_true'); ap.add_argument('--refresh-external-skills',action='store_true'); ap.add_argument('--record-global',nargs=2,metavar=('GATE','STATUS')); ap.add_argument('--record-runtime',nargs=2,metavar=('GATE','STATUS')); ap.add_argument('--mode'); ap.add_argument('--evidence',default=''); ap.add_argument('--finalize',action='store_true'); ap.add_argument('--finalize-local',action='store_true'); ap.add_argument('--status',action='store_true'); ap.add_argument('--join-team',action='store_true',help='join a shared repo locally without modifying global state'); ap.add_argument('--developer',default=''); ap.add_argument('--initialize-global',action='store_true',help='maintainer-only shared project bootstrap/finalization on main'); a=ap.parse_args()
 runtime_key=f'{a.developer}::{a.runtime}' if a.developer else a.runtime
 if a.status: print(STATUS.read_text()); print((RUNTIMES if RUNTIMES.exists() else RUNTIME_TEMPLATE).read_text()); return
 require_correct_repository()
 if a.join_team:
  if not a.developer: raise SystemExit('--developer GitHub-username required for --join-team')
  from team_setup import load_profile, check
  load_profile(a.developer,a.runtime)
  run([sys.executable,'scripts/sync_runtime_adapters.py','--runtime',a.runtime],check=False)
  x,_=runtime_entry(runtime_key); save(RUNTIMES,x)
  issues=check()
  from bootstrap_dev_tools import probe,EXPECTED
  tools=probe()
  if not all(tools[n]['version_verified'] for n in EXPECTED): issues.append('pinned local Rojo/StyLua/Selene incomplete; see 02_TECHNICAL/DEPENDENCY_BOOTSTRAP.md')
  print('TEAM JOIN:', 'PARTIAL: '+'; '.join(issues) if issues else 'CORE VERIFIED (live runtime and Studio gates remain local)')
  return
 if a.record_global:
  if (ROOT/'08_TOOLCHAIN/TEAM_POLICY.json').exists() and (not a.initialize_global or not authorized_global_branch()):
   raise SystemExit('global gate recording requires --initialize-global on main by authorized integrator')
  g,s=a.record_global
  if g not in GLOBAL: raise SystemExit('unknown global gate')
  if g=='skill_supply_chain_review' and s=='PASS':
   if not semantic_review_can_pass(): raise SystemExit('cannot record semantic review PASS: current skill lock/audit evidence is incomplete or drifted')
   ev=a.evidence+f'; skill_lock_sha256={current_lock_digest()}'
  else: ev=a.evidence
  setg(g,s,ev); return
 if a.record_runtime:
  g,s=a.record_runtime
  if g not in RUNTIME: raise SystemExit('unknown runtime gate')
  if g=='model_policy_validation' and s=='PASS':
   from validate_model_policy import validate,receipt_path as model_receipt_path
   _,entry=runtime_entry(runtime_key)
   prospective=a.mode or entry.get('mode')
   failures=validate(model_receipt_path(runtime_key),ROOT,runtime_key,require_delegates=prospective not in {'PLANNING_ONLY','READ_ONLY'})
   if failures:raise SystemExit('BLOCKED: model policy cannot PASS: '+'; '.join(failures))
  if g=='role_execution_validation' and s=='PASS' and (a.mode or runtime_entry(runtime_key)[1].get('mode')) in {'FULL_NATIVE','FULL_EMULATED'}:
   from validate_model_policy import validate,receipt_path as model_receipt_path
   failures=validate(model_receipt_path(runtime_key),ROOT,runtime_key)
   if failures:raise SystemExit('BLOCKED: role execution requires real delegated model traces: '+'; '.join(failures))
  if g=='developer_toolchain' and s=='PASS':
   from bootstrap_dev_tools import probe,EXPECTED
   inspected=probe()
   from workstation_preflight import current_preflight
   if not all(inspected[n]['version_verified'] for n in EXPECTED) or not current_preflight():
    raise SystemExit('BLOCKED: cannot record developer_toolchain PASS until pinned Rojo, StyLua, Selene AND a current native Rojo build artifact are verified locally')
  if g in {'roblox_studio_bridge','rojo_live_sync','studio_disposable_test'} and s=='PASS':
   from validate_initialization_studio import validate,RECEIPT
   stage={'roblox_studio_bridge':'mcp','rojo_live_sync':'rojo','studio_disposable_test':'full'}[g]
   failures=validate(RECEIPT,ROOT,stage,runtime_key)
   if failures:raise SystemExit('BLOCKED: cannot mark '+g+' PASS: '+'; '.join(failures))
  setr(runtime_key,g,s,a.evidence,a.mode); return
 if a.finalize_local: finalize_local(runtime_key); return
 if a.finalize:
  if (ROOT/'08_TOOLCHAIN/TEAM_POLICY.json').exists() and not a.initialize_global: raise SystemExit('Team global finalization requires --initialize-global on main or an infrastructure PR branch; use --join-team otherwise')
  finalize(runtime_key); return
 if (ROOT/'08_TOOLCHAIN/TEAM_POLICY.json').exists():
  if not a.initialize_global: raise SystemExit('Shared repository: use --join-team --developer NAME to join; integrator uses --initialize-global on main')
  if not authorized_global_branch(): raise SystemExit('--initialize-global requires main or an infrastructure PR branch and authorized human maintainer')
 initialize(runtime_key,a.offline,a.refresh_external_skills,a.runtime)
if __name__=='__main__': main()
