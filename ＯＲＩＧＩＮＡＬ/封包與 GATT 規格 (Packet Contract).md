=== FILE: docs/packet_contract.md ===
# 封包與 GATT 規格 (Packet Contract)

## Packet ID: PKT-001 (GATT STATUS 0x2A1D)
- **Direction**: GW -> App (Notify).
- **Field Table**:
| Byte Offset | Field Name | Type | Meaning | Valid Range |
| :--- | :--- | :--- | :--- | :--- |
| 0 | Header | uint8 | 封包類型標頭 | 0x01 (Status) |
| 1 | Zone | uint8 | 訊號區域 | 0:NEAR, 1:MID, 2:FAR, 3:EDGE |
| 2 | RSSI | int8 | 訊號強度 (dBm) | -120 to 0 |
| 3 | PHY | uint8 | 實體層速率 | 0:1M, 1:2M, 2:Coded |
| 4 | TX Power | int8 | 發射功率 (dBm) | -8 to +8 |

## Packet ID: PKT-002 (GATT ERROR 0x2A1E)
- **Direction**: GW -> App (Indicate).
- **Field Table**:
| Byte Offset | Field Name | Type | Meaning | Valid Range |
| :--- | :--- | :--- | :--- | :--- |
| 0 | Header | uint8 | 封包類型標頭 | 0x02 (Error) |
| 1 | Error Code | uint8 | 錯誤代碼 | 0x01:Offline, 0x02:Busy, 0x03:Denied |
| 2 | Related ID | uint16 | 相關裝置 ID | 0x0000 to 0xFFFF |

---

=== FILE: docs/acceptance_criteria.md ===
# 驗收標準 (Acceptance Criteria)

| ID | Related REQ | Preconditions | Trigger | Observable Result | Timing Bound | Pass Condition | Fail Condition | Measurement Method |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AC-001** | REQ-001 | App 已連線至 GW。 | GW 發送 STATUS 封包。 | L2 詳情頁顯示正確 RSSI 與 Zone。 | 500ms | 顯示值與封包內容一致。 | 顯示值為空或與封包不符。 | 封包模擬器比對 UI。 |
| **AC-002** | REQ-002 | 裝置處於 Active 狀態。 | 點擊 Enter Maintenance。 | 狀態變更為 Maintenance。 | 5s | 狀態成功轉移且 UI 更新。 | 狀態未轉移或 UI 顯示錯誤。 | 手動操作測試。 |
| **AC-003** | REQ-003 | `sync_state == needs_review`。 | 嘗試點擊 Replace 按鈕。 | 按鈕應為不可點擊狀態。 | N/A | 按鈕被鎖定。 | 按鈕可點擊。 | UI 互動測試。 |
| **AC-004** | REQ-004 | App 已連線。 | 收到 PKT-002 (Error Code 0x01)。 | UI 顯示「Device Offline」。 | 1s | 錯誤訊息正確顯示。 | 訊息錯誤或未顯示。 | 故障注入測試。 |
| **AC-005** | REQ-005 | 裝置斷電重啟。 | 裝置重新上線並發送 STATUS。 | App 自動恢復連線並更新狀態。 | 10s | 狀態自動校準。 | 狀態停留在離線或錯誤。 | 斷電重啟測試。 |

---

=== FILE: docs/test_cases.md ===
# 測試案例 (Test Cases)

| ID | Related AC | Test Type | Setup | Steps | Expected Result | Logs / Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-001** | AC-001 | Normal | App 連線至模擬 GW。 | 1. 模擬器發送 RSSI -56dBm, Zone MID。<br>2. 觀察 App L2 頁面。 | L2 顯示 `-56 dBm` 與 `MID`。 | App Log: `Received STATUS 0x2A1D: RSSI=-56, Zone=1` |
| **TC-002** | AC-002 | Fault Injection | App 連線至模擬 GW。 | 1. 點擊 Enter Maintenance。<br>2. 模擬器不回傳 ACK。<br>3. 觀察 App 重試行為。 | App 重試 3 次後顯示 `Sync Failed`。 | App Log: `Retry 1/3... Retry 2/3... Retry 3/3... Timeout` |
| **TC-003** | AC-001 | Boundary | App 連線至模擬 GW。 | 1. 模擬器發送 RSSI -120dBm (臨界值)。<br>2. 觀察 App L2 頁面。 | L2 顯示 `-120 dBm`。 | App Log: `Received STATUS 0x2A1D: RSSI=-120` |
| **TC-004** | AC-004 | Error Recovery | App 連線至模擬 GW。 | 1. 點擊 Enter Maintenance。<br>2. 模擬器發送 PKT-002 (Error 0x01)。 | App 停止重試並顯示 `Device Offline`。 | App Log: `Received ERROR 0x2A1E: Code=0x01` |
| **TC-005** | AC-005 | Reboot | 真實裝置連線。 | 1. 裝置斷電再通電。<br>2. 觀察 App 狀態更新。 | App 在 10s 內恢復連線並顯示 `Active`。 | App Log: `Reconnected to Device... Received STATUS` |
