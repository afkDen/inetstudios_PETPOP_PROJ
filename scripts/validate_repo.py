#!/usr/bin/env python3
from pathlib import Path
import json,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
REQ=['AGENTS.md','README.md','START_HERE.md','INITIALIZE_PROJECT.md','GAME_DESIGN.md','06_PROJECT_STATE/INITIALIZATION_STATUS.json','06_PROJECT_STATE/RUNTIME_VALIDATIONS.json','08_TOOLCHAIN/SKILL_REGISTRY.json','08_TOOLCHAIN/ROLE_CONTRACTS/roles.json','08_TOOLCHAIN/CAPABILITY_CONTRACT.json','08_TOOLCHAIN/RUNTIME_PROFILES.json','08_TOOLCHAIN/TEAM_MODEL_POLICY.json','08_TOOLCHAIN/MODEL_POLICY_SETUP.md','08_TOOLCHAIN/WORKFLOW_PROFILE.json','08_TOOLCHAIN/EXTERNAL_SKILLS.json','08_TOOLCHAIN/SKILL_AUDITS/README.md','scripts/team.py','scripts/streamlined_task.py','scripts/validate_streamlined_task.py','scripts/validate_ci_task.py','scripts/sync_runtime_adapters.py','scripts/sync_derived_docs.py','scripts/render_role_packet.py','scripts/validate_runtime.py','scripts/model_policy.py','scripts/prepare_codex_high.py','scripts/validate_model_policy.py','scripts/create_model_preflight.py','templates/TASK_TEMPLATE.md','templates/WORK_STATE_V8_TEMPLATE.md','templates/TASK_EVIDENCE_TEMPLATE.json','templates/MODEL_PREFLIGHT_TEMPLATE.json','TEAM_PROTOCOL.md','TEAM_ONBOARDING.md','08_TOOLCHAIN/TEAM_POLICY.json','scripts/validate_team.py','scripts/team_setup.py','scripts/submit_proposal.py','scripts/promote_proposal.py','scripts/team_workflow.py','default.project.json','rokit.toml','TEAM_WORKFLOW.md','02_TECHNICAL/LIVE_STUDIO_DELIVERY.md','08_TOOLCHAIN/QUALITY_SOURCE_CANDIDATES.md','scripts/validate_studio_delivery.py','scripts/prepare_studio_delivery.py','templates/STUDIO_DELIVERY_TEMPLATE.json','templates/rojo-world-opt-in.project.json','08_TOOLCHAIN/BLOXMAPS_INTEGRATION.json','08_TOOLCHAIN/BLOXMAPS_SETUP.md','scripts/bloxmaps_adapter.py','GLOSSARY.md','08_TOOLCHAIN/ENGINEERING_REASONING_V8_4.md','08_TOOLCHAIN/THIRD_PARTY_NOTICES.md','08_TOOLCHAIN/AGENT_ORCHESTRATION_V8_4.md','08_TOOLCHAIN/SCOPE_EVOLUTION_V8_5.md','MIGRATION_V8_4_TO_V8_5.md']

def fail(m): print('FAIL:',m); return 1
def valid_skill(p):
 t=p.read_text(encoding='utf-8',errors='replace') if p.exists() else ''
 return t.startswith('---') and re.search(r'(?m)^name:\s*\S+',t) and re.search(r'(?m)^description:\s*\S+',t)

def main():
 e=0
 for r in REQ:
  if not (ROOT/r).exists(): e+=fail('missing '+r)
 ag=(ROOT/'AGENTS.md').read_text(encoding='utf-8')
 for s in ['canonical top-level instruction file','.agents/skills/<skill-name>/SKILL.md','ROLE_CONTRACTS','Runtime-specific']:
  if s not in ag: e+=fail('AGENTS.md missing master-contract concept: '+s)
 root=ROOT/'.agents/skills'
 if not root.exists(): e+=fail('missing .agents/skills')
 reg=json.loads((ROOT/'08_TOOLCHAIN/SKILL_REGISTRY.json').read_text()); regskills={x['name']:x for x in reg.get('skills',[])}
 if reg.get('canonical_root')!='.agents/skills': e+=fail('skill registry canonical root mismatch')
 if len(regskills)!=len(reg.get('skills',[])): e+=fail('duplicate skill names in registry')
 # v8.4 selective-adaptation provenance and usage-economy invariants.
 sha40=re.compile(r'^[0-9a-f]{40}$')
 forbidden_reasoning={'tdd','to-spec','to-tickets','implement','implement-spec','triage','wayfinder','ask-matt','setup-matt-pocock-skills'}
 leaked=forbidden_reasoning & set(regskills)
 if leaked: e+=fail(f'v8.4 excluded upstream workflow/TDD skills are registered: {sorted(leaked)}')
 matt_adaptations=[v for v in regskills.values() if v.get('source')=='mattpocock/skills']
 if not matt_adaptations: e+=fail('v8.4 Matt Pocock reasoning adaptations are missing')
 for item in matt_adaptations:
  if item.get('origin')!='project' or item.get('state')!='bundled' or item.get('trust')!='project-authored-adaptation':
   e+=fail(f"Matt adaptation is not a bundled project adaptation: {item.get('name')}")
  if item.get('license')!='MIT': e+=fail(f"Matt adaptation license mismatch: {item.get('name')}")
  if not sha40.fullmatch(str(item.get('source_commit',''))): e+=fail(f"Matt adaptation source commit is not immutable: {item.get('name')}")
  if not sha40.fullmatch(str(item.get('upstream_blob_sha',''))): e+=fail(f"Matt adaptation upstream blob provenance missing: {item.get('name')}")
 # v8.5 revisioned-scope invariants.
 try:
  profile=json.loads((ROOT/'08_TOOLCHAIN/WORKFLOW_PROFILE.json').read_text())
  if profile.get('workflow_id')!='streamlined-v8.5': e+=fail('workflow profile must be streamlined-v8.5')
  flow=profile.get('normal_flow',{})
  if flow.get('require_scope_amendment_approval_after_initial_approval') is not True: e+=fail('v8.5 must require approval for post-approval scope amendments')
  if flow.get('preserve_prior_scope_approvals') is not True: e+=fail('v8.5 must preserve prior scope approval history')
 except (OSError,ValueError,TypeError): e+=fail('v8.5 workflow profile is unreadable')
 if (ROOT/'VERSION').read_text().strip()!='v8.5-scope-evolution': e+=fail('VERSION must identify v8.5-scope-evolution')
 try:
  studio_template=json.loads((ROOT/'templates/STUDIO_DELIVERY_TEMPLATE.json').read_text())
  quality_template=json.loads((ROOT/'templates/QUALITY_EVIDENCE_TEMPLATE.json').read_text())
  task_evidence=json.loads((ROOT/'templates/TASK_EVIDENCE_TEMPLATE.json').read_text())
  if studio_template.get('schema_version')!=2 or 'scope_revision' not in studio_template: e+=fail('v8.5 Studio receipt template must be scope-aware schema 2')
  if quality_template.get('schema_version')!=2 or 'scope_revision' not in quality_template: e+=fail('v8.5 quality evidence template must be scope-aware schema 2')
  if task_evidence.get('schema_version')!=2 or not {'scope_revision','required_scope_revision','scope_attestation'} <= set(task_evidence): e+=fail('v8.5 task evidence template must bind scope revision')
 except (OSError,ValueError,TypeError): e+=fail('v8.5 evidence templates are unreadable')
 ga=(ROOT/'.gitattributes').read_text(errors='ignore')
 if '04_CHANGESETS/**/SCOPE_AMENDMENTS/** -text' not in ga: e+=fail('scope amendments and references must be byte-preserved with -text')
 for token in ('create_scope_amendment','approve_scope_amendment','attest_evidence_scope'):
  if token not in (ROOT/'scripts/streamlined_task.py').read_text(): e+=fail('v8.5 scope API missing: '+token)

 sysdbg=regskills.get('systematic-debugging',{})
 if sysdbg.get('origin')!='project' or sysdbg.get('state')!='bundled': e+=fail('systematic-debugging must be bundled in v8.4')
 adapted_sources=sysdbg.get('adapted_sources',[])
 if len(adapted_sources)<2: e+=fail('systematic-debugging must preserve both reviewed adaptation sources')
 for source in adapted_sources:
  if not sha40.fullmatch(str(source.get('commit',''))): e+=fail('systematic-debugging adapted source commit is not immutable')
  if not sha40.fullmatch(str(source.get('blob_sha',''))): e+=fail('systematic-debugging adapted source blob provenance missing')
 for p in root.iterdir() if root.exists() else []:
  if p.is_dir():
   if p.name not in regskills: e+=fail(f'unregistered skill directory: {p.name}')
   if not (p/'SKILL.md').exists(): e+=fail(f'non-skill directory in canonical skill root: {p.name}')
   elif not valid_skill(p/'SKILL.md'): e+=fail(f'invalid skill {p.name}')
   if list(p.rglob('AGENTS.md')): e+=fail(f'AGENTS.md must not exist inside skill {p.name}')
 if (root/'.external_install_manifest.json').exists(): e+=fail('legacy external install manifest pollutes canonical skill root')
 if (ROOT/'08_TOOLCHAIN/FALLBACK_SKILLS').exists(): e+=fail('deprecated fallback skill tree still exists')
 ext=json.loads((ROOT/'08_TOOLCHAIN/EXTERNAL_SKILLS.json').read_text()); inst=ext.get('installer',{})
 if inst.get('agent')!='universal' or inst.get('canonical_destination')!='.agents/skills' or inst.get('scope')!='project' or inst.get('method')!='copy': e+=fail('external installer is not canonical universal project copy')
 expected_external={n for src in ext['sources'] if src.get('install')=='required' for n in src['skills']}
 registry_external={n for n,v in regskills.items() if v.get('origin')=='external'}
 if expected_external!=registry_external: e+=fail(f'external skill config/registry mismatch: config_only={sorted(expected_external-registry_external)} registry_only={sorted(registry_external-expected_external)}')
 lock_path=ROOT/'08_TOOLCHAIN/SKILL_LOCK.json'
 if lock_path.exists():
  from initialize_project import treehash
  lock=json.loads(lock_path.read_text())
  source_by_name={n:s for s in lock.get('sources',[]) for n in s.get('skills',[])}
  hashes=lock.get('skill_tree_sha256',{})
  if set(hashes)!=expected_external or set(source_by_name)!=expected_external:e+=fail('external skill lock/config mismatch')
  for n in expected_external & set(regskills) & set(hashes) & set(source_by_name):
   item=regskills[n]; source=source_by_name[n]
   if (item.get('state')!='locked' or item.get('trust')!='semantic-review-approved' or
       item.get('source')!=source.get('repository') or item.get('license')!=source.get('declared_license') or
       item.get('source_commit')!=source.get('verified_source_commit') or item.get('tree_sha256')!=hashes[n]):
    e+=fail(f'external skill registry/lock provenance mismatch: {n}')
   if (root/n/'SKILL.md').exists() and treehash(root/n)!=hashes[n]:e+=fail(f'external skill tree drift: {n}')
 bundled={p.parent.name for p in root.glob('*/SKILL.md')}
 for n in bundled:
  if regskills[n].get('origin')=='project' and regskills[n].get('state')!='bundled': e+=fail(f'project skill {n} is present but registry state is not bundled')
 from model_policy import validate_policy_structure,ModelPolicyError
 try:validate_policy_structure(ROOT)
 except (ModelPolicyError,KeyError,ValueError) as exc:e+=fail('invalid team model policy: '+str(exc))
 caps=set(json.loads((ROOT/'08_TOOLCHAIN/CAPABILITY_CONTRACT.json').read_text())['capabilities'])
 roles=json.loads((ROOT/'08_TOOLCHAIN/ROLE_CONTRACTS/roles.json').read_text())['roles']; allowed={'FAST','BALANCED','DEEP','REVIEW','REVIEW_DEEP','TOOL_RELIABLE'}
 if len(roles)<10: e+=fail('too few canonical roles')
 for r in roles:
  if r['model_class'] not in allowed: e+=fail(f"invalid model class {r['id']}")
  missing_caps=set(r.get('required_capabilities',[]))-caps
  if missing_caps:e+=fail(f"role {r['id']} requests unknown capabilities: {sorted(missing_caps)}")
  blob=json.dumps(r).lower()
  if any(x in blob for x in ['gemini-','claude sonnet','gpt-','antigravity']): e+=fail(f"provider/model lock in canonical role {r['id']}")
  missing=set(r.get('required_skills',[]))-set(regskills)
  if missing: e+=fail(f"role {r['id']} references unregistered skills: {sorted(missing)}")
  pp=ROOT/'08_TOOLCHAIN/ROLE_CONTRACTS'/r['prompt']
  if not pp.exists(): e+=fail(f"missing role prompt {r['id']}")
 init=json.loads((ROOT/'06_PROJECT_STATE/INITIALIZATION_STATUS.json').read_text())
 if 'project_status' not in init or 'environment_status' in init: e+=fail('project initialization status not runtime-neutral')
 rv=json.loads((ROOT/'06_PROJECT_STATE/RUNTIME_VALIDATIONS.json').read_text())
 if 'runtimes' not in rv: e+=fail('runtime validation registry malformed')
 profiles=json.loads((ROOT/'08_TOOLCHAIN/RUNTIME_PROFILES.json').read_text())
 if profiles.get('fallback_profile')!='generic': e+=fail('missing generic future-runtime fallback')
 for name,p in profiles.get('profiles',{}).items():
  if p.get('skill_source')!='.agents/skills': e+=fail(f'runtime {name} does not use canonical skill source')
  if not p.get('requires_direct_validation'): e+=fail(f'runtime {name} must require direct validation')
  if 'default_mode' in p: e+=fail(f'runtime {name} uses deprecated default_mode instead of non-authoritative mode_hint')
 cp=subprocess.run([__import__('sys').executable,'scripts/sync_derived_docs.py','--check'],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if cp.returncode: e+=fail(cp.stdout.strip() or 'derived documentation stale')
 gi=(ROOT/'.gitignore').read_text()
 for x in ['.env.local','.agents/agents/','.claude/skills/','.codex/agents/','.codex/config.toml','.gemini/agents/','.cursor/agents/','08_TOOLCHAIN/SKILL_QUARANTINE/']:
  if x not in gi: e+=fail('.gitignore missing '+x)
 # Current-state docs must not contain known superseded architecture claims.
 current_docs=[ROOT/'06_PROJECT_STATE/CURRENT_STATE.md',ROOT/'06_PROJECT_STATE/FINAL_SCAFFOLD_REVIEW.md',ROOT/'08_TOOLCHAIN/INITIALIZATION_PROTOCOL.md',ROOT/'08_TOOLCHAIN/TOOLCHAIN_MANIFEST.md']
 stale=['custom Antigravity agents','fallback adapters retained outside','targets the Antigravity agent','real Antigravity workstation']
 for p in current_docs:
  text=p.read_text(errors='ignore')
  for s in stale:
   if s.lower() in text.lower(): e+=fail(f'superseded claim in current doc {p.relative_to(ROOT)}: {s}')
 # Historical Antigravity directive is allowed only as raw/history material.
 cp=subprocess.run(['git','ls-files','*SKILL.md'],cwd=ROOT,text=True,stdout=subprocess.PIPE,check=False)
 if cp.returncode==0:
  tracked=[s for s in cp.stdout.splitlines() if s]
  bad=[s for s in tracked if not s.startswith('.agents/skills/')]
  if bad: e+=fail(f'tracked canonical SKILL.md outside .agents/skills: {bad}')
 cp=subprocess.run([__import__('sys').executable,'scripts/validate_team.py'],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if cp.returncode: e+=fail(cp.stdout.strip() or 'team validation failed')
 if e: raise SystemExit(1)
 print(f"PASS: portable repository contract; {len(bundled)} canonical skills currently present; {len(regskills)} registered skills; {len(roles)} roles")
if __name__=='__main__': main()
