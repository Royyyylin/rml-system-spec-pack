# Evidence Field Contract — Cross-repo Alignment Draft

**Status**：`draft-for-review`（不是正式 spec freeze）

## 結論

Page 4 Evidence panel UI 可成立。欄位 contract 必須**明確分成兩類**：

1. **Owner raw evidence**（`Central` / `Firmware` 提供，wire 真實欄位）
2. **App derived state**（`App` 在本機計算的 compare gate / reconciliation state，不上 wire）

混在一起會讓 Page 4 mock 的欄位被誤當成 wire protocol。

## Scope

- 只處理 Page 4 Evidence panel + Page 3 resolution action 涉及的欄位
- 不重新設計 wire / protocol；只把 mock 對齊既有 owner SSOT
- 不 freeze；下一輪由 owner repo 各自正式化

## 主要結論

- **Central side**：`updated_at` / `revision` / `assignment_version` / `last_switch_at` / `last_failover_at` 都已存在 SSOT，可直接引用
- **Runtime side**：`failover_generation` / `uptime_s` / `reset_count` / `EVT.seq` / `GW_CFG_VERSION` 是已實作 age evidence；`ts_device / ts_gateway / ts_central` 屬 Phase 2 deferred，目前**不可作為 wire-level observed_at**
- **App derived（全部 missing）**：`can_compare` / `reason` / `mismatch_field` / `is_fresh` / `last_synced` / freshness window 數值，全部要 App repo 正式化
- **Central only ≠ missing runtime**：對齊正式 spec — Central only 是 FSM state，`can_compare = true`，Runtime source fresh 但 attach 內容為 not visible
- **Recommended action**：`Recover runtime` / `Accept runtime as new assignment` 兩條 path 名稱、權限、reason、audit 規則目前**spec 沒寫**，需 Central + App 共同定

## 詳細表

- 欄位矩陣：[field-matrix.md](field-matrix.md)
- 待解問題：[open-questions.md](open-questions.md)

## 對應 evidence handoff

- 既有 SSOT 盤點：[../2026-04-15-upstream-evidence-audit.md](../2026-04-15-upstream-evidence-audit.md)
- 細節：[../2026-04-15-upstream-evidence-audit/fields-detail.md](../2026-04-15-upstream-evidence-audit/fields-detail.md)
- Wave 1 收尾：[../2026-04-15-reconciliation-ui-review/WAVE1-COMPLETE.md](../2026-04-15-reconciliation-ui-review/WAVE1-COMPLETE.md)
- Page 4 設計：[../2026-04-15-reconciliation-ui-review/page-4-design.md](../2026-04-15-reconciliation-ui-review/page-4-design.md)
- Page 4 mock：[../2026-04-15-reconciliation-ui-review/04-evidence-panel.html](../2026-04-15-reconciliation-ui-review/04-evidence-panel.html)
- Evidence flow 圖：[../2026-04-15-reconciliation-ui-review/central-vs-runtime-evidence-flow.d2](../2026-04-15-reconciliation-ui-review/central-vs-runtime-evidence-flow.d2)

## Next gates（建議順序）

1. **App repo formalize derived fields** — 在 `ble_qos_app/docs/specs/app-scope/04-local-state.md` 補 `central_reference_is_fresh` / `runtime_observation_is_fresh` / `can_compare` / `reason` / `mismatch_field` / `last_synced` 並標 upstream 依賴
2. **Central repo confirm assignment timestamp / revision / audit** — `central-device-metadata` 確認 `updated_at` 精度、`revision` 用法、為 `Accept runtime as new assignment` 提供 `audit + reason` 欄位
3. **Firmware repo confirm runtime age evidence** — `ble_qos_demo_V1.2m` 對 `observed_at` / `boot_id` / `msg_seq` 給時程：用 `failover_generation + uptime_s + EVT.seq` 過渡，Phase 2 才補 wall-clock ts
4. **回 spec-pack 補正式 wording** — `feature-assignment-reconciliation.md` 補 BND：`Accept runtime as new assignment` 權限 / audit / reason 規則

## 不在本輪做

- 不改正式 spec
- 不發明新 wire field
- 不 freeze 欄位命名
- 不改 Page 4 mock
