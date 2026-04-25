# STEP 5 — 一致性檢查與缺口分析 (Consistency Check & Gap Analysis)

## Consistency Check Summary
- **可追蹤性 (Traceability)**: 已建立從 RML-lite (上游) 到工程圖 (中游) 再到 AC/TC (下游) 的 ID 體系。
- **覆蓋率 (Coverage)**: 示例 REQ-001 與 REQ-002 已完整對應至 BLK, STA, SEQ, PKT, AC 與 TC。
- **同步規則 (Sync Rules)**: 已定義 CIR-001 至 CIR-009，涵蓋主要變更場景。

## Missing Inputs / Gaps
- **RML-RSK (風險處理)**: 目前僅定義了連線逾時，尚未定義「資料衝突 (Conflict)」與「裝置重啟 (Reboot)」的恢復路徑。
- **RML-CST (約束條件)**: 尚未定義 BLE 連線參數（如 Connection Interval）對功耗與延遲的具體影響。
- **AC 測量工具**: 部分 AC (如 AC-001) 需要特定的封包模擬器或 BLE Sniffer 支援，目前尚未定義工具鏈規格。

## Suggested Additions
1. **補強 RML-RSK-002**: 定義當 App 與 GW 狀態不一致時的「權威來源 (Source of Truth)」判定規則。
2. **新增 PKT-002 (Error Packet)**: 定義當 GW 無法執行動作時回傳的錯誤代碼封包。
3. **擴展 TC-003 (Boundary Test)**: 針對 RSSI 臨界值 (-120dBm) 與 Zone 切換邊界進行測試。

## Impacted Artifacts (本次更新影響範圍)
- **New**: `rml_lite.md`, `requirements.md`, `acceptance_criteria.md`, `test_cases.md`, `trace_map.yaml`, `change_rules.md`.
- **Updated**: `architecture.md`, `state_machine.md`, `sequence_flows.md`, `packet_contract.md` (增加 ID 與 Traceability 標註)。

## Top 3 Desync Risks
1. **圖改需求沒改**: 開發者直接修改 `state_diagram.png` 增加狀態，但未更新 `requirements.md` 與 `AC-*`，導致測試漏測。
2. **需求改測試沒改**: PM 修改 `REQ-001` 的顯示頻率，但 `TC-001` 仍沿用舊的判定標準，導致測試誤判 Pass。
3. **封包位移偏移**: 修改 `PKT-001` 欄位順序後，未同步更新 `architecture.md` 的解析邏輯，導致全系統資料錯誤。
