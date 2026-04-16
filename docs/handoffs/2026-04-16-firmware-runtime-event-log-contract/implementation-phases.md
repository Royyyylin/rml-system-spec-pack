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
- 既有 33 條 `[EVT]` tag 必須**逐條對應**到 [event-taxonomy.md](event-taxonomy.md) 的 family + code（含 BOOT / BLE_LINK / ROSTER（含 TOPOLOGY）/ FAILOVER（含 QOS_HEARTBEAT）/ CMD / CC_RELAY / UPLINK（UPLINK_DISPATCH 改名 `frame_family=`））；無法對應者列為缺漏 follow-up，不可自行發明 family
- 仍是 RTT only；**不上 wire**
- 不需要新增 GATT 欄位、不需要 firmware code 大改

## Phase 1 — Firmware local in-memory ring buffer

**目標**：firmware 維護有界 event ring buffer（深度依 RAM 預算）；可被 RTT / debug command 讀取與 drain；含每 class 的 `dropped_count`。

**Eviction policy 與 firmware reliability SSOT 對齊**（見 `ble_qos_demo_V1.2m/docs/specs/firmware-phase3-reliability.md` Task 3.2）：

- 每筆 event record 帶 reliability class（`A` / `B` / `C`），由 family / severity 對應（建議 mapping 待 firmware 端確認）
- ring 滿時：**先踢最舊 C → 再踢最舊 B → A 不可 eviction，必要時拒收新 entry**
- 不使用 newest-overwrites-oldest；不發明新 eviction 語意
- dropped 計數需 per-class 區分（`dropped_a` 應永遠為 0；若 ≠ 0 視為 firmware bug）

**Acceptance**：
- ring buffer schema 對齊 [event-record-schema.md](event-record-schema.md)
- Class A 永不被 silent drop（沿用既有 `R1` 規則）
- 拒收 / drop 都會被下次 drain 攜出（per-class counter）
- HIL 可下 command（既有 CMD_V2 或新增 debug command）讀取最近 N 條
- `event_seq` / `boot_id` / `uptime_ms` 都已可由 firmware 內部供應
- 仍**不主動上 wire**；只在 debug / engineer drain 時送出
- Event family ↔ reliability class 的對應表納入下一輪 spec 修訂（見 [open-questions.md](open-questions.md) Q8）

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
