# Open Questions

主檔：[README.md](README.md)　Status：`draft-for-review`

## Q1 — `event_seq` 與既有 `EVT.seq` / `msg_seq` 的關係

**問題**：本 contract 的 `event_seq` 應「擴增現有 `EVT.seq`」還是「另立全新 sequence」？

- **背景**：
  - `EVT.seq` 目前是 `uint8_t per-type, for drop detection`（GATT `6f8a9c13`），8-bit wrap、per family 不共序
  - `msg_seq` 在 spec 出現但 firmware 尚未實作（見 `2026-04-15-upstream-evidence-audit.md`）
- **Decision needed by**：`ble_qos_demo_V1.2m`（firmware）
- **Impact**：Phase 2 wire 設計、HIL test 解析、跨 family 全域排序

## Q2 — `boot_id` 是否正式複用 `reset_count`

**問題**：`boot_id` 是新欄位還是直接用 NVS `reset_count`（uint16_t）？brownout / NVS write 失敗如何標示？

- **背景**：`reset_count` 已存在但 16-bit wrap（65535 後 0）；`boot_id` 在 `data-model.md` 提及但實作 deferred
- **Decision needed by**：`ble_qos_demo_V1.2m`（firmware）
- **Impact**：跨 boot 排序、wrap 風險、debug 時辨識重啟

## Q3 — Wall-clock timestamp 是否 deferred

**問題**：device 端目前無 wall-clock；本 contract 只用 `uptime_ms / s`。是否要 firmware 加 wall-clock（NTP / Central time hint）？

- **背景**：`ts_device / ts_gateway / ts_central` 在 spec 是 Phase 2 槽，無 GATT 實作
- **Decision needed by**：`ble_qos_demo_V1.2m` + `central-device-metadata`
- **Impact**：跨 device 真實時間排序、與 OPC UA / 工業 SoE 對齊度

## Q4 — CC relay event 是否進 Central audit

**問題**：CC relay 自身的 session / forward / result event 是否寫進 Central audit？

- **背景**：CC 是 relay 不是 authority；audit owner 是 Central（見 evidence-field-contract-alignment Q3）
- **Decision needed by**：`central-device-metadata`
- **Impact**：Central audit storage 大小、relay 健康度可追溯性

## Q5 — `EVT` characteristic 擴欄位 vs 新增 diagnostic characteristic / uplink family

**問題**：把 schema 灌進現有 `EVT` 6-byte struct（會打破 backward compat）還是新建 `DIAG_EVT` characteristic 或新 uplink family？

- **背景**：現 `EVT` 為 ALARM/INFO 通知，6 bytes，固定 layout
- **Decision needed by**：`ble_qos_demo_V1.2m`（wire owner）
- **Impact**：MTU / fragment / subscribe 模式、App / Central 訂閱實作、舊 phone 的相容性

## Q6 — App 端 raw event viewer 的 scope

**問題**：手機 App 是否需要 raw structured event viewer，還是只在 Page 4 Engineering details 顯示？

- **背景**：Page 4 已定 first screen 顯示人話結論；raw 收進 Engineering details
- **Decision needed by**：`ble_qos_app`
- **Proposal**：Engineering details 顯示「最近 N 條 family/code/severity 過濾後」即可；獨立 viewer 留 Engineer mode
- **Impact**：App UI scope；事件量大時 phone bandwidth / storage

## Q8 — Event family ↔ reliability class 對應表

**問題**：Phase 1 ring buffer 沿用 firmware reliability Class A/B/C eviction（A 永不 drop / B 次之 / C 先踢）。每個 event family / severity 應對應哪一 class？

- **背景**：既有 `firmware-phase3-reliability.md` 定義 Class A 為 critical data 必須 buffer+replay+seq；event log 是新加類別，未在原 mapping 內
- **Decision needed by**：`ble_qos_demo_V1.2m`（firmware）
- **Proposal（draft）**：FATAL / ERROR + FAILOVER family → A；WARN + ROSTER / CMD → B；INFO / DEBUG 其他 → C
- **Impact**：拒收策略、NVS persist 範圍、Phase 1 acceptance

## Q9 — BLE_LINK `link_session_id` 來源

**問題**：[ordering-correlation.md](ordering-correlation.md) BLE_LINK lifecycle 段定為 target rule，但目前無共享 `link_session_id`。三個候選方式如何擇一？

- **背景**：GW / ED 兩端各自看到自己的 `conn_idx` / `conn_handle`，對端 handle 不可見；無 session-level 共享識別
- **Decision needed by**：`ble_qos_demo_V1.2m`（firmware）
- **Proposal**：候選 1（hash from initiator + addr + open uptime）影響最小、不需 wire 改動，可先試
- **Impact**：跨 device link 對齊；在落地前 App / Central 只能 best-effort heuristic match，不可 audit

## Q10 — `QOS_HEARTBEAT` 該歸哪裡（或不該收編到 event log）

**問題**：`[EVT] QOS_HEARTBEAT pdr/lat/jit/conn`（gw_qos.c emits, periodic）是 GW 端 rolling QoS metrics，本輪明文移出 `FAILOVER`。應走哪條路？

- **背景**：
  - `role-mapping.md` 既有原則：「telemetry / measurement 本身不算 event（屬 STATUS / METRICS_V2），measurement-driven 異常才升格」
  - QOS_HEARTBEAT 是週期性指標，不是 state transition，混進 event log 會稀釋 event 語意，也污染 Page 4 / Central audit 的 failover 過濾
- **候選方案**：
  1. 新開 `RUNTIME_HEALTH` / `DIAGNOSTIC` family 收編（保留 event 形式但與 FAILOVER 分開）
  2. 改走 STATUS / METRICS_V2 telemetry stream，event log 不收
  3. 拆兩半：rolling metrics 走 telemetry；只在 threshold 違反時 emit `QOS_DEGRADED` event（升格規則待定）
- **Decision needed by**：`ble_qos_demo_V1.2m`（firmware）+ `central-device-metadata`（audit owner）
- **Impact**：Page 4 evidence 過濾條件、Central audit 大小、HIL test 對 QoS 健康度的觀察介面

## Q7 — Severity 與 ALARM 業務語意的分界

**問題**：`severity = ERROR/FATAL` 與既有 `EVT type=ALARM` 是否完全對應？是否需要在 schema 內額外標 `is_alarm`？

- **背景**：現 `EVT` 用 `type` 區 ALARM/INFO（delivery 也不同：indicate vs notify）
- **Decision needed by**：`ble_qos_demo_V1.2m` + `ble_qos_app`
- **Impact**：Page 4 / Central audit 能否用單一 severity 過濾，或需要 cross-check `family/code` + delivery
