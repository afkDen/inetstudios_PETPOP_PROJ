from __future__ import annotations
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from streamlined_task import (
    approve_scope_amendment, approve_task, attest_evidence_scope, create_scope_amendment,
    create_task, load_task, reopen_approval, scope_fingerprint, set_gates, validate_task, withdraw_scope_amendment,
)
from validate_studio_delivery import validate_delivery
from validate_feature_evidence import validate_packet


class ScopeEvolutionV85Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);(self.root/'04_CHANGESETS').mkdir()
        src=self.root/'request.txt';src.write_text('Build the accepted feature slice.\n',encoding='utf-8')
        self.dst=create_task(source=src,issue=42,kind='update',title='Scope test',slug='scope-test',
                             branch='feat/42-scope-test',owner='alice',risk='STANDARD',root=self.root)

    def approve_initial(self):
        approve_task(42,'alice','initial scope',studio_required=False,root=self.root)
        return load_task(42,self.root)[1]

    def draft(self,change='Add ranked queue'):
        path=create_scope_amendment(42,'user requested post-approval change','alice',root=self.root)
        text=path.read_text(encoding='utf-8')
        path.write_text(text.replace('### Add\n- ',f'### Add\n- {change}'),encoding='utf-8')
        return path

    def test_initial_approval_creates_revision_one(self):
        meta=self.approve_initial()
        self.assertEqual(meta['scope_revision'],1)
        self.assertEqual(meta['scope_approval']['revision'],1)
        self.assertEqual(meta['scope_approval']['approval_kind'],'INITIAL')
        self.assertEqual([x['revision'] for x in meta['scope_history']],[1])
        self.assertEqual(validate_task(42,self.root,require_approved=True),[])

    def test_draft_amendment_does_not_invalidate_current_scope(self):
        self.approve_initial();self.draft()
        meta=load_task(42,self.root)[1]
        self.assertEqual(meta['scope_revision'],1)
        self.assertEqual(meta['scope_approval']['status'],'APPROVED')
        self.assertEqual(meta['scope_amendments'][0]['status'],'DRAFT')
        self.assertEqual(validate_task(42,self.root,require_approved=True),[])
        self.assertIn('scope amendment 1 is still DRAFT','; '.join(validate_task(42,self.root,require_approved=True,require_delivery=True)))

    def test_approved_amendment_advances_revision_and_preserves_history(self):
        self.approve_initial();self.draft()
        approve_scope_amendment(42,1,'alice','approved addition',studio_required=False,root=self.root)
        meta=load_task(42,self.root)[1]
        self.assertEqual(meta['scope_revision'],2)
        self.assertEqual([x['revision'] for x in meta['scope_history']],[1,2])
        self.assertEqual(meta['scope_history'][-1]['approval_kind'],'AMENDMENT')
        self.assertEqual(meta['scope_history'][-1]['amendment_id'],1)
        self.assertEqual(meta['scope_amendments'][0]['status'],'APPROVED')
        self.assertEqual(validate_task(42,self.root,require_approved=True),[])

    def test_approved_amendment_is_immutable(self):
        self.approve_initial();path=self.draft();approve_scope_amendment(42,1,'alice',root=self.root)
        path.write_text(path.read_text(encoding='utf-8').replace('Add ranked queue','Add hidden admin powers'),encoding='utf-8')
        self.assertIn('finalized scope amendment 1 changed after decision','; '.join(validate_task(42,self.root)))

    def test_withdrawn_amendment_does_not_advance_revision_and_is_immutable(self):
        self.approve_initial();path=self.draft()
        withdraw_scope_amendment(42,1,'alice','changed my mind',root=self.root)
        meta=load_task(42,self.root)[1]
        self.assertEqual(meta['scope_revision'],1)
        self.assertEqual(meta['scope_amendments'][0]['status'],'WITHDRAWN')
        self.assertEqual(validate_task(42,self.root,require_approved=True),[])
        path.write_text(path.read_text(encoding='utf-8').replace('Add ranked queue','tampered'),encoding='utf-8')
        self.assertIn('finalized scope amendment 1 changed after decision','; '.join(validate_task(42,self.root)))

    def test_post_approval_gate_mutation_requires_amendment(self):
        self.approve_initial()
        with self.assertRaisesRegex(ValueError,'approved scope'):
            set_gates(42,studio_required=True,root=self.root)
        self.draft('Require live Studio acceptance')
        approve_scope_amendment(42,1,'alice',studio_required=True,evidence_impact='refresh-affected',root=self.root)
        meta=load_task(42,self.root)[1]
        self.assertTrue(meta['gates']['studio_required'])
        self.assertEqual(meta['scope_revision'],2)

    def test_default_amendment_preserves_but_stales_evidence_until_attested(self):
        self.approve_initial()
        ev=json.loads((self.dst/'EVIDENCE.json').read_text())
        self.assertEqual(ev['scope_revision'],1)
        self.draft();approve_scope_amendment(42,1,'alice',studio_required=False,evidence_impact='refresh-affected',root=self.root)
        ev=json.loads((self.dst/'EVIDENCE.json').read_text())
        self.assertEqual(ev['scope_revision'],1)
        self.assertEqual(ev['required_scope_revision'],2)
        self.assertEqual(ev['scope_attestation'],{})
        self.assertIn('delivery evidence is not attested for current scope revision 2','; '.join(validate_task(42,self.root,require_delivery=True)))
        attest_evidence_scope(42,'alice','reviewed affected evidence and refreshed what changed',root=self.root)
        ev=json.loads((self.dst/'EVIDENCE.json').read_text())
        self.assertEqual(ev['scope_revision'],2)
        self.assertEqual(ev['scope_attestation']['revision'],2)

    def test_retain_evidence_is_explicit_human_choice(self):
        self.approve_initial();self.draft('Clarify copy only; behavior unchanged')
        approve_scope_amendment(42,1,'alice','existing verification remains applicable',studio_required=False,evidence_impact='retain',root=self.root)
        ev=json.loads((self.dst/'EVIDENCE.json').read_text())
        self.assertEqual(ev['scope_revision'],2)
        self.assertEqual(ev['required_scope_revision'],2)
        self.assertEqual(ev['scope_attestation']['mode'],'human-approved-retain')


    def test_gate_deescalation_requires_human_note(self):
        approve_task(42,'alice','initial critical scope',risk='CRITICAL',studio_required=True,root=self.root)
        path=create_scope_amendment(42,'remove Studio-dependent critical behavior','alice',root=self.root)
        path.write_text(path.read_text().replace('### Remove / defer\n- ','### Remove / defer\n- Remove the critical Studio-dependent behavior'))
        with self.assertRaisesRegex(ValueError,'approval note'):
            approve_scope_amendment(42,1,'alice',risk='STANDARD',studio_required=False,independent_review_required=False,full_quality_packet_required=False,root=self.root)

    def test_critical_risk_downgrade_requires_substantive_scope_change(self):
        approve_task(42,'alice','initial critical scope',risk='CRITICAL',studio_required=True,root=self.root)
        create_scope_amendment(42,'just lower risk','alice',root=self.root)
        with self.assertRaisesRegex(ValueError,'substantive scope change'):
            approve_scope_amendment(42,1,'alice','critical behavior removed',risk='STANDARD',root=self.root)

    def test_retain_evidence_requires_human_note(self):
        self.approve_initial();self.draft('Clarify wording only')
        with self.assertRaisesRegex(ValueError,'retaining existing evidence'):
            approve_scope_amendment(42,1,'alice',evidence_impact='retain',root=self.root)


    def test_retain_rebinds_existing_heavy_receipts_with_audit_note(self):
        self.approve_initial()
        for template_name,out_name in (('STUDIO_DELIVERY_TEMPLATE.json','STUDIO_DELIVERY.json'),('QUALITY_EVIDENCE_TEMPLATE.json','QUALITY_EVIDENCE.json')):
            doc=json.loads((ROOT/'templates'/template_name).read_text())
            doc['issue']=42;doc['scope_revision']=1
            if out_name=='QUALITY_EVIDENCE.json':doc['branch']='feat/42-scope-test'
            (self.dst/out_name).write_text(json.dumps(doc,indent=2)+'\n')
        self.draft('Clarify behavior without changing verification')
        approve_scope_amendment(42,1,'alice','Reviewed: existing Studio and quality observations remain applicable',studio_required=False,evidence_impact='retain',root=self.root)
        for name in ('STUDIO_DELIVERY.json','QUALITY_EVIDENCE.json'):
            doc=json.loads((self.dst/name).read_text())
            self.assertEqual(doc['scope_revision'],2)
            self.assertEqual(doc['scope_rebind']['revision'],2)
            self.assertEqual(doc['scope_rebind']['by'],'alice')

    def test_evidence_scope_rebinds_existing_heavy_receipts_but_reset_does_not(self):
        self.approve_initial()
        for template_name,out_name in (('STUDIO_DELIVERY_TEMPLATE.json','STUDIO_DELIVERY.json'),('QUALITY_EVIDENCE_TEMPLATE.json','QUALITY_EVIDENCE.json')):
            doc=json.loads((ROOT/'templates'/template_name).read_text());doc['issue']=42;doc['scope_revision']=1
            if out_name=='QUALITY_EVIDENCE.json':doc['branch']='feat/42-scope-test'
            (self.dst/out_name).write_text(json.dumps(doc,indent=2)+'\n')
        self.draft();approve_scope_amendment(42,1,'alice','refresh affected',studio_required=False,evidence_impact='refresh-affected',root=self.root)
        self.assertEqual(json.loads((self.dst/'STUDIO_DELIVERY.json').read_text())['scope_revision'],1)
        attest_evidence_scope(42,'alice','Reviewed/refreshed affected evidence',root=self.root)
        self.assertEqual(json.loads((self.dst/'STUDIO_DELIVERY.json').read_text())['scope_revision'],2)

    def test_legacy_full_reopen_refuses_unresolved_draft_amendment(self):
        self.approve_initial();self.draft()
        with self.assertRaisesRegex(ValueError,'withdraw the DRAFT'):
            reopen_approval(42,'base repair',root=self.root)

    def test_empty_amendment_cannot_be_approved(self):
        self.approve_initial();create_scope_amendment(42,'empty proposal','alice',root=self.root)
        with self.assertRaisesRegex(ValueError,'no substantive scope or gate change'):
            approve_scope_amendment(42,1,'alice',root=self.root)

    def test_orphan_amendment_file_fails_integrity(self):
        self.approve_initial()
        folder=self.dst/'SCOPE_AMENDMENTS';folder.mkdir();(folder/'AMENDMENT-9999.md').write_text('orphan')
        self.assertIn('unregistered scope amendment file','; '.join(validate_task(42,self.root)))

    def test_legacy_full_reopen_reapproval_preserves_history_and_increments_revision(self):
        self.approve_initial();self.draft();approve_scope_amendment(42,1,'alice',studio_required=False,root=self.root)
        reopen_approval(42,'base repair',root=self.root)
        text=(self.dst/'TASK.md').read_text(encoding='utf-8').replace('## Acceptance criteria','## Acceptance criteria\n- [ ] corrected base criterion')
        (self.dst/'TASK.md').write_text(text,encoding='utf-8')
        approve_task(42,'alice','base repaired',studio_required=False,root=self.root)
        meta=load_task(42,self.root)[1]
        self.assertEqual(meta['scope_revision'],3)
        self.assertEqual([x['revision'] for x in meta['scope_history']],[1,2,3])
        self.assertEqual(meta['scope_history'][-1]['approval_kind'],'BASE_REAPPROVAL')
        self.assertEqual(validate_task(42,self.root,require_approved=True),[])

    def test_history_tamper_is_detected(self):
        self.approve_initial()
        meta=json.loads((self.dst/'TASK.json').read_text())
        meta['scope_history'][0]['approved_by']='mallory'
        (self.dst/'TASK.json').write_text(json.dumps(meta,indent=2)+'\n')
        self.assertIn('scope approval history fingerprint mismatch','; '.join(validate_task(42,self.root)))


    def test_amendment_references_are_copied_hashed_and_bound_to_decision(self):
        self.approve_initial()
        supporting=self.root/'revised-brief.txt'
        supporting.write_bytes(b'line one\r\nline two\r\n')
        path=create_scope_amendment(42,'revised brief arrived','alice',[str(supporting),'https://example.com/spec'],root=self.root)
        text=path.read_text(encoding='utf-8')
        path.write_text(text.replace('### Add\n- ','### Add\n- Apply revised brief'),encoding='utf-8')
        meta=load_task(42,self.root)[1]
        refs=meta['scope_amendments'][0]['references']
        self.assertEqual(len(refs),2)
        copied=self.dst/refs[0]['path']
        self.assertEqual(copied.read_bytes(),b'line one\r\nline two\r\n')
        approve_scope_amendment(42,1,'alice',studio_required=False,root=self.root)
        self.assertEqual(validate_task(42,self.root),[])
        copied.write_bytes(b'tampered\n')
        errors='; '.join(validate_task(42,self.root))
        self.assertIn('amendment reference file hash mismatch',errors)

    def test_finalized_amendment_reference_metadata_tamper_is_detected(self):
        self.approve_initial()
        supporting=self.root/'brief.txt';supporting.write_text('brief',encoding='utf-8')
        path=create_scope_amendment(42,'supporting brief','alice',[str(supporting)],root=self.root)
        path.write_text(path.read_text().replace('### Add\n- ','### Add\n- Brief-driven change'))
        approve_scope_amendment(42,1,'alice',studio_required=False,root=self.root)
        meta=json.loads((self.dst/'TASK.json').read_text())
        meta['scope_amendments'][0]['references'][0]['name']='other.txt'
        (self.dst/'TASK.json').write_text(json.dumps(meta,indent=2)+'\n')
        self.assertIn('reference provenance changed after decision','; '.join(validate_task(42,self.root)))

    def test_legacy_metadata_upgrade_does_not_stale_unchanged_evidence(self):
        self.approve_initial()
        meta=json.loads((self.dst/'TASK.json').read_text())
        task_text=(self.dst/'TASK.md').read_text()
        approval=dict(meta['scope_approval'])
        approval.pop('revision',None);approval.pop('approval_kind',None)
        approval['scope_sha256']=scope_fingerprint(task_text)
        for key in ('scope_revision','scope_base_sha256','scope_history','scope_history_sha256','scope_amendments'):
            meta.pop(key,None)
        meta['schema_version']=3;meta['workflow']='streamlined-v8.3';meta['scope_approval']=approval
        (self.dst/'TASK.json').write_text(json.dumps(meta,indent=2)+'\n')
        ev=json.loads((self.dst/'EVIDENCE.json').read_text())
        for key in ('scope_revision','required_scope_revision','scope_attestation'):
            ev.pop(key,None)
        ev['schema_version']=1
        (self.dst/'EVIDENCE.json').write_text(json.dumps(ev,indent=2)+'\n')
        create_scope_amendment(42,'post-migration proposal','alice',root=self.root)
        ev=json.loads((self.dst/'EVIDENCE.json').read_text())
        self.assertEqual(ev['scope_revision'],1)
        self.assertEqual(ev['required_scope_revision'],1)
        self.assertEqual(ev['scope_attestation']['mode'],'legacy-migration')

    def test_v85_studio_and_quality_receipts_are_bound_to_scope_revision(self):
        self.approve_initial()
        studio=json.loads((ROOT/'templates/STUDIO_DELIVERY_TEMPLATE.json').read_text())
        studio['issue']=42;studio['scope_revision']=0
        studio_path=self.dst/'STUDIO_DELIVERY.json';studio_path.write_text(json.dumps(studio,indent=2)+'\n')
        self.assertIn('Studio receipt scope revision does not match TASK.json','; '.join(validate_delivery(studio_path,self.root,expect_issue=42)))
        quality=json.loads((ROOT/'templates/QUALITY_EVIDENCE_TEMPLATE.json').read_text())
        quality['issue']=42;quality['branch']='feat/42-scope-test';quality['scope_revision']=0
        quality_path=self.dst/'QUALITY_EVIDENCE.json';quality_path.write_text(json.dumps(quality,indent=2)+'\n')
        self.assertIn('quality packet scope revision does not match TASK.json','; '.join(validate_packet(quality_path,self.root)))


    def test_crlf_amendment_reference_survives_real_git_roundtrip(self):
        payload=b'alpha\r\nbeta\r\n'
        with tempfile.TemporaryDirectory() as tmp:
            origin=Path(tmp)/'origin';clone=Path(tmp)/'clone';origin.mkdir()
            def git(repo,*args):
                return subprocess.run(['git',*args],cwd=repo,capture_output=True,check=True)
            git(origin,'init');git(origin,'config','user.name','fixture');git(origin,'config','user.email','fixture@example.invalid');git(origin,'config','core.autocrlf','true')
            (origin/'.gitattributes').write_bytes((ROOT/'.gitattributes').read_bytes())
            ref=origin/'04_CHANGESETS/GH-000042_scope-test/SCOPE_AMENDMENTS/REFERENCES/AMENDMENT-0001/01_notes.txt'
            ref.parent.mkdir(parents=True);ref.write_bytes(payload)
            git(origin,'add','.gitattributes',ref.relative_to(origin).as_posix());git(origin,'commit','-m','fixture')
            blob=subprocess.run(['git','show','HEAD:'+ref.relative_to(origin).as_posix()],cwd=origin,capture_output=True,check=True).stdout
            self.assertEqual(blob,payload);self.assertEqual(hashlib.sha256(blob).hexdigest(),hashlib.sha256(payload).hexdigest())
            subprocess.run(['git','-c','core.autocrlf=true','clone',str(origin),str(clone)],capture_output=True,check=True)
            self.assertEqual((clone/ref.relative_to(origin)).read_bytes(),payload)

    def test_cross_platform_attribute_covers_scope_amendments(self):
        self.assertIn('04_CHANGESETS/**/SCOPE_AMENDMENTS/** -text',(ROOT/'.gitattributes').read_text())

    def test_workflow_contract_is_revisioned(self):
        profile=json.loads((ROOT/'08_TOOLCHAIN/WORKFLOW_PROFILE.json').read_text())
        self.assertEqual(profile['workflow_id'],'streamlined-v8.5')
        self.assertTrue(profile['normal_flow']['require_scope_amendment_approval_after_initial_approval'])
        self.assertTrue(profile['normal_flow']['preserve_prior_scope_approvals'])
        self.assertIn('team.py amend',(ROOT/'TEAM_WORKFLOW.md').read_text())
        self.assertTrue((ROOT/'08_TOOLCHAIN/SCOPE_EVOLUTION_V8_5.md').is_file())


if __name__=='__main__':
    unittest.main()
