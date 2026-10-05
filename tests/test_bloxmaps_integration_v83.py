from __future__ import annotations
import json, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class BloxMapsIntegrationV83Tests(unittest.TestCase):
    def data(self,rel): return json.loads((ROOT/rel).read_text(encoding='utf-8'))

    def test_pin_is_user_fork_and_source_is_isolated(self):
        cfg=self.data('08_TOOLCHAIN/BLOXMAPS_INTEGRATION.json')
        self.assertEqual(cfg['fork']['repository'],'afkDen/bloxmaps')
        self.assertRegex(cfg['fork']['ref'],r'^[0-9a-f]{40}$')
        self.assertEqual(cfg['checkout']['default_path'],'.local/tools/bloxmaps')
        self.assertTrue(cfg['checkout']['must_be_clean_for_execution'])
        self.assertEqual(cfg['license'],'FSL-1.1-ALv2')
        self.assertEqual(cfg['components']['mapgen']['state'],'priority')
        self.assertEqual(cfg['components']['bloxui_runtime']['state'],'human-architecture-gate')
        self.assertEqual(cfg['components']['bloxui_ai_or_hosted_service']['state'],'not-required')
        self.assertEqual(cfg['security']['allowed_plan_output_roots'],['.local/bloxmaps','04_CHANGESETS'])

    def test_visual_design_is_provider_neutral(self):
        skill=(ROOT/'.agents/skills/visual-design-orchestration/SKILL.md').read_text().lower()
        self.assertIn('provider-neutral',skill)
        self.assertIn('never required',skill)
        lead=(ROOT/'08_TOOLCHAIN/ROLE_CONTRACTS/prompts/lead-orchestrator.md').read_text().lower()
        self.assertIn('claude design may be used',lead)
        self.assertIn('never a canonical dependency',lead)

    def test_bloxmaps_is_tool_not_agent_and_concurrency_stays_three(self):
        roles={r['id']:r for r in self.data('08_TOOLCHAIN/ROLE_CONTRACTS/roles.json')['roles']}
        self.assertEqual(len(roles),10)
        self.assertIn('bloxmaps-world-production',roles['content-production-worker']['required_skills'])
        self.assertIn('bloxmaps-ui-accelerator',roles['frontend-worker']['required_skills'])
        self.assertEqual(self.data('08_TOOLCHAIN/WORKFLOW_PROFILE.json')['orchestration']['max_concurrent_subagents'],3)

    def test_adapter_status_is_read_only_and_structured(self):
        cp=subprocess.run([sys.executable,'scripts/bloxmaps_adapter.py','status','--json'],cwd=ROOT,text=True,capture_output=True)
        self.assertIn(cp.returncode,(0,2))
        d=json.loads(cp.stdout)
        self.assertEqual(d['repository'],'afkDen/bloxmaps')
        self.assertIn('mapgen_ready',d)

    def test_workstation_doctor_reports_bloxmaps_readiness(self):
        cp=subprocess.run([sys.executable,'scripts/workstation_doctor.py','--json'],cwd=ROOT,text=True,capture_output=True)
        self.assertIn(cp.returncode,(0,2))
        d=json.loads(cp.stdout)
        self.assertIn('BLOXMAPS_READY',d['readiness'])
        self.assertIn('bloxmaps',d)

if __name__=='__main__': unittest.main()
