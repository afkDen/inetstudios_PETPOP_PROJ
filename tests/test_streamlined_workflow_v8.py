from __future__ import annotations
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from streamlined_task import create_task,load_task,approve_task,reopen_approval,set_gates,validate_task


class StreamlinedWorkflowV8Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);(self.root/'04_CHANGESETS').mkdir()

    def create(self,data=b'Idea\r\nFear -> Sindak\r\n',risk='STANDARD'):
        source=self.root/'idea.txt';source.write_bytes(data)
        return create_task(source=source,issue=6,kind='idea',title='First slice',slug='first-slice',
                           branch='feat/6-first-slice',owner='test-owner',risk=risk,root=self.root)

    def test_raw_request_bytes_are_preserved_exactly(self):
        data=b'\xef\xbb\xbfUnang linya\r\nFear -> Sindak\nMixed\r\n'
        dst=self.create(data)
        meta=json.loads((dst/'TASK.json').read_text())
        self.assertEqual((dst/'USER_REQUEST.txt').read_bytes(),data)
        self.assertEqual(meta['request_sha256'],hashlib.sha256(data).hexdigest())
        self.assertEqual(validate_task(6,self.root),[])

    def test_normal_task_is_one_changeset_not_legacy_proposal_chain(self):
        dst=self.create()
        self.assertEqual({p.name for p in dst.iterdir()},
                         {'USER_REQUEST.txt','TASK.json','TASK.md','WORK_STATE.md','EVIDENCE.json'})
        self.assertFalse((self.root/'00_INPUT').exists())

    def test_tampered_request_fails_integrity(self):
        dst=self.create();(dst/'USER_REQUEST.txt').write_bytes(b'changed')
        self.assertIn('differs from recorded SHA-256','; '.join(validate_task(6,self.root)))

    def test_scope_approval_and_reopen_boundary(self):
        self.create();approve_task(6,'test-owner','approved slice',root=self.root)
        _,meta=load_task(6,self.root);self.assertEqual(meta['scope_approval']['status'],'APPROVED')
        self.assertEqual(validate_task(6,self.root,require_approved=True),[])
        reopen_approval(6,'changed risk',root=self.root)
        _,meta=load_task(6,self.root);self.assertEqual(meta['scope_approval']['status'],'PENDING')
        self.assertIn('human scope approval is still PENDING','; '.join(validate_task(6,self.root,require_approved=True)))

    def test_approved_scope_fingerprint_detects_post_approval_rewrite(self):
        dst=self.create();approve_task(6,'test-owner','approved',root=self.root)
        text=(dst/'TASK.md').read_text();(dst/'TASK.md').write_text(text.replace('## Acceptance criteria','## Acceptance criteria\n- [ ] silently expanded scope'))
        self.assertIn('scope changed after human approval','; '.join(validate_task(6,self.root)))

    def test_critical_risk_cannot_waive_deep_gates(self):
        self.create(risk='CRITICAL')
        set_gates(6,independent_review_required=False,full_quality_packet_required=False,root=self.root)
        _,meta=load_task(6,self.root)
        self.assertTrue(meta['gates']['independent_review_required'])
        self.assertTrue(meta['gates']['full_quality_packet_required'])

    def test_references_can_be_collaboratively_preserved(self):
        ref=self.root/'moodboard.png'; ref.write_bytes(b'not-a-real-image-fixture')
        source=self.root/'idea2.txt'; source.write_text('visual update')
        dst=create_task(source=source,issue=7,kind='update',title='Visual update',slug='visual-update',
                        branch='feat/7-visual-update',owner='test-owner',risk='STANDARD',
                        references=[str(ref),'https://example.com/reference'],root=self.root)
        meta=json.loads((dst/'TASK.json').read_text())
        self.assertEqual(len(meta['references']),2)
        self.assertTrue((dst/meta['references'][0]['path']).is_file())
        self.assertTrue((dst/'REFERENCES.md').is_file())
        self.assertEqual(validate_task(7,self.root),[])

    def test_profile_is_streamlined_and_keeps_human_remote_gates(self):
        cfg=json.loads((ROOT/'08_TOOLCHAIN/WORKFLOW_PROFILE.json').read_text())
        self.assertEqual(cfg['workflow_id'],'streamlined-v8.5')
        normal=cfg['normal_flow']
        self.assertFalse(normal['require_separate_proposal_branch'])
        self.assertFalse(normal['require_separate_proposal_pr'])
        self.assertFalse(normal['require_promotion_pr'])
        self.assertTrue(normal['require_scope_approval_before_substantial_implementation'])
        self.assertTrue(normal['require_second_human_for_substantial_pr'])
        self.assertFalse(normal['automatic_merge'])
        self.assertFalse(normal['automatic_roblox_publish'])

    def test_raw_request_git_attribute_is_binary_exact(self):
        text=(ROOT/'.gitattributes').read_text()
        self.assertIn('04_CHANGESETS/**/USER_REQUEST.txt -text',text)

    def test_public_docs_point_to_single_cli(self):
        for rel in ['README.md','START_HERE.md','TEAM_WORKFLOW.md','AGENTS.md']:
            text=(ROOT/rel).read_text()
            self.assertIn('scripts/team.py',text,rel)


if __name__=='__main__':unittest.main()
