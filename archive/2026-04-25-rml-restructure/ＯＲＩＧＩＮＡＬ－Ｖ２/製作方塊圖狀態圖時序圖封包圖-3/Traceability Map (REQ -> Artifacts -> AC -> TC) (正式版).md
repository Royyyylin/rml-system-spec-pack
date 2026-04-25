=== FILE: trace/trace_map.yaml ===
# Traceability Map (REQ -> Artifacts -> AC -> TC) (正式版)

requirement_to_artifacts:
  REQ-001: [BLK-001, PKT-001]
  REQ-002: [STA-001, SEQ-001]
  REQ-003: [STA-003, BLK-001]
  REQ-004: [PKT-002, SEQ-002]
  REQ-005: [STA-001, SEQ-003]
  REQ-006: [BLK-003]

requirement_to_acceptance:
  REQ-001: [AC-001]
  REQ-002: [AC-002]
  REQ-003: [AC-003]
  REQ-004: [AC-004]
  REQ-005: [AC-005]
  REQ-006: [TODO: AC-006]

requirement_to_tests:
  REQ-001: [TC-001, TC-003]
  REQ-002: [TC-002]
  REQ-003: [TODO: TC-006]
  REQ-004: [TC-004]
  REQ-005: [TC-005]

artifact_to_requirements:
  BLK-001: [REQ-001, REQ-003]
  STA-001: [REQ-002, REQ-005]
  PKT-001: [REQ-001]
  PKT-002: [REQ-004]

acceptance_to_tests:
  AC-001: [TC-001, TC-003]
  AC-002: [TC-002]
  AC-004: [TC-004]
  AC-005: [TC-005]

state_to_sequences:
  STA-001: [SEQ-001, SEQ-003]
  STA-003: [SEQ-001, SEQ-002]

packet_to_sequences:
  PKT-001: [SEQ-001, SEQ-003]
  PKT-002: [SEQ-002]

owners:
  RML: PM
  REQ: PM/Firmware
  BLK: Architect
  STA: Firmware
  SEQ: Firmware/App
  PKT: Firmware/App
  AC: QA/PM
  TC: QA

source_of_truth:
  - trace/source_of_truth.md

sync_rules:
  - trace/change_rules.md

evidence_requirements:
  TC-001: [App Log, Screenshot]
  TC-002: [App Log, GW Log]
  TC-004: [App Log, BLE Trace]
  TC-005: [App Log, Device Uptime Log]

---

=== FILE: trace/change_rules.md ===
# 變更同步規則 (Change Impact Rules)

| Rule ID | Trigger | Must Update | Should Review | Risk if skipped |
| :--- | :--- | :--- | :--- | :--- |
| **CIR-001** | **Requirement text changed** (REQ-*) | AC-*, TC-* | STA-*, SEQ-*, PKT-* | 需求與驗收脫節，導致開發完成後無法通過測試。 |
| **CIR-002** | **New state added** (STA-*) | state_machine.md, sequence_flows.md | architecture.md, REQ-* | 狀態機邏輯不完整，導致系統進入未定義狀態。 |
| **CIR-003** | **State transition changed** | state_machine.md, sequence_flows.md | AC-*, TC-* | 通訊時序與狀態邏輯不符，導致 App 與 GW 狀態不一致。 |
| **CIR-004** | **Sequence timeout changed** | sequence_flows.md, state_machine.md | AC-*, TC-* | 測試案例的逾時判定標準錯誤，導致誤報。 |
| **CIR-005** | **Packet field added/removed** (PKT-*) | packet_contract.md, architecture.md | REQ-*, TC-* | 韌體與 App 解析封包位移錯誤，導致資料顯示亂碼。 |
| **CIR-006** | **Role / scope changed** (RML-*) | requirements.md, architecture.md | AC-*, TC-* | 權限控制失效，非授權使用者可能執行敏感操作。 |
| **CIR-007** | **Acceptance changed** (AC-*) | test_cases.md | REQ-* | 測試案例無法反映最新的驗收標準，導致品質把關失效。 |

---

=== FILE: trace/source_of_truth.md ===
# 單一真相來源 (Source of Truth)

## 唯一真相來源清單
- **需求層**: `docs/rml_lite.md`, `docs/requirements.md` (Markdown)。
- **架構層**: `docs/architecture.md` (Markdown)。
- **邏輯層**: `docs/state_machine.md`, `docs/sequence_flows.md` (Markdown + Mermaid/D2 原始碼)。
- **封包層**: `docs/packet_contract.md` (Markdown)。
- **驗收層**: `docs/acceptance_criteria.md`, `docs/test_cases.md` (Markdown)。
- **追蹤層**: `trace/trace_map.yaml` (YAML)。

## 渲染產物 (Render Artifacts)
- **圖片**: 所有 `.png`, `.jpg`, `.svg` 檔案均為渲染產物。
- **規則**: 禁止手動修改圖片。若圖片與原始碼不一致，以原始碼為準。

## 修改流程順序
1. **修改原始碼**: 編輯對應的 `.md`, `.mmd`, `.d2` 或 `.yaml` 檔案。
2. **重新渲染**: 使用 `manus-render-diagram` 工具重新產生圖片。
3. **更新追蹤**: 若涉及 ID 變更，更新 `trace/trace_map.yaml`。
4. **提交變更**: 將原始碼與渲染產物一併提交至版本控制系統。
