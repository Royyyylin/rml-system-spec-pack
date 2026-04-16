# Reconciliation UI Review — Wave 1 Complete

主檔：[README.md](README.md)。Wave 1 page-by-page review 全部 passed。

## Pages

| # | 頁面 | 用途 |
|---|------|------|
| 1 | [01-entry-list.html](01-entry-list.html) | 選要連線的 peer（pre-connect entry，極簡）|
| 2 | [02-detail-summary.html](02-detail-summary.html) | 連線後 runtime overview + role-based information layering（巡視人員 / Engineer）|
| 3 | [03-central-vs-runtime.html](03-central-vs-runtime.html) | Central vs Runtime 並列差異 + resolution action strip |
| 4 | [04-evidence-panel.html](04-evidence-panel.html) | Evidence panel：先人話結論，raw / internal 欄位收進 Engineering details |

## Accepted commits（本輪重點）

- `1fe628f` Page 3 初版（Central vs Runtime dual-source）
- `cdb99b4` Page 3 resolution action strip（recommended / danger / link）
- `fc10868` Page 3 microcopy polish（中英標點、人話 state label）— accepted
- `7627457` Page 4 初版 + README 拆 sub-files（page-2/3/4-design.md）
- `0b71812` Page 4 human-first evidence summary（first screen 結論優先；Central only 修為 cannot compare）— accepted

## Key design decisions

- **Central 是 canonical / authoritative assignment；Runtime 是 observed / actual attach evidence**，不做等權合併
- **不做 Central / Runtime 等權二選一**；Conflict 採非對等 recommended action
- Conflict primary action：`Recover runtime`（恢復回 Central 分配）
- Conflict danger 替代：`Accept runtime as new assignment` — 高風險，需 Engineer confirmation / reason / audit
- **Page 4 first screen 一律先人話**：state + 結論 + 建議處理 + 三條「為什麼」
- raw / internal 欄位（`updated_at` / `observed_at` / `revision` / `can_compare` / `mismatch_field` / event source）收在 `Engineering details` 折疊區
- **Page 1–3 完全不顯示 raw timestamp / revision / observed_at / can_compare**；Page 4 才允許露 internal key
- Freshness 用詞分層鎖定：**最後更新**（runtime live）/ **上次同步**（Central / sync ref）/ **最後看到**（member item）；時間中文 `X 前`
- **Compare gate 真值表**：Conflict → can_compare = true；Not compared → false（stale Central reference）；Central only → false（missing runtime evidence）
- Reconciliation 在 Page 2 是 exception flow（只在 conflict 才浮 banner）

## Remaining risks / deferred

- HTML mock 尚未接 Flutter 實作；action buttons 與 confirmation modal 都只是 mock
- Evidence schema / exact source fields 仍需後續與 App / Central / Firmware 實作對齊
- Page 4 `Engineering details` 內欄位命名屬 review mock 約定，**不是 wire protocol 名稱**
- Page 3 `Recover runtime` / `Accept runtime as new assignment` 真實實作流程（誰下指令、誰寫 audit、reason 欄位）尚未綁定 spec
- Wave 1 沒涵蓋 metadata / manage flow（rename 等）— 已標 boundary，留給後續

## Next recommended gates（擇一推進）

1. 將 Page 1–4 UI decision 回寫成 **implementation handoff** 給 App repo（mock → spec：欄位、role gate、action audit 流程）
2. 回到 **diagram wave 2**（拆 FEA-001/002/003 + quality data flow 圖）
3. 對 **evidence field contract 做 cross-repo alignment**（Central / Firmware / App 共識 evidence schema 與命名）
