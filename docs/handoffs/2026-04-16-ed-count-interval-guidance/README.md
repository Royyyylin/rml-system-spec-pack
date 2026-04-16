# Quick Start — ED-count Interval Wizard

3-step commissioning wizard：填數量 → 看建議 → 必要才微調。系統帶順序、做 validation，安裝人員不必自己記。

**Review 入口**：[review.html](review.html)

## 流程

| Step | 內容 | 必經 |
|------|------|------|
| 1 | Device mix — 輸入 Powered ED + Battery ED 數量 | ✓ |
| 2 | Recommended settings — 自動算出 3 個建議值；按 `Apply recommended` 帶入 override | ✓ |
| 3 | Engineer override — 預設收合，僅在 Step 2 後可進入 | 選用 |

預設安裝路徑：Step 1 → Step 2 → `Apply recommended` 結束。

## Mixed conservative rule

當 Powered count > 0 且 Battery count > 0 為 Mixed。逐項取較保守：
- BLE connection interval：較大 ms
- Packet / data send interval：較慢 range
- Connection supervision timeout：較長 s

UI 顯示：`Mixed (conservative) · Calculated from Powered X + Battery Y`

## Bucket

- Powered：1–3 / 4–5 / 6–8 / 9+
- Battery：1–3 / 4–5 / 6+
- 任一 count = 0 → 該類別不參與 Mixed 比較

## Validation

### Hard error（紅字、Apply custom disabled）

1. 任一欄位空值 / ≤ 0
2. CI 超出 100–1000 ms
3. PI 超出範圍：Powered 100 ms – 2 s / Battery 1 s – 60 s / Mixed 100 ms – 60 s
4. ST 超出範圍：Powered 4–20 s / Battery / Mixed 10–30 s
5. recommendation 未建立（Step 1 都 0）
6. ST 太短不足以支撐 CI（保守檢查：supervision_ms ≥ 2 × CI_ms；UI 文案：`Supervision timeout is too short for the selected connection interval`）

### Soft warning（黃字、可送出）

- CI / PI / ST 比 recommendation 更激進
- Battery only：CI < 500 ms 或 PI < 1 s
- Mixed：低於 conservative recommendation
- Total ≥ 6：CI ≤ 200 ms 或 PI < 500 ms
- 全部剛好等於 recommendation → 不出 warning

### Validation summary 顯示

- 有 hard error：`Fix N errors`
- 無 error 但有 warning：`Ready to apply · N warnings`
- 都沒有：`Ready to apply`

## 不在本輪範圍

- Mixed conservative 與 validation 都是 UI recommendation 邏輯，不是新 protocol
- 不新增任何 wire field
- 不改既有正式 spec wording
