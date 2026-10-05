from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

import bloxmaps_adapter as blox
import validate_ci_task
from streamlined_task import approve_task, create_task, validate_task


def run_git(repo: Path, *args: str, text: bool = True):
    return subprocess.run(['git', *args], cwd=repo, capture_output=True, text=text, check=True)


class ByteIntegrityHardeningTests(unittest.TestCase):
    def test_reference_tree_is_protected_from_line_ending_normalization(self):
        attrs = (ROOT / '.gitattributes').read_text(encoding='utf-8')
        self.assertIn('04_CHANGESETS/**/REFERENCES/** -text', attrs)

    def test_crlf_reference_survives_git_add_commit_and_checkout_byte_exact(self):
        payload = b'Line one\r\nLine two\r\n'
        with tempfile.TemporaryDirectory() as tmp:
            origin = Path(tmp) / 'origin'
            clone = Path(tmp) / 'clone'
            origin.mkdir()
            run_git(origin, 'init')
            run_git(origin, 'config', 'user.name', 'fixture')
            run_git(origin, 'config', 'user.email', 'fixture@example.invalid')
            run_git(origin, 'config', 'core.autocrlf', 'true')
            (origin / '.gitattributes').write_bytes((ROOT / '.gitattributes').read_bytes())
            ref = origin / '04_CHANGESETS/GH-000007_visual-update/REFERENCES/01_notes.txt'
            ref.parent.mkdir(parents=True)
            ref.write_bytes(payload)
            run_git(origin, 'add', '.gitattributes', ref.relative_to(origin).as_posix())
            run_git(origin, 'commit', '-m', 'fixture')

            blob = subprocess.run(
                ['git', 'show', 'HEAD:' + ref.relative_to(origin).as_posix()],
                cwd=origin, capture_output=True, check=True,
            ).stdout
            self.assertEqual(blob, payload)
            self.assertEqual(hashlib.sha256(blob).hexdigest(), hashlib.sha256(payload).hexdigest())

            subprocess.run(
                ['git', '-c', 'core.autocrlf=true', 'clone', str(origin), str(clone)],
                capture_output=True, check=True,
            )
            checked = clone / ref.relative_to(origin)
            self.assertEqual(checked.read_bytes(), payload)

    def test_human_approval_binds_reference_metadata_as_well_as_file_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / '04_CHANGESETS').mkdir()
            source = root / 'idea.txt'
            source.write_bytes(b'Build the room.\r\n')
            reference = root / 'notes.txt'
            reference.write_bytes(b'Original notes\r\n')
            dst = create_task(
                source=source, issue=9, kind='idea', title='Room', slug='room',
                branch='feat/9-room', owner='owner', risk='STANDARD',
                references=[str(reference)], root=root,
            )
            approve_task(9, 'owner', 'approved', root=root)
            self.assertEqual(validate_task(9, root, require_approved=True), [])

            # Simulate a coordinated metadata+file rewrite that would defeat a
            # simple "file hash matches TASK.json" check.
            task_path = dst / 'TASK.json'
            task = json.loads(task_path.read_text(encoding='utf-8'))
            ref_path = dst / task['references'][0]['path']
            replacement = b'Rewritten after approval\r\n'
            ref_path.write_bytes(replacement)
            task['references'][0]['sha256'] = hashlib.sha256(replacement).hexdigest()
            task['references'][0]['bytes'] = len(replacement)
            task_path.write_text(json.dumps(task, indent=2) + '\n', encoding='utf-8')
            errors = validate_task(9, root, require_approved=True)
            self.assertIn('intake provenance changed after human approval', '; '.join(errors))


class BloxMapsHardeningTests(unittest.TestCase):
    def _checkout(self, root: Path) -> tuple[Path, str, str]:
        checkout = root / 'checkout'
        checkout.mkdir()
        run_git(checkout, 'init')
        run_git(checkout, 'config', 'user.name', 'fixture')
        run_git(checkout, 'config', 'user.email', 'fixture@example.invalid')
        remote = 'https://github.com/example/reviewed-bloxmaps.git'
        run_git(checkout, 'remote', 'add', 'origin', remote)
        (checkout / 'tools').mkdir()
        (checkout / 'src/MapGen').mkdir(parents=True)
        (checkout / 'tools/mapgen.py').write_text('# fixture\n', encoding='utf-8')
        (checkout / 'src/MapGen/init.luau').write_text('-- fixture\n', encoding='utf-8')
        run_git(checkout, 'add', '.')
        run_git(checkout, 'commit', '-m', 'fixture')
        ref = run_git(checkout, 'rev-parse', 'HEAD').stdout.strip()
        return checkout, ref, remote

    def test_dirty_reviewed_checkout_is_not_mapgen_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            checkout, ref, remote = self._checkout(root)
            with patch.object(blox, 'ROOT', root), \
                 patch.object(blox, 'CHECKOUT', checkout), \
                 patch.object(blox, 'REF', ref), \
                 patch.object(blox, 'REMOTE', remote), \
                 patch.object(blox.shutil, 'which', side_effect=lambda name: '/fixture/luau' if name.startswith('luau') else None):
                clean = blox.status()
                self.assertTrue(clean['clean'])
                self.assertTrue(clean['mapgen_ready'])
                (checkout / 'tools/mapgen.py').write_text('# locally modified\n', encoding='utf-8')
                dirty = blox.status()
                self.assertFalse(dirty['clean'])
                self.assertFalse(dirty['mapgen_ready'])
                self.assertIn('checkout is dirty; do not auto-upgrade/reset it', dirty['issues'])

    def test_generated_plan_output_is_confined_to_approved_roots(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            allowed_local = root / '.local/bloxmaps'
            allowed_task = root / '04_CHANGESETS'
            with patch.object(blox, 'ROOT', root), patch.object(blox, 'ALLOWED_OUTPUT_ROOTS', (allowed_local, allowed_task)):
                self.assertEqual(
                    blox.resolve_output_path('.local/bloxmaps/plan.json'),
                    allowed_local / 'plan.json',
                )
                self.assertEqual(
                    blox.resolve_output_path('04_CHANGESETS/GH-000001_x/map-plan.json'),
                    allowed_task / 'GH-000001_x/map-plan.json',
                )
                with self.assertRaisesRegex(ValueError, 'approved root'):
                    blox.resolve_output_path(str(root.parent / 'outside.json'))


class WorkflowBoundaryHardeningTests(unittest.TestCase):
    def test_new_v83_workflow_and_bloxmaps_files_are_integration_owned(self):
        policy = json.loads((ROOT / '08_TOOLCHAIN/TEAM_POLICY.json').read_text(encoding='utf-8'))
        protected = set(policy['integrator_owned'])
        for path in (
            '.gitattributes',
            '08_TOOLCHAIN/BLOXMAPS_INTEGRATION.json',
            '08_TOOLCHAIN/BLOXMAPS_SETUP.md',
            'scripts/bloxmaps_adapter.py',
            '08_TOOLCHAIN/AGENT_ORCHESTRATION_V8_3.md',
            '08_TOOLCHAIN/MCP_CAPABILITY_PROFILES.json',
            '08_TOOLCHAIN/FRONTEND_SKILLS.md',
            '08_TOOLCHAIN/CONTEXT_AND_MEMORY.md',
            'scripts/validate_feature_evidence.py',
            'templates/QUALITY_EVIDENCE_TEMPLATE.json',
        ):
            with self.subTest(path=path):
                self.assertIn(path, protected)

    def test_asset_only_change_uses_delivery_gate_in_ci_validator(self):
        calls = []

        def fake_git(*args):
            if args[:2] == ('rev-parse', '--verify'):
                return SimpleNamespace(returncode=0, stdout='deadbeef\n', stderr='')
            if args[:2] == ('branch', '--show-current'):
                return SimpleNamespace(returncode=0, stdout='feat/42-art-pass\n', stderr='')
            raise AssertionError('unexpected git call: ' + repr(args))

        def fake_validate(issue, root, *, require_approved=False, require_delivery=False):
            calls.append((issue, require_approved, require_delivery))
            return ['fixture stops after gate assertion']

        with patch.object(validate_ci_task, 'git', side_effect=fake_git), \
             patch.object(validate_ci_task, 'changed_src', return_value=['07_ASSETS/APPROVED/rock.glb']), \
             patch.object(validate_ci_task, 'validate_task', side_effect=fake_validate), \
             patch.object(sys, 'argv', ['validate_ci_task.py', '--compare', 'origin/main']), \
             patch.dict(os.environ, {}, clear=False):
            os.environ.pop('GITHUB_HEAD_REF', None)
            self.assertEqual(validate_ci_task.main(), 1)
        self.assertEqual(calls, [(42, True, True)])

    def test_quality_template_uses_canonical_branch_and_role(self):
        doc = json.loads((ROOT / 'templates/QUALITY_EVIDENCE_TEMPLATE.json').read_text(encoding='utf-8'))
        self.assertEqual(doc['branch'], 'feat/123-feature')
        self.assertEqual(doc['skill_use_receipts'][0]['role'], 'content-production-worker')

    def test_skill_counts_are_registry_derived_and_current(self):
        cp = subprocess.run(
            [sys.executable, 'scripts/sync_derived_docs.py', '--check'],
            cwd=ROOT, text=True, capture_output=True,
        )
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        state = (ROOT / '06_PROJECT_STATE/CURRENT_STATE.md').read_text(encoding='utf-8')
        reg = json.loads((ROOT / '08_TOOLCHAIN/SKILL_REGISTRY.json').read_text(encoding='utf-8'))['skills']
        bundled = sum(1 for s in reg if s.get('origin') == 'project' and s.get('state') == 'bundled')
        external = sum(1 for s in reg if s.get('origin') == 'external')
        self.assertIn(f'Skills: {bundled} bundled + {external} reviewed external = {len(reg)} registered', state)

    def test_historical_master_directive_is_explicitly_non_authoritative(self):
        head = (ROOT / '00_INPUT/SYSTEM/MASTER_PROJECT_DIRECTIVE.md').read_text(encoding='utf-8')[:700]
        self.assertIn('HISTORICAL SOURCE DIRECTIVE — NON-AUTHORITATIVE', head)
        self.assertIn('/AGENTS.md', head)


if __name__ == '__main__':
    unittest.main()
