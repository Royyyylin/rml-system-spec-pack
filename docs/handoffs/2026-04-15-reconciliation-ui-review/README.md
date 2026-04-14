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
- **詳細資料一律在連線後讀取**：can_compare、timestamp、reconciliation 等都不在這層
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
