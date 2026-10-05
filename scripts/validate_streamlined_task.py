#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from streamlined_task import validate_task,load_task


def main() -> int:
    ap=argparse.ArgumentParser(description='Validate one v8 streamlined issue changeset')
    ap.add_argument('--issue',type=int,required=True)
    ap.add_argument('--require-approved',action='store_true')
    ap.add_argument('--require-delivery',action='store_true')
    args=ap.parse_args()
    errors=validate_task(args.issue,ROOT,require_approved=args.require_approved,require_delivery=args.require_delivery)
    if not errors and args.require_delivery:
        dst,meta=load_task(args.issue,ROOT)
        if meta['gates'].get('studio_required') is True:
            from validate_studio_delivery import validate_delivery
            errors += validate_delivery(dst/'STUDIO_DELIVERY.json',ROOT,expect_issue=args.issue)
        if meta['gates'].get('full_quality_packet_required') is True:
            from validate_feature_evidence import validate_packet
            errors += validate_packet(dst/'QUALITY_EVIDENCE.json',ROOT)
    if errors:
        for e in errors: print('FAIL:',e)
        return 1
    print('PASS: streamlined task integrity'+(' and delivery gates' if args.require_delivery else ''))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
