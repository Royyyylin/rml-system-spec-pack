# Connection State vs BLE Connection Interval vs Packet Send Interval

整理三個常被混淆的概念，避免後續 mock / spec / handoff 把它們綁在同一個設定旋鈕。

## 三者快速區分

### 1. Connection state（連線狀態）

- **本質**：state，不是 configurable timing
- **代表**：GW ↔ ED 此刻有沒有 BLE 連線（connected / disconnected）
- **不該與誰混**：不是一個可以「調長短」的 interval；要表達「沒連上」就用 disconnected，不要去調 interval
- **典型呈現**：UI 上的 `Alive / Offline`、`Connected / Disconnected` 狀態徽章

### 2. BLE connection interval（BLE 連線間隔）

- **本質**：configurable timing（已連線後的底層節奏）
- **代表**：連線存在時，BLE link 多久排一次 connection event 可交換資料
- **單位**：BLE units（1.25 ms / unit）；常用值 100 / 200 / 500 ms
- **寫入目標**：`CTRL.interval`（不是 `GW_CFG`）
- **不該與誰混**：
  - 它**不能**用來判斷有沒有連線（連線狀態請看 connection state）
  - 它**不是**應用層送資料的頻率（送資料頻率是 packet send interval）

### 3. Packet / data send interval（資料送出間隔）

- **本質**：configurable timing（應用層節奏）
- **代表**：在 BLE 連線存在的前提下，應用資料（telemetry、heartbeat 等）多久真的被送出一次
- **不該與誰混**：
  - 它**不是** BLE link state；無論有沒有送 packet，連線可能仍在
  - 它**不是** BLE connection interval；application send rate 通常 ≪ link interval bucket，由上層 schedule 決定

## 對照表

| 名稱 | 本質 | 白話 | Owner / 決策層 |
|------|------|------|---------------|
| Connection state | state | 有沒有通話中 | runtime observation（Firmware 第一手；UI 顯示） |
| BLE connection interval | configurable timing | 通話中多久輪到你能講一次 | Engineer 進階設定 → `CTRL.interval` → GW → ED |
| Packet send interval | configurable timing | 你多久真的講一句話 | 應用層 / telemetry schedule（不在本輪 mock 範圍） |

## 產品原則

**不要把這三者塞進同一個設定旋鈕。**

- 顯示「沒連上」就用 disconnected，不要透過調 interval 表達
- 調 BLE link 節奏走 Engineer-only Advanced wireless settings（preset first / advanced override second）
- 調應用資料送出頻率屬另一條 flow，目前不在 BLE interval 設定畫面範圍

## 一行記憶

- `connected / disconnected` = 是否通話中
- `connection interval` = 通話中多久輪到你能講一次
- `packet send interval` = 你多久真的講一句話

## 相關 handoff

- BLE connection interval 設定 mock：[../2026-04-16-ble-interval-setting/](../2026-04-16-ble-interval-setting/)
- Page 2 連線後 operational overview（呈現 connection state）：[../2026-04-15-reconciliation-ui-review/02-detail-summary.html](../2026-04-15-reconciliation-ui-review/02-detail-summary.html)
