from __future__ import annotations
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class EngineeringReasoningV84Tests(unittest.TestCase):
    def setUp(self):
        self.reg=json.loads((ROOT/'08_TOOLCHAIN/SKILL_REGISTRY.json').read_text())['skills']
        self.by={s['name']:s for s in self.reg}
        self.roles={r['id']:r for r in json.loads((ROOT/'08_TOOLCHAIN/ROLE_CONTRACTS/roles.json').read_text())['roles']}

    def test_selective_adaptations_are_bundled_and_provenanced(self):
        names={
            'decision-grilling','external-questionnaire','domain-modeling','codebase-design',
            'agent-instruction-design','workflow-retrospective','primary-source-research','assurance-two-axis'
        }
        for name in names:
            item=self.by[name]
            self.assertEqual(item['origin'],'project',name)
            self.assertEqual(item['state'],'bundled',name)
            self.assertEqual(item['trust'],'project-authored-adaptation',name)
            self.assertEqual(item['source'],'mattpocock/skills',name)
            self.assertEqual(item['source_commit'],'24fe0ef7737efae15c87225755e9f6f5965e4888',name)
            self.assertRegex(item['source_commit'],r'^[0-9a-f]{40}$',name)
            self.assertRegex(item['upstream_blob_sha'],r'^[0-9a-f]{40}$',name)
            self.assertTrue((ROOT/item['path']/'SKILL.md').is_file(),name)

    def test_tdd_and_process_owning_matt_flows_are_not_registered(self):
        excluded={'tdd','to-spec','to-tickets','implement','implement-spec','triage','wayfinder','ask-matt','setup-matt-pocock-skills'}
        self.assertFalse(excluded & set(self.by), excluded & set(self.by))
        doc=(ROOT/'08_TOOLCHAIN/ENGINEERING_REASONING_V8_4.md').read_text()
        self.assertIn('does **not** import Matt Pocock',doc)
        self.assertIn('TDD is intentionally not part',doc)

    def test_systematic_debugging_is_now_bundled_budget_aware(self):
        item=self.by['systematic-debugging']
        self.assertEqual(item['origin'],'project')
        self.assertEqual(item['state'],'bundled')
        ext=json.loads((ROOT/'08_TOOLCHAIN/EXTERNAL_SKILLS.json').read_text())
        configured={n for src in ext['sources'] for n in src['skills']}
        self.assertNotIn('systematic-debugging',configured)
        skill=(ROOT/'.agents/skills/systematic-debugging/SKILL.md').read_text()
        self.assertIn('cheapest tight feedback loop',skill)
        self.assertIn('do not introduce TDD ceremony',skill)
        self.assertIn('Studio MCP',skill)

    def test_reasoning_skills_route_without_new_roles(self):
        self.assertEqual(len(self.roles),10)
        self.assertIn('decision-grilling',self.roles['lead-orchestrator']['required_skills'])
        self.assertIn('external-questionnaire',self.roles['lead-orchestrator']['required_skills'])
        self.assertIn('codebase-design',self.roles['technical-architect']['required_skills'])
        self.assertIn('assurance-two-axis',self.roles['assurance-reviewer']['required_skills'])
        self.assertIn('agent-instruction-design',self.roles['project-initializer']['required_skills'])
        self.assertNotIn('decision-grilling',self.roles['implementation-worker']['required_skills'])

    def test_human_decision_gate_uses_smallest_mechanism(self):
        skill=(ROOT/'.agents/skills/human-decision-gates/SKILL.md').read_text()
        self.assertIn('Choose the smallest decision mechanism',skill)
        self.assertIn('decision-grilling',skill)
        self.assertIn('external-questionnaire',skill)
        self.assertIn("Facts are the agent's job",skill)

    def test_assurance_two_axes_do_not_add_reviewer_agents(self):
        prompt=(ROOT/'08_TOOLCHAIN/ROLE_CONTRACTS/prompts/assurance-reviewer.md').read_text()
        self.assertIn('Scope/spec fidelity',prompt)
        self.assertIn('Engineering/project standards',prompt)
        self.assertIn('Do not spawn extra reviewers',prompt)

    def test_task_template_has_decision_record_inside_approval_fingerprint(self):
        template=(ROOT/'templates/TASK_TEMPLATE.md').read_text()
        self.assertLess(template.index('## Decision record'),template.index('## Delivery summary'))
        self.assertIn('Open decision frontier',template)
        self.assertIn('External knowledge blockers / questionnaires',template)
        renderer=(ROOT/'scripts/streamlined_task.py').read_text()
        self.assertIn('## Decision record',renderer)

    def test_glossary_is_domain_only_and_feature_editable(self):
        glossary=(ROOT/'GLOSSARY.md').read_text()
        self.assertIn('implementation-free',glossary)
        policy=json.loads((ROOT/'08_TOOLCHAIN/TEAM_POLICY.json').read_text())
        self.assertNotIn('GLOSSARY.md',policy['integrator_owned'])

    def test_reasoning_infrastructure_is_integration_owned(self):
        owned=set(json.loads((ROOT/'08_TOOLCHAIN/TEAM_POLICY.json').read_text())['integrator_owned'])
        for rel in ['08_TOOLCHAIN/ENGINEERING_REASONING_V8_4.md','08_TOOLCHAIN/THIRD_PARTY_NOTICES.md','08_TOOLCHAIN/AGENT_ORCHESTRATION_V8_4.md','tests','05_RELEASES','VERSION','FINAL_PACKAGE_MANIFEST.json']:
            self.assertIn(rel,owned)


    def test_decision_grilling_preserves_approved_scope_fingerprint(self):
        skill=(ROOT/'.agents/skills/decision-grilling/SKILL.md').read_text()
        self.assertIn('After approval, record non-scope-changing operational decisions/pointers in `WORK_STATE.md`',skill)
        self.assertIn('Scope-changing answers after approval require a revisioned scope amendment',skill)

    def test_external_count_reduced_without_registry_config_drift(self):
        ext=json.loads((ROOT/'08_TOOLCHAIN/EXTERNAL_SKILLS.json').read_text())
        expected={n for src in ext['sources'] if src.get('install')=='required' for n in src['skills']}
        registered={s['name'] for s in self.reg if s.get('origin')=='external'}
        self.assertEqual(expected,registered)
        self.assertEqual(len(expected),37)

if __name__=='__main__':
    unittest.main()
