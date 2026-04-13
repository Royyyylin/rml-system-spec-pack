#!/usr/bin/env python3
"""Sync Wave 1 diagram review package from d2 sources.

Build mode (default):
    python3 tools/sync_wave1_review_package.py

Check mode (CI-friendly, no writes):
    python3 tools/sync_wave1_review_package.py --check
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "tools" / "wave1_manifest.json"
REVIEW_DIR = REPO_ROOT / "docs" / "handoffs" / "2026-04-13-wave-1-diagram-review"
CONTRACT_CHECKER = REPO_ROOT / "tools" / "check_diagram_contract.py"


def load_manifest():
    with open(MANIFEST) as f:
        return json.load(f)


def run_contract_check(entries):
    """Run diagram contract lint on all source files."""
    result = subprocess.run(
        [sys.executable, str(CONTRACT_CHECKER)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    failed = []
    for line in result.stdout.splitlines():
        if line.startswith("FAIL"):
            failed.append(line)
    return failed


def render_d2(source, output, fmt="svg", scale=None):
    """Render a d2 source to svg or png."""
    cmd = ["d2", str(source), str(output)]
    if scale:
        cmd.extend(["--scale", str(scale)])
    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(REPO_ROOT)
    )
    if result.returncode != 0:
        print(f"  ERROR rendering {source} -> {output}: {result.stderr.strip()}")
        return False
    return True


def generate_drawio(png_path, title, focus):
    """Generate a drawio XML string with embedded PNG."""
    with open(png_path, "rb") as f:
        png_data = f.read()

    # Get dimensions via PNG header (IHDR chunk)
    # Width at bytes 16-19, height at bytes 20-23 (big-endian)
    w = int.from_bytes(png_data[16:20], "big")
    h = int.from_bytes(png_data[20:24], "big")
    # Display at half size (rendered at 2x)
    sw = w // 2
    sh = h // 2

    b64 = base64.b64encode(png_data).decode("ascii")
    data_uri = f"data:image/png;base64,{b64}"
    title_esc = urllib.parse.quote(f"<b>{title}</b>", safe="<>/=")
    focus_esc = urllib.parse.quote(focus, safe="<>/=:")

    return f'''<mxfile host="app.diagrams.net" type="device">
<diagram name="{title}" id="page-0">
  <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="0" arrows="0" fold="0" page="1" pageScale="1" pageWidth="1600" pageHeight="1100" math="0" shadow="0">
    <root>
      <mxCell id="0"/>
      <mxCell id="1" parent="0"/>
      <mxCell id="title" value="{title_esc}" style="text;html=1;fontSize=18;fontStyle=1;align=left;verticalAlign=top;whiteSpace=wrap;" vertex="1" parent="1">
        <mxGeometry x="40" y="10" width="800" height="30" as="geometry"/>
      </mxCell>
      <mxCell id="focus" value="{focus_esc}" style="text;html=1;fontSize=12;fontStyle=2;align=left;verticalAlign=top;whiteSpace=wrap;fontColor=#666666;" vertex="1" parent="1">
        <mxGeometry x="40" y="45" width="800" height="25" as="geometry"/>
      </mxCell>
      <mxCell id="img" value="" style="shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image={data_uri};" vertex="1" parent="1">
        <mxGeometry x="40" y="80" width="{sw}" height="{sh}" as="geometry"/>
      </mxCell>
    </root>
  </mxGraphModel>
</diagram>
</mxfile>'''


def generate_readme(entries):
    """Generate the review package README.md."""
    lines = [
        "# Wave 1 Diagram Review",
        "",
        "本資料夾包含 3 張 Wave 1 核心圖的 review 用 drawio 檔。",
        "",
        "| # | 標題 | 先看什麼 | Source | Render | Review |",
        "|---|------|---------|--------|--------|--------|",
    ]
    for e in entries:
        drawio_basename = Path(e["drawio"]).name
        lines.append(
            f'| {e["id"]} | {e["title"]} | {e["focus"]} '
            f'| `{e["source_name"]}` | `{e["render_name"]}` '
            f"| [{drawio_basename}]({drawio_basename}) |"
        )
    lines.append("")
    return "\n".join(lines)


def content_matches(path, content):
    """Check if file exists and has identical content."""
    if not path.exists():
        return False
    if isinstance(content, str):
        content = content.encode("utf-8")
    return path.read_bytes() == content


def build(entries):
    """Full build: lint, render, generate drawio + README."""
    errors = []

    # 1. Contract check
    print("Checking diagram contracts...")
    failed = run_contract_check(entries)
    if failed:
        for line in failed:
            print(f"  {line}")
        errors.extend(failed)
        print("  Contract check FAILED — continuing with render anyway")
    else:
        print("  All contracts PASS")

    # 2. Render SVG + PNG
    for e in entries:
        src = REPO_ROOT / e["source"]
        svg_out = REPO_ROOT / e["svg"]
        png_out = REPO_ROOT / e["png"]

        print(f"Rendering {e['source']}...")
        if not render_d2(src, svg_out):
            errors.append(f"SVG render failed: {e['source']}")
        if not render_d2(src, png_out, scale=2):
            errors.append(f"PNG render failed: {e['source']}")

    # 3. Generate drawio files
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    for e in entries:
        png_path = REPO_ROOT / e["png"]
        drawio_path = REPO_ROOT / e["drawio"]
        if not png_path.exists():
            errors.append(f"PNG missing, cannot generate drawio: {e['png']}")
            continue
        print(f"Generating {e['drawio']}...")
        content = generate_drawio(png_path, e["title"], e["focus"])
        drawio_path.write_text(content, encoding="utf-8")

    # 4. Generate README
    readme_path = REVIEW_DIR / "README.md"
    print(f"Generating {readme_path.relative_to(REPO_ROOT)}...")
    readme_content = generate_readme(entries)
    readme_path.write_text(readme_content, encoding="utf-8")

    if errors:
        print(f"\nBuild completed with {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("\nBuild OK")
    return 0


def check(entries):
    """Check mode: verify all targets exist and match expected content."""
    stale = []

    # 1. Contract check
    failed = run_contract_check(entries)
    if failed:
        for line in failed:
            stale.append(f"contract: {line}")

    # 2. Check renders exist
    for e in entries:
        for key in ("svg", "png"):
            p = REPO_ROOT / e[key]
            if not p.exists():
                stale.append(f"missing: {e[key]}")

    # 3. Check drawio content matches what would be generated
    for e in entries:
        drawio_path = REPO_ROOT / e["drawio"]
        png_path = REPO_ROOT / e["png"]
        if not drawio_path.exists():
            stale.append(f"missing: {e['drawio']}")
            continue
        if not png_path.exists():
            stale.append(f"cannot verify drawio (PNG missing): {e['png']}")
            continue
        expected = generate_drawio(png_path, e["title"], e["focus"])
        if not content_matches(drawio_path, expected):
            stale.append(f"content drift: {e['drawio']}")

    # 4. Check README
    readme_path = REVIEW_DIR / "README.md"
    expected_readme = generate_readme(entries)
    if not content_matches(readme_path, expected_readme):
        stale.append(f"content drift: {readme_path.relative_to(REPO_ROOT)}")

    if stale:
        print(f"CHECK FAILED — {len(stale)} issue(s):")
        for s in stale:
            print(f"  - {s}")
        return 1
    print("CHECK OK — all targets up to date")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check mode: verify targets without writing files",
    )
    args = parser.parse_args()

    os.chdir(REPO_ROOT)
    entries = load_manifest()

    if args.check:
        sys.exit(check(entries))
    else:
        sys.exit(build(entries))


if __name__ == "__main__":
    main()
