#!/usr/bin/env python3
from __future__ import annotations
import argparse, re, shutil, json, hashlib, sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "00_INPUT" / "UPDATES" / "INBOX"
PROCESSING = ROOT / "00_INPUT" / "UPDATES" / "PROCESSING"
CHANGESETS = ROOT / "04_CHANGESETS"
TEMPLATE = ROOT / "templates" / "CHANGESET_TEMPLATE"

def next_update_id() -> str:
    max_id = 0
    pat = re.compile(r"(?:^|_)U(\d{3})(?:_|-)")
    for p in CHANGESETS.glob("*"):
        m = pat.search(p.name)
        if m:
            max_id = max(max_id, int(m.group(1)))
    for base in (PROCESSING, ROOT / "00_INPUT" / "UPDATES" / "PROCESSED"):
        for p in base.glob("*"):
            m = re.search(r"U(\d{3})", p.name)
            if m:
                max_id = max(max_id, int(m.group(1)))
    return f"U{max_id + 1:03d}"

def slugify(name: str) -> str:
    s = re.sub(r"\.[^.]+$", "", name)
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s[:60] or "update"

def create_changeset(src: Path, update_id: str | None = None) -> Path:
    if not src.exists() or src.parent.resolve() != INBOX.resolve():
        raise SystemExit(f"Input must be a file directly inside {INBOX}")
    update_id = update_id or next_update_id()
    slug = slugify(src.name)
    dirname = f"{date.today().isoformat()}_{update_id}_{slug}"
    dst = CHANGESETS / dirname
    if dst.exists():
        raise SystemExit(f"Changeset already exists: {dst}")
    shutil.copytree(TEMPLATE, dst)
    raw = src.read_bytes()
    (dst / "USER_REQUEST.txt").write_bytes(raw)
    PROCESSING.mkdir(parents=True, exist_ok=True)
    moved = PROCESSING / f"{update_id}_{src.name}"
    shutil.move(str(src), str(moved))
    print(dst.relative_to(ROOT))
    return dst


def create_issue_changeset(proposal: Path, issue: int) -> Path:
    """Create one branch-local GH issue changeset; never move the shared proposal."""
    proposals = ROOT / '00_INPUT/PROPOSALS'
    proposal = Path(proposal)
    if not proposal.is_absolute(): proposal = ROOT / proposal
    if not proposal.is_file() or proposal.is_symlink() or proposal.suffix.lower() != '.txt':
        raise ValueError('provide a real issue-backed proposal .txt')
    # Resolve before testing containment, excluding symlink/path escapes.
    if proposal.resolve().parent not in ((proposals/'IDEAS').resolve(), (proposals/'UPDATES').resolve()):
        raise ValueError('proposal must be directly in IDEAS or UPDATES')
    key=f'GH-{issue:06d}'
    if not (1 <= issue <= 999999) or not proposal.name.startswith(key+'_'):
        raise ValueError('proposal must match the requested GitHub Issue number')
    metadata=proposal.with_suffix('.json')
    if not metadata.is_file() or metadata.is_symlink():raise ValueError('missing proposal metadata')
    meta=json.loads(metadata.read_text())
    raw=proposal.read_bytes()
    if (meta.get('issue')!=issue or meta.get('sha256')!=hashlib.sha256(raw).hexdigest() or
            meta.get('raw_file')!=proposal.relative_to(ROOT).as_posix()):
        raise ValueError('proposal hash, location or issue ID does not match metadata')
    if list(CHANGESETS.glob(key+'_*')):raise ValueError(f'{key} already has a changeset on this branch')
    name=f'{key}_{slugify(proposal.stem[len(key)+1:])}'
    # The canonical issue ID is stable; no branch-local U### allocation.
    dst=CHANGESETS/name
    shutil.copytree(TEMPLATE,dst)
    (dst/'USER_REQUEST.txt').write_bytes(raw)
    (dst/'SOURCE_PROPOSAL.json').write_text(json.dumps({'schema_version':1,'issue':issue,'source':meta['raw_file'],'sha256':meta['sha256'],'author':meta.get('submitted_by')},indent=2)+'\n')
    return dst

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?", help="Inbox filename")
    ap.add_argument("--next", action="store_true", help="Process the lexically first .txt file in inbox")
    ap.add_argument('--proposal', type=Path, help='Issue-backed synced proposal path (team mode)')
    ap.add_argument('--issue', type=int, help='GitHub Issue number; required with --proposal')
    ap.add_argument('--solo', action='store_true', help='Explicit legacy solo U### intake (unsafe on concurrent team branches)')
    args = ap.parse_args()
    if args.proposal:
        if args.issue is None: ap.error('--issue required with --proposal')
        dst=create_issue_changeset(args.proposal,args.issue)
        print(dst.relative_to(ROOT))
        return
    team_policy = ROOT/'08_TOOLCHAIN/TEAM_POLICY.json'
    if team_policy.exists() and json.loads(team_policy.read_text()).get('collaboration_enabled') and not args.solo:
        ap.error('Team mode requires --proposal PATH --issue N. Use --solo only for legacy offline sequential intake.')
    candidates = sorted(p for p in INBOX.iterdir() if p.is_file() and p.suffix.lower()==".txt")
    if args.next:
        if not candidates:
            raise SystemExit("No .txt files in inbox.")
        src = candidates[0]
    elif args.file:
        src = INBOX / args.file
    else:
        raise SystemExit("Provide a filename or --next.")
    create_changeset(src)

if __name__ == "__main__":
    main()
