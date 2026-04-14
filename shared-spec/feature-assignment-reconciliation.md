# Feature Spec — RML-FEA-004 Assignment Reconciliation

Status: formal
Feature ID: `RML-FEA-004`
Primary Stage: `target`

## Purpose

定義 BLE QoS Demo 中「Central assignment truth 與 firmware runtime attach 不一致時，系統如何可見、可解釋、可收斂」這個 cross-repo feature。

Diagram render: [feature-assignment-reconciliation.svg](/Users/create94520/Projects/ble_qos_demo/rml-system-spec-pack/renders/feature-assignment-reconciliation.svg)

本 feature 回答的是：
- 什麼叫 authoritative assignment，什麼叫 runtime attach
- App 何時顯示 `confirmed`、`pending_reconciliation`、`conflict`、`central_only`、`orphaned`
- failover / hold-down / sync 延遲下，哪些不一致是正常 migration reality
- 何時只能顯示雙來源，不能偷偷合併成單一 gateway

## Feature Intent

| ID | Statement |
| :--- | :--- |
| `FEA-004-INT-001` | 當 Central 與 firmware 對 End Device 目前所屬 Gateway 的觀測不一致時，App 必須顯示差異，而不是靜默覆寫。 |
| `FEA-004-INT-002` | assignment reconciliation 必須建立在 authority boundary 上：Central 擁有 assignment truth，Firmware 擁有 runtime attach observation，App 擁有 human-facing explanation。 |
| `FEA-004-INT-003` | failover、hold-down、sync lag 與 orphaned recovery 都屬正常系統情境；其 UI 與 evidence 不得被誤標成隨機錯誤。 |
| `FEA-004-INT-004` | `conflict` 只在 Central assignment 與 runtime observation 兩邊都可比較時成立；若 Central 不在當前 session 可達範圍，App 不得偽造衝突。 |

## Truth Sources

| Source | Owner | What It Provides | What It Does Not Provide |
| :--- | :--- | :--- | :--- |
| `active_gateway_id`, `assignment_state`, `assignment_version` | `Central` | authoritative End Device-to-Gateway assignment、lease / version、orphaned decision | first-hand runtime attach |
| `runtimeGatewayId`, `failover_generation`, roster observation | `Firmware` | device-side attach observation、failover event、runtime recovery | canonical assignment truth |
| `assignmentSyncState`, dual-row / badge UI | `App` | human-facing comparison、pending/conflict/orphaned explanation | system-of-record decision |

## Authority Boundary

| ID | Rule |
| :--- | :--- |
| `FEA-004-BND-001` | `Central` 是 assignment arbitrator；其他層不得把 runtime attach 升格成 authoritative assignment。 |
| `FEA-004-BND-002` | `Firmware` 擁有 `runtimeGatewayId` 與 `failover_generation` 這類第一手 observation；Central 與 App 只能消費與呈現。 |
| `FEA-004-BND-003` | `App` 負責把 authoritative 與 runtime 並列顯示，並導出 `assignmentSyncState`；不得只留一個 gateway 欄位掩蓋差異。 |
| `FEA-004-BND-004` | `Conductor` 可追蹤 evidence 與 gate，但不得在 cross-repo 文件重定 assignment truth。 |
| `FEA-004-BND-005` | `App` 採 `single active session` 模式。若當前連接 `CC bridge`，視為 Central-side session，CC bridge 只負責 relay，不擁有 assignment authority。若連接 `Gateway` / `End Device`，視為 Firmware-side session，`Central` 只可作為 last-synced reference，不視為即時 observation。 |
| `FEA-004-BND-006` | `conflict` 只在 `can_compare == true` 時才可導出；若任一側資料不存在、不新鮮或來自 last-synced reference，App 必須顯示 `not compared` / `last synced`，不得升格為 `conflict`。 |

## Comparison Evidence

Reconciliation 依賴 owner repo 提供的 `source_timestamp` 或等價 age evidence。spec-pack 本身不發明 wire field。

| Side | Evidence Candidates（來自 owner repo SSOT） |
| :--- | :--- |
| Central | `updated_at`、`revision`、`assignment_version`、`last_failover_at`（見 `central-device-metadata/docs/specs/data-model.md`）|
| Firmware | `failover_generation`、`uptime_s`、`EVT.seq`、`GW_CFG_VERSION`、`boot_id`（見 `ble_qos_demo_V1.2m/docs/specs/data-model.md`；Phase 2 `ts_device / ts_gateway / ts_central` 尚未實作）|

若 owner repo 尚未提供任何 age evidence → App 僅能做保守判定（`can_compare = false`），不得偽裝成可精確 freshness 判定。

## Comparison Flow

```
(1) 判 source state：unknown / not_synced / stale / fresh
(2) 算 can_compare（兩邊都 fresh 才能 true）
(3) can_compare == false：UI 顯示 not compared / last synced，不進 FSM
(4) can_compare == true：落到 5-state FSM（confirmed / pending_reconciliation / conflict / central_only / orphaned）
```

- `stale` 是 source-level annotation，可與 FSM 狀態並存（例：FSM 處於 `central_only` 且 Central reference 為 stale）
- `not compared` 是 comparison gate result，直接阻止進入 FSM
- 5-state FSM 只描述 reconciliation relationship，不取代 source freshness label

## Reconciliation States

| State | Meaning | Must Not Be Interpreted As |
| :--- | :--- | :--- |
| `confirmed` | Central 與 runtime 指向相同 gateway | 唯一資料來源存在 |
| `pending_reconciliation` | runtime 已切換或先觀測到 attach，Central 尚未追上 | bug / random drift |
| `conflict` | 兩端都有 active gateway，且值不同 | UI 可自行決定哪個才是真的 |
| `central_only` | Central 有 assignment，但 runtime 尚未可見 | failover success |
| `orphaned` | 無 authoritative assignment，亦無 runtime attach | temporary loading |

## Human-Facing Rules

- detail 與 roster 在 `pending_reconciliation` / `conflict` 時，必須同時顯示 Central Gateway 與 Runtime Gateway
- main page 只有在偵測到可比較的不一致時，才顯示 conflict entry / badge；點擊後再進 detail 顯示雙來源
- `confirmed` 時可隱藏 reconciliation badge，避免 UI 噪音
- `central_only` 應明確表達「Central 已知，但 runtime 尚未可見」
- `orphaned` 必須被顯示為異常運行狀態，不得被包裝成正常 idle
- 若當前 session 沒有可用的 Central side 資料，App 應顯示 `not compared`、`last synced` 或等價語意，不得直接標 `conflict`

## Baseline / Target / Migration

### Baseline

- App 已有 `assignmentSyncState`、`authoritativeGatewayId`、`runtimeGatewayId` 與 dual-row UI。
- Central 已定義 assignment arbitration、hold-down 與 explainability policy。
- Firmware 已定義 `assignment_state`、`failover_generation` 與 failover event 基本語意。

### Target

- App 能以單一 feature 語言解釋 `confirmed / pending_reconciliation / conflict / central_only / orphaned`
- 任何不一致都能追回 Central decision 與 firmware observation，而不是只剩畫面截圖
- requirement、AC、TC、handoff 對 assignment reconciliation 使用同一套 state vocabulary

### Migration

- failover 發生後的短暫不一致屬正常 migration reality，不要求兩端零延遲同步
- hold-down、delta sync、runtime-first attach 都可能造成 `pending_reconciliation` 或 `central_only`
- 若某些舊路徑仍只提供 roster attach、尚未附完整 explainability evidence，必須明文標示為 `migration`

## Failure / Mismatch Cases

| Case | Required Behavior |
| :--- | :--- |
| runtime 先切到新 Gateway，Central 尚未更新 | 顯示 `pending_reconciliation`，保留 Runtime Gateway 與 Central Gateway 雙來源 |
| Central 改 assignment，但 runtime 尚未觀測到 attach | 顯示 `central_only` |
| 兩端皆有 gateway 但不同 | 顯示 `conflict`，不可只顯示其一 |
| 目前只連到近端 Gateway / End Device，沒有可比較的 Central 即時資料 | 不顯示 `conflict`；若有 Central 快取，可標示 `last synced` / `not compared` |
| 無 assignment 且無 runtime attach | 顯示 `orphaned` |
| failover 收斂完成 | 狀態回到 `confirmed`，badge 可消失 |

## Downstream Mappings

| Kind | IDs |
| :--- | :--- |
| Primary requirement | `REQ-004` |
| Adjacent requirements | `REQ-001`, `REQ-003` |
| App formal docs | `app-scope/04-local-state.md`, `app-scope/05-interface-contract.md` |
| App implementation plan | `2026-03-28-assignment-reconciliation/plan.md` |
| Central formal docs | `assignment-policy.md` |
| Firmware formal docs | `data-model.md`, `failover-policy.md` |

## References

- [rml-lite.md](rml-lite.md)
- [requirements.md](requirements.md)
- [baseline-target-migration.md](baseline-target-migration.md)
- [app local state](../../ble_qos_app/docs/specs/app-scope/04-local-state.md)
- [app interface contract](../../ble_qos_app/docs/specs/app-scope/05-interface-contract.md)
- [app reconciliation plan](../../ble_qos_app/docs/plans/2026-03-28-assignment-reconciliation/plan.md)
- [central assignment policy](../../central-device-metadata/docs/specs/assignment-policy.md)
- [firmware data model](../../ble_qos_demo_V1.2m/docs/specs/data-model.md)
- [firmware failover policy](../../ble_qos_demo_V1.2m/docs/specs/failover-policy.md)
