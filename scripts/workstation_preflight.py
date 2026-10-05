#!/usr/bin/env python3
"""Local workstation initializer: pinned tools + native Rojo build + blank live Studio receipt.

Does not launch Studio, perform MCP calls, silently download Rokit, or claim a live pass.
An agent following INITIALIZE_PROJECT.md completes the live Studio stages.
"""
from __future__ import annotations
import argparse,hashlib,json,shutil,subprocess,sys
from pathlib import Path
from bootstrap_dev_tools import EXPECTED,probe
ROOT=Path(__file__).resolve().parents[1]
LOCAL=ROOT/'.local'

def prepare(root=ROOT):
    receipt=root/'.local/INIT_STUDIO_PREFLIGHT.json'
    receipt.parent.mkdir(parents=True,exist_ok=True)
    if not receipt.exists():
        shutil.copyfile(root/'templates/INIT_STUDIO_PREFLIGHT_TEMPLATE.json',receipt)
    return receipt

def preflight(install=False,plugin=False,root=ROOT,which=shutil.which,runner=subprocess.run):
    if plugin and not install:raise ValueError('--install-plugin requires --install')
    if install:
        if not which('rokit'):return {'status':'BLOCKED','message':'Install Rokit yourself from the reviewed official release; no automatic system-wide bootstrap'}
        cp=runner(['rokit','install'],cwd=root,check=False)
        if cp.returncode:return {'status':'BLOCKED','message':'Rokit dependency installation failed'}
        if plugin:
            if not which('rojo'):return {'status':'BLOCKED','message':'Rojo unavailable after Rokit install'}
            cp=runner(['rojo','plugin','install'],cwd=root,check=False)
            if cp.returncode:return {'status':'BLOCKED','message':'Rojo Studio plugin installation failed; inspect inside Studio'}
    tools=probe(which=which,runner=runner)
    missing=[name for name in EXPECTED if not tools[name]['version_verified']]
    if missing:return {'status':'BLOCKED','message':'Missing/wrong pinned binaries: '+', '.join(missing),'tools':tools}
    (root/'build').mkdir(exist_ok=True)
    built=root/'build/initialization_preflight.rbxlx'
    if built.exists():built.unlink()  # stale artifact must not satisfy this run
    cp=runner(['rojo','build','default.project.json','--output','build/initialization_preflight.rbxlx'],cwd=root,check=False)
    if cp.returncode or not built.is_file() or built.stat().st_size<64:
        return {'status':'BLOCKED','message':'Native Rojo build failed or produced no valid-sized place artifact','tools':tools}
    prepare(root)
    proof={'status':'LOCAL_TOOLS_PASS_LIVE_STUDIO_PENDING',
           'rokit_manifest_sha256':hashlib.sha256((root/'rokit.toml').read_bytes()).hexdigest(),
           'project_map_sha256':hashlib.sha256((root/'default.project.json').read_bytes()).hexdigest(),
           'native_build_path':'build/initialization_preflight.rbxlx',
           'native_build_sha256':hashlib.sha256(built.read_bytes()).hexdigest(),
           'pinned_versions':{name:tools[name]['version_required'] for name in EXPECTED}}
    out=root/'.local/WORKSTATION_PREFLIGHT.json'
    serialized=json.dumps(proof,indent=2)+'\n'
    if not out.exists() or out.read_text()!=serialized:out.write_text(serialized)
    return {'status':'LOCAL_TOOLS_PASS_LIVE_STUDIO_PENDING','message':'Pinned tools and actual native Rojo build verified; now execute MCP+Rojo+Studio test on confirmed test place','tools':tools}

def current_preflight(root=ROOT):
    proof=root/'.local/WORKSTATION_PREFLIGHT.json'
    try:
        p=json.loads(proof.read_text())
        if p.get('status')!='LOCAL_TOOLS_PASS_LIVE_STUDIO_PENDING':return False
        if p['native_build_path']!='build/initialization_preflight.rbxlx':return False
        artifact=root/p['native_build_path']
        if artifact.is_symlink() or artifact.stat().st_size<64:return False
        for path,key in [('rokit.toml','rokit_manifest_sha256'),('default.project.json','project_map_sha256')]:
            if hashlib.sha256((root/path).read_bytes()).hexdigest()!=p.get(key):return False
        return hashlib.sha256(artifact.read_bytes()).hexdigest()==p.get('native_build_sha256') and p.get('pinned_versions')==EXPECTED
    except (ValueError,OSError,KeyError,TypeError):return False

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--install',action='store_true',help='Run already-installed Rokit; requires explicit user approval')
    ap.add_argument('--install-plugin',action='store_true',help='Modify local Studio plugin; separate explicit user approval')
    ap.add_argument('--json',action='store_true')
    a=ap.parse_args()
    if a.install_plugin and not a.install:ap.error('--install-plugin requires --install')
    result=preflight(a.install,a.install_plugin)
    if a.json: print(json.dumps(result,indent=2))
    else:print(result['status']+': '+result['message'])
    return 0 if result['status']=='LOCAL_TOOLS_PASS_LIVE_STUDIO_PENDING' else 2
if __name__=='__main__':sys.exit(main())
