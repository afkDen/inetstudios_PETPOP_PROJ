#!/usr/bin/env python3
"""Render a role packet for runtimes without reliable native agent scoping."""
import argparse,json
from pathlib import Path
from model_policy import ROOT, resolve,ModelPolicyError

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--role',required=True);ap.add_argument('--task',required=True)
    ap.add_argument('--runtime',default='generic');ap.add_argument('--model',default=None)
    ap.add_argument('--effort',default=None);ap.add_argument('--escalate',action='store_true');ap.add_argument('--justification',default='')
    a=ap.parse_args()
    roles={r['id']:r for r in json.loads((ROOT/'08_TOOLCHAIN/ROLE_CONTRACTS/roles.json').read_text())['roles']}
    if a.role not in roles:raise SystemExit(f'Unknown role {a.role}')
    r=roles[a.role];prompt=(ROOT/'08_TOOLCHAIN/ROLE_CONTRACTS'/r['prompt']).read_text()
    try:
        eff=resolve(a.runtime,a.role,a.effort,a.model,escalate=a.escalate,justification=a.justification)
        selection=f"Requested model: `{eff['model']}`\nRequested effort: `{eff['effort']}`\nLive verification: REQUIRED before execution\n"
    except ModelPolicyError as e:
        if a.runtime=='generic' and not a.model:
            selection='Requested model: UNRESOLVED — human must approve a real runtime/model before executing this packet.\nRequested effort: use class baseline, verify supported equivalent.\n'
        else:raise SystemExit(f'POLICY BLOCKED: {e}')
    print(f"# Portable Role Packet: {r['id']}\n\nMaster contract: read and obey root `AGENTS.md`.\nModel class: {r['model_class']}\n{selection}Required capabilities: {', '.join(r['required_capabilities'])}\nRequired skills: {', '.join(r['required_skills']) or 'none'}\nWrite policy: {r['write_policy']}\nFresh context required: {r['fresh_context_required']}\n\n## Role instructions\n{prompt}\n\n## Assigned task\n{a.task}\n")
if __name__=='__main__':main()
