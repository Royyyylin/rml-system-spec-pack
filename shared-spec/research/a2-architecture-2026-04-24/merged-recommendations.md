<!-- A2 research dump from 8 sub-agent fan-out, 2026-04-24 -->

# Merged Recommendations — A2 Architecture 整合建議

> 本文件整合 8 個 sub-agent finding（finding-01 到 finding-08）的結論，
> 形成可直接作為決策依據的行動建議。

---

## 1. NCS 升級策略 → v3.2.0 推薦

**決定**：鎖定升級至 NCS v3.2.0，不升至 v3.3.0。

**理由**：
- v3.2.0 提供 A2 所需的所有功能：Channel Survey（正式 Supported）、rssi_power_control sample、path_loss_monitoring sample、最小 3ms interval
- v3.3.0 額外 breaking change（NVS header 路徑、bt_conn_le_info.interval 單位）增加遷移成本，但無對應的 A2 功能收益
- 遷移工程估算：3-5 人日（見 finding-02）

**行動**：`west.yml` 固定 NCS v3.2.0，禁止自動浮動至最新版本。

---

## 2. A2 實作路線 → 4 Sub-Feature × 3 Role Matrix（finding-09 更新）

**決定**：A2 拆分為 4 個獨立 sub-feature，按序實作；並區分 GW / ED / CC 三角色的 profile。

| Sub-Feature | 功能 | 依賴 |
|-------------|------|------|
| **F-A2-INGEST** | HCI event 接收、0x80/0x82 event parsing、gap detection | F-LOG-BITMAP SDD 完成 |
| **F-A2-METRICS** | per-conn RSSI/channel quality/interval 量測與歷史 ring buffer | F-A2-INGEST |
| **F-A2-POLICY** | 多維度決策引擎（channel map / interval / TX power / PHY） | F-A2-METRICS |
| **F-A2-CONTROL** | SDC API 執行、TX power 聯動 channel manager、FCC 合規強制 | F-A2-POLICY |

**三角色 profile**：優先實作 GW 版本（full），ED / CC 共用 50-100% 的 core framework，
policy 和 control 依角色差異化（ED 60% 共用，CC 30% 共用）。
不需要 12 份獨立 spec；整體實作量 ≈ 1.5× 單角色工作量。

**對應第二份報告 10 milestone**：Milestone 1-3（PoC）對應 F-A2-INGEST/METRICS，Milestone 4-7 對應 F-A2-POLICY/CONTROL。

---

## 3. p99 驗收目標 → 20ms（GW 定義，finding-09 補加角色說明）

**決定**：第一代 p99 驗收標準定為 20ms，10ms 列為第二代 stretch goal。

**角色說明（finding-09 補充）**：
- **20ms 是 GW-to-Phone/Central system-level p99**：GW 作為 central，管理 8 ED + 1 Phone 連線的端對端延遲
- **ED p99**：由 GW QoS 決策決定；ED 自身無 p99 authority，不獨立驗收
- **CC p99**：transport reliability 優先；CC 作為 bridge，指標為 throughput / packet loss，不直接套用 20ms

**共同理由**：
- 業界傳統 BLE 實測：15-30ms（clean 環境），50-100ms（干擾環境）
- 20ms 對應 clean 環境下限，需要 A2 主動 QoS 介入才能在有干擾環境達標
- 10ms 需要 BT 6.2 SCI + nRF54L15，超出第一代硬體能力（見 finding-06、finding-08）
- Roy 第二份報告的目標與此一致

**驗收條件**：測試環境必須包含 2.4GHz 干擾（Wi-Fi + 微波爐模擬），不接受 clean 環境單獨驗收。

---

## 4. F-LOG-BITMAP SDD 先完成 → 接 F-A2-INGEST BDD

**決定**：F-LOG-BITMAP SDD 必須在 F-A2-INGEST BDD 開始前完成。

**理由**：
- A2 INGEST 層依賴 LOG observability 基礎，需要 LOG event 的接收與解析能力
- F-LOG-BITMAP 的 27 個 LOG event 中，與 A2 相關的事件（QoS event report、anchor event）必須在 SDD 中明定 encoding
- 若 F-LOG-BITMAP SDD 未完成，F-A2-INGEST 的 BDD scenario 無法準確描述 event 格式

**行動**：目前 F-LOG-BITMAP SDD 狀態為最高優先，F-A2-INGEST BDD 暫不開工。

---

## 5. IMPL FREEZE 對 A2 PoC 例外規則

**決定**：A2 PoC（Milestone 1-3）作為 IMPL FREEZE 例外，Milestone 4+ 走正式解凍流程。

**例外範圍**：
- F-A2-INGEST：HCI event parsing 最小可行版本
- F-A2-METRICS：RSSI + channel quality 基礎量測
- RAM budget verification（nRF52833 ~21KB 實測確認）

**Milestone 4+ 解凍流程**：需提交 PoC 量測結果 + POLICY 演算法設計文件 + spec 更新，才可開始 F-A2-POLICY 實作。

---

## 6. Clean-Room 雙軌團隊建議

**決定**：A2 實作採用 clean-room 雙軌隔離。

| 團隊 | 職責 | 禁止事項 |
|------|------|---------|
| Spec/Measurement | 制定 A2 AC、量測方法、驗收標準 | 禁止看 implementation code |
| Implementation | 按 spec 實作 A2 sub-feature | 禁止參與 spec 制定討論 |

**理由**：業界無 open source 可借鑑（finding-04），A2 是首創實作，clean-room 可避免設計被實作細節反向污染。

---

## 7. Discardable Pool 加大（不貿然 patch）

**決定**：`BT_BUF_EVT_DISCARDABLE_COUNT=20`，輔以 app gap detection，禁止 patch hci_driver.c。

```kconfig
CONFIG_BT_BUF_EVT_DISCARDABLE_COUNT=20
CONFIG_BT_BUF_EVT_DISCARDABLE_SIZE=58
```

RAM 影響：+1.1 KB（可接受，見 finding-08）。
App gap detection：F-A2-INGEST 必須實作 sequence number 監控，跳號時告警。

---

## 8. nRF21540 TX Power Policy 聯動 Channel Manager

**決定**：A2 CONTROL 層強制實作 FCC AFH 聯動。

**規則**：
- Active channel 數 ≥ 15：TX power 可使用最大值（+20dBm antenna）
- Active channel 數 < 15：TX power 必須降至合規水準（待 FCC 認證確認閾值）
- 此聯動邏輯必須寫入 F-A2-CONTROL 的 AC 項目

**Kconfig 強制**：`CONFIG_BT_CTLR_TX_PWR_ANTENNA=20` 為必設項目。

---

## 9. 第一代 nRF52833 繼續，nRF54L15 第二代

**決定**：第一代產品繼續使用 nRF52833，nRF54L15 作為第二代升級目標。

**升級觸發條件**（任一滿足即啟動第二代規劃）：
1. MAX_ED（最大連線數）需求 > 12
2. 需要 Channel Sounding 功能（BT 6.0+）
3. p99 目標要求 < 10ms

**升級成本預估**：3-6 人週（BSP 移植 + 驅動更新 + 認證重跑）。
