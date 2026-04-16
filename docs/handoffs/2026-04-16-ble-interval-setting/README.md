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

- **Preset first**：3 個 preset（Responsive / Balanced / Conservative），每個一句人話描述
- **Advanced override second**：預設收合；展開才看到 raw `Min interval` / `Max interval`，標示單位（BLE units 1.25 ms）並換算 ms
- **Guardrail 文案**：明示「進階設定，建議先用 preset；不建議在巡視模式調整」
- **Apply path**：明畫 `App (Engineer) → CTRL.interval → GW → ED link param update`
- **不要把 `GW_CFG`** 畫成 interval owner
- **不要出現** packet / throughput interval 設定

## 對應現有 spec

- 本 mock 不改動 spec wording
- 引用既有 `CTRL.interval` 欄位（屬 firmware SSOT `ble_api.yaml`）
- Engineer role 概念對齊 app repo 既有 `normal / maintenance / engineer`，本 mock 仍以「Engineer」呈現

## 不在本輪範圍

- packet / throughput / send interval
- 多 GW 或 group-level interval policy
- App repo / firmware 實作
- 正式 spec wording 變更
