"""Additional adversarial tests for multi-runtime local model receipts."""
from __future__ import annotations
import hashlib, json, sys, tempfile, tomllib, unittest
from pathlib import Path
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import create_model_preflight as cmp
import validate_model_policy as vmp
from tests import test_model_policy_v7 as old_tests


class ModelPolicyHardeningTests(unittest.TestCase):
    def fixture(self, tmp):
        return old_tests.TeamModelPolicyTests()._receipt_fixture(tmp)

    def test_separate_local_receipts_for_two_runtimes_same_developer(self):
        with tempfile.TemporaryDirectory() as t:
            r = Path(t)
            a = vmp.receipt_path('friend::claude-code', r)
            b = vmp.receipt_path('friend::codex', r)
            c = vmp.receipt_path('friend::claude-code', r)
            self.assertNotEqual(a, b)
            self.assertEqual(a, c)
            self.assertTrue(a.is_relative_to(r / '.local/model_preflights'))

    def test_hash_bound_receipt_rejects_mutated_evidence_even_if_pass(self):
        with tempfile.TemporaryDirectory() as t:
            root, f, data = self.fixture(t)
            self.assertEqual(vmp.validate(f, root, 'friend::claude-code'), [])
            (root / '.local/worker.txt').write_text('adversarial test changed content after human verification')
            self.assertIn('changed hash-bound', ' '.join(vmp.validate(f, root, 'friend::claude-code')))

    def test_provider_can_offer_high_but_claude_team_must_not_use_it(self):
        with tempfile.TemporaryDirectory() as t:
            root, f, data = self.fixture(t)
            data['available_efforts_observed'] = ['low','medium','high','xhigh']
            f.write_text(json.dumps(data))
            self.assertEqual(vmp.validate(f, root, 'friend::claude-code'), [])
            data['delegated_observations'][0]['effort'] = 'high'
            f.write_text(json.dumps(data))
            self.assertTrue(vmp.validate(f, root, 'friend::claude-code'))

    def test_malformed_receipts_never_crash(self):
        with tempfile.TemporaryDirectory() as t:
            root, f, data = self.fixture(t)
            for field, bad in [('main_observation', None), ('delegated_observations', [None]), ('developer', 99), ('available_efforts_observed', [{'bad':'entry'}]), ('human_verification', [])]:
                broken = dict(data)
                broken[field] = bad
                f.write_text(json.dumps(broken))
                self.assertTrue(vmp.validate(f, root, 'friend::claude-code'), field)

    def test_duplicate_delegate_observations_fail(self):
        with tempfile.TemporaryDirectory() as t:
            root, f, data = self.fixture(t)
            data['delegated_observations'].append(dict(data['delegated_observations'][0]))
            f.write_text(json.dumps(data))
            self.assertIn('duplicate', ' '.join(vmp.validate(f, root, 'friend::claude-code')))

    def test_cli_seal_binds_real_local_file_and_resets_prior_pass_on_change(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / '08_TOOLCHAIN').mkdir(parents=True)
            (root / 'templates').mkdir(parents=True)
            (root / '08_TOOLCHAIN/TEAM_MODEL_POLICY.json').write_bytes((ROOT / '08_TOOLCHAIN/TEAM_MODEL_POLICY.json').read_bytes())
            (root / 'templates/MODEL_PREFLIGHT_TEMPLATE.json').write_bytes((ROOT / 'templates/MODEL_PREFLIGHT_TEMPLATE.json').read_bytes())
            key = 'friend::claude-code'
            with patch.object(cmp, 'ROOT', root), patch.object(cmp, 'policy', __import__('model_policy').policy), patch.object(sys, 'argv', ['preflight','--runtime','claude-code','--developer','friend']):
                cmp.main()
            f = vmp.receipt_path(key, root)
            data = json.loads(f.read_text())
            for index, item in enumerate([data['main_observation']] + data['delegated_observations']):
                rel=f'.local/proof-{index}.txt'
                (root / rel).write_text('sanitized real trace placeholder, test fixture')
                item['evidence_file'] = rel
            data['status']='PASS'
            data['human_verification']={'confirmed_by':'friend','confirmed_same_model':True,'confirmed_reasoning_limits':True}
            f.write_text(json.dumps(data))
            with patch.object(cmp, 'ROOT', root), patch.object(sys, 'argv', ['preflight','--runtime','claude-code','--developer','friend','--seal']):
                cmp.main()
            sealed=json.loads(f.read_text())
            self.assertEqual(sealed['status'],'WORK_IN_PROGRESS')
            self.assertTrue(all(item['evidence_sha256'] for item in [sealed['main_observation']]+sealed['delegated_observations']))
            # A second seal does not re-confirm or mutate hashes.
            sealed['status']='PASS';sealed['human_verification']=data['human_verification'];f.write_text(json.dumps(sealed))
            with patch.object(cmp, 'ROOT', root), patch.object(sys, 'argv', ['preflight','--runtime','claude-code','--developer','friend','--seal']):
                cmp.main()
            self.assertEqual(json.loads(f.read_text())['status'],'PASS')


if __name__ == '__main__':
    unittest.main()

class CodexHighExceptionTests(unittest.TestCase):
    def test_only_approved_deep_roles_get_temporary_high_agent(self):
        import prepare_codex_high as h
        from model_policy import ModelPolicyError
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / '.codex/agents').mkdir(parents=True)
            original=(ROOT / '.codex/agents/assurance-reviewer.toml')
            if not original.exists():
                import subprocess
                subprocess.run([sys.executable, 'scripts/sync_runtime_adapters.py', '--runtime', 'codex'],cwd=ROOT,check=True,capture_output=True)
            (root / '.codex/agents/assurance-reviewer.toml').write_bytes(original.read_bytes())
            reason='Security analysis of remote trading ownership trust boundary'
            preview=h.generate('assurance-reviewer','GH-000123',reason,'friend',root=root)
            self.assertIn('PREVIEW',preview)
            self.assertEqual(len(list((root/'.codex/agents').glob('*high.toml'))),0)
            actual=h.generate('assurance-reviewer','GH-000123',reason,'friend',activate=True,root=root)
            self.assertIn('PREPARED',actual)
            variant=root/'.codex/agents/assurance-reviewer-gh-000123-high.toml'
            doc=tomllib.loads(variant.read_text())
            self.assertEqual(doc['model'],'gpt-6.1-sol')
            self.assertEqual(doc['model_reasoning_effort'],'high')
            self.assertEqual(doc['sandbox_mode'],'read-only')
            self.assertIn('GH-000123',doc['developer_instructions'])
            with self.assertRaises(ModelPolicyError):
                h.generate('assurance-reviewer','GH-000123',reason,'friend',activate=True,root=root)
            self.assertIn('DEACTIVATED',h.deactivate('assurance-reviewer','GH-000123',root))
            self.assertFalse(variant.exists())
            with self.assertRaises(ModelPolicyError):
                h.generate('implementation-worker','GH-000124',reason,'friend',root=root)
            with self.assertRaises(ModelPolicyError):
                h.generate('assurance-reviewer','123',reason,'friend',root=root)
            with self.assertRaises(ModelPolicyError):
                h.generate('assurance-reviewer','GH-000124','short','friend',root=root)
            with self.assertRaises(ModelPolicyError):
                h.generate('assurance-reviewer','GH-000124',reason,'',root=root)
