# STEP 2 — 建立完整資訊架構 (Information Architecture)

## 樹狀目錄結構
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

## 文件角色說明表

| Document | Purpose | Owner | Sync Trigger |
| :--- | :--- | :--- | :--- |
| **rml_lite.md** | 定義系統目標、角色與範圍。 | PM / Architect | 商業目標變更、角色權限調整。 |
| **requirements.md** | 將 RML 轉化為可實作的功能需求。 | PM / Firmware | RML 變更、功能新增/刪除。 |
| **architecture.md** | 模組化職責與輸入輸出定義。 | Architect | 模組重構、外部依賴變更。 |
| **state_machine.md** | 狀態轉換與異常處理邏輯。 | Firmware | 業務邏輯變更、錯誤處理策略調整。 |
| **sequence_flows.md** | 跨模組/裝置的通訊時序。 | Firmware / App | 通訊協定變更、效能優化需求。 |
| **packet_contract.md** | 封包位元結構與資料型別。 | Firmware / App | 資料欄位增減、傳輸效率優化。 |
| **acceptance_criteria.md** | 定義功能完成的判定標準。 | QA / PM | 需求變更、法規/安全標準更新。 |
| **test_cases.md** | 具體的測試步驟與預期結果。 | QA | 驗收標準變更、發現邊界漏洞。 |
| **trace_map.yaml** | 維護各層級 ID 的映射關係。 | Cross-functional | 任何 ID 新增、刪除或關聯變更。 |
| **change_rules.md** | 定義變更時的連動更新規則。 | Architect | 流程優化、文件治理策略調整。 |
