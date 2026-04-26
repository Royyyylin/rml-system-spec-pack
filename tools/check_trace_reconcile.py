#!/usr/bin/env python3
"""Dual trace_map reconcile advisory check.

Compares spec-pack trace/trace_map.yaml vs upstream workspace
docs/trace_map.yaml (fetched via raw GitHub URL).

Emits ::warning:: on F-04 or SEQ- count drift between the two files.
Exit 0 always (advisory only — never blocks CI).
"""

import sys
import re
import urllib.request
import urllib.error
import os

WORKSPACE_URL = (
    "https://raw.githubusercontent.com/Royyyylin/"
    "ble-qos-demo-workspace/main/docs/trace_map.yaml"
)

SPEC_PACK_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "trace", "trace_map.yaml",
)

PATTERNS = {
    "F-04": re.compile(r"F-04"),
    "SEQ-": re.compile(r"SEQ-"),
}

THRESHOLD = 0  # any count difference triggers warning


def count_patterns(text: str) -> dict:
    return {name: len(pat.findall(text)) for name, pat in PATTERNS.items()}


def fetch_url(url: str) -> str | None:
    """Return content string, or None if fetch fails (advisory)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "trace-reconcile-check/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        print(f"::warning::trace-reconcile: upstream fetch HTTP {exc.code} — {url}")
        return None
    except Exception as exc:  # noqa: BLE001
        print(f"::warning::trace-reconcile: upstream fetch failed — {exc}")
        return None


def load_spec_pack(path: str) -> str | None:
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        print(f"::warning::trace-reconcile: cannot read spec-pack file — {exc}")
        return None


def main() -> int:
    # Load spec-pack local file
    spec_text = load_spec_pack(SPEC_PACK_PATH)
    if spec_text is None:
        print("::warning::trace-reconcile: spec-pack trace_map.yaml unreadable — skipping check")
        return 0

    spec_counts = count_patterns(spec_text)
    print(f"[trace-reconcile] spec-pack counts: {spec_counts}")

    # Fetch workspace upstream
    ws_text = fetch_url(WORKSPACE_URL)
    if ws_text is None:
        # Fetch failed; warning already emitted inside fetch_url
        print("[trace-reconcile] upstream fetch unavailable — advisory check skipped")
        return 0

    ws_counts = count_patterns(ws_text)
    print(f"[trace-reconcile] workspace counts: {ws_counts}")

    # Compare and emit warnings on drift
    drifts = []
    for name in PATTERNS:
        spec_val = spec_counts[name]
        ws_val = ws_counts[name]
        if abs(spec_val - ws_val) > THRESHOLD:
            drifts.append(f"{name} spec-pack={spec_val} workspace={ws_val}")

    if drifts:
        drift_summary = "; ".join(drifts)
        print(f"::warning::trace-reconcile: drift detected — {drift_summary}")
    else:
        print("[trace-reconcile] no drift detected — spec-pack and workspace counts match")

    return 0  # advisory: always exit 0


if __name__ == "__main__":
    sys.exit(main())
