#!/usr/bin/env python3
"""Read-only workstation dependency doctor with explicit opt-in installs.

Default behavior only probes. It never installs Python, Blender, Node, Rokit,
uv, pipx, GUI apps, or system packages. ``--install-recommended`` may install
or repair exact pinned project CLI capabilities through an already-installed
``uv`` (preferred) or ``pipx`` plus Rokit. Blender addon mutation remains a
separate explicit flag.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "08_TOOLCHAIN/WORKSTATION_DEPENDENCIES.json").read_text())
LOCAL = ROOT / ".local"

GRAPHIFY_PACKAGE = "graphifyy==0.9.74"
GRAPHIFY_VERSION = "0.9.74"
BLENDER_MCP_PACKAGE = "mcp-for-blender==2.1.3"
BLENDER_MCP_VERSION = "2.1.3"
BLENDER_MIN = (4, 2, 0)
PYTHON_MIN = (3, 10, 0)
BLENDER_RUNTIME_DEFAULTS = {
    "BLENDER_HOST": "localhost",
    "BLENDER_MCP_SAFE_MODE": "1",
    "DISABLE_TELEMETRY": "true",
}


def run(argv, timeout=30):
    try:
        return subprocess.run(
            argv,
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None


def version(command, args=("--version",)):
    path = shutil.which(command)
    if not path:
        return {"found": False, "path": None, "version_output": None}
    cp = run([path, *args])
    raw = (((cp.stdout or "") + " " + (cp.stderr or "")).strip()[:500]) if cp else ""
    return {
        "found": True,
        "path": path,
        "version_output": raw,
        "exit_code": cp.returncode if cp else None,
    }


def semver(raw):
    m = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", raw or "")
    return tuple(map(int, m.groups(default="0"))) if m else None


def python_candidates():
    out, seen = [], set()
    launchers = ["py", "python3.13", "python3.12", "python3.11", "python3.10", "python3", "python"]
    for name in launchers:
        path = shutil.which(name)
        if not path:
            continue
        variants = []
        if os.name == "nt" and Path(path).name.lower().startswith("py"):
            for selector in ("-3.13", "-3.12", "-3.11", "-3.10"):
                variants.append([path, selector])
        variants.append([path])
        for prefix in variants:
            cp = run(prefix + ["-c", 'import sys; print(sys.executable); print("%d.%d.%d"%sys.version_info[:3])'])
            if not cp or cp.returncode:
                continue
            lines = [x.strip() for x in cp.stdout.splitlines() if x.strip()]
            if len(lines) < 2:
                continue
            exe = lines[0]
            if exe in seen:
                continue
            seen.add(exe)
            out.append(
                {
                    "launcher": name,
                    "path": path,
                    "executable": exe,
                    "argv_prefix": prefix,
                    "version": lines[1],
                }
            )
    return out


def suitable_python(candidates):
    valid = [x for x in candidates if semver(x["version"]) and semver(x["version"]) >= PYTHON_MIN]
    if not valid:
        return None
    # Prefer 3.11/3.12 for broad third-party wheel compatibility, otherwise first valid.
    for wanted in ((3, 11), (3, 12), (3, 10), (3, 13)):
        for item in valid:
            v = semver(item["version"])
            if v and v[:2] == wanted:
                return item
    return valid[0]


def locate_blender():
    candidates = []
    if os.environ.get("BLENDER_PATH"):
        candidates.append(os.environ["BLENDER_PATH"])
    direct = shutil.which("blender")
    if direct:
        candidates.append(direct)
    if os.name == "nt":
        import glob

        candidates += sorted(
            glob.glob(r"C:\Program Files\Blender Foundation\Blender *\blender.exe"), reverse=True
        )
    elif sys.platform == "darwin":
        candidates += ["/Applications/Blender.app/Contents/MacOS/Blender"]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(Path(candidate))
    return None


def pipx_versions():
    pipx = shutil.which("pipx")
    if not pipx:
        return {}
    cp = run([pipx, "list", "--json"])
    if not cp or cp.returncode:
        return {}
    try:
        data = json.loads(cp.stdout)
    except ValueError:
        return {}
    out = {}
    for name, venv in (data.get("venvs") or {}).items():
        main = ((venv or {}).get("metadata") or {}).get("main_package") or {}
        ver = main.get("package_version")
        if ver:
            out[name] = str(ver)
    return out


def uv_tool_versions():
    uv = shutil.which("uv")
    if not uv:
        return {}
    cp = run([uv, "tool", "list"])
    if not cp or cp.returncode:
        return {}
    out = {}
    # Typical form: "ruff v0.14.0" followed by executable bullets.
    for line in cp.stdout.splitlines():
        m = re.match(r"^([A-Za-z0-9_.-]+)\s+v?(\d+(?:\.\d+){1,3}(?:[^\s]*)?)\s*$", line.strip())
        if m:
            out[m.group(1).lower()] = m.group(2)
    return out


def installed_package_version(name, uv_tools, pipx_tools):
    return uv_tools.get(name.lower()) or pipx_tools.get(name)


def package_manager_hint(uv_tools, pipx_tools, package_name):
    if package_name.lower() in uv_tools:
        return "uv"
    if package_name in pipx_tools:
        return "pipx"
    return None


def probe():
    tool_names = [
        "git",
        "node",
        "npm",
        "npx",
        "rokit",
        "rojo",
        "stylua",
        "selene",
        "gh",
        "uv",
        "uvx",
        "pipx",
        "graphify",
        "mcp-for-blender",
        "blender-mcp",  # legacy compatibility detection only
        "luau",
        "lune",
    ]
    tools = {name: version(name) for name in tool_names}

    blender_path = locate_blender()
    if blender_path:
        cp = run([blender_path, "--version"])
        raw = (((cp.stdout or "") + " " + (cp.stderr or "")).strip()[:500]) if cp else ""
        tools["blender"] = {
            "found": True,
            "path": blender_path,
            "version_output": raw,
            "exit_code": cp.returncode if cp else None,
        }
    else:
        tools["blender"] = {"found": False, "path": None, "version_output": None}

    uv_tools = uv_tool_versions()
    pipx_tools = pipx_versions()
    py = python_candidates()
    py_ok = suitable_python(py)
    skill_lock_present = (ROOT / "08_TOOLCHAIN/SKILL_LOCK.json").is_file()
    skill_resolution_ready = bool(skill_lock_present or (tools["node"]["found"] and tools["npx"]["found"]))

    graph_pkg = installed_package_version("graphifyy", uv_tools, pipx_tools)
    blender_pkg = installed_package_version("mcp-for-blender", uv_tools, pipx_tools)
    if graph_pkg:
        tools["graphify"]["package_version"] = graph_pkg
        tools["graphify"]["installed_by"] = package_manager_hint(uv_tools, pipx_tools, "graphifyy")
    if blender_pkg:
        tools["mcp-for-blender"]["package_version"] = blender_pkg
        tools["mcp-for-blender"]["installed_by"] = package_manager_hint(uv_tools, pipx_tools, "mcp-for-blender")

    core_versions = {"rojo": "7.7.0", "stylua": "2.5.2", "selene": "0.31.0"}
    core_ok = (
        bool(tools["git"]["found"])
        and bool(py_ok)
        and all(tools[name]["found"] and wanted in (tools[name]["version_output"] or "") for name, wanted in core_versions.items())
    )

    graph_cli_version = semver(tools["graphify"]["version_output"])
    graph_ok = bool(
        tools["graphify"]["found"]
        and (
            graph_pkg == GRAPHIFY_VERSION
            or (graph_cli_version and graph_cli_version[:3] == semver(GRAPHIFY_VERSION))
        )
    )

    blender_ver = semver(tools["blender"]["version_output"])
    blender_app_ok = bool(tools["blender"]["found"] and blender_ver and blender_ver >= BLENDER_MIN)
    blender_cli_version = semver(tools["mcp-for-blender"]["version_output"])
    blender_mcp_ok = bool(
        tools["mcp-for-blender"]["found"]
        and (
            blender_pkg == BLENDER_MCP_VERSION
            or (blender_cli_version and blender_cli_version[:3] == semver(BLENDER_MCP_VERSION))
        )
    )
    creative_cli_ok = bool(blender_app_ok and blender_mcp_ok and py_ok)

    try:
        from bloxmaps_adapter import status as bloxmaps_status
        blox = bloxmaps_status()
    except Exception as exc:
        blox = {"mapgen_ready": False, "issues": [f"BloxMaps adapter probe failed: {exc}"]}

    readiness = {
        "CORE_READY": bool(core_ok),
        "GITHUB_CLI_READY": bool(tools["gh"]["found"]),
        "SKILL_RESOLUTION_READY": skill_resolution_ready,
        "GRAPH_READY": bool(graph_ok),
        "CREATIVE_CLI_READY": bool(creative_cli_ok),
        "BLOXMAPS_READY": bool(blox.get("mapgen_ready")),
        "BLENDER_MCP_RUNTIME_REGISTRATION": "PENDING_MANUAL" if creative_cli_ok else "BLOCKED_BY_CLI_PREREQUISITES",
        "BLENDER_ADDON_LIVE_VERIFICATION": "PENDING_MANUAL" if creative_cli_ok else "BLOCKED_BY_CLI_PREREQUISITES",
        "STUDIO_LIVE_VERIFICATION": "DEFERRED_UNTIL_REQUIRED",
    }

    fixes = []
    py_display = py_ok["executable"] if py_ok else "<python>=3.10"
    isolated_installer = "uv" if tools["uv"]["found"] else ("pipx" if tools["pipx"]["found"] else None)
    if not isolated_installer:
        fixes.append(
            "Install uv (preferred) or pipx once using official platform instructions, then open a new shell. "
            "The bootstrap never installs a package manager silently."
        )

    if graph_pkg == GRAPHIFY_VERSION and not tools["graphify"]["found"]:
        manager = package_manager_hint(uv_tools, pipx_tools, "graphifyy")
        fixes.append(
            "Graphify is installed but its CLI is not on PATH. "
            + ("Run `uv tool update-shell`, open a new shell, then rerun doctor." if manager == "uv" else "Run `pipx ensurepath`, open a new shell, then rerun doctor.")
        )
    elif not graph_ok:
        fixes.append(
            f'Graphify recommended: `uv tool install --force --python "{py_display}" "{GRAPHIFY_PACKAGE}"` '
            f'or pipx fallback `pipx install --force --python "{py_display}" "{GRAPHIFY_PACKAGE}"`.'
        )

    if not blender_app_ok:
        fixes.append(
            "Install/upgrade Blender >=4.2 manually from an approved source. "
            "Set BLENDER_PATH if Blender is installed but not discoverable."
        )

    if not py_ok:
        fixes.append("Install Python >=3.10 manually and rerun doctor; the bootstrap will not install Python silently.")

    if blender_pkg == BLENDER_MCP_VERSION and not tools["mcp-for-blender"]["found"]:
        manager = package_manager_hint(uv_tools, pipx_tools, "mcp-for-blender")
        fixes.append(
            "MCP for Blender is installed but its CLI is not on PATH. "
            + ("Run `uv tool update-shell`, open a new shell, then rerun doctor." if manager == "uv" else "Run `pipx ensurepath`, open a new shell, then rerun doctor.")
        )
    elif not blender_mcp_ok:
        fixes.append(
            f'Priority Blender authoring tool: `uv tool install --force --python "{py_display}" "{BLENDER_MCP_PACKAGE}"` '
            f'or pipx fallback `pipx install --force --python "{py_display}" "{BLENDER_MCP_PACKAGE}"`.'
        )

    if tools["blender-mcp"]["found"] and not tools["mcp-for-blender"]["found"]:
        fixes.append(
            "Legacy `blender-mcp` CLI detected. New bootstrap installs use `mcp-for-blender==2.1.3`; "
            "keep legacy only if another project depends on it, otherwise migrate deliberately."
        )

    if not blox.get("mapgen_ready"):
        details = "; ".join(blox.get("issues") or [])
        fixes.append(
            "BloxMaps world-generation capability pending. Review `08_TOOLCHAIN/BLOXMAPS_SETUP.md`; "
            "after approval run `python scripts/bloxmaps_adapter.py install --confirm`, ensure Python >=3.11 + Luau CLI, then run its smoke test."
            + (f" Current: {details}" if details else "")
        )

    if not tools["gh"]["found"]:
        fixes.append("GitHub CLI (`gh`) is recommended for automatic Issue/PR creation and verification. Without it, create/verify Issues and draft PRs manually as the workflow prompts." )

    if not skill_resolution_ready:
        fixes.append("The reviewed external-skill lock is not present and Node/npx is unavailable. For the first maintainer-only skill resolution, install a current Node LTS that provides npx, then rerun setup. Normal contributors do not need Node once the reviewed skill lock is committed.")

    if not tools["rokit"]["found"]:
        fixes.append("Install Rokit manually from its reviewed official release; then `rokit install` can provision pinned Rojo/StyLua/Selene.")
    if tools["rokit"]["found"] and not core_ok:
        fixes.append("After reviewing the plan, run `python scripts/workstation_doctor.py --install-recommended` to execute `rokit install` and repair pinned Roblox CLI tools.")

    return {
        "schema_version": 2,
        "tools": tools,
        "uv_tools": uv_tools,
        "pipx_packages": pipx_tools,
        "python_candidates": py,
        "selected_python": py_ok,
        "preferred_isolated_installer": isolated_installer,
        "skill_lock_present": skill_lock_present,
        "blender_runtime_defaults": BLENDER_RUNTIME_DEFAULTS,
        "bloxmaps": blox,
        "readiness": readiness,
        "fix_plan": fixes,
    }


def _toml_quote(value):
    return json.dumps(str(value))


def write_runtime_registration_hint(data):
    """Write local, non-authoritative runtime snippets with the resolved absolute CLI path.

    GUI MCP clients often do not inherit the same PATH as the terminal. The doctor therefore
    records a copy/paste-safe absolute executable path after the pinned CLI is actually present,
    without editing any global runtime configuration.
    """
    tool = (data.get("tools") or {}).get("mcp-for-blender") or {}
    command = tool.get("path") if tool.get("found") else None
    target = LOCAL / "BLENDER_MCP_RUNTIME_REGISTRATION.md"
    if not command:
        if target.exists():
            target.unlink()
        return
    env = data.get("blender_runtime_defaults") or BLENDER_RUNTIME_DEFAULTS
    json_snippet = {
        "mcpServers": {
            "blender": {
                "command": command,
                "env": env,
            }
        }
    }
    lines = [
        "# Local Blender MCP runtime registration hint",
        "",
        "Generated by `scripts/workstation_doctor.py` from this workstation. It is local/ignored state.",
        "Use the absolute executable path below for GUI-launched MCP clients to avoid PATH inheritance failures.",
        "Do not commit this file and do not treat registration as live proof; verify the active runtime and Blender target at task time.",
        "",
        "## JSON-style clients",
        "",
        "```json",
        json.dumps(json_snippet, indent=2),
        "```",
        "",
        "## Codex TOML",
        "",
        "```toml",
        "[mcp_servers.blender]",
        f"command = {_toml_quote(command)}",
        "env = { " + ", ".join(f"{k} = {_toml_quote(v)}" for k, v in env.items()) + " }",
        "```",
        "",
        "After registering/restarting the runtime, perform a live capability probe before any Blender mutation.",
        "",
    ]
    target.write_text("\n".join(lines), encoding="utf-8")


def write_report(data):
    LOCAL.mkdir(exist_ok=True)
    (LOCAL / "WORKSTATION_DOCTOR.json").write_text(json.dumps(data, indent=2) + "\n")
    (LOCAL / "WORKSTATION_FIX_PLAN.txt").write_text(
        "No fixes required.\n" if not data["fix_plan"] else "\n".join(f"- {x}" for x in data["fix_plan"]) + "\n"
    )
    write_runtime_registration_hint(data)


def install_isolated(package, python_executable):
    uv = shutil.which("uv")
    pipx = shutil.which("pipx")
    if uv:
        argv = [uv, "tool", "install", "--force", "--python", python_executable, package]
        manager = "uv tool"
    elif pipx:
        argv = [pipx, "install", "--force", "--python", python_executable, package]
        manager = "pipx"
    else:
        raise SystemExit(
            "BLOCKED: neither uv nor pipx is installed. Install uv (preferred) or pipx manually; "
            "no system/package-manager bootstrap is performed automatically."
        )
    cp = subprocess.run(argv, cwd=ROOT, check=False)
    if cp.returncode:
        raise SystemExit(f"BLOCKED: pinned {package} install failed through {manager}")


def install_recommended(data, install_blender_addon=False):
    py = data.get("selected_python")
    if not py:
        raise SystemExit("BLOCKED: Python >=3.10 is required before recommended isolated tools can be installed")

    if not data["readiness"]["GRAPH_READY"]:
        install_isolated(GRAPHIFY_PACKAGE, py["executable"])

    blender_cli_version = semver(data["tools"]["mcp-for-blender"].get("version_output"))
    blender_mcp_current = bool(
        data["tools"]["mcp-for-blender"]["found"]
        and (
            data["tools"]["mcp-for-blender"].get("package_version") == BLENDER_MCP_VERSION
            or (blender_cli_version and blender_cli_version[:3] == semver(BLENDER_MCP_VERSION))
        )
    )
    if not blender_mcp_current:
        install_isolated(BLENDER_MCP_PACKAGE, py["executable"])

    if shutil.which("rokit"):
        cp = subprocess.run(["rokit", "install"], cwd=ROOT, check=False)
        if cp.returncode:
            raise SystemExit("BLOCKED: rokit install failed")

    if install_blender_addon:
        cli = shutil.which("mcp-for-blender")
        if not cli:
            raise SystemExit(
                "BLOCKED: mcp-for-blender CLI is not visible on PATH after install. "
                "Run `uv tool update-shell` or `pipx ensurepath`, open a new shell, then rerun the addon install flag."
            )
        env = dict(os.environ)
        env.update(BLENDER_RUNTIME_DEFAULTS)
        cp = subprocess.run([cli, "install-addon"], cwd=ROOT, env=env, check=False)
        if cp.returncode:
            raise SystemExit("BLOCKED: MCP for Blender addon install failed")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true")
    ap.add_argument(
        "--install-recommended",
        action="store_true",
        help="Explicitly install exact pinned CLI capabilities using already-installed uv (preferred) or pipx, plus Rokit",
    )
    ap.add_argument(
        "--install-blender-addon",
        action="store_true",
        help="Also run `mcp-for-blender install-addon`; requires --install-recommended",
    )
    args = ap.parse_args()
    if args.install_blender_addon and not args.install_recommended:
        ap.error("--install-blender-addon requires --install-recommended")

    data = probe()
    write_report(data)
    if args.install_recommended:
        install_recommended(data, args.install_blender_addon)
        data = probe()
        write_report(data)

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print("WORKSTATION DOCTOR")
        for key, value in data["readiness"].items():
            print(f"{key}: {value}")
        print("BLENDER MCP DEFAULTS: localhost + safe mode ON + telemetry disabled")
        if data["fix_plan"]:
            print("\nNEXT FIXES")
            for item in data["fix_plan"]:
                print("- " + item)
        print("\nNo system dependency was installed unless an explicit install flag was supplied.")
    return 0 if data["readiness"]["CORE_READY"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
