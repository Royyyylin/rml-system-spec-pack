# X-1 Cross-Repo Wire Parity Check — Implementation Plan

Status: draft
Spec: [x1-cross-repo-wire-parity-spec.md](x1-cross-repo-wire-parity-spec.md)

## Goal

在 3 個 repo（firmware / central / app）部署 X-1 wire parity check：
1. 各 repo codegen 新增 `_canonical_wire.json` target
2. spec-pack `tools/` 新增 `x1-wire-parity-check.py`
3. 各 repo `.github/workflows/x1-parity.yml` CI 整合

---

## Affected Files

### firmware (`ble_qos_demo_V1.2m`)

| 動作 | 檔案 |
|---|---|
| 修改 | `tools/codegen/gen_cmd_v2_dispatch.py` — 加 `--canonical-json` flag，輸出 S1/S2 |
| 修改 | `tools/codegen/gen_data_sections.py` — 加 canonical JSON target，輸出 S3/S4/S5/S6/S7 |
| 新增 | `src/generated/_canonical_wire.json` — codegen 產出，commit 進 repo |
| 新增 | `.github/workflows/x1-parity.yml` |

### central (`central-device-metadata`)

| 動作 | 檔案 |
|---|---|
| 修改 | `tools/codegen/gen_data_sections.py` — 加 canonical JSON target（S3/S4/S7）+ 新增 S5/S6 生成 |
| 新增 | `app/generated/_canonical_wire.json` — codegen 產出，commit 進 repo |
| 新增 | `app/generated/zone_enum.py` — S5 新增（Phase 1） |
| 新增 | `app/generated/nvs_roles.py` — S6 新增（Phase 1） |
| 新增 | `.github/workflows/x1-parity.yml` |

### app (`ble_qos_app`)

| 動作 | 檔案 |
|---|---|
| 修改 | `tools/codegen/gen_data_sections.py` — 加 canonical JSON target（S3/S4/S7）+ 新增 S5/S6 生成 |
| 新增 | `lib/generated/_canonical_wire.json` — codegen 產出，commit 進 repo |
| 新增 | `lib/generated/zone_enum.dart` — S5 新增（Phase 1） |
| 新增 | `lib/generated/nvs_roles.dart` — S6 新增（Phase 1） |
| 新增 | `.github/workflows/x1-parity.yml` |

### spec-pack (`rml-system-spec-pack`)

| 動作 | 檔案 |
|---|---|
| 新增 | `tools/x1-wire-parity-check.py` — 讀 3 repo canonical JSON → diff |
| 新增 | `.github/workflows/x1-parity.yml` — submodule / path 觸發（若 spec-pack 有 submodule）|

---

## Implementation Phases

### Phase 1 — Codegen JSON Target (per repo)

**Scope**: 修改各 repo `gen_data_sections.py`，加入 `--emit-canonical-json <output>` flag。

**Firmware specifics**:
- `gen_cmd_v2_dispatch.py` 已有 opcode table，新增 S1/S2 JSON 輸出到 `_canonical_wire.json`
- `gen_data_sections.py` 輸出 S3/S4/S5/S6/S7 並 merge 進同一 JSON 檔

**Central/App specifics**:
- 補齊 S5 zone_enum、S6 nvs_roles 生成（目前缺這兩個 target）
- S1/S2（cmd_v2_dispatch / reject_codes）目前無對應生成，Phase 1 補 canonical JSON 中的這兩 section，不要求 central/app 必須有對應語言 source 檔（JSON 即為 parity 基礎）

**Output contract**:
- 檔名固定：`<generated_dir>/_canonical_wire.json`
- Schema 見 [spec](x1-cross-repo-wire-parity-spec.md#canonical-json-schema-abbreviated)
- 包含 `yaml_version` 字串，供 check tool 交叉驗證

**Done signal**: `_canonical_wire.json` 可被 `python3 -m json.tool` 驗證；3 repo 手跑 codegen 後 JSON diff 為空。

### Phase 2 — x1-wire-parity-check.py

**Location**: `tools/x1-wire-parity-check.py`（spec-pack root `tools/`）

**Interface**:
```
python3 tools/x1-wire-parity-check.py \
  --firmware  <path>/src/generated/_canonical_wire.json \
  --central   <path>/app/generated/_canonical_wire.json \
  --app       <path>/lib/generated/_canonical_wire.json
```

**Logic**（函數 ≤ 40 行）:
1. Load 3 JSON → validate schema version match
2. Per section（S1–S7）：deep-equal compare；collect mismatches
3. Print `[X-1 PASS] N/7 sections OK` or `[X-1 FAIL]` with structured diff
4. Exit 0 if all pass, exit 1 if any section mismatches

**Constraints**:
- 不 import 第三方 library（只用 stdlib `json`, `sys`, `argparse`）
- 每個 compare helper 函數 ≤ 40 行

**Done signal**: `python3 tools/x1-wire-parity-check.py --firmware ... --central ... --app ...` 在同步狀態回 exit 0；人為改一個值回 exit 1 + 正確 diff。

### Phase 3 — CI Integration

**Workflow file**: `.github/workflows/x1-parity.yml`（各 repo 各一份）

**Trigger**:
```yaml
on:
  push:
    paths: ['ble_api.yaml', 'tools/codegen/**']
  pull_request:
    paths: ['ble_api.yaml', 'tools/codegen/**']
  schedule:
    - cron: '0 2 * * *'   # daily 02:00 UTC
```

**Steps**:
1. Checkout 3 repo（或 submodule）
2. 各 repo 跑 codegen（`python3 tools/codegen/gen_data_sections.py ...`）
3. 執行 `python3 tools/x1-wire-parity-check.py --firmware ... --central ... --app ...`
4. Upload `_canonical_wire.json` 為 artifact（供 debug）

**Done signal**: PR 修 `ble_api.yaml` 後，Actions check `x1-wire-parity` 出現在 PR check 列表；全綠則 pass，漂移則 fail + artifact。

---

## Ordering Dependencies

```
Phase 1 firmware  ──┐
Phase 1 central   ──┼──► Phase 2 check tool ──► Phase 3 CI
Phase 1 app       ──┘
```

Phase 1 三個 repo 可並行。Phase 2 依賴 Phase 1 完成後有實際 JSON 可測試。Phase 3 依賴 Phase 2 check tool 存在。

---

## Done Bullets

- [ ] firmware `_canonical_wire.json` codegen 可跑，7 sections 齊全
- [ ] central `_canonical_wire.json` codegen 可跑，補齊 S5/S6
- [ ] app `_canonical_wire.json` codegen 可跑，補齊 S5/S6
- [ ] `tools/x1-wire-parity-check.py` 函數 ≤ 40 行，exit 0/1 正確
- [ ] 3 repo CI `x1-parity.yml` 各到位，daily cron + PR trigger 均測試過
- [ ] AC-X1-001 ~ AC-X1-016 全部驗過（見 spec AC 清單）
