# App Display Contract: Impact-based Update 完整報告

本報告根據 `pasted_content.txt` 的任務目標，將現有的工程圖擴展為包含 RML-lite 上游需求、Traceability、驗收標準與測試案例的完整規格系統。

---

## A. 現況分析表 (STEP 1)
| Artifact | Purpose | Strength | Missing Upstream | Risk |
| :--- | :--- | :--- | :--- | :--- |
| **Block Diagram** | 定義 App 三層架構與 GW 資料來源的靜態對應關係。 | 清楚界定 L1/L2/L3 職責與資料流向。 | 缺少 RML-ROL (角色權限) 與 RML-SCP (功能範圍) 的具體定義。 | 若角色權限變更，方塊圖無法體現存取限制。 |
| **State Diagram** | 描述 `operational_state` 與 `sync_state` 的動態轉換。 | 涵蓋了主要的狀態轉移邏輯與同步狀態。 | 缺少 RML-CST (約束) 與 RML-RSK (風險處理)。 | 狀態機在異常邊界（Timeout/Retry）定義不明。 |
| **Sequence Diagram** | 描述 App 與 GW 之間的通訊時序。 | 視覺化了通訊流程與同步機制。 | 缺少 RML-FLW (業務流程) 與 RML-FEA (功能分解)。 | 通訊協定變更時，時序圖與需求可能脫節。 |
| **Packet Diagram** | 定義 GATT STATUS 與 Roster Entry 的位元結構。 | 提供實作層級的精確資料格式。 | 缺少 RML-OBJ (系統目標) 與 RML-CST (頻寬/功耗約束)。 | 封包設計若未考慮功耗約束，可能導致裝置耗電過快。 |

---

## B. 建議文件目錄樹 (STEP 2)
```text
docs/
  ├── rml_lite.md           # 上游需求 (Goals, Roles, Scope, Features)
  ├── requirements.md       # 功能需求 (REQ-001...)
  ├── architecture.md       # 系統架構與模組 (BLK-001...)
  ├── state_machine.md      # 狀態機定義 (STA-001...)
  ├── sequence_flows.md     # 通訊時序 (SEQ-001...)
  ├── packet_contract.md    # 封包與 GATT 規格 (PKT-001...)
  ├── acceptance_criteria.md # 驗收標準 (AC-001...)
  └── test_cases.md         # 測試案例 (TC-001...)
trace/
  ├── trace_map.yaml        # 追蹤矩陣 (REQ -> AC -> TC)
  └── change_rules.md       # 變更同步規則 (Impact Rules)
```

---

## C. 每份文件的角色說明 (STEP 2)
| Document | Purpose | Owner | Sync Trigger |
| :--- | :--- | :--- | :--- |
| **rml_lite.md** | 定義系統目標、角色與範圍。 | PM / Architect | 商業目標變更、角色權限調整。 |
| **requirements.md** | 將 RML 轉化為可實作的功能需求。 | PM / Firmware | RML 變更、功能新增/刪除。 |
| **acceptance_criteria.md** | 定義功能完成的判定標準。 | QA / PM | 需求變更、法規/安全標準更新。 |
| **trace_map.yaml** | 維護各層級 ID 的映射關係。 | Cross-functional | 任何 ID 新增、刪除或關聯變更。 |

---

## D. 全部文件骨架內容 (STEP 3)
*(詳見附件 `step3_skeletons_part1.md`, `step3_skeletons_part2.md`, `step3_skeletons_part3.md`)*

### 示例：功能需求 (requirements.md)
| ID | Description | Rationale | Priority | Source | Related Artifacts | AC Link | TC Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-001** | App 應能顯示 ED 的即時 RSSI 與 Zone 資訊。 | 讓 Installer 判斷訊號品質。 | High | RML-FEA-001 | BLK-001, PKT-001 | AC-001 | TC-001 |

---

## E. trace_map.yaml 範本 (STEP 3)
```yaml
requirement_to_artifacts:
  REQ-001: [BLK-001, PKT-001]
  REQ-002: [STA-001, SEQ-001]

requirement_to_acceptance:
  REQ-001: [AC-001]
  REQ-002: [AC-002]

requirement_to_tests:
  REQ-001: [TC-001]
  REQ-002: [TC-002]
```

---

## F. Change Impact Rules (STEP 4)
| Rule ID | Trigger | Must Update | Should Review | Risk if skipped |
| :--- | :--- | :--- | :--- | :--- |
| **CIR-001** | **Requirement text changed** | AC-*, TC-* | STA-*, SEQ-*, PKT-* | 需求與驗收脫節。 |
| **CIR-002** | **New state added** | state_machine.md, sequence_flows.md | architecture.md, REQ-* | 系統進入未定義狀態。 |
| **CIR-005** | **Packet field added/removed** | packet_contract.md, architecture.md | REQ-*, TC-* | 封包解析位移錯誤。 |

---

## G. Consistency Check Summary (STEP 5)
- **可追蹤性**: 已建立從 RML-lite 到 AC/TC 的 ID 體系。
- **覆蓋率**: 示例需求已完整對應至所有下游 Artifacts。
- **同步規則**: 已定義 CIR-001 至 CIR-009。

---

## H. Missing Inputs / Suggested Additions / Top 3 Desync Risks (STEP 5)
### Missing Inputs
- **RML-RSK (風險處理)**: 尚未定義「資料衝突 (Conflict)」與「裝置重啟 (Reboot)」的恢復路徑。
- **AC 測量工具**: 尚未定義封包模擬器或 BLE Sniffer 的工具鏈規格。

### Suggested Additions
1. **補強 RML-RSK-002**: 定義「權威來源 (Source of Truth)」判定規則。
2. **新增 PKT-002 (Error Packet)**: 定義錯誤代碼封包。

### Top 3 Desync Risks
1. **圖改需求沒改**: 修改狀態圖但未更新需求與驗收標準，導致漏測。
2. **需求改測試沒改**: 修改顯示頻率但測試案例仍沿用舊標準，導致誤判。
3. **封包位移偏移**: 修改封包結構後未同步更新解析邏輯，導致全系統資料錯誤。
