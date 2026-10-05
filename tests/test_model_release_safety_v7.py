"""Safety/regression checks for local adapter regeneration and live-MCP reachability."""
from __future__ import annotations
import json,os,sys,tempfile,tomllib,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import sync_runtime_adapters as sync
import validate_team
import initialize_project
from model_policy import ModelPolicyError

class GeneratedAdapterOwnershipTests(unittest.TestCase):
    def test_preserves_custom_files_and_is_idempotent(self):
        (ROOT/'.local').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'.local') as temp:
            d=Path(temp)/'agents';d.mkdir()
            (d/'my-personal-agent.md').write_text('Personal agent: do not delete!')
            sync.update_owned(d,{'managed.md':'First version\n'})
            marker=d/sync.OWNERSHIP
            original=marker.read_bytes()
            sync.update_owned(d,{'managed.md':'First version\n'})
            self.assertEqual(marker.read_bytes(),original)
            self.assertEqual((d/'my-personal-agent.md').read_text(),'Personal agent: do not delete!')
            sync.update_owned(d,{'managed.md':'Updated version\n'})
            self.assertEqual((d/'managed.md').read_text(),'Updated version\n')
            sync.update_owned(d,{})
            self.assertFalse((d/'managed.md').exists())
            self.assertTrue((d/'my-personal-agent.md').exists())

    def test_refuses_local_edits_and_unmarked_conflict_without_partial_writes(self):
        (ROOT/'.local').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'.local') as temp:
            d=Path(temp)/'agents';d.mkdir()
            sync.update_owned(d,{'known.md':'canonical\n'})
            (d/'known.md').write_text('user change!\n')
            with self.assertRaisesRegex(RuntimeError,'LOCAL ADAPTER MODIFIED'):
                sync.update_owned(d,{'known.md':'new canonical\n'})
            self.assertEqual((d/'known.md').read_text(),'user change!\n')
            (d/'known.md').write_bytes(b'canonical\n')
            (d/'foreign.md').write_text('my own\n')
            with self.assertRaisesRegex(RuntimeError,'UNMANAGED ADAPTER CONFLICT'):
                sync.update_owned(d,{'known.md':'should not write\n','foreign.md':'conflicting\n'})
            self.assertEqual((d/'known.md').read_text(),'canonical\n')
            self.assertEqual((d/'foreign.md').read_text(),'my own\n')

    def test_adopts_identical_legacy_generated_files(self):
        (ROOT/'.local').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'.local') as temp:
            d=Path(temp)/'agents';d.mkdir()
            (d/'older.md').write_bytes(b'identical\n')
            sync.update_owned(d,{'older.md':'identical\n'})
            self.assertTrue((d/sync.OWNERSHIP).exists())

    def test_generated_adapter_rejects_dangling_symlink_and_skill_mirror_symlink(self):
        (ROOT/'.local').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'.local') as temp:
            d=Path(temp)/'agents';d.mkdir()
            role=d/'role.md'
            original=Path.is_symlink
            with patch.object(Path,'is_symlink',lambda path: path==role or original(path)):
                with self.assertRaisesRegex(RuntimeError,'UNSAFE ADAPTER SYMLINK'):
                    sync.update_owned(d,{'role.md':'safe content'})
            safe=Path(temp)/'skill';safe.mkdir();(safe/'SKILL.md').write_text('---\nname: test\n---\n')
            resource=safe/'resource';resource.write_bytes(b'fixture')
            with patch.object(Path,'is_symlink',lambda path: path==resource or original(path)):
                with self.assertRaisesRegex(RuntimeError,'cannot contain symlinks'):
                    sync.update_owned(d,{'skill':safe})
            try:role.symlink_to('nonexistent-target')
            except OSError as exc:
                if getattr(exc,'winerror',None)!=1314:raise
            else:
                with self.assertRaisesRegex(RuntimeError,'UNSAFE ADAPTER SYMLINK'):
                    sync.update_owned(d,{'role.md':'safe content'})
                self.assertTrue(role.is_symlink())

    def test_real_studio_agent_inherits_dynamic_mcp_tools_in_claude(self):
        sync.sync('claude-code')
        text=(ROOT/'.claude/agents/studio-operator.md').read_text()
        header=text.split('---',2)[1]
        self.assertNotIn('\ntools:',header,'Fixed built-in allowlist can exclude real MCP server tools')
        self.assertIn('disallowedTools: Edit, Write',header)
        self.assertIn('model: claude-opus-5-5',header)
        self.assertIn('effort: medium',header)
        for role in ('creative-director','implementation-worker'):
            hdr=(ROOT/'.claude/agents'/f'{role}.md').read_text().split('---',2)[1]
            self.assertIn('WebSearch',hdr)
            self.assertIn('WebFetch',hdr)
        lead=(ROOT/'.claude/agents/lead-orchestrator.md').read_text().split('---',2)[1]
        self.assertIn('Agent',lead)

    def test_codex_high_variant_survives_default_regeneration(self):
        sync.sync('codex')
        base=ROOT/'.codex/agents';exception=base/'assurance-reviewer-gh-000123-high.toml'
        exception.write_text('personal authorized test fixture\n')
        try:
            sync.sync('codex')
            self.assertEqual(exception.read_text(),'personal authorized test fixture\n')
            self.assertEqual(tomllib.loads((base/'assurance-reviewer.toml').read_text())['model_reasoning_effort'],'medium')
        finally:exception.unlink()

    def test_codex_conflict_does_not_write_new_default_config(self):
        (ROOT/'.local').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'.local') as temp:
            local_root=Path(temp)
            base=local_root/'.codex/agents';base.mkdir(parents=True)
            (base/'lead-orchestrator.toml').write_text('personal agent, do not overwrite\n')
            with patch.object(sync,'ROOT',local_root), patch.object(sync,'prompt',return_value='Role test fixture'):
                with self.assertRaisesRegex(RuntimeError,'UNMANAGED ADAPTER CONFLICT'):
                    sync.codex()
            self.assertFalse((local_root/'.codex/config.toml').exists())
            self.assertEqual((base/'lead-orchestrator.toml').read_text(),'personal agent, do not overwrite\n')

    def test_generated_codex_config_cannot_overwrite_local_changes(self):
        sync.sync('codex')
        path=ROOT/'.codex/config.toml';original=path.read_text()
        try:
            path.write_text(original+'# Personal modification\n')
            with self.assertRaisesRegex(RuntimeError,'LOCAL CODEX CONFIG MODIFIED'):
                sync.sync('codex')
        finally:path.write_text(original)

    def test_generated_antigravity_frontmatter_is_valid_yaml(self):
        # Python-only optional parsing check: metadata must remain valid YAML
        # even when a role description contains a colon followed by a space.
        try: import yaml
        except ImportError:self.skipTest('PyYAML optional; manually inspect generated frontmatter');return
        sync.sync('antigravity')
        for role in sync.ROLES:
            doc=(ROOT/'.agents/agents'/role['id']/'agent.md').read_text()
            header=yaml.safe_load(doc.split('---',2)[1])
            self.assertEqual(header['name'],role['id'])
            self.assertEqual(header['description'],role['description'])
            self.assertEqual(header['model'],'inherit')


class SharedIntegrationOwnershipTests(unittest.TestCase):
    def _compare(self, changed_path: str, branch: str, github_head_ref: str | None = None):
        def fake_git(args):
            if args[0] == 'rev-parse': return SimpleNamespace(returncode=0, stdout='deadbeef\n')
            if args[:2] == ['diff','--name-status']: return SimpleNamespace(returncode=0, stdout='')
            if args[0] == 'ls-tree': return SimpleNamespace(returncode=0, stdout='')
            if args[:2] == ['diff','--name-only']: return SimpleNamespace(returncode=0, stdout=changed_path+'\n')
            if args[:2] == ['branch','--show-current']: return SimpleNamespace(returncode=0, stdout=branch+'\n')
            raise AssertionError('unexpected git request: '+str(args))
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop('GITHUB_HEAD_REF', None)
            if github_head_ref is not None:
                os.environ['GITHUB_HEAD_REF'] = github_head_ref
            with patch.object(validate_team, 'git', side_effect=fake_git):
                return validate_team.validate_against_base('origin/main')

    def test_branch_detection_isolated_from_ambient_ci_head_ref(self):
        path = 'scripts/initialize_project.py'
        with patch.dict(os.environ, {'GITHUB_HEAD_REF': 'infra/ambient-ci-branch'}):
            self.assertTrue(self._compare(path, 'feat/GH-000123-ui'))
            self.assertFalse(self._compare(path, 'infra/approved-model-policy'))

    def test_ci_head_ref_takes_precedence_over_checkout_branch(self):
        path = 'scripts/initialize_project.py'
        self.assertFalse(self._compare(path, 'feat/GH-000123-ui', 'infra/approved-model-policy'))
        self.assertTrue(self._compare(path, 'infra/approved-model-policy', 'feat/GH-000123-ui'))

    def test_new_model_and_bootstrap_paths_are_integration_owned(self):
        for path in ('scripts/initialize_project.py','scripts/create_model_preflight.py',
                     'scripts/render_role_packet.py','08_TOOLCHAIN/CAPABILITY_CONTRACT.json',
                     '08_TOOLCHAIN/RUNTIME_PROFILES.json','08_TOOLCHAIN/EXTERNAL_SKILLS.json',
                     '.agents/skills/model-policy-governor/SKILL.md',
                     'tests/test_engineering_reasoning_v84.py',
                     '05_RELEASES/V8_4_ENGINEERING_REASONING_AUDIT_2026-10-05.md'):
            with self.subTest(path=path):
                self.assertTrue(self._compare(path,'feat/GH-000123-ui'))
                self.assertFalse(self._compare(path,'infra/approved-model-policy'))

    def test_team_policy_is_authoritative_for_protected_file_list(self):
        policy=json.loads((ROOT/'08_TOOLCHAIN/TEAM_POLICY.json').read_text())
        self.assertIn('scripts/initialize_project.py',policy['integrator_owned'])
        self.assertIn('.agents/skills',policy['integrator_owned'])


class GlobalCheckpointFailureTests(unittest.TestCase):
    def _attempt_finalization(self, fail_step: str):
        with tempfile.TemporaryDirectory(dir=ROOT/'.local') as tmp:
            fake_root=Path(tmp)
            (fake_root/'06_PROJECT_STATE').mkdir()
            state={'project_status':'INITIALIZATION_REQUIRED', 'checks':{
                k:{'status':'PASS','evidence': 'reviewed skill_lock_sha256=abc' if k=='skill_supply_chain_review' else 'local fixture'}
                for k in initialize_project.GLOBAL}}
            runtime={'mode':'FULL_NATIVE','status':'VALIDATION_REQUIRED','checks':{
                k:{'status':'PASS','evidence':'local fixture'} for k in initialize_project.RUNTIME}}
            def fake_run(args,check=False):
                if args[:2]==['git','add']:return SimpleNamespace(returncode=int(fail_step=='stage'),stdout='simulated stage error')
                if args[:3]==['git','diff','--cached']:return SimpleNamespace(returncode=1,stdout='')
                if args[0]=='git' and 'commit' in args:return SimpleNamespace(returncode=int(fail_step=='commit'),stdout='simulated commit error')
                raise AssertionError('unexpected git request: '+str(args))
            with patch.object(initialize_project,'ROOT',fake_root),\
                 patch.object(initialize_project,'authorized_global_branch',return_value=True),\
                 patch.object(initialize_project,'load',return_value=state),\
                 patch.object(initialize_project,'runtime_entry',return_value=({'runtimes':{}},runtime)),\
                 patch.object(initialize_project,'current_lock_digest',return_value='abc'),\
                 patch.object(initialize_project,'run',side_effect=fake_run),\
                 patch.object(initialize_project,'save'),\
                 patch('validate_initialization_studio.validate',return_value=[]),\
                 patch('validate_model_policy.validate',return_value=[]),\
                 patch('workstation_preflight.current_preflight',return_value=True):
                with self.assertRaisesRegex(SystemExit,'NOT FINALIZED'):
                    initialize_project.finalize('alice::codex')

    def test_staging_error_cannot_report_global_ready(self):
        self._attempt_finalization('stage')

    def test_commit_error_cannot_report_global_ready(self):
        self._attempt_finalization('commit')
