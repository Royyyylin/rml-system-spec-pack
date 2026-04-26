<!-- A2 research dump from 8 sub-agent fan-out, 2026-04-24 -->

# Finding 08 — nRF52833 vs nRF54L15 資源分析

## Sub-Agent 任務描述

評估 nRF52833 的 RAM 是否足以支撐 A2 中等配置，
計算詳細記憶體估算，並分析 nRF54L15 的升級成本與觸發條件。

---

## Key Findings

### nRF52833 RAM 估算

**硬體規格**：nRF52833 共 64 KB RAM

#### A2 中等配置記憶體估算（9 連線）

| 項目 | 估算 | 備註 |
|------|------|------|
| SDC 9 連線基礎 | ~8.3 KB | sdc.h 文件數值 |
| A2 per-conn runtime | ~7 KB | 9 連線 × ~780 bytes |
| A2 全域狀態 | ~6 KB | METRICS history buffer + POLICY state |
| **A2 總計** | **~21 KB** | SDC + per-conn + 全域 |
| **剩餘可用** | **~43 KB** | 64KB - 21KB |

**結論：nRF52833 RAM 可行，剩餘 43 KB 足夠 Zephyr kernel + stack + heap。**

#### 5 個 RAM 精簡策略

1. **History buffer 壓縮**：METRICS 歷史資料用 ring buffer，固定 N 個 slot，超出捨棄最舊
2. **Per-conn struct 共用欄位提取**：將所有連線共用的常數移到全域 singleton
3. **Channel quality bitmap 壓縮**：37 channels 用 64-bit bitmap 替代 array
4. **POLICY 計算 on-demand**：不預存計算結果，決策時即時計算
5. **BT_BUF_EVT_DISCARDABLE_COUNT 調整**：pool 加大至 20 增加 ~1KB，但換取 event 不遺漏

### nRF54L15 規格

| 項目 | 規格 |
|------|------|
| RAM | 256 KB（nRF52833 的 4 倍） |
| BT 版本 | BT 6.0（支援 BT 6.2 SCI 升級路徑） |
| 發布時間 | 2024-11（已量產） |
| NCS 支援 | v2.9+ |
| 升級成本 | 3-6 人週（BSP + 驅動 + 認證） |

### 升級觸發條件（第一代 → 第二代）

| 觸發條件 | 說明 |
|---------|------|
| `MAX_ED > 12` | 最大節點數超過 12，RAM 開始吃緊 |
| 需要 Channel Sounding | BT 6.0+ 功能，nRF52833 不支援 |
| p99 < 10ms 要求 | 需要 BT 6.2 SCI，nRF52833 不支援 |

---

## 業界 Reference

| 名稱 | URL |
|------|-----|
| SDC sdc.h（RAM 估算依據） | https://github.com/nrfconnect/sdk-nrfxlib/blob/main/softdevice_controller/include/sdc.h |
| Nordic nRF54L15 發布公告 | https://www.nordicsemi.com/Nordic-news/2024/11/Nordic-Semiconductor-launches-nRF54L15-nRF54L10-and-nRF54L05-next-generation-wireless-SoCs |

---

## 對 A2 架構的影響

- **第一代 A2 設計以 nRF52833 為基準**，RAM 預算 21 KB，需嚴格控制。
- A2 per-conn struct 大小是關鍵設計約束，建議在 SDD 中明列 struct size budget（≤780 bytes/conn）。
- 5 個精簡策略中，history buffer 壓縮（策略 1）和 channel quality bitmap 壓縮（策略 3）應作為預設設計，其他列為 fallback。

## 對我們系統的影響

- **第一代繼續使用 nRF52833**，RAM 估算 ~21 KB 可行，無需立即升級。
- **nRF54L15 作為第二代目標**，觸發條件明確（MAX_ED > 12 / Channel Sounding / p99 < 10ms）。
- A2 SDD 必須包含 RAM budget table，確保實作不超過估算。
- 升級成本 3-6 人週需提前排入路線圖（非緊急，但需在第二代規劃時預算）。
