<!--
AI-DIAGRAM: required
primary_message: BLE 連線從 scan 到 subscribe 的生命週期主流程
reader: newcomer
template_id: flow-linear-gate
diagram_type: flowchart
layout: top-to-bottom
max_nodes: 8
max_groups: 2
keep: scan→connect→discover→subscribe→idle 主流程、斷線觸發點
avoid: retry backoff參數、RSSI過濾細節、多 GW 並行連線
-->

# BLE 連線生命週期流程圖

**主訊息**：App 從掃描開始，連上 GW/ED 後完成服務探索與 notify 訂閱，進入 idle 等待事件或斷線。

```mermaid
flowchart TD
    A[App\n開始 BLE Scan] -->|偵測到 ADV packet\n符合 network_id| B[發起 connect]
    B -->|GATT connect 成功| C[Discover Services\n找 QoS Service UUID]
    C -->|服務存在| D[Discover Characteristics\nCAPS_V2, STATUS, METRICS_V2, CMD_V2, CMD_RESULT]
    D -->|Enable Notifications\nCMD_RESULT + STATUS + METRICS_V2| E[Subscribe 完成\n連線就緒]
    E --> F[Idle\n等待 notify / 使用者操作]
    F -->|收到 STATUS notify| F
    F -->|使用者觸發指令| G[寫入 CMD_V2\n等待 CMD_RESULT]
    G --> F
    F -->|Link Loss / 使用者斷線\n或 reconnect 條件| H[Disconnect]
    H -->|需要重連| A
    H -->|不需要重連| I[End]
    B -->|connect 失敗 / timeout| J[retry backoff\n最多 N 次]
    J -->|仍失敗| I
    J -->|重試| B
```

**說明**：此圖呈現 App 連線的主線生命週期。reconnect 路徑（ED 端）詳見 [`seq-ed-reconnect.md`](../sequence/seq-ed-reconnect.md)；服務快取失效（GW 重啟）見 [`seq-cache-invalidation-3tier.md`](../sequence/seq-cache-invalidation-3tier.md)。

**Reference**：
- Requirement: [`../../requirements.md`](../../requirements.md) `REQ-006`
- Wire SSOT: `ble_api.yaml` (owner: `ble_qos_demo_V1.2m`)
