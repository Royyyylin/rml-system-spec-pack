#!/usr/bin/env python3
"""Generate a report-only governance summary for spec-pack file changes."""

from __future__ import annotations

import argparse
import fnmatch
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class ManualException:
    rule_id: str
    reason: str
    owner: str = ""
    expires_on: str = ""
    path_glob: str = ""
    source: str = ""


@dataclass
class RuleHit:
    rule_id: str
    severity: str
    trigger_files: list[str]
    required_updates: list[str]
    missing_updates: list[str]
    review_candidates: list[str]
    notes: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a report-only changed-only governance summary."
    )
    parser.add_argument(
        "--changed-file",
        action="append",
        dest="changed_files",
        required=True,
        help="Changed file path. Repeat this flag for multiple files.",
    )
    parser.add_argument(
        "--manual-exception",
        action="append",
        default=[],
        help="Optional exception in RULE_ID:note format. Repeatable.",
    )
    parser.add_argument(
        "--json-out",
        help="Optional path to write the JSON report.",
    )
    parser.add_argument(
        "--exceptions-file",
        type=Path,
        default=None,
        help="Optional YAML-ish exception registry. Defaults to trace/manual_exceptions.yaml if present.",
    )
    parser.add_argument(
        "--spec-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Spec-pack root. Defaults to the parent of this script.",
    )
    return parser


def parse_manual_exception(raw: str) -> ManualException:
    if ":" in raw:
        rule_id, reason = raw.split(":", 1)
    else:
        rule_id, reason = raw, ""
    rule_id = rule_id.strip()
    reason = reason.strip()
    if not rule_id:
        raise ValueError(f"Invalid manual exception: {raw!r}")
    return ManualException(rule_id=rule_id, reason=reason, source="cli")


def normalize_path(raw: str, workspace_root: Path, spec_root: Path) -> str:
    raw_path = Path(raw)
    candidates = []
    if raw_path.is_absolute():
        candidates.append(raw_path)
    else:
        candidates.extend(
            [
                Path.cwd() / raw_path,
                workspace_root / raw_path,
                spec_root / raw_path,
            ]
        )

    workspace_root = workspace_root.resolve()
    for candidate in candidates:
        resolved = candidate.resolve(strict=False)
        try:
            return resolved.relative_to(workspace_root).as_posix()
        except ValueError:
            continue

    normalized = raw_path.as_posix()
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def unique_sorted(items: Iterable[str]) -> list[str]:
    return sorted(set(items))


def parse_scalar(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_key_value(raw: str, path: Path, lineno: int) -> tuple[str, str]:
    if ":" not in raw:
        raise ValueError(f"{path}:{lineno}: expected key: value entry")
    key, value = raw.split(":", 1)
    key = key.strip()
    if not key:
        raise ValueError(f"{path}:{lineno}: missing key")
    return key, parse_scalar(value)


def load_manual_exceptions(
    path: Path | None, workspace_root: Path, spec_root: Path
) -> list[ManualException]:
    if path is None:
        default_path = spec_root / "trace" / "manual_exceptions.yaml"
        path = default_path if default_path.exists() else None
    if path is None:
        return []

    path = path.resolve()
    if not path.exists():
        return []

    lines = path.read_text(encoding="utf-8").splitlines()
    items: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_exceptions = False

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not in_exceptions:
            if stripped == "exceptions: []":
                return []
            if stripped == "exceptions:":
                in_exceptions = True
                continue
            raise ValueError(f"{path}:{lineno}: expected 'exceptions:'")
        if line.startswith("  - "):
            if current is not None:
                items.append(current)
            current = {}
            remainder = line[4:]
            if remainder:
                key, value = parse_key_value(remainder, path, lineno)
                current[key] = value
            continue
        if line.startswith("    "):
            if current is None:
                raise ValueError(f"{path}:{lineno}: field without list item")
            key, value = parse_key_value(line[4:], path, lineno)
            current[key] = value
            continue
        raise ValueError(f"{path}:{lineno}: unsupported structure")

    if current is not None:
        items.append(current)

    source_value = normalize_path(str(path), workspace_root, spec_root)
    exceptions = []
    for item in items:
        rule_id = item.get("rule_id", "").strip()
        if not rule_id:
            raise ValueError(f"{path}: every exception requires rule_id")
        path_glob = item.get("path_glob", "").strip()
        if path_glob:
            path_glob = normalize_path(path_glob, workspace_root, spec_root)
        exceptions.append(
            ManualException(
                rule_id=rule_id,
                reason=item.get("reason", "").strip(),
                owner=item.get("owner", "").strip(),
                expires_on=item.get("expires_on", "").strip(),
                path_glob=path_glob,
                source=source_value,
            )
        )
    return exceptions


def applicable_exceptions(
    manual_exceptions: list[ManualException], rule_id: str, paths: Iterable[str]
) -> list[ManualException]:
    trigger_paths = list(paths)
    matches = []
    for item in manual_exceptions:
        if item.rule_id != rule_id:
            continue
        if item.path_glob and not any(
            fnmatch.fnmatch(path, item.path_glob) for path in trigger_paths
        ):
            continue
        matches.append(item)
    return matches


def build_report(
    changed_files: list[str], manual_exceptions: list[ManualException], spec_root: Path
) -> dict:
    spec_root = spec_root.resolve()
    workspace_root = spec_root.parent.resolve()
    spec_pack_name = spec_root.name
    spec_prefix = f"{spec_pack_name}/"
    changed_files = unique_sorted(
        normalize_path(item, workspace_root, spec_root) for item in changed_files
    )
    changed_set = set(changed_files)

    ble_api = "ble_qos_demo_V1.2m/ble_api.yaml"
    packet_contract = f"{spec_prefix}firmware-spec/packet_contract.md"
    packet_diagram = f"{spec_prefix}firmware-spec/packet_diagram.d2"
    diagram_to_doc = {
        f"{spec_prefix}app-spec/block_diagram.d2": f"{spec_prefix}app-spec/architecture.md",
        f"{spec_prefix}app-spec/state_diagram.mmd": f"{spec_prefix}app-spec/state_machine.md",
        f"{spec_prefix}app-spec/sequence_diagram.mmd": f"{spec_prefix}app-spec/sequence_flows.md",
        f"{spec_prefix}firmware-spec/packet_diagram.d2": f"{spec_prefix}firmware-spec/packet_contract.md",
    }
    render_prefix = f"{spec_prefix}renders/"
    source_prefixes = (
        f"{spec_prefix}shared-spec/",
        f"{spec_prefix}app-spec/",
        f"{spec_prefix}firmware-spec/",
        f"{spec_prefix}trace/",
        f"{spec_prefix}docs/",
    )

    rule_hits: list[RuleHit] = []
    applied_exception_keys: set[tuple[str, str, str, str, str, str]] = set()

    def remember_applied(exceptions: list[ManualException]) -> None:
        for item in exceptions:
            applied_exception_keys.add(
                (
                    item.rule_id,
                    item.reason,
                    item.owner,
                    item.expires_on,
                    item.path_glob,
                    item.source,
                )
            )

    if ble_api in changed_set:
        required_updates = [packet_contract, packet_diagram]
        missing_updates = [path for path in required_updates if path not in changed_set]
        review_candidates = [
            f"{spec_prefix}app-spec/sequence_flows.md",
            f"{spec_prefix}app-spec/acceptance_criteria.md",
            f"{spec_prefix}app-spec/test_cases.md",
            f"{spec_prefix}shared-spec/requirements.md",
            f"{spec_prefix}app-spec/architecture.md",
        ]
        rule_exceptions = applicable_exceptions(manual_exceptions, "CIR-003", [ble_api])
        if missing_updates and rule_exceptions:
            severity = "info"
            remember_applied(rule_exceptions)
            notes = "ble_api.yaml fan-out exception accepted by manual registry or CLI override."
        elif missing_updates:
            severity = "warn"
            notes = "ble_api.yaml changed without all required packet artifacts."
        else:
            severity = "info"
            notes = "ble_api.yaml fan-out satisfied for required packet artifacts; review candidates remain."
        rule_hits.append(
            RuleHit(
                rule_id="CIR-003",
                severity=severity,
                trigger_files=[ble_api],
                required_updates=required_updates,
                missing_updates=missing_updates,
                review_candidates=[path for path in review_candidates if path not in changed_set],
                notes=notes,
            )
        )

    changed_diagrams = [path for path in diagram_to_doc if path in changed_set]
    if changed_diagrams:
        required_updates = unique_sorted(diagram_to_doc[path] for path in changed_diagrams)
        missing_updates = [path for path in required_updates if path not in changed_set]
        rule_exceptions = applicable_exceptions(manual_exceptions, "CIR-008", changed_diagrams)
        if missing_updates and rule_exceptions:
            severity = "info"
            remember_applied(rule_exceptions)
            notes = "Diagram/prose fan-out exception accepted by manual registry or CLI override."
        elif missing_updates:
            severity = "warn"
            notes = "Diagram source changed without matching prose update."
        else:
            severity = "info"
            notes = "Diagram source and prose moved together. Render artifact check is deferred until a render pipeline exists."
        rule_hits.append(
            RuleHit(
                rule_id="CIR-008",
                severity=severity,
                trigger_files=changed_diagrams,
                required_updates=required_updates,
                missing_updates=missing_updates,
                review_candidates=[],
                notes=notes,
            )
        )

    changed_renders = [path for path in changed_files if path.startswith(render_prefix)]
    if changed_renders:
        has_matching_source = any(
            path.startswith(source_prefixes) and not path.startswith(render_prefix)
            for path in changed_files
        )
        rule_exceptions = applicable_exceptions(manual_exceptions, "CIR-009", changed_renders)
        missing_updates = []
        severity = "info"
        notes = ""
        if not has_matching_source and not rule_exceptions:
            missing_updates = ["matching source artifact or documented temporary exception"]
            severity = "warn"
            notes = "Render-only diff detected without source change or exception."
        elif rule_exceptions:
            remember_applied(rule_exceptions)
            notes = "Render-only diff accepted by manual exception."
        else:
            notes = "Render artifacts changed with at least one source artifact."
        rule_hits.append(
            RuleHit(
                rule_id="CIR-009",
                severity=severity,
                trigger_files=changed_renders,
                required_updates=["matching source artifact or documented temporary exception"],
                missing_updates=missing_updates,
                review_candidates=[],
                notes=notes,
            )
        )

    status = "warn" if any(hit.severity == "warn" for hit in rule_hits) else "pass"
    return {
        "version": "1",
        "mode": "report-only",
        "status": status,
        "changed_files": changed_files,
        "rule_hits": [asdict(item) for item in rule_hits],
        "changed_requirements": [],
        "changed_states": [],
        "changed_packets": [],
        "manual_exceptions": [
            {
                "rule_id": key[0],
                "reason": key[1],
                "owner": key[2],
                "expires_on": key[3],
                "path_glob": key[4],
                "source": key[5],
            }
            for key in sorted(applied_exception_keys)
        ],
        "candidate_gate_rules": ["CIR-009"],
    }


def render_text(report: dict) -> str:
    lines = [
        f"Status: {report['status'].upper()}",
        "Changed files:",
    ]
    if report["changed_files"]:
        lines.extend(f"- {path}" for path in report["changed_files"])
    else:
        lines.append("- none")

    lines.append("Rule hits:")
    if report["rule_hits"]:
        for hit in report["rule_hits"]:
            headline = (
                f"- {hit['rule_id']} [{hit['severity']}]: "
                f"{', '.join(hit['trigger_files']) or 'no triggers'}"
            )
            lines.append(headline)
            if hit["missing_updates"]:
                lines.append(
                    f"  missing: {', '.join(hit['missing_updates'])}"
                )
            if hit["review_candidates"]:
                lines.append(
                    f"  review: {', '.join(hit['review_candidates'])}"
                )
            if hit["notes"]:
                lines.append(f"  notes: {hit['notes']}")
    else:
        lines.append("- none")

    lines.append("Manual exceptions:")
    if report["manual_exceptions"]:
        for item in report["manual_exceptions"]:
            detail = f"{item['rule_id']}: {item['reason']}".rstrip(": ")
            meta = []
            if item["owner"]:
                meta.append(f"owner={item['owner']}")
            if item["expires_on"]:
                meta.append(f"expires={item['expires_on']}")
            if item["path_glob"]:
                meta.append(f"path={item['path_glob']}")
            if item["source"]:
                meta.append(f"source={item['source']}")
            if meta:
                detail = f"{detail} ({', '.join(meta)})"
            lines.append(f"- {detail}")
    else:
        lines.append("- none")

    lines.append("Next actions:")
    missing = [
        item
        for hit in report["rule_hits"]
        for item in hit["missing_updates"]
    ]
    if missing:
        lines.extend(f"- {item}" for item in unique_sorted(missing))
    else:
        lines.append("- no immediate missing updates detected")

    return "\n".join(lines)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        spec_root = args.spec_root.resolve()
        workspace_root = spec_root.parent.resolve()
        manual_exceptions = load_manual_exceptions(
            path=args.exceptions_file,
            workspace_root=workspace_root,
            spec_root=spec_root,
        )
        manual_exceptions.extend(parse_manual_exception(item) for item in args.manual_exception)
    except ValueError as exc:
        parser.error(str(exc))

    report = build_report(
        changed_files=args.changed_files,
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
