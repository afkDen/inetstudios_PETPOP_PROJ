#!/usr/bin/env python3
"""Offline project-layout guard: Rojo owns only three versioned script subtrees.
CLI build is separately performed when Rojo is installed; static checks do
not constitute a successful native Rojo build or Studio playtest.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EXPECTED={
 'ReplicatedStorage/GameShared':'src/shared',
 'ServerScriptService/GameServer':'src/server',
 'StarterPlayer/StarterPlayerScripts/GameClient':'src/client',
}
def validate(root=ROOT):
    errors=[]
    try:
        j=json.loads((root/'default.project.json').read_text())
    except (OSError,ValueError) as exc:
        return [f'invalid/missing default.project.json: {exc}']
    t=j.get('tree',{})
    if t.get('$className')!='DataModel' or t.get('$ignoreUnknownInstances') is not True:
        errors.append('root must preserve unmanaged game content')
    def walk(tree,path=''):
        for key,val in tree.items():
            if key.startswith('$') or not isinstance(val,dict):continue
            name=f'{path}/{key}'.strip('/')
            if val.get('$path'):
                if EXPECTED.get(name)!=val['$path']:
                    errors.append('unapproved Rojo filesystem mapping: '+name)
                if val.get('$ignoreUnknownInstances') is not True:
                    errors.append('Rojo mapping must preserve unrelated Studio Instances: '+name)
                if not (root/val['$path']).is_dir():errors.append('missing '+val['$path'])
            if val.get('$ignoreUnknownInstances') is not True:
                errors.append('all mapped parent Instances must preserve Studio content: '+name)
            walk(val,name)
    walk(t)
    def collected(tree,path=''):
        found={}
        for k,v in tree.items():
            if k.startswith('$') or not isinstance(v,dict):continue
            name=f'{path}/{k}'.strip('/')
            if '$path' in v:found[name]=v['$path']
            found.update(collected(v,name))
        return found
    if collected(t)!=EXPECTED:errors.append('Rojo managed subtree drift; review before accepting')
    toolpin=(root/'rokit.toml').read_text()
    for expected in ('rojo-rbx/rojo@7.7.0','JohnnyMorganz/StyLua@2.5.2','Kampfkarren/selene@0.31.0'):
        if expected not in toolpin:errors.append('missing or altered reviewed CLI tool pin: '+expected)
    return errors
if __name__=='__main__':
    errors=validate()
    if errors:
        for e in errors:print('FAIL:',e)
        raise SystemExit(1)
    print('PASS: scoped filesystem-first Rojo layout static guard (not a native build)')
