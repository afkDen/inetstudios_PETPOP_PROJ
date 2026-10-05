#!/usr/bin/env python3
"""Core task-state helpers for the v8 streamlined team workflow.

This module deliberately keeps raw human input byte-preserved while avoiding the
v7 proposal -> promotion -> implementation triple lifecycle. A single GitHub
Issue and a single implementation branch/PR are the normal path.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANGESETS = ROOT / "04_CHANGESETS"
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
BRANCH = re.compile(r"^(?:feat|fix|docs)/(\d{1,6})-([a-z0-9]+(?:-[a-z0-9]+)*)$")
RISKS = {"LIGHT", "STANDARD", "CRITICAL"}
INTEGRITY_PROFILE = "v8.3.1-byte-provenance"
INTEGRITY_MARKER = f"- Intake integrity profile: {INTEGRITY_PROFILE}"
CURRENT_TASK_SCHEMA = 4
CURRENT_WORKFLOW = "streamlined-v8.5"
AMENDMENT_DIR = "SCOPE_AMENDMENTS"


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def issue_key(issue: int) -> str:
    if not 1 <= int(issue) <= 999999:
        raise ValueError("issue must be between 1 and 999999")
    return f"GH-{int(issue):06d}"


def slugify(value: str) -> str:
    text = re.sub(r"\.[^.]+$", "", str(value))
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    text = re.sub(r"-+", "-", text)[:60].strip("-")
    return text or "task"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def scope_fingerprint(text: str) -> str:
    """Legacy v8.3/v8.4 scope fingerprint kept for in-flight task compatibility."""
    text = re.sub(
        r"<!-- TEAM_APPROVAL_START -->.*?<!-- TEAM_APPROVAL_END -->",
        "<!-- TEAM_APPROVAL_BLOCK -->",
        text,
        flags=re.S,
    )
    text = text.split("## Delivery summary", 1)[0]
    return sha256_bytes(text.encode("utf-8"))


def base_scope_fingerprint(text: str) -> str:
    """Hash stable TASK.md design text for revisioned v8.5 scope.

    Risk/gates are machine-managed and are bound separately in the effective
    scope fingerprint, so an approved amendment can change them without
    rewriting or invalidating the immutable base design snapshot.
    """
    text = re.sub(
        r"<!-- TEAM_APPROVAL_START -->.*?<!-- TEAM_APPROVAL_END -->",
        "<!-- TEAM_APPROVAL_BLOCK -->",
        text,
        flags=re.S,
    )
    text = text.split("## Delivery summary", 1)[0]
    replacements = {
        r"(?m)^- Risk: .*?$": "- Risk: <MACHINE_MANAGED>",
        r"(?m)^- Risk tier: .*?$": "- Risk tier: <MACHINE_MANAGED>",
        r"(?m)^- Studio required: .*?$": "- Studio required: <MACHINE_MANAGED>",
        r"(?m)^- Independent AI review required: .*?$": "- Independent AI review required: <MACHINE_MANAGED>",
        r"(?m)^- Full quality packet required: .*?$": "- Full quality packet required: <MACHINE_MANAGED>",
        r"(?m)^- Active scope revision: .*?$": "- Active scope revision: <MACHINE_MANAGED>",
    }
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)
    return sha256_bytes(text.encode("utf-8"))


def amendment_fingerprint(text: str) -> str:
    """Hash the exact proposed amendment while excluding its decision receipt."""
    text = re.sub(
        r"<!-- TEAM_AMENDMENT_DECISION_START -->.*?<!-- TEAM_AMENDMENT_DECISION_END -->",
        "<!-- TEAM_AMENDMENT_DECISION_BLOCK -->",
        text,
        flags=re.S,
    )
    return sha256_bytes(text.encode("utf-8"))


def amendment_provenance_fingerprint(record: dict) -> str:
    """Bind a finalized amendment to any supplemental references supplied with it."""
    refs = []
    for ref in record.get("references", []) or []:
        if ref.get("type") == "file":
            refs.append({k: ref.get(k) for k in ("type", "name", "path", "sha256", "bytes")})
        elif ref.get("type") == "url":
            refs.append({"type": "url", "source": ref.get("source")})
        else:
            refs.append(ref)
    payload = {"amendment_sha256": record.get("sha256", ""), "references": refs}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return sha256_bytes(raw)


def approved_amendments(meta: dict) -> list[dict]:
    return sorted(
        [a for a in (meta.get("scope_amendments") or []) if a.get("status") == "APPROVED"],
        key=lambda a: int(a.get("id", 0)),
    )


def scope_history_fingerprint(meta: dict) -> str:
    raw = json.dumps(meta.get("scope_history") or [], sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return sha256_bytes(raw)


def effective_scope_fingerprint(meta: dict, task_text: str) -> str:
    payload = {
        "base_scope_sha256": meta.get("scope_base_sha256") or base_scope_fingerprint(task_text),
        "approved_amendments": [
            {"id": int(a["id"]), "sha256": a.get("sha256"), "provenance_sha256": a.get("provenance_sha256", "")} for a in approved_amendments(meta)
        ],
        "risk": meta.get("risk"),
        "gates": meta.get("gates", {}),
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return sha256_bytes(raw)


def provenance_fingerprint(meta: dict) -> str:
    """Bind approval to the exact intake provenance metadata.

    File bytes are validated independently against their recorded SHA-256. This
    fingerprint prevents an approved task from silently changing both a copied
    reference/request hash and its metadata without reopening human approval.
    Older v8.3 tasks without the v8.3.1 integrity profile remain readable.
    """
    refs=[]
    for ref in meta.get("references", []) or []:
        if ref.get("type") == "file":
            refs.append({k:ref.get(k) for k in ("type","name","path","sha256","bytes")})
        elif ref.get("type") == "url":
            refs.append({"type":"url","source":ref.get("source")})
        else:
            refs.append(ref)
    payload={
        "request_sha256":meta.get("request_sha256"),
        "references":refs,
    }
    raw=json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
    return sha256_bytes(raw)


def find_changesets(issue: int, root: Path = ROOT) -> list[Path]:
    key = issue_key(issue)
    return sorted((root / "04_CHANGESETS").glob(key + "_*"))


def find_changeset(issue: int, root: Path = ROOT) -> Path:
    matches = find_changesets(issue, root)
    if not matches:
        raise FileNotFoundError(f"no changeset found for {issue_key(issue)}")
    if len(matches) != 1:
        raise ValueError(f"multiple changesets found for {issue_key(issue)}: {', '.join(p.name for p in matches)}")
    return matches[0]


def _approval_block(status: str, approved_by: str = "", note: str = "", approved_at: str = "") -> str:
    return (
        "<!-- TEAM_APPROVAL_START -->\n"
        f"- Status: {status}\n"
        f"- Approved by: {approved_by or ''}\n"
        f"- Approved at: {approved_at or ''}\n"
        f"- Approval note/reference: {note or ''}\n"
        "<!-- TEAM_APPROVAL_END -->"
    )


def render_task_md(meta: dict) -> str:
    return f"""# TASK

## Identity
- Issue: {meta['key']}
- Kind: {meta['kind'].upper()}
- Branch: {meta['branch']}
- Human owner: {meta.get('owner') or 'TBD'}
- Risk: {meta['risk']}
- Intake integrity profile: {meta.get('integrity_profile') or 'legacy-v8.3'}
- Status: DESIGN

## Original request
See `USER_REQUEST.txt`. It is byte-preserved and must not be rewritten.
SHA-256: `{meta['request_sha256']}`

## References
{'See `REFERENCES.md` and the tracked `REFERENCES/` copies supplied at intake.' if meta.get('references') else 'No separate references were supplied at intake.'}

## Interpretation
- Requested:
- Recommended:
- Deferred / out of scope:
- Ambiguities that need a human decision:

## Decision record
- Open decision frontier:
- Resolved material decisions / rationale:
- External knowledge blockers / questionnaires:
- Research notes / primary sources:

## Approved scope
{_approval_block(meta['scope_approval']['status'], meta['scope_approval'].get('approved_by',''), meta['scope_approval'].get('note',''), meta['scope_approval'].get('approved_at',''))}
- Active scope revision: {meta.get('scope_revision', 0)}
- Scope evolution: `TASK.md` is the base scope. After initial approval, each APPROVED file under `SCOPE_AMENDMENTS/` overlays the prior revision in order; later approved text supersedes conflicting earlier scope. DRAFT amendments are proposals only.

## Risk / gate decisions
- Risk tier: {meta['risk']}
- Studio required: {meta['gates']['studio_required']}
- Independent AI review required: {meta['gates']['independent_review_required']}
- Full quality packet required: {meta['gates']['full_quality_packet_required']}

The Lead may recommend escalation from STANDARD to CRITICAL during design. Do not silently downgrade risk or waive a required gate.

## Design / architecture
- Player loop / behavior:
- Systems affected:
- Server/client authority:
- Persistence/networking/security impact:
- UI/UX impact:
- Assets/visual impact:
- Performance constraints:

## Implementation plan
1.

## Acceptance criteria
- [ ]

## Testing and evidence plan
- Static/unit checks:
- Native Rojo build:
- Studio/live scenarios:
- Independent review:

## Delivery summary
- Implemented:
- Deferred:
- Tests:
- Reviews:
- Blockers:
"""


def create_task(
    *,
    source: Path,
    issue: int,
    kind: str,
    title: str,
    slug: str,
    branch: str,
    owner: str = "",
    risk: str = "STANDARD",
    github_verified: bool = False,
    references: list[str] | None = None,
    root: Path = ROOT,
) -> Path:
    kind = kind.lower()
    risk = risk.upper()
    if kind not in {"idea", "update"}:
        raise ValueError("kind must be idea or update")
    if risk not in RISKS:
        raise ValueError("risk must be LIGHT, STANDARD, or CRITICAL")
    if not SLUG.fullmatch(slug):
        raise ValueError("invalid slug")
    if not BRANCH.fullmatch(branch):
        raise ValueError("invalid task branch")
    if int(BRANCH.fullmatch(branch).group(1)) != int(issue):
        raise ValueError("branch issue does not match task issue")
    source = Path(source).expanduser().resolve()
    if not source.is_file() or source.is_symlink() or source.suffix.lower() != ".txt":
        raise ValueError("source must be a real .txt file")
    raw = source.read_bytes()
    if not raw or len(raw) > 256 * 1024:
        raise ValueError("request must be 1 byte to 256 KiB")
    if find_changesets(issue, root):
        raise FileExistsError(f"{issue_key(issue)} already has a changeset; use team.py resume")

    key = issue_key(issue)
    dst = root / "04_CHANGESETS" / f"{key}_{slug}"
    dst.mkdir(parents=True, exist_ok=False)
    (dst / "USER_REQUEST.txt").write_bytes(raw)

    ref_records = []
    ref_dir = dst / "REFERENCES"
    for idx, value in enumerate(references or [], 1):
        value = str(value).strip()
        if not value:
            continue
        if re.match(r"^https?://", value, flags=re.I):
            ref_records.append({"type":"url","source":value})
            continue
        src_ref = Path(value).expanduser().resolve()
        if not src_ref.is_file() or src_ref.is_symlink():
            raise ValueError(f"reference is not a regular file: {value}")
        data = src_ref.read_bytes()
        if not data or len(data) > 20 * 1024 * 1024:
            raise ValueError(f"reference file must be 1 byte to 20 MiB: {src_ref.name}")
        safe = re.sub(r"[^A-Za-z0-9._-]+", "-", src_ref.name).strip("-.") or f"reference-{idx}"
        ref_dir.mkdir(exist_ok=True)
        target = ref_dir / f"{idx:02d}_{safe}"
        target.write_bytes(data)
        ref_records.append({
            "type":"file",
            "name":src_ref.name,
            "path":target.relative_to(dst).as_posix(),
            "sha256":sha256_bytes(data),
            "bytes":len(data),
        })

    meta = {
        "schema_version": CURRENT_TASK_SCHEMA,
        "workflow": CURRENT_WORKFLOW,
        "issue": int(issue),
        "key": key,
        "kind": kind,
        "title": title.strip() or slug.replace("-", " ").title(),
        "slug": slug,
        "branch": branch,
        "owner": owner,
        "risk": risk,
        "request_sha256": sha256_bytes(raw),
        "integrity_profile": INTEGRITY_PROFILE,
        "github_verified": bool(github_verified),
        "references": ref_records,
        "created_at": now(),
        "scope_revision": 0,
        "scope_base_sha256": "",
        "scope_history": [],
        "scope_history_sha256": "",
        "scope_amendments": [],
        "scope_approval": {"status": "PENDING", "revision": 0, "approved_by": "", "approved_at": "", "note": ""},
        "gates": {
            "studio_required": "AUTO",
            "independent_review_required": risk != "LIGHT",
            "full_quality_packet_required": risk == "CRITICAL",
        },
    }
    (dst / "TASK.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    if ref_records:
        lines=["# TASK REFERENCES","","These references were supplied with the human task intake. Local files are byte-copied into this changeset for team collaboration; URLs are recorded verbatim.",""]
        for r in ref_records:
            if r["type"] == "url":
                lines.append(f"- URL: {r['source']}")
            else:
                lines.append(f"- File: `{r['path']}` — `{r['sha256']}` ({r['bytes']} bytes)")
        (dst / "REFERENCES.md").write_text("\n".join(lines)+"\n", encoding="utf-8")
    (dst / "TASK.md").write_text(render_task_md(meta), encoding="utf-8")
    (dst / "WORK_STATE.md").write_text(
        "# WORK STATE\n\n"
        "- Status: OPEN\n"
        "- Stage: INTAKE\n"
        "- Current owner: LEAD_ORCHESTRATOR\n"
        f"- Risk: {risk}\n"
        "- Scope approval: PENDING\n"
        "- Active scope revision: 0\n"
        "- Pending scope amendment: none\n"
        "- Completed: raw request preserved and task branch created\n"
        "- In progress: repository inspection and design\n"
        "- Remaining: design, scope approval, implementation, tests, review, PR\n"
        "- Changed files:\n"
        "- Changed Studio instances:\n"
        "- Tests/evidence:\n"
        "- Blockers:\n"
        "- Next action: inspect request and repository, select relevant skills/roles, then prepare the implementation plan\n",
        encoding="utf-8",
    )
    evidence = {
        "schema_version": 2,
        "issue": int(issue),
        "risk": risk,
        "scope_revision": 0,
        "required_scope_revision": 0,
        "scope_attestation": {},
        "status": "DRAFT",
        "native_build": {"status": "PENDING", "evidence": ""},
        "studio": {"status": "PENDING" if meta["gates"]["studio_required"] is True else "NOT_DECIDED", "reason": "", "receipt": ""},
        "independent_review": {"status": "PENDING" if meta["gates"]["independent_review_required"] else "NOT_REQUIRED", "reviewer": "", "report": ""},
        "human_review": {"status": "PENDING", "reference": ""},
        "notes": [],
    }
    (dst / "EVIDENCE.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    return dst


def load_task(issue: int, root: Path = ROOT) -> tuple[Path, dict]:
    dst = find_changeset(issue, root)
    path = dst / "TASK.json"
    if not path.is_file():
        raise FileNotFoundError(f"{dst.name}/TASK.json missing; this may be a legacy v7 changeset")
    return dst, json.loads(path.read_text(encoding="utf-8"))


def _sync_evidence(dst: Path, meta: dict) -> None:
    path = dst / "EVIDENCE.json"
    if not path.is_file():
        return
    try:
        ev = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError):
        return
    ev["risk"] = meta["risk"]
    if meta.get("schema_version", 0) >= CURRENT_TASK_SCHEMA:
        ev.setdefault("schema_version", 2)
        ev.setdefault("scope_revision", 0)
        ev.setdefault("required_scope_revision", meta.get("scope_revision", 0))
        ev.setdefault("scope_attestation", {})
    gates = meta.get("gates", {})
    independent = ev.setdefault("independent_review", {})
    if gates.get("independent_review_required") is True:
        if independent.get("status") in {None, "NOT_REQUIRED"}:
            independent["status"] = "PENDING"
    elif independent.get("status") == "PENDING":
        independent["status"] = "NOT_REQUIRED"
    studio = ev.setdefault("studio", {})
    studio_gate = gates.get("studio_required")
    if studio_gate is True and studio.get("status") in {None, "NOT_REQUIRED", "NOT_DECIDED"}:
        studio["status"] = "PENDING"
    elif studio_gate is False and studio.get("status") in {None, "PENDING", "NOT_DECIDED"}:
        studio["status"] = "NOT_REQUIRED"
    elif studio_gate == "AUTO" and studio.get("status") in {None, "NOT_REQUIRED"}:
        studio["status"] = "NOT_DECIDED"
    path.write_text(json.dumps(ev, indent=2) + "\n", encoding="utf-8")


def _replace_or_append_line(text: str, label: str, value: str) -> str:
    pattern = rf"(?m)^- {re.escape(label)}: .*?$"
    line = f"- {label}: {value}"
    if re.search(pattern, text):
        return re.sub(pattern, line, text)
    if text and not text.endswith("\n"):
        text += "\n"
    return text + line + "\n"


def _sync_work_state(dst: Path, meta: dict, *, stage: str | None = None) -> None:
    ws = dst / "WORK_STATE.md"
    text = ws.read_text(encoding="utf-8") if ws.exists() else "# WORK STATE\n\n"
    approval = meta.get("scope_approval", {})
    revision = int(meta.get("scope_revision", 0) or 0)
    pending = [a for a in meta.get("scope_amendments", []) or [] if a.get("status") == "DRAFT"]
    text = _replace_or_append_line(text, "Scope approval", approval.get("status", "PENDING"))
    text = _replace_or_append_line(text, "Active scope revision", str(revision))
    text = _replace_or_append_line(text, "Pending scope amendment", str(pending[0]["id"]) if pending else "none")
    text = _replace_or_append_line(text, "Risk", str(meta.get("risk", "STANDARD")))
    if stage:
        text = _replace_or_append_line(text, "Stage", stage)
    ws.write_text(text, encoding="utf-8")


def _amendment_decision_block(status: str, actor: str = "", note: str = "", at: str = "", *,
                              resulting_revision: int | None = None, evidence_impact: str = "",
                              gate_changes: dict | None = None) -> str:
    return (
        "<!-- TEAM_AMENDMENT_DECISION_START -->\n"
        f"- Status: {status}\n"
        f"- Decided by: {actor or ''}\n"
        f"- Decided at: {at or ''}\n"
        f"- Resulting scope revision: {resulting_revision if resulting_revision is not None else ''}\n"
        f"- Evidence impact: {evidence_impact or ''}\n"
        f"- Approved risk/gate changes: {json.dumps(gate_changes or {}, sort_keys=True)}\n"
        f"- Decision note/reference: {note or ''}\n"
        "<!-- TEAM_AMENDMENT_DECISION_END -->"
    )


def render_scope_amendment(meta: dict, amendment_id: int, reason: str, requested_by: str = "", references: list[dict] | None = None) -> str:
    return f"""# SCOPE AMENDMENT {amendment_id:04d}

## Identity
- Issue: {meta['key']}
- Base scope revision: {int(meta.get('scope_revision', 0))}
- Proposed next revision: {int(meta.get('scope_revision', 0)) + 1}
- Requested by: {requested_by or meta.get('owner') or 'TBD'}
- Reason: {reason.strip()}

The currently approved scope remains authoritative until this amendment is explicitly approved. Pause only work affected by this proposal; unaffected work may continue within the current approved scope.

## Supplemental references
{chr(10).join(f"- {r.get('path') if r.get('type') == 'file' else r.get('source')}" for r in (references or [])) or '- None'}

## Requested scope changes
### Add
- 

### Change
- 

### Remove / defer
- 

## Acceptance-criteria impact
- 

## Design / architecture impact
- 

## Risk / gate impact
- Risk tier change needed: no / LIGHT / STANDARD / CRITICAL
- Studio gate change needed: no / yes / no
- Independent-review gate change needed: no / yes / no
- Full-quality-packet gate change needed: no / yes / no

## Existing-work impact
- Work that remains valid:
- Work to revise or discard:

## Evidence impact
- Evidence that remains applicable:
- Evidence that must be refreshed:
- Additional evidence required:

## Decision
{_amendment_decision_block('DRAFT')}
"""


def save_task(dst: Path, meta: dict) -> None:
    (dst / "TASK.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    task_md = dst / "TASK.md"
    text = task_md.read_text(encoding="utf-8") if task_md.exists() else render_task_md(meta)
    block = _approval_block(
        meta["scope_approval"]["status"],
        meta["scope_approval"].get("approved_by", ""),
        meta["scope_approval"].get("note", ""),
        meta["scope_approval"].get("approved_at", ""),
    )
    text = re.sub(
        r"<!-- TEAM_APPROVAL_START -->.*?<!-- TEAM_APPROVAL_END -->",
        block,
        text,
        flags=re.S,
    )
    text = re.sub(r"(?m)^- Risk: .*?$", f"- Risk: {meta['risk']}", text, count=1)
    text = re.sub(r"(?m)^- Risk tier: .*?$", f"- Risk tier: {meta['risk']}", text)
    text = re.sub(r"(?m)^- Studio required: .*?$", f"- Studio required: {meta['gates']['studio_required']}", text)
    text = re.sub(r"(?m)^- Independent AI review required: .*?$", f"- Independent AI review required: {meta['gates']['independent_review_required']}", text)
    text = re.sub(r"(?m)^- Full quality packet required: .*?$", f"- Full quality packet required: {meta['gates']['full_quality_packet_required']}", text)
    text = re.sub(r"(?m)^- Active scope revision: .*?$", f"- Active scope revision: {meta.get('scope_revision', 0)}", text)
    task_md.write_text(text, encoding="utf-8")
    _sync_evidence(dst, meta)


def _validate_username(value: str, label: str = "username") -> None:
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", value):
        raise ValueError(f"{label} must look like a GitHub username")


def _apply_gate_changes(meta: dict, *, risk: str | None = None, studio_required: bool | None = None,
                        independent_review_required: bool | None = None,
                        full_quality_packet_required: bool | None = None) -> dict:
    changes = {}
    if risk:
        risk = risk.upper()
        if risk not in RISKS:
            raise ValueError("risk must be LIGHT, STANDARD, or CRITICAL")
        if risk != meta.get("risk"):
            changes["risk"] = {"from": meta.get("risk"), "to": risk}
        meta["risk"] = risk
    for field, value in (
        ("studio_required", studio_required),
        ("independent_review_required", independent_review_required),
        ("full_quality_packet_required", full_quality_packet_required),
    ):
        if value is not None:
            value = bool(value)
            old = meta["gates"].get(field)
            if old != value:
                changes[field] = {"from": old, "to": value}
            meta["gates"][field] = value
    if meta["risk"] == "CRITICAL":
        for field in ("independent_review_required", "full_quality_packet_required"):
            old = meta["gates"].get(field)
            if old is not True:
                changes[field] = {"from": old, "to": True}
            meta["gates"][field] = True
    return changes


def _ensure_revisioned_scope(dst: Path, meta: dict) -> None:
    """Lazily upgrade an approved v8.3/v8.4 task without changing its meaning."""
    if meta.get("schema_version", 0) >= CURRENT_TASK_SCHEMA and "scope_revision" in meta:
        return
    task_md = dst / "TASK.md"
    task_text = task_md.read_text(encoding="utf-8")
    prior = dict(meta.get("scope_approval", {}))
    meta["schema_version"] = CURRENT_TASK_SCHEMA
    meta["workflow"] = CURRENT_WORKFLOW
    meta["scope_amendments"] = []
    meta["scope_history"] = []
    meta["scope_history_sha256"] = ""
    if prior.get("status") == "APPROVED":
        legacy_hash = prior.get("scope_sha256", "")
        meta["scope_revision"] = 1
        meta["scope_base_sha256"] = base_scope_fingerprint(task_text)
        migrated = dict(prior)
        migrated.update({"revision": 1, "approval_kind": "INITIAL_MIGRATED", "legacy_scope_sha256": legacy_hash, "risk": meta.get("risk"), "gates": dict(meta.get("gates", {}))})
        migrated["scope_sha256"] = effective_scope_fingerprint(meta, task_text)
        meta["scope_approval"] = migrated
        meta["scope_history"].append(dict(migrated))
        meta["scope_history_sha256"] = scope_history_fingerprint(meta)
    else:
        meta["scope_revision"] = 0
        meta["scope_base_sha256"] = ""
        meta["scope_approval"] = {"status": "PENDING", "revision": 0, "approved_by": "", "approved_at": "", "note": prior.get("note", "")}
    save_task(dst, meta)
    if prior.get("status") == "APPROVED":
        ev_path = dst / "EVIDENCE.json"
        if ev_path.is_file():
            ev = json.loads(ev_path.read_text(encoding="utf-8"))
            ev["schema_version"] = max(int(ev.get("schema_version", 1)), 2)
            ev["scope_revision"] = 1
            ev["required_scope_revision"] = 1
            ev["scope_attestation"] = {
                "revision": 1,
                "mode": "legacy-migration",
                "by": prior.get("approved_by") or "MIGRATION",
                "at": prior.get("approved_at") or now(),
                "note": "Metadata-only migration to revisioned scope; approved scope and evidence meaning are unchanged.",
            }
            ev_path.write_text(json.dumps(ev, indent=2) + "\n", encoding="utf-8")
    _sync_work_state(dst, meta)


def approve_task(issue: int, approved_by: str, note: str = "", *, risk: str | None = None,
                 studio_required: bool | None = None, independent_review_required: bool | None = None,
                 full_quality_packet_required: bool | None = None, root: Path = ROOT) -> Path:
    _validate_username(approved_by, "approved-by")
    dst, meta = load_task(issue, root)
    if meta.get("scope_approval", {}).get("status") == "APPROVED":
        raise ValueError("scope is already approved; create a scope amendment instead of overwriting approval history")
    _ensure_revisioned_scope(dst, meta)
    _apply_gate_changes(
        meta, risk=risk, studio_required=studio_required,
        independent_review_required=independent_review_required,
        full_quality_packet_required=full_quality_packet_required,
    )
    task_md = dst / "TASK.md"
    if not task_md.is_file():
        raise FileNotFoundError(f"{dst.name}/TASK.md missing")
    task_text = task_md.read_text(encoding="utf-8")
    if meta.get("integrity_profile") == INTEGRITY_PROFILE and INTEGRITY_MARKER not in task_text:
        raise ValueError("TASK.md is missing the v8.3.1 intake integrity marker; restore/review it before approval")
    base_hash = base_scope_fingerprint(task_text)
    prior_revision = int(meta.get("scope_revision", 0) or 0)
    new_revision = prior_revision + 1
    meta["scope_revision"] = new_revision
    meta["scope_base_sha256"] = base_hash
    approval = {
        "status": "APPROVED",
        "revision": new_revision,
        "approval_kind": "INITIAL" if prior_revision == 0 else "BASE_REAPPROVAL",
        "approved_by": approved_by,
        "approved_at": now(),
        "note": note.strip(),
        "provenance_sha256": provenance_fingerprint(meta),
        "risk": meta.get("risk"),
        "gates": dict(meta.get("gates", {})),
    }
    meta["scope_approval"] = approval
    approval["scope_sha256"] = effective_scope_fingerprint(meta, task_text)
    if prior_revision == 0:
        meta["scope_history"] = [dict(approval)]
    else:
        meta.setdefault("scope_history", []).append(dict(approval))
    meta["scope_history_sha256"] = scope_history_fingerprint(meta)
    save_task(dst, meta)
    ev_path = dst / "EVIDENCE.json"
    if ev_path.is_file():
        ev = json.loads(ev_path.read_text(encoding="utf-8"))
        ev["schema_version"] = max(int(ev.get("schema_version", 1)), 2)
        ev["required_scope_revision"] = new_revision
        if prior_revision == 0:
            ev["scope_revision"] = new_revision
            ev["scope_attestation"] = {"revision": new_revision, "mode": "initial-approval", "by": approved_by, "at": approval["approved_at"], "note": "Initial evidence baseline starts at approved scope revision 1."}
        else:
            ev["status"] = "DRAFT"
            ev["scope_attestation"] = {}
            ev.setdefault("notes", []).append(f"Base scope was reapproved as revision {new_revision}; delivery evidence must be reviewed/refreshed before final delivery.")
        ev_path.write_text(json.dumps(ev, indent=2) + "\n", encoding="utf-8")
    _sync_work_state(dst, meta, stage="IMPLEMENTATION_READY")
    return dst


def create_scope_amendment(issue: int, reason: str, requested_by: str = "", references: list[str] | None = None, *, root: Path = ROOT) -> Path:
    if not reason.strip():
        raise ValueError("scope amendment reason cannot be blank")
    if requested_by:
        _validate_username(requested_by, "requested-by")
    dst, meta = load_task(issue, root)
    if meta.get("scope_approval", {}).get("status") != "APPROVED":
        raise ValueError("initial scope must be approved before creating a scope amendment")
    _ensure_revisioned_scope(dst, meta)
    pending = [a for a in meta.get("scope_amendments", []) if a.get("status") == "DRAFT"]
    if pending:
        raise ValueError(f"scope amendment {pending[0]['id']} is already DRAFT; approve or withdraw it before creating another")
    amendment_id = 1 + max([int(a.get("id", 0)) for a in meta.get("scope_amendments", [])] or [0])
    folder = dst / AMENDMENT_DIR
    folder.mkdir(exist_ok=True)
    ref_records = []
    prepared_files = []
    ref_dir = folder / "REFERENCES" / f"AMENDMENT-{amendment_id:04d}"
    for idx, value in enumerate(references or [], 1):
        if re.match(r"^https?://", value, flags=re.I):
            ref_records.append({"type": "url", "source": value})
            continue
        src_ref = Path(value).expanduser().resolve()
        if not src_ref.is_file() or src_ref.is_symlink():
            raise ValueError(f"amendment reference is not a regular file: {value}")
        raw = src_ref.read_bytes()
        if not (1 <= len(raw) <= 20 * 1024 * 1024):
            raise ValueError(f"amendment reference file must be 1 byte to 20 MiB: {src_ref.name}")
        safe = re.sub(r"[^A-Za-z0-9._-]+", "-", src_ref.name).strip("-.") or f"reference-{idx}"
        target = ref_dir / f"{idx:02d}_{safe}"
        prepared_files.append((target, raw))
        ref_records.append({
            "type": "file", "name": src_ref.name, "path": target.relative_to(dst).as_posix(),
            "sha256": sha256_bytes(raw), "bytes": len(raw),
        })
    if prepared_files:
        ref_dir.mkdir(parents=True, exist_ok=True)
        for target, raw in prepared_files:
            target.write_bytes(raw)
    path = folder / f"AMENDMENT-{amendment_id:04d}.md"
    path.write_text(render_scope_amendment(meta, amendment_id, reason, requested_by, ref_records), encoding="utf-8")
    record = {
        "id": amendment_id,
        "status": "DRAFT",
        "base_revision": int(meta.get("scope_revision", 0)),
        "target_revision": int(meta.get("scope_revision", 0)) + 1,
        "path": path.relative_to(dst).as_posix(),
        "reason": reason.strip(),
        "requested_by": requested_by or meta.get("owner", ""),
        "created_at": now(),
        "references": ref_records,
    }
    meta.setdefault("scope_amendments", []).append(record)
    save_task(dst, meta)
    _sync_work_state(dst, meta, stage="SCOPE_AMENDMENT_DRAFT")
    return path


def _find_amendment(meta: dict, amendment_id: int) -> dict:
    matches = [a for a in meta.get("scope_amendments", []) or [] if int(a.get("id", -1)) == int(amendment_id)]
    if len(matches) != 1:
        raise ValueError(f"scope amendment {amendment_id} not found")
    return matches[0]


def _write_amendment_decision(dst: Path, record: dict, status: str, actor: str, note: str, at: str, *, resulting_revision: int | None = None, evidence_impact: str = "", gate_changes: dict | None = None) -> None:
    path = dst / record["path"]
    text = path.read_text(encoding="utf-8")
    block = _amendment_decision_block(status, actor, note, at, resulting_revision=resulting_revision, evidence_impact=evidence_impact, gate_changes=gate_changes)
    text = re.sub(
        r"<!-- TEAM_AMENDMENT_DECISION_START -->.*?<!-- TEAM_AMENDMENT_DECISION_END -->",
        block,
        text,
        flags=re.S,
    )
    path.write_text(text, encoding="utf-8")


def _rebind_scope_receipts(dst: Path, revision: int, actor: str, note: str, mode: str) -> None:
    """Explicitly rebind existing heavy receipts after human review of applicability.

    This never changes PASS/PENDING status or manufactures evidence; it only
    records which approved scope revision the existing receipt was reviewed for.
    """
    for name in ("STUDIO_DELIVERY.json", "QUALITY_EVIDENCE.json"):
        path = dst / name
        if not path.is_file():
            continue
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError):
            continue
        doc["schema_version"] = max(int(doc.get("schema_version", 1)), 2)
        doc["scope_revision"] = revision
        doc["scope_rebind"] = {
            "revision": revision, "mode": mode, "by": actor, "at": now(), "note": note.strip(),
        }
        path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")


def approve_scope_amendment(issue: int, amendment_id: int, approved_by: str, note: str = "", *,
                            risk: str | None = None, studio_required: bool | None = None,
                            independent_review_required: bool | None = None,
                            full_quality_packet_required: bool | None = None,
                            evidence_impact: str = "refresh-affected", root: Path = ROOT) -> Path:
    _validate_username(approved_by, "approved-by")
    if evidence_impact not in {"retain", "refresh-affected", "reset"}:
        raise ValueError("evidence-impact must be retain, refresh-affected, or reset")
    dst, meta = load_task(issue, root)
    if meta.get("scope_approval", {}).get("status") != "APPROVED":
        raise ValueError("there is no active approved scope to amend")
    _ensure_revisioned_scope(dst, meta)
    record = _find_amendment(meta, amendment_id)
    if record.get("status") != "DRAFT":
        raise ValueError(f"scope amendment {amendment_id} is not DRAFT")
    current_revision = int(meta.get("scope_revision", 0))
    if int(record.get("base_revision", -1)) != current_revision:
        raise ValueError("scope amendment is stale because the active scope revision changed; withdraw and redraft it")
    path = dst / record["path"]
    if not path.is_file() or path.is_symlink():
        raise ValueError("scope amendment file missing or invalid")
    amendment_text = path.read_text(encoding="utf-8")
    if not re.search(r"(?ms)^## Requested scope changes\s+.*?^## Acceptance-criteria impact", amendment_text):
        raise ValueError("scope amendment structure is incomplete")
    proposed_hash = amendment_fingerprint(amendment_text)
    requested_block = re.search(r"(?ms)^## Requested scope changes\s+(.*?)^## Acceptance-criteria impact", amendment_text)
    substantive_scope_change = bool(requested_block and re.search(r"(?m)^-[ \t]+\S", requested_block.group(1)))
    prior_risk = meta.get("risk")
    prior_gates = dict(meta.get("gates", {}))
    gate_changes = _apply_gate_changes(
        meta, risk=risk, studio_required=studio_required,
        independent_review_required=independent_review_required,
        full_quality_packet_required=full_quality_packet_required,
    )
    if not substantive_scope_change and not gate_changes:
        raise ValueError("scope amendment has no substantive scope or gate change; do not approve an empty amendment")
    deescalations = []
    if prior_risk == "CRITICAL" and meta.get("risk") != "CRITICAL":
        deescalations.append("risk")
        if not substantive_scope_change:
            raise ValueError("downgrading CRITICAL risk requires a substantive scope change that removes the critical behavior")
    for field in ("studio_required", "independent_review_required", "full_quality_packet_required"):
        if prior_gates.get(field) is True and meta.get("gates", {}).get(field) is False:
            deescalations.append(field)
    if deescalations and not note.strip():
        raise ValueError("risk/gate de-escalation requires a nonblank human approval note explaining why it is safe")
    if evidence_impact == "retain" and not note.strip():
        raise ValueError("retaining existing evidence across a scope amendment requires a nonblank human approval note")
    decided_at = now()
    record.update({
        "status": "APPROVED",
        "sha256": proposed_hash,
        "approved_by": approved_by,
        "approved_at": decided_at,
        "note": note.strip(),
        "evidence_impact": evidence_impact,
        "gate_changes": gate_changes,
    })
    record["provenance_sha256"] = amendment_provenance_fingerprint(record)
    meta["scope_revision"] = current_revision + 1
    task_text = (dst / "TASK.md").read_text(encoding="utf-8")
    current = {
        "status": "APPROVED",
        "revision": meta["scope_revision"],
        "approval_kind": "AMENDMENT",
        "amendment_id": amendment_id,
        "approved_by": approved_by,
        "approved_at": decided_at,
        "note": note.strip(),
        "provenance_sha256": provenance_fingerprint(meta),
        "risk": meta.get("risk"),
        "gates": dict(meta.get("gates", {})),
        "amendment_sha256": record.get("sha256", ""),
        "amendment_provenance_sha256": record.get("provenance_sha256", ""),
        "evidence_impact": evidence_impact,
        "gate_changes": gate_changes,
    }
    meta["scope_approval"] = current
    current["scope_sha256"] = effective_scope_fingerprint(meta, task_text)
    meta.setdefault("scope_history", []).append(dict(current))
    meta["scope_history_sha256"] = scope_history_fingerprint(meta)
    _write_amendment_decision(dst, record, "APPROVED", approved_by, note.strip(), decided_at, resulting_revision=meta["scope_revision"], evidence_impact=evidence_impact, gate_changes=gate_changes)
    save_task(dst, meta)
    ev_path = dst / "EVIDENCE.json"
    if ev_path.is_file():
        ev = json.loads(ev_path.read_text(encoding="utf-8"))
        ev["schema_version"] = max(int(ev.get("schema_version", 1)), 2)
        ev["required_scope_revision"] = meta["scope_revision"]
        if evidence_impact == "retain":
            ev["scope_revision"] = meta["scope_revision"]
            ev["scope_attestation"] = {"revision": meta["scope_revision"], "mode": "human-approved-retain", "by": approved_by, "at": decided_at, "note": note.strip() or "Scope amendment approved with existing evidence retained."}
        elif evidence_impact == "reset":
            ev["scope_revision"] = meta["scope_revision"]
            ev["status"] = "DRAFT"
            ev["native_build"] = {"status": "PENDING", "evidence": ""}
            ev["studio"] = {"status": "PENDING" if meta["gates"].get("studio_required") is True else ("NOT_REQUIRED" if meta["gates"].get("studio_required") is False else "NOT_DECIDED"), "reason": "", "receipt": ""}
            ev["independent_review"] = {"status": "PENDING" if meta["gates"].get("independent_review_required") else "NOT_REQUIRED", "reviewer": "", "report": ""}
            ev["scope_attestation"] = {"revision": meta["scope_revision"], "mode": "reset", "by": approved_by, "at": decided_at, "note": "Evidence reset by approved scope amendment."}
        else:
            ev["status"] = "DRAFT"
            ev["scope_attestation"] = {}
            ev.setdefault("notes", []).append(f"Scope revision {meta['scope_revision']} approved; affected evidence must be reviewed/refreshed before delivery.")
        ev_path.write_text(json.dumps(ev, indent=2) + "\n", encoding="utf-8")
    if evidence_impact == "retain":
        _rebind_scope_receipts(dst, meta["scope_revision"], approved_by, note.strip(), "human-approved-retain")
    _sync_work_state(dst, meta, stage="IMPLEMENTATION_READY")
    return path


def withdraw_scope_amendment(issue: int, amendment_id: int, actor: str, note: str, *, root: Path = ROOT) -> Path:
    _validate_username(actor, "withdrawn-by")
    if not note.strip():
        raise ValueError("withdrawal note cannot be blank")
    dst, meta = load_task(issue, root)
    _ensure_revisioned_scope(dst, meta)
    record = _find_amendment(meta, amendment_id)
    if record.get("status") != "DRAFT":
        raise ValueError(f"scope amendment {amendment_id} is not DRAFT")
    at = now()
    path = dst / record["path"]
    withdrawn_hash = amendment_fingerprint(path.read_text(encoding="utf-8"))
    record.update({"status": "WITHDRAWN", "sha256": withdrawn_hash, "withdrawn_by": actor, "withdrawn_at": at, "withdrawal_note": note.strip()})
    record["provenance_sha256"] = amendment_provenance_fingerprint(record)
    _write_amendment_decision(dst, record, "WITHDRAWN", actor, note.strip(), at, resulting_revision=int(meta.get("scope_revision", 0)))
    save_task(dst, meta)
    _sync_work_state(dst, meta, stage="IMPLEMENTATION_READY")
    return dst / record["path"]


def attest_evidence_scope(issue: int, actor: str, note: str, *, root: Path = ROOT) -> Path:
    _validate_username(actor, "attested-by")
    if not note.strip():
        raise ValueError("evidence scope attestation note cannot be blank")
    dst, meta = load_task(issue, root)
    if meta.get("scope_approval", {}).get("status") != "APPROVED":
        raise ValueError("scope must be approved before evidence can be attested")
    pending = [a for a in meta.get("scope_amendments", []) or [] if a.get("status") == "DRAFT"]
    if pending:
        raise ValueError("resolve the pending scope amendment before marking delivery evidence current")
    ev_path = dst / "EVIDENCE.json"
    if not ev_path.is_file():
        raise FileNotFoundError("EVIDENCE.json missing")
    ev = json.loads(ev_path.read_text(encoding="utf-8"))
    revision = int(meta.get("scope_revision", 0))
    ev["schema_version"] = max(int(ev.get("schema_version", 1)), 2)
    ev["scope_revision"] = revision
    ev["required_scope_revision"] = revision
    ev["scope_attestation"] = {"revision": revision, "mode": "reviewed-current", "by": actor, "at": now(), "note": note.strip()}
    ev_path.write_text(json.dumps(ev, indent=2) + "\n", encoding="utf-8")
    _rebind_scope_receipts(dst, revision, actor, note.strip(), "reviewed-current")
    return ev_path


def reopen_approval(issue: int, note: str = "", *, root: Path = ROOT) -> Path:
    """Legacy escape hatch for old tooling; v8.5 normally uses scope amendments.

    This intentionally invalidates the whole active approval. Use it only when
    repairing/rebasing a legacy task whose base TASK.md itself must be rewritten.
    """
    dst, meta = load_task(issue, root)
    pending = [a for a in meta.get("scope_amendments", []) or [] if a.get("status") == "DRAFT"]
    if pending:
        raise ValueError("withdraw the DRAFT scope amendment before using the legacy full-reopen recovery path")
    prior = meta.get("scope_approval", {})
    meta["scope_approval"] = {
        "status": "PENDING",
        "revision": int(meta.get("scope_revision", 0) or 0),
        "approved_by": "",
        "approved_at": "",
        "note": ("Legacy full reopen after prior approval" + (f": {note.strip()}" if note.strip() else "")),
        "previous": prior,
    }
    save_task(dst, meta)
    _sync_work_state(dst, meta, stage="DESIGN")
    return dst


def set_gates(issue: int, *, studio_required: bool | None = None, independent_review_required: bool | None = None,
              full_quality_packet_required: bool | None = None, risk: str | None = None, root: Path = ROOT,
              allow_approved: bool = False) -> Path:
    dst, meta = load_task(issue, root)
    if meta.get("scope_approval", {}).get("status") == "APPROVED" and not allow_approved:
        raise ValueError("risk/gates are part of approved scope; change them through an approved scope amendment")
    _apply_gate_changes(
        meta, risk=risk, studio_required=studio_required,
        independent_review_required=independent_review_required,
        full_quality_packet_required=full_quality_packet_required,
    )
    save_task(dst, meta)
    _sync_work_state(dst, meta)
    return dst


def _validate_revisioned_scope(dst: Path, meta: dict, errors: list[str]) -> None:
    task_md = dst / "TASK.md"
    task_text = task_md.read_text(encoding="utf-8") if task_md.is_file() else ""
    base_expected = meta.get("scope_base_sha256")
    if not base_expected:
        errors.append("revisioned task is missing base scope fingerprint")
    elif base_scope_fingerprint(task_text) != base_expected:
        errors.append("approved TASK.md scope changed after human approval; use a scope amendment or legacy full reopen")
    seen_ids = set()
    for record in meta.get("scope_amendments", []) or []:
        try:
            aid = int(record.get("id"))
        except (TypeError, ValueError):
            errors.append("scope amendment has invalid id")
            continue
        if aid in seen_ids:
            errors.append(f"duplicate scope amendment id: {aid}")
        seen_ids.add(aid)
        rel = record.get("path", "")
        path = dst / rel
        try:
            if not path.is_file() or path.is_symlink() or path.resolve().parent != (dst / AMENDMENT_DIR).resolve():
                errors.append(f"scope amendment file missing/invalid: {rel}")
                continue
        except OSError:
            errors.append(f"scope amendment file unreadable: {rel}")
            continue
        for ref in record.get("references", []) or []:
            if ref.get("type") == "file":
                rel_ref = ref.get("path") or ""
                rp = dst / rel_ref
                expected_parent = (dst / AMENDMENT_DIR / "REFERENCES" / f"AMENDMENT-{aid:04d}").resolve()
                try:
                    if not rp.is_file() or rp.is_symlink() or rp.resolve().parent != expected_parent:
                        errors.append(f"amendment reference file missing/invalid: {rel_ref}")
                    elif sha256_bytes(rp.read_bytes()) != ref.get("sha256"):
                        errors.append(f"amendment reference file hash mismatch: {rel_ref}")
                except OSError:
                    errors.append(f"amendment reference file unreadable: {rel_ref}")
            elif ref.get("type") == "url":
                if not re.match(r"^https?://", str(ref.get("source", "")), flags=re.I):
                    errors.append(f"scope amendment {aid} has invalid reference URL")
            else:
                errors.append(f"scope amendment {aid} has unknown reference type")
        if record.get("status") in {"APPROVED", "WITHDRAWN"}:
            actual = amendment_fingerprint(path.read_text(encoding="utf-8"))
            if not record.get("sha256") or actual != record.get("sha256"):
                errors.append(f"finalized scope amendment {aid} changed after decision")
            elif not record.get("provenance_sha256") or record.get("provenance_sha256") != amendment_provenance_fingerprint(record):
                errors.append(f"finalized scope amendment {aid} reference provenance changed after decision")
        elif record.get("status") != "DRAFT":
            errors.append(f"scope amendment {aid} has invalid status")
    amendment_root = dst / AMENDMENT_DIR
    if amendment_root.is_dir():
        registered = {str(a.get("path", "")) for a in meta.get("scope_amendments", []) or []}
        for candidate in amendment_root.glob("AMENDMENT-*.md"):
            rel = candidate.relative_to(dst).as_posix()
            if rel not in registered:
                errors.append(f"unregistered scope amendment file: {rel}")
    history = meta.get("scope_history") or []
    expected_history_hash = meta.get("scope_history_sha256")
    if history and (not expected_history_hash or expected_history_hash != scope_history_fingerprint(meta)):
        errors.append("scope approval history fingerprint mismatch")
    revisions = [int(h.get("revision", -1)) for h in history if isinstance(h, dict)]
    current_revision = int(meta.get("scope_revision", 0) or 0)
    if history and revisions != list(range(1, current_revision + 1)):
        errors.append("scope approval history revisions are not contiguous")
    approved_records = approved_amendments(meta)
    amendment_history = [h for h in history if h.get("approval_kind") == "AMENDMENT"]
    if len(amendment_history) != len(approved_records):
        errors.append("approved scope amendments do not match approval history")
    else:
        for hist, rec in zip(amendment_history, approved_records):
            if int(hist.get("amendment_id", -1)) != int(rec.get("id", -2)):
                errors.append("scope amendment approval history order mismatch")
                break
            if hist.get("amendment_sha256") != rec.get("sha256") or hist.get("amendment_provenance_sha256") != rec.get("provenance_sha256"):
                errors.append("scope amendment approval history fingerprint mismatch")
                break
    approval = meta.get("scope_approval", {})
    if approval.get("status") == "APPROVED":
        if int(approval.get("revision", -1)) != int(meta.get("scope_revision", -2)):
            errors.append("active scope approval revision does not match TASK.json scope_revision")
        expected = approval.get("scope_sha256")
        actual = effective_scope_fingerprint(meta, task_text)
        if not expected or actual != expected:
            errors.append("effective approved scope fingerprint changed after approval")
        history = meta.get("scope_history") or []
        if not history or int(history[-1].get("revision", -1)) != int(meta.get("scope_revision", -2)):
            errors.append("scope approval history does not end at the active revision")


def validate_task(issue: int, root: Path = ROOT, *, require_approved: bool = False, require_delivery: bool = False) -> list[str]:
    errors: list[str] = []
    try:
        dst, meta = load_task(issue, root)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        return [str(exc)]
    raw = dst / "USER_REQUEST.txt"
    if not raw.is_file() or raw.is_symlink():
        errors.append("USER_REQUEST.txt missing or symlinked")
    elif sha256_bytes(raw.read_bytes()) != meta.get("request_sha256"):
        errors.append("USER_REQUEST.txt differs from recorded SHA-256")
    if meta.get("schema_version") not in {2, 3, 4} or meta.get("workflow") not in {"streamlined-v8", "streamlined-v8.1", "streamlined-v8.2", "streamlined-v8.3", CURRENT_WORKFLOW}:
        errors.append("TASK.json is not a supported streamlined-v8 through v8.5 task")
    if meta.get("issue") != int(issue) or meta.get("key") != issue_key(issue):
        errors.append("TASK.json issue identity mismatch")
    if meta.get("risk") not in RISKS:
        errors.append("invalid task risk")
    branch = str(meta.get("branch", ""))
    m = BRANCH.fullmatch(branch)
    if not m or int(m.group(1)) != int(issue):
        errors.append("invalid task branch identity")
    for ref in meta.get("references", []) or []:
        if ref.get("type") == "file":
            rel = ref.get("path") or ""
            rp = dst / rel
            try:
                if not rp.is_file() or rp.is_symlink() or rp.resolve().parent != (dst / "REFERENCES").resolve():
                    errors.append(f"reference file missing/invalid: {rel}")
                elif sha256_bytes(rp.read_bytes()) != ref.get("sha256"):
                    errors.append(f"reference file hash mismatch: {rel}")
            except OSError:
                errors.append(f"reference file unreadable: {rel}")
        elif ref.get("type") == "url":
            if not re.match(r"^https?://", str(ref.get("source", "")), flags=re.I):
                errors.append("invalid task reference URL")
        else:
            errors.append("unknown task reference type")

    approval = meta.get("scope_approval", {})
    if require_approved and approval.get("status") != "APPROVED":
        errors.append("human scope approval is still PENDING")
    if approval.get("status") == "APPROVED":
        task_md = dst / "TASK.md"
        task_text = task_md.read_text(encoding="utf-8") if task_md.is_file() else ""
        if meta.get("schema_version", 0) >= CURRENT_TASK_SCHEMA or "scope_revision" in meta:
            _validate_revisioned_scope(dst, meta, errors)
        else:
            expected_scope = approval.get("scope_sha256")
            if not task_md.is_file() or not expected_scope:
                errors.append("approved task is missing its scope fingerprint")
            elif scope_fingerprint(task_text) != expected_scope:
                errors.append("approved TASK.md scope changed after human approval; reopen and reapprove")
        hardened_task = INTEGRITY_MARKER in task_text or meta.get("integrity_profile") == INTEGRITY_PROFILE
        if hardened_task:
            if meta.get("integrity_profile") != INTEGRITY_PROFILE:
                errors.append("v8.3.1 task integrity profile metadata is missing or changed")
            if INTEGRITY_MARKER not in task_text:
                errors.append("v8.3.1 TASK.md intake integrity marker is missing")
            expected_provenance = approval.get("provenance_sha256")
            if not expected_provenance:
                errors.append("approved task is missing its intake provenance fingerprint")
            elif provenance_fingerprint(meta) != expected_provenance:
                errors.append("approved task intake provenance changed after human approval; scope amendment cannot rewrite intake")
    gates = meta.get("gates", {})
    if gates.get("studio_required") not in {True, False, "AUTO"}:
        errors.append("studio_required must be true, false, or AUTO")
    if meta.get("risk") == "CRITICAL":
        if gates.get("independent_review_required") is not True:
            errors.append("CRITICAL tasks cannot waive independent review")
        if gates.get("full_quality_packet_required") is not True:
            errors.append("CRITICAL tasks require the full quality packet")
    if require_delivery:
        pending = [a for a in meta.get("scope_amendments", []) or [] if a.get("status") == "DRAFT"]
        if pending:
            errors.append(f"scope amendment {pending[0]['id']} is still DRAFT; approve or withdraw it before final delivery")
        ev_path = dst / "EVIDENCE.json"
        if not ev_path.is_file():
            errors.append("EVIDENCE.json missing")
        else:
            try:
                ev = json.loads(ev_path.read_text(encoding="utf-8"))
                if ev.get("issue") != int(issue):
                    errors.append("EVIDENCE.json issue mismatch")
                if meta.get("schema_version", 0) >= CURRENT_TASK_SCHEMA:
                    revision = int(meta.get("scope_revision", 0))
                    if ev.get("scope_revision") != revision or ev.get("required_scope_revision") != revision:
                        errors.append(f"delivery evidence is not attested for current scope revision {revision}")
                    att = ev.get("scope_attestation") or {}
                    if att.get("revision") != revision or not att.get("by") or not att.get("note"):
                        errors.append("current scope revision evidence attestation is missing")
                if gates.get("independent_review_required") is True and ev.get("independent_review", {}).get("status") != "PASS":
                    errors.append("required independent review is not PASS")
                if gates.get("studio_required") == "AUTO":
                    errors.append("studio_required is still AUTO; resolve it before final delivery")
                elif gates.get("studio_required") is True:
                    receipt = dst / "STUDIO_DELIVERY.json"
                    if not receipt.is_file():
                        errors.append("Studio is required but STUDIO_DELIVERY.json is missing")
                if gates.get("full_quality_packet_required") is True and not (dst / "QUALITY_EVIDENCE.json").is_file():
                    errors.append("full quality packet required but QUALITY_EVIDENCE.json is missing")
            except (OSError, ValueError, json.JSONDecodeError):
                errors.append("EVIDENCE.json is malformed")
    return errors

