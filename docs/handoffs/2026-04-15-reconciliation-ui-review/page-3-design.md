# Page 3 — Central vs Runtime 設計原則

主檔：[README.md](README.md)　Mock：[03-central-vs-runtime.html](03-central-vs-runtime.html)

## Layout / vocabulary

- 由 Page 2 conflict banner「查看差異」進入，主畫面 = Central vs Runtime 並列
- 兩側分明：左側 Central（authoritative · 後台分配）、右側 Runtime（observed · 現場觀測）；視覺上不靜默合併
- 每側都顯示 freshness（最後更新 / 上次同步）與對應 tag（fresh / stale / last synced / 尚未回報）
- 5 個切換情境：`converged` / `conflict` / `pending_reconciliation` / `central_only` / `not compared`
- diff hint 條同步說明 reviewer 下一步注意點；UI 上以「可比對 / 不可比對」呈現，對應 internal `can_compare` gate（不直接寫 `can_compare = true/false`）
- 主畫面 state label 用人類可讀短詞（Converged / Conflict / Pending sync / Central only / Not compared）；formal enum 留在 spec 與 README，不出現在 phone surface
- 用詞延用 Page 2 freshness 分層（最後更新 = runtime / 上次同步 = central），不引入新 vocabulary
- 不在本頁攤開 raw timestamp / revision / observed_at；證據細節屬 Page 4

## UI scenario ↔ formal FSM mapping

UI 顯示的 5 個 scenario ≠ spec FSM 的 5 個 state。對照：

| UI scenario | 對應 spec | 說明 |
|------------|----------|------|
| Converged | FSM `confirmed` | |
| Conflict | FSM `conflict` | |
| Pending sync | FSM `pending_reconciliation` | |
| Central only | FSM `central_only` | `can_compare = true`，Runtime fresh 但 attach not visible |
| Not compared | **pre-FSM gate** result（非 FSM state） | `can_compare = false`，Central stale / source 缺，不進 FSM |

正式 FSM 的 `orphaned` state 不在本輪 Page 3 / Page 4 mock 顯示。

## Resolution action

Conflict 不只是顯示狀態；Page 3 在 diff hint 下方加一條 resolution action strip，明示 reviewer 下一步：

- **Conflict**：primary `Recover runtime`（Central 是 canonical default）；danger 替代 `Accept runtime as new assignment`（明示需 Engineer 確認 / audit）；link `View evidence`
- **Pending sync**：`Wait for sync` + `View evidence`（不要叫人選哪邊正確）
- **Central only**：`Wait for runtime` / `Send check command` / `View evidence`
- **Not compared**：`Refresh Central` + `View evidence`（先取得 fresh Central 再判定）
- **Converged**：`No action needed`，僅低權重 `View evidence`

不做成「Central / Runtime 兩邊等權選正確」— 兩側角色不對等：Central 是 canonical assignment，Runtime 是 observed evidence。所有 action 在本輪皆為 mock，未串實作；危險動作以紅框 outline + 註記呈現權重差異。
