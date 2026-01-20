#!/usr/bin/env python3
"""
List per-plugin versions across the monorepo.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from bump_version import VersionBumper, setup_encoding

def main():
    setup_encoding()
    script_dir = Path(__file__).parent.resolve()
    repo_root = script_dir.parent.parent.parent.parent

    print("Plugin versions:\n")

    try:
        bumper = VersionBumper(repo_root)
        versions = bumper.get_plugin_versions()

        for name, version in versions.items():
            print(f"  {name}: {version}")

        print(f"\nTotal: {len(versions)} plugins")

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
