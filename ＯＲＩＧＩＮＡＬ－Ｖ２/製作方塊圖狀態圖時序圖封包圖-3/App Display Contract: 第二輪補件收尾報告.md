# App Display Contract: 第二輪補件收尾報告

本報告彙整了「第二輪補件」的所有正式檔案產出，將規格包從「骨架/示例」補齊為「正式可用包」。

## New Files (新增檔案)
- **docs/README.md**: 規格包入口文件，定義角色導讀與修改流程。
- **trace/source_of_truth.md**: 明確定義唯一真相來源與修改順序。
- **tools/trace_lint_spec.md**: 定義自動化檢查腳本的介面規格。
- **tools/changed_only_report.schema.json**: 定義變更報告的 JSON Schema。

## Updated Files (更新檔案)
- **docs/rml_lite.md**: 補齊工業級目標、風險 (RML-RSK-002/003) 與約束。
- **docs/requirements.md**: 擴展至完整功能需求 (REQ-001 ~ REQ-006)。
- **docs/architecture.md**: 補齊模組職責與輸入輸出細節。
- **docs/state_machine.md**: 補齊所有狀態、轉換、逾時與重試邏輯。
- **docs/sequence_flows.md**: 補齊正常路徑、異常路徑與恢復路徑。
- **docs/packet_contract.md**: 補齊 PKT-001 並新增 PKT-002 (Error Packet)。
- **docs/acceptance_criteria.md**: 從示例擴展至完整覆蓋 (AC-001 ~ AC-005)。
- **docs/test_cases.md**: 從示例擴展至完整覆蓋 (TC-001 ~ TC-005)，包含邊界測試。
- **trace/trace_map.yaml**: 從範本補齊為正式可機器讀取版本。
- **trace/change_rules.md**: 補齊變更同步規則。

## Remaining TODOs (待辦事項)
- **AC-006**: 補齊 L3 診斷頁顯示 `device_identity` 的驗收標準。
- **TC-006**: 補齊對應 AC-006 的測試案例。
- **自動化腳本實作**: 根據 `tools/trace_lint_spec.md` 實作 Python 檢查腳本。

## Top 3 Residual Risks (前三大殘留風險)
1. **狀態衝突判定延遲**: 雖然定義了以 GW 為權威來源，但在高延遲環境下，App UI 的短暫不一致仍可能誤導操作員。
2. **重試耗盡後的恢復**: 當進入 `Needs Review` 狀態後，若人工介入不及時，裝置可能長時間處於非預期狀態。
3. **封包位元壓縮極限**: 隨著功能增加，23 Bytes 的 MTU 限制可能導致封包結構過於複雜，增加解析錯誤的風險。
