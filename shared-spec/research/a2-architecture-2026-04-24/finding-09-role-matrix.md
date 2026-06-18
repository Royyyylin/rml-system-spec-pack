<!-- A2 research dump from 8 sub-agent fan-out, 2026-04-24 -->

# Finding 09 — GW / ED / CC 三角色 A2 Profile Matrix

## 1. 背景：8 個 Sub-Agent 研究的盲點

Finding-01 至 Finding-08 均以 GW（Gateway）視角分析 A2 架構。
GW 是最複雜角色（9 連線、雙向 HCI opcode、主動 Control plane），
但系統同時部署 ED（End Device）和 CC（CC bridge），三者同為 nRF52833 + nRF21540 硬體，
韌體透過 NVS role byte 切換（`APP_ROLE_GATEWAY=2` / `APP_ROLE_END_DEVICE=1` / `APP_ROLE_CC=4`）。

三角色差異在以下面向顯著：
- HCI opcode 可用集合不同
- 連線數與方向不同（central vs peripheral）
- RAM 預算差異達 3-5×
- p99 責任歸屬不同（GW 是 system-level 決策者，ED/CC 是被動或 transport 層）

不補充三角色 matrix，A2 設計決策（4 sub-feature 範圍、RAM 預算、p99 目標定義）將遺漏重要約束。

---

## 2. VS HCI Opcode 對三角色可用性 Matrix

> 硬體 invariant：nRF52833 + nRF21540 PA/LNA；BLE 5.x；不涉 nRF54L15 / BT 6.2 SCI / Channel Sounding。

| Opcode | 功能 | GW | ED | CC |
|--------|------|----|----|-----|
| 0xfd04 QoS conn event report | 每個 conn event 的 RSSI / CRC / anchor timing | 雙向（主動讀 + 被通知）| 被動（只收自身 conn event）| 被動（收 Phone/Backend conn event）|
| 0xfd05 Event length set | 控制 conn event 最大長度 | **只 central** — GW 作為 central 對 ED 下指令 | ❌ ED 是 peripheral，無法主動 set | ⚠️ CC 上行（對 Phone）為 peripheral，下行（對 Backend）可能是 central，方向依 session 決定 |
| 0xfd0e Channel survey | 掃描 37 channel 背景雜訊 | 雙向 | 雙向 | 雙向 |
| 0xfd11 Average RSSI | 取特定 channel 的平均 RSSI | 雙向 | 雙向 | 雙向 |
| 0xfd12 Central ACL event spacing | 多連線 fairness — 調整 central 到各 peripheral 的 slot 間隔 | **只 central** — GW 管理 8 ED + 1 Phone 的 slot fairness | ❌ ED 是 peripheral，無此需求 | ⚠️ CC 若對 Backend 做 central，可能有限度適用 |
| 0xfd1e Event start task | 對齊 anchor point 觸發外部任務（GPIO / PPI） | 雙向 | 雙向 | 雙向 |
| 0xfd1f Anchor point update | 通知應用層 anchor point timing | 雙向 | 雙向 | 雙向 |
| Channel map update（LL procedure）| 更新 AFH 使用的 37 channel subset | **只 central** 主動發起 — GW 決定哪些 channel 跳頻 | 被動接受 GW 指令 | ⚠️ CC 對 Backend 連線方向時可主動；對 Phone 方向時被動 |
| Conn parameter update（LL procedure）| 更新 interval / latency / timeout | 主動發起（GW 作為 central 對 ED 推送）| 請求 only（向 GW 提出更新請求，GW 有否決權）| ⚠️ 雙向，依上/下行方向而異 |

**⚠️ 說明**：CC bridge 的角色依連線方向分兩面：
- 上行面（CC → Phone）：CC 作為 **peripheral**，被 Phone 連入，行為類似 ED
- 下行面（CC → Backend/Central）：CC 作為 **central**（BLE USB dongle 或 central-side connection），可主動下指令

因此 CC 的 opcode 可用性隨上/下行方向而異，標 ⚠️ 表示「依方向有條件適用」。

---

## 3. 三角色 A2 Profile

| 維度 | GW-A2 | ED-A2 | CC-A2 |
|------|-------|-------|-------|
| Telemetry ingestion | 全 6 維度：RSSI / channel quality / interval / anchor / event length / spacing | 自身 conn 的 RSSI + channel quality；上報至 GW | Transport metric：throughput / RSSI（Phone 側）|
| Policy 決策 | 主排：8 ED + 1 Phone 多連線 fairness + channel map + TX power | 接受 GW 指令；local QoS hint（interval 請求）| Transport layer：throughput / reliability 優先，不做 QoS 排程 |
| Control plane | 主動：channel map update / conn param update / event length set | 請求 only：conn parameter request → GW 決定 | Transport-level：對 Backend 可送 conn param，對 Phone 被動 |
| MAX 連線數 | 9（8 ED + 1 Phone） | 1（與 GW 連線）| 2-3（Phone + Backend/Central）|
| RAM 預算（A2 runtime） | ~27 KB（見第 7 節重算）| ~6 KB | ~10 KB |
| p99 目標 | **20 ms system-level**（GW → Phone/Central 路徑）| 被 GW QoS 決策決定；ED 自身無 p99 authority | Transport throughput 優先；p99 指標為 transport reliability |
| Compliance focus | FCC AFH ≥15 ch 聯動 + audit log | Compliance event 上報至 GW/Central | Transport reliability；不獨立負責 FCC AFH |

---

## 4. 4 Sub-Feature × 3 Role Matrix

| Sub-Feature | GW | ED | CC |
|-------------|----|----|-----|
| **F-A2-INGEST** HCI event 接收 + parsing | **必做（full）**：0xfd04/0xfd0e/0xfd11/0xfd1f/0xfd1e 全解析 | **必做（lightweight subset）**：0xfd04（自身 conn）+ 0xfd0e + 0xfd11 | **必做（transport metric only）**：0xfd04（Phone conn）+ throughput counter |
| **F-A2-METRICS** per-conn ring buffer + 量測 | **必做**：9 conn × 全 6 維度；METRICS history + spacing fairness | **必做（上報型）**：1 conn × RSSI + channel quality；定期打包上報 GW | **必做（transport-focused）**：throughput / latency metric；無 channel fairness |
| **F-A2-POLICY** 多維度決策引擎 | **必做（複雜多連線）**：channel map + interval + TX power + slot fairness；0xfd12 spacing 聯動 | **共用 60%**：interval 請求邏輯 + TX power hint；無 channel map authority | **共用 30% + CC-specific transport policy**：transport throughput 目標替代 QoS 排程 |
| **F-A2-CONTROL** SDC API 執行 | **必做（central 主動）**：channel map update / event length set / 0xfd12 / conn param update（主動推送）| **N/A**：只回 conn parameter request；TX power 被動接受 GW zone 指令 | **有限（transport-level only）**：對 Backend 可送 conn param；TX power 跟通用路徑 |

---

## 5. 實作共用率估算

| 模組 | 共用率 | 說明 |
|------|--------|------|
| Core framework（ingestion queue / event parser / HCI dispatcher）| **100%** | 三角色共享同一套 event 接收與 dispatch 框架 |
| Metrics collection（ring buffer / timestamp / per-conn struct）| **80%** | 欄位數量不同（GW 6 維度 vs ED/CC 子集），但 buffer 結構共用 |
| Policy engine（決策邏輯 + threshold 表）| **50%** | GW 最複雜（多連線 fairness + channel map）；ED 只需 interval hint；CC 改為 transport policy |
| Control plane（SDC API 呼叫 + FCC 聯動）| **30%** | 僅共用 TX power 調整（通用路徑）+ path_loss hint；channel map update 只 GW 用 |

**總結**：A2 實作量 ≈ 1.5× 單角色工作量（非 3× 也非 12 份獨立 spec）。
共用 core framework 一份，policy 和 control 依角色差異化，ED/CC 各取 GW 版本的子集。

---

## 6. 既有規格對三角色的映射

### F-04（GW QoS Scheduler Tuning）
- **GW-only feature**：CMD_V2 opcode 0x07 SET_SCHED_TUNE 本來即針對 GW 的 QoS 排程器。
- ED / CC 不需要 F-04 preset；接受 GW 根據 F-04 做出的 QoS 決策即可。

### F-LOG-BITMAP（27 LOG events）
- **三角色均需**：LOG bitmap 控制 event 輸出，三個 role 的韌體都有 LOG 輸出需求。
- `docs/research/` 中 events.md 已有 `roles` 欄位（例：`GW, ED`），需 annotate 每個 event 適用哪個 role。
- A2 相關 LOG event（QoS event report、anchor point event）需確認 GW / ED / CC 三欄位。

### 27 LOG events 角色 annotation 需求
以現有 events.md 的 `roles` 欄位為 SSOT，補全 CC 欄位（目前推測多數 CC 不 emit GW/ED 專屬事件）。

---

## 7. RAM 預算重算（三角色）

> 原 finding-08 ~21 KB 是 GW（9 連線）的估算數值；以下補全 ED / CC 並修正 GW 估算。

| 角色 | A2 per-conn runtime | SDC 連線基礎 | 全域狀態 + buffer | A2 總計 | 剩餘可用（64 KB RAM - existing ~50%）|
|------|---------------------|-------------|-------------------|---------|--------------------------------------|
| GW | 9 conn × ~780 B ≈ 7 KB | ~8.3 KB（9 conn，sdc.h）| ~12 KB（METRICS history + POLICY + spacing）| **~27 KB** | **餘 ~37 KB** |
| ED | 1 conn × ~350 B ≈ 0.4 KB | ~1 KB（1 conn）| ~2.5 KB（RSSI ring buffer + report buffer）| **~6 KB** | **餘 ~58 KB** |
| CC | 2-3 conn × ~500 B ≈ 1.2 KB | ~2 KB（2-3 conn）| ~4 KB（transport metric + throughput buffer）| **~10 KB** | **餘 ~54 KB** |

**說明**：
- Finding-08 的 GW 估算 ~21 KB 偏低；本次重算加入 POLICY state（~3 KB）和 spacing fairness buffer（~3 KB），
  修正後 GW ≈ 27 KB。剩餘 ~37 KB 仍足夠 Zephyr kernel + stack + heap。
- ED / CC RAM 餘裕充足，無資源壓力。
- nRF52833 64 KB RAM 三角色均可行，結論不變。

---

## 8. 對 Roy 拍板四問題的影響

| 問題 | Finding-08 結論 | Finding-09 補充 / 修正 |
|------|-----------------|------------------------|
| **Q1 NCS 升級（v3.2.0）** | 推薦 v3.2.0，三角色受益相同 | 無影響；v3.2.0 Channel Survey / rssi_power_control 三角色均適用 |
| **Q2 A2 實作路線** | 拆 4 sub-feature | 升級為「4 sub-feature × 3 role profile」；共用率 50-100%，非 12 份獨立 spec |
| **Q3 p99 20ms 目標** | 第一代合理，10ms 為第二代 stretch goal | **修正定義**：20ms 是 GW-to-Phone/Central system-level p99；ED p99 由 GW QoS 決策決定；CC p99 = transport reliability |
| **Q4 F-LOG-BITMAP SDD 順序** | F-LOG-BITMAP SDD 先完成再做 F-A2-INGEST BDD | 無影響；LOG events annotate 三角色 roles 欄位納入 F-LOG-BITMAP SDD scope |

---

## 9. Sources

- `~/Projects/ble_qos_demo/rml-system-spec-pack/shared-spec/glossary.md`（三角色定義、role enum）
- `~/Projects/ble_qos_demo/AGENTS.md`（Role Mapping、Firmware Roles 表）
- `~/Projects/ble_qos_demo/ble_qos_demo_V1.2m/CLAUDE.md`（APP_ROLE_* enum、NVS role byte）
- Finding-01 至 Finding-08（本次研究既有 8 個 sub-agent 結果）
- Finding-08 nRF52833 RAM 估算（~21 KB，本 finding 修正至 ~27 KB）
