# Reconciliation UI Review Mock

Page-by-page review。一次只看一頁，上一頁通過後才做下一頁。

## Review 順序

| # | 頁面 | 回答什麼 | 狀態 |
|---|------|---------|------|
| 1 | [01-entry-list.html](01-entry-list.html) | 入口：現在可以連誰？哪個對象值得先連？ | Passed |
| 2 | [02-detail-summary.html](02-detail-summary.html) | 連線後 peer overview + role-based information layering（巡視人員 / Engineer） | **Ready for Roy review** |
| 3 | 03-central-vs-runtime.html | Central vs Runtime 怎麼並列？ | 待第 2 頁通過 |
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
