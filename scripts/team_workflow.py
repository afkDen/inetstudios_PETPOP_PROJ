#!/usr/bin/env python3
"""Safe local Git handoffs for the model-neutral Roblox team workflow.

This program NEVER silently pushes, opens PRs, merges, rewrites local edits, or
publishes to Roblox. The calling AI is responsible for the full design/review
lifecycle; this utility enforces Git and raw-input boundaries only.
"""
from __future__ import annotations
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ISSUE_BRANCH = re.compile(r"^(?:feat|fix|docs)/([1-9]\d{0,5})-[a-z0-9]+(?:-[a-z0-9]+)*$")

class WorkflowError(RuntimeError):
    pass

class Workspace:
    def __init__(self, root: Path = ROOT):
        self.root = Path(root).resolve()
        self.policy = json.loads((self.root/'08_TOOLCHAIN/TEAM_POLICY.json').read_text())
        self.main = self.policy['canonical_branch']

    def run(self, argv: list[str], *, check=True):
        result = subprocess.run(argv, cwd=self.root, text=True, encoding='utf-8',
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if check and result.returncode:
            # Suppress auth/token-bearing subprocess stderr in public CI logs.
            raise WorkflowError(f"{argv[0]} {argv[1] if len(argv)>1 else ''} failed (exit {result.returncode}); inspect locally")
        return result

    def git(self, *args: str, check=True) -> str:
        return self.run(['git', *args], check=check).stdout.strip()

    def remote(self):
        return self.git('remote', 'get-url', 'origin')

    def verify_remote(self):
        if self.policy.get('template_unconfigured') is not False:
            raise WorkflowError('unconfigured bootstrap template: prepare a new game repository first')
        expected = self.policy['remote_url']
        actual = self.remote()
        def norm(u):
            u = u.strip()
            if u.startswith('git@github.com:'):
                u = 'https://github.com/' + u.split(':', 1)[1]
            if u.startswith('ssh://git@github.com/'):
                u = 'https://github.com/' + u.split('ssh://git@github.com/', 1)[1]
            return u.removesuffix('.git').rstrip('/').lower()
        if norm(actual) != norm(expected):
            raise WorkflowError('origin does not match TEAM_POLICY.json; inspect the repository and resolve manually')

    def branch(self):
        return self.git('branch', '--show-current')

    def require_clean(self):
        if self.git('status', '--porcelain=v1', '--untracked-files=all'):
            raise WorkflowError('working tree is dirty; checkpoint/commit your work first; never auto-stash/reset')

    def fetch(self):
        self.verify_remote()
        self.git('fetch', '--prune', 'origin')
        self.git('rev-parse', '--verify', f'origin/{self.main}')

    def sync(self):
        self.require_clean()
        current = self.branch()
        self.fetch()
        if current != self.main:
            print(f'Fetched origin/{self.main}; stayed on {current}. Review upstream changes before integrating.')
            print(f'To update this task branch explicitly: git merge origin/{self.main}  (then rerun tests)')
            return
        self.git('pull', '--ff-only', 'origin', self.main)
        if self.git('rev-parse', 'HEAD') != self.git('rev-parse', f'origin/{self.main}'):
            raise WorkflowError('local main contains unpublished commits; do not base new work on a divergent main')
        print(f'Synchronized main at {self.git("rev-parse", "--short", "HEAD")}')

    def start(self, *, kind: str, issue: int, proposal: str, slug: str, category: str = 'feat'):
        if not 1 <= issue <= 999999 or not SLUG.fullmatch(slug):
            raise WorkflowError('invalid issue or slug')
        if category not in {'feat', 'fix', 'docs'}:
            raise WorkflowError('invalid branch category')
        self.require_clean()
        if self.branch() != self.main:
            raise WorkflowError('start from clean main; preserve your current task branch (or use a separate worktree)')
        # Never switch branches until fetching and proposal verification succeed.
        self.sync()
        rel = Path(proposal)
        if rel.is_absolute() or '..' in rel.parts or rel.suffix != '.txt':
            raise WorkflowError('proposal must be a repository-relative .txt path')
        folder = 'IDEAS' if kind == 'idea' else 'UPDATES'
        expected = (self.root/'00_INPUT/PROPOSALS'/folder).resolve()
        src = self.root/rel
        if not src.is_file() or src.is_symlink() or src.resolve().parent != expected:
            raise WorkflowError('proposal must already be an accepted, synced file on main')
        if not src.name.startswith(f'GH-{issue:06d}_'):
            raise WorkflowError('proposal issue does not match assigned issue')
        sys.path.insert(0, str(self.root/'scripts'))
        from validate_team import check_proposal
        errors = check_proposal(src, self.root)
        if errors:
            raise WorkflowError('proposal integrity failed: ' + '; '.join(errors))
        # Being present on main proves proposal PR integration, NOT scope approval.
        # Human must confirm issue approval and ownership before using start.
        branch = f'{category}/{issue}-{slug}'
        if self.git('show-ref', '--verify', f'refs/heads/{branch}', check=False) or self.git('ls-remote', '--heads', 'origin', branch):
            raise WorkflowError(f'branch already exists: {branch}; resume its original workspace instead')
        self.git('switch', '-c', branch, f'origin/{self.main}')
        self.run([sys.executable, str(self.root/'scripts/intake_request.py'), '--proposal', rel.as_posix(), '--issue', str(issue)])
        print(f'Created {branch} from latest origin/{self.main}; changeset is local and UNCOMMITTED.')
        print('Read canonical game idea if present. Perform full skills/subagents/review lifecycle on this branch.')
        print('Approval and branch ownership must be verified against the GitHub Issue by a human/authorized GitHub tool.')
        return branch

    def propose(self, *, kind: str, issue: int, by: str, source: str, slug: str):
        if not 1 <= issue <= 999999 or not SLUG.fullmatch(slug):
            raise WorkflowError('invalid issue or slug')
        self.require_clean()
        if self.branch() != self.main:
            raise WorkflowError('propose from clean main; preserve active task branches')
        # Keep source in ignored .local/ or outside repository to avoid dirty preflight.
        src = Path(source).expanduser().resolve()
        if not src.is_file() or src.suffix.lower() != '.txt':
            raise WorkflowError('source must be an existing .txt file')
        self.sync()
        branch = f'proposal/{issue}-{slug}'
        if self.git('show-ref', '--verify', f'refs/heads/{branch}', check=False) or self.git('ls-remote', '--heads', 'origin', branch):
            raise WorkflowError(f'proposal branch already exists: {branch}')
        self.git('switch', '-c', branch, f'origin/{self.main}')
        sys.path.insert(0, str(self.root/'scripts'))
        from submit_proposal import add_proposal
        path = add_proposal(src, issue, by, kind, self.root)
        print(f'Created {path.relative_to(self.root)}. Commit and submit proposal PR for approval.')
        print('STOP: no implementation until proposal is merged and issue scope is human-approved.')

    def preflight(self, *, issue: int, run_tests=False, quality_required=True):
        branch = self.branch()
        m = ISSUE_BRANCH.fullmatch(branch)
        if not m or int(m.group(1)) != issue:
            raise WorkflowError('current branch must match the assigned implementation issue')
        self.fetch()
        if self.run(['git','merge-base','--is-ancestor', f'origin/{self.main}', 'HEAD'], check=False).returncode:
            raise WorkflowError('branch is behind or diverged from origin/main; merge current main explicitly, resolve conflicts and retest')
        if run_tests:
            cmds = [
                [sys.executable, 'scripts/sync_derived_docs.py', '--check'],
                [sys.executable, 'scripts/validate_repo.py'],
                [sys.executable, 'scripts/validate_team.py'],
                [sys.executable, 'scripts/validate_rojo_layout.py'],
                [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests'],
                [sys.executable, 'scripts/disposable_pipeline_test.py'],
            ]
            if quality_required:
                cmds.append([sys.executable, 'scripts/validate_feature_evidence.py', '--compare', f'origin/{self.main}'])
            records=[]
            for cmd in cmds:
                result=self.run(cmd)
                records.append({'command':cmd,'exit_code':result.returncode,'stdout':result.stdout[-10000:],'stderr':result.stderr[-10000:]})
            logdir=self.root/'.local/workflow_checks'
            logdir.mkdir(parents=True,exist_ok=True)
            logpath=logdir/f'GH-{issue:06d}.json'
            logpath.write_text(json.dumps({'issue':issue,'base_main':self.git('rev-parse',f'origin/{self.main}'),'branch':branch,'portable_checks':records,'native_rojo_build':'NOT_RUN_BY_THIS_SCRIPT','studio_test':'NOT_RUN_BY_THIS_SCRIPT','independent_review':'NOT_RUN_BY_THIS_SCRIPT','feature_evidence':'STRUCTURAL_CHECKED' if quality_required else 'PENDING_DRAFT_PR_ONLY'},indent=2)+'\n')
            print(f'Portable checks passed. Local-only evidence: {logpath.relative_to(self.root)}. Independent AI review, native Rojo and Studio tests require separate evidence.')
        print(f'Preflight complete for {branch}. Do not infer human approval or live Studio PASS.')

    def publish(self, issue: int, confirm: bool):
        if not confirm:
            print('PREVIEW ONLY: with explicit approval, push task branch and create DRAFT PR; no action taken.')
            return
        self.require_clean()
        # Draft PR can request teammate/Studio operator assistance while evidence is pending.
        # CI and human integrator still block non-draft merge until full evidence arrives.
        self.preflight(issue=issue, run_tests=True, quality_required=False)
        if shutil.which('gh') is None:
            raise WorkflowError('GitHub CLI unavailable: install/authenticate gh or create the PR manually')
        branch = self.branch()
        self.git('push', '--set-upstream', 'origin', branch)
        self.run(['gh', 'pr', 'create', '--base', self.main, '--head', branch,
                  '--draft', '--title', f'GH-{issue:06d}: {branch.split("-",1)[-1]}',
                  '--body', f'Refs #{issue}\n\nReview against TEAM_PROTOCOL.md and .github/PULL_REQUEST_TEMPLATE.md.\n'
                            'Human scope approval, test evidence and independent reviewer must be attached before ready.'])
        print('Created DRAFT PR; gameplay/visual Studio evidence remains mandatory before CI can pass and any human-authorized merge.')

    def next_task(self, *, after_pr: int, issue: int, kind: str, proposal: str, slug: str, category: str='feat'):
        """Start another assigned task only after prior PR is actually merged."""
        self.require_clean()
        self.verify_remote()
        if shutil.which('gh') is None:
            raise WorkflowError('cannot verify prior PR merge: gh unavailable; inspect GitHub and switch to main manually')
        repo = self.policy['remote_url'].removesuffix('.git').split('github.com/')[-1]
        p = json.loads(self.run(['gh','pr','view',str(after_pr),'--repo',repo,
                                 '--json','state,mergedAt,baseRefName,headRefName']).stdout)
        if p.get('state') != 'MERGED' or not p.get('mergedAt') or p.get('baseRefName') != self.main:
            raise WorkflowError('previous PR is not verified as merged into the canonical main')
        if self.branch() not in (self.main, p.get('headRefName')):
            raise WorkflowError('current task branch does not match previous merged PR; preserve its work before switching')
        self.git('switch',self.main)
        return self.start(kind=kind,issue=issue,proposal=proposal,slug=slug,category=category)

    def merge(self, issue: int, pr: int, *, confirm: bool):
        # A headless agent may inspect but never use this command to simulate consent.
        if shutil.which('gh') is None:
            raise WorkflowError('GitHub CLI unavailable; inspect/merge in GitHub UI after approval')
        self.verify_remote()
        repo = self.policy['remote_url'].removesuffix('.git').split('github.com/')[-1]
        out = self.run(['gh','pr','view',str(pr),'--repo',repo,
                        '--json','number,author,body,headRefName,baseRefName,headRefOid,isDraft,reviewDecision,mergeStateStatus,statusCheckRollup,state,reviews'])
        p = json.loads(out.stdout)
        if p.get('number') != pr or not ISSUE_BRANCH.fullmatch(p.get('headRefName', '')) or int(ISSUE_BRANCH.fullmatch(p['headRefName']).group(1)) != issue or not re.search(rf'(?:Refs|Closes|Fixes)\s+#{issue}\b', p.get('body') or '', re.I):
            raise WorkflowError('PR issue/branch/body must match the requested issue')
        if p['state'] != 'OPEN' or p['baseRefName'] != self.main or p['isDraft']:
            raise WorkflowError('PR must be open, non-draft, and target the canonical main')
        reviews = p.get('reviews', [])
        author = (p.get('author') or {}).get('login', '')
        external = [r for r in reviews if r.get('state') == 'APPROVED'
                    and (r.get('author') or {}).get('login') not in {author,''}
                    and not (r.get('author') or {}).get('login', '').endswith('[bot]')]
        if p.get('reviewDecision') != 'APPROVED' or not external:
            raise WorkflowError('requires a recorded approval from another human on GitHub')
        checks = p.get('statusCheckRollup') or []
        if not checks or any(c.get('conclusion', c.get('state')) not in {'SUCCESS','NEUTRAL','SKIPPED'} for c in checks):
            raise WorkflowError('required checks must be reported and passing')
        if p.get('mergeStateStatus') != 'CLEAN':
            raise WorkflowError('PR is not cleanly mergeable; inspect GitHub review/branch status')
        print(f'PR #{pr} passes visible GitHub review/check preflight; manual Studio gates may still be required.')
        if not confirm:
            print('PREVIEW ONLY. Human integrator must explicitly authorize merge after Studio/integration evidence.')
            return
        if not sys.stdin.isatty():
            raise WorkflowError('non-interactive merge refused; authorized human must merge via GitHub UI')
        username=self.run(['gh','api','user','--jq','.login']).stdout.strip()
        if username not in self.policy.get('human_integrators', []):
            raise WorkflowError('authenticated GitHub user is not an authorized integrator in TEAM_POLICY.json')
        phrase = f'MERGE PR #{pr} INTO {self.main}'
        if input(f'Type exactly "{phrase}" after verifying Studio/manual checks: ').strip() != phrase:
            raise WorkflowError('human merge confirmation not received')
        self.run(['gh','pr','merge',str(pr),'--repo',repo,
                  '--squash','--delete-branch','--match-head-commit',p['headRefOid']])
        print('Merge requested. Fetch main and inspect actual state; integration owner updates canonical docs and release gates.')


def main():
    ap=argparse.ArgumentParser(description='Git-first, approval-gated team handoffs; read AGENTS.md and TEAM_PROTOCOL.md first')
    sub=ap.add_subparsers(dest='command',required=True)
    sub.add_parser('sync',help='fetch remote; fast-forward clean main, never discard feature changes')
    p=sub.add_parser('propose',help='create a new immutable idea/update proposal branch');p.add_argument('--kind',choices=['idea','update'],required=True);p.add_argument('--issue',type=int,required=True);p.add_argument('--by',required=True);p.add_argument('--source',required=True);p.add_argument('--slug',required=True)
    s=sub.add_parser('start',help='start an approved proposal/issue from latest clean main');s.add_argument('--kind',choices=['idea','update'],required=True);s.add_argument('--issue',type=int,required=True);s.add_argument('--proposal',required=True);s.add_argument('--slug',required=True);s.add_argument('--category',choices=['feat','fix','docs'],default='feat')
    f=sub.add_parser('check',help='check current issue branch against main');f.add_argument('--issue',type=int,required=True);f.add_argument('--test',action='store_true')
    p=sub.add_parser('pr',help='preview or explicitly publish draft PR');p.add_argument('--issue',type=int,required=True);p.add_argument('--confirm-publish',action='store_true')
    m=sub.add_parser('merge',help='preview PR merge eligibility; actual merge requires interactive human');m.add_argument('--issue',type=int,required=True);m.add_argument('--pr',type=int,required=True);m.add_argument('--confirm-merge',action='store_true')
    n=sub.add_parser('next',help='after a verified merged PR, sync main and create an assigned next issue branch');n.add_argument('--after-pr',type=int,required=True);n.add_argument('--kind',choices=['idea','update'],required=True);n.add_argument('--issue',type=int,required=True);n.add_argument('--proposal',required=True);n.add_argument('--slug',required=True);n.add_argument('--category',choices=['feat','fix','docs'],default='feat')
    args=ap.parse_args(); w=Workspace()
    try:
        if args.command=='sync':w.sync()
        elif args.command=='propose':w.propose(kind=args.kind,issue=args.issue,by=args.by,source=args.source,slug=args.slug)
        elif args.command=='start':w.start(kind=args.kind,issue=args.issue,proposal=args.proposal,slug=args.slug,category=args.category)
        elif args.command=='check':w.preflight(issue=args.issue,run_tests=args.test)
        elif args.command=='pr':w.publish(issue=args.issue,confirm=args.confirm_publish)
        elif args.command=='merge':w.merge(issue=args.issue,pr=args.pr,confirm=args.confirm_merge)
        elif args.command=='next':w.next_task(after_pr=args.after_pr,issue=args.issue,kind=args.kind,proposal=args.proposal,slug=args.slug,category=args.category)
    except (WorkflowError, ValueError, FileNotFoundError) as e:
        ap.exit(2, f'BLOCKED: {e}\n')

if __name__=='__main__':main()
