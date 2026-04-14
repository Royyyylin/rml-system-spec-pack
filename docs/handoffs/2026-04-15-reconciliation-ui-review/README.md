# Reconciliation UI Review Mock

Page-by-page review。一次只看一頁，上一頁通過後才做下一頁。

## Review 順序

| # | 頁面 | 回答什麼 | 狀態 |
|---|------|---------|------|
| 1 | [01-entry-list.html](01-entry-list.html) | 使用者第一眼看到什麼？哪些該點？ | **Ready for Roy review** |
| 2 | 02-detail-summary.html | 點進去後怎麼理解？ | 待第 1 頁通過 |
| 3 | 03-central-vs-runtime.html | Central vs Runtime 怎麼並列？ | 待第 2 頁通過 |
| 4 | 04-evidence-panel.html | 追證據去哪裡看？ | 待第 3 頁通過 |

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
