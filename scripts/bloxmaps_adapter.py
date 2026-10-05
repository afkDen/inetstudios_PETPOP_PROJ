#!/usr/bin/env python3
"""Pinned external BloxMaps production adapter.

This keeps FSL-licensed BloxMaps source in an ignored isolated checkout while
providing the reusable Roblox bootstrap a stable, model-neutral interface for
world generation and smoke validation.

Default commands are read-only. `install --confirm` is the only command here
that clones/changes the external checkout.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFG_PATH = ROOT / "08_TOOLCHAIN" / "BLOXMAPS_INTEGRATION.json"
CFG = json.loads(CFG_PATH.read_text(encoding="utf-8"))
CHECKOUT = ROOT / CFG["checkout"]["default_path"]
REPO = CFG["fork"]["repository"]
REF = CFG["fork"]["ref"]
REMOTE = f"https://github.com/{REPO}.git"
LOCAL = ROOT / ".local" / "bloxmaps"
ALLOWED_OUTPUT_ROOTS = tuple((ROOT / p).resolve() for p in CFG.get("security", {}).get(
    "allowed_plan_output_roots", [".local/bloxmaps", "04_CHANGESETS"]
))


def run(argv, *, cwd=None, env=None, capture=True, timeout=120):
    try:
        return subprocess.run(
            [str(x) for x in argv], cwd=str(cwd or ROOT), env=env, text=True,
            encoding="utf-8", stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.PIPE if capture else None, check=False, timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        class Result:
            returncode = 127
            stdout = ""
            stderr = str(exc)
        return Result()


def git(*args, cwd=None):
    return run(["git", *args], cwd=cwd or CHECKOUT)


def _norm_remote(v: str) -> str:
    v = (v or "").strip().lower().removesuffix(".git").rstrip("/")
    if v.startswith("git@github.com:"):
        v = "https://github.com/" + v.split(":", 1)[1]
    return v


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def resolve_output_path(raw: str) -> Path:
    """Resolve a generated-plan path without granting arbitrary filesystem writes."""
    out = Path(raw).expanduser()
    if not out.is_absolute():
        out = ROOT / out
    out = out.resolve()
    if not any(_is_within(out, allowed) for allowed in ALLOWED_OUTPUT_ROOTS):
        allowed = ", ".join(str(p.relative_to(ROOT)) for p in ALLOWED_OUTPUT_ROOTS)
        raise ValueError(f"output must stay under an approved root: {allowed}")
    return out


def status() -> dict:
    result = {
        "schema_version": 1,
        "repository": REPO,
        "expected_ref": REF,
        "checkout": str(CHECKOUT.relative_to(ROOT)),
        "license": CFG["license"],
        "installed": False,
        "clean": None,
        "remote_ok": False,
        "ref_ok": False,
        "python_ok": sys.version_info >= (3, 11),
        "luau": shutil.which("luau") or shutil.which("luau.exe"),
        "lune": shutil.which("lune") or shutil.which("lune.exe"),
        "mapgen_ready": False,
        "issues": [],
    }
    if not CHECKOUT.is_dir() or not (CHECKOUT / ".git").exists():
        result["issues"].append("isolated BloxMaps checkout missing")
        return result
    result["installed"] = True
    head = git("rev-parse", "HEAD")
    origin = git("remote", "get-url", "origin")
    dirty = git("status", "--porcelain=v1", "--untracked-files=all")
    result["head"] = (head.stdout or "").strip()
    result["origin"] = (origin.stdout or "").strip()
    result["clean"] = dirty.returncode == 0 and not (dirty.stdout or "").strip()
    result["remote_ok"] = origin.returncode == 0 and _norm_remote(result["origin"]) == _norm_remote(REMOTE)
    result["ref_ok"] = head.returncode == 0 and result["head"] == REF
    result["mapgen_ready"] = bool(
        result["python_ok"] and result["luau"] and result["remote_ok"] and result["ref_ok"] and result["clean"]
        and (CHECKOUT / "tools" / "mapgen.py").is_file()
        and (CHECKOUT / "src" / "MapGen" / "init.luau").is_file()
    )
    if not result["remote_ok"]: result["issues"].append("checkout origin does not match pinned fork")
    if not result["ref_ok"]: result["issues"].append("checkout HEAD is not the pinned reviewed ref")
    if not result["clean"]: result["issues"].append("checkout is dirty; do not auto-upgrade/reset it")
    if not result["python_ok"]: result["issues"].append("BloxMaps local tools require Python >=3.11")
    if not result["luau"]: result["issues"].append("Luau CLI not found; local MapGen cannot execute")
    return result


def install(confirm: bool) -> int:
    if not confirm:
        raise SystemExit("BLOCKED: external FSL checkout creation requires `install --confirm`")
    if CHECKOUT.exists():
        s = status()
        if s["installed"] and s["remote_ok"] and s["ref_ok"] and s["clean"]:
            print("BloxMaps checkout already pinned correctly; no change made.")
            return 0
        if s["installed"] and s["remote_ok"] and s["ref_ok"] and not s["clean"]:
            raise SystemExit(f"BLOCKED: {CHECKOUT} is pinned but dirty; inspect/reconcile local changes manually")
        raise SystemExit(f"BLOCKED: {CHECKOUT} already exists but does not match the reviewed pin; inspect it manually")
    CHECKOUT.parent.mkdir(parents=True, exist_ok=True)
    cp = run(["git", "clone", "--no-checkout", REMOTE, str(CHECKOUT)], capture=False, timeout=300)
    if cp.returncode:
        raise SystemExit("BLOCKED: git clone of the approved BloxMaps fork failed")
    cp = git("checkout", "--detach", REF)
    if cp.returncode:
        raise SystemExit("BLOCKED: cloned fork but could not checkout pinned ref")
    cp = git("config", "advice.detachedHead", "false")
    s = status()
    if not s["remote_ok"] or not s["ref_ok"]:
        raise SystemExit("BLOCKED: post-install verification failed")
    print(f"Installed pinned BloxMaps checkout at {CHECKOUT.relative_to(ROOT)}")
    print(f"Ref: {REF}")
    print("No BloxMaps source was copied into the tracked game repository.")
    return 0


def smoke(prompt: str, seed: int) -> int:
    s = status()
    LOCAL.mkdir(parents=True, exist_ok=True)
    report = LOCAL / "SMOKE.json"
    if not s["mapgen_ready"]:
        report.write_text(json.dumps({"status":"BLOCKED","readiness":s}, indent=2)+"\n", encoding="utf-8")
        print(json.dumps({"status":"BLOCKED","readiness":s}, indent=2))
        return 2
    out = LOCAL / "smoke-plan.json"
    env = dict(os.environ)
    env["BLOX_NO_OVERLAY"] = "1"
    cp = run([
        sys.executable, "tools/mapgen.py", "generate", prompt,
        "--seed", str(seed), "--no-library", "--out", str(out)
    ], cwd=CHECKOUT, env=env, timeout=180)
    ok = cp.returncode == 0 and out.is_file()
    plan_meta = None
    if ok:
        try:
            plan = json.loads(out.read_text(encoding="utf-8"))
            plan_meta = plan.get("meta") or {}
            ok = bool(plan_meta.get("seed") == seed and plan.get("terrain") is not None)
        except (OSError, ValueError, TypeError):
            ok = False
    payload = {
        "status": "PASS" if ok else "FAIL",
        "fork_ref": REF,
        "prompt": prompt,
        "seed": seed,
        "plan": str(out.relative_to(ROOT)) if out.exists() else None,
        "meta": plan_meta,
        "stdout_tail": (cp.stdout or "")[-3000:],
        "stderr_tail": (cp.stderr or "")[-3000:],
    }
    report.write_text(json.dumps(payload, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if ok else 1


def generate(args) -> int:
    s = status()
    if not s["mapgen_ready"]:
        raise SystemExit("BLOCKED: BloxMaps MapGen is not ready; run status/doctor and fix prerequisites")
    try:
        out = resolve_output_path(args.out)
    except ValueError as exc:
        raise SystemExit(f"BLOCKED: {exc}") from exc
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd=[sys.executable,"tools/mapgen.py","generate",args.prompt,"--seed",str(args.seed),"--out",str(out)]
    if args.no_library: cmd.append("--no-library")
    for flag in ("size","time","genre","theme","layout"):
        value=getattr(args,flag)
        if value: cmd += ["--"+flag,value]
    env=dict(os.environ); env["BLOX_NO_OVERLAY"]="1"
    if args.assets:
        env["BLOXMAP_ASSETS"] = str(Path(args.assets).expanduser().resolve())
    cp=run(cmd,cwd=CHECKOUT,env=env,timeout=240)
    if cp.returncode:
        sys.stderr.write((cp.stdout or "")[-4000:] + (cp.stderr or "")[-4000:])
        return cp.returncode
    print(cp.stdout.strip())
    print(f"Plan: {out}")
    return 0


def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest="command",required=True)
    s=sub.add_parser("status"); s.add_argument("--json",action="store_true")
    i=sub.add_parser("install"); i.add_argument("--confirm",action="store_true")
    sm=sub.add_parser("smoke"); sm.add_argument("--prompt",default="small spooky village with one central plaza"); sm.add_argument("--seed",type=int,default=1337)
    g=sub.add_parser("generate"); g.add_argument("prompt"); g.add_argument("--seed",type=int,required=True); g.add_argument("--out",required=True); g.add_argument("--assets"); g.add_argument("--no-library",action="store_true");
    g.add_argument("--size",choices=["small","medium","large","huge"]); g.add_argument("--time",choices=["day","sunset","dawn","night"]); g.add_argument("--genre"); g.add_argument("--theme"); g.add_argument("--layout")
    a=ap.parse_args()
    if a.command=="status":
        d=status(); print(json.dumps(d,indent=2) if a.json else "\n".join([f"BloxMaps: {'READY' if d['mapgen_ready'] else 'PENDING'}",f"Checkout: {d['checkout']}",f"Fork/ref: {d['repository']}@{d['expected_ref']}",*(f"- {x}" for x in d['issues'])])); return 0 if d['mapgen_ready'] else 2
    if a.command=="install": return install(a.confirm)
    if a.command=="smoke": return smoke(a.prompt,a.seed)
    if a.command=="generate": return generate(a)
    return 2

if __name__=="__main__":
    raise SystemExit(main())
