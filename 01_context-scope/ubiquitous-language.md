# Ubiquitous Language

> arc42 §3 + DDD core. Canonical vocabulary for all 4 repos.
> renamed from: glossary.md (git mv to arc42 location, PR#3).
> Machine-readable authority boundary → [authority-map.yaml](authority-map.yaml) (commit 3/8).

## 角色（Roles）

| Role | Definition | Authority | Owner Repo |
|---|---|---|---|
| ED (End Device) | BLE peripheral sensor node | None | firmware |
| GW (Gateway) | BLE dual-role aggregator | local QoS + roster | firmware |
| CC bridge firmware | BLE-to-Central relay (transport only, NOT authority) | none | firmware |
| Central | Backend system | canonical truth (identity, assignment, metadata) | central-device-metadata |
| Mobile / App | Phone client | local view state + Central offline cache | ble_qos_app |

## 韌體 Role Enum (NVS 儲存值)

衍生自 `ble_qos_demo_V1.2m/ble_api.yaml:nvs_roles` SSOT（codegen → `src/generated/nvs_roles.h`）：

| Constant | Value | Description |
|---|---|---|
| `NVS_ROLE_END_DEVICE` | 0x00 | ED 角色 |
| `NVS_ROLE_GATEWAY` | 0x01 | GW 角色 |
| `NVS_ROLE_REPEATER` | 0x02 | reserved（未實作）|
| `NVS_ROLE_RESERVED_3` | 0x03 | reserved |
| `NVS_ROLE_CC` | 0x04 | CC bridge 角色 |

注意：App side 用 `APP_ROLE_*` 命名（值不同，從 0 連續），不可混用。

## Spec ID 命名規範

| Prefix | Meaning | Owner Repo | Example |
|---|---|---|---|
| F-NN | Feature ID（跨 repo） | spec-pack | F-04 GW QoS scheduler tuning |
| FW-NN[A/B] | Firmware spec phase | firmware | FW-3A CMD_V2 length guard |
| A-N | App work item | app | A-1 Dart model schema |
| C-N | Central work item | central | C-1 spec-contract review |
| S-N | System / spec-pack work | spec-pack | S-1 AC catalog |
| X-N | Cross-repo coordination | spec-pack | X-1 wire parity test |
| W##[A-Z] | Wave（per-repo internal planning） | per-repo | W26D F-04 Central API |

## F-04 vs FW-3A 命名澄清

- **F-04** GW QoS scheduler tuning：跨三個 repo 的 feature ID。Owner = spec-pack
  `03_building-blocks/F-04-gw-qos-scheduler-tuning/tuning.md`
- **FW-3A** CMD_V2 per-opcode length guard：firmware spec phase，**F-04 韌體工作的子集**。
  Owner = firmware repo。
- 兩者層次不同，**禁止混用**。Documentation 引用時必須使用完整 prefix。

## Wire 名詞

衍生自 `ble_api.yaml`（firmware repo SSOT），下列只列語意說明，數值見原始定義：

| Term | 定義 | 參考 |
|---|---|---|
| CMD_V2 | Transaction-based command characteristic | `ble_api.yaml` → characteristics.CMD_V2 |
| CMD_RESULT | CMD_V2 回應 characteristic（subscribe for async result） | `ble_api.yaml` → characteristics.CMD_RESULT |
| CAPS_V2 | CBOR-encoded capability map（取代 CAP v1） | `ble_api.yaml` → characteristics.CAPS_V2 |
| TUNE-VAL | QoS scheduler preset 參數包（opcode 0x07 payload） | `ble_api.yaml` → opcodes 0x07 + TUNE-VAL rules |
| Preset | BALANCED / AGGRESSIVE / CONSERVATIVE 三種 QoS 排程策略 | `ble_api.yaml` → presets: |
| Zone | NEAR / MID / FAR / EDGE — PHY + TX power 聯動區間 | firmware `.claude/rules/qos-zones.md` |
| MAX_ED | GW 每次最大 ED slot 數（compile-time 上限，runtime 可降） | `ble_api.yaml` → system_constants.MAX_ED |
| CMD_V2_TIMEOUT_MS | App 端 CMD_V2 等待 timeout | `ble_api.yaml` → system_constants.CMD_V2_TIMEOUT_MS |

## 流程詞彙

| Term | 定義 |
|---|---|
| plan → spec → impl → integration | 4-gate acceptance pipeline（見 Phase 2 acceptance pipeline） |
| handoff | Cross-session 工作交接文件，存於 `docs/handoffs/` |
| CURRENT.md | 各 repo 當前狀態 snapshot（`.claude/CURRENT.md`） |
| ADR | Architecture Decision Record，存於 `docs/decisions/` 或 `docs/adr/` |
| SSOT | Single Source of Truth — 數值只能有一個定義來源，其他引用 |

## NCS Version SSOT

NCS（nRF Connect SDK）版本 SSOT = firmware repo `scripts/dev.sh` 中的預設路徑：
```
NCS_HOME:=$HOME/ncs/v2.9.2   # 見 dev.sh line ~32
```
文件引用時請寫「見 `scripts/dev.sh`」，不得硬編碼版本號。

## 身份識別詞彙（Identity）

| Term | Canonical Form | camelCase (Dart/JS) | snake_case (Python/C) | 定義 | Owner Repo |
|---|---|---|---|---|---|
| stableId / stable_id | `stableId` (Dart/JS), `stable_id` (Python/C) | `stableId` | `stable_id` | 裝置永久不變識別碼，由 Central 指派，跨 boot 保留 | central-device-metadata |
| deviceId / device_id | `deviceId` (Dart/JS), `device_id` (Python/C) | `deviceId` | `device_id` | App/Central 層裝置邏輯 ID（非 BLE MAC）；與 stableId 同義，Central 為準 | central-device-metadata |
| gateway_id | `gateway_id` | `gatewayId` | `gateway_id` | GW 的邏輯識別碼，由 Central 維護 | central-device-metadata |
| assignmentSyncState / assignment_sync_state | `assignmentSyncState` (Dart/JS), `assignment_sync_state` (Python/C) | `assignmentSyncState` | `assignment_sync_state` | App 與 Central 的指派同步狀態機（IDLE / SYNCING / IN_SYNC / CONFLICT） | ble_qos_app |
| assignment_state | `assignment_state` | `assignmentState` | `assignment_state` | Central 側裝置指派狀態（UNASSIGNED / ASSIGNED / PENDING_REMOVAL） | central-device-metadata |

## Alias 詞彙（Alias）

| Term | Canonical Form | camelCase (Dart/JS) | snake_case (Python/C) | 定義 | Owner Repo |
|---|---|---|---|---|---|
| alias | `alias` | `alias` | `alias` | 使用者為裝置設定的顯示名稱，App 端顯示用 | ble_qos_app |
| DEVICE_ALIAS / device_alias | `DEVICE_ALIAS` (C macro), `device_alias` (Python) | `deviceAlias` | `device_alias` | 韌體 NVS 儲存的裝置別名字串，CC 路徑也使用 | firmware |
| central_alias | `central_alias` | `centralAlias` | `central_alias` | Central 端維護的標準化別名（優先於 DEVICE_ALIAS） | central-device-metadata |

## Domain 行為詞彙（Domain Behavior）

| Term | Canonical Form | camelCase (Dart/JS) | snake_case (Python/C) | 定義 | Owner Repo |
|---|---|---|---|---|---|
| failover | `failover` | `failover` | `failover` | GW 主鏈失效後自動切換備援路徑的機制；跨 4 repo 核心術語 | firmware (primary) |
| reconciliation / reconcile | `reconciliation` | `reconciliation` | `reconciliation` | App / Central 之間狀態對帳（expected vs actual）；FEA-004 主題詞 | central-device-metadata |
| heartbeat | `heartbeat` | `heartbeat` | `heartbeat` | ED 定期傳送的存活信號；韌體週期發送，Central 依此判斷 online/offline | firmware |
| last_seen | `last_seen` | `lastSeen` | `last_seen` | Central 最後一次收到裝置訊號的 UTC timestamp | central-device-metadata |
| peer_id | `peer_id` | `peerId` | `peer_id` | 韌體 BLE 連線層的對端識別碼（connection handle 層） | firmware |
| retry_count | `retry_count` | `retryCount` | `retry_count` | CMD_V2 / API call 重試次數計數 | firmware (primary) |

## 遙測詞彙（Telemetry）

| Term | Canonical Form | camelCase (Dart/JS) | snake_case (Python/C) | 定義 | Owner Repo |
|---|---|---|---|---|---|
| rssi | `rssi` | `rssi` | `rssi` | Received Signal Strength Indicator（dBm），BLE 信號強度量測值 | firmware (primary) |
| tx_power | `tx_power` | `txPower` | `tx_power` | 發送功率（dBm），與 Zone 聯動控制 | firmware |
| ed_count | `ed_count` | `edCount` | `ed_count` | GW 目前管理中的 ED 數量；Central 使用此統計做 load 評估 | firmware (primary) |
| boot_id | `boot_id` | `bootId` | `boot_id` | 每次韌體重啟遞增的識別碼，用於區分連線 session | firmware |
| msg_seq | `msg_seq` | `msgSeq` | `msg_seq` | 訊息序號，用於重複偵測與有序確認 | firmware |

## HA / 同步詞彙（High Availability / Sync）

| Term | Canonical Form | camelCase (Dart/JS) | snake_case (Python/C) | 定義 | Owner Repo |
|---|---|---|---|---|---|
| uplink_ring | `uplink_ring` | `uplinkRing` | `uplink_ring` | GW 上行路徑環形緩衝佇列，failover 路徑切換單元 | firmware |
| uplink_class | `uplink_class` | `uplinkClass` | `uplink_class` | 上行流量分類（A/B/C），決定優先權與重試策略 | firmware |
| UL_CLASS_A | `UL_CLASS_A` | `ulClassA` | `UL_CLASS_A` | 最高優先 uplink class，不可延遲 | firmware |
| UL_CLASS_B | `UL_CLASS_B` | `ulClassB` | `UL_CLASS_B` | 中優先 uplink class，允許短延遲 | firmware |
| UL_CLASS_C | `UL_CLASS_C` | `ulClassC` | `UL_CLASS_C` | 低優先 uplink class，允許 backoff | firmware |
| ed_roster | `ed_roster` | `edRoster` | `ed_roster` | GW 維護的 ED 清單（含狀態），roster 的 ED 子集 | firmware |
| roster | `roster` | `roster` | `roster` | GW 所有已知節點清單（ED + CC），persistence 在 NVS | firmware |

## BLE 協定詞彙（BLE Protocol）

| Term | Canonical Form | camelCase (Dart/JS) | snake_case (Python/C) | 定義 | Owner Repo |
|---|---|---|---|---|---|
| phy | `phy` | `phy` | `phy` | BLE 物理層模式（1M / 2M / Coded）；與 Zone 聯動 | firmware |
| gatt | `gatt` | `gatt` | `gatt` | Generic Attribute Profile — BLE 服務/特徵值協定層 | firmware |
| discovery | `discovery` | `discovery` | `discovery` | App 掃描並識別 GW/ED 服務的流程 | firmware |
| advertising | `advertising` | `advertising` | `advertising` | 裝置廣播 BLE adv packet 的行為 | firmware |
| scanning | `scanning` | `scanning` | `scanning` | App / GW 掃描附近裝置的行為 | ble_qos_app (primary) |
