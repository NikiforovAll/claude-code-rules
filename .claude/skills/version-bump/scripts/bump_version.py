#!/usr/bin/env python3
"""
Version Bump Script for Claude Code Handbook Monorepo

This script manages version bumping across the monorepo by:
- Reading current versions from marketplace.json and plugin.json files
- Validating version consistency across all files
- Bumping the specified version component (major, minor, or patch)
- Updating all version locations atomically

Usage:
    python bump_version.py <bump_type>

    bump_type: major | minor | patch

Examples:
    python bump_version.py patch   # 1.0.0 -> 1.0.1
    python bump_version.py minor   # 1.0.0 -> 1.1.0
    python bump_version.py major   # 1.0.0 -> 2.0.0
"""

import json
import sys
import io
from pathlib import Path
from typing import Tuple, Dict, List

# Fix encoding issues on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class VersionBumper:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.marketplace_path = repo_root / ".claude-plugin" / "marketplace.json"

    def discover_plugins(self) -> List[Dict]:
        """Discover all plugins from marketplace.json dynamically."""
        marketplace_data = self.read_json(self.marketplace_path)
        plugins = []

        for plugin_entry in marketplace_data.get('plugins', []):
            plugin_name = plugin_entry.get('name')
            source = plugin_entry.get('source')  # e.g., "./plugins/cc-handbook"

            if plugin_name and source:
                # Convert relative path to absolute
                plugin_json_path = self.repo_root / source.lstrip('./') / ".claude-plugin" / "plugin.json"
                plugins.append({
                    'name': plugin_name,
                    'path': plugin_json_path,
                    'marketplace_entry': plugin_entry
                })

        return plugins

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
            raise ValueError(f"Invalid bump type: {bump_type}. Must be 'major', 'minor', or 'patch'")

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
            f.write('\n')  # Add trailing newline

    def validate_consistency(self) -> Dict[str, str]:
        """Validate that all versions are consistent across files."""
        versions = {}

        # Read marketplace.json
        marketplace_data = self.read_json(self.marketplace_path)
        marketplace_version = marketplace_data.get('metadata', {}).get('version')
        if marketplace_version:
            versions['marketplace'] = marketplace_version

        # Read plugin versions from marketplace.json
        for plugin in marketplace_data.get('plugins', []):
            plugin_name = plugin.get('name')
            if plugin_name:
                versions[f'marketplace.plugins.{plugin_name}'] = plugin.get('version')

        # Read individual plugin.json files dynamically
        plugins = self.discover_plugins()
        for plugin_info in plugins:
            plugin_name = plugin_info['name']
            plugin_path = plugin_info['path']

            if plugin_path.exists():
                plugin_data = self.read_json(plugin_path)
                versions[f'{plugin_name}.plugin'] = plugin_data.get('version')
            else:
                print(f"⚠️  Warning: Plugin file not found: {plugin_path}")

        return versions

    def check_version_consistency(self, versions: Dict[str, str]) -> List[str]:
        """Check if all versions are consistent. Returns list of inconsistencies."""
        inconsistencies = []
        version_set = set(versions.values())

        if len(version_set) > 1:
            inconsistencies.append(f"Version mismatch detected:")
            for location, version in versions.items():
                inconsistencies.append(f"  {location}: {version}")

        return inconsistencies

    def perform_bump(self, bump_type: str) -> Dict[str, str]:
        """Perform the version bump across all files."""
        print("Reading current versions...")
        versions = self.validate_consistency()

        # Check consistency
        inconsistencies = self.check_version_consistency(versions)
        if inconsistencies:
            print("\n⚠️  WARNING: Inconsistent versions detected:")
            for msg in inconsistencies:
                print(msg)
            response = input("\nContinue anyway? (y/N): ").strip().lower()
            if response != 'y':
                print("Aborted by user.")
                sys.exit(1)

        # Get current version (use marketplace version as source of truth)
        current_version_str = versions.get('marketplace')
        if not current_version_str:
            raise ValueError("Could not read marketplace version")

        current_version = self.parse_version(current_version_str)
        new_version = self.bump_version(current_version, bump_type)
        new_version_str = self.format_version(*new_version)

        print(f"\nBumping version: {current_version_str} → {new_version_str}")
        print(f"Bump type: {bump_type}")

        # Update all files
        print("\nUpdating files...")

        # Update marketplace.json
        marketplace_data = self.read_json(self.marketplace_path)
        if 'metadata' in marketplace_data and 'version' in marketplace_data['metadata']:
            marketplace_data['metadata']['version'] = new_version_str
        for plugin in marketplace_data.get('plugins', []):
            plugin['version'] = new_version_str
        self.write_json(self.marketplace_path, marketplace_data)
        print(f"✓ Updated {self.marketplace_path}")

        # Update all plugin.json files dynamically
        plugins = self.discover_plugins()
        for plugin_info in plugins:
            plugin_path = plugin_info['path']
            plugin_name = plugin_info['name']

            if plugin_path.exists():
                plugin_data = self.read_json(plugin_path)
                plugin_data['version'] = new_version_str
                self.write_json(plugin_path, plugin_data)
                print(f"✓ Updated {plugin_path}")
            else:
                print(f"⚠️  Warning: Plugin file not found: {plugin_path}")

        # Verify consistency after update
        print("\nVerifying consistency...")
        updated_versions = self.validate_consistency()
        inconsistencies = self.check_version_consistency(updated_versions)

        if inconsistencies:
            raise RuntimeError("Version update failed: versions are still inconsistent after update")

        print(f"✓ All versions successfully updated to {new_version_str}")

        return {
            'old_version': current_version_str,
            'new_version': new_version_str,
            'bump_type': bump_type
        }


def main():
    if len(sys.argv) != 2:
        print("Usage: python bump_version.py <bump_type>")
        print("  bump_type: major | minor | patch")
        sys.exit(1)

    bump_type = sys.argv[1].lower()

    if bump_type not in ['major', 'minor', 'patch']:
        print(f"Error: Invalid bump type '{bump_type}'")
        print("Must be one of: major, minor, patch")
        sys.exit(1)

    # Find repository root (script is in .claude/skills/version-bump/scripts/)
    script_dir = Path(__file__).parent.resolve()
    repo_root = script_dir.parent.parent.parent.parent

    try:
        bumper = VersionBumper(repo_root)
        result = bumper.perform_bump(bump_type)

        print("\n" + "="*60)
        print("Version bump completed successfully!")
        print("="*60)
        print(f"Old version: {result['old_version']}")
        print(f"New version: {result['new_version']}")
        print(f"Bump type:   {result['bump_type']}")
        print("\nNext steps:")
        print("1. Update CHANGELOG.md with the new version entry")
        print("2. Review changes: git diff")
        print("3. Commit changes: git add . && git commit -m 'chore: bump version to {}'".format(result['new_version']))
        print("4. Create tag (optional): git tag v{}".format(result['new_version']))

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()