# Step 1: 檔案更新清單 (File Update List)

## 更新既有檔案 (Updated Files)
- **docs/rml_lite.md**: 補齊工業級目標、風險 (RML-RSK-002/003) 與約束。
- **docs/requirements.md**: 擴展至完整功能需求，對應 STA/SEQ/PKT。
- **docs/architecture.md**: 補齊模組職責與輸入輸出細節。
- **docs/state_machine.md**: 補齊所有狀態、轉換、逾時與重試邏輯。
- **docs/sequence_flows.md**: 補齊正常路徑、異常路徑與恢復路徑。
- **docs/packet_contract.md**: 補齊 PKT-001 並新增 PKT-002 (Error Packet)。
- **docs/acceptance_criteria.md**: 從示例擴展至完整覆蓋 (AC-001 ~ AC-010+)。
- **docs/test_cases.md**: 從示例擴展至完整覆蓋 (TC-001 ~ TC-010+)，包含邊界測試。
- **trace/trace_map.yaml**: 從範本補齊為正式可機器讀取版本。
- **trace/change_rules.md**: 補齊變更同步規則。

## 新增檔案 (New Files)
- **docs/README.md**: 規格包入口文件，定義角色導讀與修改流程。
- **trace/source_of_truth.md**: 明確定義唯一真相來源與修改順序。
- **tools/trace_lint_spec.md**: 定義自動化檢查腳本的介面規格。
- **tools/changed_only_report.schema.json**: 定義變更報告的 JSON Schema。
