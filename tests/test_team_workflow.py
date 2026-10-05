"""Real local bare-remote handoff tests. No GitHub network, Roblox, or AI tools needed."""
from __future__ import annotations
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('team_workflow',ROOT/'scripts/team_workflow.py')
workflow=importlib.util.module_from_spec(spec);spec.loader.exec_module(workflow)


def git(cwd,*args):
    p=subprocess.run(['git',*args],cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if p.returncode:raise AssertionError('git command failed: '+' '.join(args)+'\n'+p.stderr)
    return p.stdout.strip()

class TeamWorkflowGit(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name)
        self.bare=self.base/'origin.git';git(self.base,'init','--bare','-b','main',str(self.bare))
        self.work=self.base/'alice';git(self.base,'clone',str(self.bare),str(self.work))
        git(self.work,'config','user.name','Alice');git(self.work,'config','user.email','alice@example.invalid')
        for rel in ['scripts','08_TOOLCHAIN','00_INPUT/PROPOSALS/IDEAS','00_INPUT/PROPOSALS/UPDATES','templates/CHANGESET_TEMPLATE','.local/ideas']:(self.work/rel).mkdir(parents=True,exist_ok=True)
        for file in ['scripts/intake_request.py','scripts/submit_proposal.py','scripts/validate_team.py']:
            shutil.copy2(ROOT/file,self.work/file)
        shutil.copytree(ROOT/'templates/CHANGESET_TEMPLATE',self.work/'templates/CHANGESET_TEMPLATE',dirs_exist_ok=True)
        (self.work/'08_TOOLCHAIN/TEAM_POLICY.json').write_text(json.dumps({'canonical_branch':'main','remote_url':str(self.bare),'template_unconfigured':False}))
        (self.work/'.gitignore').write_text('.local/\n')
        (self.work/'README.md').write_text('fixture\n')
        git(self.work,'add','.');git(self.work,'commit','-m','bootstrap');git(self.work,'push','origin','main')
        self.w=workflow.Workspace(self.work)
    def tearDown(self):
        self.tmp.cleanup()

    def second_contributor_updates_main(self):
        bob=self.base/'bob';git(self.base,'clone',str(self.bare),str(bob))
        git(bob,'config','user.name','Bob');git(bob,'config','user.email','bob@example.invalid')
        (bob/'OTHER.txt').write_text('another teammate added this\n')
        git(bob,'add','.');git(bob,'commit','-m','Bob approved change');git(bob,'push','origin','main')
        return git(bob,'rev-parse','HEAD')

    def test_proposal_syncs_newest_remote_and_preserves_bytes(self):
        newer=self.second_contributor_updates_main()
        source=self.work/'.local/ideas/pets.txt';source.write_bytes(b'Add pets.\r\nKeep bonuses modest.\r\n')
        self.w.propose(kind='update',issue=123,by='alice',source=str(source),slug='pets')
        self.assertEqual(git(self.work,'branch','--show-current'),'proposal/123-pets')
        self.assertEqual(git(self.work,'merge-base','HEAD',newer),newer)
        raw=self.work/'00_INPUT/PROPOSALS/UPDATES/GH-000123_pets.txt'
        self.assertEqual(raw.read_bytes(),source.read_bytes())
        self.assertTrue((raw.with_suffix('.json')).is_file())
        self.assertTrue((self.work/'OTHER.txt').exists())

    def test_dirty_main_refuses_without_touching_edits_or_branch(self):
        dirty=self.work/'personal-untracked.txt';dirty.write_text('do not lose')
        source=self.work/'.local/ideas/pets.txt';source.write_text('pets')
        before=git(self.work,'rev-parse','HEAD')
        with self.assertRaisesRegex(workflow.WorkflowError,'dirty'):
            self.w.propose(kind='update',issue=123,by='alice',source=str(source),slug='pets')
        self.assertEqual(dirty.read_text(),'do not lose')
        self.assertEqual(git(self.work,'rev-parse','HEAD'),before)
        self.assertEqual(git(self.work,'branch','--show-current'),'main')

    def test_wrong_origin_refuses_even_on_clean_main(self):
        other=self.base/'wrong.git';git(self.base,'init','--bare','-b','main',str(other))
        git(self.work,'remote','set-url','origin',str(other))
        with self.assertRaisesRegex(workflow.WorkflowError,'origin does not match'):
            self.w.sync()

    def test_approved_proposal_is_intaken_from_up_to_date_main(self):
        # Proposal accepted into the simulated main by a separate reviewer.
        fixture=self.work/'00_INPUT/PROPOSALS/IDEAS/GH-000321_caves.txt'
        raw=b'A new cave game.\r\n'
        fixture.write_bytes(raw)
        import hashlib
        fixture.with_suffix('.json').write_text(json.dumps({'schema_version':1,'issue':321,'key':'GH-000321','kind':'idea','submitted_by':'alice','sha256':hashlib.sha256(raw).hexdigest(),'raw_file':fixture.relative_to(self.work).as_posix()}))
        git(self.work,'add','.');git(self.work,'commit','-m','accepted proposal');git(self.work,'push','origin','main')
        self.second_contributor_updates_main()
        self.w.start(kind='idea',issue=321,proposal=fixture.relative_to(self.work).as_posix(),slug='caves')
        self.assertEqual(git(self.work,'branch','--show-current'),'feat/321-caves')
        changeset=self.work/'04_CHANGESETS/GH-000321_caves'
        self.assertEqual((changeset/'USER_REQUEST.txt').read_bytes(),raw)
        self.assertTrue((changeset/'SOURCE_PROPOSAL.json').exists())
        self.assertTrue((self.work/'OTHER.txt').exists())

    def test_local_main_ahead_blocks_new_work(self):
        (self.work/'EXTRA.txt').write_text('not pushed')
        git(self.work,'add','.');git(self.work,'commit','-m','unpublished main commit')
        with self.assertRaisesRegex(workflow.WorkflowError,'unpublished'):
            self.w.sync()

    def test_preview_never_pushes_or_creates_pr(self):
        self.w.publish(issue=777,confirm=False)
        self.assertEqual(git(self.work,'branch','-r').splitlines(),['  origin/main'] if git(self.work,'branch','-r').startswith('  ') else ['origin/main'])

    def test_next_task_requires_verified_merge_then_syncs_main(self):
        # Prior task is complete and clean; a second merged proposal is on latest main.
        raw=b'First idea\r\n'
        first=self.work/'00_INPUT/PROPOSALS/IDEAS/GH-000321_caves.txt'
        import hashlib
        def create_prop(path, issue, kind, data):
            path.write_bytes(data)
            path.with_suffix('.json').write_text(json.dumps({'schema_version':1,'issue':issue,'key':f'GH-{issue:06d}','kind':kind,'submitted_by':'alice','sha256':hashlib.sha256(data).hexdigest(),'raw_file':path.relative_to(self.work).as_posix()}))
        create_prop(first,321,'idea',raw)
        git(self.work,'add','.');git(self.work,'commit','-m','accept first proposal');git(self.work,'push','origin','main')
        self.w.start(kind='idea',issue=321,proposal=first.relative_to(self.work).as_posix(),slug='caves')
        git(self.work,'add','.');git(self.work,'commit','-m','complete first issue')
        bob=self.base/'bob';git(self.base,'clone',str(self.bare),str(bob))
        git(bob,'config','user.name','Bob');git(bob,'config','user.email','bob@example.invalid')
        second=bob/'00_INPUT/PROPOSALS/UPDATES/GH-000456_pets.txt';second.parent.mkdir(parents=True,exist_ok=True);second.write_bytes(b'New pets\r\n')
        second.with_suffix('.json').write_text(json.dumps({'schema_version':1,'issue':456,'key':'GH-000456','kind':'update','submitted_by':'bob','sha256':hashlib.sha256(second.read_bytes()).hexdigest(),'raw_file':second.relative_to(bob).as_posix()}))
        git(bob,'add','.');git(bob,'commit','-m','accept next proposal');git(bob,'push','origin','main')
        from unittest.mock import patch
        from types import SimpleNamespace
        old=self.w.run
        def intercept(argv,**kwargs):
            if argv[0]=='gh':return SimpleNamespace(stdout=json.dumps({'state':'MERGED','mergedAt':'2026-09-23T00:00:00Z','baseRefName':'main','headRefName':'feat/321-caves'}))
            return old(argv,**kwargs)
        with patch.object(workflow.shutil,'which',return_value='/mock/gh'),patch.object(self.w,'run',side_effect=intercept):
            self.w.next_task(after_pr=12,issue=456,kind='update',proposal=second.relative_to(bob).as_posix(),slug='pets')
        self.assertEqual(git(self.work,'branch','--show-current'),'feat/456-pets')
        self.assertEqual((self.work/'04_CHANGESETS/GH-000456_pets/USER_REQUEST.txt').read_bytes(),b'New pets\r\n')

    def test_next_task_refuses_unmerged_prior_pr(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        old=self.w.run
        def fake(argv, **kwargs):
            if argv[0]=='gh':return SimpleNamespace(stdout=json.dumps({'state':'OPEN','mergedAt':None,'baseRefName':'main','headRefName':'feat/321-caves'}))
            return old(argv,**kwargs)
        with patch.object(workflow.shutil,'which',return_value='/mock/gh'),patch.object(self.w,'run',side_effect=fake):
            with self.assertRaisesRegex(workflow.WorkflowError,'not verified as merged'):
                self.w.next_task(after_pr=12,issue=456,kind='update',proposal='unused.txt',slug='pets')
        self.assertEqual(git(self.work,'branch','--show-current'),'main')

    def test_merge_requires_other_human_and_refuses_headless_execution(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        response={'number':12,'author':{'login':'alice'},'body':'Refs #321',
                  'headRefName':'feat/321-caves','baseRefName':'main','headRefOid':'abc123',
                  'isDraft':False,'reviewDecision':'APPROVED','mergeStateStatus':'CLEAN',
                  'statusCheckRollup':[{'conclusion':'SUCCESS'}],'state':'OPEN',
                  'reviews':[{'state':'APPROVED','author':{'login':'bob'}}]}
        calls=[]
        old=self.w.run
        def fake(argv,**kwargs):
            calls.append(argv)
            if argv[0]=='gh' and argv[1:3]==['pr','view']:
                return SimpleNamespace(stdout=json.dumps(response))
            if argv[0]=='git':return old(argv,**kwargs)
            raise AssertionError('non-interactive test must not submit a merge')
        with patch.object(workflow.shutil,'which',return_value='/mock/gh'),patch.object(self.w,'run',side_effect=fake),patch.object(workflow.sys,'stdin',SimpleNamespace(isatty=lambda:False)):
            self.w.merge(issue=321,pr=12,confirm=False)
            with self.assertRaisesRegex(workflow.WorkflowError,'non-interactive'):
                self.w.merge(issue=321,pr=12,confirm=True)
            response['reviews']=[{'state':'APPROVED','author':{'login':'alice'}}]
            with self.assertRaisesRegex(workflow.WorkflowError,'another human'):
                self.w.merge(issue=321,pr=12,confirm=False)
        self.assertTrue(all(cmd[1:3]!=['pr','merge'] for cmd in calls))

    def test_rojo_layout_is_intentionally_scoped(self):
        sys.path.insert(0,str(ROOT/'scripts'))
        import validate_rojo_layout
        self.assertEqual(validate_rojo_layout.validate(ROOT),[])
        self.assertEqual(json.loads((ROOT/'default.project.json').read_text())['tree']['$ignoreUnknownInstances'],True)

if __name__=='__main__':unittest.main()
