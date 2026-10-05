#!/usr/bin/env python3
"""Verify issue-local Studio MCP + Rojo handoff receipts are structurally consistent.

Cannot prove reported MCP calls genuinely occurred or judge artistic quality. Human
verification of the actual target place and playtest remains mandatory.
"""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from validate_feature_evidence import safe_file,valid_image
ROOT=Path(__file__).resolve().parents[1]
MANAGED=('ReplicatedStorage/GameShared','ServerScriptService/GameServer','StarterPlayer/StarterPlayerScripts/GameClient')
PROBES=('list_roblox_studios','get_studio_state','search_game_tree')

def validate_delivery(path:Path,root=ROOT,expect_issue=None):
    errors=[]
    try:
        doc=json.loads(path.read_text());rel=path.relative_to(root).as_posix()
    except (OSError,ValueError) as exc:return [f'bad Studio receipt: {exc}']
    match=re.fullmatch(r'04_CHANGESETS/GH-(\d{6})_[\w-]+/STUDIO_DELIVERY\.json',rel)
    if not match:errors.append('Studio receipt must be issue-local under GH-###### changeset')
    if doc.get('schema_version') not in {1,2}:errors.append('Studio receipt schema must be 1 or 2')
    issue=int(match.group(1)) if match else expect_issue
    if doc.get('issue')!=issue or (expect_issue is not None and doc.get('issue')!=expect_issue):errors.append('Studio receipt issue mismatch')
    task_path=path.parent/'TASK.json'
    if task_path.is_file():
        try:
            task=json.loads(task_path.read_text(encoding='utf-8'))
            if int(task.get('schema_version',0) or 0)>=4:
                if doc.get('schema_version')!=2:errors.append('v8.5 Studio receipt must use schema 2')
                if doc.get('scope_revision')!=int(task.get('scope_revision',0) or 0):errors.append('Studio receipt scope revision does not match TASK.json')
        except (OSError,ValueError,TypeError):errors.append('TASK.json unreadable while validating Studio scope revision')
    if doc.get('status')!='PASS':errors.append('live Studio delivery status not PASS')
    if not all(isinstance(doc.get(k),str) and doc.get(k).strip() for k in ('operator','git_commit')):errors.append('operator or source commit missing')
    target=doc.get('target',{})
    if not all(target.get(k) for k in ('name','studio_instance_id','human_confirmed')):errors.append('target place/window not human-confirmed')
    # Unpublished Baseplates can have no published place ID; never invent one.
    mcp=doc.get('mcp',{})
    if not (mcp.get('connected') is True and isinstance(mcp.get('selected_client'),str) and mcp['selected_client'].strip()):errors.append('MCP client not connected/identified')
    if any(not isinstance(mcp.get('probes',{}).get(k),str) or not mcp['probes'][k].strip() for k in PROBES):errors.append('MCP probe results absent')
    if not safe_file(root,mcp.get('raw_probe_evidence','')):errors.append('actual MCP probe evidence missing')
    rojo=doc.get('rojo',{})
    if not (rojo.get('project')=='default.project.json' and rojo.get('source_commit')==doc.get('git_commit') and rojo.get('serve_command')=='rojo serve default.project.json' and rojo.get('plugin_connected') is True and rojo.get('managed_path') in MANAGED):errors.append('Rojo sync target, commit or plugin proof incomplete')
    if not safe_file(root,rojo.get('marker_proof','')):errors.append('Rojo managed-path marker evidence missing')
    play=doc.get('playtest',{})
    if not(play.get('started_and_stopped') is True and play.get('scenario') and play.get('observed_result')):errors.append('real Studio playtest scenario incomplete')
    for k in ('console','input_trace'):
        if not safe_file(root,play.get(k,'')):errors.append(f'playtest {k} missing')
    if not valid_image(root,play.get('screenshot','')):errors.append('actual Studio screenshot evidence invalid/missing')
    human=doc.get('human_verification',{})
    if not (human.get('reviewer') and human.get('reference')):errors.append('second human target/gameplay verification missing')
    return errors

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--receipt',required=True);a=p.parse_args()
    errs=validate_delivery(ROOT/a.receipt)
    if errs:
        for e in errs:print('FAIL:',e)
        raise SystemExit(1)
    print('PASS: live Studio delivery receipt structurally complete; second human must verify authenticity and visual quality')
if __name__=='__main__':main()
