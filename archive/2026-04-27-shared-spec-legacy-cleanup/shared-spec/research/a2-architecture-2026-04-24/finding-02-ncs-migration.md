<!-- A2 research dump from 8 sub-agent fan-out, 2026-04-24 -->

# Finding 02 — NCS v2.9.2 → v3.3.0 Breaking Change 分析

## Sub-Agent 任務描述

調查從 NCS (nRF Connect SDK) v2.9.2 升級至 v3.3.0 的所有 breaking change，
評估遷移難度與工程人日估算，重點關注 BLE / SDC / HCI 相關 API。

---

## Key Findings

- **遷移難度**：中等（3-5 工程人日）
- **主要 breaking change 數量**：5 個影響 BLE QoS 實作的重大變更

### Breaking Change 清單

#### BC-1: NVS Header 路徑變更（Zephyr 4.4）

```c
// 舊路徑（v2.9.2）
#include <zephyr/fs/nvs.h>

// 新路徑（v3.3.0 / Zephyr 4.4）
#include <zephyr/kvss/nvs.h>
```

影響範圍：所有使用 NVS 的模組（config 持久化）

#### BC-2: `bt_conn_le_info.interval` 單位變更（Zephyr 4.4）

```c
// 舊語意：1.25ms 單位（v2.9.2）
uint16_t interval;  // 單位 1.25ms

// 新語意：微秒（v3.3.0）
uint32_t interval;  // 單位 us
```

影響範圍：A2 METRICS 層所有 connection interval 讀取與計算邏輯

#### BC-3: `sdc_support_*` 函數回傳型別變更（NCS v3.2.0）

```c
// 舊（v2.9.2）
int sdc_support_le_2m_phy(void);
int sdc_support_le_coded_phy(void);

// 新（v3.2.0+）
void sdc_support_le_2m_phy(void);
void sdc_support_le_coded_phy(void);
```

影響範圍：SDC 初始化程式碼中的回傳值檢查

#### BC-4: TX Power 語意變更

- 舊語意：SoC output power（晶片輸出）
- 新語意：antenna power（天線等效功率）
- 影響 nRF21540 FEM 場景下的 TX power 計算（詳見 finding-07）

#### BC-5: GATT / HCI API 棄用

- `_bt_gatt_ccc` rename（影響 GATT notification 訂閱）
- `bt_hci_cmd_create` deprecated（影響 HCI raw command 場景）

---

## 業界 Reference

| 文件 | URL |
|------|-----|
| NCS 3.0 Migration Guide | https://docs.nordicsemi.com/bundle/ncs-3.0.1/page/nrf/releases_and_maturity/migration/migration_guide_3.0.html |
| Zephyr 4.4 Migration Guide | https://docs.zephyrproject.org/latest/releases/migration-guide-4.4.html |

---

## 對 A2 架構的影響

- **METRICS 層**：`bt_conn_le_info.interval` 單位變更直接影響 connection interval 量測，需全面更新計算邏輯。
- **INGEST 層**：NVS header 變更影響 QoS 歷史資料持久化模組。
- **CONTROL 層**：SDC API 回傳型別變更影響 SDC 初始化與 PHY 支援宣告。

## 對我們系統的影響

- **推薦升至 v3.2.0 而非 v3.3.0**（見 finding-03），v3.2.0 已有所需新功能且 breaking change 集中在 BC-3，比 v3.3.0 再疊加 BC-1/BC-2 更簡單。
- 工程人日估算：
  - BC-1（header）：0.5 人日（全域 grep + replace）
  - BC-2（interval 單位）：1-2 人日（邏輯驗算）
  - BC-3（sdc_support 回傳）：0.5 人日
  - BC-4（TX power）：0.5 人日（需搭配 finding-07 聯動）
  - BC-5（GATT/HCI）：0.5-1 人日
  - 總計：3-5 人日
