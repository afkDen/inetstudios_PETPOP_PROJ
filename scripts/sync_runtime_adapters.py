#!/usr/bin/env python3
"""Generate disposable runtime agent adapters from canonical roles and team model policy.

Generated files are local compatibility artifacts; canonical authority remains AGENTS.md,
roles.json and TEAM_MODEL_POLICY.json. Static adapters do not prove a live model setting.
"""
from __future__ import annotations
import argparse,hashlib,json,shutil
from pathlib import Path
from model_policy import ROOT, policy, resolve, ModelPolicyError

ROLES=json.loads((ROOT/'08_TOOLCHAIN/ROLE_CONTRACTS/roles.json').read_text())['roles']
PROFILES=json.loads((ROOT/'08_TOOLCHAIN/RUNTIME_PROFILES.json').read_text())['profiles']
SKILLS=ROOT/'.agents/skills'
# Limit eager context loading; the full required skill list stays in each role contract.
# Unavailable upstream skills must be installed at global bootstrap, never faked here.
def eager_skills(role):
    return [name for name in role['required_skills'] if (SKILLS/name/'SKILL.md').exists()][:2]


def prompt(role):
    return (ROOT/'08_TOOLCHAIN/ROLE_CONTRACTS'/role['prompt']).read_text(encoding='utf-8')

# Never delete a teammate's own custom agents or modified generated files.
# Each adapter directory records the exact files/trees that THIS generator owns.
OWNERSHIP = '.portable-agent-ownership.json'

def _digest(path:Path):
    h=hashlib.sha256()
    if path.is_file() and not path.is_symlink():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    for entry in sorted(path.rglob('*'),key=lambda x:x.relative_to(path).as_posix()):
        h.update(entry.relative_to(path).as_posix().encode()+b'\0')
        if entry.is_symlink():h.update(b'L'+entry.readlink().as_posix().encode())
        elif entry.is_file():h.update(b'F'+entry.read_bytes())
        elif entry.is_dir():h.update(b'D')
    return h.hexdigest()

def _matches_owned_digest(path:Path, expected:str):
    if _digest(path)==expected:return True
    # Older Windows adapter generation translated LF to CRLF after hashing.
    # Recognize only that exact historical byte change, then rewrite as LF.
    if path.is_file() and not path.is_symlink():
        data=path.read_bytes()
        return b'\r\n' in data and hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest()==expected
    return False

def update_owned(base:Path, outputs:dict[str,str|Path]):
    """Replace only previously generated files, preserve unrelated local agents.

    An unmarked existing path may be adopted only when it is byte-identical
    to the desired output (v6 migration); otherwise, stop for manual review.
    """
    if not base.resolve().is_relative_to(ROOT.resolve()):
        raise RuntimeError('refusing to generate adapters outside project root')
    marker=base/OWNERSHIP
    if marker.is_symlink():raise RuntimeError('adapter ownership marker must not be a symlink')
    previous=json.loads(marker.read_text())['owned'] if marker.exists() else {}
    if not isinstance(previous,dict):raise RuntimeError('invalid adapter ownership manifest')
    desired={}
    for name,source in outputs.items():
        if Path(name).name!=name or name in {'.','..',OWNERSHIP}:
            raise RuntimeError('invalid generated adapter name: '+name)
        src=source if isinstance(source,Path) else None
        if src is not None and (not src.exists() or src.is_symlink()):
            raise RuntimeError('missing/unsafe canonical skill: '+str(src))
        if src is not None and src.is_dir() and any(p.is_symlink() for p in src.rglob('*')):
            raise RuntimeError('canonical skill mirror cannot contain symlinks: '+str(src))
        digest=_digest(src) if src is not None else hashlib.sha256(source.encode('utf-8')).hexdigest()
        desired[name]=(source,digest)
    # Validate all paths BEFORE writing anything; never swallow personal edits.
    for name,old in previous.items():
        current=base/name
        if current.is_symlink():
            raise RuntimeError(f'LOCAL ADAPTER SYMLINK: {current}; inspect manually')
        if current.exists() and not _matches_owned_digest(current,old):
            raise RuntimeError(f'LOCAL ADAPTER MODIFIED: {current}; back it up before regenerating')
    for name,(_,digest) in desired.items():
        current=base/name
        if current.is_symlink():
            raise RuntimeError(f'UNSAFE ADAPTER SYMLINK: {current}; inspect manually')
        if current.exists() and name not in previous and _digest(current)!=digest:
            raise RuntimeError(f'UNMANAGED ADAPTER CONFLICT: {current}; inspect/move manually')
    base.mkdir(parents=True,exist_ok=True)
    for name in previous:
        if name not in desired:
            current=base/name
            if current.is_dir() and not current.is_symlink():shutil.rmtree(current)
            elif current.exists():current.unlink()
    for name,(source,digest) in desired.items():
        current=base/name
        if current.exists() and _digest(current)==digest:continue
        if isinstance(source,Path):
            if current.is_dir() and not current.is_symlink():shutil.rmtree(current)
            elif current.exists() or current.is_symlink():current.unlink()
            shutil.copytree(source,current)
        else:current.write_bytes(source.encode('utf-8'))
    # Deterministic manifest: repeated sync is a true no-op for unchanged skills.
    content=json.dumps({'schema_version':1,'owned':{n:x[1] for n,x in sorted(desired.items())}},indent=2)+'\n'
    if not marker.exists() or marker.read_text()!=content:marker.write_text(content,encoding='utf-8')

def materialize_skill_mirror(dst:Path):
    outputs={d.name:d for d in sorted(SKILLS.iterdir()) if d.is_dir() and (d/'SKILL.md').exists()}
    update_owned(dst,outputs)

def antigravity():
    base=ROOT/'.agents/agents';outputs={}
    cap_to_tool={'repo.read':['view_file','list_dir','grep_search'],
                 'repo.write':['write_to_file','replace_file_content','multi_replace_file_content'],
                 'exec.local':['run_command'],'web.search':['search_web','read_url_content'],
                 'agent.delegate':['invoke_subagent'],'image.generate':['generate_image']}
    for r in ROLES:
        tools=list(dict.fromkeys(t for c in r['required_capabilities'] for t in cap_to_tool.get(c,[])))
        # Antigravity custom agent YAML supports inherit|flash|pro, not an exact model ID
        # or reliably portable per-subagent reasoning-effort override. Do not silently
        # swap to a different model by mapping REVIEW_DEEP to pro.
        # Descriptions may contain `: ` or other YAML syntax; quote them safely.
        fm=['---',f"name: {r['id']}",f"description: {json.dumps(r['description'],ensure_ascii=False)}",
            f"mainAgent: {'true' if r['entrypoint'] else 'false'}",
            f"subagent: {'true' if r['isolated_worker'] else 'false'}",
            'model: inherit','commandExecutionPolicy: sandbox',
            f"inheritCustomizations: {'true' if r['id']=='studio-operator' else 'false'}",'tools:']
        fm += [f'  - {t}' for t in tools]
        fm += ['skills:']+[f'  - skills/{s}' for s in eager_skills(r)]
        if r.get('may_delegate'):fm += ['agents:']+[f'  - agents/{a}' for a in r['may_delegate']]
        fm += ['---','',f"# Local model policy\nThis is an Antigravity adapter for `{r['id']}`. Inherit the *validated* session model. Target `{r['model_class']}` class from `08_TOOLCHAIN/TEAM_MODEL_POLICY.json`. This agent definition cannot enforce actual effort; verify main/subagent runtime selection during preflight. Do not claim Low or High is available without observing it.\n",prompt(r)]
        # Each generated role is one owned directory; unrelated local agents survive.
        outputs[r['id']]='\n'.join(fm)+'\n'
    # For Antigravity, a role is a directory containing agent.md.
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        src=Path(tmp)
        for name,content in outputs.items():
            folder=src/name;folder.mkdir();(folder/'agent.md').write_text(content,encoding='utf-8')
        update_owned(base,{name:src/name for name in outputs})

def claude_code():
    base=ROOT/'.claude/agents';outputs={}
    for r in ROLES:
        eff=resolve('claude-code',r['id'])
        cap=set(r['required_capabilities'])
        read_only=r['write_policy']=='read-only'
        # Studio tools are dynamic MCP names; a fixed built-in allowlist would
        # silently remove the actual Studio bridge from this specialist.
        tools=['Read','Grep','Glob']
        if 'exec.local' in cap and not read_only:tools.append('Bash')
        if 'repo.write' in cap and not read_only:tools+=['Edit','Write']
        if 'web.search' in cap:tools+=['WebSearch','WebFetch']
        if 'agent.delegate' in cap:tools.append('Agent')
        if 'skills.consume' in cap:tools.append('Skill')
        # Exact ID and explicit effort avoid silent alias upgrades and high-effort inheritance.
        fm=['---',f"name: {r['id']}",f"description: {json.dumps(r['description'])}",
            f'model: {eff["model"]}',f'effort: {eff["effort"]}']
        if r['write_policy']=='studio-only' or 'mcp.client' in cap:
            # Dynamic MCP names are runtime-local. Do not accidentally hide an approved
            # Studio/Blender server behind a static built-in allowlist. The role prompt
            # and MCP orchestration skill still require capability probing, least privilege
            # and explicit approval before any new server/install.
            fm += ['# Dynamic MCP role: inherit session tools, then probe/use only approved capability groups.']
            if read_only or r['write_policy']=='studio-only':
                fm.append('disallowedTools: Edit, Write')
        else: fm.append(f'tools: {", ".join(dict.fromkeys(tools))}')
        if eager_skills(r): fm+=['skills:']+[f'  - {skill}' for skill in eager_skills(r)]
        fm += ['---','',f"Model/effort must be `{eff['model']}` / `{eff['effort']}`. Verify active session, environment overrides and per-invocation overrides; no silent fallback. Canonical rules: `AGENTS.md`. Required skills: {', '.join(r['required_skills'])}. Load up to two eager skills here; read other relevant required SKILL.md on demand. External skills absent before global bootstrap are blockers, not reasons to skip skill work.", '',prompt(r)]
        outputs[f"{r['id']}.md"]='\n'.join(fm)+'\n'
    update_owned(base,outputs)
    materialize_skill_mirror(ROOT/'.claude/skills')

def codex():
    base=ROOT/'.codex/agents';outputs={}
    cfg=ROOT/'.codex/config.toml';cfg.parent.mkdir(parents=True,exist_ok=True)
    config='model = "gpt-6.1-sol"\nmodel_reasoning_effort = "medium"\n\n[agents]\nenabled = true\nmax_concurrent_threads_per_session = 3\ndefault_subagent_model = "gpt-6.1-sol"\ndefault_subagent_reasoning_effort = "medium"\n'
    if cfg.exists() and cfg.read_text()!=config:
        raise RuntimeError('LOCAL CODEX CONFIG MODIFIED: inspect/move .codex/config.toml before regeneration')
    for r in ROLES:
        eff=resolve('codex',r['id'])
        instructions=('Canonical master: AGENTS.md. Canonical role: 08_TOOLCHAIN/ROLE_CONTRACTS/roles.json. '
            f'Use skill registry and only relevant required skills: {", ".join(r["required_skills"])}. '
            'Use fresh independent review contexts when required. No unauthorized model substitution. '
            'Higher effort needs explicitly justified invocation, not a silent inherited override.\n\n'+prompt(r))
        parts=[f'name = {json.dumps(r["id"])}',f'description = {json.dumps(r["description"])}',
            f'model = {json.dumps(eff["model"])}',f'model_reasoning_effort = {json.dumps(eff["effort"])}']
        if r['write_policy']=='read-only':parts.append('sandbox_mode = "read-only"')
        parts.append('developer_instructions = '+json.dumps(instructions,ensure_ascii=False))
        outputs[f"{r['id']}.toml"]='\n'.join(parts)+'\n'
    update_owned(base,outputs)
    # Only write the default config after all agent ownership/conflicts have passed.
    # Otherwise an unmanaged local agent collision could leave a partial setup.
    if not cfg.exists():cfg.write_text(config,encoding='utf-8')

def simple_agents(runtime,base:Path,suffix='.md'):
    outputs={}
    for r in ROLES:
        # Generic adapter: a human-verified local mapping is required; never pretend
        # this Markdown instruction overrides the runtime's actual model selector.
        outputs[r['id']+suffix]=f"# Runtime adapter: {r['id']}\n\nCanonical master: `AGENTS.md`. Canonical role: `08_TOOLCHAIN/ROLE_CONTRACTS/roles.json`.\n\nModel class: `{r['model_class']}`. Resolve via `08_TOOLCHAIN/TEAM_MODEL_POLICY.json`; verify model and effort on this runtime. Required skills: {', '.join(r['required_skills']) or 'none'}.\n\n"+prompt(r)
    update_owned(base,outputs)

def sync(runtime):
    if runtime not in PROFILES:runtime='generic'
    if runtime=='antigravity':antigravity()
    elif runtime=='claude-code':claude_code()
    elif runtime=='codex':codex()
    elif runtime=='gemini-cli':simple_agents(runtime,ROOT/'.gemini/agents')
    elif runtime=='cursor':simple_agents(runtime,ROOT/'.cursor/agents')
    elif runtime=='github-copilot':simple_agents(runtime,ROOT/'.github/agents',suffix='.agent.md')
    print(f'PASS: generated {runtime} runtime adapter; live model/effort still requires explicit validation')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--runtime',default='generic');a=ap.parse_args();sync(a.runtime)
if __name__=='__main__':main()
