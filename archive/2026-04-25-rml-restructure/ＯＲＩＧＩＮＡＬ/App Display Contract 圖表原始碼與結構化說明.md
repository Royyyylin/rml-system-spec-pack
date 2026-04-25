# App Display Contract 圖表原始碼與結構化說明

本文件彙整了根據 `2026-03-15-app-display-contract.md` 製作的四種技術圖表原始碼，包含 **Mermaid**、**PlantUML** 及 **結構化文字圖**。

---

## 1. 方塊圖 (Block Diagram) — 三層架構與資料來源

### Mermaid 原始碼
```mermaid
graph LR
    subgraph App [Phone App]
        L1[L1: Device List]
        L2[L2: Device Detail]
        L3[L3: Engineer Debug]
        L1 -->|點擊卡片| L2
        L2 -->|長按/解鎖| L3
    end

    subgraph GW [Gateway]
        Roster[(gw_ed_roster)]
        State[(gw_point_state)]
        QoS[(gw_qos)]
        Ack[(gw_ack)]
    end

    Roster -.->|point_name, connectivity| L1
    State -.->|operational_state| L1
    QoS -.->|Zone, RSSI, PHY, TX Power| L2
    Ack -.->|sync_state| L2
    Roster -.->|point_uid, logical_slot, conn_slot| L3
    State -.->|raw enum values| L3
```

### 結構化文字圖
```text
[ Phone App ]                      [ Gateway ]
+-----------------------+          +-----------------------+
| L1: Device List       |<---------| gw_ed_roster (Name)   |
| (User/Patrol)         |          | gw_point_state (State)|
+-----------+-----------+          +-----------------------+
            | Click
            v
+-----------+-----------+          +-----------------------+
| L2: Device Detail     |<---------| gw_qos (RSSI/Zone)    |
| (Installer/Maint)     |          | gw_ack (Sync State)   |
+-----------+-----------+          +-----------------------+
            | Long Press
            v
+-----------+-----------+          +-----------------------+
| L3: Engineer Debug    |<---------| Full Roster Info      |
| (Dev/Debug)           |          | Raw Enum Values       |
+-----------------------+          +-----------------------+
```

---

## 2. 狀態圖 (State Diagram) — 運作與同步狀態

### Mermaid 原始碼
```mermaid
stateDiagram-v2
    state "Operational States" as OS {
        [*] --> active
        active --> maintenance: Enter Maintenance (Installer)
        maintenance --> active: Exit Maintenance (Installer)
        active --> disabled: Disable (Engineer)
        maintenance --> disabled: Disable (Engineer)
        disabled --> active: Re-enable (Engineer)
        active --> retire_requested: Request Retire (Engineer)
        maintenance --> retire_requested: Request Retire (Engineer)
        disabled --> retire_requested: Request Retire (Engineer)
        retire_requested --> disabled: Cancel Retire (Engineer)
    }

    state "Sync States" as SS {
        [*] --> pending_sync
        pending_sync --> synced: Success
        pending_sync --> sync_failed: Failure
        sync_failed --> pending_sync: Retry
        synced --> needs_review: Conflict
        needs_review --> synced: Resolved
        needs_review --> rejected: Rejected
    }
```

### PlantUML 原始碼
```plantuml
@startuml
state "Operational States" as OS {
  [*] --> active
  active --> maintenance : Enter Maintenance
  maintenance --> active : Exit Maintenance
  active --> disabled : Disable
  disabled --> active : Re-enable
  active --> retire_requested : Request Retire
  retire_requested --> disabled : Cancel Retire
}

state "Sync States" as SS {
  [*] --> pending_sync
  pending_sync --> synced : Success
  pending_sync --> sync_failed : Failure
  sync_failed --> pending_sync : Retry
  synced --> needs_review : Conflict
  needs_review --> synced : Resolved
  needs_review --> rejected : Rejected
}
@enduml
```

---

## 3. 時序圖 (Sequence Diagram) — App 與 GW 互動

### Mermaid 原始碼
```mermaid
sequenceDiagram
    participant App as Phone App
    participant GW as Gateway (GW)
    participant ED as End Device (ED)

    Note over App, GW: Phase 1: Monitoring
    App->>GW: Read STATUS (0x2A1D)
    GW-->>App: RSSI, Zone, PHY, TX Power

    Note over App, GW: Phase 2: Inventory Sync
    App->>GW: Request Roster (CMD)
    GW-->>App: point_name, operational_state, sync_state

    Note over App, GW: Action Execution
    App->>GW: Action: Enter Maintenance
    GW->>GW: Update local state
    GW-->>App: ACK (sync_state = pending_sync)

    Note over GW, ED: Backend Sync
    GW->>ED: Update Config
    ED-->>GW: Confirm
    GW->>GW: Update sync_state = synced
```

---

## 4. 封包圖 (Packet Diagram) — GATT 資料結構

### 結構化文字圖 (GATT STATUS 0x2A1D)
```text
Byte Offset | Field Name | Description
------------|------------|---------------------------------------
0           | Header     | Control/Type Header (1 Byte)
1           | Zone       | 0:NEAR, 1:MID, 2:FAR, 3:EDGE (1 Byte)
2           | RSSI       | Signed Integer dBm (1 Byte)
3           | PHY        | 0:1M, 1:2M, 2:Coded (1 Byte)
4           | TX Power   | -8 to +8 dBm (1 Byte)
5..N        | Reserved   | Future Expansion
```

### PlantUML 原始碼 (Roster Entry Structure)
```plantuml
@startuml
class "Roster Entry (Phase 2)" as Roster {
  + point_uid : uint16
  + logical_slot : uint8
  + operational_state : uint8
  + sync_state : uint8
  + device_identity : byte[6]
}
@enduml
```
