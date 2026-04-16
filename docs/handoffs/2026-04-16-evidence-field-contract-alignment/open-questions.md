# Evidence Field Contract — Open Questions

主檔：[README.md](README.md)　Status：`draft-for-review`

每題列：問題 / 影響 / decision needed by / impact。

## Q1 — Runtime `observed_at` 時程

**問題**：`observed_at` / `ts_device` / `ts_gateway` 在 `feature-assignment-reconciliation.md` 與 `central-device-metadata/data-model.md` TelemetryEnvelope 是 schema 槽，但 `ble_api.yaml` **沒有 GATT 實作**（Phase 2 deferred）。Runtime side freshness 在過渡期該如何計算？

- **Decision needed by**：`ble_qos_demo_V1.2m`（firmware）+ `ble_qos_app`
- **Proposal**：過渡期用 `failover_generation` + `uptime_s` + `EVT.seq` 三者組合作為 age proxy；Phase 2 才補 wall-clock `ts_*`
- **Impact**：Page 4 `observed_age` / `runtime_observation_is_fresh` 的 derive 來源；若無共識，App 只能用 weak proxy 並標 freshness as best-effort

## Q2 — Central freshness window 是 App local 還是 Central server-driven？

**問題**：`central_reference_is_fresh` 的判斷需要 freshness window 數值。目前無 spec / config 指定。

- **Decision needed by**：`ble_qos_app`（App local）或 `central-device-metadata`（server-driven hint）
- **Proposal**：App local config（hard-coded const 起步），未來若 Central 提供 hint header，再切 server-driven
- **Impact**：`Not compared` vs `central_only` 的分界完全取決於這個 window；不同 window 會讓同樣 evidence 落到不同 UI label

## Q3 — `Accept runtime as new assignment` 的 audit owner

**問題**：高風險動作把 Runtime 升格成 canonical。audit 要由哪個 owner 寫入？選項：

1. Central 單一 audit log（App 只送 mutation 請求 + reason）
2. App 本機暫存 + 後續同步給 Central
3. 雙寫（App + Central）

- **Decision needed by**：`central-device-metadata` + `ble_qos_app`
- **Proposal**：Central 單一 audit log（避免 App 端被竄改）；App 只負責收集 reason 字串並送進 Central API
- **Impact**：`capability-ownership.md` 的 `Central = canonical owner` 原則要與 audit owner 一致；spec 須補 BND

## Q4 — `reason` 欄位的位置

**問題**：`reason`（變更原因字串）目前 mock 只在 UI 收集，沒有對應 wire 欄位。它屬於：

1. command payload（與 `Accept runtime` mutation 一起送）
2. audit payload（單獨送 audit endpoint）
3. Central metadata API 的 generic field

- **Decision needed by**：`central-device-metadata`
- **Proposal**：command payload + 由 Central 自動寫入 audit；不另外送
- **Impact**：API 設計、必填 / 選填、長度上限；spec 須補 schema

## Q5 — `runtime attach not visible` 由哪個 firmware signal 表達？

**問題**：`Central only` 情境下，Runtime side 是 fresh 的，但「沒有 attach」這件事要從哪個 firmware signal 推斷？

- **Decision needed by**：`ble_qos_demo_V1.2m`（firmware）+ `ble_qos_app`
- **Proposal**：用 `ROSTER_LIST` 不含該 ED 的 attach 紀錄 + 該 ROSTER 是新鮮的 → 即「fresh source, no attach」；不需要新 signal
- **Impact**：Page 4 Runtime evidence rows（`gw = —（attach not visible）` / `srcpath = roster`）的合法性

## Q6 — `assignmentSyncState` enum 是否要加 `Not compared` / `Pending sync` label

**問題**：`ble_qos_app/docs/specs/app-scope/04-local-state.md` 的 enum 是 4-value：`confirmed / pending_reconciliation / conflict / orphaned`。UI mock 用 5 個 scenario（含 `Not compared`，且 `Pending sync` 是 `pending_reconciliation` 的 label）。

- **Decision needed by**：`ble_qos_app`
- **Proposal**：保留 4-value enum 為 FSM state；新增 `compareGateState` enum（`comparable` / `not_compared`）作為 pre-FSM gate 結果；UI 顯示時組合兩者
- **Impact**：App local state schema；spec 對應更新

## Q7 — Recommended action 的命名與權限對應

**問題**：mock 用 `Recover runtime` / `Accept runtime as new assignment` / `Refresh Central` / `Wait for runtime` / `Send check command` 五個 label。沒對應 spec 的 command name 或 role gate。

- **Decision needed by**：`central-device-metadata`（command API） + `ble_qos_app`（role gate UI）
- **Proposal**：在 `feature-assignment-reconciliation.md` 補 BND 列舉 5 種 action + role / audit 要求；Central API 對應 `recover-runtime` / `runtime-promote` / `refresh-snapshot` / `runtime-check`
- **Impact**：Page 3 resolution action 是否能進實作；spec freeze 前必須鎖
