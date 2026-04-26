# Feature Spec — FEA-001 Telemetry & Roster Visibility

Status: formal
Feature ID: `FEA-001`
Primary Stage: `target`

## Purpose

定義 BLE QoS Demo 中「telemetry 與 roster 可見性」這個 cross-repo feature 的上游意圖、資料來源、truth boundary 與驗收鉤子。

Diagram render: [feature-telemetry-roster-visibility.svg](/Users/create94520/Projects/ble_qos_demo/rml-system-spec-pack/renders/feature-telemetry-roster-visibility.svg)

本 feature 回答的是：
- App 應看見哪些 telemetry / roster 資訊
- 這些資訊各自來自哪個 authority owner
- sparse / stale / unknown / not_synced 代表什麼
- roster observation、identity、assignment 三者如何分層

## Feature Intent

| ID | Statement |
| :--- | :--- |
| `FEA-001-INT-001` | Operator / Engineer 必須能在 App 中看見與裝置狀態有關的 telemetry 與 roster 資訊，而不需自行推測 wire semantics。 |
| `FEA-001-INT-002` | 可見性必須建立在 authority boundary 上：Firmware 提供 runtime observation，Central 提供 global metadata / assignment truth，App 負責 human-facing merge 與呈現。 |
| `FEA-001-INT-003` | feature 必須容納 P0 / P1 profile 差異，不得把 sparse payload 誤判為錯誤或資料遺失。 |
| `FEA-001-INT-004` | 可見性必須尊重現場 session 邊界：App 一次只操作一個 active target，未連到的對象不應被假裝成即時可讀。 |

## Data Sources

| Source | Owner | What It Provides | What It Does Not Provide |
| :--- | :--- | :--- | :--- |
| `STATUS` / `METRICS_V2` / `EVT` / `ROSTER_LIST` / `CAPS_V2` | `Firmware` | runtime telemetry、slot snapshot、runtime observation、capability hints | canonical assignment truth、global metadata、auth truth |
| metadata / assignment / health / sync | `Central` | canonical identity、assignment、alias、role / permission、authoritative snapshot | first-hand runtime measurement |
| local cache / UI state | `App` | last-valid display、local merge、sparse/stale UI、interaction context | system-of-record truth |

## Truth Boundary

| ID | Rule |
| :--- | :--- |
| `FEA-001-BND-001` | Firmware runtime telemetry 是第一手 observation；App 與 Central 可顯示與整合，但不得假裝擁有 runtime truth。 |
| `FEA-001-BND-002` | Central 是 canonical identity、assignment 與 `ed_idx -> ed_id` 最終映射 owner。App 可近端暫時解析 roster，但該映射不是 authoritative。 |
| `FEA-001-BND-003` | App 是 human-facing visibility owner，負責將 runtime observation 與 authoritative metadata 同屏呈現，但不得把 local cache 升格為 system truth。 |
| `FEA-001-BND-004` | roster 代表 runtime / discovery-side observation，不等同 Central authoritative inventory 或 assignment truth。 |
| `FEA-001-BND-005` | App 採 `single active session` 模式；若當前 session 只連到 Gateway / End Device，則 Central 不屬於當前即時 observation scope。 |
| `FEA-001-BND-006` | 經 `CC bridge`、`Gateway` 或 `Central` 轉述的其他節點資料屬 relayed / cached view，不等於 App 自己對該節點的第一手 BLE observation。 |
| `FEA-001-BND-007` | `stale` 與 `not_synced` 的 freshness 判定必須可追溯到 owner repo 提供的 `source_timestamp` 或等價 age evidence（例如 `updated_at` / `revision` / `observed_at` / `failover_generation` / `uptime_s`）；App 不得僅以 local clock 推測 freshness。freshness window 數值以 owner repo SSOT 或 app contract 定義為準，spec-pack 本身不拍秒數；若尚未定義，標為 migration dependency。 |

## Visibility Scope

### Telemetry

App 至少必須能顯示：
- RSSI、PDR、latency、jitter
- profile / PHY / TX / interval 或其可見替代
- heartbeat / liveness / health summary
- payload freshness 與最近觀測狀態

### Roster

App 至少必須能顯示：
- 哪些 End Device 目前被 roster 觀測到
- slot / runtime attach 類資訊的 human-facing 呈現
- 裝置 identity、alias、assignment、runtime attach 的分層結果
- orphaned / conflict / pending-reconciliation 類狀態

## Value-State Semantics

| State | Meaning | Must Not Be Interpreted As |
| :--- | :--- | :--- |
| `present` | 有值，且來源欄位存在 | 唯一真相層級 |
| `sparse` | P0 profile 正常缺欄位 | error / data loss |
| `stale` | 曾有值但已過 freshness window | unknown |
| `unknown` | 從未取得過該欄位 | stale |
| `not_synced` | Central 尚未同步到可用狀態 | runtime failure |

## Baseline / Target / Migration

### Baseline

- App 已有 `telemetry_snapshot`、`ed_roster_cache`、payload profile-aware state。
- Central 已定 profile-aware ingest，並承認 P0 / P1 欄位完整度不同。
- Firmware 已提供 `STATUS`、`METRICS_V2`、`ROSTER_LIST` 等 runtime 輸出。

### Target

- App 不只顯示數值，還能清楚標示 value-state 與來源層級。
- roster visibility 與 assignment truth 並列呈現，不互相覆蓋。
- telemetry 與 roster UI 可追回 authority owner 與 acceptance evidence。

### Migration

- `P0 sparse` 長期存在，屬於正常 bridge state，不要求被硬補成 P1 完整度。
- `ed_idx -> ed_id` 對某些 legacy / P0 path 仍依賴 roster mapping，屬 migration reality。
- 若 Central / App / Firmware 對同一欄位仍存在 legacy fallback，必須明文標示為 `migration`，不得偽裝成穩態 target。

## Failure / Mismatch Cases

| Case | Required Behavior |
| :--- | :--- |
| runtime telemetry 有值，但 Central 尚未同步 | App 顯示 runtime observation，並標示 `not_synced` 或等價 sync 狀態。 |
| Central assignment 與 runtime attach 不一致 | App 顯示雙來源，不可靜默合併。 |
| 目前只連到 `CC bridge`，`Gateway` / `End Device` 不在 BLE 可達範圍 | App 只把 `CC bridge` 視為當前 live peer；若畫面帶出其他節點資料，必須標示為 relayed / cached，而非第一手 BLE observation。 |
| 目前只連到近端 Gateway / End Device，Central 不在當前 session 可達範圍 | App 顯示近端 runtime observation；若有快取，可標示 `last synced` / `cached`，不得假裝是即時 Central 資料。 |
| P0 payload 缺欄位 | 以 `sparse` 呈現，不報錯、不亂補值。 |
| roster 看到 End Device，但 Central 尚未註冊 | 允許顯示 runtime observation，但不得把該 End Device 當成 authoritative registered device。 |
| 欄位過期 | 顯示 `stale`，保留 last-valid 與時間語意。 |

## Downstream Mappings

| Kind | IDs |
| :--- | :--- |
| Primary requirement | `REQ-001` |
| Adjacent requirements | `REQ-003`, `REQ-004`, `REQ-005` |
| App formal docs | `app-scope/04-local-state.md`, `app-scope/05-interface-contract.md` |
| Central formal docs | `telemetry-schema.md`, `central-auth-sync-contract.md` |
| Firmware formal docs | `dispatch-wire-contract.md`, `telemetry-schema.md` |

## References

- [rml-lite.md](rml-lite.md)
- [requirements.md](requirements.md)
- [baseline-target-migration.md](baseline-target-migration.md)
- [app local state](../../ble_qos_app/docs/specs/app-scope/04-local-state.md)
- [app interface contract](../../ble_qos_app/docs/specs/app-scope/05-interface-contract.md)
- [central telemetry schema](../../central-device-metadata/docs/specs/telemetry-schema.md)
- [central auth sync contract](../../central-device-metadata/docs/specs/central-auth-sync-contract.md)
- [firmware dispatch wire contract](../../ble_qos_demo_V1.2m/docs/01_definition/02_contract/dispatch-wire-contract.md)
