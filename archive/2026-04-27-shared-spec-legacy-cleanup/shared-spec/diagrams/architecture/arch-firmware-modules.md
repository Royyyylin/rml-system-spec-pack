<!--
AI-DIAGRAM: required
primary_message: Firmware 模組分層：ble_port / qos_service / role_* / nvs / ha / uplink / cmd_v2_dispatch
reader: engineer
template_id: map-source-surface
diagram_type: flowchart
layout: top-to-bottom
max_nodes: 8
max_groups: 4
keep: 七個主要模組、模組間依賴方向、cmd_v2_dispatch作為指令入口
avoid: 函數級別細節、BLE GATT UUID、NCS/Zephyr API
-->

# Firmware 模組架構圖

**主訊息**：Firmware 由七個主要模組組成，`cmd_v2_dispatch` 是指令入口，`qos_service` 是核心排程邏輯，`nvs` 持久化所有設定。

```mermaid
flowchart TD
    subgraph Transport層
        BLE[ble_port\nBLE 連線管理\nGATT server]
        UPLINK[uplink\n遙測上傳\nSTATUS / METRICS_V2]
    end

    subgraph Command層
        CMD[cmd_v2_dispatch\n指令路由\nbusy guard]
    end

    subgraph Business層
        QOS[qos_service\nQoS Scheduler\ngw_qos_calc_interval]
        ROLE[role_*\nED / GW / CC\n角色行為]
        HA[ha\nHA heartbeat\nfailover detection]
    end

    subgraph Persistence層
        NVS[nvs\nNVS 讀寫\nrole / tune config / network_id]
    end

    BLE -->|收到 CMD_V2 Write| CMD
    CMD -->|dispatch opcode 0x07| QOS
    CMD -->|dispatch role change| ROLE
    QOS -->|寫入 step table| NVS
    ROLE -->|寫入 role| NVS
    HA -->|心跳狀態| UPLINK
    UPLINK -->|BLE Notify| BLE
    QOS -->|connection interval 計算| BLE
```

**說明**：`cmd_v2_dispatch` 作為 command plane 的單一入口（Single Responsibility），解耦了 BLE transport 和業務邏輯。`nvs` 是所有持久化狀態的 SSOT，模組不直接互相讀取設定。

**Reference**：
- Wire SSOT: `ble_api.yaml` (owner: `ble_qos_demo_V1.2m`)
- State: [`../state/state-role-machine.md`](../state/state-role-machine.md)
- Dispatcher state: [`../state/state-cmd-v2-dispatcher.md`](../state/state-cmd-v2-dispatcher.md)
