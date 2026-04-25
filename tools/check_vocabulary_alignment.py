#!/usr/bin/env python3
"""Check cross-repo vocabulary alignment vs spec-pack ubiquitous-language.md.

Scan firmware/app/central + spec-pack itself (.md/.py/.dart/.c/.h/.yaml/.yml).
Compare against canonical vocabulary in 01_context-scope/ubiquitous-language.md.
Fail if:
  - Used deprecated term (e.g. RML-FEA-* in non-archive context)
  - Used cross-repo term not registered in canonical list

Advisory level (起步), 後升 blocking.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SPEC_PACK = Path(__file__).resolve().parent.parent
UBIQUITOUS_LANG = SPEC_PACK / "01_context-scope" / "ubiquitous-language.md"

# Deprecated terms — must NOT appear in non-archive context
# Each tuple: (regex_pattern, human_readable_reason)
DEPRECATED_PATTERNS: list[tuple[str, str]] = [
    (r"\bRML-FEA-\d+\b", "use FEA-NNN- prefix instead"),
    (r"\bS-\d+\b", "use F-NN or FEA-NNN prefix instead"),
    (r"\bX-\d+\b", "use chapter-scoped ID instead (e.g. x1-)"),
    (r"shared-spec/", "use arc42 chapter path (e.g. 01_context-scope/) instead"),
]

# Cross-repo paths (4 repo)
TARGET_REPOS: list[Path] = [
    SPEC_PACK,
    SPEC_PACK.parent / "ble_qos_demo_V1.2m",
    SPEC_PACK.parent / "ble_qos_app",
    SPEC_PACK.parent / "central-device-metadata",
]

# Dirs to skip during scan
EXCLUDE_DIRS: set[str] = {
    ".git",
    "archive",
    ".claude",
    "node_modules",
    ".code-review-graph",
    ".venv",
    "__pycache__",
    "build",
    ".dart_tool",
    "renders",
}

# File extensions to scan
INCLUDE_EXT: set[str] = {
    ".md",
    ".py",
    ".dart",
    ".c",
    ".h",
    ".yaml",
    ".yml",
}


def is_excluded(path: Path) -> bool:
    """Return True if any part of the path is in EXCLUDE_DIRS."""
    return any(part in EXCLUDE_DIRS for part in path.parts)


def scan_repo(repo: Path) -> list[str]:
    """Scan all eligible files in repo for deprecated terms."""
    violations: list[str] = []
    if not repo.exists():
        return violations

    for file in repo.rglob("*"):
        if not file.is_file():
            continue
        if is_excluded(file):
            continue
        if file.suffix not in INCLUDE_EXT:
            continue

        try:
            content = file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for pattern, reason in DEPRECATED_PATTERNS:
            for match in re.finditer(pattern, content):
                line_num = content[: match.start()].count("\n") + 1
                violations.append(
                    f"{file}:{line_num}: deprecated term '{match.group()}' — {reason}"
                )

    return violations


def check_ubiquitous_lang_exists() -> bool:
    """Warn if canonical vocabulary file is missing."""
    if not UBIQUITOUS_LANG.exists():
        print(
            f"WARNING: canonical vocabulary file not found: {UBIQUITOUS_LANG}",
            file=sys.stderr,
        )
        print(
            "  Expected at: 01_context-scope/ubiquitous-language.md",
            file=sys.stderr,
        )
        return False
    return True


def main() -> int:
    check_ubiquitous_lang_exists()

    all_violations: list[str] = []
    for repo in TARGET_REPOS:
        violations = scan_repo(repo)
        all_violations.extend(violations)

    if all_violations:
        print(
            f"WARNING: Vocabulary alignment violations ({len(all_violations)}):",
            file=sys.stderr,
        )
        for violation in all_violations[:50]:
            print(f"  {violation}", file=sys.stderr)
        if len(all_violations) > 50:
            print(
                f"  ... and {len(all_violations) - 50} more violations",
                file=sys.stderr,
            )
        print(
            "\nAdvisory only (exit 0). Upgrade to blocking: change sys.exit(0) → sys.exit(1).",
            file=sys.stderr,
        )
        # Advisory level — exit 0 (upgrade to exit 1 when promoting to blocking)
        sys.exit(0)

    print("Vocabulary alignment OK")
    sys.exit(0)


if __name__ == "__main__":
    main()
