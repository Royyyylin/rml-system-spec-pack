# STEP 1 — 現況分析與影響評估 (Impacted Artifacts)

根據 `manus-spec-governance-instruction.md`，本次整合任務將對現有產出進行以下影響評估：

| Artifact | Impact Status | Change Description |
| :--- | :--- | :--- |
| **rml_lite.md** | **Update** | 強化 RML-OBJ (工業級目標) 與 RML-RSK (風險處理)，對齊高利潤市場策略。 |
| **requirements.md** | **Update** | 補齊 REQ-001 ~ REQ-006，確保每個需求都有對應的 AC 與 TC。 |
| **architecture.md** | **Update** | 補齊 BLK-001 ~ BLK-004，明確定義模組職責與輸入輸出。 |
| **state_machine.md** | **Update** | 補齊 STA-001 ~ STA-005，包含 Timeout、Retry 與 Recovery Path。 |
| **sequence_flows.md** | **Update** | 補齊 SEQ-001 ~ SEQ-003，涵蓋 Normal、Error 與 Reboot 流程。 |
| **packet_contract.md** | **Update** | 補齊 PKT-001 (Status) 並新增 PKT-002 (Error Packet)。 |
| **acceptance_criteria.md** | **Update** | 補齊 AC-001 ~ AC-005，確保可量測、可測試。 |
| **test_cases.md** | **Update** | 補齊 TC-001 ~ TC-005，包含 Boundary Test 與 Fault Injection。 |
| **trace_map.yaml** | **Update** | 補齊為正式可機器讀取版本，建立完整追蹤矩陣。 |
| **source_of_truth.md** | **New** | 根據指令明確定義唯一真相來源與修改流程。 |
| **README.md** | **New** | 建立規格包入口導讀。 |
| **tools/** | **New** | 建立 `trace_lint_spec` 與 `changed_only_report` 規格。 |

### 核心變更摘要：
1.  **工業級定位**：將 RML-OBJ 鎖定在取代 RS485 的高利潤工業應用。
2.  **異常閉環**：強制加入 Timeout (5s)、Retry (3次) 與 Recovery (Needs Review) 邏輯。
3.  **單一真相來源**：嚴格區分原始碼 (.md, .yaml, .mmd, .d2) 與渲染產物 (.png)。
