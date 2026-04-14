# Reconciliation UI Review Mock

Page-by-page review。一次只看一頁，上一頁通過後才做下一頁。

## Review 順序

| # | 頁面 | 回答什麼 | 狀態 |
|---|------|---------|------|
| 1 | [01-entry-list.html](01-entry-list.html) | 入口：現在可以連誰？哪個對象值得先連？ | **Ready for Roy review** |
| 2 | 02-detail-summary.html | 連上後的對象摘要與成員清單 | 待第 1 頁通過 |
| 3 | 03-central-vs-runtime.html | Central vs Runtime 怎麼並列？ | 待第 2 頁通過 |
| 4 | 04-evidence-panel.html | 追證據去哪裡看？ | 待第 3 頁通過 |

## 第 1 頁設計原則

入口頁不是狀態展示板，是「選誰連線」的選擇題。

- **主體是 connectable peers**：GW group / CC bridge / orphan ED
- **不展開 ED 清單**，只顯示成員數量摘要
- **此頁所有摘要都是 cached / last-synced reference，不是 live truth**
- 用「上次同步皆正常 / 上次同步顯示有待確認」這類降級語言，避免被誤讀為 live judgement
- 改名 / 裝置操作 / live reconciliation / can_compare / evidence 都不在這層
- 每個 peer 都有 `Connect` 按鍵

## 操作

用 Chrome 直接打開 `01-entry-list.html`。

## 對應 formal spec

- `RML-FEA-001`（telemetry / value states）
- `RML-FEA-004`（assignment reconciliation）
- `REQ-007`（evidence basis）
- `REQ-008`（compare gate）
- `AC-004`（reconciliation + can_compare gate）
- `AC-007`（evidence visibility）

## 舊檔

`review.html` 是早期一次塞完整條 flow 的版本，保留為對照；正式 review 走 page-by-page。
