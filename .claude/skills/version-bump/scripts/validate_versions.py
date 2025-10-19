#!/usr/bin/env python3
"""
Quick validation script to check version consistency without making changes.
"""

import sys
from pathlib import Path

# Add the parent directory to path to import bump_version module
sys.path.insert(0, str(Path(__file__).parent))

from bump_version import VersionBumper

def main():
    # Find repository root
    script_dir = Path(__file__).parent.resolve()
    repo_root = script_dir.parent.parent.parent.parent

    print("Validating version consistency...")
    print(f"Repository root: {repo_root}\n")

    try:
        bumper = VersionBumper(repo_root)
        versions = bumper.validate_consistency()

        print("Current versions:")
        for location, version in versions.items():
            print(f"  {location}: {version}")

        inconsistencies = bumper.check_version_consistency(versions)

        if inconsistencies:
            print("\n⚠️  WARNING: Version inconsistencies detected:")
            for msg in inconsistencies:
                print(msg)
            sys.exit(1)
        else:
            print("\n✓ All versions are consistent!")
            sys.exit(0)

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
