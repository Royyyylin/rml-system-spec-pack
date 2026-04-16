# Reconciliation UI Review Mock

Page-by-page review。一次只看一頁，上一頁通過後才做下一頁。

## Review 順序

| # | 頁面 | 回答什麼 | 狀態 |
|---|------|---------|------|
| 1 | [01-entry-list.html](01-entry-list.html) | 入口：現在可以連誰？哪個對象值得先連？ | Passed |
| 2 | [02-detail-summary.html](02-detail-summary.html) | 連線後 peer overview + role-based information layering（巡視人員 / Engineer） | Passed |
| 3 | [03-central-vs-runtime.html](03-central-vs-runtime.html) | Central vs Runtime 並列差異視圖（dual-source evidence） | **Ready for Roy review** |
| 4 | 04-evidence-panel.html | 追證據去哪裡看？ | 待第 3 頁通過 |

## 第 1 頁設計原則

入口頁 = 選擇要連線的對象。

- 每個 peer 只有 3 個元素：人類看得懂的名稱、一句極短狀態、`Connect` 按鍵
- 不顯示工程代號（GW-A / ED id 等）
- 不顯示成員數量（ED count、members）
- 不提供任何 rename / edit 入口
- 所有詳細資料都在連線後才讀取
- Group / peer 顯示名稱屬於 Central/App 側可見 metadata，不代表 firmware runtime 也持有相同命名

## 第 2 頁設計原則

- Main：peer operational overview（health / connections / short log）
- 巡視人員看 quick health；Engineer 多看 deeper diagnostics（jitter / throughput / PHY / TX Power / compare gate 摘要）
- Reconciliation 仍是 exception flow，只有 conflict 才浮出 banner
- 此 role switcher 為 mock 閱讀層，參考 app repo 既有 `normal / maintenance / engineer` 概念，本輪先收斂為兩層
- Page 2 以 Gateway / End Device 為主；`Central Bridge` 僅為 Central-side path 的特殊路徑示意，非一般巡視入口
- Gateway 視角採 overview + expandable members / bridge 結構（accordion），點開才顯示個別 ED 或 bridge 的短摘要；不展開時保持極簡

### Page 2 update strategy（4 層）

mock 假設不是所有區塊同頻率更新，與現有 app contract / firmware SSOT 對齊：

- **overview**：~2s polling（STATUS）—— Gateway overview / 收合 ED 列
- **expanded detail**：notify-driven，UI ~1s 節流（METRICS_V2）—— 只在「展開中且正在看的項目」發生
- **event/log/alarm**：event-driven（EVT）—— conflict banner、recent events（弱化的 collapsible 區塊；conflict 時關鍵事件會在 overview 下方先露一條）
- **static / semi-static**：on open 或 30s（DEVICE_INFO）/ 手動 refresh（FW_VERSION / CAPS_V2 / ROSTER / alias）

不把 50–100ms 級的更新搬進手機主 flow。

Runtime 主畫面**只顯示 freshness / quality 結果**（「最後更新 2s 前」/「即時」/「資料較舊」/「目前無法比對」/`Online` / `Alive` / `Degraded` / `Offline`），不在畫面上出現 polling / notify / event-driven / acquisition cycle 這類機制細節——即使收合也不行。更新機制說明僅保留於本 README，不常駐顯示於畫面上。

### Freshness 用詞分層

為避免後續頁面混用，Page 2 採以下一致規則：

- **最後更新**：runtime / live observation（Gateway、ED page-level health sub）
- **上次同步**：Central / bridge / sync reference（Central Bridge、sync status 類）
- **最後看到**：member item / accordion 內 ED 列
- 時間一律用中文 `X 前`（不用 `X ago`）

## 第 3 頁設計原則

- 由 Page 2 conflict banner「查看差異」進入，主畫面 = Central vs Runtime 並列
- 兩側分明：左側 Central（authoritative · 後台分配）、右側 Runtime（observed · 現場觀測）；視覺上不靜默合併
- 每側都顯示 freshness（最後更新 / 上次同步）與對應 tag（fresh / stale / last synced / 尚未回報）
- 5 個切換情境：`converged` / `conflict` / `pending_reconciliation` / `central_only` / `not compared`
- diff hint 條同步說明 reviewer 下一步注意點；UI 上以「可比對 / 不可比對」呈現，對應 internal `can_compare` gate（不直接寫 `can_compare = true/false`）
- 主畫面 state label 用人類可讀短詞（Converged / Conflict / Pending sync / Central only / Not compared）；formal enum 留在 spec 與 README，不出現在 phone surface
- 用詞延用 Page 2 freshness 分層（最後更新 = runtime / 上次同步 = central），不引入新 vocabulary
- 不在本頁攤開 raw timestamp / revision / observed_at；證據細節屬 Page 4

### Page 3 resolution action

Conflict 不只是顯示狀態；Page 3 在 diff hint 下方加一條 resolution action strip，明示 reviewer 下一步：

- **Conflict**：primary `Recover runtime`（Central 是 canonical default）；danger 替代 `Accept runtime as new assignment`（明示需 Engineer 確認 / audit）；link `View evidence`
- **Pending sync**：`Wait for sync` + `View evidence`（不要叫人選哪邊正確）
- **Central only**：`Wait for runtime` / `Send check command` / `View evidence`
- **Not compared**：`Refresh Central` + `View evidence`（先取得 fresh Central 再判定）
- **Converged**：`No action needed`，僅低權重 `View evidence`

不做成「Central / Runtime 兩邊等權選正確」— 兩側角色不對等：Central 是 canonical assignment，Runtime 是 observed evidence。所有 action 在本輪皆為 mock，未串實作；危險動作以紅框 outline + 註記呈現權重差異。

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
