# Feature Spec — RML-FEA-003 Identity, Alias, and Metadata Display

Status: formal
Feature ID: `RML-FEA-003`
Primary Stage: `target`

## Purpose

定義 BLE QoS Demo 中「identity、alias 與 metadata 顯示」這個 cross-repo feature 的上游意圖、來源分層、display precedence 與禁止混線規則。

Diagram render: [feature-identity-alias-metadata-display.svg](/Users/create94520/Projects/ble_qos_demo/rml-system-spec-pack/renders/feature-identity-alias-metadata-display.svg)

本 feature 回答的是：
- `stableId`、`central_ref`、MAC 各自代表什麼
- alias 為什麼只是 display label，不是 canonical identity
- `local_pending > central > cached > DEVICE_ALIAS > adv_name` 為什麼成立
- App 何時可以顯示 firmware name，何時必須回到 Central metadata

## Feature Intent

| ID | Statement |
| :--- | :--- |
| `FEA-003-INT-001` | App 必須把 canonical identity、display alias、firmware reported name 視為不同層級，不得混成單一欄位。 |
| `FEA-003-INT-002` | 使用者在畫面上看到的名稱可變，但跨 repo canonical identity 不可因 rename、failover 或 cache 合併而改變。 |
| `FEA-003-INT-003` | 顯示名稱的 precedence 必須可解釋、可追蹤，並容納離線 pending 與 Central sync lag。 |
| `FEA-003-INT-004` | App 的 live peer layer 採 BLE session-driven 模式；必須先決定當前 BLE 可達對象，再在該 scope 內套用 display precedence。 |

## Truth Sources

| Source | Owner | What It Provides | What It Does Not Provide |
| :--- | :--- | :--- | :--- |
| `central_ref`, assignment-linked metadata, `alias`, `revision` | `Central` | authoritative metadata、Central-synced alias、revision truth | runtime BLE name、App local pending alias |
| `DEVICE_ALIAS`, `adv_name`, MAC-derived identifiers | `Firmware` | firmware reported display hint、transport identity、debug fallback | canonical metadata authority |
| `stableId`, local cache, pending alias queue | `App` | local PK、optimistic rename state、display merge | cross-system canonical identity truth |

## Authority Boundary

| ID | Rule |
| :--- | :--- |
| `FEA-003-BND-001` | `Central` 擁有 `central_ref` 與 alias metadata truth；App 不得以本地 rename queue 重定 canonical identity。 |
| `FEA-003-BND-002` | `Firmware` 擁有 MAC、`DEVICE_ALIAS` 與 `adv_name` 這類 transport/debug display hints；它們只能當 fallback。 |
| `FEA-003-BND-003` | `App` 擁有 human-facing display merge，可決定當下顯示哪個 label，但不得讓 display label 污染 identity truth。 |
| `FEA-003-BND-004` | 畫面若顯示 MAC，必須標示它是 transport identity，不得讓使用者誤認為 app / Central 主鍵。 |
| `FEA-003-BND-005` | 若當前只有 `CC bridge` 在 BLE 可達範圍，App 對 `Gateway` / `End Device` 的名稱只能視為 relayed / cached view，不得偽裝成第一手 BLE observation。 |

## Visibility Gate

- App 先判斷目前哪個 peer 對自己是 BLE 可達，再談名稱怎麼顯示
- display precedence 只在「同一個當前可達對象」的候選名稱之間成立
- `CC bridge` 轉述的 `Gateway` / `End Device` 名稱屬 relayed / cached view，不等於 App 親自收到的廣播或連線名稱

## Diagram Reading Guide

- `BLE Scan List`：解釋 App 目前在 BLE 上看得到、連得到誰；它不是整個 topology 的全量清單。
- `Tap to Connect`：解釋使用者從 scan list 點一個對象後，如何進入單一 `active session`。
- `Current Peer Detail`：解釋進入某個對象後，detail 頁要看什麼；它只代表該 peer，不代表整個系統。
- `Display Precedence`：解釋在當前 peer detail 內，App 最後要挑哪個名稱當主顯示名稱。
- `Live BLE data`：代表 selected peer 直接回給 App 的第一手 BLE 資料，例如 `DEVICE_ALIAS`、`adv_name`、MAC。
- `Central / cache metadata`：代表與該 peer 有關的 Central 主資料或快取背景，例如 `central_alias`、`cached_alias`、`central_ref`。
- `App local state`：代表 App 為了顯示與互動而持有的本地狀態，例如 `local_pending_alias`、`stableId`；它不是 authoritative truth。

## Display Precedence

| Context | Precedence |
| :--- | :--- |
| pending rename | `local_pending_alias > central_alias > cached_alias > DEVICE_ALIAS > adv_name` |
| no pending rename | `central_alias > cached_alias > DEVICE_ALIAS > adv_name` |
| no alias at all | `DEVICE_ALIAS > adv_name > canonical id` |

## Identity Layers

| Layer | Example | Meaning | Must Not Be Used As |
| :--- | :--- | :--- | :--- |
| App local PK | `stableId` | App 內部穩定主鍵 | firmware / Central canonical ref |
| Central canonical ref | `gw:{mac}` / `ed:{mac}` | cross-system metadata key | UI rename target label |
| Transport identity | BLE MAC | transport / hardware identity | 唯一 UI display name |
| Display label | alias / `DEVICE_ALIAS` / `adv_name` | 人類可讀名稱 | canonical identity |

## Human-Facing Rules

- detail 頁應能同時看見 canonical id、display label 與 transport identity 的區別
- 先決定當前 BLE 可達對象，再決定 display label precedence；不要把 topology 可見性和名稱排序混成同一條規則
- rename 成功或 pending 時，畫面可優先顯示 alias，但 canonical id 不可消失到無法追查
- `DEVICE_ALIAS` 與 `adv_name` 屬 fallback/debug only；不得在有 Central alias 時覆蓋 Central metadata
- failover 後若名稱未變，不代表 identity 層可被重新計算

## Baseline / Target / Migration

### Baseline

- App 已有 `stableId`、alias cache、pending alias queue 與 display precedence 規則。
- Central 已有 alias sync API、revision 與 `409 conflict` 語意。
- Firmware 仍提供 `DEVICE_ALIAS` / `adv_name` 作為 fallback name。

### Target

- 畫面與文件都使用同一套 vocabulary：`stableId`、`central_ref`、MAC、alias、firmware name
- rename / sync / conflict / fallback 都能回推到單一 owner truth
- feature、requirements、AC、TC 對 identity 與 alias 不再混寫

### Migration

- `DEVICE_ALIAS`、`adv_name` 與 cached alias 仍會在某些路徑充當 bridge display source
- 離線 pending alias 與 Central revision lag 屬 migration reality，不等於 metadata truth 已改寫
- 若某條舊路徑仍把 firmware name 直接顯示成主名稱，必須明文列為 migration gap

## Failure / Mismatch Cases

| Case | Required Behavior |
| :--- | :--- |
| local pending alias 尚未 sync | 顯示 pending alias，但保留 canonical id 與 sync 狀態 |
| Central 回 `409 conflict` | 顯示 conflict，不能把本地 alias 當已成功 truth |
| App 只連到 `CC bridge`，`Gateway` / `End Device` 不在當前 BLE 可達範圍 | 可顯示 `CC bridge` 轉述或承載的 Central-backed metadata；若顯示其他對象名稱，必須標示為 relayed / cached，不得當成當前第一手 BLE 名稱 |
| 無 Central alias 但有 `DEVICE_ALIAS` | 可用作 fallback display，不升格成 canonical metadata |
| 只有 `adv_name` | 允許顯示，但視為最低階 fallback |
| failover 後 gateway 改變 | 不得因此改寫 End Device canonical identity |

## Downstream Mappings

| Kind | IDs |
| :--- | :--- |
| Primary requirements | `REQ-003`, `REQ-005` |
| App formal docs | `app-scope/03-identity-contract.md`, `app-scope/06-alias-qos-role.md` |
| Central formal docs | `alias-sync-spec.md`, `data-model.md` |
| Firmware formal docs | `data-model.md` |

## References

- [rml-lite.md](rml-lite.md)
- [requirements.md](requirements.md)
- [baseline-target-migration.md](baseline-target-migration.md)
- [app identity contract](../../ble_qos_app/docs/specs/app-scope/03-identity-contract.md)
- [app alias / qos / role](../../ble_qos_app/docs/specs/app-scope/06-alias-qos-role.md)
- [central alias sync spec](../../central-device-metadata/docs/specs/alias-sync-spec.md)
- [central data model](../../central-device-metadata/docs/specs/data-model.md)
- [firmware data model](../../ble_qos_demo_V1.2m/docs/01_definition/02_contract/data-model.md)
