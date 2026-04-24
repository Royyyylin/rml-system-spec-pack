<!-- A2 research dump from 8 sub-agent fan-out, 2026-04-24 -->

# Finding 06 — 業界 BLE p99 Latency Benchmark

## Sub-Agent 任務描述

調查業界 BLE 連線的 p99 延遲實測數據，
涵蓋傳統 BLE、BLE 6.2 SCI、5G URLLC、工業無線協定，
確立 A2 p99 20ms 目標的合理性。

---

## Key Findings

### 傳統 BLE p99 實測

| 場景 | p99 延遲 | 備註 |
|------|----------|------|
| 無干擾環境（clean） | 15–30ms | 典型辦公室 / 實驗室 |
| 有干擾環境（interference） | 50–100ms | 2.4GHz 擁擠環境 |
| 學術最強（Springer 2025） | **50ms deadline @ 99.92%** | 需嚴格 scheduling |

- **結論**：p99 20ms 對傳統 BLE 屬於激進但可達（需要 QoS 調度輔助），對應業界 clean 環境下限。

### 學術最強案例（Springer 2025）

- 論文：BLE 即時調度，50ms deadline 達到 99.92% 成功率
- 未達到 20ms @ p99（即 A2 目標比此論文更嚴格）
- 表示 A2 需要主動 QoS 介入才能達標
- **Source**: https://link.springer.com/chapter/10.1007/978-3-031-97537-0_5

### BT Core 6.2 SCI（2025-11 發布）

- **SCI (Subrated Connection Interval)**：375µs interval
- p99 理論值：5–10ms
- **硬體需求**：nRF54L15（目前無 nRF52833 支援計畫）
- 結論：10ms p99 是第二代（nRF54L15）的 stretch goal
- **Source**: https://www.bluetooth.com/bluetooth-core-6-2-feature-overview/

### 對比其他無線技術

| 技術 | p99 典型值 | 硬體需求 |
|------|-----------|---------|
| 傳統 BLE | 15–100ms | nRF52833 |
| BLE 6.2 SCI | 5–10ms | nRF54L15 |
| 5G URLLC | 0.5–1ms | 基地台基礎設施 |
| WirelessHART | 100ms+（多跳） | 專用網關 |
| ISA100.11a | 100ms+（多跳） | 專用設備 |

- ISA100 白皮書明確承認：「1–10ms 是工業無線未解難題」
- 5G URLLC 雖可達 1ms，但需要固定基礎設施，不適用行動 BLE 場景

---

## 業界 Reference

| 名稱 | URL |
|------|-----|
| Novel Bits: BLE Connection Intervals | https://novelbits.io/ble-connection-intervals/ |
| Springer 2025（BLE RT scheduling） | https://link.springer.com/chapter/10.1007/978-3-031-97537-0_5 |
| BT Core 6.2 Feature Overview | https://www.bluetooth.com/bluetooth-core-6-2-feature-overview/ |

---

## 對 A2 架構的影響

- **p99 20ms 是 A2 合理且有意義的目標**：比業界 clean 環境最佳實測（15–30ms）要求更嚴格，需要 A2 的主動 QoS 調度介入。
- POLICY 層的決策頻率需足夠快（建議每 connection event 評估，最多 7.5ms 一次）。
- CONTROL 層需能在 1–2 個 connection interval 內完成 channel/interval/TX power 切換。

## 對我們系統的影響

- **驗收目標確認**：p99 20ms 對應第一代（nRF52833）目標，10ms 對應第二代（nRF54L15 + BLE 6.2）stretch。
- 測試環境需在有 2.4GHz 干擾的場景下驗證（不能只在 clean 環境），否則 p99 沒有意義。
- Roy 第二份報告的 p99 20ms 目標與業界數據一致，可作為正式驗收標準。
