# EOD — 2026-04-16 · Page 2 收斂為 runtime view

## Summary

完成 P0 evidence audit、Page 1 入口極簡化（5 輪迭代）、Page 2 從 reconciliation summary 重構成 peer operational overview，並收斂為大廠 runtime 風格（freshness 結果為主，update policy 移出畫面）。

## Modified Files

- `docs/handoffs/2026-04-15-upstream-evidence-audit.md` + 子檔 — Central/Firmware/App SSOT age evidence 盤點
- `docs/handoffs/2026-04-15-reconciliation-ui-review/01-entry-list.html` — 入口頁，5 輪迭代到「name + 短狀態 + Connect」
- `docs/handoffs/2026-04-15-reconciliation-ui-review/02-detail-summary.html` — peer overview + accordion + role layering + recent events + freshness 結果
- `docs/handoffs/2026-04-15-reconciliation-ui-review/README.md` — page-by-page 說明、freshness 用詞分層、rename boundary、update policy

## Key Changes

- **REQ-007 / REQ-008 / AC-007 / TC-012** 已由 `bf8ae80` 落地（pre-session），本 session audit 確認 wording 與 SSOT 一致，無需再改 spec
- **入口頁邊界**：pre-connect 只顯示 cached / last-synced 名稱與短狀態；rename / detail / can_compare 全部 deferred 到後續頁
- **Page 2 結構**：Gateway overview + Connected EDs accordion + Central Bridge accordion + Recent events（弱化 collapsible）
- **Role layering**：巡視人員 / Engineer 兩層，accordion 展開內容深度依 role 變化
- **Conflict = exception flow**：banner + 主體輕量 patch + 關鍵事件 hint，非主流 layout
- **Update policy 移出畫面**（ADR candidate）：runtime UI 只顯示 freshness / quality 結果（最後更新 / 上次同步 / 最後看到 / Alive / Degraded），機制細節（polling / notify / event-driven）僅保留於 README
- **Freshness 用詞鎖定**：最後更新 = runtime live；上次同步 = central/sync ref；最後看到 = member item；時間統一 `X 前`

## Immediate

下次 session 第一件事：
1. Roy 確認 Page 2 runtime-view 收斂方向 OK
2. 若通過，開始 Page 3 `03-central-vs-runtime.html`（Central vs Runtime 並列差異），用詞延用 freshness 分層
3. Page 3 完成後再 Page 4 `04-evidence-panel.html`（追 timestamp / revision / evidence）

## Backlog

- P1-2: `feature-assignment-reconciliation.d2` 的 `pending` → `pending_reconciliation`（vocabulary consistency pass，等 Page 3/4 定稿後一起做）
- P1-3: AC-006 CMD_V2 timeout 30s 假設，等 app timeout matrix 回寫
- App repo follow-up：在 `04-local-state.md` formal 定義 `central_reference_is_fresh` / `can_compare` / `last_synced`
- Firmware repo follow-up：Phase 2 `telemetry-schema.md` 決定 `ts_*` / `boot_id` / `msg_seq` wire 實作
- Central repo follow-up：freshness window 數值（若 server-driven）
- 第二輪 diagram wave（Wave 2/3）

## Key Insights

- **入口頁迭代教訓**：1 輪做完入口會踩很多 affordance / 工程代號 / member count / rename 暗示的雷；分多輪極簡化才到位
- **Page 2 重構教訓**：reconciliation 不該當 detail 主角，應降級為 exception banner；operational overview 才是大廠 runtime 主流
- **大廠 runtime view 原則**：runtime 畫面顯示 freshness/quality 結果，機制（polling/notify）屬 engineering config 不上主畫面
- **Scope drift 教訓**：bf8ae80 commit 把幾輪 diagram 改動掃進 P0 commit；後續 commit 前要先 `git status` 核對禁區
- **Unrelated dirty file**：`renders/feature-telemetry-roster-visibility.svg` 全 session 維持 untracked dirty，所有 commit 都明確排除

## Environment Notes

- spec-pack 為獨立 git repo（init 於 `5963ca3` 之前），無 remote，全 session 本地 commit
- d2 PNG export 需 Playwright headless Chromium（已下載）
- web draw.io 已確認對 PNG/SVG embed image cell 支援度不穩；review mock 改走純 HTML + SVG/PNG 直接顯示

## Files NOT Committed

- `renders/feature-telemetry-roster-visibility.svg`（unrelated dirty，不在本 session scope，刻意未動）
