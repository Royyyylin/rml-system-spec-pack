#!/usr/bin/env python3
"""Scan firmware/app/central + spec-pack for deprecated terms (DEPRECATED_PATTERNS regex).

Coverage: source files matching INCLUDE_EXT (markdown / python / dart / C / yaml / typescript / javascript / C++).
Skips: directories in EXCLUDE_DIRS (archive, .git, .claude, build artifacts, etc.) and files in EXCLUDE_FILES (this script, CLAUDE.md, ubiquitous-language.md, capability-map.md migration mapping table, ADR-013).

Canonical alignment check (term registration in `01_context-scope/ubiquitous-language.md`) is NOT implemented — see Phase K6 backlog (K6-009 test fixtures + K6-010 audit pattern accumulator). The UBIQUITOUS_LANG existence sanity check is retained as warning-only sentinel.

Fail (exit 1) if any deprecated term used in non-archive non-EXCLUDE_FILES context. Blocking mode active 2026-04-25. ADR-013 (2026-04-27) added 6 RML opaque ID prefix patterns.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SPEC_PACK = Path(__file__).resolve().parent.parent
UBIQUITOUS_LANG = SPEC_PACK / "01_context-scope" / "ubiquitous-language.md"

# Deprecated terms — must NOT appear in non-archive context
# Each tuple: (regex_pattern, human_readable_reason)
# Note: S-\d+ / X-\d+ patterns use negative lookbehind to avoid matching
# legitimate REQ domain prefix occurrences like REQ-S-001 / REQ-X-001.
#
# RML opaque ID schema (OBJ/INT/CST/RSK/ACT/ROL/CAP/OWN/HOF/AUT/SCP) deprecated by
# task-b L3 refactor (2026-04-27) per ADR-013. Use name-canonical primary key +
# chapter-position-canonical (per Backstage / C4 / arc42 reference). Cross-ref by
# `file.md#section-anchor`, NOT opaque ID prefix.
DEPRECATED_PATTERNS: list[tuple[str, str]] = [
    (r"\bRML-FEA-\d+\b", "use FEA-NNN- prefix instead"),
    (r"(?<!REQ-)\bS-\d+\b", "use F-NN or FEA-NNN prefix instead"),
    (r"(?<!REQ-)\bX-\d+\b", "use chapter-scoped ID instead (e.g. x1-)"),
    (r"shared-spec/", "use arc42 chapter path (e.g. 01_context-scope/) instead"),
    (r"\bRML-OBJ-\d+\b", "廢 ADR-013 — use Strategic Goal name in system-intent.md#strategic-goals"),
    (r"\bRML-INT-\d+\b", "廢 ADR-013 — use System Intent name in system-intent.md#system-intent"),
    (r"\bRML-CST-\d+\b", "廢 ADR-013 — use Engineering Invariant name in system-intent.md#engineering-invariants (architectural) or constraints.md (legal/regulatory)"),
    (r"\bRML-RSK-\d+\b", "廢 ADR-013 — use risk name in 99_appendix/risks-and-debt.md"),
    (r"\bRML-(ACT|ROL)-\d+\b", "廢 ADR-013 — use unified role name in stakeholders.md (human/AI roles) or bounded-context-map.md System Actors (system entities)"),
    (r"\bRML-(CAP|OWN|HOF|AUT|SCP)-\d+\b", "廢 ADR-013 — use TOGAF capability-name / DDD aggregate root name in 02_solution-strategy/capability-map.md"),
]

# Cross-repo paths (4 repo) — default when no --repo arg is given
DEFAULT_TARGET_REPOS: list[Path] = [
    SPEC_PACK,
    SPEC_PACK.parent / "ble_qos_demo_V1.2m",
    SPEC_PACK.parent / "ble_qos_app",
    SPEC_PACK.parent / "central-device-metadata",
]

# Dirs to skip during scan
EXCLUDE_DIRS: set[str] = {
    ".git",
    "archive",
    "handoffs",  # historical handoff docs — intentional legacy references
    ".claude",
    "node_modules",
    ".code-review-graph",
    ".venv",
    "__pycache__",
    "build",
    ".dart_tool",
    "renders",
}

# Files to skip — intentional references (e.g. vocabulary canonical list, this script itself)
EXCLUDE_FILES: set[str] = {
    "check_vocabulary_alignment.py",  # this file — patterns appear as regex strings
    "CLAUDE.md",  # vocabulary canonical list — deprecated terms appear as intentional reference
    "ubiquitous-language.md",  # DDD canonical vocabulary — Spec ID Naming table shows legacy prefixes as examples
    "capability-map.md",  # contains the canonical "## ID Schema Migration Mapping" preamble — RML-CAP/OWN/HOF appear as Legacy ID column entries by design (per ADR-013)
    "ADR-013-rml-schema-cleanup-l3.md",  # ADR-013 itself documents the deprecated patterns as reference
}

# File extensions to scan
INCLUDE_EXT: set[str] = {
    ".md",
    ".py",
    ".dart",
    ".c",
    ".cc",
    ".cpp",
    ".h",
    ".hpp",
    ".js",
    ".ts",
    ".tsx",
    ".yaml",
    ".yml",
}


def is_excluded(path: Path) -> bool:
    """Return True if any part of the path is in EXCLUDE_DIRS or filename is in EXCLUDE_FILES."""
    if any(part in EXCLUDE_DIRS for part in path.parts):
        return True
    return path.name in EXCLUDE_FILES


def scan_repo(repo: Path) -> list[str]:
    """Scan all eligible files in repo for deprecated terms."""
    violations: list[str] = []
    if not repo.exists():
        print(
            f"WARNING: skipping non-existent repo: {repo}",
            file=sys.stderr,
        )
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
    parser = argparse.ArgumentParser(
        description="Check cross-repo vocabulary alignment vs spec-pack ubiquitous-language.md."
    )
    parser.add_argument(
        "--repo",
        metavar="PATH",
        action="append",
        dest="repos",
        help="Repo path to scan. May be given multiple times. Default: all 4 repos.",
    )
    args = parser.parse_args()

    target_repos: list[Path] = (
        [Path(r).resolve() for r in args.repos] if args.repos else DEFAULT_TARGET_REPOS
    )

    check_ubiquitous_lang_exists()

    all_violations: list[str] = []
    for repo in target_repos:
        violations = scan_repo(repo)
        all_violations.extend(violations)

    if all_violations:
        print(
            f"ERROR: Vocabulary alignment violations ({len(all_violations)}):",
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
            "\nFix deprecated terms per CLAUDE.md Vocabulary Canonical List.",
            file=sys.stderr,
        )
        sys.exit(1)

    print("Vocabulary alignment OK")
    sys.exit(0)


if __name__ == "__main__":
    main()
