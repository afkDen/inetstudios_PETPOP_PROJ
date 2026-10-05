"""Portable contract/negative fixtures only: never mislabel as real Studio MCP tests."""
from __future__ import annotations
import importlib.util,json,shutil,struct,subprocess,sys,tempfile,unittest,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import validate_initialization_studio as vst
import workstation_preflight as wp
import initialize_project as ip

def valid_fixture_png():
    def chunk(tag,data):return struct.pack('!I',len(data))+tag+data+struct.pack('!I',zlib.crc32(tag+data)&0xffffffff)
    # Local fake PNG used exclusively by schema tests, NOT a claimed Studio screenshot.
    row=b'\0'+b'\xaa\xbb\xcc'*320
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('!IIBBBBB',320,180,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(row*180))+chunk(b'IEND',b'')

class FullWorkstationInitializationContract(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.root=Path(self.t.name);(self.root/'.local').mkdir()
        doc=json.loads((ROOT/'templates/INIT_STUDIO_PREFLIGHT_TEMPLATE.json').read_text())
        self.doc=doc
        doc.update(status='WORK_IN_PROGRESS',operator='fixture-operator',runtime_key='friend::claude-code',source_commit='123456789abcdef')
        doc['target'].update(name='Disposable Baseplate',studio_instance_id='fictional-studio-instance',human_confirmed=True,non_production=True)
        doc['mcp'].update(selected_client='claude-code',connected=True)
        doc['mcp']['probes'].update({k:'fictional fixture' for k in vst.PROBES})
        (self.root/'.local/probes.txt').write_text('fixture only, not real MCP')
        doc['mcp']['raw_probe_evidence']='.local/probes.txt'
        self.path=self.root/'.local/INIT_STUDIO_PREFLIGHT.json';self.flush()
    def flush(self):self.path.write_text(json.dumps(self.doc))
    def test_empty_template_cannot_claim_mcp_or_full(self):
        p=self.root/'.local/blank.json';p.write_text((ROOT/'templates/INIT_STUDIO_PREFLIGHT_TEMPLATE.json').read_text())
        self.assertTrue(vst.validate(p,self.root,'mcp'))
        self.assertTrue(vst.validate(p,self.root,'full'))
    def test_mcp_phase_only_passes_matching_active_runtime(self):
        self.assertEqual(vst.validate(self.path,self.root,'mcp','friend::claude-code'),[])
        self.assertTrue(vst.validate(self.path,self.root,'mcp','owner::antigravity'))
        self.assertTrue(vst.validate(self.path,self.root,'rojo','friend::claude-code'))
    def test_rojo_needs_separate_plugin_and_both_marker_states(self):
        r=self.doc['rojo'];r.update(plugin_connected=True,source_commit=self.doc['source_commit'],managed_path='ReplicatedStorage/GameShared')
        r['marker_added_evidence']='.local/added.txt';(self.root/'.local/added.txt').write_text('fixture marker added')
        self.flush();self.assertTrue(vst.validate(self.path,self.root,'rojo','friend::claude-code'))
        r['marker_removed_evidence']='.local/removed.txt';(self.root/'.local/removed.txt').write_text('fixture marker removed')
        self.flush();self.assertEqual(vst.validate(self.path,self.root,'rojo','friend::claude-code'),[])
    def test_full_needs_play_console_screenshot_human_and_nonproduction(self):
        r=self.doc['rojo'];r.update(plugin_connected=True,source_commit=self.doc['source_commit'],managed_path='ReplicatedStorage/GameShared',marker_added_evidence='.local/added.txt',marker_removed_evidence='.local/removed.txt')
        for name in ('added','removed','console','input'):(self.root/f'.local/{name}.txt').write_text('fixture only')
        self.doc['status']='PASS'
        self.doc['playtest'].update(started_and_stopped=True,scenario='disposable click',observed_result='fixture only',console='.local/console.txt',input_trace='.local/input.txt',screenshot='.local/screen.png')
        (self.root/'.local/screen.png').write_bytes(valid_fixture_png())
        self.flush();self.assertTrue(vst.validate(self.path,self.root,'full','friend::claude-code'))
        self.doc['human_verification'].update(confirmed_by='fixture human',checked_target=True,checked_playtest=True)
        self.flush();self.assertEqual(vst.validate(self.path,self.root,'full','friend::claude-code'),[])
        self.doc['target']['non_production']=False;self.flush();self.assertTrue(vst.validate(self.path,self.root,'full'))
        self.doc['target']['non_production']=True;self.doc['playtest']['screenshot']='.local/fake.png';self.flush();self.assertTrue(vst.validate(self.path,self.root,'full'))
    def test_preflight_missing_native_tools_does_not_claim_ready(self):
        self.path.unlink()
        r=wp.preflight(root=self.root,which=lambda name:None)
        self.assertEqual(r['status'],'BLOCKED')
        self.assertFalse((self.root/'.local/INIT_STUDIO_PREFLIGHT.json').exists())
        with self.assertRaises(ValueError):wp.preflight(plugin=True,root=self.root)
    def test_preflight_success_requires_actual_native_artifact_and_fresh_hash(self):
        (self.root/'rokit.toml').write_text('[tools]\n')
        (self.root/'default.project.json').write_text('{}')
        class Result:
            returncode=0
            stdout='7.7.0'
            stderr=''
        def installed(name):return '/fixture/tool'  # not installed; negative unit fixture
        from unittest.mock import patch
        fake_probe={n:{'version_verified':True,'version_required':v} for n,v in wp.EXPECTED.items()}
        with patch.object(wp,'probe',return_value=fake_probe):
            r=wp.preflight(root=self.root,which=installed,runner=lambda *a,**kw:Result())
            self.assertEqual(r['status'],'BLOCKED')
            def fake_runner(args,**kw):
                if args[:2]==['rojo','build']:
                    (self.root/'build/initialization_preflight.rbxlx').write_bytes(b'fixture only'*32)
                return Result()
            r=wp.preflight(root=self.root,which=installed,runner=fake_runner)
            self.assertEqual(r['status'],'LOCAL_TOOLS_PASS_LIVE_STUDIO_PENDING')
            self.assertTrue(wp.current_preflight(self.root))
            (self.root/'default.project.json').write_text('{"modified":true}')
            self.assertFalse(wp.current_preflight(self.root))
    def test_initializer_has_real_studio_sync_gate(self):
        self.assertIn('rojo_live_sync',ip.RUNTIME)
        self.assertIn('studio_disposable_test',ip.RUNTIME)
        self.assertIn('developer_toolchain',ip.RUNTIME)
        self.assertIn('validate_initialization_studio', (ROOT/'scripts/initialize_project.py').read_text())
    def test_v8_bootstrap_defers_live_studio_until_task_time(self):
        prompt=(ROOT/'TEAM_BOOTSTRAP_PROMPT.txt').read_text()
        guide=(ROOT/'INITIALIZE_PROJECT.md').read_text()
        for text in (prompt,guide):
            self.assertIn('scripts/team.py setup',text)
            self.assertIn('Studio',text)
        self.assertIn('Do NOT require a disposable Studio playtest merely to let me submit an idea',prompt)
        self.assertIn('task-time',prompt)
        self.assertIn('LIVE_STUDIO_DELIVERY.md',prompt)
        # Low-level live Studio validators remain available for tasks that need them.
        self.assertTrue((ROOT/'scripts/workstation_preflight.py').exists())
        self.assertTrue((ROOT/'scripts/validate_initialization_studio.py').exists())

if __name__=='__main__':unittest.main()
