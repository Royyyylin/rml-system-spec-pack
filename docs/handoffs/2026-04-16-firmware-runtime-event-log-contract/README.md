# Firmware Runtime Event Log Contract

**Status**：`draft-for-review`（不是正式 spec freeze）

## 結論

GW / ED / CC 必須輸出**結構化 runtime event**，不能只靠 RTT printf。事件本身要有來源、時間、順序、嚴重度、處置語意；下游消費者（Page 4 evidence、App debug、Central audit）共用同一份證據欄位。

## 為什麼現在做

- 沒有結構化 event → debug GW/ED/CC 順序與連線狀態只能靠 RTT 的 `[EVT]` printf 文字（已 33 條），**不能跨 device 排序、無法被 App / Central 消費**
- Page 4 Evidence panel 已定稿，但 raw evidence 欄位 contract 仍是 mock（見 `2026-04-16-evidence-field-contract-alignment/`）
- Central audit、App debug 若各自定 schema 會再分裂；先在 firmware 端定 contract，下游再對齊

## 與既有 spec / handoff 的關係

- 既有 RTT `[EVT]` 文字 tags 是 Phase 0 起點，不是 contract（見 `ble_qos_demo_V1.2m/docs/specs/hil-evt-tag-inventory.md`）
- 現有 `EVT` GATT characteristic（6f8a9c13）只承載 `type/id/v0/v1/seq/flags` 6 bytes per-type drop detection，**不足以承載 structured event record**
- `assignmentSyncState` / `failover_generation` / `EVT.seq` 等概念散落在多份 spec；本 contract 不重定義它們，只規範如何被 event record 引用

## 檔案

- [event-record-schema.md](event-record-schema.md) — 最小 event record 欄位
- [event-taxonomy.md](event-taxonomy.md) — 事件分類（family / code）
- [ordering-correlation.md](ordering-correlation.md) — 順序保證與相關性
- [role-mapping.md](role-mapping.md) — GW / ED / CC 各自吐什麼事件
- [implementation-phases.md](implementation-phases.md) — 三階段落地策略
- [open-questions.md](open-questions.md) — 待 owner repo decision

## 如何支援 Page 4 evidence

Page 4 第一層顯示**人話摘要**（`human_message`）；Engineering details 折疊區才顯示 raw event record（`event_seq` / `boot_id` / `uptime_ms` / `correlation_id` / `payload`）。同一份 event 同時餵 App debug 與 Central audit。

## 如何支援後續 App / Central

- App debug：直接消費 firmware 結構化 event，做 `Recent events` / Engineering details；不再自己拼字串
- Central audit：把高重要度 event（severity / family）寫進 audit log；`reason` / `recommended_action` 等 App 加註欄位另由 Central API 處理

## 不在本輪做

- 不寫 firmware code
- 不改 wire / GATT 欄位（只列 candidate）
- 不指定 ring buffer 大小、deferred logging 細節
- 不 freeze event_code 數值列表
- 不規範 App / Central 端 schema（下一個 gate）
