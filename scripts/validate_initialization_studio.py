#!/usr/bin/env python3
"""Validate a LOCAL initialization Studio preflight receipt, never pretend to execute MCP.

A syntactically valid receipt is NOT proof of tool use. Runtime operator records genuine
MCP/Rojo calls, and the developer must confirm the target and observed playtest.
"""
from __future__ import annotations
import argparse,json,re,subprocess
from pathlib import Path
from validate_feature_evidence import safe_file,valid_image
ROOT=Path(__file__).resolve().parents[1]
RECEIPT=ROOT/'.local/INIT_STUDIO_PREFLIGHT.json'
MANAGED={'ReplicatedStorage/GameShared','ServerScriptService/GameServer','StarterPlayer/StarterPlayerScripts/GameClient'}
PROBES=('list_roblox_studios','get_studio_state','search_game_tree')

def value(x):
    return isinstance(x,str) and bool(x.strip())

def validate(path=RECEIPT,root=ROOT,stage='full',runtime_key=None):
    try:
        doc=json.loads(path.read_text())
    except (ValueError,OSError) as exc:
        return [f'local Studio initialization receipt missing or malformed: {exc}']
    errors=[]
    if doc.get('schema_version')!=1:errors.append('invalid schema version')
    if (stage=='full' and doc.get('status')!='PASS') or (stage!='full' and doc.get('status') not in ('WORK_IN_PROGRESS','PASS')):
        errors.append('receipt status must reflect real staged or completed live evidence')
    if not value(doc.get('operator')) or not value(doc.get('runtime_key')):errors.append('operator/runtime identity missing')
    if runtime_key and doc.get('runtime_key')!=runtime_key:errors.append('runtime does not match personal validation entry')
    if not re.fullmatch(r'[0-9a-fA-F]{7,40}',doc.get('source_commit','')):errors.append('source commit missing/invalid')
    target=doc.get('target',{})
    if not(value(target.get('name')) and value(target.get('studio_instance_id')) and target.get('human_confirmed') is True and target.get('non_production') is True):
        errors.append('human-confirmed disposable/nonproduction Studio target missing')
    mcp=doc.get('mcp',{})
    if mcp.get('connected') is not True or not value(mcp.get('selected_client')):
        errors.append('correct active MCP client must be connected')
    if any(not value(mcp.get('probes',{}).get(k)) for k in PROBES):
        errors.append('genuine required MCP tool results must be recorded')
    if not safe_file(root,mcp.get('raw_probe_evidence',''),'.local/'):
        errors.append('local raw MCP tool evidence missing')
    if stage=='mcp':return errors
    rojo=doc.get('rojo',{})
    if not(rojo.get('project')=='default.project.json' and rojo.get('serve_command')=='rojo serve default.project.json'
           and rojo.get('plugin_connected') is True and rojo.get('source_commit')==doc.get('source_commit')
           and rojo.get('managed_path') in MANAGED):
        errors.append('Rojo server/plugin/managed-tree/commit evidence incomplete')
    for k in ('marker_added_evidence','marker_removed_evidence'):
        if not safe_file(root,rojo.get(k,''),'.local/'):errors.append('Rojo '+k+' missing; both live appearance and removal are required')
    if stage=='rojo':return errors
    play=doc.get('playtest',{})
    if not(play.get('started_and_stopped') is True and value(play.get('scenario')) and value(play.get('observed_result'))):
        errors.append('disposable real playtest not completed')
    for k in ('console','input_trace'):
        if not safe_file(root,play.get(k,''),'.local/'):errors.append('local playtest '+k+' missing')
    if not valid_image(root,play.get('screenshot','')) or not str(play.get('screenshot','')).startswith('.local/'):
        errors.append('local real Studio screenshot invalid/missing')
    human=doc.get('human_verification',{})
    if not(value(human.get('confirmed_by')) and human.get('checked_target') is True and human.get('checked_playtest') is True):
        errors.append('human confirmation of intended test place and playtest missing')
    return errors

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--receipt',default='.local/INIT_STUDIO_PREFLIGHT.json')
    ap.add_argument('--stage',choices=['mcp','rojo','full'],default='full')
    ap.add_argument('--runtime-key')
    a=ap.parse_args(); p=Path(a.receipt)
    if not p.is_absolute():p=ROOT/p
    try:p.relative_to(ROOT/'.local')
    except ValueError:raise SystemExit('Receipt must be local/ignored under .local/')
    failures=validate(p,ROOT,a.stage,a.runtime_key)
    if failures:
        for failure in failures:print('BLOCKED:',failure)
        raise SystemExit(2)
    print('STRUCTURAL PASS:',a.stage,'initialization receipt; local human/operator must attest actual tool results')
if __name__=='__main__':main()
