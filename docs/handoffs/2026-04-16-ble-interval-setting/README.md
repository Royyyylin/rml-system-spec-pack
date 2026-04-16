# BLE Connection Interval — Engineer-only Setting

小型設計 mock，回答「GW ↔ ED 的 BLE connection interval 應該怎麼設定」。

**Review 入口**：[review.html](review.html)（用 Chrome 打開）

## Placement / Ownership

- **Engineer-only / Advanced wireless settings**
- **不屬於** pre-connect entry（Page 1）
- **不屬於** Page 2 operational overview（巡視主流程）
- 寫入目標：`CTRL.interval`
- **不是** `GW_CFG`（GW_CFG 不持有 BLE connection interval 欄位）
- 本輪只處理 **BLE connection interval**，不處理 packet / throughput interval

## 決策表

| 問題 | 決策 |
|------|------|
| 放哪裡 | Advanced wireless settings · Engineer path（不放主畫面） |
| 誰能改 | Engineer only |
| 先怎麼改 | Preset 優先（Responsive / Balanced / Conservative） |
| 真正寫哪裡 | `CTRL.interval` |

## UI 原則

- **Preset first**：3 個 preset，**每個直接列出實際 interval（BLE units + ms）**
  - Responsive：`80 units · 100 ms`
  - Balanced：`160 units · 200 ms`（預設）
  - Conservative：`400 units · 500 ms`
- **Advanced override second**：預設收合；展開才看到 raw `Min interval` / `Max interval`，標示單位（BLE units 1.25 ms）並換算 ms
- **Guardrail 文案**：明示「進階設定，建議先用 preset；不建議在巡視模式調整」
- **Apply path**：明畫 `App (Engineer) → CTRL.interval → GW → ED link param update`
- **不要把 `GW_CFG`** 畫成 interval owner
- **不要出現** packet / throughput interval 設定

## 用詞與 preset bucket 決策

- **Preset 卡顯示實際 interval**：不能只給形容詞；engineer 需要直接看出三個 preset 的 interval 差異與換算
- **用 `連線間隔` / `BLE connection interval`，不用 `延遲`**：避免和 telemetry latency 混淆
- **`1000 ms` 不列入主 preset**：主 preset 對應目前常用 bucket（100 / 200 / 500 ms）；更慢值留在 advanced override 由 engineer 視情況指定，不浪費 preset 槽位

## 對應現有 spec

- 本 mock 不改動 spec wording
- 引用既有 `CTRL.interval` 欄位（屬 firmware SSOT `ble_api.yaml`）
- Engineer role 概念對齊 app repo 既有 `normal / maintenance / engineer`，本 mock 仍以「Engineer」呈現

## 不在本輪範圍

- packet / throughput / send interval
- 多 GW 或 group-level interval policy
- App repo / firmware 實作
- 正式 spec wording 變更
