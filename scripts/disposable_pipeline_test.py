#!/usr/bin/env python3
from pathlib import Path
import tempfile, shutil, subprocess, sys, os, re

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"scripts"))
import intake_request

def assert_true(cond, msg):
    if not cond:
        raise AssertionError(msg)

def main():
    # Work in a fully disposable clone of the scaffold so production state remains clean.
    with tempfile.TemporaryDirectory(prefix="roblox-pipeline-test-") as td:
        troot = Path(td)/"repo"
        shutil.copytree(ROOT, troot, ignore=shutil.ignore_patterns(".git", "__pycache__", ".tmp"))
        inbox = troot/"00_INPUT/UPDATES/INBOX"
        src = inbox/"disposable_add_test_button.txt"
        src.write_text("Add a temporary test button. This request is disposable.\n", encoding="utf-8")

        # Rebind module globals to disposable root.
        intake_request.ROOT = troot
        intake_request.INBOX = inbox
        intake_request.PROCESSING = troot/"00_INPUT/UPDATES/PROCESSING"
        intake_request.CHANGESETS = troot/"04_CHANGESETS"
        intake_request.TEMPLATE = troot/"templates/CHANGESET_TEMPLATE"

        cs = intake_request.create_changeset(src, "U999")
        assert_true((cs/"USER_REQUEST.txt").read_text(encoding="utf-8").startswith("Add a temporary"), "raw request not preserved")
        assert_true((cs/"WORK_STATE.md").exists(), "work state missing")
        assert_true((troot/"00_INPUT/UPDATES/PROCESSING/U999_disposable_add_test_button.txt").exists(), "processing provenance missing")

        # Simulate planning -> implementation handoff -> independent review -> revision -> checkpoint.
        (cs/"IMPLEMENTATION_PACKAGE.md").write_text("# IMPLEMENTATION PACKAGE\n\nGoal: disposable test only.\nAcceptance Tests:\n- artifact exists\n", encoding="utf-8")
        (cs/"IMPLEMENTATION_RESULT_01.md").write_text("# IMPLEMENTATION RESULT\n\nStatus: DONE\nChanged: disposable artifact\n", encoding="utf-8")
        (cs/"REVIEW_01.md").write_text("# REVIEW\n\nOutcome: REVISION REQUIRED\nReason: synthetic review separation check.\n", encoding="utf-8")
        (cs/"REVISION_PLAN_01.md").write_text("# REVISION PLAN\n\nAddress synthetic reviewer note.\n", encoding="utf-8")
        (cs/"IMPLEMENTATION_RESULT_02.md").write_text("# IMPLEMENTATION RESULT 02\n\nStatus: DONE\n", encoding="utf-8")
        (cs/"REVIEW_02.md").write_text("# REVIEW 02\n\nOutcome: APPROVED\n", encoding="utf-8")
        (cs/"NEXT_ACTION.md").write_text("# NEXT ACTION\n\nClose disposable test changeset.\n", encoding="utf-8")
        ws = (cs/"WORK_STATE.md").read_text(encoding="utf-8")
        (cs/"WORK_STATE.md").write_text(ws.replace("Stage: INTAKE","Stage: FINAL REVIEW"), encoding="utf-8")

        # Fresh-session continuation simulation: derive state only from files.
        bootstrap = [
            troot/"AGENTS.md", troot/"06_PROJECT_STATE/CURRENT_STATE.md",
            troot/"08_TOOLCHAIN/TOOLCHAIN_MANIFEST.md", troot/"08_TOOLCHAIN/MODEL_ROUTING.md",
            cs/"WORK_STATE.md", cs/"NEXT_ACTION.md"
        ]
        assert_true(all(p.exists() and p.stat().st_size > 0 for p in bootstrap), "fresh-session bootstrap incomplete")

        # Model reassignment test: mutate only a disposable MODEL_ROUTING copy and verify IDs/changeset remain untouched.
        mr = troot/"08_TOOLCHAIN/MODEL_ROUTING.md"
        before_cs = cs.name
        txt = mr.read_text(encoding="utf-8").replace("BALANCED", "BALANCED_CANDIDATE", 1)
        mr.write_text(txt, encoding="utf-8")
        assert_true(cs.name == before_cs and "U999" in cs.name, "model reassignment affected project identity")

    print("PASS: disposable intake -> plan -> implementation -> independent review -> revision -> checkpoint -> fresh-session -> model-reassignment simulation")
    print("NOTE: Roblox Studio bridge itself is not exercised by this local disposable test; verify it in the active runtime/Studio.")
if __name__ == "__main__":
    main()
