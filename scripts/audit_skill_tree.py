\
#!/usr/bin/env python3
"""Conservative static pre-filter for third-party Agent Skills. Not a security proof."""
import argparse, json, re
from pathlib import Path
RISK_PATTERNS={
 'network': re.compile(r'\b(curl|wget|requests\.|urllib\.|fetch\(|axios\.|Invoke-WebRequest)\b',re.I),
 'process': re.compile(r'\b(subprocess|os\.system|child_process|exec\(|spawn\(|powershell|cmd\.exe|bash\s+-c)\b',re.I),
 'secrets': re.compile(r'\b(\.ssh|\.aws|credentials|token|api[_-]?key|password|cookie|secret)\b',re.I),
 'destructive': re.compile(r'\b(rm\s+-rf|Remove-Item\s+.*-Recurse|shutil\.rmtree|unlink\(|rmdir\()\b',re.I),
 'lifecycle': re.compile(r'\b(preinstall|postinstall|prepare|pretest|posttest)\b',re.I),
}
TEXT_EXT={'.md','.txt','.py','.js','.ts','.json','.yaml','.yml','.toml','.sh','.ps1','.bat','.cmd','.lua','.luau'}

def audit(root: Path):
 root=root.resolve()
 project_root=Path(__file__).resolve().parents[1]
 findings=[]; files=0
 for p in root.rglob('*'):
  if not p.is_file() or p.suffix.lower() not in TEXT_EXT: continue
  files+=1
  try: text=p.read_text(encoding='utf-8',errors='ignore')
  except Exception: continue
  for name,rx in RISK_PATTERNS.items():
   for m in list(rx.finditer(text))[:20]:
    line=text.count('\n',0,m.start())+1
    findings.append({'risk':name,'path':str(p.relative_to(root)),'line':line,'match':m.group(0)[:120]})
 counts={k:sum(1 for f in findings if f['risk']==k) for k in RISK_PATTERNS}
 display_root=root.relative_to(project_root).as_posix() if root.is_relative_to(project_root) else str(root)
 return {'root':display_root,'skill_files':sum(1 for _ in root.rglob('SKILL.md')),'scanned_text_files':files,'finding_counts':counts,'findings':findings,'verdict':'SEMANTIC_REVIEW_REQUIRED' if findings else 'NO_STATIC_RED_FLAGS_FOUND'}

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('path'); ap.add_argument('--output'); args=ap.parse_args(); result=audit(Path(args.path))
 out=json.dumps(result,indent=2)+'\n'
 if args.output: Path(args.output).write_text(out,encoding='utf-8')
 else: print(out,end='')
if __name__=='__main__': main()
