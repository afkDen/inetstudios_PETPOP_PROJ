#!/usr/bin/env python3
"""Team workstation dependency bootstrap. Never silently install a system-wide manager.

--check: inspect project tools without changing files.
--install: with user consent, run installed Rokit to install manifest tools.
--install-plugin: additionally install version-matched Rojo Studio plugin with consent.
The verified results are LOCAL evidence; no shared project status is modified.
"""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EXPECTED={'rojo':'7.7.0','stylua':'2.5.2','selene':'0.31.0'}

def probe(which=shutil.which, runner=subprocess.run):
    result={}
    for name,version in EXPECTED.items():
        path=which(name)
        item={'found':bool(path),'path':path,'version_required':version,'version_verified':False}
        if path:
            try:
                cp=runner([name,'--version'],cwd=ROOT,capture_output=True,text=True,timeout=15,check=False)
                raw=(cp.stdout+' '+cp.stderr).strip()
                item['version_output']=raw[:180]
                item['version_verified']=cp.returncode==0 and version in raw
            except (OSError,subprocess.TimeoutExpired):pass
        result[name]=item
    result['rokit']={'found':bool(which('rokit'))}
    result['studio_plugin']={'status':'MANUAL_VERIFICATION_REQUIRED','note':'Matching Rojo Studio plugin must be verified inside each local Studio installation.'}
    result['studio_mcp']={'status':'MANUAL_VERIFICATION_REQUIRED','note':'Verify only where supported; MCP configuration is not a connectivity test.'}
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check',action='store_true',help='Read-only local dependency probe (default)')
    p.add_argument('--install',action='store_true',help='Run rokit install if Rokit already exists; requires human consent')
    p.add_argument('--install-plugin',action='store_true',help='With --install, also run rojo plugin install on this workstation')
    p.add_argument('--json',action='store_true')
    a=p.parse_args()
    if a.install_plugin and not a.install: p.error('--install-plugin requires --install')
    if a.install:
        if shutil.which('rokit') is None:
            raise SystemExit('BLOCKED: Rokit is not installed. Install Rokit from the reviewed official release on your workstation; rerun --install. Never execute a remote install script automatically.')
        cp=subprocess.run(['rokit','install'],cwd=ROOT,check=False)
        if cp.returncode:raise SystemExit('BLOCKED: rokit install failed; inspect output and fix manually')
        if a.install_plugin:
            if shutil.which('rojo') is None:raise SystemExit('BLOCKED: rojo not on PATH after Rokit install')
            cp=subprocess.run(['rojo','plugin','install'],cwd=ROOT,check=False)
            if cp.returncode:raise SystemExit('BLOCKED: Rojo plugin installation failed; verify matching plugin manually')
    results=probe()
    if a.json: print(json.dumps(results,indent=2))
    else:
        for name in EXPECTED:
            value=results[name]
            print(f'{name}: '+('VERIFIED' if value['version_verified'] else 'MISSING' if not value['found'] else 'WRONG/UNVERIFIED VERSION')+f" (required {value['version_required']})")
        print('Studio plugin + Studio MCP: manual live verification required')
    # Exit nonzero for false readiness; without Rokit or Studio this is expected on CI-free hosts.
    return 0 if all(results[n]['version_verified'] for n in EXPECTED) else 2
if __name__=='__main__':sys.exit(main())
