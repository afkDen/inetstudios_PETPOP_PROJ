#!/usr/bin/env python3
"""Portable role-class -> model/effort policy. Never implies an actual provider connection."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT/'08_TOOLCHAIN/TEAM_MODEL_POLICY.json'
ROLES_PATH = ROOT/'08_TOOLCHAIN/ROLE_CONTRACTS/roles.json'
EFFORT_ORDER = ('low', 'medium', 'high')

class ModelPolicyError(ValueError): pass

def policy(): return json.loads(POLICY_PATH.read_text(encoding='utf-8'))
def roles(): return {r['id']:r for r in json.loads(ROLES_PATH.read_text(encoding='utf-8'))['roles']}
def profile(runtime):
    p=policy()['profiles']
    return p.get(runtime,p['generic'])

def resolve(runtime, role_id, effort=None, model=None, *, escalate=False, justification='', available_efforts=None):
    """Resolve policy (not live verification). Higher effort needs explicit, recorded justification.

    Unknown runtimes must supply an explicitly approved model in local configuration;
    this function does not guess. `available_efforts` is optional, direct runtime evidence.
    """
    pol=policy(); r=roles().get(role_id)
    if r is None:raise ModelPolicyError(f'unknown role: {role_id}')
    p=profile(runtime)
    chosen_model=model if model is not None else p['model']
    if not chosen_model:raise ModelPolicyError('unknown runtime: an explicitly human-approved model is required')
    if p['model'] and chosen_model != p['model']:
        raise ModelPolicyError(f'{runtime} permits only {p["model"]}; {chosen_model} is an unapproved substitution')
    desired=effort or pol['baseline_effort_by_class'][r['model_class']]
    if desired not in p['allowed_efforts']:
        raise ModelPolicyError(f'{runtime} does not permit effort={desired}')
    if desired == 'high':
        if p['high_policy']!='explicit_justification_only' or r['model_class'] not in p.get('high_eligible_classes',[]):
            raise ModelPolicyError(f'high effort prohibited for {runtime}/{role_id}')
        if not escalate or len(justification.strip())<15:
            raise ModelPolicyError('high requires --escalate and a concrete justification (15+ chars)')
    fallback=None
    if available_efforts is not None and desired not in available_efforts:
        if (desired=='low' and r['model_class']=='FAST' and
            p['unavailable_effort_policy']=='documented_medium_fallback_for_fast_only' and
            'medium' in available_efforts):
            desired='medium';fallback='FAST low unavailable; medium used only after explicit runtime capability evidence'
        else:raise ModelPolicyError(f'requested effort {desired} is unavailable in the active runtime')
    return {'runtime':runtime,'role':role_id,'model':chosen_model,'effort':desired,
            'model_class':r['model_class'],'escalation_justification':justification.strip() if desired=='high' else None,
            'fallback_note':fallback,'live_verified':False}

def validate_policy_structure(root=ROOT):
    """Check policy data against canonical role classes and known current runtime profiles."""
    p=json.loads((root/'08_TOOLCHAIN/TEAM_MODEL_POLICY.json').read_text())
    r=json.loads((root/'08_TOOLCHAIN/ROLE_CONTRACTS/roles.json').read_text())['roles']
    canonical={x['model_class'] for x in r}
    if set(p['baseline_effort_by_class'])!=canonical:raise ModelPolicyError('incomplete model class effort mapping')
    if any(v!='medium' for v in p['baseline_effort_by_class'].values()):
        raise ModelPolicyError('baseline policy must be MEDIUM for all consolidated role classes')
    if p['profiles']['claude-code']['model']!='claude-opus-5-5' or p['profiles']['claude-code']['allowed_efforts']!=['low','medium']:
        raise ModelPolicyError('Claude strict Opus/low-medium policy changed')
    if p['profiles']['codex']['model']!='gpt-6.1-sol' or p['profiles']['codex']['allowed_efforts']!=['low','medium','high']:
        raise ModelPolicyError('Codex strict GPT-6.1 Sol/low-high policy changed')
    for key,config in p['profiles'].items():
        if config['default_effort']!='medium':raise ModelPolicyError(f'{key}: default must be medium')
        if not config['allow_unapproved_model_substitution'] is False:raise ModelPolicyError(f'{key}: no silent substitution')
        if not set(config['allowed_efforts']).issubset(EFFORT_ORDER):raise ModelPolicyError(f'{key}: unknown efforts')
    return True
