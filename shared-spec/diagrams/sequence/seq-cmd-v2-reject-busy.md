<!--
AI-DIAGRAM: required
primary_message: 當第一個 CMD_V2 in-flight 時，第二個 CMD_V2 被 GW 以 0xFD BUSY 拒絕
reader: engineer
template_id: sequence-main-branch
diagram_type: sequenceDiagram
layout: left-to-right
max_nodes: 4
max_groups: 2
keep: 第一個CMD in-flight、第二個CMD被reject 0xFD、dispatcher busy guard
avoid: TUNE-VAL細節、NVS寫入、成功路徑
-->

# CMD_V2 Reject — Busy Guard 時序圖

**主訊息**：GW dispatcher 同時只處理一個 CMD_V2；第二個請求在第一個 in-flight 期間會收到 0xFD BUSY reject。

```mermaid
sequenceDiagram
    participant App
    participant GW as GW Firmware

    App->>GW: BLE Write CMD_V2 #1<br/>opcode=0x07（第一個請求）
    Note over GW: dispatcher state = dispatching<br/>response_pending

    App->>GW: BLE Write CMD_V2 #2<br/>opcode=0x07（第二個請求，in-flight）
    GW-->>App: BLE Notify CMD_RESULT #2<br/>opcode=0x07, status=0xFD BUSY

    Note over GW: 繼續處理第一個請求
    GW->>GW: handler 執行 + NVS 寫入
    GW-->>App: BLE Notify CMD_RESULT #1<br/>opcode=0x07, status=0x00 SUCCESS

    App->>App: 檢查 #2 = BUSY<br/>等第一個完成後可重送 #2
```

**說明**：0xFD BUSY 是 dispatcher 層的 guard，非 handler 層的業務邏輯 reject。App 在收到 BUSY 後應等待第一個 CMD_RESULT 再重送，不應立即放棄。dispatcher 狀態機見 [`../state/state-cmd-v2-dispatcher.md`](../state/state-cmd-v2-dispatcher.md)。

**Reference**：
- Spec: [`../../feature-gw-qos-scheduler-tuning.md`](../../feature-gw-qos-scheduler-tuning.md) CMD_V2 Timeout Contract
- State: [`../state/state-cmd-v2-dispatcher.md`](../state/state-cmd-v2-dispatcher.md)
