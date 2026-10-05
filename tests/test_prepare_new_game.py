"""Safe new-game identity binding must never overwrite source history or local proof."""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import prepare_new_game as new

class NewGamePreparationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.src = self.base/'source'
        for folder in ['scripts', '08_TOOLCHAIN', '.github', 'templates']:
            (self.src/folder).mkdir(parents=True, exist_ok=True)
        self.policy={'remote_url':new.SOURCE_URL,'human_integrators':['REPLACE_MAINTAINER'],'template_unconfigured':True}
        (self.src/'08_TOOLCHAIN/TEAM_POLICY.json').write_text(json.dumps(self.policy))
        (self.src/'.github/CODEOWNERS').write_text('/AGENTS.md @REPLACE_MAINTAINER\n')
        for f in ['TEAM_ONBOARDING.md','TEAM_PROTOCOL.md','TEAM_IMPORT_GITHUB.md','NEW_GAME_SETUP.md']:
            (self.src/f).write_text(new.SOURCE_URL + '\n')
        (self.src/'default.project.json').write_text(json.dumps({'name':'REPLACE_REPOSITORY', 'tree':{}}))
        (self.src/'templates/rojo-world-opt-in.project.json').write_text(json.dumps({'name':'REPLACE_REPOSITORY-world-opt-in-EXAMPLE'}))
        (self.src/'AGENTS.md').write_text('canonical source')
        (self.src/'.env.local').write_text('LOCAL_SECRET=should-not-copy')
        (self.src/'.git').mkdir()
        (self.src/'.git/config').write_text('source history must stay source-local')
        (self.src/'.local').mkdir()
        (self.src/'.local/RUNTIME_VALIDATIONS.json').write_text('false PASS')
        (self.src/'build').mkdir()
        (self.src/'build/old-place.rbxlx').write_text('old')

    def test_binds_only_new_game_and_never_copies_old_evidence(self):
        dest=self.base/'fresh'
        url='https://github.com/example-owner/NEW-Game.git'
        with patch.object(new,'ROOT',self.src):
            new.preflight(dest,url)
            dest.mkdir()
            new.copy_scaffold(dest)
            new.bind(dest,url,'example-owner','NEW-Game')
        policy=json.loads((dest/'08_TOOLCHAIN/TEAM_POLICY.json').read_text())
        self.assertFalse(policy['template_unconfigured'])
        self.assertEqual(policy['remote_url'],url)
        self.assertEqual(policy['human_integrators'],['example-owner'])
        self.assertEqual((dest/'default.project.json').read_text().count('NEW-Game'),1)
        self.assertEqual(json.loads((dest/'PREPARED_GAME.json').read_text())['global_bootstrap_status'],'INITIALIZATION_REQUIRED')
        self.assertIn('@example-owner',(dest/'.github/CODEOWNERS').read_text())
        self.assertFalse((dest/'.env.local').exists())
        self.assertFalse((dest/'.git').exists())
        self.assertFalse((dest/'.local').exists())
        self.assertFalse((dest/'build').exists())
        self.assertEqual((self.src/'08_TOOLCHAIN/TEAM_POLICY.json').read_text(),json.dumps(self.policy))

    def test_initializer_refuses_template_and_wrong_remote_before_writes(self):
        import initialize_project as init
        with patch.object(init,'ROOT',self.src):
            with self.assertRaisesRegex(SystemExit,'template is unconfigured'):
                init.require_correct_repository()
        prepared=self.base/'prepared'
        with patch.object(new,'ROOT',self.src):
            new.preflight(prepared,'https://github.com/example-owner/new-validated-game.git')
            prepared.mkdir();new.copy_scaffold(prepared)
            new.bind(prepared,'https://github.com/example-owner/new-validated-game.git','example-owner','new-validated-game')
        subprocess.run(['git','init','--quiet',str(prepared)],check=True)
        subprocess.run(['git','-C',str(prepared),'remote','add','origin','https://github.com/example-owner/wrong-game.git'],check=True)
        with patch.object(init,'ROOT',prepared),patch.object(init,'run',return_value=type('Result',(),{'returncode':0,'stdout':'https://github.com/example-owner/wrong-game.git\n'})()):
            with self.assertRaisesRegex(SystemExit,'origin differs'):
                init.require_correct_repository()
        self.assertFalse((prepared/'.local').exists())

    def test_promotion_issue_url_comes_from_target_policy(self):
        import submit_proposal, promote_proposal
        target=self.base/'project'
        for d in ['00_INPUT/PROPOSALS/IDEAS','00_INPUT/GAME_IDEA','08_TOOLCHAIN']:
            (target/d).mkdir(parents=True,exist_ok=True)
        policy=dict(self.policy,template_unconfigured=False,remote_url='https://github.com/example-owner/ANOTHER-game.git')
        (target/'08_TOOLCHAIN/TEAM_POLICY.json').write_text(json.dumps(policy))
        source=target/'idea.txt';source.write_text('my game idea')
        submit_proposal.add_proposal(source,123,'example-owner','idea',target)
        promoted=promote_proposal.promote(123,'idea','example-owner',root=target,allow_test_branch=True)
        metadata=json.loads(promoted.with_name('APPROVAL.json').read_text())
        self.assertEqual(metadata['github_issue_url'],'https://github.com/example-owner/ANOTHER-game/issues/123')
        self.assertFalse(metadata['github_review_verified_by_script'])

    def test_rejects_populated_and_original_game_targets(self):
        target=self.base/'existing';target.mkdir()
        marker=target/'Important.uncommitted';marker.write_text('keep this')
        with patch.object(new,'ROOT',self.src):
            with self.assertRaisesRegex(ValueError,'not empty'):
                new.preflight(target,'https://github.com/example-owner/new-game.git')
            with self.assertRaisesRegex(ValueError,'separate'):
                new.preflight(self.src,'https://github.com/example-owner/new-game.git')
        self.assertEqual(marker.read_text(),'keep this')
        for u in ['https://username:token@github.com/a/repo.git','https://github.com/a/repo.git?token=secret', 'https://github.com/a/../b.git']:
            with self.subTest(url=u):
                with self.assertRaises(ValueError):new.parse_url(u)

    def test_allows_matching_empty_git_clone_but_not_wrong_origin(self):
        target=self.base/'gitclone';target.mkdir()
        subprocess.run(['git','init','--quiet',str(target)],check=True)
        subprocess.run(['git','-C',str(target),'remote','add','origin','git@github.com:example-owner/SECOND-game.git'],check=True)
        with patch.object(new,'ROOT',self.src):
            new.preflight(target,'https://github.com/example-owner/SECOND-game.git')
            with self.assertRaisesRegex(ValueError,'origin differs'):
                new.preflight(target,'https://github.com/example-owner/different-game.git')
        self.assertTrue((target/'.git').is_dir())
        self.assertEqual(list(target.iterdir()),[target/'.git'])

if __name__=='__main__':unittest.main()
