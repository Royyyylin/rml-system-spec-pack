# STEP 4 — 變更同步規則 (Change Impact Rules)

| Rule ID | Trigger | Must Update | Should Review | Risk if skipped |
| :--- | :--- | :--- | :--- | :--- |
| **CIR-001** | **Requirement text changed** (REQ-*) | AC-*, TC-* | STA-*, SEQ-*, PKT-* | 需求與驗收脫節，導致開發完成後無法通過測試。 |
| **CIR-002** | **New state added** (STA-*) | state_machine.md, sequence_flows.md | architecture.md, REQ-* | 狀態機邏輯不完整，導致系統進入未定義狀態 (Undefined State)。 |
| **CIR-003** | **State transition changed** | state_machine.md, sequence_flows.md | AC-*, TC-* | 通訊時序與狀態邏輯不符，導致 App 與 GW 狀態不一致。 |
| **CIR-004** | **Sequence timeout changed** | sequence_flows.md, state_machine.md | AC-*, TC-* | 測試案例的逾時判定標準錯誤，導致誤報 (False Positive)。 |
| **CIR-005** | **Packet field added/removed** (PKT-*) | packet_contract.md, architecture.md | REQ-*, TC-* | 韌體與 App 解析封包位移錯誤，導致資料顯示亂碼或系統崩潰。 |
| **CIR-006** | **Role / scope changed** (RML-*) | requirements.md, architecture.md | AC-*, TC-* | 權限控制失效，非授權使用者可能執行敏感操作。 |
| **CIR-007** | **Acceptance changed** (AC-*) | test_cases.md | REQ-* | 測試案例無法反映最新的驗收標準，導致品質把關失效。 |
| **CIR-008** | **Architecture module added/removed** | architecture.md, requirements.md | trace_map.yaml | 系統職責劃分不明，導致開發時模組間產生循環依賴。 |
| **CIR-009** | **Function deleted** | trace_map.yaml, all related docs | - | 殘留的過時需求與測試案例會干擾後續 AI 的維護與生成。 |
