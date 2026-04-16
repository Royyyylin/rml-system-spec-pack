# Implementation Phases

主檔：[README.md](README.md)　Status：`draft-for-review`

不要這輪寫 firmware code。分三階段，每階段有獨立 acceptance。

## Phase 0 — 標準化 RTT / HIL `[EVT]` structured text

**起點**：firmware 已有 33 條 `[EVT]` text tags（見 `ble_qos_demo_V1.2m/docs/specs/hil-evt-tag-inventory.md`）。

**目標**：把現有 free-form `[EVT]` 文字標準化成可被 grep / parse 的 `key=value` 格式，欄位對齊 [event-record-schema.md](event-record-schema.md)。

例：
- 原：`[EVT] BLE_LINK_UP role=GW peer=ED addr=AA:BB conn_idx=1`
- 標準化：`[EVT] family=BLE_LINK code=BLE_LINK_UP role=GW boot_id=42 uptime_ms=12345 event_seq=87 peer_id=AA:BB severity=INFO`

**Acceptance**：
- HIL test 改用 `family=` / `code=` 過濾，不再靠子字串
- 33 條 tag 全部 covered；缺漏列 follow-up
- 仍是 RTT only；**不上 wire**
- 不需要新增 GATT 欄位、不需要 firmware code 大改

## Phase 1 — Firmware local in-memory ring buffer

**目標**：firmware 維護有界 event ring buffer（建議 64–256 條，依 RAM）；可被 RTT / debug command 讀取與 drain；含 `dropped_count`。

**Acceptance**：
- ring buffer schema 對齊 [event-record-schema.md](event-record-schema.md)
- 滿載時用 newest-overwrites-oldest，並把 dropped 數字計入下次 drain
- HIL 可下 command（既有 CMD_V2 或新增 debug command）讀取最近 N 條
- `event_seq` / `boot_id` / `uptime_ms` 都已可由 firmware 內部供應
- 仍**不主動上 wire**；只在 debug / engineer drain 時送出

## Phase 2 — Wire / uplink + 對接 Page 4 / Central audit

**目標**：定一條 event uplink path（擴 `EVT` characteristic 或新增 `DIAG_EVT` characteristic / uplink family），讓 App / Central 可訂閱結構化 event；對接 Page 4 Evidence panel 的 Engineering details 與 Central audit。

**Acceptance**：
- Wire 欄位明訂（解 open question Q1）
- 訂閱 / 過濾 by family / severity；含 dropped 計數
- App 端 Page 4 `Recent events` 與 Engineering details 改成消費結構化 event，不再用 mock label
- Central 端把指定 severity / family 寫進 audit log（解 alignment Q3 / Q4）
- 與既有 `EVT.seq` 並存或取代的決策已寫入正式 spec

## 跨 phase 共用原則

- 每個 phase 結束都要回頭更新 `feature-assignment-reconciliation.md` / `feature-telemetry-roster-visibility.md` 對應段落
- 任何 phase 都**不允許**繞過 schema 直接送 free-form 字串到 wire
- 任何 phase 都**不允許** App / Central 假裝產出 firmware event（見 [role-mapping.md](role-mapping.md)）
