# STEP 3 — 文件骨架與示例內容 (Part 2)

## 4. docs/state_machine.md
```markdown
# 狀態機定義 (State Machine)

## State List
- **STA-001 (Active)**: 正常運作狀態。
- **STA-002 (Maintenance)**: 維護模式，部分功能鎖定。
- **STA-003 (Pending Sync)**: 狀態變更中，等待 GW 確認。

## Transitions
- **Event-001 (Enter Maintenance)**: Active -> Pending Sync -> Maintenance.
- **Event-002 (Sync Success)**: Pending Sync -> Maintenance.
- **Event-003 (Sync Timeout)**: Pending Sync -> Active (Recovery Path).

## Timeout & Retry
- **Timeout**: 5s (等待 GW 回傳 ACK)。
- **Retry**: 3 次 (每次間隔 1s)。

## Failure Handling
- 若 3 次重試失敗，App 應顯示 `Sync Failed` 標籤並回復至前一狀態。
```

## 5. docs/sequence_flows.md
```markdown
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

## Timeout Path (SEQ-002)
1. App 發送請求後 5s 未收到 ACK。
2. App 自動發起重試 (Retry 1/3)。
3. 若 3 次重試皆無回應，進入 Failure Response。

## Failure Response
- App 彈出 Toast 提示「連線逾時，請檢查 GW 狀態」。
```

## 6. docs/packet_contract.md
```markdown
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

## Error Handling Notes
- 若 RSSI 為 0x7F (127)，表示裝置離線。
- 若 Zone 超出 0-3 範圍，App 應顯示 `Unknown`。
```
