#!/usr/bin/env python3
"""Shape/path/role-separation validator for issue-local quality evidence.

Does not certify image aesthetics or the truth of a human's/manual test claims.
A feature PR that changes managed source, approved assets, or Rojo mapping must
provide the required issue-local evidence packet(s).
"""
from __future__ import annotations
import argparse,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from streamlined_task import BRANCH
IMG={'.png':b'\x89PNG\r\n\x1a\n','.jpg':b'\xff\xd8','.jpeg':b'\xff\xd8','.webp':b'RIFF'}

def safe_file(root:Path,path:str,allowed=None):
    if not isinstance(path,str) or not path or '\\' in path or path.startswith('/') or '..' in Path(path).parts:return False
    p=root/path
    if not p.is_file() or p.is_symlink() or any(q.is_symlink() for q in [p,*p.parents] if q!=root and root in q.parents):return False
    if allowed and not p.relative_to(root).as_posix().startswith(allowed):return False
    return True

def valid_image(root,path):
    if not safe_file(root,path):return False
    p=root/path
    if p.suffix.lower() not in IMG:return False
    raw=p.read_bytes()
    if len(raw)<32 or not raw.startswith(IMG[p.suffix.lower()]):return False
    if p.suffix.lower()=='.png':
        # Sanity check a recognizable nontrivial image structure. Not proof that image came from Studio.
        if len(raw)<64 or raw[12:16]!=b'IHDR' or b'IDAT' not in raw or not raw.endswith(b'IEND\xaeB`\x82'):
            return False
        width=int.from_bytes(raw[16:20],'big');height=int.from_bytes(raw[20:24],'big')
        if width<320 or height<180:return False
    elif p.suffix.lower() in ('.jpg','.jpeg'):
        if len(raw)<2048 or not raw.endswith(b'\xff\xd9'):return False
    elif p.suffix.lower()=='.webp':
        if len(raw)<2048 or raw[8:12]!=b'WEBP':return False
    return True

def validate_packet(path:Path,root=ROOT):
    errors=[]
    try:
        doc=json.loads(path.read_text()); rel=path.relative_to(root).as_posix()
    except (ValueError,OSError) as exc:return [f'bad evidence JSON: {exc}']
    if not re.search(r'04_CHANGESETS/GH-\d{6}_[\w-]+/QUALITY_EVIDENCE\.json$',rel):errors.append('evidence must be in a GH-###### changeset')
    if doc.get('schema_version') not in {1,2}:errors.append('schema version unsupported')
    m=re.search(r'GH-(\d{6})_',rel)
    if m and doc.get('issue')!=int(m.group(1)):errors.append('issue ID does not match changeset')
    branch=str(doc.get('branch',''))
    bm=BRANCH.fullmatch(branch)
    if not bm or (m and int(bm.group(1))!=int(m.group(1))):errors.append('branch must be canonical feat/fix/docs/<issue>-<slug> and match changeset issue')
    task_path=path.parent/'TASK.json'
    if task_path.is_file():
        try:
            task=json.loads(task_path.read_text(encoding='utf-8'))
            if task.get('branch')!=branch:errors.append('quality packet branch does not match TASK.json')
            if int(task.get('schema_version',0) or 0)>=4:
                if doc.get('schema_version')!=2:errors.append('v8.5 quality packet must use schema 2')
                if doc.get('scope_revision')!=int(task.get('scope_revision',0) or 0):errors.append('quality packet scope revision does not match TASK.json')
        except (OSError,ValueError,TypeError):errors.append('TASK.json unreadable while validating quality packet branch')
    if doc.get('status')!='ACCEPTANCE_READY':errors.append('packet not acceptance-ready')
    if not safe_file(root,doc.get('quality_brief','')):errors.append('QUALITY_BRIEF missing')
    art=doc.get('art_direction',{})
    if art.get('required') and not(all(art.get(k) for k in ('human_approved','reviewer','approval_reference'))):errors.append('art direction human approval missing')
    receipts=doc.get('skill_use_receipts',[])
    if not receipts or any(not (x.get('role') and x.get('skill') and x.get('purpose') and x.get('output') and safe_file(root,x.get('loaded_from',''),'.agents/skills/') and safe_file(root,x.get('output',''))) for x in receipts):errors.append('skill use receipts missing/incomplete or skill missing')
    if any(not p.get('removed_or_approved_as_final') for p in doc.get('placeholders',[])):errors.append('unresolved placeholders exist')
    ft=doc.get('functional_tests',[])
    if not ft or any(t.get('result')!='PASS' or not all(t.get(k) for k in ('scenario','operator','commit','console')) or not safe_file(root,t.get('evidence','')) or not safe_file(root,t.get('console','')) for t in ft):errors.append('functional tests incomplete/missing real evidence')
    live=doc.get('live_studio',{})
    if live.get('status')!='PASS' or not all(live.get(k) for k in ('operator','test_place','commit')) or not safe_file(root,live.get('evidence','')):errors.append('real Studio evidence incomplete')
    delivery=doc.get('studio_delivery_receipt','')
    if not safe_file(root,delivery):
        errors.append('issue-local STUDIO_DELIVERY receipt missing')
    else:
        # Late import avoids circular import because delivery validator reuses image/path validation.
        from validate_studio_delivery import validate_delivery
        delivery_errors=validate_delivery(root/delivery,root,expect_issue=doc.get('issue'))
        errors.extend('Studio delivery: '+e for e in delivery_errors)
    visual=doc.get('visual_review',{})
    if visual.get('status')=='PASS':
        if not visual.get('reviewer') or not visual.get('screenshots') or not all(valid_image(root,x) for x in visual.get('screenshots',[])):errors.append('independent visual review/screenshots absent')
    elif visual.get('status')=='NOT_APPLICABLE':
        if art.get('required') or not visual.get('rationale'):errors.append('visual N/A not justified or art required')
    else:errors.append('independent visual review pending or invalid')
    ui=doc.get('ui_review',{})
    if ui.get('status')=='PASS':
        if not ui.get('reviewer') or not ui.get('device_screenshots') or not all(valid_image(root,x) for x in ui['device_screenshots']) or not safe_file(root,ui.get('interaction_evidence','')):errors.append('UI review proof incomplete')
    elif ui.get('status')=='NOT_APPLICABLE':
        if not ui.get('rationale'):errors.append('UI N/A must give a concrete reason')
    else:errors.append('UI review status must be PASS or NOT_APPLICABLE')
    rev=doc.get('independent_review',{})
    implementers=set(rev.get('implementers',[])); reviewers=set(rev.get('reviewers',[]))
    if not implementers or not reviewers or implementers&reviewers or not safe_file(root,rev.get('report','')):errors.append('independent reviewer separation/report missing')
    if visual.get('status')=='PASS' and visual.get('reviewer') in implementers:errors.append('visual reviewer is implementer')
    if ui.get('status')=='PASS' and ui.get('reviewer') in implementers:errors.append('UI reviewer is implementer')
    if doc.get('human_integration_approval')!='PENDING':errors.append('branch packet must leave actual PR merge to human')
    return errors

def changed_src(root,base):
    """Game-visible managed changes across commits AND current local edits.

    Historical function name kept for callers; now includes approved art assets
    and Rojo mapping changes so asset-only PRs cannot bypass Studio evidence.
    """
    filters=('src/','07_ASSETS/APPROVED/','default.project.json')
    def relevant(path):
        return path.startswith(filters[:2]) or path=='default.project.json'
    paths=set()
    for args in ([f'{base}...HEAD'],['HEAD']):
        cp=subprocess.run(['git','diff','--name-only',*args,'--',*filters],cwd=root,text=True,capture_output=True)
        if cp.returncode:raise RuntimeError(f'base ref {base} unavailable or Git diff failed; fetch full Git history')
        paths.update(path for path in cp.stdout.splitlines() if relevant(path))
    # A brand-new untracked game source/approved art asset is relevant locally.
    cp=subprocess.run(['git','ls-files','--others','--exclude-standard','--',*filters],cwd=root,text=True,capture_output=True)
    if cp.returncode:raise RuntimeError('Git worktree inspection failed')
    paths.update(path for path in cp.stdout.splitlines() if relevant(path))
    return sorted(paths)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--compare',help='in CI, require issue evidence for code-changing PRs');p.add_argument('--packet',help='validate one issue-local packet');a=p.parse_args()
    packets=[ROOT/a.packet] if a.packet else sorted((ROOT/'04_CHANGESETS').glob('GH-*/QUALITY_EVIDENCE.json'))
    if a.compare:
        files=changed_src(ROOT,a.compare)
        if files and not packets:raise SystemExit('BLOCKED: managed game code/assets/project mapping changed but no issue-local QUALITY_EVIDENCE.json (Studio delivery, live test + reviewers required)')
        if not files and not packets:
            print('PASS: no changed managed game code; no feature packet required');return
    errors=[]
    for packet in packets: errors.extend(f'{packet.relative_to(ROOT)}: {x}' for x in validate_packet(packet))
    if errors:
        for err in errors:print('FAIL:',err)
        raise SystemExit(1)
    print(f'PASS: {len(packets)} issue evidence packet(s) structurally valid; manual tests/images require human verification')
if __name__=='__main__': main()
