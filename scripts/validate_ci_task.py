#!/usr/bin/env python3
"""Risk-aware PR delivery gate for streamlined v8 task branches.

Infrastructure/integration PRs are validated by the repository/team contract and
are not forced to carry a gameplay task packet. feat/fix/docs task PRs must have
an approved v8 task and satisfy the task's declared risk gates.
"""
from __future__ import annotations
import argparse, os, re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from streamlined_task import BRANCH,find_changeset,load_task,validate_task
from validate_feature_evidence import changed_src


def git(*args):
    return subprocess.run(['git',*args],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--compare',default='origin/main')
    args=ap.parse_args()
    if git('rev-parse','--verify',args.compare).returncode:
        print('FAIL: comparison base unavailable')
        return 1
    branch=os.getenv('GITHUB_HEAD_REF') or git('branch','--show-current').stdout.strip()
    if branch.startswith(('infra/','integration/','proposal/')):
        print('PASS: infrastructure/integration/legacy proposal PR; task delivery packet not required')
        return 0
    m=BRANCH.fullmatch(branch)
    managed_changed=bool(changed_src(ROOT,args.compare))
    if not m:
        if managed_changed:
            print('FAIL: managed game-changing PR must use feat/fix/docs/<issue>-<slug> task branch')
            return 1
        print('PASS: no managed game-visible change and no streamlined task branch')
        return 0
    issue=int(m.group(1))
    errors=validate_task(issue,ROOT,require_approved=True,require_delivery=managed_changed)
    if not errors and managed_changed:
        dst,meta=load_task(issue,ROOT)
        if meta['gates'].get('studio_required') is True:
            from validate_studio_delivery import validate_delivery
            errors += validate_delivery(dst/'STUDIO_DELIVERY.json',ROOT,expect_issue=issue)
        if meta['gates'].get('full_quality_packet_required') is True:
            from validate_feature_evidence import validate_packet
            errors += validate_packet(dst/'QUALITY_EVIDENCE.json',ROOT)
    if errors:
        for e in errors:print('FAIL:',e)
        return 1
    print(f'PASS: risk-aware delivery gate for GH-{issue:06d}'+(' with managed game-visible changes' if managed_changed else ''))
    return 0

if __name__=='__main__':raise SystemExit(main())
