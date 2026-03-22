#!/usr/bin/env python3
"""
Discover all plugins in a Claude Code marketplace by scanning the local repo.

Usage:
    discover.py                              # scan cc-handbook marketplace
    discover.py --marketplace <name>         # scan a specific marketplace
    discover.py --repo-root <path>           # scan from explicit path
    discover.py --detailed                   # show component names
    discover.py --json                       # machine-readable output
    discover.py --filter <keyword>           # filter by name/keyword
    discover.py --uninstalled                # only show uninstalled plugins
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

DEFAULT_MARKETPLACE = "cc-handbook"


def find_marketplace_root(marketplace_name):
    """Resolve marketplace root via `claude plugin marketplace list --json`."""
    try:
        result = subprocess.run(
            ["claude", "plugin", "marketplace", "list", "--json"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return None
        marketplaces = json.loads(result.stdout)
        for m in marketplaces:
            if m.get("name") == marketplace_name:
                return Path(m.get("installLocation") or m.get("path", ""))
    except (FileNotFoundError, json.JSONDecodeError, subprocess.TimeoutExpired):
        pass
    return None


def get_installed_plugins(marketplace_name):
    """Return dict of {plugin_name: {"enabled": bool, "version": str}}."""
    installed = {}
    try:
        result = subprocess.run(
            ["claude", "plugin", "list", "--json"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return installed
        data = json.loads(result.stdout)
        plugins_list = data if isinstance(data, list) else data.get("installed", [])
        suffix = f"@{marketplace_name}"
        for p in plugins_list:
            pid = p.get("id", "")
            if pid.endswith(suffix):
                name = pid[: -len(suffix)]
                installed[name] = {
                    "enabled": p.get("enabled", False),
                    "version": p.get("version", ""),
                }
    except (FileNotFoundError, json.JSONDecodeError, subprocess.TimeoutExpired):
        pass
    return installed


def scan_plugin(plugin_dir):
    """Scan a plugin directory and return its metadata + components."""
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    if not manifest_path.exists():
        return None

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None

    components = {
        "skills": [],
        "agents": [],
        "commands": [],
        "mcp_servers": [],
        "lsp_servers": [],
        "hooks": [],
    }

    # Skills
    skills_dir = plugin_dir / "skills"
    if skills_dir.is_dir():
        for skill_dir in sorted(skills_dir.iterdir()):
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                components["skills"].append(skill_dir.name)

    # Agents
    agents_dir = plugin_dir / "agents"
    if agents_dir.is_dir():
        for f in sorted(agents_dir.glob("*.md")):
            components["agents"].append(f.stem)

    # Commands
    commands_dir = plugin_dir / "commands"
    if commands_dir.is_dir():
        for f in sorted(commands_dir.glob("*.md")):
            components["commands"].append(f.stem)

    # MCP servers
    mcp_path = plugin_dir / ".mcp.json"
    if mcp_path.exists():
        try:
            mcp = json.loads(mcp_path.read_text(encoding="utf-8"))
            components["mcp_servers"] = sorted(mcp.get("mcpServers", {}).keys())
        except (json.JSONDecodeError, OSError):
            pass

    # LSP servers
    lsp_path = plugin_dir / ".lsp.json"
    if lsp_path.exists():
        try:
            lsp = json.loads(lsp_path.read_text(encoding="utf-8"))
            components["lsp_servers"] = sorted(lsp.keys())
        except (json.JSONDecodeError, OSError):
            pass

    # Hooks
    hooks_path = plugin_dir / "hooks" / "hooks.json"
    if hooks_path.exists():
        try:
            hooks = json.loads(hooks_path.read_text(encoding="utf-8"))
            components["hooks"] = sorted(hooks.get("hooks", {}).keys())
        except (json.JSONDecodeError, OSError):
            pass

    return {
        "name": manifest.get("name", plugin_dir.name),
        "version": manifest.get("version", "?"),
        "description": manifest.get("description", ""),
        "keywords": manifest.get("keywords", []),
        "components": components,
    }


def status_marker(name, installed_map):
    """Return [+] enabled, [o] disabled, [ ] not installed, [?] unknown."""
    if installed_map is None:
        return "[?]"
    info = installed_map.get(name)
    if info is None:
        return "[ ]"
    return "[+]" if info["enabled"] else "[o]"


def component_summary(components):
    """Return short string like 'S:3 A:1 C:2 M:1'."""
    parts = []
    mapping = [
        ("S", "skills"),
        ("A", "agents"),
        ("C", "commands"),
        ("M", "mcp_servers"),
        ("L", "lsp_servers"),
        ("H", "hooks"),
    ]
    for label, key in mapping:
        count = len(components[key])
        if count > 0:
            parts.append(f"{label}:{count}")
    return " ".join(parts) if parts else "-"


def print_table(plugins, installed_map, detailed=False):
    """Print formatted table output."""
    if not plugins:
        print("No plugins found.")
        return

    # Header
    print(f"\n{'St':>3}  {'Plugin':<32} {'Version':<10} {'Components':<18} Description")
    print(f"{'---':>3}  {'─' * 32} {'─' * 10} {'─' * 18} {'─' * 40}")

    for p in plugins:
        st = status_marker(p["name"], installed_map)
        comp = component_summary(p["components"])
        desc = p["description"][:50]
        print(f"{st:>3}  {p['name']:<32} {p['version']:<10} {comp:<18} {desc}")

        if detailed:
            for label, key in [
                ("skills", "skills"),
                ("agents", "agents"),
                ("commands", "commands"),
                ("mcp", "mcp_servers"),
                ("lsp", "lsp_servers"),
                ("hooks", "hooks"),
            ]:
                items = p["components"][key]
                if items:
                    print(f"       {label}: {', '.join(items)}")

    # Legend
    print(f"\n[+] installed & enabled  [o] installed & disabled  [ ] not installed  [?] unknown")
    print(f"S=skills A=agents C=commands M=mcp L=lsp H=hooks")
    print(f"\nTotal: {len(plugins)} plugins")


def main():
    parser = argparse.ArgumentParser(description="Discover Claude Code marketplace plugins")
    parser.add_argument("--marketplace", "-m", default=DEFAULT_MARKETPLACE, help="Marketplace name (default: cc-handbook)")
    parser.add_argument("--repo-root", "-r", type=Path, help="Explicit path to marketplace repo root")
    parser.add_argument("--detailed", "-d", action="store_true", help="Show component names")
    parser.add_argument("--json", "-j", dest="json_output", action="store_true", help="JSON output")
    parser.add_argument("--filter", "-f", dest="filter_kw", help="Filter by name or keyword")
    parser.add_argument("--uninstalled", "-u", action="store_true", help="Only show uninstalled plugins")
    args = parser.parse_args()

    # Resolve repo root
    root = args.repo_root
    if root is None:
        root = find_marketplace_root(args.marketplace)
    if root is None or not root.exists():
        print(f"Error: Could not find marketplace '{args.marketplace}'.", file=sys.stderr)
        print(f"Try: --repo-root <path> or ensure marketplace is added via `claude plugin marketplace add`", file=sys.stderr)
        sys.exit(1)

    plugins_dir = root / "plugins"
    if not plugins_dir.is_dir():
        print(f"Error: No plugins/ directory found in {root}", file=sys.stderr)
        sys.exit(1)

    # Scan all plugins
    plugins = []
    for d in sorted(plugins_dir.iterdir()):
        if d.is_dir():
            info = scan_plugin(d)
            if info:
                plugins.append(info)

    # Get installed status
    installed_map = get_installed_plugins(args.marketplace)

    # Filter
    if args.filter_kw:
        kw = args.filter_kw.lower()
        plugins = [
            p for p in plugins
            if kw in p["name"].lower()
            or kw in p["description"].lower()
            or any(kw in k.lower() for k in p["keywords"])
        ]

    if args.uninstalled:
        plugins = [p for p in plugins if p["name"] not in installed_map]

    # Output
    if args.json_output:
        output = []
        for p in plugins:
            entry = {**p, "status": status_marker(p["name"], installed_map)}
            if p["name"] in installed_map:
                entry["installed_version"] = installed_map[p["name"]]["version"]
            output.append(entry)
        print(json.dumps(output, indent=2))
    else:
        print_table(plugins, installed_map, detailed=args.detailed)


if __name__ == "__main__":
    main()
