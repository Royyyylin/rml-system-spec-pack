# Functional Requirements

> `Stage` 依 [baseline-target-migration.md](baseline-target-migration.md) 定義。每條 requirement 只標一個 primary stage。

| ID | Stage | Description | Source | Related Artifacts | AC | TC |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `REQ-001` | `target` | App 應以 `STATUS` / `METRICS_V2` 顯示 telemetry，並把缺欄位區分為 `sparse`、`stale`、`unknown`、`not_synced`。 | `FEA-001`, `RML-CST-003` | `BLK-002`, `STA-001`, `SEQ-001`, `PKT-001`, `PKT-002` | `AC-001` | `TC-001`, `TC-002` |
| `REQ-002` | `migration` | App 應依 `CAPS_V2` 或 `CAP` fallback 決定可用功能，且不得暴露未宣告能力的操作。 | `FEA-002`, `RML-CST-001` | `BLK-005`, `SEQ-001`, `PKT-003` | `AC-002` | `TC-003` |
| `REQ-003` | `target` | App 應將 `stableId`、`central_ref`、MAC 視為不同層級身分；若畫面顯示 MAC，必須標示它是 transport identity。 | `FEA-003`, `RML-OBJ-002`, `RML-RSK-002` | `BLK-001`, `PKT-006` | `AC-003` | `TC-004` |
| `REQ-004` | `target` | 當 Central 權威分配與 firmware runtime attach 不一致時，App 應顯示雙來源 gateway 與 `assignmentSyncState`。 | `FEA-004`, `RML-RSK-003` | `BLK-003`, `STA-002`, `SEQ-002`, `PKT-004` | `AC-004` | `TC-005` |
| `REQ-005` | `target` | Alias 顯示應遵守 `local_pending > central > cached > DEVICE_ALIAS > adv_name`。 | `FEA-003` | `BLK-001`, `STA-003`, `SEQ-003`, `PKT-006` | `AC-005` | `TC-006` |
| `REQ-006` | `target` | 使用者操作應透過 `CMD_V2` / `CMD_RESULT` 執行，並在成功、失敗、timeout、retry 間有可觀測 UI 狀態。 | `FEA-002`, `RML-RSK-004` | `BLK-004`, `STA-004`, `SEQ-004`, `PKT-005` | `AC-006` | `TC-007`, `TC-008`, `TC-011` |
| `REQ-007` | `migration` | App 用於 freshness / comparison 的 upstream evidence 必須可追溯到 owner repo 提供的 `source_timestamp` 或等價 age evidence（例如 `updated_at` / `revision` / `observed_at` / `failover_generation`）；若 owner repo 尚未提供，App 不得偽裝成可精確 freshness 判定。 | `FEA-001`, `FEA-004`, `RML-OBJ-003` | `BLK-002`, `BLK-003` | `AC-007` | — |
| `REQ-008` | `target` | App 僅在 `can_compare == true` 時可導出 `conflict`；任一側資料不存在、不新鮮或來自 last-synced reference，必須顯示 `not compared` / `last synced`。 | `FEA-004`, `RML-RSK-003` | `BLK-003`, `STA-002` | `AC-004`, `AC-007` | `TC-012` |

## Stage Notes

- `REQ-002` 之所以標成 `migration`，是因為 `CAP` fallback 屬於 compatibility bridge，不是長期 steady-state target。
