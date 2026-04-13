#!/usr/bin/env python3
"""Collect changed files from workspace repos and feed changed_only_report."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from changed_only_report import (
    build_report,
    load_manual_exceptions,
    parse_manual_exception,
    render_text,
)


DEFAULT_REPOS = {
    "app": "ble_qos_app",
    "firmware": "ble_qos_demo_V1.2m",
    "central": "central-device-metadata",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Collect git changes from workspace repos and run changed_only_report."
    )
    parser.add_argument(
        "--changed-file",
        action="append",
        default=[],
        help="Additional changed file path, typically for local spec-pack edits.",
    )
    parser.add_argument(
        "--manual-exception",
        action="append",
        default=[],
        help="Optional exception in RULE_ID:reason format. Repeatable.",
    )
    parser.add_argument(
        "--json-out",
        help="Optional path to write the JSON report.",
    )
    parser.add_argument(
        "--exceptions-file",
        type=Path,
        default=None,
        help="Optional manual exception registry. Defaults to trace/manual_exceptions.yaml if present.",
    )
    parser.add_argument(
        "--spec-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Spec-pack root. Defaults to the parent of this script.",
    )
    parser.add_argument(
        "--no-default-repos",
        action="store_true",
        help="Do not auto-collect changes from the three default workspace repos.",
    )
    parser.add_argument(
        "--repo",
        action="append",
        default=[],
        help="Additional repo mapping in name=path form. Path may be absolute or workspace-relative.",
    )
    parser.add_argument(
        "--base-ref",
        action="append",
        default=[],
        help="Optional base ref in name=ref form. Adds committed diff from ref...HEAD for that repo.",
    )
    return parser


def parse_mapping(raw: str, label: str) -> tuple[str, str]:
    if "=" not in raw:
        raise ValueError(f"Invalid {label}: {raw!r}; expected name=value")
    name, value = raw.split("=", 1)
    name = name.strip()
    value = value.strip()
    if not name or not value:
        raise ValueError(f"Invalid {label}: {raw!r}; expected name=value")
    return name, value


def resolve_repo_map(
    spec_root: Path, no_default_repos: bool, repo_args: list[str]
) -> dict[str, Path]:
    workspace_root = spec_root.parent.resolve()
    repo_map: dict[str, Path] = {}
    if not no_default_repos:
        for name, rel_path in DEFAULT_REPOS.items():
            repo_map[name] = (workspace_root / rel_path).resolve()
    for raw in repo_args:
        name, value = parse_mapping(raw, "repo mapping")
        path = Path(value)
        if not path.is_absolute():
            path = (workspace_root / path).resolve()
        repo_map[name] = path
    return repo_map


def resolve_base_refs(raw_items: list[str]) -> dict[str, str]:
    base_refs = {}
    for raw in raw_items:
        name, value = parse_mapping(raw, "base ref")
        base_refs[name] = value
    return base_refs


def run_git(repo_path: Path, args: list[str]) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(repo_path), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def collect_repo_changes(repo_path: Path, repo_label: str, workspace_root: Path) -> list[str]:
    if not (repo_path / ".git").exists():
        raise ValueError(f"Repo '{repo_label}' is not a git repository: {repo_path}")

    rel_prefix = repo_path.resolve().relative_to(workspace_root.resolve()).as_posix()
    paths = set()
    for git_args in (
        ["diff", "--name-only", "--relative", "HEAD"],
        ["diff", "--name-only", "--relative", "--cached"],
        ["ls-files", "--others", "--exclude-standard"],
    ):
        for rel_path in run_git(repo_path, git_args):
            paths.add(f"{rel_prefix}/{rel_path}")
    return sorted(paths)


def collect_base_ref_changes(
    repo_path: Path, repo_label: str, workspace_root: Path, base_ref: str
) -> list[str]:
    if not (repo_path / ".git").exists():
        raise ValueError(f"Repo '{repo_label}' is not a git repository: {repo_path}")

    rel_prefix = repo_path.resolve().relative_to(workspace_root.resolve()).as_posix()
    paths = set()
    for rel_path in run_git(
        repo_path, ["diff", "--name-only", "--relative", f"{base_ref}...HEAD"]
    ):
        paths.add(f"{rel_prefix}/{rel_path}")
    return sorted(paths)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    spec_root = args.spec_root.resolve()
    workspace_root = spec_root.parent.resolve()

    try:
        repo_map = resolve_repo_map(
            spec_root=spec_root,
            no_default_repos=args.no_default_repos,
            repo_args=args.repo,
        )
        base_refs = resolve_base_refs(args.base_ref)
        manual_exceptions = load_manual_exceptions(
            path=args.exceptions_file,
            workspace_root=workspace_root,
            spec_root=spec_root,
        )
        manual_exceptions.extend(parse_manual_exception(item) for item in args.manual_exception)
    except ValueError as exc:
        parser.error(str(exc))

    changed_files = set(args.changed_file)

    try:
        for repo_name, repo_path in repo_map.items():
            changed_files.update(
                collect_repo_changes(
                    repo_path=repo_path,
                    repo_label=repo_name,
                    workspace_root=workspace_root,
                )
            )
            if repo_name in base_refs:
                changed_files.update(
                    collect_base_ref_changes(
                        repo_path=repo_path,
                        repo_label=repo_name,
                        workspace_root=workspace_root,
                        base_ref=base_refs[repo_name],
                    )
                )
    except (ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(2, f"{exc}\n")

    report = build_report(
        changed_files=sorted(changed_files),
        manual_exceptions=manual_exceptions,
        spec_root=spec_root,
    )
    print(render_text(report))

    if args.json_out:
        output_path = Path(args.json_out)
        if not output_path.is_absolute():
            output_path = Path.cwd() / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
