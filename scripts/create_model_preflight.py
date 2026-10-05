#!/usr/bin/env python3
"""Create or seal a developer/runtime-specific local evidence receipt.

--seal hashes only the referenced local observation files. It never fabricates
those files, sets PASS, or claims to have queried an AI provider.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from model_policy import ROOT, policy
from validate_model_policy import receipt_path, evidence_path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--runtime', required=True)
    ap.add_argument('--developer', default='')
    ap.add_argument('--force', action='store_true', help='archive previous local receipt before replacing')
    ap.add_argument('--seal', action='store_true', help='bind recorded observations to hashes after genuine local runs')
    args = ap.parse_args()
    key = (args.developer + '::' if args.developer else '') + args.runtime
    out = receipt_path(key, ROOT)
    if args.seal:
        if not out.exists():
            raise SystemExit('BLOCKED: create a receipt first, then record real local evidence and run --seal')
        data = json.loads(out.read_text(encoding='utf-8'))
        observations = [data.get('main_observation', {})] + data.get('delegated_observations', [])
        for item in observations:
            if not isinstance(item, dict) or evidence_path(item.get('evidence_file'), ROOT) is None:
                raise SystemExit('BLOCKED: each observation must point to an existing sanitized file under .local/')
        new_hashes = [hashlib.sha256(evidence_path(item['evidence_file'], ROOT).read_bytes()).hexdigest() for item in observations]
        changed = any(item.get('evidence_sha256') != digest for item, digest in zip(observations, new_hashes))
        for item, digest in zip(observations, new_hashes):
            item['evidence_sha256'] = digest
        if changed:
            data['status'] = 'WORK_IN_PROGRESS'
            data['human_verification'] = {'confirmed_by': '', 'confirmed_same_model': False, 'confirmed_reasoning_limits': False}
        out.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
        print('SEALED: hashed local observation files; operator must still inspect active settings and confirm PASS')
        return
    if out.exists():
        if not args.force:
            print(f'PRESERVED: {out.relative_to(ROOT)}; use --force to archive and replace')
            return
        history = ROOT / '.local/model_preflights/history'
        history.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha256(out.read_bytes()).hexdigest()[:16]
        archived = history / f'{out.stem}-{digest}.json'
        if archived.exists():
            raise SystemExit('BLOCKED: identical archived receipt already exists; inspect it before --force')
        out.replace(archived)
    p = policy()['profiles'].get(args.runtime, policy()['profiles']['generic'])
    template = json.loads((ROOT / 'templates/MODEL_PREFLIGHT_TEMPLATE.json').read_text(encoding='utf-8'))
    template['runtime'] = args.runtime
    template['developer'] = args.developer
    template['runtime_key'] = key
    template['selected_model'] = p['model'] or ''
    template['policy_sha256'] = hashlib.sha256((ROOT / '08_TOOLCHAIN/TEAM_MODEL_POLICY.json').read_bytes()).hexdigest()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(template, indent=2) + '\n', encoding='utf-8')
    print(f'CREATED: {out.relative_to(ROOT)} (WORK_IN_PROGRESS; live verification required)')


if __name__ == '__main__':
    main()
