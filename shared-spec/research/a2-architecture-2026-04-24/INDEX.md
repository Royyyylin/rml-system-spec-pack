<!-- A2 research dump from 8 sub-agent fan-out, 2026-04-24 -->

# A2 Architecture Research — 2026-04-24

## 背景

Roy 提供兩份報告觸發本次研究：

1. **A2 架構報告** — 描述 BLE QoS 自適應演算法 (A2) 的整體設計，含 INGEST/METRICS/POLICY/CONTROL 四層分解。
2. **量產穩定 BLE 韌體 RT (Real-Time) 報告** — 提出 p99 延遲目標與 nRF52833 資源分析。

「LinkBlu RT」名稱出現在報告中，8 輪 WebSearch 零命中，研究確認該名稱對應的產品不存在，已找到 3 個真實參考。

---

## 8 Sub-Agent 任務清單

| # | 主題 | 檔案 |
|---|------|------|
| 01 | LinkBlu RT 真實性深查 | [finding-01-linkblu-rt.md](finding-01-linkblu-rt.md) |
| 02 | NCS v2.9.2 → v3.3.0 breaking change | [finding-02-ncs-migration.md](finding-02-ncs-migration.md) |
| 03 | NCS v3.3.0 新 opcode + sample | [finding-03-ncs-3-3-opcode.md](finding-03-ncs-3-3-opcode.md) |
| 04 | 業界 BLE QoS open source 現況 | [finding-04-open-source-runtime.md](finding-04-open-source-runtime.md) |
| 05 | discardable HCI event patch 分析 | [finding-05-discardable-patch.md](finding-05-discardable-patch.md) |
| 06 | 業界 BLE p99 benchmark | [finding-06-industry-p99.md](finding-06-industry-p99.md) |
| 07 | nRF21540 + QoS 整合 | [finding-07-nrf21540-integration.md](finding-07-nrf21540-integration.md) |
| 08 | nRF52833 vs nRF54L15 資源分析 | [finding-08-nrf52833-vs-54l15.md](finding-08-nrf52833-vs-54l15.md) |
| 09 | GW / ED / CC 三角色 A2 Profile Matrix | [finding-09-role-matrix.md](finding-09-role-matrix.md) |

整合建議見 [merged-recommendations.md](merged-recommendations.md)。

---

## 核心結論（8 條）

1. **LinkBlu RT 不存在** — 8 輪 WebSearch 零命中，最可能源頭為 IEEE Infocom 2023 學術論文 RT-BLE，真實商業參考為 Nordic 合作夥伴 Blecon。
2. **業界 BLE QoS 完全空白** — open source 只有 Nordic ble_qos.c 涵蓋 1/6 維度，A2 在多維度即時自適應上無任何可參考的開源實作，處領先位置。
3. **nRF52833 撐得住** — GW A2 RAM 修正估算 ~27 KB（原 finding-08 ~21 KB 偏低），剩餘 ~37 KB；ED ~6 KB、CC ~10 KB，三角色均可行。
4. **NCS 升 v3.2.0 推薦** — rssi_power_control + path_loss_monitoring + Channel Survey 在 v3.2.0 已 supported，不需冒 v3.3.0 額外 breaking change 風險。
5. **discardable 不能貿然 patch** — 0x80/0x82 event 標為 discardable 是 anti-deadlock 設計，推薦 pool 加大（BT_BUF_EVT_DISCARDABLE_COUNT=20）+ app gap detection。
6. **clean-room 強制** — A2 PoC 實作必須與 spec/measurement team 隔離，避免知識污染。
7. **p99 20ms 是 GW-to-Phone/Central system-level 目標** — ED p99 由 GW QoS 決策決定；CC p99 = transport reliability；10ms 需 BT 6.2 SCI + nRF54L15（第二代 stretch goal）。
8. **A2 需拆 3 role profile（GW / ED / CC），非全統一 runtime** — 4 sub-feature × 3 role = matrix 設計；core framework 100% 共用，policy/control 依角色差異化；共用率約 50-100%，整體實作量 ≈ 1.5× 單角色工作量，不需 12 份獨立 spec。

---

## 與既有 Spec 的對應

| 既有 Spec | A2 Research 對應點 |
|-----------|-------------------|
| F-04 (gw-qos-scheduler-tuning) | A2 POLICY 層 runtime preset，finding-02 NCS migration 影響 SDC API |
| F-LOG-BITMAP (27 LOG events) | A2 INGEST 層 observability 基礎，F-LOG-BITMAP SDD 須先完成 |
| market-compliance-matrix | finding-07 FCC AFH ≥15 ch 聯動限制，TX power zone 重校 |
| requirements.md p99 target | finding-06 確認 20ms 合理，10ms 為第二代目標 |

---

## 建議下一步（4 個拍板問題）

1. **NCS 版本鎖定**：確認鎖 v3.2.0 還是跟上 v3.3.0？（影響 3-5 工程人日）
2. **A2 PoC IMPL FREEZE 例外範圍**：Milestone 1-3 例外，Milestone 4+ 走解凍流程，是否確認？
3. **nRF21540 TX power 政策**：Channel manager 跟 TX policy 聯動是否作為 A2 CONTROL 層的強制需求？
4. **nRF54L15 升級觸發條件**：MAX_ED > 12 / 需要 Channel Sounding 觸發，是否作為第二代正式 trigger？

> Finding-09 補充澄清：Q3 p99 目標 20ms 僅對 GW 有效（GW-to-Phone/Central system-level）；ED/CC p99 各自定義，不沿用同一數值。
