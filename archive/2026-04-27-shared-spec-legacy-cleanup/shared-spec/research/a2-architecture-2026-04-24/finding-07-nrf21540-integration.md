<!-- A2 research dump from 8 sub-agent fan-out, 2026-04-24 -->

# Finding 07 — nRF21540 FEM + QoS 整合分析

## Sub-Agent 任務描述

調查 nRF21540 FEM (Front-End Module) 與 BLE QoS 整合的現有案例，
評估 TX power 重校需求、FCC 法規限制與 A2 CONTROL 層的聯動要求。

---

## Key Findings

### 公開整合案例

- **nRF21540 + BLE QoS 整合案例：0 個**
- 全球無任何公開的 nRF21540 + 即時 QoS 自適應整合記錄
- **first-of-its-kind** 確認（與 finding-04 一致）

### TX Power 重校需求

nRF21540 提供：
- **TX gain**：+20 dBm（PA 放大）
- **RX gain**：+13 dBm（LNA 低雜訊放大）

**必須設定的 Kconfig**：
```kconfig
CONFIG_BT_CTLR_TX_PWR_ANTENNA=20
```

不設定此值會導致 TX power 語意錯誤（SoC output vs antenna output，見 finding-02 BC-4）。

### FCC 法規限制

| 限制項目 | 規範 | 對 A2 的影響 |
|---------|------|------------|
| BLE +20dBm | 踩上限，無餘量 | 預設 TX zone 不能再升 |
| AFH 最少 15 channels | 若 channel 數不足，必須降功率 | channel manager 跟 TX policy 必聯動 |

**關鍵約束**：FCC Part 15 要求 BLE 使用 AFH (Adaptive Frequency Hopping) 時，
若活躍 channel 數 < 15，必須降低 TX power，
否則視為違法（超出 spread spectrum 豁免條件）。

### FEM Settling Time 問題

- nRF21540 PDN (Power Down) settling time：~18µs
- BT 6.2 SCI 最小 interval：375µs
- **衝突風險**：SCI 模式下每個 interval 都需要 PDN cycle，18µs settling time 佔 375µs 的 4.8%，可能造成 Tx/Rx timing violation
- **影響**：第二代（nRF54L15 + BT 6.2）才需要處理此問題，第一代（7.5ms interval）無影響

### 認證參考

- **FCC ID**: x8wbt40n（Fanstel BT40N，nRF52833 + nRF21540）
- 可作為硬體認證設計參考
- **Source**: https://fcc.report/FCC-ID/x8wbt40n/6540258.pdf

---

## 業界 Reference

| 名稱 | URL |
|------|-----|
| nRF21540 NCS Optional Properties | https://developer.nordicsemi.com/nRF_Connect_SDK/doc-legacy/2.7.0-rc3/nrf/device_guides/fem/fem_nRF21540_optional_properties.html |
| Fanstel BT40N FCC ID | https://fcc.report/FCC-ID/x8wbt40n/6540258.pdf |
| Nordic DevZone: nRF21540 + nRF52833 BLE | https://devzone.nordicsemi.com/f/nordic-q-a/94461/add-support-for-fem-nrf21540-with-ble-nrf52833-running-on-softdevice |

---

## 對 A2 架構的影響

- **A2 CONTROL 層**必須實作 channel manager 與 TX policy 的強制聯動：
  - 當 active channel 數 < 15 → 強制降功率（FCC 合規）
  - 當降功率後 channel quality 惡化 → 觸發 channel scan 擴充 channel 數
  - 形成閉環控制：channel count ↔ TX power
- TX power zone 分級必須以 antenna power 為準（非 SoC output），影響 POLICY 層的 zone 定義。

## 對我們系統的影響

- **A2 CONTROL 層 AC 項目新增**：FCC AFH ≥15 channel 強制，channel manager 跟 TX policy 必聯動。
- `CONFIG_BT_CTLR_TX_PWR_ANTENNA=20` 必須寫入 firmware 的 `prj.conf`（非可選）。
- FEM settling time 問題暫不處理（第一代 interval ≥7.5ms 無衝突），列入第二代 backlog。
- 建議 market-compliance-matrix 補充此 FCC AFH 條目。
