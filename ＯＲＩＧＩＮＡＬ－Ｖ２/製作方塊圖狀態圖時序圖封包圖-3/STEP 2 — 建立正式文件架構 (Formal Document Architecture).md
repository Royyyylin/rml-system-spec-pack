# STEP 2 — 建立正式文件架構 (Formal Document Architecture)

根據「Manus 規格治理指令」，本規格包採用以下目錄結構：

```text
docs/
  ├── README.md             # 規格包入口導讀與角色指引
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
  ├── change_rules.md       # 變更同步規則 (Impact Rules)
  └── source_of_truth.md    # 單一真相來源定義與修改流程
tools/
  ├── trace_lint_spec.md    # 自動化檢查腳本介面規格
  └── changed_only_report.schema.json # 變更報告 JSON Schema
```

## 文件角色與職責定義

| Document | Purpose | Owner | Sync Trigger |
| :--- | :--- | :--- | :--- |
| **rml_lite.md** | 定義系統目標、角色與範圍。 | PM / Architect | 商業目標變更、角色權限調整。 |
| **requirements.md** | 將 RML 轉化為可實作的功能需求。 | PM / Firmware | RML 變更、功能新增/刪除。 |
| **state_machine.md** | 狀態轉換與異常處理邏輯。 | Firmware | 業務邏輯變更、錯誤處理策略調整。 |
| **packet_contract.md** | 封包位元結構與資料型別。 | Firmware / App | 資料欄位增減、傳輸效率優化。 |
| **acceptance_criteria.md** | 定義功能完成的判定標準。 | QA / PM | 需求變更、法規/安全標準更新。 |
| **trace_map.yaml** | 維護各層級 ID 的映射關係。 | Cross-functional | 任何 ID 新增、刪除或關聯變更。 |
| **source_of_truth.md** | 定義唯一真相來源與修改流程。 | Architect | 治理策略調整、工具鏈變更。 |
