# Constraints — arc42 §2

> arc42 §2 Architecture Constraints: legally mandated, technically imposed, and organizationally
> agreed constraints that shape every architectural decision in this system.
>
> Cross-ref: `06_crosscutting-integration/market-compliance-matrix.md` (per-standard repo split)
> SSOT for NCS SDK version: `ble_qos_demo_V1.2m/scripts/dev.sh` (`NCS_HOME` default, line ~32)

---

## 1. 法規限制（Legal / Regulatory）

### 1.1 無線電認證

| 標準 | 要求摘要 | 影響範圍 | 責任 repo |
|------|---------|---------|---------|
| **BLE SIG** Bluetooth Qualification | 使用 Bluetooth 商標及協定必須通過 Bluetooth SIG QDID 認證流程；底層 SoftDevice / Zephyr BLE Host 均須持有有效 QDID | Firmware (BLE Host stack) | firmware |
| **NCC** (台灣通傳會) 電信法第 49 條 | 在台灣市場銷售或使用的短距離射頻模組（2.4 GHz BLE）須取得 NCC 型式認證（型式驗證標誌 `CCAF-XXXX`） | nRF52833 模組、射頻前端 | firmware / HW |
| **FCC** Part 15 (美國) | 在美國市場部署須符合 FCC Part 15 Subpart B（無意輻射）及 Subpart C（有意輻射）；BLE 落入 Part 15.247 (2.4 GHz) | nRF52833 模組 | firmware / HW |
| **CE / RED** (歐盟) | 進入歐盟市場須符合 Radio Equipment Directive 2014/53/EU，提交 DoC 及技術文件 | 射頻模組、韌體 | firmware / HW |

> **QDID 衍生約束**：系統不得自行修改 Bluetooth Host 協定層行為（如自訂 LL PDU 格式）以免
> 使現有 QDID 失效。任何 BLE Host stack 升級必須驗證 QDID 有效性。

### 1.2 工控 / 資安合規

| 標準 | 要求摘要 | 影響範圍 |
|------|---------|---------|
| **IEC 62443** SL 1–2 | Industrial Automation and Control Systems 安全等級：SL 1（authenticated pairing）由韌體 + App 共同實作；SL 2（audit log timestamps）由韌體 NVS ring + Central persistence 共同實作；詳見 `market-compliance-matrix.md § ISA-62443` | firmware, central, app |
| **IEC 62304** Class B | 軟體生命週期管理：anomaly log in NVS、version traceability (git hash)、unit test coverage gate；僅在 Medical 市場設定檔啟用 | firmware, central |
| **ISO 21434 / UNECE R155** | 汽車後裝市場：FOTA 簽名驗證、CSMS audit export；僅在 Automotive 設定檔啟用 | firmware, central |

> 市場設定檔由韌體 Kconfig `menu "Market Compliance Profile"` 控制（SSOT: firmware repo `Kconfig`）。
> 上述法規不全部同時啟用；spec-pack 只記錄系統能支援的義務，實際啟用見 Kconfig。

---

## 2. 技術限制（Technical）

### 2.1 Zephyr / NCS SDK 邊界

| 約束 | 細節 | 引用 |
|------|------|------|
| **NCS SDK 版本 SSOT** | `NCS_HOME` 預設路徑定義於 `scripts/dev.sh` line ~32；所有 CI、本地 build、文件引用均以此為 SSOT，禁止各處硬編碼版本號 | `ble_qos_demo_V1.2m/scripts/dev.sh` |
| **Zephyr RTOS 排程器** | 使用 Zephyr 協作式 + 搶佔式多執行緒；`CONFIG_PREEMPT_ENABLED=y` 為預設；GW QoS 排程器不得使用 busy-wait 阻塞 Zephyr 主迴圈 | Zephyr kernel config |
| **Zephyr BLE Host** | 使用 Zephyr 原生 BLE Host（非 SoftDevice）；NCS SDK 提供 LL + Host 整合；不得繞過 Zephyr BLE API 直接操作 radio | `ble_api.yaml` GATT 定義 |
| **NCS 設定系統** | Kconfig + devicetree 為 NCS 唯一 config 機制；runtime 可調參數透過 `CMD_V2 opcode 0x07`（TUNE-VAL）注入，不得 build-time hardcode | `ble_api.yaml` → opcodes 0x07 |
| **Zephyr FLASH API** | NVS 使用 Zephyr NVS subsystem；Flash driver 依 devicetree overlay 決定（nRF52833 內部 Flash 或外接 SPI Flash）；不得直接呼叫 nrfx Flash API | firmware docs |
| **West workspace** | NCS 採用 West manifest 管理多 repo；不得在 `CMakeLists.txt` 中自行 `add_subdirectory` NCS 子模組 | `west.yml` |

### 2.2 nRF52833 硬體限制

| 資源 | 容量 / 規格 | 架構影響 |
|------|-----------|---------|
| Internal Flash | 512 KB | 韌體 image + NVS 共用；LOG ring buffer 移至外接 SPI Flash（見 ADR-009） |
| RAM | 128 KB | BLE 連線數受限（每條連線約消耗 ~3 KB 連線 context）；GW MAX_ED 上限由此推導 |
| BLE connections | nRF52833 硬體最大 20 條（含 Central + Peripheral 角色混合） | GW 同時作 Central（連 ED）+ Peripheral（連 App）消耗 ≥2 role slot |
| TX power range | −20 dBm ～ +8 dBm | QoS Zone TX power cap 必須在此範圍內；ATEX profile 另有上限 |
| Clock | 64 MHz Cortex-M4F | QoS 排程計算不得超過 1 ms 時間槽（避免 RTOS deadline miss） |
| 外接 SPI Flash | 容量由 PCB BOM 決定（HW constraint） | LOG subsystem SSOT；見 ADR-009 |

### 2.3 BLE 協定限制

| 約束 | 細節 |
|------|------|
| MTU / ATT payload | ATT MTU 最大 247 bytes（BLE 5.2 LE Data Length Extension）；CAPS_V2 CBOR payload 必須分包傳輸若超出 MTU |
| PHY 相容性 | 2M PHY 與 Coded PHY 不可同時在同一個 connection 啟用；Zone 切換需走 LL PHY Update Procedure |
| Advertising interval | 合規 BLE SIG 規範下 adv interval 不得 < 20 ms（non-connectable undirected）；connectable: < 100 ms 可能影響 scan duty cycle |
| Connection parameter | `conn_interval` / `slave_latency` / `supervision_timeout` 三者互鎖（BLE Spec §6.C.1）；GW 若自行更新 connection parameters 必須符合 App 端接受視窗 |

---

## 3. 組織限制（Organizational）

### 3.1 四 Repo Workspace 結構

| 限制 | 說明 |
|------|------|
| 強制 4-repo split | `ble_qos_demo_V1.2m/`（firmware）、`ble_qos_app/`（App）、`central-device-metadata/`（Central）、`rml-system-spec-pack/`（spec）四個 repo 各自獨立 git history；不得合併成 monorepo | 
| 跨 repo 變更協議 | 任何觸及 `ble_api.yaml` 的變更必須同步通知下游 3 個 repo，並完成 cascade test（Spec Hygiene Rule 12）|
| PR ≤ 5 files 限制 | 每個 PR 改動檔案 ≤ 5 個（global AI coding standard governance rule） |
| Branch protection | `main` branch 受 protection；不得 force push；所有變更必須走 PR + CI gate |

### 3.2 Spec-as-Code 強制規範

| 限制 | 說明 |
|------|------|
| arc42 章節結構 | 所有系統 spec 必須遵循 arc42 10-chapter 結構（`00_introduction-goals/` ～ `11_risks-and-debt/`）；不得在結構外放 spec 文件 |
| 詞彙管制 | 新 cross-repo 術語必須先在 `01_context-scope/ubiquitous-language.md` 登錄（Spec Hygiene Rule 13）；廢棄詞彙前綴（如舊版路徑前綴、舊 feature ID 格式）觸發 CI vocab-check 失敗 |
| 圖表 contract | 所有 `.d2` / `.mmd` 圖表必須帶 AI Diagram Contract comment block；render artifact（PNG）不是 SSOT |
| 文件大小限制 | 每個 `.md` 檔 ≤ 300 行（doc-size-limit hook 強制）；超過必須 fractal split |

### 3.3 Vocab-Check CI Ruleset

CI pipeline 包含 `vocab-check` linter（`tools/check_vocabulary_alignment.py`），掃描規則：
- 禁止：已廢棄的舊 feature ID 格式（`RML-FEA-\d+`）
- 禁止：已廢棄的舊路徑前綴（legacy dir — 已由 arc42 章節路徑取代）
- 禁止：單獨出現的 `S-\d+` / `X-\d+`（應使用 F-NN 或 FEA-NNN）
- 強制出現：新 feature 必須使用 `FEA-NNN-` 或 `F-NN` 前綴
- CI gate 失敗 → PR 不得 merge

---

## 4. 商業限制（Business）

### 4.1 硬體成本與數量

| 項目 | 數量 | 說明 |
|------|------|------|
| nRF52833 DK 開發板 | 4 片 | GW × 1、ED × 2、CC × 1；Nordic PCA10100 EVK 單片市價 ~NT$3,000 |
| Pixel 7a（Android 16） | 1 支 | App 目標裝置（ADB SN: `3A271JEHN05259`）；代表 Android 13+ 目標市場 |
| Mac mini（M 系列） | 1 台 | Central 開發主機；FastAPI + PostgreSQL 開發環境 |

> **成本約束**：Demo 設備數量固定（不得透過 spec 決策額外增加 DK 數量），
> 所有 multi-ED 測試場景最多 2 個 ED 同時在線。

### 4.2 開發時程

| 約束 | 說明 |
|------|------|
| 里程碑驅動 | 10-milestone 路線圖（見 `00_introduction-goals/system-intent.md`）；每個 milestone 對應明確的 acceptance criteria |
| Spec-first pipeline | 新功能必須先完成 BDD spec → Contract spec → SDD 三階段 gate，再開始 impl；不接受 spec 追 code |
| AI-assisted delivery | Claude Code 作為主要 implementation agent；每個 PR ≤ 500 行（AI Code Governance standard） |

### 4.3 COTS 依賴

| 依賴 | 版本 SSOT | 替換成本評估 |
|------|----------|------------|
| NCS SDK（含 Zephyr） | `scripts/dev.sh` `NCS_HOME` 預設路徑 | 高：替換需重寫 BSP + BLE Host 整合；不接受 |
| Flutter SDK | `ble_qos_app/pubspec.yaml` | 中：僅 App 層受影響 |
| FastAPI + PostgreSQL | `central-device-metadata/requirements.txt` | 中：僅 Central 層受影響 |
| D2 diagram tooling | `scripts/render-diagrams.sh` | 低：圖表 source 可轉 Mermaid |
| Docker（unit test sandbox） | `scripts/run_unit_tests.sh` | 低：僅 CI 環境依賴 |

> **Lock-in 風險**：NCS SDK 是最高依賴風險項；任何 NCS 大版本升級（如 v2.x → v3.x）
> 必須立即更新 `scripts/dev.sh` 並觸發全 repo CI 驗證。

---

## 5. Cross-references

- 法規詳細 repo 責任分工：`06_crosscutting-integration/market-compliance-matrix.md`
- NCS SDK 版本 SSOT：`ble_qos_demo_V1.2m/scripts/dev.sh`（`NCS_HOME` 預設路徑）
- 硬體 inventory：`04_runtime-view/deployment-topology.md` §1
- Vocab 管制規則：`01_context-scope/ubiquitous-language.md`
- ADR 決策追蹤：`docs/decisions/` (ADR-001 ～ ADR-012)
