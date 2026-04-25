# X-1 Cross-Repo Wire Parity Test Spec

Status: draft
Primary Stage: `target`
Spec ID: `REQ-X-1`

## Context

`ble_api.yaml` 是 3 個 repo 的 wire format SSOT：

- **firmware** (`ble_qos_demo_V1.2m`): `tools/codegen/gen_cmd_v2_dispatch.py` + `gen_data_sections.py` → `src/generated/*.h`
- **central** (`central-device-metadata`): `tools/codegen/gen_data_sections.py` → `app/generated/*.py`
- **app** (`ble_qos_app`): `tools/codegen/gen_data_sections.py` → `lib/generated/*.dart`

**漂移風險**：各 repo 獨立 codegen。`ble_api.yaml` 改一個 byte → 若任一 repo 未重跑 codegen，或 codegen 邏輯有 bug，wire format 在三端靜默不一致。範例：opcode `0x07` valid_lens firmware `[4,8,16]` vs central/app `[4,16]` → central 拒絕合法 8-byte payload，無 error log。

X-1 自動驗 3 repo wire parity，CI 阻擋任何漂移進 main。

---

## Test Scope — 7 Wire Sections

| ID | Section | Firmware | Central | App |
|---|---|---|---|---|
| S1 | CMD_V2 dispatch table | `cmd_v2_dispatch.h` | _(Phase 1 新增)_ | _(Phase 1 新增)_ |
| S2 | Reject codes | `cmd_v2_dispatch.h` | _(Phase 1 新增)_ | _(Phase 1 新增)_ |
| S3 | Preset values | `presets.h` | `presets.py` | `presets.dart` |
| S4 | TUNE-VAL rules | `tune_val_rules.h` | `tune_val_rules.py` | `tune_val_rules.dart` |
| S5 | Zone enum | `zone_enum.h` | _(Phase 1 新增)_ | _(Phase 1 新增)_ |
| S6 | NVS roles | `nvs_roles.h` | _(Phase 1 新增)_ | _(Phase 1 新增)_ |
| S7 | System constants | `system_constants.h` | `system_constants.py` | `system_constants.dart` |

S5/S6：central 和 app 目前尚無對應生成檔，Phase 1 codegen 需補齊。

---

## Architecture — Recommended Option C

### Options Evaluated

| Option | 方法 | 評估 |
|---|---|---|
| (a) Direct parse | Python 解析 C/Dart/Python | 各語言 parser 維護成本高，不推薦 |
| (b) Self-consistency | 各 repo codegen → diff checked-in | 無法捕捉 codegen 邏輯各異的 bug，不推薦 |
| **(c) Canonical JSON** | 各 repo 產 `_canonical_wire.json` → central diff | **推薦**：統一格式，diff 簡單，CI 易整合 |

### Option C Data Flow

```
ble_api.yaml
    ├── firmware codegen → src/generated/*.h
    │                    → src/generated/_canonical_wire.json  [NEW]
    ├── central codegen  → app/generated/*.py
    │                    → app/generated/_canonical_wire.json  [NEW]
    └── app codegen      → lib/generated/*.dart
                         → lib/generated/_canonical_wire.json  [NEW]

CI: tools/x1-wire-parity-check.py
    reads 3 × _canonical_wire.json → section diff → pass / fail
```

### Canonical JSON Schema (abbreviated)

```json
{
  "yaml_version": "1.2",
  "sections": {
    "cmd_v2_dispatch": [
      { "opcode": "0x07", "valid_lens": [4, 16], "name": "SET_SCHED_TUNE" }
    ],
    "reject_codes": [
      { "code": "0x00", "name": "SUCCESS" },
      { "code": "0xFF", "name": "BAD_LENGTH" }
    ],
    "presets": {
      "balanced": { "cutoff1": 3, "cutoff2": 5, "cutoff3": 8,
                    "interval1": 80, "interval2": 160,
                    "interval3": 400, "interval4": 800 }
    },
    "tune_val_rules": [
      { "id": "TUNE-VAL-001", "field": "cutoffs",
        "op": "strictly_increasing", "severity": "hard_reject" }
    ],
    "zones": [
      { "name": "NEAR", "value": 0 }, { "name": "EDGE", "value": 3 }
    ],
    "nvs_roles": [
      { "name": "END_DEVICE", "value": "0x00" },
      { "name": "CC", "value": "0x04" }
    ],
    "system_constants": {
      "MAX_ED": 8, "CMD_V2_TIMEOUT_MS": 10000
    }
  }
}
```

### Failure Output Format

```
[X-1 FAIL] Section: cmd_v2_dispatch — opcode 0x07 valid_lens mismatch
  firmware : [4, 8, 16]
  central  : [4, 16]
  app      : [4, 16]
Action: re-run central/app codegen against latest ble_api.yaml
```

---

## Done Criteria

1. 7 wire sections 全部被 canonical JSON 涵蓋（S5/S6 需 Phase 1 codegen 補齊）
2. `tools/x1-wire-parity-check.py`：函數 ≤ 40 行、diff output 含 section / repo / expected / actual
3. CI `x1-parity.yml` 在 `ble_api.yaml` 變更時觸發，加入 daily cron
4. 3 repo 各 codegen target 產 `_canonical_wire.json` 並 commit 進 repo

---

## Acceptance Criteria

**Format**: GIVEN / WHEN / THEN。每 section 各 1 positive + 1 negative。

### S1 — CMD_V2 Dispatch Table

**AC-X1-001**
GIVEN 3 repo 均 sync 至最新 `ble_api.yaml`（dispatch table 一致）
WHEN `x1-wire-parity-check.py` 執行
THEN exit 0，`cmd_v2_dispatch` section 標記 PASS

**AC-X1-002**
GIVEN `ble_api.yaml` 將 opcode `0x07` valid_lens 改為 `[4, 8, 16]`，只 firmware 重 codegen
WHEN `x1-wire-parity-check.py` 執行
THEN exit 1，報 `cmd_v2_dispatch mismatch: 0x07 valid_lens — firmware=[4,8,16], central=[4,16], app=[4,16]`

### S2 — Reject Codes

**AC-X1-003**
GIVEN 3 repo reject codes 0x00–0xFF mapping 完全一致
WHEN `x1-wire-parity-check.py` 執行
THEN exit 0，`reject_codes` section 標記 PASS

**AC-X1-004**
GIVEN firmware 新增 `0xFC = UNKNOWN_PRESET`，central/app 未更新
WHEN `x1-wire-parity-check.py` 執行
THEN exit 1，報 `reject_codes mismatch: 0xFC absent in central/app`

### S3 — Preset Values

**AC-X1-005**
GIVEN 3 repo `balanced` / `conservative` / `aggressive` 各 7 數值完全一致
WHEN `x1-wire-parity-check.py` 執行
THEN exit 0，`presets` section 標記 PASS

**AC-X1-006**
GIVEN firmware `balanced.interval4` 改為 1000，central/app 仍為 800
WHEN `x1-wire-parity-check.py` 執行
THEN exit 1，報 `presets mismatch: balanced.interval4 — firmware=1000, central=800, app=800`

### S4 — TUNE-VAL Rules

**AC-X1-007**
GIVEN 3 repo TUNE-VAL rule id / field / op / severity 完全一致
WHEN `x1-wire-parity-check.py` 執行
THEN exit 0，`tune_val_rules` section 標記 PASS

**AC-X1-008**
GIVEN `ble_api.yaml` TUNE-VAL-003 intervals max 改為 `1600`，只 firmware 重 codegen
WHEN `x1-wire-parity-check.py` 執行
THEN exit 1，報 `tune_val_rules mismatch: TUNE-VAL-003 max — firmware=1600, central=3200, app=3200`

### S5 — Zone Enum

**AC-X1-009**
GIVEN 3 repo zone values 一致（NEAR=0, MID=1, FAR=2, EDGE=3）
WHEN `x1-wire-parity-check.py` 執行
THEN exit 0，`zones` section 標記 PASS

**AC-X1-010**
GIVEN `ble_api.yaml` 新增 `CRITICAL=4`，只 firmware 重 codegen
WHEN `x1-wire-parity-check.py` 執行
THEN exit 1，報 `zones mismatch: CRITICAL absent in central/app`

### S6 — NVS Roles

**AC-X1-011**
GIVEN 3 repo NVS role bytes 一致（END_DEVICE=0x00, GATEWAY=0x01, CC=0x04）
WHEN `x1-wire-parity-check.py` 執行
THEN exit 0，`nvs_roles` section 標記 PASS

**AC-X1-012**
GIVEN `ble_api.yaml` CC role 改為 `0x05`，只 firmware 重 codegen
WHEN `x1-wire-parity-check.py` 執行
THEN exit 1，報 `nvs_roles mismatch: CC — firmware=0x05, central=0x04, app=0x04`

### S7 — System Constants

**AC-X1-013**
GIVEN 3 repo MAX_ED / CMD_V2_TIMEOUT_MS 等常數完全一致
WHEN `x1-wire-parity-check.py` 執行
THEN exit 0，`system_constants` section 標記 PASS

**AC-X1-014**
GIVEN `ble_api.yaml` CMD_V2_TIMEOUT_MS 改為 `15000`，只 central 重 codegen
WHEN `x1-wire-parity-check.py` 執行
THEN exit 1，報 `system_constants mismatch: CMD_V2_TIMEOUT_MS — central=15000, firmware=10000, app=10000`

### Full Suite

**AC-X1-015**
GIVEN 3 repo 均 sync 至最新 `ble_api.yaml`，7 sections 全一致
WHEN `x1-wire-parity-check.py` 執行
THEN exit 0，stdout 印 `[X-1 PASS] 7/7 sections OK`

**AC-X1-016**
GIVEN PR 修改 `ble_api.yaml`
WHEN GitHub Actions `x1-parity.yml` 觸發
THEN `x1-wire-parity-check.py` 自動執行，result 出現在 PR check 列表

---

## trace_map Entry (Phase B 預留)

```yaml
# 待 Phase B 加入 trace/trace_map.yaml
- req_id: REQ-X-1-001
  description: "x1 wire parity check — 3 repo 7 sections 100% parity"
  spec: 06_crosscutting-integration/x1-wire-parity-spec.md
  ac_ids: [AC-X1-001 .. AC-X1-016]
  affected_repos: [firmware, central, app]
```
