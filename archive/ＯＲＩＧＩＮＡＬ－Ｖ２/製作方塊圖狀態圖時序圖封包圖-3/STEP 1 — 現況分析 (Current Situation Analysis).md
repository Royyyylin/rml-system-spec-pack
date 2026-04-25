# STEP 1 — 現況分析 (Current Situation Analysis)

| Artifact | Purpose | Strength | Missing Upstream | Risk |
| :--- | :--- | :--- | :--- | :--- |
| **Block Diagram** | 定義 App 三層架構與 GW 資料來源的靜態對應關係。 | 清楚界定 L1/L2/L3 職責與資料流向。 | 缺少 RML-ROL (角色權限) 與 RML-SCP (功能範圍) 的具體定義。 | 若角色權限變更（如 Installer 權限下放），方塊圖無法體現存取限制。 |
| **State Diagram** | 描述 `operational_state` 與 `sync_state` 的動態轉換。 | 涵蓋了主要的狀態轉移邏輯與同步狀態。 | 缺少 RML-CST (約束) 與 RML-RSK (風險處理)，如斷線重連的重試次數限制。 | 狀態機可能在異常邊界（Timeout/Retry）定義不明，導致韌體實作不一致。 |
| **Sequence Diagram** | 描述 App 與 GW 之間的通訊時序與 Phase 1/2 演進。 | 視覺化了通訊流程與同步機制。 | 缺少 RML-FLW (業務流程) 與 RML-FEA (功能分解) 的上游對應。 | 若通訊協定變更（如從 Poll 改為 Notify），時序圖與需求可能脫節。 |
| **Packet Diagram** | 定義 GATT STATUS 與 Roster Entry 的位元結構。 | 提供實作層級的精確資料格式。 | 缺少 RML-OBJ (系統目標) 與 RML-CST (頻寬/功耗約束)。 | 封包設計若未考慮功耗約束，可能導致高頻更新造成裝置耗電過快。 |

### 哪些資訊最容易失同步？
1. **狀態與時序 (STA vs SEQ)**：當狀態機增加一個 `retrying` 狀態，時序圖若未同步更新 Retry 流程，會導致實作歧義。
2. **需求與驗收 (REQ vs AC)**：需求描述若過於籠統（如「顯示 RSSI」），而驗收標準未定義更新頻率，測試將無法判定 Pass/Fail。
3. **封包與狀態 (PKT vs STA)**：封包欄位長度若不足以承載新增的狀態 Enum，會導致資料溢位或解析錯誤。
