<!--
AI-DIAGRAM: required
primary_message: GW-A heartbeat timeout → CC bridge relay → GW-B 升級為 primary GW 的 HA failover 流程
reader: engineer
template_id: sequence-main-branch
diagram_type: sequenceDiagram
layout: left-to-right
max_nodes: 5
max_groups: 2
keep: GW-A心跳超時、CC bridge偵測、Central決策、GW-B promotion、App更新
avoid: hold-down timer參數、ED reconnect細節、failback流程
-->

# HA Failover 時序圖

**主訊息**：GW-A 心跳超時後，CC bridge 通報 Central，Central 決策並提升 GW-B 為 primary，App 收到更新。

```mermaid
sequenceDiagram
    participant GW_A as GW-A（原 Primary）
    participant CC as CC Bridge
    participant Central
    participant GW_B as GW-B（候補）
    participant App

    GW_A->>CC: 心跳停止（timeout）
    CC->>CC: 偵測 GW-A 心跳超時
    CC->>Central: 上報 GW-A unreachable
    Central->>Central: 評估 failover eligibility<br/>確認 GW-B 可接管
    Central->>GW_B: 通知升級為 Primary GW
    GW_B->>GW_B: 接受 promotion<br/>開始接收 ED 連線
    Central->>Central: 更新 assignment truth<br/>GW-B = active, revision++
    Central-->>App: Push / polling 回傳<br/>assignment 變更通知
    App->>App: UI 更新<br/>顯示新 primary GW + state
```

**說明**：CC bridge 是 HA 架構中的監控中繼節點；Central 保有最終 failover 決策權（`FEA-004-BND-001`）。GW-A 下線後的 ED reconnect 流程見 [`seq-ed-reconnect.md`](seq-ed-reconnect.md)。failback 操作見 [`../flow/flow-failback.md`](../flow/flow-failback.md)。

**Reference**：
- Spec: [`../../feature-assignment-reconciliation.md`](../../feature-assignment-reconciliation.md)
- Architecture: [`../architecture/arch-system-overview.md`](../architecture/arch-system-overview.md)
