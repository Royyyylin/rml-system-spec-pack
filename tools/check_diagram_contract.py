#!/usr/bin/env python3
"""Check AI Diagram Contract blocks in formal .d2/.mmd sources."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN_DIRS = ("shared-spec", "app-spec", "firmware-spec")
SUFFIXES = (".d2", ".mmd")
REQUIRED_KEYS = (
    "ai-diagram",
    "primary_message",
    "reader",
    "template_id",
    "diagram_type",
    "layout",
    "max_nodes",
    "max_groups",
    "keep",
    "avoid",
)
TEMPLATES = {
    "ctx-owner-merge-state": {
        "diagram_types": {"d2-context"},
        "max_nodes": 5,
        "max_groups": 3,
    },
    "ctx-owner-fallback": {
        "diagram_types": {"d2-context"},
        "max_nodes": 5,
        "max_groups": 3,
    },
    "flow-dual-path-feedback": {
        "diagram_types": {"d2-flow"},
        "max_nodes": 5,
        "max_groups": 3,
    },
    "map-source-surface": {
        "diagram_types": {"d2-block"},
        "max_nodes": 8,
        "max_groups": 5,
    },
    "map-service-use": {
        "diagram_types": {"d2-map"},
        "max_nodes": 8,
        "max_groups": 3,
    },
    "state-dual-fsm": {
        "diagram_types": {"stateDiagram-v2"},
        "max_nodes": 10,
        "max_groups": 2,
    },
    "sequence-main-branch": {
        "diagram_types": {"sequenceDiagram"},
        "max_nodes": 8,
        "max_groups": 3,
    },
}
COMMENT_PREFIXES = {
    ".d2": ("#", "//"),
    ".mmd": ("%%",),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate AI Diagram Contract blocks in diagram source files."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Optional diagram files to check. Defaults to shared-spec/app-spec/firmware-spec.",
    )
    return parser.parse_args()


def iter_targets(paths: list[str]) -> list[Path]:
    if paths:
        return [Path(path).resolve() for path in paths]

    targets: list[Path] = []
    for rel_dir in SCAN_DIRS:
        base = ROOT / rel_dir
        for suffix in SUFFIXES:
            targets.extend(sorted(base.rglob(f"*{suffix}")))
    return targets


def strip_comment_prefix(text: str, suffix: str) -> str | None:
    stripped = text.strip()
    for prefix in COMMENT_PREFIXES[suffix]:
        if stripped.startswith(prefix):
            return stripped[len(prefix) :].strip()
    return None


def extract_contract(path: Path) -> dict[str, str]:
    content = path.read_text(encoding="utf-8").splitlines()
    suffix = path.suffix
    block: list[str] = []
    started = False

    for line in content:
        stripped = line.strip()
        if not stripped:
            if started:
                break
            continue

        payload = strip_comment_prefix(line, suffix)
        if payload is None:
            break

        started = True
        block.append(payload)

    contract: dict[str, str] = {}
    for line in block:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        contract[key.strip().lower()] = value.strip()
    return contract


def validate_contract(path: Path) -> list[str]:
    if path.suffix not in COMMENT_PREFIXES:
        return [f"unsupported suffix: {path.suffix}"]
    if not path.exists():
        return ["file does not exist"]

    contract = extract_contract(path)
    errors: list[str] = []

    missing = [key for key in REQUIRED_KEYS if not contract.get(key)]
    if missing:
        errors.append(f"missing keys: {', '.join(missing)}")

    if contract.get("ai-diagram") and contract["ai-diagram"] != "required":
        errors.append("ai-diagram must be 'required'")

    for numeric_key in ("max_nodes", "max_groups"):
        value = contract.get(numeric_key)
        if value and not value.isdigit():
            errors.append(f"{numeric_key} must be an integer")

    template_id = contract.get("template_id")
    if template_id:
        template = TEMPLATES.get(template_id)
        if template is None:
            errors.append(f"unknown template_id: {template_id}")
        else:
            diagram_type = contract.get("diagram_type")
            if diagram_type and diagram_type not in template["diagram_types"]:
                errors.append(
                    f"diagram_type {diagram_type} not allowed for template_id {template_id}"
                )
            for numeric_key in ("max_nodes", "max_groups"):
                value = contract.get(numeric_key)
                if value and value.isdigit():
                    limit = template[numeric_key]
                    if int(value) > limit:
                        errors.append(
                            f"{numeric_key} exceeds template limit {limit} for {template_id}"
                        )

    return errors


def main() -> int:
    args = parse_args()
    failures = 0
    targets = iter_targets(args.paths)

    if not targets:
        print("No diagram sources found.")
        return 0

    for path in targets:
        errors = validate_contract(path)
        rel_path = path.relative_to(ROOT.parent.resolve())
        if errors:
            failures += 1
            print(f"FAIL {rel_path}")
            for error in errors:
                print(f"  - {error}")
            continue
        print(f"PASS {rel_path}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
