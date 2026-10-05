from __future__ import annotations
import json,subprocess,sys,tempfile,unittest,zlib,struct
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import validate_feature_evidence as ev,bootstrap_dev_tools as tool
def png_fixture(width=400,height=240):
    def chunk(name,body):
        data=name+body
        return struct.pack('>I',len(body))+data+struct.pack('>I',zlib.crc32(data)&0xffffffff)
    header=chunk(b'IHDR',struct.pack('>2I5B',width,height,8,2,0,0,0))
    pixels=b''.join([b'\x00'+b'\x80\x80\x80'*width for _ in range(height)])
    return b'\x89PNG\r\n\x1a\n'+header+chunk(b'IDAT',zlib.compress(pixels))+chunk(b'IEND',b'')
PNG=png_fixture() # deterministic source-only test fixture; not a real Studio capture
class ProductionQualityTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.d=self.root/'04_CHANGESETS/GH-000123_rocks';self.d.mkdir(parents=True)
        (self.d/'QUALITY_BRIEF.md').write_text('# approved mock brief for unit fixture\n')
        (self.d/'functional.txt').write_text('Real session evidence fixture; test verifies paths only')
        (self.d/'console.txt').write_text('No errors (test fixture only)')
        (self.d/'studio.txt').write_text('Simulated studio operator proof; test only checks schema')
        (self.d/'reviews.md').write_text('# simulated independent review')
        (self.d/'screen.png').write_bytes(PNG)
        (self.d/'ui.png').write_bytes(PNG)
        (self.d/'ui-interactions.txt').write_text('Test fixture')
        sp=self.root/'.agents/skills/visual-production';sp.mkdir(parents=True);(sp/'SKILL.md').write_text('# skill')
        self.j={'schema_version':1,'issue':123,'branch':'feat/123-rocks','status':'ACCEPTANCE_READY','quality_brief':'04_CHANGESETS/GH-000123_rocks/QUALITY_BRIEF.md','art_direction':{'required':True,'human_approved':True,'reviewer':'alice','approval_reference':'PR #12 comment'},'skill_use_receipts':[{'role':'content-production-worker','skill':'visual-production','loaded_from':'.agents/skills/visual-production/SKILL.md','purpose':'rock family','output':'04_CHANGESETS/GH-000123_rocks/studio.txt'}],'placeholders':[],'functional_tests':[{'scenario':'mine a rock','operator':'op1','commit':'abc','result':'PASS','evidence':'04_CHANGESETS/GH-000123_rocks/functional.txt','console':'04_CHANGESETS/GH-000123_rocks/console.txt'}],'live_studio':{'status':'PASS','operator':'op1','test_place':'disposable','commit':'abc','evidence':'04_CHANGESETS/GH-000123_rocks/studio.txt'},'visual_review':{'status':'PASS','reviewer':'viewer','screenshots':['04_CHANGESETS/GH-000123_rocks/screen.png'],'notes':'fixture'},'ui_review':{'status':'PASS','reviewer':'ux','device_screenshots':['04_CHANGESETS/GH-000123_rocks/ui.png'],'interaction_evidence':'04_CHANGESETS/GH-000123_rocks/ui-interactions.txt'},'independent_review':{'implementers':['builder'],'reviewers':['viewer','ux'],'report':'04_CHANGESETS/GH-000123_rocks/reviews.md'},'human_integration_approval':'PENDING'}
        self.receipt_path=self.d/'STUDIO_DELIVERY.json'
        self.j['studio_delivery_receipt']='04_CHANGESETS/GH-000123_rocks/STUDIO_DELIVERY.json'
        self.receipt={'schema_version':1,'issue':123,'status':'PASS','operator':'fixture-operator',
          'git_commit':'abc','target':{'name':'fixture-baseplate','studio_instance_id':'fixture-session','place_id':None,'human_confirmed':True},
          'mcp':{'selected_client':'fixture-runtime','connected':True,'probes':{'list_roblox_studios':'fixture response','get_studio_state':'fixture response','search_game_tree':'fixture response'},
                 'raw_probe_evidence':'04_CHANGESETS/GH-000123_rocks/studio.txt'},
          'rojo':{'project':'default.project.json','source_commit':'abc','serve_command':'rojo serve default.project.json','plugin_connected':True,
                  'managed_path':'ReplicatedStorage/GameShared','marker_proof':'04_CHANGESETS/GH-000123_rocks/studio.txt'},
          'playtest':{'started_and_stopped':True,'scenario':'fixture movement','observed_result':'fixture-only',
                      'console':'04_CHANGESETS/GH-000123_rocks/console.txt','screenshot':'04_CHANGESETS/GH-000123_rocks/screen.png','input_trace':'04_CHANGESETS/GH-000123_rocks/functional.txt'},
          'human_verification':{'reviewer':'fixture-human','reference':'fixture-only'}}
        self.receipt_path.write_text(json.dumps(self.receipt))
        self.packet=self.d/'QUALITY_EVIDENCE.json'
        self.dump()
    def tearDown(self):self.temp.cleanup()
    def dump(self):self.packet.write_text(json.dumps(self.j,indent=2))
    def errors(self):self.dump();return ev.validate_packet(self.packet,self.root)
    def test_populated_fixture_structurally_valid_without_claiming_genuine_playtest(self):self.assertEqual(self.errors(),[])
    def test_draft_or_pending_live_evidence_blocks(self):
        self.j['status']='DRAFT';self.j['live_studio']['status']='PENDING';self.assertTrue(self.errors())
    def test_missing_skill_receipt_blocks(self):
        self.j['skill_use_receipts'][0]['loaded_from']='.agents/skills/absent/SKILL.md';self.assertIn('skill use receipts', ' '.join(self.errors()))
    def test_missing_human_art_approval_blocks(self):
        self.j['art_direction']['human_approved']=False;self.assertIn('art direction',' '.join(self.errors()))
    def test_unresolved_placeholder_blocks(self):
        self.j['placeholders']=[{'path':'Workspace/Brick1','purpose':'BLOCKOUT','removed_or_approved_as_final':False}];self.assertIn('placeholders',' '.join(self.errors()))
    def test_same_implementer_and_reviewer_blocks(self):
        self.j['independent_review']['reviewers']=['builder'];self.assertIn('reviewer separation',' '.join(self.errors()))
    def test_fake_screenshot_bytes_block(self):
        (self.d/'screen.png').write_bytes(b'not really an image but is named png');self.assertIn('visual review',' '.join(self.errors()))
    def test_backend_only_visual_na_requires_explanation(self):
        self.j['art_direction']['required']=False
        self.j['visual_review']={'status':'NOT_APPLICABLE','rationale':'Server-only inventory idempotency fix: no rendering changed'}
        self.j['ui_review']={'status':'NOT_APPLICABLE','rationale':'No player UI changed'}
        self.assertEqual(self.errors(),[])
        self.j['visual_review']['rationale']=''
        self.assertIn('visual N/A',' '.join(self.errors()))
    def test_visual_na_for_art_required_is_blocked(self):
        self.j['visual_review']={'status':'NOT_APPLICABLE','rationale':'Skipped'}
        self.assertIn('visual N/A',' '.join(self.errors()))
    def test_1px_placeholder_image_blocks(self):
        (self.d/'screen.png').write_bytes(png_fixture(1,1))
        self.assertIn('visual review',' '.join(self.errors()))
    def test_missing_console_transcript_blocks(self):
        self.j['functional_tests'][0]['console']='04_CHANGESETS/GH-000123_rocks/notthere.txt'
        self.assertIn('functional tests',' '.join(self.errors()))
    def test_missing_skill_output_blocks(self):
        self.j['skill_use_receipts'][0]['output']='missing.txt'
        self.assertIn('skill use receipts',' '.join(self.errors()))
    def test_committed_src_change_requires_quality_packet(self):
        repo=self.root/'git-demo';(repo/'src').mkdir(parents=True)
        def git(*args):return subprocess.run(['git',*args],cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
        git('init','-q','-b','main')
        (repo/'src/a.luau').write_text('return {}\n')
        git('add','.');git('-c','user.name=fixture','-c','user.email=fixture@local.invalid','commit','-qm','baseline')
        git('checkout','-qb','feat/123-test')
        (repo/'src/a.luau').write_text('return {ok=true}\n')
        git('add','.');git('-c','user.name=fixture','-c','user.email=fixture@local.invalid','commit','-qm','code change')
        self.assertEqual(ev.changed_src(repo,'main'),['src/a.luau'])
    def test_unsafe_path_blocks(self):
        self.j['quality_brief']='../../etc/passwd';self.assertIn('QUALITY_BRIEF',' '.join(self.errors()))
    def test_wrong_issue_blocks(self):
        self.j['issue']=124;self.assertIn('issue ID',' '.join(self.errors()))
    def test_tool_probe_does_not_guess_plugin_and_detects_versions(self):
        def fake_which(x):return '/bin/'+x if x in ('rokit','rojo','stylua') else None
        def fake_run(cmd,**kwargs):return SimpleNamespace(returncode=0,stdout=tool.EXPECTED[cmd[0]],stderr='')
        r=tool.probe(fake_which,fake_run);self.assertTrue(r['rojo']['version_verified']);self.assertFalse(r['selene']['found']);self.assertEqual(r['studio_plugin']['status'],'MANUAL_VERIFICATION_REQUIRED')
    def test_dev_toolchain_gate_refuses_missing_binaries(self):
        from unittest.mock import patch
        import initialize_project
        original=sys.argv
        try:
            sys.argv=['initialize_project.py','--record-runtime','developer_toolchain','PASS','--runtime','fixture']
            # Unit-test the developer-tool gate itself. The reusable template is
            # deliberately unconfigured, so bypass only the repository-identity
            # precondition to reach the gate under test.
            with patch.object(initialize_project,'require_correct_repository',return_value=None), \
                 patch('bootstrap_dev_tools.probe',return_value={n:{'version_verified':False} for n in tool.EXPECTED}):
                with self.assertRaisesRegex(SystemExit,'BLOCKED: cannot record developer_toolchain PASS'):
                    initialize_project.main()
        finally:sys.argv=original
    def test_team_quality_contract_ci_and_roles(self):
        r=json.loads((ROOT/'08_TOOLCHAIN/ROLE_CONTRACTS/roles.json').read_text())['roles'];names={x['id'] for x in r}
        self.assertTrue({'creative-director','frontend-worker','assurance-reviewer'}<=names)
        self.assertIn('image.inspect',next(x for x in r if x['id']=='assurance-reviewer')['required_capabilities'])
        self.assertTrue(all(x['fresh_context_required'] and x['write_policy']=='read-only' for x in r if x['id']=='assurance-reviewer'))
        ci=(ROOT/'.github/workflows/portable-ci.yml').read_text()
        self.assertIn('validate_ci_task.py --compare origin/main',ci)
        self.assertIn('bootstrap_dev_tools.py --check',ci)
        self.assertIn('stylua --check src',ci)
        self.assertIn("'developer_toolchain'", (ROOT/'scripts/initialize_project.py').read_text())
    def test_declared_tools_do_not_pretend_installed(self):
        script=(ROOT/'scripts/bootstrap_dev_tools.py').read_text();self.assertIn('Rokit is not installed',script)
        self.assertIn('--install-plugin',script);self.assertIn('Studio plugin + Studio MCP: manual live verification',script)
if __name__=='__main__':unittest.main()
