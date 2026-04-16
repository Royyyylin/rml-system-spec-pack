# CURRENT — rml-system-spec-pack

最後更新：2026-04-16

## 進度快照

- **Spec layer**：FEA-001~004 + REQ-007/008 + AC-007 + TC-012 已落地（commit `bf8ae80`），upstream evidence audit 完成（`763c970`）
- **Diagram Wave 1**：3 張核心圖（actors-authority / session-topology / fea-004-reconciliation-states）已完成 + review handoff
- **UI Review Mock — Page 1**：已通過方向 review（5 輪迭代到極簡入口）
- **UI Review Mock — Page 2**：剛收斂為大廠 runtime view（freshness 結果為主，update policy 移出畫面）— 等 Roy review

## 下一步（按優先序）

1. **等 Roy 確認 Page 2 runtime-view 收斂方向**
2. 通過後做 Page 3 `03-central-vs-runtime.html`（Central vs Runtime 並列差異），用詞延用 freshness 分層
3. Page 3 通過後做 Page 4 `04-evidence-panel.html`
4. 第二輪 diagram wave（拆 FEA-001/002/003，補 quality data flow 圖）

## 已知問題 / 待回收

- `renders/feature-telemetry-roster-visibility.svg` 維持 untracked dirty（unrelated to current scope，刻意未動）
- P1-2 deferred：`feature-assignment-reconciliation.d2` 的 `pending` → `pending_reconciliation`
- P1-3 deferred：AC-006 CMD_V2 timeout 30s 假設待 app timeout matrix 回寫
- App / Firmware / Central repo 需補 evidence contract follow-up（見 audit handoff）

## 環境備註

- 獨立 git repo，無 remote（本地 commit only）
- d2 v0.7.1，PNG export 走 Playwright headless Chromium
- web draw.io 不支援 data URI image embed → review mock 走純 HTML + SVG/PNG

## 主要 handoff 入口

- `docs/handoffs/2026-04-13-wave-1-diagram-review/` — Wave 1 圖 review
- `docs/handoffs/2026-04-15-upstream-evidence-audit.md` — SSOT evidence 盤點
- `docs/handoffs/2026-04-15-reconciliation-ui-review/` — UI mock pages
- `docs/handoffs/2026-04-16-eod-page2-runtime-view.md` — 本次 EOD
