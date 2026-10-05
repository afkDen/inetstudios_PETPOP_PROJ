#!/usr/bin/env python3
"""Bind this reusable bootstrap scaffold to a NEW GitHub repository, without Git writes.

Run FROM THE EXTRACTED BOOTSTRAP after creating / cloning a separate game repo:
    python scripts/prepare_new_game.py --repo-url https://github.com/OWNER/NEW-GAME.git --destination PATH [--maintainer USER]

Copies only the distributable scaffold into an empty target directory (or into a
truly empty git clone). Never overwrites files, configures Git, commits or pushes.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
URL = re.compile(r'https://github\.com/([A-Za-z0-9](?:[A-Za-z0-9-]{0,38}[A-Za-z0-9])?)/([A-Za-z0-9][A-Za-z0-9_.-]*?)(?:\.git)?/?\Z', re.I)
USERNAME = re.compile(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?\Z')
# Never copy local secrets, Git history, generated evidence, untrusted caches or native output.
SKIP_DIRS = {'.git', '.local', '.worktrees', 'build', 'dist', 'out', '.venv', 'venv', '__pycache__', 'node_modules', '.pytest_cache', '.runtime_generated', '.system_generated', '.claude', '.codex', '.cursor', '.gemini', '.antigravity'}
SKIP_SUBTREES = {('.agents', 'agents'), ('.github', 'agents')}
SKIP_FILES = {'.env', '.env.local', '.DS_Store', 'Thumbs.db', 'desktop.ini'}
SKIP_SUFFIXES = {'.pyc', '.pyo', '.pem', '.key', '.p12'}
SOURCE_URL = 'https://github.com/REPLACE_OWNER/REPLACE_REPOSITORY.git'


def parse_url(raw: str) -> tuple[str, str, str]:
    m = URL.fullmatch(raw.strip())
    if not m:
        raise ValueError('Only a plain HTTPS GitHub repository URL is allowed: https://github.com/OWNER/REPO.git (no tokens, query or fragment)')
    owner, repo = m.groups()
    if repo in {'.', '..'} or '..' in repo or repo.endswith('.'):
        raise ValueError('Invalid GitHub repository name')
    return f'https://github.com/{owner}/{repo}.git', owner, repo


def norm_remote(url: str) -> str:
    url = url.strip()
    if url.startswith('git@github.com:'):
        url = 'https://github.com/' + url.partition(':')[2]
    if url.startswith('ssh://git@github.com/'):
        url = 'https://github.com/' + url.split('ssh://git@github.com/', 1)[1]
    return url.removesuffix('.git').rstrip('/').lower()


def preflight(destination: Path, url: str) -> None:
    src = ROOT.resolve()
    target = destination.resolve()
    if target == src or src in target.parents or target in src.parents:
        raise ValueError('Destination must be separate from the bootstrap source folder')
    if destination.is_symlink():
        raise ValueError('Destination cannot be a symlink')
    if destination.exists():
        if not destination.is_dir():
            raise ValueError('Destination exists but is not a directory')
        entries = list(destination.iterdir())
        if any(x.name != '.git' for x in entries):
            raise ValueError('Destination is not empty. Clone an empty NEW repository or choose a new empty folder; no files were changed.')
        if entries:
            if entries[0].is_symlink():
                raise ValueError('The target Git directory cannot be a symlink')
            result = subprocess.run(['git', '-C', str(destination), 'remote', 'get-url', 'origin'],
                                    capture_output=True, text=True, check=False)
            if result.returncode or norm_remote(result.stdout) != norm_remote(url):
                raise ValueError('Existing clone origin differs from the provided NEW repository URL; no files were changed.')


def copy_scaffold(destination: Path) -> None:
    for entry in ROOT.rglob('*'):
        rel = entry.relative_to(ROOT)
        if any(part in SKIP_DIRS or part == '.bootstrap_private' for part in rel.parts):
            continue
        if any(tuple(rel.parts[:len(prefix)]) == prefix for prefix in SKIP_SUBTREES):
            continue
        if entry.is_symlink():
            raise ValueError(f'Symlinks are not shipped by this bootstrap: {rel}')
        if entry.is_dir():
            continue
        if entry.name in SKIP_FILES or entry.suffix.lower() in SKIP_SUFFIXES:
            continue
        dest = destination / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive create ensures this tool cannot overwrite unanticipated work.
        with entry.open('rb') as inp, dest.open('xb') as out:
            shutil.copyfileobj(inp, out)


def bind(destination: Path, url: str, maintainer: str, repo: str) -> None:
    p = destination / '08_TOOLCHAIN/TEAM_POLICY.json'
    config = json.loads(p.read_text(encoding='utf-8'))
    if config.get('template_unconfigured') is not True or config.get('remote_url') != SOURCE_URL:
        raise ValueError('Source is not the unconfigured reusable bootstrap; never reset an already-initialized game')
    config['remote_url'] = url
    config['human_integrators'] = [maintainer]
    config['template_unconfigured'] = False
    p.write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
    c = destination / '.github/CODEOWNERS'
    content = c.read_text(encoding='utf-8')
    if '@REPLACE_MAINTAINER' not in content:
        raise ValueError('Missing template CODEOWNERS placeholder; inspect before proceeding')
    c.write_text(content.replace('@REPLACE_MAINTAINER', '@' + maintainer), encoding='utf-8')
    for rel in ['TEAM_ONBOARDING.md', 'TEAM_PROTOCOL.md', 'TEAM_IMPORT_GITHUB.md', 'NEW_GAME_SETUP.md']:
        f = destination / rel
        txt = f.read_text(encoding='utf-8')
        txt = txt.replace('https://github.com/REPLACE_OWNER/REPLACE_REPOSITORY.git', url)
        txt = txt.replace('https://github.com/REPLACE_OWNER/REPLACE_REPOSITORY', url.removesuffix('.git'))
        f.write_text(txt, encoding='utf-8')
    for rel, name in [('default.project.json', repo), ('templates/rojo-world-opt-in.project.json', repo + '-world-opt-in-EXAMPLE')]:
        f = destination / rel
        cfg = json.loads(f.read_text(encoding='utf-8'))
        cfg['name'] = name
        f.write_text(json.dumps(cfg, indent=2) + '\n', encoding='utf-8')
    (destination / 'PREPARED_GAME.json').write_text(json.dumps({
        'schema_version': 1,
        'target_repository': url,
        'maintainer': maintainer,
        'scaffold_version': 'v8.5-scope-evolution',
        'global_bootstrap_status': 'INITIALIZATION_REQUIRED',
        'proof_of_github_access': False,
        'proof_of_studio_validation': False
    }, indent=2) + '\n', encoding='utf-8')


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo-url', required=True, help='New HTTPS GitHub repository clone URL')
    p.add_argument('--destination', required=True, type=Path, help='New empty folder or freshly cloned empty repository')
    p.add_argument('--maintainer', help='GitHub username of human integration owner (default: repository owner)')
    args = p.parse_args(argv)
    try:
        url, owner, repo = parse_url(args.repo_url)
        maintainer = args.maintainer or owner
        if not USERNAME.fullmatch(maintainer):
            raise ValueError('Maintainer must be a valid GitHub username (for organization repos pass --maintainer explicitly)')
        # Validate all source template preconditions before copying anything.
        policy = json.loads((ROOT / '08_TOOLCHAIN/TEAM_POLICY.json').read_text(encoding='utf-8'))
        if not policy.get('template_unconfigured') or policy.get('remote_url') != SOURCE_URL:
            raise ValueError('This folder is not the unconfigured bootstrap package. Never derive new games from an initialized game without a reviewed template export.')
        preflight(args.destination, url)
        args.destination.mkdir(parents=True, exist_ok=True)
        copy_scaffold(args.destination)
        bind(args.destination, url, maintainer, repo)
    except (ValueError, OSError) as exc:
        p.exit(2, f'BLOCKED: {exc}\n')
    print(f'PREPARED: {args.destination}')
    print(f'Target origin expected: {url}')
    print(f'Integrator: {maintainer}; fresh shared initialization is required')
    print('No Git remote, branches, commits, pushes, external skills, or Studio place were modified.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
