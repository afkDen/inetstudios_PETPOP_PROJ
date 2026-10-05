#!/usr/bin/env python3
import shutil, json
TOOLS={'blender':'Blender technical-art automation','gltf-transform':'glTF inspection/optimization','ffmpeg':'audio/video conversion','node':'skill CLI/runtime','npx':'Agent Skills installer'}
print(json.dumps({k:{'path':shutil.which(k),'purpose':v,'available':bool(shutil.which(k))} for k,v in TOOLS.items()}, indent=2))
