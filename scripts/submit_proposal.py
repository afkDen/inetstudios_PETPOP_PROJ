#!/usr/bin/env python3
"""Byte-preserving, collision-free GitHub-Issue-scoped proposal intake.

Creates proposal artifacts in the branch; never calls GitHub or mutates main.
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PROPOSALS = ROOT / '00_INPUT' / 'PROPOSALS'


def issue_key(n: int) -> str:
    if n < 1 or n > 999999: raise ValueError('issue must be between 1 and 999999')
    return f'GH-{n:06d}'


def slugify(s: str) -> str:
    s = re.sub(r'[^a-z0-9]+','-', Path(s).stem.lower()).strip('-')
    return s[:55].strip('-') or 'proposal'


def add_proposal(source: Path, issue: int, author: str, kind: str, root: Path=ROOT):
    if kind not in {'idea','update'}: raise ValueError('kind must be idea or update')
    if not re.fullmatch(r'[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,37}[a-zA-Z0-9])?',author):
        raise ValueError('author must be a GitHub username, no email or path')
    source=Path(source)
    if source.suffix.lower()!='.txt' or not source.is_file(): raise ValueError('provide an existing .txt source')
    raw=source.read_bytes()
    if not raw or len(raw)>256*1024: raise ValueError('proposal must be between 1 byte and 256 KiB')
    key=issue_key(issue); destroot=root/'00_INPUT'/'PROPOSALS'
    if list(destroot.rglob(key+'_*.txt')): raise FileExistsError(f'{key} already has a proposal (use issue discussion or a new issue)')
    slug=slugify(source.name)
    folder=destroot/('IDEAS' if kind=='idea' else 'UPDATES')
    folder.mkdir(parents=True,exist_ok=True)
    dest=folder/f'{key}_{slug}.txt'
    # Exclusive creation; never modify already-proposed raw bytes.
    with dest.open('xb') as f: f.write(raw)
    try:
        head=subprocess.run(['git','rev-parse','HEAD'],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,check=False)
        metadata={'schema_version':1,'issue':issue,'key':key,'kind':kind,'submitted_by':author,'source_filename':source.name,'sha256':hashlib.sha256(raw).hexdigest(),'base_commit':head.stdout.strip() if head.returncode==0 else None,'raw_file':dest.relative_to(root).as_posix()}
        dest.with_suffix('.json').write_text(json.dumps(metadata,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    except Exception:
        dest.unlink(missing_ok=True)
        raise
    return dest


def main():
    ap=argparse.ArgumentParser(description='Copy a raw .txt idea/update into a unique issue-backed proposal without changing original bytes.')
    ap.add_argument('--kind',required=True,choices=['idea','update'])
    ap.add_argument('--issue',type=int,required=True)
    ap.add_argument('--by',required=True,help='GitHub username')
    ap.add_argument('--source',type=Path,required=True,help='Original Notepad .txt path (not overwritten)')
    args=ap.parse_args()
    try:
        dest=add_proposal(args.source,args.issue,args.by,args.kind)
    except (ValueError,FileExistsError) as e:
        ap.error(str(e))
    print(dest.relative_to(ROOT).as_posix())
if __name__=='__main__':main()
