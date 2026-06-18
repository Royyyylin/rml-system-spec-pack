<!-- A2 research dump from 8 sub-agent fan-out, 2026-04-24 -->

# Finding 04 — 業界 BLE QoS Open Source 現況

## Sub-Agent 任務描述

全面調查業界 BLE QoS 相關的 open source 實作，
評估功能覆蓋範圍，確認 A2 的差異化定位。

---

## Key Findings

### 整體結論：業界完全空白（p99 tail latency 可控）

- open source 中**零個**實作能控制 p99 tail latency
- **零個**涵蓋多維度即時自適應（RSSI + channel quality + interval + TX power + PHY + 事件長度）

### 現有 Open Source 實作盤點

#### 1. Nordic ble_qos.c（nrf_desktop 應用）

- 功能：Channel Survey + Channel Map 更新
- 維度：1/6（只有 channel management，無 RSSI/TX power/interval/PHY/事件長度控制）
- 維護狀態：活躍（NCS 主線維護）
- **A2 差距**：缺少 METRICS 量測、POLICY 決策、CONTROL 執行三層

#### 2. AdaptaBLE（2020 學術 prototype）

- 功能：自適應調整 data rate、TX power、connection interval
- 維度：3/6（較接近，但無 channel survey 聯動）
- 維護狀態：**無 open repo**，僅論文描述
- 論文：ResearchGate 2020

#### 3. BlueSync（GitHub）

- 功能：Anchor point synchronization
- 維度：0/6（純時鐘同步，與 QoS 無關）
- **A2 差距**：完全不同問題域

### BLE Core 6.2 新功能（2025-11 發布）

- **SCI (Subrated Connection Interval)**：375µs interval
- **Frame Space Negotiation**：減少空中時隙浪費
- p99 5-10ms 理論可行，但需 nRF54L15 硬體支援
- 目前無任何 open source 整合 BLE 6.2 SCI + QoS 自適應

---

## 業界 Reference

| 名稱 | URL |
|------|-----|
| Nordic ble_qos.c | https://github.com/nrfconnect/sdk-nrf/blob/main/applications/nrf_desktop/src/modules/ble_qos.c |
| BT Core 6.2 Overview | https://www.bluetooth.com/bluetooth-core-6-2-feature-overview/ |
| AdaptaBLE (ResearchGate) | https://www.researchgate.net/publication/343951605_AdaptaBLE_Adaptive_control_of_data_rate_transmission_power_and_connection_interval_in_bluetooth_low_energy |

---

## 對 A2 架構的影響

- A2 的 4 層架構（INGEST/METRICS/POLICY/CONTROL）在業界無對應開源實作可借鑑。
- Nordic ble_qos.c 的 channel map 管理邏輯可作為 A2 CONTROL 層 channel management 的參考，但不可直接整合（缺少 POLICY 決策層）。
- AdaptaBLE 的三維自適應概念（data rate + TX power + interval）是最接近 A2 的學術設計，但無程式碼可用。

## 對我們系統的影響

- **A2 具有業界首創（first-of-its-kind）定位**：多維度 BLE QoS 即時自適應，無任何 open source 競品。
- 這同時意味著**沒有踩坑紀錄可參考**，implementation risk 較高，需要更嚴格的 clean-room 隔離（見 merged-recommendations）。
- BLE 6.2 SCI 是第二代（nRF54L15）的長期路線，不影響第一代 A2 設計。
