#!/usr/bin/env python3
"""Small Graphify wrapper that keeps local repo intelligence optional, reproducible and cheap."""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'graphify-out/graph.json'

def call(args):
    exe=shutil.which('graphify')
    if not exe:raise SystemExit('BLOCKED: graphify unavailable. Run `python scripts/workstation_doctor.py` for the pinned install plan.')
    return subprocess.run([exe,*args],cwd=ROOT,check=False)

def main():
    ap=argparse.ArgumentParser(description=__doc__); sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('status'); sub.add_parser('build'); sub.add_parser('update')
    q=sub.add_parser('query'); q.add_argument('question')
    p=sub.add_parser('path'); p.add_argument('a');p.add_argument('b')
    e=sub.add_parser('explain');e.add_argument('node')
    a=ap.parse_args()
    if a.cmd=='status':
        print(json.dumps({'installed':bool(shutil.which('graphify')),'graph_exists':OUT.exists(),'graph_path':str(OUT.relative_to(ROOT))},indent=2));return 0
    if a.cmd=='build':return call(['extract','.','--code-only','--no-viz']).returncode
    if a.cmd=='update':
        return call(['update','.']).returncode if OUT.exists() else call(['extract','.','--code-only','--no-viz']).returncode
    if not OUT.exists():raise SystemExit('BLOCKED: no Graphify graph yet. Run `python scripts/graphify_sync.py build`.')
    if a.cmd=='query':return call(['query',a.question]).returncode
    if a.cmd=='path':return call(['path',a.a,a.b]).returncode
    if a.cmd=='explain':return call(['explain',a.node]).returncode
    return 2
if __name__=='__main__':raise SystemExit(main())
