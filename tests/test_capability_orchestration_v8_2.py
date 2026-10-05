from __future__ import annotations
import json, subprocess, sys, tomllib, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class CapabilityOrchestrationV82Tests(unittest.TestCase):
    def data(self,rel):return json.loads((ROOT/rel).read_text(encoding='utf-8'))

    def test_role_set_is_ten_and_consolidated(self):
        roles={r['id']:r for r in self.data('08_TOOLCHAIN/ROLE_CONTRACTS/roles.json')['roles']}
        self.assertEqual(len(roles),10)
        for old in ('repository-scout','quality-reviewer','experience-reviewer','risk-reviewer','release-reviewer','art-director','ui-implementation-worker','world-builder','asset-worker'):
            self.assertNotIn(old,roles)
        self.assertTrue({'lead-orchestrator','creative-director','frontend-worker','content-production-worker','assurance-reviewer'}<=set(roles))
        self.assertIn('repo.graph',roles['lead-orchestrator']['required_capabilities'])
        self.assertTrue(roles['assurance-reviewer']['fresh_context_required'])
        prompt=(ROOT/'08_TOOLCHAIN/ROLE_CONTRACTS/prompts/assurance-reviewer.md').read_text()
        for mode in ('FUNCTIONAL','EXPERIENCE','RISK','RELEASE'):self.assertIn(mode,prompt)

    def test_hard_concurrency_cap_is_three(self):
        cfg=self.data('08_TOOLCHAIN/WORKFLOW_PROFILE.json')['orchestration']
        self.assertEqual(cfg['max_concurrent_subagents'],3)
        self.assertLessEqual(cfg['delegation_budgets']['LIGHT']['active_subagents'],1)
        self.assertLessEqual(cfg['delegation_budgets']['STANDARD']['active_subagents'],2)
        self.assertLessEqual(cfg['delegation_budgets']['CRITICAL']['active_subagents'],3)
        self.assertIn('sequential',cfg['delegation_budgets']['CRITICAL']['notes'])
        self.assertIn('max_concurrent_threads_per_session = 3',(ROOT/'.codex/config.toml').read_text())

    def test_graphify_is_recommended_and_graphiti_removed(self):
        p=self.data('08_TOOLCHAIN/MCP_CAPABILITY_PROFILES.json')['profiles']
        self.assertEqual(p['graphify']['state'],'recommended')
        self.assertEqual(p['graphify']['package'],'graphifyy==0.9.74')
        self.assertNotIn('graphiti',p)
        self.assertEqual(p['graphify']['source_ref'],'e10df08877f8819a625a1afa38c3297a31fda296')
        self.assertTrue((ROOT/'.agents/skills/graphify-repo-intelligence/SKILL.md').is_file())

    def test_blender_mcp_is_priority_with_pinned_dependencies(self):
        p=self.data('08_TOOLCHAIN/MCP_CAPABILITY_PROFILES.json')['profiles']['blender']
        self.assertEqual(p['state'],'priority-for-asset-authoring')
        self.assertEqual(p['package'],'mcp-for-blender==2.1.3')
        self.assertEqual(p['source_repository'],'ahujasid/mcp-for-blender')
        self.assertEqual(p['source_ref'],'60d2a31b4632a7bc178f3dd636f7e68dfb5c8ae4')
        self.assertEqual(p['runtime_defaults']['BLENDER_MCP_SAFE_MODE'],'1')
        self.assertEqual(p['prerequisites']['blender'],'>=4.2')
        self.assertEqual(p['prerequisites']['python'],'>=3.10')
        roles={r['id']:r for r in self.data('08_TOOLCHAIN/ROLE_CONTRACTS/roles.json')['roles']}
        self.assertIn('blender-mcp-production',roles['content-production-worker']['required_skills'])
        self.assertIn('priority',(ROOT/'08_TOOLCHAIN/ROLE_CONTRACTS/prompts/content-production-worker.md').read_text().lower())
        self.assertTrue((ROOT/'08_TOOLCHAIN/MCP_RUNTIME_SETUP.md').is_file())

    def test_frontend_bundle_and_assurance_experience_mode(self):
        roles={r['id']:r for r in self.data('08_TOOLCHAIN/ROLE_CONTRACTS/roles.json')['roles']}
        for skill in ('roblox-frontend-systems','impeccable-ui','design-taste'):
            self.assertIn(skill,roles['frontend-worker']['required_skills'])
        self.assertIn('roblox-frontend-systems',roles['assurance-reviewer']['required_skills'])
        doc=(ROOT/'08_TOOLCHAIN/FRONTEND_SKILLS.md').read_text().lower()
        self.assertNotIn('issue #12',doc);self.assertNotIn('pr #13',doc)
        self.assertIn('dimensional',doc)

    def test_external_skill_sources_are_immutable_refs(self):
        cfg=self.data('08_TOOLCHAIN/EXTERNAL_SKILLS.json')
        for s in cfg['sources']:
            self.assertRegex(s['ref'],r'^[0-9a-f]{40}$')
        code=(ROOT/'scripts/initialize_project.py').read_text()
        self.assertIn("'#'+src['ref']",code)

    def test_workstation_doctor_is_read_only_by_default(self):
        code=(ROOT/'scripts/workstation_doctor.py').read_text()
        self.assertIn('--install-recommended',code)
        self.assertIn('--install-blender-addon',code)
        self.assertIn('graphifyy==0.9.74',code)
        self.assertIn('mcp-for-blender==2.1.3',code)
        cp=subprocess.run([sys.executable,'scripts/workstation_doctor.py','--json'],cwd=ROOT,text=True,capture_output=True)
        self.assertIn(cp.returncode,(0,2)); data=json.loads(cp.stdout); self.assertIn('readiness',data); self.assertIn('BLENDER_MCP_RUNTIME_REGISTRATION',data['readiness'])

    def test_codex_policy_and_generated_config(self):
        subprocess.run([sys.executable,'scripts/sync_runtime_adapters.py','--runtime','codex'],cwd=ROOT,check=True,capture_output=True)
        config=tomllib.loads((ROOT/'.codex/config.toml').read_text())
        self.assertEqual(config['model'],'gpt-6.1-sol')
        self.assertEqual(config['agents']['max_concurrent_threads_per_session'],3)

if __name__=='__main__':unittest.main()
