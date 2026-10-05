#!/usr/bin/env python3
"""Validate shared team contract, task provenance, and legacy proposal records.

v8 normal flow validates byte-preserved 04_CHANGESETS/.../USER_REQUEST.txt via
TASK.json. The v7 proposal/promotion format remains accepted for migration.
--compare additionally protects already-merged raw inputs and integration-owned
workflow files on pull requests. This validator never writes repository state.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
IDEAS='00_INPUT/PROPOSALS/IDEAS/'
UPDATES='00_INPUT/PROPOSALS/UPDATES/'
PROPOSALS=ROOT/'00_INPUT/PROPOSALS'
PAT=re.compile(r'^GH-(\d{6})_([a-z0-9]+(?:-[a-z0-9]+)*)\.(txt|json)$')
REQUIRED=[
 'AGENTS.md','README.md','START_HERE.md','TEAM_PROTOCOL.md','TEAM_ONBOARDING.md','TEAM_IMPORT_GITHUB.md',
 'TEAM_RELEASE_CHECKLIST.md','08_TOOLCHAIN/TEAM_POLICY.json','08_TOOLCHAIN/WORKFLOW_PROFILE.json',
 '.github/workflows/portable-ci.yml','.github/CODEOWNERS','scripts/team_setup.py','scripts/team.py',
 'scripts/streamlined_task.py','scripts/validate_streamlined_task.py','scripts/validate_ci_task.py',
 'scripts/team_workflow.py','TEAM_WORKFLOW.md','TEAM_TASK_PROMPT.txt','TEAM_PROPOSAL_PROMPT.txt',
 '02_TECHNICAL/ROJO_WORKFLOW.md','scripts/validate_rojo_layout.py','default.project.json','rokit.toml',
 '02_TECHNICAL/DEPENDENCY_BOOTSTRAP.md','02_TECHNICAL/PRODUCTION_QUALITY_CONTRACT.md',
 'scripts/bootstrap_dev_tools.py','scripts/validate_feature_evidence.py','templates/QUALITY_BRIEF_TEMPLATE.md',
 'templates/QUALITY_EVIDENCE_TEMPLATE.json','templates/TASK_TEMPLATE.md','templates/TASK_EVIDENCE_TEMPLATE.json',
 'GAME_DESIGN.md','.gitattributes','08_TOOLCHAIN/SCOPE_EVOLUTION_V8_5.md','MIGRATION_V8_4_TO_V8_5.md','08_TOOLCHAIN/WORKSTATION_DEPENDENCIES.json','08_TOOLCHAIN/GRAPHIFY_POLICY.md','08_TOOLCHAIN/BLENDER_MCP_SETUP.md','scripts/workstation_doctor.py','scripts/graphify_sync.py','08_TOOLCHAIN/BLOXMAPS_INTEGRATION.json','08_TOOLCHAIN/BLOXMAPS_SETUP.md','scripts/bloxmaps_adapter.py'
]


def check_proposal(raw:Path,root=ROOT):
    """Legacy v7 proposal validator retained for existing repositories."""
    errors=[]
    try: rel=raw.relative_to(root).as_posix()
    except ValueError: return ['proposal outside project']
    if raw.is_symlink(): return [f'{rel}: symlink proposals disallowed']
    m=PAT.match(raw.name)
    if not m: return [f'{rel}: expected GH-000123_slug.txt']
    if rel.startswith(IDEAS):kind='idea'
    elif rel.startswith(UPDATES):kind='update'
    else:return [f'{rel}: invalid proposal location']
    meta=raw.with_suffix('.json')
    if not meta.is_file() or meta.is_symlink(): return [f'{rel}: matching metadata missing or symlinked']
    try:
        j=json.loads(meta.read_text())
        if (j.get('issue')!=int(m.group(1)) or j.get('key')!='GH-'+m.group(1) or
            j.get('kind')!=kind or j.get('sha256')!=hashlib.sha256(raw.read_bytes()).hexdigest() or
            j.get('raw_file')!=rel): errors.append(f'{rel}: metadata/hash mismatch')
        if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?',str(j.get('submitted_by',''))):errors.append(f'{rel}: invalid author')
        if j.get('schema_version')!=1:errors.append(f'{rel}: unsupported schema')
    except (ValueError,OSError) as e: errors.append(f'{rel}: malformed metadata: {type(e).__name__}')
    if raw.stat().st_size>256*1024 or raw.stat().st_size==0:errors.append(f'{rel}: invalid raw size')
    return errors


def git(args):
    return subprocess.run(['git',*args],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)


def _validate_changeset(cs:Path,root:Path) -> list[str]:
    errors=[]
    task=cs/'TASK.json'
    if task.exists():
        m=re.match(r'^GH-(\d{6})_',cs.name)
        if not m:return [f'invalid v8 changeset name: {cs.name}']
        from streamlined_task import validate_task
        return [f'{cs.name}: {e}' for e in validate_task(int(m.group(1)),root)]
    # Legacy v7 changeset remains accepted.
    evidence=cs/'SOURCE_PROPOSAL.json'
    if not evidence.exists():return ['issue changeset has neither TASK.json nor legacy SOURCE_PROPOSAL.json: '+cs.name]
    try:
        ev=json.loads(evidence.read_text());src=root/ev['source'];dest=cs/'USER_REQUEST.txt'
        if not src.is_file() or not dest.is_file() or dest.read_bytes()!=src.read_bytes() or ev['sha256']!=hashlib.sha256(src.read_bytes()).hexdigest():
            errors.append('issue changeset raw request differs from proposal: '+cs.name)
    except (KeyError,OSError,ValueError):errors.append('invalid legacy changeset proposal record: '+cs.name)
    return errors


def validate_all(root=ROOT):
    errors=[]
    for p in REQUIRED:
        if not (root/p).is_file():errors.append('missing '+p)
    try:policy=json.loads((root/'08_TOOLCHAIN/TEAM_POLICY.json').read_text())
    except Exception:return errors+['TEAM_POLICY.json malformed']
    if policy.get('template_unconfigured') is not False:errors.append('new-game template not bound: run scripts/prepare_new_game.py before project use')
    if not re.fullmatch(r'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?',policy.get('remote_url','')):errors.append('team policy requires an explicit GitHub remote URL')
    if policy.get('canonical_branch')!='main':errors.append('unexpected canonical branch')
    if policy.get('workflow_mode')!='streamlined-v8.5':errors.append('TEAM_POLICY workflow_mode must be streamlined-v8.5')
    if policy.get('workflow_profile')!='08_TOOLCHAIN/WORKFLOW_PROFILE.json':errors.append('missing streamlined workflow profile binding')
    if policy.get('local_runtime_validation')!='.local/RUNTIME_VALIDATIONS.json':errors.append('personal runtime evidence must be local')
    if '.local/' not in (root/'.gitignore').read_text():errors.append('.local/ must be gitignored')
    ga=(root/'.gitattributes').read_text(errors='ignore')
    if '04_CHANGESETS/**/USER_REQUEST.txt -text' not in ga:errors.append('USER_REQUEST.txt must be protected from Git line-ending normalization')
    if '04_CHANGESETS/**/REFERENCES/** -text' not in ga:errors.append('task REFERENCES/ must be protected from Git line-ending normalization')
    if '04_CHANGESETS/**/SCOPE_AMENDMENTS/** -text' not in ga:errors.append('scope amendments must be protected from Git line-ending normalization')
    from validate_rojo_layout import validate as validate_rojo
    errors+=validate_rojo(root)

    # Legacy proposal records, if present, remain immutable/valid.
    seen=set()
    for raw in sorted((root/'00_INPUT/PROPOSALS').rglob('*.txt')):
        m=PAT.match(raw.name)
        if m:
            if m.group(1) in seen:errors.append(f'issue GH-{m.group(1)} used in multiple legacy proposal files')
            seen.add(m.group(1))
        errors+=check_proposal(raw,root)
    for meta in sorted((root/'00_INPUT/PROPOSALS').rglob('*.json')):
        if not meta.with_suffix('.txt').exists():errors.append(f'orphan proposal metadata {meta.relative_to(root)}')

    # Legacy promoted inputs, if present, still have to match their source proposal.
    accepted=[root/'00_INPUT/GAME_IDEA/rough_game_idea.txt']
    accepted+=list((root/'00_INPUT/UPDATES/PROCESSED').glob('GH-*.txt'))
    for raw in accepted:
        if not raw.exists():continue
        record=raw.with_name('APPROVAL.json') if raw.parent.name=='GAME_IDEA' else raw.with_suffix('.json')
        if not record.is_file():errors.append('approved legacy raw input has no review record: '+str(raw.relative_to(root)));continue
        try:
            rec=json.loads(record.read_text());source=root/rec['proposal']
            if not source.is_file() or source.is_symlink() or source.resolve().parent not in ((root/'00_INPUT/PROPOSALS/IDEAS').resolve(),(root/'00_INPUT/PROPOSALS/UPDATES').resolve()):
                errors.append('approved legacy input points to a missing/invalid proposal: '+str(raw.relative_to(root)))
            elif raw.read_bytes()!=source.read_bytes() or rec['sha256']!=hashlib.sha256(raw.read_bytes()).hexdigest():
                errors.append('approved raw input differs from original proposal: '+str(raw.relative_to(root)))
        except (ValueError,KeyError,OSError):errors.append('malformed approved-input record: '+str(record.relative_to(root)))

    for cs in sorted((root/'04_CHANGESETS').glob('GH-*')):
        if cs.is_dir(): errors += _validate_changeset(cs,root)

    tracked=git(['ls-files','-z']).stdout.split('\0') if root==ROOT and (root/'.git').exists() else []
    for p in tracked:
        if p.startswith('.local/') or p in ('.env.local','.env'):
            errors.append('tracked personal/secret file: '+p)
    return errors


def validate_against_base(base):
    errors=[]
    if git(['rev-parse','--verify',base]).returncode:return [f'base {base} unavailable (CI must checkout with fetch-depth: 0)']

    # Protect all previously merged human raw requests from edits/deletes.
    for prefix in ['04_CHANGESETS','00_INPUT/PROPOSALS','00_INPUT/GAME_IDEA','00_INPUT/UPDATES/PROCESSED']:
        base_files=git(['ls-tree','-r','--name-only',base,'--',prefix]).stdout.splitlines()
        for rel in base_files:
            if not (rel.endswith('/USER_REQUEST.txt') or rel.endswith('.txt') or (prefix=='00_INPUT/PROPOSALS' and rel.endswith('.json'))):continue
            if git(['diff','--quiet',base,'HEAD','--',rel]).returncode:
                errors.append('existing immutable raw/provenance record edited since base: '+rel)

    policy=json.loads((ROOT/'08_TOOLCHAIN/TEAM_POLICY.json').read_text())
    entries=policy['integrator_owned']
    # Directory ownership is declared by TEAM_POLICY; infer directory entries from the tree
    # so new protected surfaces do not also require validator code changes.
    directories={x for x in entries if (ROOT/x).is_dir()}
    global_only=set(entries)-directories
    global_prefixes=tuple(x.rstrip('/')+'/' for x in sorted(directories))
    changed_all=git(['diff','--name-only',f'{base}...HEAD']).stdout.splitlines()
    changed_globals=sorted(p for p in changed_all if p in global_only or p.startswith(global_prefixes))
    branch=os.getenv('GITHUB_HEAD_REF') or git(['branch','--show-current']).stdout.strip()
    if changed_globals and not branch.startswith(('infra/','integration/')):
        errors.append('integration-owner workflow files modified on non-integration PR: '+', '.join(changed_globals))
    return errors


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--compare',help='compare immutable inputs/integration ownership against base');a=ap.parse_args()
    errors=validate_all()
    if a.compare:errors+=validate_against_base(a.compare)
    if errors:
        for e in errors:print('FAIL:',e)
        raise SystemExit(1)
    print('PASS: streamlined team contract, raw-request integrity, local secret protection'+(', PR immutability/integration ownership' if a.compare else ''))
if __name__=='__main__':main()
