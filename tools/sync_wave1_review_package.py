#!/usr/bin/env python3
"""Thin wrapper — delegates to sync_review_package.py --package wave1.

Kept for backward compatibility. Prefer:
    python3 tools/sync_review_package.py --package wave1
"""

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GENERIC = REPO_ROOT / "tools" / "sync_review_package.py"

args = [sys.executable, str(GENERIC), "--package", "wave1"]
if "--check" in sys.argv:
    args.append("--check")

os.chdir(REPO_ROOT)
sys.exit(subprocess.run(args).returncode)
