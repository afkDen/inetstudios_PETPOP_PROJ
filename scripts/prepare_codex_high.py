#!/usr/bin/env python3
"""Explicit, issue-scoped GPT-6 Sol High escalation for eligible Codex agents.

Default: PREVIEW ONLY. --activate requires the named human operator's explicit
approval and writes ONLY ignored local artifacts. Human and runtime verification
remain mandatory; this script cannot prove GitHub permissions or active model.
"""
from __future__ import annotations
import argparse, hashlib, json, re, tomllib
from pathlib import Path
from model_policy import ROOT, ModelPolicyError, resolve, roles


def generate(role: str, issue: str, reason: str, approved_by: str, *, activate: bool = False, root: Path = ROOT):
    if not re.fullmatch(r'GH-\d{6}', issue):
        raise ModelPolicyError('issue must be GH- followed by exactly six digits')
    if not isinstance(approved_by, str) or not approved_by.strip():
        raise ModelPolicyError('a named human approver is required; this script cannot verify their authority')
    selection = resolve('codex', role, effort='high', escalate=True, justification=reason)
    prior = root / '.codex/agents' / f'{role}.toml'
    if not prior.is_file():
        raise ModelPolicyError('generate the base Codex adapters before creating a High exception')
    base = tomllib.loads(prior.read_text(encoding='utf-8'))
    if base.get('model') != selection['model'] or base.get('model_reasoning_effort') != 'medium':
        raise ModelPolicyError('base Codex agent was modified or is not Medium; regenerate it first')
    name = f'{role}-{issue.lower()}-high'
    target = root / '.codex/agents' / f'{name}.toml'
    instructions = (base['developer_instructions'] +
        f'\n\nISSUE-ONLY HIGH ESCALATION: {issue}. Authorized by claimed human operator {approved_by}. '
        f'Justification: {reason.strip()}. Use High ONLY for this issue. Do not perform unrelated work, approve your own PR, or bypass the required human review. '
        'The user must verify actual model/effort and GitHub permissions. Delete this local agent when the issue closes.')
    lines = [f'name = {json.dumps(name)}',
             f'description = {json.dumps("ISSUE ONLY " + issue + ": " + base["description"])}',
             f'model = {json.dumps(selection["model"])}',
             'model_reasoning_effort = "high"']
    if base.get('sandbox_mode') == 'read-only':
        lines.append('sandbox_mode = "read-only"')
    lines.append('developer_instructions = ' + json.dumps(instructions, ensure_ascii=False))
    content = '\n'.join(lines) + '\n'
    if not activate:
        return f'PREVIEW: would prepare {target.relative_to(root)}; no files changed. '
    if target.exists():
        raise ModelPolicyError('high agent exists: remove it explicitly before making another issue-specific exception')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding='utf-8')
    log = root / '.local/high_escalations' / f'{name}.json'
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(json.dumps({'schema_version': 1, 'issue': issue, 'role': role,
                'model': selection['model'], 'effort': 'high', 'claimed_human_approver': approved_by.strip(),
                'justification': reason.strip(), 'agent_sha256': hashlib.sha256(content.encode()).hexdigest(),
                'status': 'LOCAL_PENDING_RUNTIME_VERIFICATION', 'not_git_authorization_evidence': True},indent=2)+'\n',encoding='utf-8')
    return f'PREPARED {target.relative_to(root)} for {issue}; restart/refresh Codex agent discovery and verify actual model/effort. Delete with --deactivate after issue.'


def deactivate(role: str, issue: str, root: Path = ROOT):
    if not re.fullmatch(r'GH-\d{6}', issue) or role not in roles():
        raise ModelPolicyError('invalid role or issue')
    name = f'{role}-{issue.lower()}-high'
    agent = root / '.codex/agents' / f'{name}.toml'
    if agent.exists():
        agent.unlink()
    log = root / '.local/high_escalations' / f'{name}.json'
    if log.exists():
        data = json.loads(log.read_text())
        data['status'] = 'DEACTIVATED'
        log.write_text(json.dumps(data, indent=2)+'\n')
    return f'DEACTIVATED {name}; check running Codex sessions manually (they may keep prior settings).'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--role', required=True)
    p.add_argument('--issue', required=True)
    p.add_argument('--justification', default='')
    p.add_argument('--approved-by', default='')
    grp = p.add_mutually_exclusive_group()
    grp.add_argument('--activate', action='store_true')
    grp.add_argument('--deactivate', action='store_true')
    args = p.parse_args()
    try:
        if args.deactivate:
            print(deactivate(args.role, args.issue))
        else:
            print(generate(args.role, args.issue, args.justification, args.approved_by,
                           activate=args.activate))
    except (ModelPolicyError, OSError, KeyError, ValueError) as error:
        raise SystemExit(f'BLOCKED: {error}')


if __name__ == '__main__':
    main()
