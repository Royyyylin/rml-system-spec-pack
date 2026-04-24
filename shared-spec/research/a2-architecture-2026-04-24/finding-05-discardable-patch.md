<!-- A2 research dump from 8 sub-agent fan-out, 2026-04-24 -->

# Finding 05 — HCI Discardable Event Patch 分析

## Sub-Agent 任務描述

調查 HCI event buffer 中 discardable flag 的設計意圖，
分析 0x80 QoS conn event report 與 0x82 anchor event 的 patch PR，
評估三種處理作法的風險與推薦。

---

## Key Findings

### Discardable 設計意圖

- HCI event buffer 中，部分 event 被標為 `discardable`（可丟棄）
- **設計目的**：anti-deadlock — 當 event buffer 滿時，允許丟棄非關鍵 event，避免 controller 阻塞
- **不是 bug**，是 Zephyr BT stack 的刻意設計

### 兩個關鍵 PR

#### PR #2219 — 0x80 QoS Conn Event Report（2020）

- 事件代碼：`0x80` VS_QoS_Conn_Event_Report（Nordic vendor-specific）
- 問題：A2 INGEST 層需要持續接收此 event，若被 discard 會造成量測缺口
- PR 狀態：已合入（2020），但實作方式是標為 discardable 的 anti-deadlock 設計
- **Source**: https://github.com/nrfconnect/sdk-nrf/pull/2219

#### PR #17441 — 0x82 Anchor Report（2024）

- 事件代碼：`0x82` VS_Conn_Event_Anchor_Point（Nordic vendor-specific）
- 同樣標為 discardable 的 anti-deadlock 設計
- **Source**: https://github.com/nrfconnect/sdk-nrf/pull/17441

### Kconfig 參數

```kconfig
# 可丟棄 event pool 大小（預設 3，最大 255）
BT_BUF_EVT_DISCARDABLE_COUNT=3

# 每個可丟棄 event buffer 大小（預設 43-58 bytes，最大 255）
BT_BUF_EVT_DISCARDABLE_SIZE=58
```

### 3 種作法評估

| 作法 | 描述 | 風險 | 推薦度 |
|------|------|------|--------|
| **Pool 加大** | 提高 `BT_BUF_EVT_DISCARDABLE_COUNT` 至 20 | 低（增加 RAM ~1KB） | **推薦** |
| **Patch（移除 discardable 標記）** | 直接修改 `hci_driver.c` 移除 discardable flag | 高（deadlock 風險） | 不推薦 |
| **App gap detection** | Application 層偵測 event 缺口，補插值 | 中（需額外邏輯） | 輔助手段 |

---

## 業界 Reference

| 名稱 | URL |
|------|-----|
| PR #2219 (QoS 0x80) | https://github.com/nrfconnect/sdk-nrf/pull/2219 |
| PR #17441 (Anchor 0x82) | https://github.com/nrfconnect/sdk-nrf/pull/17441 |

---

## 對 A2 架構的影響

- **A2 INGEST 層**直接依賴 `0x80` QoS Conn Event Report，若 event 被 discard 則 METRICS 量測資料出現缺口。
- Pool 加大是最安全的作法，BT_BUF_EVT_DISCARDABLE_COUNT=20 增加約 1KB RAM（對 nRF52833 可接受，見 finding-08）。
- App gap detection 作為輔助：當 INGEST 層偵測到 sequence number 跳號時觸發插值或告警。

## 對我們系統的影響

- **禁止貿然 patch hci_driver.c**：移除 discardable 標記會破壞 anti-deadlock 保護，在高負載或干擾場景下可能造成整個 BT stack 死鎖。
- **Kconfig 設定**：在 `prj.conf` 加入：
  ```kconfig
  CONFIG_BT_BUF_EVT_DISCARDABLE_COUNT=20
  CONFIG_BT_BUF_EVT_DISCARDABLE_SIZE=58
  ```
- App gap detection 需寫入 A2 INGEST 層的設計規格（F-A2-INGEST AC 項目）。
