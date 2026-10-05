#!/usr/bin/env python3
"""Validate a *local, human-confirmed* model/effort preflight.

This is a consistency/integrity gate, NOT provider attestation. Only the active
runtime/operator can actually observe the model, effort, and delegated workers.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from model_policy import ROOT, ModelPolicyError, EFFORT_ORDER, resolve, validate_policy_structure

LEGACY = ROOT / '.local/MODEL_PREFLIGHT.json'
DEFAULT = LEGACY  # Read-only migration fallback for older v7 local receipts.
REQUIRED_ROLES = {'implementation-worker', 'assurance-reviewer'}
KNOWN_CAPABILITIES = set(EFFORT_ORDER) | {'none', 'minimal', 'xhigh', 'max'}


def receipt_path(runtime_key: str, root: Path = ROOT) -> Path:
    """Store receipts independently for multiple developers/runtimes per clone."""
    if not isinstance(runtime_key, str) or not runtime_key or len(runtime_key) > 256:
        raise ValueError('nonempty runtime key of at most 256 characters required')
    label = re.sub(r'[^a-zA-Z0-9_.-]+', '-', runtime_key).strip('-.')[:54] or 'runtime'
    suffix = hashlib.sha256(runtime_key.encode('utf-8')).hexdigest()[:12]
    return root / '.local/model_preflights' / f'{label}-{suffix}.json'


def policy_sha(root: Path = ROOT) -> str:
    return hashlib.sha256((root / '08_TOOLCHAIN/TEAM_MODEL_POLICY.json').read_bytes()).hexdigest()


def evidence_path(path: object, root: Path) -> Path | None:
    if not isinstance(path, str) or not path.startswith('.local/'):
        return None
    try:
        local_root = (root / '.local').resolve()
        resolved = (root / path).resolve()
        if not resolved.is_relative_to(local_root) or not resolved.is_file():
            return None
        if not 10 <= resolved.stat().st_size <= 2_000_000:
            return None
        return resolved
    except (OSError, ValueError):
        return None


def observation_valid(item: object, root: Path) -> bool:
    if not isinstance(item, dict):
        return False
    path = evidence_path(item.get('evidence_file'), root)
    digest = item.get('evidence_sha256')
    if not path or not isinstance(digest, str) or len(digest) != 64:
        return False
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest() == digest
    except OSError:
        return False


def validate(receipt: Path | None = None, root: Path = ROOT, runtime_key: str | None = None,
             *, require_delegates: bool = True) -> list[str]:
    errors: list[str] = []
    if receipt is None:
        if not runtime_key:
            return ['runtime_key required to select a developer/runtime-specific receipt']
        receipt = receipt_path(runtime_key, root)
        if not receipt.exists() and (root / '.local/MODEL_PREFLIGHT.json').exists():
            receipt = root / '.local/MODEL_PREFLIGHT.json'
    path = Path(receipt)
    if not path.exists():
        return ['model preflight missing: inspect active main and delegated model/effort in this runtime']
    try:
        if not path.resolve().is_relative_to((root / '.local').resolve()):
            return ['model preflight must remain under ignored .local/']
        record = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError, TypeError):
        return ['model preflight is unreadable or invalid JSON']
    if not isinstance(record, dict):
        return ['model preflight must be a JSON object']
    runtime = record.get('runtime')
    if not isinstance(runtime, str) or not runtime:
        return ['runtime is missing']
    developer = record.get('developer', '')
    if not isinstance(developer, str):
        return ['developer field must be a string']
    identity = (developer + '::' if developer else '') + runtime
    if record.get('runtime_key') != identity:
        errors.append('receipt identity does not match developer/runtime fields')
    if runtime_key and runtime_key != identity:
        errors.append('receipt identity differs from active developer/runtime')
    if record.get('status') != 'PASS':
        errors.append('preflight is not PASS')
    if record.get('policy_sha256') != policy_sha(root):
        errors.append('model policy changed since receipt; revalidate')
    try:
        profile = json.loads((root / '08_TOOLCHAIN/TEAM_MODEL_POLICY.json').read_text())['profiles']
        conf = profile.get(runtime, profile['generic'])
    except (OSError, ValueError, KeyError, TypeError):
        return errors + ['model policy invalid or missing']
    mid = record.get('selected_model')
    if not isinstance(mid, str) or not mid or (conf['model'] and mid != conf['model']):
        errors.append('selected model does not match the exact team-approved model')
    available = record.get('available_efforts_observed', [])
    if not isinstance(available, list) or any(not isinstance(v, str) for v in available):
        errors.append('available_efforts_observed must be a list of effort names')
        available = []
    if len(available) != len(set(available)) or any(v not in KNOWN_CAPABILITIES for v in available):
        errors.append('observed effort capabilities contain duplicates or unknown names')
    # Provider availability is NOT the team allowlist; e.g. Claude may expose High,
    # but no Claude worker in this team is permitted to select it.
    if 'medium' not in available:
        errors.append('observed effort capabilities must include Medium')
    main = record.get('main_observation')
    if not isinstance(main, dict) or main.get('model') != mid or main.get('effort') != 'medium' or not observation_valid(main, root):
        errors.append('main agent requires a hash-bound local trace of exact model at Medium')
    delegates = record.get('delegated_observations', [])
    if not isinstance(delegates, list):
        errors.append('delegated_observations must be a list')
        delegates = []
    seen: set[str] = set()
    for item in delegates:
        if not isinstance(item, dict):
            errors.append('delegated observation must be an object')
            continue
        role = item.get('role')
        if not isinstance(role, str) or not role:
            errors.append('delegated observation has invalid role')
            continue
        if role in seen:
            errors.append(f'{role}: duplicate delegate evidence is not independent execution')
        seen.add(role)
        if item.get('model') != mid:
            errors.append(f'{role}: delegated model differs from exact approved model')
        effort = item.get('effort')
        if effort not in available or effort not in conf['allowed_efforts']:
            errors.append(f'{role}: effort not observed or outside the team allowlist')
        else:
            try:
                # A high-effort exception is issue-specific, never a default config.
                justification = item.get('escalation_justification', '')
                if not isinstance(justification, str):
                    justification = ''
                expected = resolve(runtime, role, effort=effort, model=mid,
                                   escalate=effort == 'high', justification=justification,
                                   available_efforts=available)
            except ModelPolicyError as exc:
                errors.append(f'{role}: {exc}')
        if not observation_valid(item, root):
            errors.append(f'{role}: missing or changed hash-bound local execution trace')
    if require_delegates and not REQUIRED_ROLES.issubset(seen):
        errors.append('need separate delegated BALANCED implementation and REVIEW_DEEP assurance execution traces')
    human = record.get('human_verification')
    if not isinstance(human, dict) or not isinstance(human.get('confirmed_by'), str) or not human.get('confirmed_by', '').strip() or not human.get('confirmed_same_model') or not human.get('confirmed_reasoning_limits'):
        errors.append('human confirmation of observed main/delegate model and effort required')
    return errors


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--check-config', action='store_true', help='validate shared model policy schema without a live receipt')
    ap.add_argument('--runtime-key', required=False)
    ap.add_argument('--receipt', type=Path, default=None)
    args = ap.parse_args()
    if args.check_config:
        try:
            validate_policy_structure(ROOT)
        except (ModelPolicyError, KeyError, ValueError, OSError) as exc:
            raise SystemExit(f'BLOCKED: shared model policy invalid: {exc}')
        print('PASS: shared model policy and role classes are structurally consistent (not live runtime evidence)')
        return
    if not args.runtime_key:
        ap.error('--runtime-key required except when checking static config')
    errors = validate(args.receipt, ROOT, args.runtime_key)
    if errors:
        for error in errors:
            print('BLOCKED:', error)
        raise SystemExit(2)
    print('PASS: local, hash-bound model/effort receipt is consistent with shared policy; live authenticity remains human-verified')


if __name__ == '__main__':
    main()
