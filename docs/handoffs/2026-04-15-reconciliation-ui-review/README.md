# Reconciliation UI Review Mock

Page-by-page review。一次只看一頁，上一頁通過後才做下一頁。

**Wave 1 status**：所有 4 頁已 passed。收尾摘要 + accepted commits + 下一步建議見 [WAVE1-COMPLETE.md](WAVE1-COMPLETE.md)。

## Review 順序

| # | 頁面 | 回答什麼 | 狀態 |
|---|------|---------|------|
| 1 | [01-entry-list.html](01-entry-list.html) | 入口：現在可以連誰？哪個對象值得先連？ | Passed |
| 2 | [02-detail-summary.html](02-detail-summary.html) | 連線後 peer overview + role-based information layering（巡視人員 / Engineer） | Passed |
| 3 | [03-central-vs-runtime.html](03-central-vs-runtime.html) | Central vs Runtime 並列差異視圖 + resolution action strip | Passed |
| 4 | [04-evidence-panel.html](04-evidence-panel.html) | Evidence panel：為什麼 UI 這樣判斷？ | Passed |

## 第 1 頁設計原則

入口頁 = 選擇要連線的對象。

- 每個 peer 只有 3 個元素：人類看得懂的名稱、一句極短狀態、`Connect` 按鍵
- 不顯示工程代號（GW-A / ED id 等）
- 不顯示成員數量（ED count、members）
- 不提供任何 rename / edit 入口
- 所有詳細資料都在連線後才讀取
- Group / peer 顯示名稱屬於 Central/App 側可見 metadata，不代表 firmware runtime 也持有相同命名

## 第 2 頁設計原則

詳見 [page-2-design.md](page-2-design.md)。摘要：peer operational overview + 巡視人員 / Engineer 分層；reconciliation 為 exception flow；Gateway 視角用 overview + accordion；4 層 update strategy；freshness 用詞分層（最後更新 / 上次同步 / 最後看到）。

## 第 3 頁設計原則

詳見 [page-3-design.md](page-3-design.md)。摘要：左 Central authoritative / 右 Runtime observed 並列；5 情境切換；resolution action strip 明示下一步；Conflict 採非對等動作（primary `Recover runtime` + danger `Accept runtime as new assignment`）；raw evidence 留 Page 4。

## 第 4 頁設計原則

詳見 [page-4-design.md](page-4-design.md)。摘要：evidence detail 層；first screen 是 summary（state + 結論 + compare gate + recommended action）；Central / Runtime dual evidence card 攤開 raw 欄位；compare gate card 允許露 internal key；recent timeline 限 3–5 條；action confirmation hint 註明 Engineer role / reason / audit；情境：Conflict / Not compared / Central only。

## Rename boundary

Rename 不屬於 Page 1 / Page 2 的範圍：

- 不屬於 pre-connect entry（Page 1）
- 不屬於 operational overview（Page 2）
- 屬於後續 metadata / manage flow，非本輪 UI mock 範圍
- Canonical name 由 Central 擁有
- Firmware `DEVICE_ALIAS` 是 fallback / rescue，不是 canonical source
- 運維人員在 runtime 改的是 value / command / mode；改名走工程 / 管理層路徑

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
