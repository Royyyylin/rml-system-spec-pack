=== FILE: docs/rml_lite.md ===
# RML-lite: App Display Contract 上游需求 (正式版)

## System Goals
- **RML-OBJ-001**: 提供高可靠性的工業級裝置監控介面，取代傳統 RS485 有線傳輸，適用於礦坑、油井等極端環境。
- **RML-OBJ-002**: 確保 App、GW 與 ED 之間的狀態顯示具備強一致性，避免因通訊延遲導致的誤判。
- **RML-OBJ-003**: 最小化現場維護成本，透過精確的 L3 診斷資訊快速定位硬體故障。

## Stakeholders / Roles
- **RML-ROL-001 (Installer)**: 負責現場安裝、更換設備與基本維護。
- **RML-ROL-002 (Engineer)**: 負責底層診斷、權限解鎖與系統除錯。
- **RML-ROL-003 (Operator)**: 負責日常巡檢與狀態監控。

## Scope / Out of Scope
- **RML-SCP-001 (In-Scope)**: BLE 裝置列表、詳情顯示、狀態同步、維護動作執行、GATT 封包解析。
- **RML-SCP-002 (Out-of-Scope)**: 雲端歷史數據分析、韌體 OTA 更新流程、多 GW 漫遊切換。

## Feature Tree
- **RML-FEA-001**: 裝置狀態即時監控 (L1/L2)。
- **RML-FEA-002**: 裝置生命週期管理 (Maintenance/Retire/Replace)。
- **RML-FEA-003**: 工程診斷與 Mapping Trace (L3)。

## Constraints
- **RML-CST-001**: BLE 通訊延遲必須低於 500ms，以符合工業即時性要求。
- **RML-CST-002**: 封包大小受限於 MTU 23 Bytes，需進行高效位元壓縮。
- **RML-CST-003**: 必須支援在 -40°C 至 +85°C 的工業環境下穩定運作。

## Risks & Recovery
- **RML-RSK-001**: 狀態同步衝突。當 App 與 GW 同時修改狀態時，以 GW 為權威來源。
- **RML-RSK-002**: **狀態不一致判定規則**。若 App 收到狀態與本地預期不符，應發起一次強制同步 (Force Sync)。
- **RML-RSK-003**: **裝置重啟恢復路徑**。裝置重啟後應進入 `active` 狀態並主動發送一次 STATUS 封包。

---

=== FILE: docs/requirements.md ===
# 功能需求 (Functional Requirements)

| ID | Description | Rationale | Priority | Source | Related Artifacts | AC Link | TC Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-001** | App 應能顯示 ED 的即時 RSSI 與 Zone 資訊。 | 讓 Installer 判斷訊號品質。 | High | RML-FEA-001 | BLK-001, PKT-001 | AC-001 | TC-001 |
| **REQ-002** | 進入 Maintenance 狀態前需確認目前為 Active。 | 防止非法狀態轉移。 | Medium | RML-FEA-002 | STA-001, SEQ-001 | AC-002 | TC-002 |
| **REQ-003** | 當 `sync_state == needs_review` 時，應鎖定 Replace 動作。 | 確保資料一致性後才允許更換硬體。 | High | RML-FEA-002 | STA-003 | AC-003 | TC-003 |
| **REQ-004** | 系統應能處理 GW 回傳的 Error Packet 並顯示錯誤原因。 | 提供具體的故障排除資訊。 | Medium | RML-FEA-003 | PKT-002, SEQ-002 | AC-004 | TC-004 |
| **REQ-005** | 裝置重啟後，App 應能自動恢復連線並同步最新狀態。 | 確保系統在斷電重啟後的可用性。 | High | RML-RSK-003 | STA-001, SEQ-003 | AC-005 | TC-005 |
| **REQ-006** | L3 診斷頁應顯示完整的 `device_identity` (MAC 地址)。 | 用於精確追蹤硬體身分。 | Low | RML-FEA-003 | BLK-003 | AC-006 | TC-006 |
