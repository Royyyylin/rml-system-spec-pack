# STEP 3 — 文件骨架與示例內容 (Part 1)

## 1. docs/rml_lite.md
```markdown
# RML-lite: App Display Contract 上游需求

## System Goals
- **RML-OBJ-001**: 提供高可靠性的工業級裝置監控介面，取代傳統 RS485 有線傳輸。
- **RML-OBJ-002**: 確保 App、GW 與 ED 之間的狀態顯示具備強一致性。

## Stakeholders / Roles
- **RML-ROL-001 (Installer)**: 負責現場安裝、更換設備與基本維護。
- **RML-ROL-002 (Engineer)**: 負責底層診斷、權限解鎖與系統除錯。

## Scope / Out of Scope
- **RML-SCP-001 (In-Scope)**: BLE 裝置列表、詳情顯示、狀態同步與基本控制動作。
- **RML-SCP-002 (Out-of-Scope)**: 雲端歷史數據分析、韌體 OTA 更新流程。

## Feature Tree
- **RML-FEA-001**: 裝置狀態即時監控 (L1/L2)。
- **RML-FEA-002**: 裝置生命週期管理 (Maintenance/Retire)。

## Constraints
- **RML-CST-001**: BLE 通訊延遲必須低於 500ms。
- **RML-CST-002**: 封包大小受限於 MTU 23 Bytes。

## Risks
- **RML-RSK-001**: 狀態同步衝突（App 與 GW 同時修改狀態）。
```

## 2. docs/requirements.md
```markdown
# 功能需求 (Functional Requirements)

| ID | Description | Rationale | Priority | Source | Related Artifacts | AC Link | TC Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-001** | App 應能顯示 ED 的即時 RSSI 與 Zone 資訊。 | 讓 Installer 判斷訊號品質。 | High | RML-FEA-001 | BLK-001, PKT-001 | AC-001 | TC-001 |
| **REQ-002** | 進入 Maintenance 狀態前需確認目前為 Active。 | 防止非法狀態轉移。 | Medium | RML-FEA-002 | STA-001, SEQ-001 | AC-002 | TC-002 |
```

## 3. docs/architecture.md
```markdown
# 系統架構與模組 (Architecture)

## 模組列表與責任
- **BLK-001 (App-UI)**: 負責 L1/L2/L3 介面渲染與使用者輸入。
- **BLK-002 (GW-Roster)**: 負責維護 ED 清單與連線狀態。
- **BLK-003 (Comm-Manager)**: 負責 BLE GATT 讀寫與封包解析。

## 輸入/輸出
- **Input**: BLE GATT Notification (STATUS char).
- **Output**: BLE GATT Write (Action command).

## 與方塊圖對應
- 參見 `block_diagram.png`，BLK-001 對應 App 節點，BLK-002 對應 GW 節點。
```
