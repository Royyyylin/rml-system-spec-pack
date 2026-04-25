# Tools

`changed_only_report.py` 是 `rml-system-spec-pack` 的最小治理報告工具。

`workspace_changed_only_report.py` 是 workspace wrapper。
它會預設掃描：
- `ble_qos_app`
- `ble_qos_demo_V1.2m`
- `central-device-metadata`

並把收集到的 git 變更，加上手動指定的 spec-pack 檔案，一起送進 `changed_only_report.py`。

目前特性：
- 接受多個 `--changed-file`
- 預設讀 `trace/manual_exceptions.yaml`
- 輸出文字摘要到 stdout
- 可用 `--json-out` 寫出 JSON 報告
- 目前只實作 `CIR-003`、`CIR-008`、`CIR-009`
- 採 `report-only`，不做 blocking gate

範例：

```bash
python3 rml-system-spec-pack/tools/changed_only_report.py \
  --changed-file ble_qos_demo_V1.2m/ble_api.yaml \
  --changed-file rml-system-spec-pack/firmware-spec/packet_contract.md \
  --json-out /tmp/changed-only-report.json
```

registry 例外：

```yaml
exceptions:
  - rule_id: CIR-009
    path_glob: rml-system-spec-pack/renders/packet_diagram.png
    reason: temporary-demo-render
    owner: roy
    expires_on: 2026-04-30
```

CLI 手動例外：

```bash
python3 rml-system-spec-pack/tools/changed_only_report.py \
  --changed-file rml-system-spec-pack/renders/packet_diagram.png \
  --manual-exception CIR-009:temporary-demo-render
```

JSON 結構定義在：
- `rml-system-spec-pack/tools/changed_only_report.schema.json`

diagram contract 檢查：

```bash
python3 rml-system-spec-pack/tools/check_diagram_contract.py
```

只檢查單一圖檔：

```bash
python3 rml-system-spec-pack/tools/check_diagram_contract.py \
  rml-system-spec-pack/03_building-blocks/FEA-001-telemetry-roster-visibility.d2
```

用途：
- 檢查 `.d2` / `.mmd` 開頭是否有 `AI Diagram Contract`
- 檢查 `template_id` 是否為正式登記模板，且 `diagram_type` / `max_nodes` / `max_groups` 不越界
- 確保後續 AI 續改 diagram source 時，不是只靠臨場 prompt
- 預設掃 8 個 arc42 chapter dirs（`00_introduction-goals/` ~ `99_appendix/`）＋ `app-spec/`、`firmware-spec/`

review package 同步（generic）：

```bash
# Build 所有 review packages
python3 rml-system-spec-pack/tools/sync_review_package.py

# Build 指定 package
python3 rml-system-spec-pack/tools/sync_review_package.py --package wave1

# Check mode（不寫檔，drift 時 exit non-zero）
python3 rml-system-spec-pack/tools/sync_review_package.py --check
python3 rml-system-spec-pack/tools/sync_review_package.py --package wave1 --check

# 列出可用 packages
python3 rml-system-spec-pack/tools/sync_review_package.py --list
```

用途：
- d2 source 修改後，一個指令同步 SVG/PNG render + drawio review 檔 + README
- manifest 在 `tools/review_packages.json`
- 新增 review package 只需在 manifest 加一個 entry，不需要複製腳本
- `--check` 用 deterministic content compare，適合 CI

backward-compatible wrapper（委派給 generic 腳本）：

```bash
python3 rml-system-spec-pack/tools/sync_wave1_review_package.py
python3 rml-system-spec-pack/tools/sync_wave1_review_package.py --check
```

workspace wrapper 範例：

```bash
python3 rml-system-spec-pack/tools/workspace_changed_only_report.py \
  --changed-file rml-system-spec-pack/app-spec/state_machine.md \
  --json-out /tmp/workspace-changed-only-report.json
```

只測單一 repo 或停用預設 repo：

```bash
python3 rml-system-spec-pack/tools/workspace_changed_only_report.py \
  --no-default-repos \
  --repo firmware=ble_qos_demo_V1.2m \
  --base-ref firmware=origin/main
```
