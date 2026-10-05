from __future__ import annotations
import hashlib, importlib, json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import submit_proposal, intake_request, promote_proposal, team_setup, validate_team, initialize_project

class SharedTeamContracts(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        for folder in ['00_INPUT/PROPOSALS/IDEAS','00_INPUT/PROPOSALS/UPDATES','00_INPUT/GAME_IDEA','00_INPUT/UPDATES/PROCESSED','04_CHANGESETS','templates']:
            (self.root/folder).mkdir(parents=True,exist_ok=True)
        shutil.copytree(ROOT/'templates/CHANGESET_TEMPLATE',self.root/'templates/CHANGESET_TEMPLATE')
        self.saved_intake={x:getattr(intake_request,x) for x in ['ROOT','CHANGESETS','TEMPLATE']}
        intake_request.ROOT=self.root
        intake_request.CHANGESETS=self.root/'04_CHANGESETS'
        intake_request.TEMPLATE=self.root/'templates/CHANGESET_TEMPLATE'
    def tearDown(self):
        for x,v in self.saved_intake.items():setattr(intake_request,x,v)
        self.temp.cleanup()
    def source(self,name='idea.txt',raw=b'I want a cave game.\r\n'):
        f=self.root/name; f.write_bytes(raw);return f
    def test_immutable_proposal_preserves_notepad_bytes_and_metadata(self):
        src=self.source(raw=b'Pets\r\nModerate bonuses\r\n')
        dest=submit_proposal.add_proposal(src,123,'alex-dev','update',self.root)
        self.assertEqual(dest.read_bytes(),src.read_bytes())
        self.assertEqual(validate_team.check_proposal(dest,self.root),[])
        meta=json.loads(dest.with_suffix('.json').read_text())
        self.assertEqual(meta['sha256'],hashlib.sha256(src.read_bytes()).hexdigest())
        self.assertEqual(meta['key'],'GH-000123')
        self.assertEqual(meta['kind'],'update')
    def test_same_issue_cannot_submit_two_proposals(self):
        p=self.source();submit_proposal.add_proposal(p,123,'alex','idea',self.root)
        with self.assertRaises(FileExistsError):submit_proposal.add_proposal(p,123,'alex','update',self.root)
    def test_proposals_on_parallel_issues_do_not_allocate_U_numbers(self):
        src=self.source()
        one=submit_proposal.add_proposal(src,123,'alice','idea',self.root)
        two=submit_proposal.add_proposal(src,124,'bob','update',self.root)
        a=intake_request.create_issue_changeset(one,123)
        b=intake_request.create_issue_changeset(two,124)
        self.assertTrue(a.name.startswith('GH-000123_'))
        self.assertTrue(b.name.startswith('GH-000124_'))
        self.assertEqual((a/'USER_REQUEST.txt').read_bytes(),src.read_bytes())
        self.assertEqual((b/'USER_REQUEST.txt').read_bytes(),src.read_bytes())
        self.assertEqual(validate_team.check_proposal(one,self.root),[])
    def test_tamper_is_detected_by_proposal_and_issue_intake(self):
        p=submit_proposal.add_proposal(self.source(),78,'alice','idea',self.root)
        p.write_bytes(p.read_bytes()+b'new content')
        self.assertTrue(validate_team.check_proposal(p,self.root))
        with self.assertRaises(ValueError):intake_request.create_issue_changeset(p,78)
    def test_validator_detects_modified_approved_game_idea(self):
        self.source(raw=b'Original\r\n')
        p=submit_proposal.add_proposal(self.root/'idea.txt',70,'alice','idea',self.root)
        accepted=promote_proposal.promote(70,'idea','lead',root=self.root,allow_test_branch=True)
        self.assertEqual(validate_team.check_proposal(p,self.root),[])
        # validate_all requires boilerplate; direct approved integrity assertions are covered by unit checks and PR simulation.
        self.assertEqual(accepted.read_bytes(),p.read_bytes())
        accepted.write_bytes(b'malicious altered game vision')
        self.assertNotEqual(accepted.read_bytes(),p.read_bytes())
        for rel in validate_team.REQUIRED:
            dst=self.root/rel; dst.parent.mkdir(parents=True,exist_ok=True)
            if not dst.exists():shutil.copy2(ROOT/rel,dst)
        (self.root/'.gitignore').write_text('.local/\n')
        errors=validate_team.validate_all(self.root)
        self.assertTrue(any('approved raw input differs from original proposal' in x for x in errors),errors)
    def test_approved_raw_integrity_validator_has_shared_input_checks(self):
        source=(ROOT/'scripts/validate_team.py').read_text()
        self.assertIn('approved raw input differs from original proposal',source)
        self.assertIn('issue changeset raw request differs from proposal',source)
    def test_wrong_issue_rejected(self):
        p=submit_proposal.add_proposal(self.source(),78,'alice','idea',self.root)
        with self.assertRaises(ValueError):intake_request.create_issue_changeset(p,79)
    def test_cannot_duplicate_changeset_on_same_branch(self):
        p=submit_proposal.add_proposal(self.source(),78,'alice','idea',self.root)
        intake_request.create_issue_changeset(p,78)
        with self.assertRaises(ValueError):intake_request.create_issue_changeset(p,78)
    def test_cannot_escape_by_symlink_proposal(self):
        p=submit_proposal.add_proposal(self.source(),78,'alice','idea',self.root)
        link=p.parent/'GH-000079_link.txt';link.write_bytes(p.read_bytes())
        original=Path.is_symlink
        with patch.object(Path,'is_symlink',lambda path: path==link or original(path)):
            with self.assertRaises(ValueError):intake_request.create_issue_changeset(link,79)
        link.unlink()
        try:link.symlink_to(p)
        except OSError as exc:
            if getattr(exc,'winerror',None)!=1314:raise
        else:
            with self.assertRaises(ValueError):intake_request.create_issue_changeset(link,79)
    def test_promotion_initial_idea_is_one_time_and_byte_preserving(self):
        src=self.source(raw=b'I want caves.\r\n\x00Keep exact bytes.\r\n')
        p=submit_proposal.add_proposal(src,78,'alice','idea',self.root)
        accepted=promote_proposal.promote(78,'idea','lead',root=self.root,allow_test_branch=True)
        self.assertEqual(accepted.read_bytes(),src.read_bytes())
        self.assertEqual(json.loads(accepted.with_name('APPROVAL.json').read_text())['proposal'],p.relative_to(self.root).as_posix())
        with self.assertRaises(FileExistsError):promote_proposal.promote(78,'idea','lead',root=self.root,allow_test_branch=True)
    def test_update_promotion_requires_integrated_changeset(self):
        p=submit_proposal.add_proposal(self.source(),90,'alex','update',self.root)
        with self.assertRaises(ValueError):promote_proposal.promote(90,'update','lead',root=self.root,allow_test_branch=True)
        intake_request.create_issue_changeset(p,90)
        out=promote_proposal.promote(90,'update','lead',root=self.root,allow_test_branch=True)
        self.assertEqual(out.read_bytes(),p.read_bytes())
    def test_invalid_input_name_or_issue_fails(self):
        with self.assertRaises(ValueError):submit_proposal.add_proposal(self.source(),0,'alice','idea',self.root)
        with self.assertRaises(ValueError):submit_proposal.add_proposal(self.source(),12,'../../bad','idea',self.root)
    def test_personal_profiles_are_developer_and_runtime_separate(self):
        a=team_setup.local_profile('alice','claude-code','1.2','Sonnet local')
        b=team_setup.local_profile('bob','codex','2.0','Custom local')
        self.assertNotEqual((a['developer'],a['runtime']),(b['developer'],b['runtime']))
        self.assertEqual(a['runtime_validation_path'],'.local/RUNTIME_VALIDATIONS.json')
        self.assertIn('.local/',(ROOT/'.gitignore').read_text())
    def test_shared_runtime_registry_stays_template(self):
        p=self.root/'.local/RUNTIME_VALIDATIONS.json'
        old=initialize_project.RUNTIMES
        initial=(ROOT/'06_PROJECT_STATE/RUNTIME_VALIDATIONS.json').read_bytes()
        initialize_project.RUNTIMES=p
        try:
            initialize_project.setr('claude-code','skill_discovery','PASS','test fixture only',mode='PLANNING_ONLY')
            self.assertTrue(p.is_file())
            self.assertNotIn('claude-code',initial.decode())
            self.assertEqual((ROOT/'06_PROJECT_STATE/RUNTIME_VALIDATIONS.json').read_bytes(),initial)
        finally: initialize_project.RUNTIMES=old
    def test_team_policy_and_workflow_files_exist(self):
        policy=json.loads((ROOT/'08_TOOLCHAIN/TEAM_POLICY.json').read_text())
        self.assertTrue(policy['collaboration_enabled'])
        for path in ['.github/workflows/portable-ci.yml','.github/CODEOWNERS','TEAM_ONBOARDING.md','TEAM_PROTOCOL.md','TEAM_IMPORT_GITHUB.md']:
            self.assertTrue((ROOT/path).is_file(),path)
    def test_legacy_sequential_cli_is_explicit_solo(self):
        src=(ROOT/'scripts/intake_request.py').read_text()
        self.assertIn('--solo',src);self.assertIn('Team mode requires --proposal',src)
    def test_global_initializer_requires_maintainer_flag(self):
        s=(ROOT/'scripts/initialize_project.py').read_text()
        self.assertIn('--initialize-global',s)
        self.assertIn('Team global finalization requires',s)
    def test_new_runtime_does_not_reset_shared_game_state(self):
        s=(ROOT/'scripts/team_setup.py').read_text()
        self.assertNotIn('setg(',s)
        self.assertNotIn('INITIALIZATION_STATUS.json',s)
        self.assertIn('LOCAL',s)
    def test_local_finalize_never_writes_shared_project_state(self):
        temp_registry=self.root/'.local/RUNTIME_VALIDATIONS.json'
        prior=initialize_project.RUNTIMES
        initialize_project.RUNTIMES=temp_registry
        source=(ROOT/'06_PROJECT_STATE/INITIALIZATION_STATUS.json').read_bytes()
        try:
            for gate in sorted(initialize_project.RUNTIME-{'roblox_studio_bridge','studio_disposable_test'}):
                initialize_project.setr('chat-only',gate,'PASS','test fixture only',mode='PLANNING_ONLY')
            from unittest.mock import patch
            with patch('validate_model_policy.validate',return_value=[]):
                initialize_project.finalize_local('chat-only')
            j=json.loads(temp_registry.read_text())
            self.assertEqual(j['runtimes']['chat-only']['status'],'VALIDATED_PLANNING_ONLY')
            self.assertEqual((ROOT/'06_PROJECT_STATE/INITIALIZATION_STATUS.json').read_bytes(),source)
            before=temp_registry.read_bytes()
            with patch('validate_model_policy.validate',return_value=[]):
                initialize_project.finalize_local('chat-only')
            self.assertEqual(temp_registry.read_bytes(),before)
        finally:initialize_project.RUNTIMES=prior
    def test_local_finalize_does_not_fake_full_studio_readiness(self):
        temp_registry=self.root/'.local/RUNTIME_VALIDATIONS.json'
        prior=initialize_project.RUNTIMES;initialize_project.RUNTIMES=temp_registry
        try:
            initialize_project.setr('local-full','capability_validation','PASS','test',mode='FULL_EMULATED')
            with self.assertRaises(SystemExit):initialize_project.finalize_local('local-full')
        finally:initialize_project.RUNTIMES=prior
    def test_per_developer_runtime_key_is_supported(self):
        source=(ROOT/'scripts/initialize_project.py').read_text()
        self.assertIn("f'{a.developer}::{a.runtime}'",source)
        self.assertIn('setr(runtime_key',source)
    def test_authorized_global_branch_accepts_reviewed_infra_not_feature(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        for branch in ('main','infra/initial-skill-bootstrap'):
            with patch.object(initialize_project,'run',return_value=SimpleNamespace(stdout=branch)):
                self.assertTrue(initialize_project.authorized_global_branch())
        with patch.object(initialize_project,'run',return_value=SimpleNamespace(stdout='feat/123-unapproved')):
            self.assertFalse(initialize_project.authorized_global_branch())
    def test_lock_absence_reports_partial_not_claim_ready(self):
        self.assertIn('no committed approved SKILL_LOCK.json',(ROOT/'scripts/team_setup.py').read_text())

if __name__=='__main__': unittest.main()
