#!/usr/bin/env python3
"""Sync diagram review packages from d2 sources.

Build all packages:
    python3 tools/sync_review_package.py

Build one package:
    python3 tools/sync_review_package.py --package wave1

Check mode (no writes, exit non-zero on drift):
    python3 tools/sync_review_package.py --check
    python3 tools/sync_review_package.py --package wave1 --check

List available packages:
    python3 tools/sync_review_package.py --list
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import urllib.parse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGES_FILE = REPO_ROOT / "tools" / "review_packages.json"
CONTRACT_CHECKER = REPO_ROOT / "tools" / "check_diagram_contract.py"


def load_packages():
    with open(PACKAGES_FILE) as f:
        return json.load(f)["packages"]


def run_contract_check():
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


def render_d2(source, output, scale=None):
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
    with open(png_path, "rb") as f:
        png_data = f.read()

    w = int.from_bytes(png_data[16:20], "big")
    h = int.from_bytes(png_data[20:24], "big")
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


def generate_readme(pkg):
    lines = [
        f"# {pkg['readme_title']}",
        "",
        pkg["readme_description"],
        "",
        "| # | 標題 | 先看什麼 | Source | Render | Review |",
        "|---|------|---------|--------|--------|--------|",
    ]
    for d in pkg["diagrams"]:
        lines.append(
            f'| {d["id"]} | {d["title"]} | {d["focus"]} '
            f'| `{d["source"]}` | `{d["svg"]}` '
            f'| [{d["drawio_name"]}]({d["drawio_name"]}) |'
        )
    lines.append("")
    return "\n".join(lines)


def content_matches(path, content):
    if not path.exists():
        return False
    if isinstance(content, str):
        content = content.encode("utf-8")
    return path.read_bytes() == content


def build_package(pkg_id, pkg):
    print(f"\n=== Building package: {pkg_id} ===")
    errors = []
    review_dir = REPO_ROOT / pkg["review_dir"]

    # 1. Contract check
    print("Checking diagram contracts...")
    failed = run_contract_check()
    if failed:
        for line in failed:
            print(f"  {line}")
        errors.extend(failed)
        print("  Contract check FAILED — continuing with render anyway")
    else:
        print("  All contracts PASS")

    # 2. Render SVG + PNG
    for d in pkg["diagrams"]:
        src = d["source"]
        print(f"Rendering {src}...")
        if not render_d2(src, d["svg"]):
            errors.append(f"SVG render failed: {src}")
        if not render_d2(src, d["png"], scale=2):
            errors.append(f"PNG render failed: {src}")

    # 3. Generate drawio files
    review_dir.mkdir(parents=True, exist_ok=True)
    for d in pkg["diagrams"]:
        png_path = REPO_ROOT / d["png"]
        drawio_path = review_dir / d["drawio_name"]
        if not png_path.exists():
            errors.append(f"PNG missing, cannot generate drawio: {d['png']}")
            continue
        print(f"Generating {drawio_path.relative_to(REPO_ROOT)}...")
        content = generate_drawio(png_path, d["title"], d["focus"])
        drawio_path.write_text(content, encoding="utf-8")

    # 4. Generate README
    readme_path = review_dir / "README.md"
    print(f"Generating {readme_path.relative_to(REPO_ROOT)}...")
    readme_content = generate_readme(pkg)
    readme_path.write_text(readme_content, encoding="utf-8")

    if errors:
        print(f"\nBuild completed with {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        return 1
    print(f"\nBuild OK: {pkg_id}")
    return 0


def check_package(pkg_id, pkg):
    print(f"\n=== Checking package: {pkg_id} ===")
    stale = []
    review_dir = REPO_ROOT / pkg["review_dir"]

    # 1. Contract check
    failed = run_contract_check()
    if failed:
        for line in failed:
            stale.append(f"contract: {line}")

    # 2. Check renders exist
    for d in pkg["diagrams"]:
        for key in ("svg", "png"):
            p = REPO_ROOT / d[key]
            if not p.exists():
                stale.append(f"missing: {d[key]}")

    # 3. Check drawio content
    for d in pkg["diagrams"]:
        drawio_path = review_dir / d["drawio_name"]
        png_path = REPO_ROOT / d["png"]
        if not drawio_path.exists():
            stale.append(f"missing: {drawio_path.relative_to(REPO_ROOT)}")
            continue
        if not png_path.exists():
            stale.append(f"cannot verify drawio (PNG missing): {d['png']}")
            continue
        expected = generate_drawio(png_path, d["title"], d["focus"])
        if not content_matches(drawio_path, expected):
            stale.append(f"content drift: {drawio_path.relative_to(REPO_ROOT)}")

    # 4. Check README
    readme_path = review_dir / "README.md"
    expected_readme = generate_readme(pkg)
    if not content_matches(readme_path, expected_readme):
        stale.append(f"content drift: {readme_path.relative_to(REPO_ROOT)}")

    if stale:
        print(f"CHECK FAILED — {len(stale)} issue(s):")
        for s in stale:
            print(f"  - {s}")
        return 1
    print(f"CHECK OK: {pkg_id}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check mode: verify targets without writing files",
    )
    parser.add_argument(
        "--package",
        metavar="ID",
        help="Only process this package (default: all)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available package IDs and exit",
    )
    args = parser.parse_args()

    os.chdir(REPO_ROOT)
    packages = load_packages()

    if args.list:
        for pkg_id, pkg in packages.items():
            n = len(pkg["diagrams"])
            print(f"  {pkg_id}: {pkg['readme_title']} ({n} diagrams)")
        return

    targets = {}
    if args.package:
        if args.package not in packages:
            print(f"Unknown package: {args.package}")
            print(f"Available: {', '.join(packages.keys())}")
            sys.exit(1)
        targets[args.package] = packages[args.package]
    else:
        targets = packages

    exit_code = 0
    for pkg_id, pkg in targets.items():
        if args.check:
            rc = check_package(pkg_id, pkg)
        else:
            rc = build_package(pkg_id, pkg)
        if rc != 0:
            exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
