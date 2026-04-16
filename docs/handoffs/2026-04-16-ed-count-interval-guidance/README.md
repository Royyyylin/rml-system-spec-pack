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

## 不在本輪範圍

- 既有 `2026-04-16-ble-interval-setting/` 不動
- 不做正式設定頁實作
- 不畫到 Page 1 / Page 2 主 flow
- 不發明新 wire field、不改 spec wording
