"""Negative contract fixtures; live provider/model/Studio checks remain workstation-only."""
from __future__ import annotations
import hashlib,json,subprocess,sys,tempfile,tomllib,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import model_policy as mp
import validate_model_policy as vmp

class TeamModelPolicyTests(unittest.TestCase):
    def test_shared_policy_structure(self):
        self.assertTrue(mp.validate_policy_structure())
        p=mp.policy();self.assertNotIn('FAST',p['baseline_effort_by_class'])
        self.assertTrue(all(v=='medium' for v in p['baseline_effort_by_class'].values()))

    def test_claude_opus_55_medium_and_low_only(self):
        r=mp.resolve('claude-code','implementation-worker');self.assertEqual((r['model'],r['effort']),('claude-opus-5-5','medium'))
        self.assertEqual(mp.resolve('claude-code','assurance-reviewer')['effort'],'medium')
        with self.assertRaises(mp.ModelPolicyError):mp.resolve('claude-code','assurance-reviewer','high',escalate=True,justification='Even serious review cannot silently exceed team cap')
        with self.assertRaises(mp.ModelPolicyError):mp.resolve('claude-code','assurance-reviewer',model='claude-sonnet-5')

    def test_codex_medium_workhorse_high_narrow_and_justified(self):
        self.assertEqual(mp.resolve('codex','lead-orchestrator')['effort'],'medium')
        for role in ('implementation-worker','frontend-worker'):
            with self.assertRaises(mp.ModelPolicyError):mp.resolve('codex',role,'high',escalate=True,justification='This is an intentionally documented deep problem')
        with self.assertRaises(mp.ModelPolicyError):mp.resolve('codex','assurance-reviewer','high')
        with self.assertRaises(mp.ModelPolicyError):mp.resolve('codex','assurance-reviewer','high',escalate=True,justification='too brief')
        r=mp.resolve('codex','assurance-reviewer','high',escalate=True,justification='Cross-place trust boundary requires additional adversarial reasoning')
        self.assertEqual((r['model'],r['effort']),('gpt-6.1-sol','high'))

    def test_generic_requires_explicit_model(self):
        with self.assertRaises(mp.ModelPolicyError):mp.resolve('future-agent','implementation-worker')
        self.assertEqual(mp.resolve('future-agent','implementation-worker',model='human-approved-future-model')['model'],'human-approved-future-model')

    def test_antigravity_requires_medium_for_normal_workers(self):
        self.assertEqual(mp.resolve('antigravity','implementation-worker',available_efforts=['medium'])['effort'],'medium')
        with self.assertRaises(mp.ModelPolicyError):mp.resolve('antigravity','implementation-worker',available_efforts=['low'])
        with self.assertRaises(mp.ModelPolicyError):mp.resolve('antigravity','implementation-worker',model='claude-opus-5-5')

    def test_generated_claude_and_codex_have_exact_per_role_model_effort(self):
        subprocess.run([sys.executable,'scripts/sync_runtime_adapters.py','--runtime','claude-code'],cwd=ROOT,check=True,capture_output=True)
        subprocess.run([sys.executable,'scripts/sync_runtime_adapters.py','--runtime','codex'],cwd=ROOT,check=True,capture_output=True)
        for role in mp.roles():
            r=mp.roles()[role]
            claude=(ROOT/'.claude/agents'/f'{role}.md').read_text()
            self.assertIn('model: claude-opus-5-5',claude)
            self.assertIn('effort: '+mp.resolve('claude-code',role)['effort'],claude)
            toml=tomllib.loads((ROOT/'.codex/agents'/f'{role}.toml').read_text())
            self.assertEqual(toml['model'],'gpt-6.1-sol')
            self.assertEqual(toml['model_reasoning_effort'],mp.resolve('codex',role)['effort'])
            if r['write_policy']=='read-only':self.assertEqual(toml['sandbox_mode'],'read-only')
        self.assertIn('model_reasoning_effort = "medium"',(ROOT/'.codex/config.toml').read_text())

    def test_generated_skills_preload_at_most_two_per_agent(self):
        subprocess.run([sys.executable,'scripts/sync_runtime_adapters.py','--runtime','claude-code'],cwd=ROOT,check=True,capture_output=True)
        lead=(ROOT/'.claude/agents/lead-orchestrator.md').read_text().split('---')[1]
        self.assertIn('skills:',lead)
        self.assertLessEqual(lead.count('  - '),2)
        self.assertIn('process-inbox',lead)

    def test_antigravity_agents_inherit_same_session_model(self):
        subprocess.run([sys.executable,'scripts/sync_runtime_adapters.py','--runtime','antigravity'],cwd=ROOT,check=True,capture_output=True)
        for r in mp.roles():
            fm=(ROOT/'.agents/agents'/r/'agent.md').read_text().split('---')[1]
            self.assertIn('model: inherit',fm)
            self.assertNotIn('model: pro',fm)

    def _receipt_fixture(self, tmp):
        root=Path(tmp)
        (root/'08_TOOLCHAIN').mkdir()
        (root/'08_TOOLCHAIN/TEAM_MODEL_POLICY.json').write_bytes(mp.POLICY_PATH.read_bytes())
        (root/'.local').mkdir()
        data=json.loads((ROOT/'templates/MODEL_PREFLIGHT_TEMPLATE.json').read_text())
        data.update(runtime='claude-code',runtime_key='friend::claude-code',developer='friend',status='PASS',
                    selected_model='claude-opus-5-5',available_efforts_observed=['low','medium'],policy_sha256=vmp.policy_sha(root))
        data['main_observation']={'model':'claude-opus-5-5','effort':'medium','evidence_file':'.local/main.txt'}
        data['delegated_observations']=[
          {'role':'implementation-worker','model':'claude-opus-5-5','effort':'medium','evidence_file':'.local/worker.txt'},
          {'role':'assurance-reviewer','model':'claude-opus-5-5','effort':'medium','evidence_file':'.local/reviewer.txt'}]
        data['human_verification']={'confirmed_by':'test-person','confirmed_same_model':True,'confirmed_reasoning_limits':True}
        for name in ('main','worker','reviewer'):(root/f'.local/{name}.txt').write_text('sanitized fixture observation: runtime and model, not a live tool run')
        for item in [data['main_observation']]+data['delegated_observations']:
            item['evidence_sha256']=hashlib.sha256((root/item['evidence_file']).read_bytes()).hexdigest()
        file=root/'.local/MODEL_PREFLIGHT.json';file.write_text(json.dumps(data))
        return root,file,data

    def test_local_preflight_rejects_blank_stale_forged_and_wrong_identity(self):
        with tempfile.TemporaryDirectory() as temp:
            root,p,data=self._receipt_fixture(temp)
            self.assertEqual(vmp.validate(p,root,'friend::claude-code'),[])
            self.assertTrue(vmp.validate(p,root,'owner::claude-code'))
            data['policy_sha256']='stale';p.write_text(json.dumps(data));self.assertTrue(vmp.validate(p,root,'friend::claude-code'))
            data['policy_sha256']=vmp.policy_sha(root);data['delegated_observations'][0]['model']='claude-haiku-4-5';p.write_text(json.dumps(data));self.assertTrue(vmp.validate(p,root,'friend::claude-code'))
            data['delegated_observations'][0]['model']='claude-opus-5-5';data['human_verification']['confirmed_same_model']=False;p.write_text(json.dumps(data));self.assertTrue(vmp.validate(p,root,'friend::claude-code'))
            self.assertTrue(vmp.validate(root/'.local/NOT_PRESENT.json',root,'friend::claude-code'))

    def test_planning_only_requires_main_evidence_but_not_delegation(self):
        with tempfile.TemporaryDirectory() as temp:
            root,p,data=self._receipt_fixture(temp)
            data['delegated_observations']=[];p.write_text(json.dumps(data))
            self.assertEqual(vmp.validate(p,root,'friend::claude-code',require_delegates=False),[])
            self.assertTrue(vmp.validate(p,root,'friend::claude-code',require_delegates=True))
            data['main_observation']['model']='not-approved';p.write_text(json.dumps(data))
            self.assertTrue(vmp.validate(p,root,'friend::claude-code',require_delegates=False))

    def test_local_preflight_rejects_high_or_missing_delegate(self):
        with tempfile.TemporaryDirectory() as temp:
            root,p,data=self._receipt_fixture(temp)
            data['delegated_observations'][0]['effort']='high';data['available_efforts_observed'].append('high')
            p.write_text(json.dumps(data));self.assertTrue(vmp.validate(p,root,'friend::claude-code'))
            data['available_efforts_observed']=['low','medium'];data['delegated_observations']=[]
            p.write_text(json.dumps(data));self.assertTrue(vmp.validate(p,root,'friend::claude-code'))

    def test_local_preflight_requires_observed_medium_and_well_formed_delegation(self):
        with tempfile.TemporaryDirectory() as temp:
            root,p,data=self._receipt_fixture(temp)
            data['available_efforts_observed']=['low']
            p.write_text(json.dumps(data))
            self.assertTrue(vmp.validate(p,root,'friend::claude-code'))
            data['available_efforts_observed']=['low','medium']
            data['delegated_observations']='not a list'
            p.write_text(json.dumps(data))
            self.assertTrue(vmp.validate(p,root,'friend::claude-code'))

    def test_initializer_gate_requires_live_model_evidence_not_static_adapter(self):
        code=(ROOT/'scripts/initialize_project.py').read_text()
        self.assertIn("if g=='model_policy_validation' and s=='PASS'",code)
        self.assertIn('validate_models(model_receipt_path(rid),ROOT,rid)',code)
        self.assertIn('from validate_model_policy import validate',code)

    def test_role_packet_never_claims_generic_model_verified(self):
        cp=subprocess.run([sys.executable,'scripts/render_role_packet.py','--role','assurance-reviewer','--task','Review networking'],cwd=ROOT,text=True,capture_output=True,check=True)
        self.assertIn('UNRESOLVED',cp.stdout)
        cp=subprocess.run([sys.executable,'scripts/render_role_packet.py','--role','assurance-reviewer','--task','Review networking','--runtime','codex'],cwd=ROOT,text=True,capture_output=True,check=True)
        self.assertIn('gpt-6.1-sol',cp.stdout)
        self.assertIn('Live verification: REQUIRED',cp.stdout)

if __name__=='__main__':unittest.main()
