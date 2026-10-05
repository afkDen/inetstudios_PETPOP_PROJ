\
import json,re,unittest,subprocess,sys,tempfile,shutil,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Contract(unittest.TestCase):
 def test_agents_is_master(self):
  t=(ROOT/'AGENTS.md').read_text(); self.assertIn('canonical top-level instruction file',t); self.assertIn('.agents/skills/<skill-name>/SKILL.md',t); self.assertIn('ROLE_CONTRACTS',t)
 def test_single_canonical_skill_root(self):
  self.assertFalse((ROOT/'08_TOOLCHAIN/FALLBACK_SKILLS').exists()); self.assertFalse((ROOT/'.agents/skills/.external_install_manifest.json').exists())
  for p in (ROOT/'.agents/skills').iterdir():
   if p.is_dir(): self.assertTrue((p/'SKILL.md').exists(),p.name); self.assertFalse(list(p.rglob('AGENTS.md')))
 def test_external_installs_universal(self):
  c=json.loads((ROOT/'08_TOOLCHAIN/EXTERNAL_SKILLS.json').read_text()); self.assertEqual(c['installer']['agent'],'universal'); self.assertEqual(c['installer']['canonical_destination'],'.agents/skills')
 def test_external_skill_policy_and_license_material_are_explicit(self):
  c=json.loads((ROOT/'08_TOOLCHAIN/EXTERNAL_SKILLS.json').read_text()); policy=ROOT/c['execution_policy']; self.assertTrue(policy.is_file()); self.assertIn(c['execution_policy'],(ROOT/'AGENTS.md').read_text())
  pt=policy.read_text();
  for token in ['not workflow authorities','not loosened merely to make the pipeline green','Production mutation','roblox-open-cloud','second sync bridge','not permission to copy']: self.assertIn(token,pt)
  for src in c['sources']:
   if src.get('install')!='required': continue
   lp=ROOT/src['license_file']; self.assertTrue(lp.is_file(),src['name']); lic=lp.read_text(errors='replace')
   if src['license']=='MIT': self.assertIn('MIT License',lic,src['name'])
   if src['license']=='Apache-2.0': self.assertIn('Apache License',lic,src['name']); self.assertIn('Version 2.0',lic,src['name'])
   if src.get('notice_file'): self.assertTrue((ROOT/src['notice_file']).is_file(),src['name'])
  owned=set(json.loads((ROOT/'08_TOOLCHAIN/TEAM_POLICY.json').read_text())['integrator_owned']); self.assertIn('08_TOOLCHAIN/EXTERNAL_SKILL_EXECUTION_POLICY.md',owned); self.assertIn('08_TOOLCHAIN/THIRD_PARTY_LICENSES',owned)
 def test_skill_registry(self):
  r=json.loads((ROOT/'08_TOOLCHAIN/SKILL_REGISTRY.json').read_text()); self.assertEqual(r['canonical_root'],'.agents/skills'); self.assertEqual(len({x['name'] for x in r['skills']}),len(r['skills'])); self.assertGreaterEqual(len(r['skills']),55)
 def test_external_registry_exact_match(self):
  r=json.loads((ROOT/'08_TOOLCHAIN/SKILL_REGISTRY.json').read_text()); c=json.loads((ROOT/'08_TOOLCHAIN/EXTERNAL_SKILLS.json').read_text())
  self.assertEqual({x['name'] for x in r['skills'] if x['origin']=='external'},{n for s in c['sources'] if s['install']=='required' for n in s['skills']})
 def test_roles_are_provider_neutral(self):
  roles=json.loads((ROOT/'08_TOOLCHAIN/ROLE_CONTRACTS/roles.json').read_text())['roles']; self.assertEqual(len(roles),10); self.assertFalse({'art-director','ui-implementation-worker','visual-reviewer','gameplay-reviewer','world-builder','asset-worker','security-reviewer'} & {r['id'] for r in roles})
  blob=json.dumps(roles).lower(); self.assertNotIn('gemini-',blob); self.assertNotIn('claude sonnet',blob); self.assertNotIn('gpt-',blob)
 def test_role_skills_are_registered(self):
  reg={x['name'] for x in json.loads((ROOT/'08_TOOLCHAIN/SKILL_REGISTRY.json').read_text())['skills']}; roles=json.loads((ROOT/'08_TOOLCHAIN/ROLE_CONTRACTS/roles.json').read_text())['roles']
  for r in roles: self.assertFalse(set(r['required_skills'])-reg,r['id'])
 def test_runtime_state_separate(self):
  s=json.loads((ROOT/'06_PROJECT_STATE/INITIALIZATION_STATUS.json').read_text()); self.assertIn('project_status',s); self.assertNotIn('environment_status',s); self.assertIn('runtimes',json.loads((ROOT/'06_PROJECT_STATE/RUNTIME_VALIDATIONS.json').read_text()))
 def test_generic_future_runtime(self):
  p=json.loads((ROOT/'08_TOOLCHAIN/RUNTIME_PROFILES.json').read_text()); self.assertEqual(p['fallback_profile'],'generic')
 def test_runtime_profiles_require_direct_validation(self):
  p=json.loads((ROOT/'08_TOOLCHAIN/RUNTIME_PROFILES.json').read_text())['profiles']
  for name,cfg in p.items(): self.assertTrue(cfg['requires_direct_validation'],name); self.assertNotIn('default_mode',cfg); self.assertIn('mode_hint',cfg)
 def test_adapter_tools_exist(self):
  for x in ['sync_runtime_adapters.py','sync_derived_docs.py','render_role_packet.py','validate_runtime.py']: self.assertTrue((ROOT/'scripts'/x).exists())
 def test_derived_routing_view_is_current(self):
  cp=subprocess.run([sys.executable,str(ROOT/'scripts/sync_derived_docs.py'),'--check'],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT); self.assertEqual(cp.returncode,0,cp.stdout)
 def test_role_packet(self):
  cp=subprocess.run([sys.executable,str(ROOT/'scripts/render_role_packet.py'),'--role','assurance-reviewer','--task','review test'],cwd=ROOT,text=True,stdout=subprocess.PIPE); self.assertEqual(cp.returncode,0); self.assertIn('Fresh context required: True',cp.stdout)
 def test_every_committed_skill_definition_is_under_canonical_root(self):
  # The reusable ZIP intentionally has no .git directory. Use Git when available,
  # otherwise audit the extracted filesystem without turning packaging into a failure.
  if (ROOT/'.git').exists():
   cp=subprocess.run(['git','ls-files','*SKILL.md'],cwd=ROOT,text=True,stdout=subprocess.PIPE,check=True); skills=[x for x in cp.stdout.splitlines() if x and (ROOT/x).exists()]
  else:
   skills=[p.relative_to(ROOT).as_posix() for p in (ROOT/'.agents/skills').rglob('SKILL.md')]
  self.assertTrue(skills); self.assertTrue(all(x.startswith('.agents/skills/') for x in skills),skills)
 def test_runtime_profiles_share_canonical_skill_source(self):
  cfg=json.loads((ROOT/'08_TOOLCHAIN/RUNTIME_PROFILES.json').read_text())
  for name,profile in cfg['profiles'].items(): self.assertEqual(profile['skill_source'],'.agents/skills',name)
 def test_master_contract_is_provider_model_neutral(self):
  text=(ROOT/'AGENTS.md').read_text().lower()
  for token in ['gemini-3','claude sonnet','gpt-5','gpt-6']: self.assertNotIn(token,text)
 def test_generated_runtime_paths_are_ignored(self):
  gi=(ROOT/'.gitignore').read_text()
  for path in ['.agents/agents/','.claude/skills/','.claude/agents/','.gemini/agents/','.cursor/agents/','.github/agents/']: self.assertIn(path,gi)
 def test_initializer_persists_new_runtime_entry(self):
  src=(ROOT/'scripts/initialize_project.py').read_text(); self.assertIn('x,_=runtime_entry(rid); save(RUNTIMES,x)',src)
 def test_initializer_uses_universal_not_antigravity(self):
  t=(ROOT/'scripts/initialize_project.py').read_text(); self.assertIn("'--agent','universal'",t); self.assertNotIn("--agent','antigravity",t)
 def test_initializer_runs_static_skill_audits_and_uses_toolchain_lock(self):
  t=(ROOT/'scripts/initialize_project.py').read_text(); self.assertIn('audit_skill_tree.py',t); self.assertIn("LOCK=ROOT/'08_TOOLCHAIN/SKILL_LOCK.json'",t); self.assertNotIn('.external_install_manifest.json',t)
 def test_normal_skill_drift_repairs_from_git_and_refresh_is_explicit(self):
  t=(ROOT/'scripts/initialize_project.py').read_text(); self.assertIn('restore_reviewed_external_from_git',t); self.assertIn('--refresh-external-skills',t); self.assertIn('refresh_external',t)
 def test_credential_policy_allows_real_local_secret_but_not_tracked_secret(self):
  spec=importlib.util.spec_from_file_location('initmod',ROOT/'scripts/initialize_project.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
  with tempfile.TemporaryDirectory() as td:
   r=Path(td); (r/'.gitignore').write_text('.env.local\n'); (r/'.env.example').write_text('TOKEN=your_token_here\n'); (r/'.env.local').write_text('TOKEN=real-secret-value\n'); subprocess.run(['git','init','-q'],cwd=r,check=True)
   ok,msg=m.credential_policy_check(r); self.assertTrue(ok,msg)
   subprocess.run(['git','add','-f','.env.local'],cwd=r,check=True); ok,msg=m.credential_policy_check(r); self.assertFalse(ok); self.assertIn('tracked',msg)
 def test_initialization_doc_uses_explicit_toolchain_paths(self):
  t=(ROOT/'INITIALIZE_PROJECT.md').read_text(); self.assertIn('08_TOOLCHAIN/PORTABILITY_ARCHITECTURE.md',t); self.assertIn('08_TOOLCHAIN/CAPABILITY_CONTRACT.json',t)
 def test_superseded_antigravity_validation_is_archived(self):
  self.assertFalse((ROOT/'06_PROJECT_STATE/BOOTSTRAP_VALIDATION.md').exists()); self.assertFalse((ROOT/'06_PROJECT_STATE/SKILL_API_EXPANSION_VALIDATION.md').exists()); self.assertTrue((ROOT/'05_RELEASES/HISTORY/2026-09-15_antigravity-bootstrap/README.md').exists())
if __name__=='__main__': unittest.main()
