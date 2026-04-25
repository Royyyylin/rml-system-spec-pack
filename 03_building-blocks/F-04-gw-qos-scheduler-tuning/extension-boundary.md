# GW QoS Extension Boundary — Config Apply vs Telemetry Profiling

主檔：[feature-gw-qos-scheduler-tuning.md](feature-gw-qos-scheduler-tuning.md)
Status: draft

## 目的

明確區分 F-04 scheduler tuning（config apply）與未來 telemetry profiling（可選欄位回報）的邊界，避免兩個 domain 混在同一個 wire protocol。

## Domain 分離

| Domain | 資料流 | F-04 scope？ |
|---|---|---|
| **Config Apply** | Central → BLE → Firmware | 是（CMD_V2 0x07） |
| **Telemetry Profiling** | Firmware → BLE → App/Central | 否，獨立 domain |

## Config Apply — F-04 原則

- Central API 提供 **catalog**（preset definitions + expert override schema + validation rules）
- App engineering mode 顯示 **checkbox / selector**，只能選 catalog-defined items
- BLE 只傳 **compact apply payload**（preset enum / profile_id / bitmask / compact config）
- Firmware 只接受 **known profile_id / bitmask / compact config**，reject 未知欄位
- 所有 firmware-bound payload 由 `ble_api.yaml` 定義

## Telemetry Profiling — 未來獨立 Domain

已知未來需求：
- PER（Packet Error Rate）
- 頻道幹擾偵測（channel interference detection）
- 白名單 / 黑名單機制
- 可選 reporting rate / experiment duration

### 架構原則（與 Config Apply 一致）

1. **Central catalog**：Central API 提供 predefined field list（每個 field 有 stable ID）
2. **App engineering mode**：從 catalog 勾選，不自創 payload
3. **BLE compact config**：profile_id 或 bitmask 告訴 firmware「這次報哪些欄位」
4. **Firmware predefined fields**：firmware 只知道已編譯的 field set，不接受 runtime 新增的未知 field
5. **`ble_api.yaml` wire truth**：新增 field 需先定義 wire encoding

### 不可做的事

| 禁止 | 原因 |
|---|---|
| App 自己組 JSON / BLE payload | Firmware 不認識 App 自創格式 |
| App 自己決定新欄位名稱 | 欄位由 spec + `ble_api.yaml` 定義 |
| App 繞過 `ble_api.yaml` 直接傳 firmware | Wire SSOT 被繞過 |
| 塞進 F-04 CMD_V2 0x07 | 語意不同、方向相反 |
| Firmware 接受未知 field ID | 安全風險 + debug 困難 |

## Factory-Rich Mode 原則

工廠內部署（短距離、穩定鏈路）可用更豐富的資料查詢，但仍遵循分層：

| 層 | 職責 |
|---|---|
| Central API | Rich query：catalog / schema / selectable fields / audit / history |
| App | 顯示 checkbox、呼叫 API、組合 UI，不自創 wire payload |
| BLE | Compact config apply / telemetry profile bitmask |
| Firmware | 按 profile 回報，不回完整 schema / metadata |

App engineering mode 可做：
- `GET .../telemetry-fields` → 拿 field catalog
- 勾選要啟用的 fields → `PUT .../telemetry-profile` 存到 Central
- Central 透過 App → BLE 把 compact profile_id / bitmask 下發到 firmware

App engineering mode 不可做：
- 不可在 BLE payload 裡自己加新欄位
- 不可把 Central API response 直接轉成 BLE write
- 不可要求 firmware 透過 BLE 回完整 field catalog

## SSOT 分佈

| 資料 | SSOT |
|---|---|
| Config Apply runtime truth | Central DB/API |
| Telemetry Profiling catalog / schema | Central DB/API（未來，需獨立定義） |
| Wire encoding（config apply + telemetry） | `ble_api.yaml` |
| Contract semantics | spec-pack |
| Field definitions | spec-pack + `ble_api.yaml` |
