=== FILE: docs/architecture.md ===
# 系統架構與模組 (Architecture)

## 模組列表與責任
- **BLK-001 (App-UI)**: 負責 L1/L2/L3 介面渲染與使用者輸入。
- **BLK-002 (GW-Roster)**: 負責維護 ED 清單與連線狀態。
- **BLK-003 (Comm-Manager)**: 負責 BLE GATT 讀寫與封包解析。
- **BLK-004 (State-Sync-Engine)**: 負責 App 與 GW 之間的狀態一致性檢查與恢復。

## 輸入/輸出
- **Input**: BLE GATT Notification (STATUS char 0x2A1D), BLE GATT Indication (ERROR char 0x2A1E).
- **Output**: BLE GATT Write (Action command char 0x2A1F).

## 外部依賴
- **GATT Service**: 0x1801 (Generic Attribute), 0x1800 (Generic Access).
- **Custom Service**: 0xFF01 (Industrial Device Service).

---

=== FILE: docs/state_machine.md ===
# 狀態機定義 (State Machine)

## State List
- **STA-001 (Active)**: 正常運作狀態。
- **STA-002 (Maintenance)**: 維護模式，部分功能鎖定。
- **STA-003 (Pending Sync)**: 狀態變更中，等待 GW 確認。
- **STA-004 (Needs Review)**: 狀態衝突或同步失敗，需人工介入。
- **STA-005 (Disabled)**: 裝置停用狀態。

## Transitions
- **Event-001 (Enter Maintenance)**: Active -> Pending Sync -> Maintenance.
- **Event-002 (Sync Success)**: Pending Sync -> Maintenance.
- **Event-003 (Sync Timeout)**: Pending Sync -> Needs Review (Recovery Path).
- **Event-004 (Error Received)**: Pending Sync -> Needs Review.
- **Event-005 (Force Sync)**: Needs Review -> Pending Sync -> Active/Maintenance.

## Timeout & Retry
- **Timeout**: 5s (等待 GW 回傳 ACK)。
- **Retry**: 3 次 (每次間隔 1s)。
- **Retry Exhaustion**: 若 3 次重試皆失敗，進入 `STA-004 (Needs Review)`。

## Failure Handling
- 若收到 `PKT-002 (Error Packet)`，App 應立即停止重試並進入 `Needs Review`。
- 若裝置重啟，狀態機應重置為 `Active` 並等待第一次 STATUS 封包校準。

---

=== FILE: docs/sequence_flows.md ===
# 通訊時序 (Sequence Flows)

## Actors
- **App**: Phone App.
- **GW**: Gateway.
- **ED**: End Device.

## Trigger
- 使用者在 L2 詳情頁點擊 `Enter Maintenance`。

## Main Flow (SEQ-001)
1. App 發送 `Action: Enter Maintenance` 封包至 GW。
2. GW 更新本地 `gw_point_state` 為 `maintenance`。
3. GW 回傳 `ACK` 給 App。
4. App 更新 UI 顯示 `Maintenance` 狀態。

## Error Path (SEQ-002)
1. App 發送 `Action: Enter Maintenance`。
2. GW 發現 ED 離線，無法執行動作。
3. GW 回傳 `PKT-002 (Error Packet)`，錯誤碼 `0x01 (Device Offline)`。
4. App 停止重試，UI 顯示 `Sync Failed: Device Offline` 並進入 `Needs Review`。

## Reboot Recovery Path (SEQ-003)
1. ED 重啟。
2. GW 偵測到 ED 連線，更新 Roster 狀態。
3. GW 主動發送 `PKT-001 (STATUS)` 給 App。
4. App 接收封包，校準本地狀態為 `Active`。
