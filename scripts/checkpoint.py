#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import argparse

ROOT = Path(__file__).resolve().parents[1]

def main():
    ap = argparse.ArgumentParser(description="Append a concise manual checkpoint marker to active WORK_STATE.")
    ap.add_argument("changeset", help="Changeset directory name under 04_CHANGESETS")
    ap.add_argument("--note", required=True)
    args = ap.parse_args()
    p = ROOT / "04_CHANGESETS" / args.changeset / "WORK_STATE.md"
    if not p.exists():
        raise SystemExit(f"Missing {p}")
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with p.open("a", encoding="utf-8") as f:
        f.write(f"\n## CHECKPOINT {stamp}\n\n{args.note.strip()}\n")
    print(f"Updated {p.relative_to(ROOT)}")
if __name__ == "__main__":
    main()
