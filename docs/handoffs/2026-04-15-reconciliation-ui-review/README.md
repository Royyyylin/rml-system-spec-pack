# Reconciliation UI Review Mock

互動式 HTML mock，模擬 App detail screen 的 reconciliation / freshness / can_compare 行為，讓 reviewer 驗證語意是否看得懂。

**這不是正式 App 實作**，是 spec-pack 的 human review mock。

## 操作方式

直接用 Chrome 開 [review.html](review.html)。

## 先操作這 4 個 scenario（左側 tabs）

1. `confirmed` — Central 與 runtime 都指向同一台 Gateway
2. `pending_reconciliation` — runtime 先切換，Central 還沒跟上（正常 failover 延遲）
3. `not compared / last synced` — Central 當前不可達，只能看快取
4. `conflict` — 雙方都 fresh 但指向不同 Gateway

## Toggle（補充互動）

- `Live Central available` — 關閉時視為 Central 不可達
- `Central reference fresh` — 關閉時 Central 資料超過 freshness window

兩個 toggle 都會影響 `can_compare`，並改變顯示狀態。

## 對應 formal spec

- `RML-FEA-001`（telemetry / value states）
- `RML-FEA-004`（assignment reconciliation）
- `REQ-007`（evidence basis）
- `REQ-008`（compare gate）
- `AC-004`（reconciliation + can_compare gate）
- `AC-007`（evidence visibility）
