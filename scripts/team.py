#!/usr/bin/env python3
"""Streamlined v8 public CLI for the Roblox team scaffold.

Normal human workflow:
  team.py setup
  team.py idea|update
  team.py status|resume
  team.py approve
  team.py amend (when approved scope needs to move)
  team.py check
  team.py pr

The deeper v7 scripts remain available for migration/advanced maintenance, but
normal work uses one GitHub Issue + one task branch + one implementation PR.
No command here silently merges or publishes a Roblox experience.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from streamlined_task import (  # noqa: E402
    BRANCH,
    RISKS,
    approve_scope_amendment,
    approve_task,
    attest_evidence_scope,
    create_scope_amendment,
    create_task,
    find_changeset,
    find_changesets,
    issue_key,
    load_task,
    set_gates,
    slugify,
    validate_task,
    withdraw_scope_amendment,
)


class TeamError(RuntimeError):
    pass


class TeamWorkspace:
    def __init__(self, root: Path = ROOT):
        self.root = Path(root).resolve()
        policy_path = self.root / "08_TOOLCHAIN/TEAM_POLICY.json"
        if not policy_path.is_file():
            raise TeamError("08_TOOLCHAIN/TEAM_POLICY.json missing")
        self.policy = json.loads(policy_path.read_text(encoding="utf-8"))
        self.main = self.policy.get("canonical_branch", "main")

    def run(self, argv: list[str], *, check: bool = True, capture: bool = True):
        cp = subprocess.run(
            argv,
            cwd=self.root,
            text=True,
            encoding="utf-8",
            stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.PIPE if capture else None,
            check=False,
        )
        if check and cp.returncode:
            cmd = " ".join(argv[:2])
            detail = (cp.stdout or cp.stderr or "").strip()[-1200:]
            raise TeamError(f"{cmd} failed (exit {cp.returncode})" + (f": {detail}" if detail else ""))
        return cp

    def git(self, *args: str, check: bool = True) -> str:
        return self.run(["git", *args], check=check).stdout.strip()

    @staticmethod
    def normalize_remote(value: str) -> str:
        value = value.strip()
        if value.startswith("git@github.com:"):
            value = "https://github.com/" + value.split(":", 1)[1]
        if value.startswith("ssh://git@github.com/"):
            value = "https://github.com/" + value.split("ssh://git@github.com/", 1)[1]
        return value.removesuffix(".git").rstrip("/").lower()

    def require_configured(self) -> None:
        if self.policy.get("template_unconfigured") is not False:
            raise TeamError(
                "this is still the reusable template; prepare a real game checkout first with scripts/prepare_new_game.py"
            )
        if not (self.root / ".git").exists():
            raise TeamError("this checkout has no .git directory; open the prepared/cloned game repository")
        actual = self.git("remote", "get-url", "origin")
        expected = self.policy.get("remote_url", "")
        if self.normalize_remote(actual) != self.normalize_remote(expected):
            raise TeamError("origin does not match 08_TOOLCHAIN/TEAM_POLICY.json")

    def branch(self) -> str:
        return self.git("branch", "--show-current")

    def dirty(self) -> list[str]:
        out = self.git("status", "--porcelain=v1", "--untracked-files=all")
        return out.splitlines() if out else []

    def require_clean(self) -> None:
        dirty = self.dirty()
        if dirty:
            raise TeamError("working tree is dirty; checkpoint/commit intended work first; never auto-stash/reset")

    def fetch(self) -> None:
        self.require_configured()
        self.git("fetch", "--prune", "origin")
        self.git("rev-parse", "--verify", f"origin/{self.main}")

    def sync_main(self) -> None:
        self.require_clean()
        if self.branch() != self.main:
            raise TeamError(f"start new work from clean {self.main}; current branch is {self.branch()}")
        self.fetch()
        self.git("pull", "--ff-only", "origin", self.main)
        if self.git("rev-parse", "HEAD") != self.git("rev-parse", f"origin/{self.main}"):
            raise TeamError("local main diverges from origin/main; reconcile manually before new work")

    def repo_slug(self) -> str:
        return self.policy["remote_url"].removesuffix(".git").split("github.com/")[-1]

    def gh_available(self) -> bool:
        return shutil.which("gh") is not None

    def verify_issue(self, issue: int) -> dict | None:
        if not self.gh_available():
            return None
        cp = self.run(
            ["gh", "issue", "view", str(issue), "--repo", self.repo_slug(), "--json", "number,state,title,assignees"],
            check=False,
        )
        if cp.returncode:
            raise TeamError(f"GitHub Issue #{issue} could not be verified; inspect authentication/repository")
        data = json.loads(cp.stdout)
        if data.get("state") != "OPEN":
            raise TeamError(f"GitHub Issue #{issue} is not OPEN")
        return data

    def create_issue(self, *, title: str, source: Path, owner: str = "", confirmed: bool = False) -> int:
        if not self.gh_available():
            raise TeamError("gh is unavailable; create the Issue manually and rerun with --issue N")
        if not confirmed:
            if not sys.stdin.isatty():
                raise TeamError("creating a remote GitHub Issue requires --confirm-create-issue in non-interactive use")
            answer = input(f'Create GitHub Issue "{title}" in {self.repo_slug()}? [y/N] ').strip().lower()
            if answer not in {"y", "yes"}:
                raise TeamError("remote Issue creation not approved")
        cmd = ["gh", "issue", "create", "--repo", self.repo_slug(), "--title", title, "--body-file", str(source)]
        if owner:
            cmd += ["--assignee", owner]
        cp = self.run(cmd)
        m = re.search(r"/issues/(\d+)", cp.stdout)
        if not m:
            raise TeamError("Issue was created but its number could not be parsed; inspect GitHub before retrying")
        return int(m.group(1))

    def remote_branch_exists(self, branch: str) -> bool:
        return bool(self.git("ls-remote", "--heads", "origin", branch, check=False))

    def local_branch_exists(self, branch: str) -> bool:
        return self.run(["git", "show-ref", "--verify", f"refs/heads/{branch}"], check=False).returncode == 0

    def create_work(self, args, kind: str) -> None:
        self.require_configured()
        source = Path(args.file).expanduser().resolve() if args.file else self._interactive_request_file(kind)
        if not source.is_file() or source.suffix.lower() != ".txt":
            raise TeamError("provide a real .txt request with --file PATH")
        title = (args.title or self._default_title(source, kind)).strip()
        owner = args.owner or ""

        # Reconcile local state before any remote Issue creation. This avoids
        # leaving an accidental/duplicate GitHub Issue behind merely because
        # the checkout was dirty, on the wrong branch, or unable to sync main.
        self.sync_main()

        issue = args.issue
        verified = False
        if issue is None:
            issue = self.create_issue(title=title, source=source, owner=owner, confirmed=args.confirm_create_issue)
            verified = True
            print(f"Created GitHub Issue #{issue}")
        else:
            info = self.verify_issue(issue)
            verified = info is not None
            if info and not args.title:
                title = info.get("title") or title

        slug = args.slug or slugify(title)
        category = args.category
        branch = f"{category}/{issue}-{slug}"
        if find_changesets(issue, self.root):
            raise TeamError(f"{issue_key(issue)} already has a task changeset; use `python scripts/team.py resume --issue {issue}`")

        if self.local_branch_exists(branch) or self.remote_branch_exists(branch):
            raise TeamError(f"task branch already exists: {branch}; resume it instead of creating a duplicate")
        self.git("switch", "-c", branch, f"origin/{self.main}")
        try:
            dst = create_task(
                source=source,
                issue=issue,
                kind=kind,
                title=title,
                slug=slug,
                branch=branch,
                owner=owner,
                risk=args.risk,
                github_verified=verified,
                references=args.reference or [],
                root=self.root,
            )
        except Exception:
            # Branch creation succeeded but no user files should be silently deleted or reset.
            # Leave the branch in place and surface the error for manual inspection.
            raise
        prompt = self.generate_prompt(issue)
        print(f"Created {branch} from latest origin/{self.main}")
        print(f"Task: {dst.relative_to(self.root)}")
        print(f"Raw request SHA-256: {json.loads((dst/'TASK.json').read_text())['request_sha256']}")
        print(f"AI prompt: {prompt.relative_to(self.root)}")
        print("Next: open your approved coding runtime in THIS checkout/branch and paste the generated prompt.")
        print("The AI must design first and stop for human scope approval before substantial implementation.")

    def _interactive_request_file(self, kind: str) -> Path:
        local = self.root / ".local" / "ideas"
        local.mkdir(parents=True, exist_ok=True)
        path = local / f"{kind}-draft.txt"
        if not path.exists():
            path.write_text("", encoding="utf-8")
        if os.name == "nt" and shutil.which("notepad.exe") and sys.stdin.isatty():
            subprocess.run(["notepad.exe", str(path)], cwd=self.root, check=False)
            if path.stat().st_size:
                return path
        editor = os.environ.get("EDITOR")
        if editor and sys.stdin.isatty():
            subprocess.run([editor, str(path)], cwd=self.root, check=False)
            if path.stat().st_size:
                return path
        raise TeamError(f"write your request in {path.relative_to(self.root)} and rerun with --file {path.relative_to(self.root)}")

    @staticmethod
    def _default_title(source: Path, kind: str) -> str:
        try:
            for line in source.read_text(encoding="utf-8-sig", errors="replace").splitlines():
                text = line.strip()
                if text:
                    return ("[IDEA] " if kind == "idea" else "[UPDATE] ") + text[:80]
        except OSError:
            pass
        return ("[IDEA] " if kind == "idea" else "[UPDATE] ") + source.stem.replace("-", " ").title()

    def generate_prompt(self, issue: int) -> Path:
        dst, meta = load_task(issue, self.root)
        local = self.root / ".local" / "prompts"
        local.mkdir(parents=True, exist_ok=True)
        out = local / f"{meta['key']}-{meta['slug']}.txt"
        common = (self.root / "TEAM_TASK_PROMPT.txt").read_text(encoding="utf-8")
        common = common.replace("<ISSUE>", str(issue)).replace("<USER>", meta.get("owner") or "YOUR_GITHUB_USERNAME")
        header = f"""RESUME/WORK THIS EXISTING STREAMLINED V8 TASK.

Issue: #{issue}
Kind: {meta['kind']}
Branch: {meta['branch']}
Changeset: {dst.relative_to(self.root).as_posix()}
Raw request: {(dst/'USER_REQUEST.txt').relative_to(self.root).as_posix()}
Task metadata: {(dst/'TASK.json').relative_to(self.root).as_posix()}
Task plan: {(dst/'TASK.md').relative_to(self.root).as_posix()}
Work state: {(dst/'WORK_STATE.md').relative_to(self.root).as_posix()}
References: {((dst/'REFERENCES.md').relative_to(self.root).as_posix() if (dst/'REFERENCES.md').exists() else 'none')}
Current risk: {meta['risk']}
Scope approval: {meta['scope_approval']['status']}
Active scope revision: {meta.get('scope_revision', 0)}
Approved scope amendments: {', '.join(str(a.get('id')) for a in meta.get('scope_amendments', []) if a.get('status') == 'APPROVED') or 'none'}
Pending scope amendment: {next((str(a.get('id')) for a in meta.get('scope_amendments', []) if a.get('status') == 'DRAFT'), 'none')}

Treat TASK.md plus every APPROVED file under SCOPE_AMENDMENTS/ in revision order as the effective scope. A DRAFT amendment is only a proposal: the current approved scope remains active, but pause work affected by the proposal until it is approved or withdrawn.

Do NOT create another Issue, proposal branch, promotion branch, task branch, or changeset.
Do NOT run the legacy proposal/promotion workflow for this task.

"""
        out.write_text(header + common.rstrip() + "\n", encoding="utf-8")
        return out

    def status(self, *, issue: int | None = None, fetch: bool = True) -> None:
        self.require_configured()
        branch = self.branch()
        dirty = self.dirty()
        print(f"Branch: {branch or '(detached)'}")
        print(f"HEAD: {self.git('rev-parse','--short','HEAD')}")
        print(f"Origin: {self.git('remote','get-url','origin')}")
        print(f"Working tree: {'DIRTY' if dirty else 'CLEAN'}")
        if dirty:
            for line in dirty[:20]: print("  "+line)
            if len(dirty)>20: print(f"  ... {len(dirty)-20} more")
        if fetch:
            try:
                self.fetch()
                counts = self.git("rev-list", "--left-right", "--count", f"HEAD...origin/{self.main}")
                left, right = counts.split()
                print(f"vs origin/{self.main}: {left} commit(s) ahead, {right} behind")
            except TeamError as exc:
                print(f"Remote comparison: UNKNOWN ({exc})")
        if issue is None:
            m = BRANCH.fullmatch(branch)
            if m: issue = int(m.group(1))
        if issue:
            try:
                dst, meta = load_task(issue, self.root)
                print(f"Task: {dst.relative_to(self.root)}")
                print(f"Kind/risk: {meta['kind']} / {meta['risk']}")
                print(f"Scope approval: {meta['scope_approval']['status']}")
                print(f"Active scope revision: {meta.get('scope_revision', 0)}")
                pending=[a for a in meta.get('scope_amendments',[]) if a.get('status')=='DRAFT']
                print(f"Pending scope amendment: {pending[0]['id'] if pending else 'none'}")
                print(f"Studio required: {meta['gates']['studio_required']}")
                print(f"Independent review: {meta['gates']['independent_review_required']}")
                print(f"Prompt: {self.generate_prompt(issue).relative_to(self.root)}")
            except (FileNotFoundError, ValueError) as exc:
                print(f"Task state: UNKNOWN ({exc})")

    def _resolve_actor(self, supplied: str | None, meta: dict, *, purpose: str) -> str:
        actor = supplied or meta.get("owner")
        if not actor and self.gh_available():
            who = self.run(["gh", "api", "user", "--jq", ".login"], check=False)
            if who.returncode == 0:
                actor = who.stdout.strip()
        if not actor:
            raise TeamError(f"{purpose} identity is unknown; pass --by YOUR_GITHUB_USERNAME or set the task owner")
        return actor

    @staticmethod
    def _tri(value):
        if value is None:
            return None
        return value == "yes"

    def approve(self, args) -> None:
        self.require_configured()
        dst, meta = load_task(args.issue, self.root)
        if self.branch() != meta["branch"]:
            raise TeamError(f"approval must be recorded on {meta['branch']}; current branch is {self.branch()}")
        errors = validate_task(args.issue, self.root)
        if errors:
            raise TeamError("task integrity failed: " + "; ".join(errors))
        approver = self._resolve_actor(args.by, meta, purpose="approval")
        gate_args=dict(
            risk=args.risk,
            studio_required=self._tri(args.studio_required),
            independent_review_required=self._tri(args.independent_review),
            full_quality_packet_required=self._tri(args.full_quality_packet),
        )
        if args.amendment is not None:
            path=approve_scope_amendment(
                args.issue,args.amendment,approver,args.note or "",
                evidence_impact=args.evidence_impact,root=self.root,**gate_args
            )
            _,fresh=load_task(args.issue,self.root)
            print(f"Approved scope amendment {args.amendment} for {issue_key(args.issue)}; active scope revision is now {fresh.get('scope_revision')}.")
            print(f"Amendment: {path.relative_to(self.root)}")
            if args.evidence_impact == "refresh-affected":
                print("Existing evidence was preserved but is not current for final delivery until reviewed/refreshed and explicitly attested with `team.py evidence-scope`.")
            print("Only the approved amendment is added to the prior scope; push, merge and Roblox publish remain separately gated.")
        else:
            approve_task(args.issue, approver, args.note or "", root=self.root, **gate_args)
            print(f"Recorded initial human scope approval for {issue_key(args.issue)} in {dst.relative_to(self.root)}")
            print("The feature may now proceed within scope revision 1. Future material scope movement should use `team.py amend`, not silently edit TASK.md.")

    def amend(self, args) -> None:
        self.require_configured()
        dst,meta=load_task(args.issue,self.root)
        if self.branch()!=meta["branch"]:
            raise TeamError(f"scope amendments belong on {meta['branch']}")
        errors=validate_task(args.issue,self.root,require_approved=True)
        if errors:
            raise TeamError("task integrity failed: "+"; ".join(errors))
        actor=self._resolve_actor(args.by,meta,purpose="scope amendment requester")
        path=create_scope_amendment(args.issue,args.reason,actor,args.reference,root=self.root)
        _,fresh=load_task(args.issue,self.root)
        rec=[a for a in fresh.get('scope_amendments',[]) if a.get('status')=='DRAFT'][0]
        print(f"Created DRAFT scope amendment {rec['id']} at {path.relative_to(self.root)}")
        print("The current approved scope remains active. Edit the amendment; pause only affected work; then record explicit human approval with:")
        print(f"  python scripts/team.py approve --issue {args.issue} --amendment {rec['id']} --by YOUR_GITHUB_USERNAME")

    def withdraw_amendment(self,args) -> None:
        self.require_configured()
        dst,meta=load_task(args.issue,self.root)
        if self.branch()!=meta["branch"]:
            raise TeamError(f"scope amendment withdrawal belongs on {meta['branch']}")
        actor=self._resolve_actor(args.by,meta,purpose="withdrawal")
        path=withdraw_scope_amendment(args.issue,args.amendment,actor,args.note,root=self.root)
        print(f"Withdrew scope amendment {args.amendment}: {path.relative_to(self.root)}")
        print("The previously approved scope revision remains unchanged.")

    def evidence_scope(self,args) -> None:
        self.require_configured()
        dst,meta=load_task(args.issue,self.root)
        if self.branch()!=meta["branch"]:
            raise TeamError(f"evidence attestation belongs on {meta['branch']}")
        actor=self._resolve_actor(args.by,meta,purpose="evidence attestation")
        path=attest_evidence_scope(args.issue,actor,args.note,root=self.root)
        print(f"Marked delivery evidence reviewed/current for scope revision {meta.get('scope_revision')}: {path.relative_to(self.root)}")
        print("This attests revision applicability only; it does not fabricate PASS results or replace required review/Studio evidence.")

    def gates(self, args) -> None:
        self.require_configured()
        dst, meta = load_task(args.issue, self.root)
        if self.branch() != meta["branch"]:
            raise TeamError(f"gate changes belong on {meta['branch']}")
        if meta.get("scope_approval", {}).get("status") == "APPROVED":
            raise TeamError("risk/gates are part of the approved scope. Create a scope amendment and approve it with the desired --risk/--studio-required/--independent-review/--full-quality-packet values.")
        set_gates(
            args.issue,
            studio_required=self._tri(args.studio_required),
            independent_review_required=self._tri(args.independent_review),
            full_quality_packet_required=self._tri(args.full_quality_packet),
            risk=args.risk,
            root=self.root,
        )
        print(f"Updated pre-approval risk/gates for {dst.relative_to(self.root)}. Initial human scope approval still controls implementation authorization.")

    def setup(self, args) -> None:
        self.require_configured()
        print("STREAMLINED SETUP")
        print(f"Repository: {self.git('remote','get-url','origin')}")
        print(f"Branch: {self.branch()}")

        # Preflight machine capabilities before any expensive/shared bootstrap work.
        doctor=[sys.executable,"scripts/workstation_doctor.py"]
        if args.install_recommended: doctor.append("--install-recommended")
        if args.install_blender_addon: doctor.append("--install-blender-addon")
        self.run(doctor,check=False,capture=False if (args.install_recommended or args.install_blender_addon) else True)
        doctor_file=self.root/".local/WORKSTATION_DOCTOR.json"
        doctor_data=json.loads(doctor_file.read_text()) if doctor_file.is_file() else {"readiness":{},"fix_plan":[]}
        rd=doctor_data.get("readiness",{})

        if args.initialize_shared_skills:
            if not args.confirm_shared_change:
                raise TeamError("first-time shared skill resolution changes tracked project files; rerun with --confirm-shared-change after review")
            if self.branch() != self.main and not self.branch().startswith("infra/"):
                raise TeamError("shared skill initialization must run on main or a dedicated infra/ branch")
            if not rd.get("SKILL_RESOLUTION_READY"):
                plan="; ".join(doctor_data.get("fix_plan",[])) or "Node/npx or a reviewed skill lock is required"
                raise TeamError("shared skill initialization prerequisites are not ready. "+plan)
            cmd=[sys.executable,"scripts/initialize_project.py","--runtime",args.runtime,"--initialize-global"]
            if args.refresh_external_skills: cmd.append("--refresh-external-skills")
            self.run(cmd, capture=False)

        # Personal/team profile and generated adapters are local/ignored conveniences.
        self.run([sys.executable,"scripts/team_setup.py","--developer",args.developer,"--runtime",args.runtime],check=False,capture=False)
        self.run([sys.executable,"scripts/sync_runtime_adapters.py","--runtime",args.runtime],check=False,capture=False)
        if args.install_tools:
            cmd=[sys.executable,"scripts/bootstrap_dev_tools.py","--install"]
            if args.install_plugin: cmd.append("--install-plugin")
            self.run(cmd,capture=False)

        if args.install_bloxmaps:
            self.run([sys.executable,"scripts/bloxmaps_adapter.py","install","--confirm"],capture=False)
            # Fail early if the pinned checkout exists but its executable prerequisites are still missing.
            self.run([sys.executable,"scripts/bloxmaps_adapter.py","status"],check=False,capture=False)

        # Re-probe after any explicit installation/repair so readiness reflects the final workstation state.
        self.run([sys.executable,"scripts/workstation_doctor.py"],check=False,capture=True)
        tool_cp=self.run([sys.executable,"scripts/bootstrap_dev_tools.py","--check"],check=False)
        repo_cp=self.run([sys.executable,"scripts/validate_repo.py"],check=False)
        model_cp=self.run([sys.executable,"scripts/validate_model_policy.py","--check-config"],check=False)
        lock = self.root/"08_TOOLCHAIN/SKILL_LOCK.json"
        external_ready=lock.is_file()
        doctor_data=json.loads(doctor_file.read_text()) if doctor_file.is_file() else {"readiness":{}}
        rd=doctor_data.get("readiness",{})
        print("\nREADINESS")
        print("Repository contract:","PASS" if repo_cp.returncode==0 else "PENDING")
        print("Shared external skill lock:","PASS" if external_ready else "PENDING (maintainer first-time resolution required before full delegation)")
        print("Model policy config:","PASS" if model_cp.returncode==0 else "PENDING")
        print("Pinned Roblox developer tools:","PASS" if tool_cp.returncode==0 else "PENDING")
        print("GitHub CLI automation:","PASS" if rd.get("GITHUB_CLI_READY") else "PENDING (manual Issue/PR fallback remains available)")
        print("External-skill resolution prerequisites:","PASS" if rd.get("SKILL_RESOLUTION_READY") else "PENDING (Node/npx needed only for first maintainer resolution)")
        print("Graphify repo intelligence:","PASS" if rd.get("GRAPH_READY") else "PENDING (recommended)")
        print("BloxMaps world-generation adapter:","PASS" if rd.get("BLOXMAPS_READY") else "PENDING (priority for procedural world/layout work)")
        print("Blender asset-authoring CLI:","PASS" if rd.get("CREATIVE_CLI_READY") else "PENDING (priority for 3D asset work)")
        print("Blender MCP runtime registration:",rd.get("BLENDER_MCP_RUNTIME_REGISTRATION","PENDING_MANUAL"))
        print("Blender MCP live addon/server:",rd.get("BLENDER_ADDON_LIVE_VERIFICATION","PENDING_MANUAL"))
        print("Roblox Studio MCP/Rojo live connection: DEFERRED until an approved task actually needs Studio")
        print("\nSetup is read-only by default. Review .local/WORKSTATION_FIX_PLAN.txt before any install flags.")
        print("You may capture a game idea/update now; task-specific implementation checks only capabilities the task actually needs.")

    def checkpoint(self, issue: int, note: str) -> None:
        self.require_configured()
        dst, meta = load_task(issue, self.root)
        if self.branch() != meta["branch"]:
            raise TeamError(f"checkpoint belongs on {meta['branch']}; current branch is {self.branch()}")
        if not note.strip():
            raise TeamError("checkpoint note cannot be blank")
        ws = dst / "WORK_STATE.md"
        if not ws.is_file():
            raise TeamError("WORK_STATE.md missing")
        stamp = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
        with ws.open("a", encoding="utf-8") as fh:
            fh.write(f"\n## CHECKPOINT {stamp}\n\n{note.strip()}\n")
        print(f"Checkpointed {dst.relative_to(self.root)}")
        print("This is local task state only; review/commit it with the rest of the issue when appropriate.")

    def check(self, issue: int, *, quick: bool = False) -> None:
        self.require_configured()
        dst, meta = load_task(issue, self.root)
        if self.branch() != meta["branch"]:
            raise TeamError(f"current branch must be {meta['branch']}")
        self.fetch()
        if self.run(["git","merge-base","--is-ancestor",f"origin/{self.main}","HEAD"],check=False).returncode:
            raise TeamError(f"branch is behind/diverged from origin/{self.main}; inspect and explicitly merge accepted upstream")
        errors=validate_task(issue,self.root,require_approved=True,require_delivery=not quick)
        if not quick and not errors:
            if meta["gates"].get("studio_required") is True:
                from validate_studio_delivery import validate_delivery
                errors += validate_delivery(dst/"STUDIO_DELIVERY.json",self.root,expect_issue=issue)
            if meta["gates"].get("full_quality_packet_required") is True:
                from validate_feature_evidence import validate_packet
                errors += validate_packet(dst/"QUALITY_EVIDENCE.json",self.root)
        if errors:
            raise TeamError("task gates failed: " + "; ".join(errors))
        commands=[
            [sys.executable,"scripts/sync_derived_docs.py","--check"],
            [sys.executable,"scripts/validate_model_policy.py","--check-config"],
            [sys.executable,"scripts/validate_repo.py"],
            [sys.executable,"scripts/validate_team.py"],
            [sys.executable,"scripts/validate_rojo_layout.py"],
        ]
        if not quick:
            commands += [
                [sys.executable,"-m","unittest","discover","-s","tests","-v"],
                [sys.executable,"scripts/disposable_pipeline_test.py"],
            ]
        records=[]
        for cmd in commands:
            cp=self.run(cmd,check=False)
            records.append({"command":cmd,"exit_code":cp.returncode,"stdout":cp.stdout[-8000:],"stderr":cp.stderr[-4000:]})
            if cp.returncode:
                raise TeamError(f"check failed: {' '.join(cmd)}\n{(cp.stdout or cp.stderr)[-1200:]}")
        native={"tools":"PENDING","rojo":"PENDING","stylua":"NOT_RUN","selene":"NOT_RUN"}
        if not quick:
            tool=self.run([sys.executable,"scripts/bootstrap_dev_tools.py","--check"],check=False)
            if tool.returncode:
                raise TeamError("pinned Rojo/StyLua/Selene are missing or wrong version; run team.py setup --install-tools only with approval")
            native["tools"]="PASS"
            build=self.root/"build";build.mkdir(exist_ok=True)
            cp=self.run(["rojo","build","default.project.json","--output","build/dev.rbxlx"],check=False)
            if cp.returncode: raise TeamError("native Rojo build failed")
            native["rojo"]="PASS"
            has_luau=any((self.root/"src").rglob("*.luau")) or any((self.root/"src").rglob("*.lua"))
            if has_luau:
                if self.run(["stylua","--check","src"],check=False).returncode: raise TeamError("StyLua check failed")
                if self.run(["selene","src"],check=False).returncode: raise TeamError("Selene check failed")
                native["stylua"]=native["selene"]="PASS"
        logdir=self.root/".local"/"workflow_checks";logdir.mkdir(parents=True,exist_ok=True)
        log=logdir/f"{issue_key(issue)}.json"
        log.write_text(json.dumps({"issue":issue,"branch":meta['branch'],"risk":meta['risk'],"quick":quick,"portable":records,"native":native},indent=2)+"\n",encoding="utf-8")
        print(f"PASS: {'quick' if quick else 'full'} checks for {issue_key(issue)}")
        print(f"Local check log: {log.relative_to(self.root)}")

    def pr(self, args) -> None:
        self.require_configured()
        dst, meta = load_task(args.issue, self.root)
        branch=meta["branch"]
        if self.branch()!=branch: raise TeamError(f"current branch must be {branch}")
        if not args.allow_incomplete:
            self.check(args.issue,quick=False)
        else:
            errors=validate_task(args.issue,self.root,require_approved=False,require_delivery=False)
            if errors: raise TeamError("task integrity failed: "+"; ".join(errors))
        self.require_clean()
        if not self.gh_available(): raise TeamError("gh unavailable; push/open the draft PR manually after approval")
        existing=self.run(["gh","pr","list","--repo",self.repo_slug(),"--head",branch,"--json","number,url,state"],check=False)
        if existing.returncode==0:
            items=json.loads(existing.stdout or "[]")
            if items:
                print(f"Existing PR: {items[0].get('url')} ({items[0].get('state')})")
                return
        bodydir=self.root/".local"/"pr_bodies";bodydir.mkdir(parents=True,exist_ok=True)
        body=bodydir/f"{issue_key(args.issue)}.md"
        body.write_text(
            f"Closes #{args.issue}\n\n"
            f"Task: `{dst.relative_to(self.root).as_posix()}`\n"
            f"Risk: **{meta['risk']}**\n"
            f"Scope approval: **{meta['scope_approval']['status']}** by `{meta['scope_approval'].get('approved_by','')}`\n"
            f"Active scope revision: **{meta.get('scope_revision', 0)}**\n"
            f"Approved scope amendments: **{len([a for a in meta.get('scope_amendments', []) if a.get('status') == 'APPROVED'])}**\n\n"
            "## Review\n"
            "- Verify USER_REQUEST.txt provenance and the effective scope: base TASK.md plus approved SCOPE_AMENDMENTS in revision order.\n"
            "- Confirm no DRAFT scope amendment remains and evidence targets the active scope revision.\n"
            "- Verify relevant CI/native/Studio evidence for this risk tier.\n"
            "- A different human must review substantial work before merge.\n"
            "- This PR does not authorize Roblox Production publishing.\n",
            encoding="utf-8",
        )
        push_cmd=f"git push -u origin {branch}"
        gh_cmd=f"gh pr create --base {self.main} --head {branch} --draft --title ... --body-file {body.relative_to(self.root)}"
        if not args.confirm_publish:
            print("PREVIEW ONLY — no remote action taken.")
            print("Would run:")
            print("  "+push_cmd)
            print("  "+gh_cmd)
            return
        self.git("push","--set-upstream","origin",branch)
        cp=self.run(["gh","pr","create","--repo",self.repo_slug(),"--base",self.main,"--head",branch,"--draft","--title",f"{meta['key']}: {meta['title']}","--body-file",str(body)])
        print(cp.stdout.strip())
        print("Created DRAFT PR. Human review/CI/manual gates still control merge; Roblox publish is always separate.")


def add_task_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--file", help="human-authored .txt request; if omitted, an ignored local draft is prepared")
    p.add_argument("--issue", type=int, help="existing GitHub Issue number; omit to create one with explicit confirmation")
    p.add_argument("--title", help="Issue/task title; defaults from first nonblank request line")
    p.add_argument("--slug", help="branch/changeset slug; defaults from title")
    p.add_argument("--owner", default="", help="primary human owner / GitHub username")
    p.add_argument("--risk", choices=sorted(RISKS), default="STANDARD")
    p.add_argument("--category", choices=["feat","fix","docs"], default="feat")
    p.add_argument("--confirm-create-issue", action="store_true", help="explicitly permit remote Issue creation")
    p.add_argument("--reference", action="append", default=[], help="repeatable URL or local reference file; local files are copied into the issue changeset for team collaboration")


def main() -> int:
    ap=argparse.ArgumentParser(description="Streamlined Roblox team workflow — one Issue, one branch, one PR")
    sub=ap.add_subparsers(dest="command",required=True)

    s=sub.add_parser("setup",help="check/configure this developer without forcing Studio live validation")
    s.add_argument("--developer",required=True)
    s.add_argument("--runtime",default="generic")
    s.add_argument("--install-tools",action="store_true",help="run already-installed Rokit to install pinned project tools")
    s.add_argument("--install-plugin",action="store_true",help="also install matching Rojo Studio plugin; requires --install-tools")
    s.add_argument("--install-recommended",action="store_true",help="explicitly install exact pinned Graphify/MCP-for-Blender CLI capabilities through already-installed uv (preferred) or pipx and run Rokit install")
    s.add_argument("--install-blender-addon",action="store_true",help="also run pinned MCP-for-Blender addon installer; requires --install-recommended")
    s.add_argument("--install-bloxmaps",action="store_true",help="explicitly clone/checkout the pinned afkDen/bloxmaps fork into ignored .local tooling; never vendors it into the game repo")
    s.add_argument("--initialize-shared-skills",action="store_true",help="maintainer-only first shared external-skill resolution")
    s.add_argument("--refresh-external-skills",action="store_true",help="explicitly refresh external skill sources during shared initialization")
    s.add_argument("--confirm-shared-change",action="store_true",help="confirm tracked shared skill/bootstrap files may change")

    d=sub.add_parser("doctor",help="read-only workstation dependency/readiness report; no installs")
    d.add_argument("--json",action="store_true")

    add_task_args(sub.add_parser("idea",help="capture first/new game idea directly into one task branch"))
    add_task_args(sub.add_parser("update",help="capture a recurring update directly into one task branch"))

    st=sub.add_parser("status",help="show current Git/task state")
    st.add_argument("--issue",type=int)
    st.add_argument("--no-fetch",action="store_true")
    r=sub.add_parser("resume",help="show current task and regenerate its ready-to-paste AI prompt")
    r.add_argument("--issue",type=int)
    p=sub.add_parser("prompt",help="regenerate the ready-to-paste prompt for an existing task")
    p.add_argument("--issue",type=int,required=True)

    a=sub.add_parser("approve",help="record initial scope approval or approve a numbered scope amendment")
    a.add_argument("--issue",type=int,required=True)
    a.add_argument("--amendment",type=int,help="approve this DRAFT scope amendment instead of the initial TASK.md scope")
    a.add_argument("--by",help="approver username; defaults to task owner or authenticated gh user")
    a.add_argument("--note",default="")
    a.add_argument("--risk",choices=sorted(RISKS))
    a.add_argument("--studio-required",choices=["yes","no"])
    a.add_argument("--independent-review",choices=["yes","no"])
    a.add_argument("--full-quality-packet",choices=["yes","no"])
    a.add_argument("--evidence-impact",choices=["retain","refresh-affected","reset"],default="refresh-affected",help="for amendments: preserve evidence as current, preserve but require review/refresh (default), or reset task evidence")

    am=sub.add_parser("amend",help="draft a revisioned scope amendment without invalidating the current approved scope")
    am.add_argument("--issue",type=int,required=True)
    am.add_argument("--reason",required=True)
    am.add_argument("--by",help="requester username; defaults to task owner")
    am.add_argument("--reference",action="append",default=[],help="repeatable URL or local file supporting this scope amendment; local files are byte-copied and hashed")

    wa=sub.add_parser("withdraw-amendment",help="explicitly withdraw a DRAFT scope amendment")
    wa.add_argument("--issue",type=int,required=True)
    wa.add_argument("--amendment",type=int,required=True)
    wa.add_argument("--by",help="actor username; defaults to task owner or authenticated gh user")
    wa.add_argument("--note",required=True)

    es=sub.add_parser("evidence-scope",help="attest that preserved/refreshed delivery evidence applies to the current approved scope revision")
    es.add_argument("--issue",type=int,required=True)
    es.add_argument("--by",help="reviewer/operator username; defaults to task owner or authenticated gh user")
    es.add_argument("--note",required=True)

    g=sub.add_parser("gates",help="set risk-proportional task gates during pre-approval design")
    g.add_argument("--issue",type=int,required=True)
    g.add_argument("--risk",choices=sorted(RISKS))
    g.add_argument("--studio-required",choices=["yes","no"])
    g.add_argument("--independent-review",choices=["yes","no"])
    g.add_argument("--full-quality-packet",choices=["yes","no"])

    cp=sub.add_parser("checkpoint",help="append a resumable note to the active issue WORK_STATE")
    cp.add_argument("--issue",type=int,required=True)
    cp.add_argument("--note",required=True)

    c=sub.add_parser("check",help="run risk-aware validation; full by default")
    c.add_argument("--issue",type=int,required=True)
    c.add_argument("--quick",action="store_true")

    pr=sub.add_parser("pr",help="preview or explicitly push/open one draft implementation PR")
    pr.add_argument("--issue",type=int,required=True)
    pr.add_argument("--confirm-publish",action="store_true")
    pr.add_argument("--allow-incomplete",action="store_true",help="publish an explicitly incomplete draft for collaboration")

    args=ap.parse_args()
    if getattr(args,"install_plugin",False) and not getattr(args,"install_tools",False):
        ap.error("--install-plugin requires --install-tools")
    if getattr(args,"install_blender_addon",False) and not getattr(args,"install_recommended",False):
        ap.error("--install-blender-addon requires --install-recommended")
    w=TeamWorkspace()
    try:
        if args.command=="setup":w.setup(args)
        elif args.command=="doctor":
            cmd=[sys.executable,"scripts/workstation_doctor.py"]
            if args.json: cmd.append("--json")
            raise SystemExit(subprocess.run(cmd,cwd=w.root,check=False).returncode)
        elif args.command=="idea":w.create_work(args,"idea")
        elif args.command=="update":w.create_work(args,"update")
        elif args.command=="status":w.status(issue=args.issue,fetch=not args.no_fetch)
        elif args.command=="resume":
            issue=args.issue
            if issue is None:
                m=BRANCH.fullmatch(w.branch())
                if not m: raise TeamError("current branch is not an issue task; pass --issue N")
                issue=int(m.group(1))
            w.status(issue=issue,fetch=True)
            print(f"Next: paste {w.generate_prompt(issue).relative_to(w.root)} into the approved runtime in this checkout.")
        elif args.command=="prompt":print(w.generate_prompt(args.issue).relative_to(w.root))
        elif args.command=="approve":w.approve(args)
        elif args.command=="amend":w.amend(args)
        elif args.command=="withdraw-amendment":w.withdraw_amendment(args)
        elif args.command=="evidence-scope":w.evidence_scope(args)
        elif args.command=="gates":w.gates(args)
        elif args.command=="checkpoint":w.checkpoint(args.issue,args.note)
        elif args.command=="check":w.check(args.issue,quick=args.quick)
        elif args.command=="pr":w.pr(args)
        return 0
    except (TeamError,ValueError,FileNotFoundError,json.JSONDecodeError) as exc:
        ap.exit(2,f"BLOCKED: {exc}\n")

if __name__=="__main__":
    raise SystemExit(main())
