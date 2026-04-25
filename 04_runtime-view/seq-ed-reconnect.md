<!--
AI-DIAGRAM: required
primary_message: ED 斷線後重新掃描並根據 network_id 自動 reconnect 到正確 GW
reader: newcomer
template_id: sequence-main-branch
diagram_type: sequenceDiagram
layout: left-to-right
max_nodes: 4
max_groups: 2
keep: ED斷線、scan、network_id匹配、reconnect、backoff
avoid: GATT discover細節、CMD_V2流程、HA promotion
-->

# ED Reconnect 時序圖

**主訊息**：End Device 斷線後，透過 scan → network_id 匹配 → reconnect 自動恢復連線，backoff 避免風暴。

```mermaid
sequenceDiagram
    participant ED as End Device
    participant GW as GW（目標）
    participant Central

    Note over ED: 連線斷失（Link Loss / GW reboot）

    ED->>ED: 進入 scanning 狀態<br/>開始掃描廣播
    ED->>GW: 偵測到 ADV packet<br/>比對 network_id
    alt network_id 不符
        ED->>ED: 略過，繼續 scan
    else network_id 符合
        ED->>GW: 發起 BLE Connect
        GW-->>ED: Connect established
        ED->>GW: 恢復 QoS session
        GW->>Central: 上報 ED reconnect<br/>更新 runtime attach
        Central-->>GW: ack
        Note over ED,GW: 連線恢復正常
    end

    alt 多次 scan 失敗
        ED->>ED: backoff delay<br/>避免掃描風暴
        ED->>ED: 重新掃描
    end
```

**說明**：ED 端以 `network_id` 為匹配 key，不綁定 GW MAC，確保 failover 後仍能自動連到新 primary GW。backoff 策略避免多台 ED 同時重連造成 radio collision。

**Reference**：
- Flow: [`../flow/flow-ble-conn-lifecycle.md`](../flow/flow-ble-conn-lifecycle.md)
- State: [`../state/state-ed-conn.md`](../state/state-ed-conn.md)
- HA context: [`seq-ha-failover.md`](seq-ha-failover.md)
