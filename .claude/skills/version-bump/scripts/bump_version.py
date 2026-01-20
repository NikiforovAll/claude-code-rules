#!/usr/bin/env python3
"""
Version Bump Script for Claude Code Handbook Monorepo

Per-plugin version bumping. Each plugin can have independent versions.

Usage:
    python bump_version.py <bump_type> --plugin <name> [--plugin <name2>...]
    python bump_version.py <bump_type> --all

    bump_type: major | minor | patch

Examples:
    python bump_version.py patch --plugin handbook-dotnet
    python bump_version.py minor --plugin handbook --plugin handbook-extras
    python bump_version.py patch --all   # bump all plugins
"""

import argparse
import json
import sys
import io
from pathlib import Path
from typing import Tuple, Dict, List


def setup_encoding():
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class VersionBumper:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.marketplace_path = repo_root / ".claude-plugin" / "marketplace.json"

    def discover_plugins(self) -> List[Dict]:
        """Discover all plugins from marketplace.json."""
        marketplace_data = self.read_json(self.marketplace_path)
        plugins = []

        for plugin_entry in marketplace_data.get('plugins', []):
            plugin_name = plugin_entry.get('name')
            source = plugin_entry.get('source')

            if plugin_name and source:
                plugin_json_path = self.repo_root / source.lstrip('./') / ".claude-plugin" / "plugin.json"
                plugins.append({
                    'name': plugin_name,
                    'path': plugin_json_path,
                    'version': plugin_entry.get('version'),
                    'marketplace_entry': plugin_entry
                })

        return plugins

    def get_plugin_names(self) -> List[str]:
        """Get list of all plugin names."""
        return [p['name'] for p in self.discover_plugins()]

    def parse_version(self, version_str: str) -> Tuple[int, int, int]:
        """Parse semantic version string into (major, minor, patch) tuple."""
        try:
            parts = version_str.split('.')
            if len(parts) != 3:
                raise ValueError(f"Invalid version format: {version_str}")
            return tuple(map(int, parts))
        except (ValueError, AttributeError) as e:
            raise ValueError(f"Failed to parse version '{version_str}': {e}")

    def format_version(self, major: int, minor: int, patch: int) -> str:
        """Format version tuple as string."""
        return f"{major}.{minor}.{patch}"

    def bump_version(self, version: Tuple[int, int, int], bump_type: str) -> Tuple[int, int, int]:
        """Bump version based on type (major, minor, or patch)."""
        major, minor, patch = version

        if bump_type == "major":
            return (major + 1, 0, 0)
        elif bump_type == "minor":
            return (major, minor + 1, 0)
        elif bump_type == "patch":
            return (major, minor, patch + 1)
        else:
            raise ValueError(f"Invalid bump type: {bump_type}")

    def read_json(self, path: Path) -> dict:
        """Read and parse JSON file."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {path}: {e}")

    def write_json(self, path: Path, data: dict):
        """Write JSON data to file with proper formatting."""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')

    def get_plugin_versions(self) -> Dict[str, str]:
        """Get current versions for all plugins."""
        versions = {}
        plugins = self.discover_plugins()
        for p in plugins:
            versions[p['name']] = p['version']
        return versions

    def bump_plugins(self, bump_type: str, plugin_names: List[str]) -> Dict[str, Dict]:
        """Bump versions for specified plugins."""
        plugins = self.discover_plugins()
        plugin_map = {p['name']: p for p in plugins}

        unknown = [n for n in plugin_names if n not in plugin_map]
        if unknown:
            raise ValueError(f"Unknown plugin(s): {', '.join(unknown)}")

        results = {}
        marketplace_data = self.read_json(self.marketplace_path)

        for plugin_name in plugin_names:
            plugin_info = plugin_map[plugin_name]
            current_version_str = plugin_info['version']
            current_version = self.parse_version(current_version_str)
            new_version = self.bump_version(current_version, bump_type)
            new_version_str = self.format_version(*new_version)

            # Update marketplace.json plugin entry
            for entry in marketplace_data.get('plugins', []):
                if entry.get('name') == plugin_name:
                    entry['version'] = new_version_str
                    break

            # Update individual plugin.json
            plugin_path = plugin_info['path']
            if plugin_path.exists():
                plugin_data = self.read_json(plugin_path)
                plugin_data['version'] = new_version_str
                self.write_json(plugin_path, plugin_data)
                print(f"✓ Updated {plugin_path}")

            results[plugin_name] = {
                'old_version': current_version_str,
                'new_version': new_version_str
            }

        self.write_json(self.marketplace_path, marketplace_data)
        print(f"✓ Updated {self.marketplace_path}")

        return results


def main():
    setup_encoding()
    parser = argparse.ArgumentParser(
        description='Bump plugin versions in the Claude Code Handbook monorepo',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python bump_version.py patch --plugin handbook-dotnet
  python bump_version.py minor --plugin handbook --plugin handbook-extras
  python bump_version.py patch --all
"""
    )
    parser.add_argument('bump_type', choices=['major', 'minor', 'patch'],
                        help='Version component to bump')
    parser.add_argument('--plugin', action='append', dest='plugins', metavar='NAME',
                        help='Plugin name to bump (can be repeated)')
    parser.add_argument('--all', action='store_true', dest='bump_all',
                        help='Bump all plugins')

    args = parser.parse_args()

    script_dir = Path(__file__).parent.resolve()
    repo_root = script_dir.parent.parent.parent.parent

    try:
        bumper = VersionBumper(repo_root)
        all_plugins = bumper.get_plugin_names()

        if not args.plugins and not args.bump_all:
            print("Error: Must specify --plugin <name> or --all\n")
            print("Available plugins:")
            versions = bumper.get_plugin_versions()
            for name in all_plugins:
                print(f"  {name}: {versions[name]}")
            sys.exit(1)

        if args.bump_all:
            target_plugins = all_plugins
        else:
            target_plugins = args.plugins

        print(f"Bumping {args.bump_type} version for: {', '.join(target_plugins)}\n")

        results = bumper.bump_plugins(args.bump_type, target_plugins)

        print("\n" + "=" * 60)
        print("Version bump completed!")
        print("=" * 60)
        for plugin_name, info in results.items():
            print(f"  {plugin_name}: {info['old_version']} → {info['new_version']}")
        print("\nNext steps:")
        print("1. Review changes: git diff")
        versions_str = ', '.join(f"{n}={r['new_version']}" for n, r in results.items())
        print(f"2. Commit: git add . && git commit -m 'chore: bump {versions_str}'")

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
