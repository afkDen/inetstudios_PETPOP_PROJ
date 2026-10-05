"""Only schema/negative contract fixtures. Does NOT emulate genuine MCP/Studio tests."""
from __future__ import annotations
import sys,unittest,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import validate_studio_delivery as sd
from tests.test_production_quality import ProductionQualityTests

class StudioDeliveryContractTests(unittest.TestCase):
    # Share deterministic fixture preparation without running the parent tests twice.
    setUp=ProductionQualityTests.setUp
    tearDown=ProductionQualityTests.tearDown
    dump=ProductionQualityTests.dump
    errors=ProductionQualityTests.errors
    def test_completed_fixture_structurally_valid_not_a_real_playtest(self):
        self.assertEqual(sd.validate_delivery(self.receipt_path,self.root),[])

    def test_wrong_mcp_client_or_missing_probes_blocks(self):
        self.receipt['mcp']['connected']=False
        self.receipt['mcp']['probes'].pop('list_roblox_studios')
        self.receipt_path.write_text(json.dumps(self.receipt))
        self.assertIn('MCP probe results absent',' '.join(sd.validate_delivery(self.receipt_path,self.root)))

    def test_wrong_rojo_sync_or_absent_plugin_blocks(self):
        self.receipt['rojo']['plugin_connected']=False
        self.receipt['rojo']['source_commit']='another-branch'
        self.receipt_path.write_text(json.dumps(self.receipt))
        self.assertIn('Rojo sync target',' '.join(sd.validate_delivery(self.receipt_path,self.root)))

    def test_no_human_target_lock_blocks(self):
        self.receipt['target']['human_confirmed']=False
        self.receipt_path.write_text(json.dumps(self.receipt))
        self.assertIn('human-confirmed',' '.join(sd.validate_delivery(self.receipt_path,self.root)))

    def test_simulated_source_only_image_does_not_claim_actual_evidence(self):
        # The structural checker detects missing/invalid files, but cannot authenticate the screenshot origin.
        (self.d/'screen.png').write_bytes(b'not a real screenshot')
        self.assertIn('screenshot evidence invalid',' '.join(sd.validate_delivery(self.receipt_path,self.root)))

    def test_quality_packet_requires_delivery_receipt(self):
        self.j.pop('studio_delivery_receipt')
        self.assertIn('STUDIO_DELIVERY receipt missing',' '.join(self.errors()))

    def test_role_and_skills_mapped(self):
        d=json.loads((ROOT/'08_TOOLCHAIN/ROLE_CONTRACTS/roles.json').read_text())
        roles={r['id']:r for r in d['roles']}
        self.assertIn('studio-place-integration',roles['studio-operator']['required_skills'])
        self.assertIn('roblox-ui-polish',roles['frontend-worker']['required_skills'])
        self.assertIn('stylized-asset-families',roles['creative-director']['required_skills'])
        reg=json.loads((ROOT/'08_TOOLCHAIN/SKILL_REGISTRY.json').read_text())
        for name in ('studio-place-integration','roblox-ui-polish','stylized-asset-families'):
            self.assertTrue((ROOT/'.agents/skills'/name/'SKILL.md').exists())
            self.assertIn(name,[r['name'] for r in reg['skills']])

    def test_real_studio_client_plus_rojo_are_separate_connections(self):
        docs=(ROOT/'02_TECHNICAL/LIVE_STUDIO_DELIVERY.md').read_text()
        for key in ('Quick connect','Antigravity','Visual Studio Code','rojo serve default.project.json','GameServer','GameClient','get_console_output','screen_capture'):
            self.assertIn(key,docs)

if __name__=='__main__':unittest.main()

class StudioReceiptPreparationTests(unittest.TestCase):
    def test_creates_draft_for_existing_issue_only_and_does_not_overwrite(self):
        import tempfile
        from prepare_studio_delivery import prepare
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/'04_CHANGESETS/GH-000123_sample').mkdir(parents=True)
            (root/'templates').mkdir()
            (root/'templates/STUDIO_DELIVERY_TEMPLATE.json').write_text((ROOT/'templates/STUDIO_DELIVERY_TEMPLATE.json').read_text())
            receipt=prepare(123,root)
            data=json.loads(receipt.read_text())
            self.assertEqual(data['issue'],123)
            self.assertEqual(data['status'],'PENDING')
            receipt.write_text(receipt.read_text().replace('PENDING','WORK_IN_PROGRESS'))
            self.assertEqual(prepare(123,root),receipt)
            self.assertIn('WORK_IN_PROGRESS',receipt.read_text())
            with self.assertRaisesRegex(ValueError,'one existing issue changeset'):
                prepare(124,root)

class GameAssetReviewBoundaryTests(unittest.TestCase):
    def test_approved_asset_changes_need_quality_evidence_even_without_scripts(self):
        import tempfile,subprocess
        from validate_feature_evidence import changed_src
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            def git(*args):return subprocess.run(['git',*args],cwd=root,text=True,capture_output=True,check=True)
            git('init','-q','-b','main')
            (root/'README.md').write_text('fixture')
            git('add','.');git('-c','user.name=Fixture','-c','user.email=fixture@invalid.local','commit','-qm','baseline')
            git('checkout','-qb','feat/123-art')
            out=root/'07_ASSETS/APPROVED/rock.glb';out.parent.mkdir(parents=True);out.write_bytes(b'fixture-file')
            self.assertEqual(changed_src(root,'main'),['07_ASSETS/APPROVED/rock.glb'])
            git('add','.');git('-c','user.name=Fixture','-c','user.email=fixture@invalid.local','commit','-qm','art')
            self.assertEqual(changed_src(root,'main'),['07_ASSETS/APPROVED/rock.glb'])
            (root/'default.project.json').write_text('{}')
            self.assertIn('default.project.json',changed_src(root,'main'))

class WorldSourceMigrationTests(unittest.TestCase):
    def test_world_mapping_is_opt_in_not_in_default_live_sync(self):
        default=json.loads((ROOT/'default.project.json').read_text())
        opt=json.loads((ROOT/'templates/rojo-world-opt-in.project.json').read_text())
        self.assertNotIn('Workspace',default['tree'])
        world=opt['tree']['Workspace']
        self.assertTrue(world['$ignoreUnknownInstances'])
        self.assertEqual(world['VersionedWorld']['$path'],'src/world')
