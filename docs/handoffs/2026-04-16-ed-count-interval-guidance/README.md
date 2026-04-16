# ED-count Guided Interval Recommendation

依「Power class（Powered / Battery）」與「同時連線 ED 數」給出三個建議值，幫 Engineer / 佈場人員快速判斷該如何設參。

**Review 入口**：[review.html](review.html)（Chrome 打開）

## 這包是要回答什麼

- 不是 runtime patrol 主畫面
- 不是正式設定頁實作
- 是 Engineer / 佈場時的 **guided guidance**
- 一次回答 3 個 timing 值：
  - BLE connection interval
  - Packet / data send interval
  - Connection supervision timeout
- 依據：power class（Powered / Battery）+ Connected ED count（1–3 / 4–5 / 6–8 / 9+）

## 短決策表

| 問題 | 答案 |
|------|------|
| 哪兩個受 ED count **強影響** | `BLE connection interval`、`Packet / data send interval` |
| 哪一個是 **間接影響** | `Connection supervision timeout`（隨 link 壓力與 interval 一起放寬）|
| 哪條路 **不該慢下來** | `event / alarm` path — 保持 event-driven，不跟 cadence 變慢 |

## 建議值（mock 內初版）

### Powered ED

| ED 數 | connection interval | packet send interval | supervision timeout |
|-------|---------------------|----------------------|---------------------|
| 1–3 | 100 ms | 100–200 ms | 4–6 s |
| 4–5 | 200 ms | 200–500 ms | 6–8 s |
| 6–8 | 500 ms | 500–1000 ms | 8–12 s |
| 9+ | 1000 ms | 1–2 s | 12–20 s |

### Battery ED

| ED 數 | connection interval | packet send interval | supervision timeout |
|-------|---------------------|----------------------|---------------------|
| 1–3 | 較保守 | 1–5 s | 10–20 s |
| 4–5 | 較保守 | 5–10 s | 15–20 s |
| 6+ | 較保守 | 10–30 s | 20 s 左右 |

備註：Battery 這組刻意不寫精確 BLE units；本輪是 guided recommendation，不是最終 protocol constant。

## 兩層結構

這包現在分兩層：

1. **Install entry**（首要）—— 直接輸入 Powered / Battery ED 數量，自動算出 Total 與 3 個建議值
2. **Engineer Advanced override**（次要）—— 預設收合；展開後可手動輸入 ms / s

Recommendation 仍是第一優先；Apply recommended 會把 3 個建議值填回 override。

## Mixed conservative rule

當 `Powered ED count > 0` 且 `Battery ED count > 0` 時為 Mixed。

計算步驟：
1. 依 Powered count 算一組 Powered recommendation
2. 依 Battery count 算一組 Battery recommendation
3. 逐項取「較保守」者：
   - BLE connection interval：數值較大者
   - Packet / data send interval：取較慢的那一組
   - Connection supervision timeout：取較長的那一組

UI 顯示：`Recommendation basis: Mixed (conservative) · Calculated from Powered X + Battery Y`

## Bucket

- Powered：1–3 / 4–5 / 6–8 / 9+
- Battery：1–3 / 4–5 / 6+
- 任一 count = 0 → 該類別不參與 Mixed conservative 比較

## 空狀態

Powered = 0 且 Battery = 0 → 顯示 `Enter device counts to get recommended settings`，Apply 按鈕 disabled。

## Override 欄位

- BLE connection interval（ms 輸入 + 即時換算 BLE units，100–1000 ms）
- Packet / data send interval（單位隨情境切換 ms ↔ s；Powered 100 ms – 2 s / Battery 1 s – 60 s）
- Supervision timeout（s 輸入；Powered 4–20 s / Battery 10–30 s）
- Guardrail：先用 recommendation；不要比 recommendation 更激進；event / alarm 不跟 cadence 慢

## 重要限制

- Mixed conservative 是 UI recommendation 邏輯，不是新 protocol
- 不新增任何 wire field
- 不改既有正式 spec wording

## 不在本輪範圍

- 既有 `2026-04-16-ble-interval-setting/` 不動
- 不做正式設定頁實作
- 不畫到 Page 1 / Page 2 主 flow
- 不發明新 wire field、不改 spec wording
