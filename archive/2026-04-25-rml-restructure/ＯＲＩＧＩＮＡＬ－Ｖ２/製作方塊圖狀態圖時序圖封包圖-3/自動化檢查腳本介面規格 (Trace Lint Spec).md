=== FILE: tools/trace_lint_spec.md ===
# 自動化檢查腳本介面規格 (Trace Lint Spec)

## 腳本目標
本腳本旨在自動化檢查 `docs/` 與 `trace/` 目錄下文件的一致性，確保需求、圖表、驗收標準與測試案例之間沒有斷層。

## 檢查項目 (Checklist)
- **需求覆蓋率**: 檢查 `requirements.md` 中的每個 REQ-ID 是否在 `trace_map.yaml` 中至少對應一個 AC-ID 與一個 TC-ID。
- **狀態機一致性**: 檢查 `state_machine.md` 中的每個 STA-ID 是否在 `sequence_flows.md` 中至少被引用一次。
- **封包合約一致性**: 檢查 `packet_contract.md` 中的每個 PKT-ID 是否在 `sequence_flows.md` 中至少被引用一次。
- **驗收與測試對應**: 檢查 `acceptance_criteria.md` 中的每個 AC-ID 是否在 `test_cases.md` 中至少對應一個 TC-ID。
- **ID 唯一性**: 檢查所有文件中是否存在重複的 ID (RML-*, REQ-*, BLK-*, STA-*, SEQ-*, PKT-*, AC-*, TC-*)。
- **證據需求檢查**: 檢查 `trace_map.yaml` 中的 `evidence_requirements` 是否完整覆蓋所有 TC-ID。

## 輸出格式
- **Pass**: 輸出 `Traceability Check Passed.`。
- **Fail**: 輸出 `Traceability Check Failed.` 並列出具體的錯誤位置與建議修復動作。

---

=== FILE: tools/changed_only_report.schema.json ===
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Changed Only Report Schema",
  "description": "Schema for reporting impacts of changes in the App Display Contract specification package.",
  "type": "object",
  "properties": {
    "changed_files": {
      "type": "array",
      "items": { "type": "string" },
      "description": "List of files modified in the current change set."
    },
    "changed_requirements": {
      "type": "array",
      "items": { "type": "string" },
      "description": "List of REQ-IDs affected by the change."
    },
    "changed_states": {
      "type": "array",
      "items": { "type": "string" },
      "description": "List of STA-IDs affected by the change."
    },
    "changed_packets": {
      "type": "array",
      "items": { "type": "string" },
      "description": "List of PKT-IDs affected by the change."
    },
    "impacted_artifacts": {
      "type": "array",
      "items": { "type": "string" },
      "description": "List of downstream artifacts (diagrams, docs) that must be updated."
    },
    "missing_updates": {
      "type": "array",
      "items": { "type": "string" },
      "description": "List of required updates that have not yet been performed."
    },
    "evidence_gaps": {
      "type": "array",
      "items": { "type": "string" },
      "description": "List of test cases lacking required evidence (logs, screenshots)."
    },
    "desync_risks": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Top risks identified due to potential desynchronization between documents."
    }
  },
  "required": ["changed_files", "impacted_artifacts", "missing_updates"],
  "additionalProperties": false
}
