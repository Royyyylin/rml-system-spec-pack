<!--
AI-DIAGRAM: required
primary_message: Central 四層架構：presentation / application / domain / infrastructure，職責分層清晰
reader: engineer
template_id: map-source-surface
diagram_type: flowchart
layout: top-to-bottom
max_nodes: 8
max_groups: 4
keep: 四層名稱與職責、FastAPI在presentation層、domain擁有assignment truth、DB/sync在infrastructure
avoid: API endpoint list、資料庫 schema細節、deployment環境
-->

# Central 分層架構圖

**主訊息**：Central（`central-device-metadata`）採四層架構；domain 層擁有 assignment truth，infrastructure 層負責持久化與同步。

```mermaid
flowchart TD
    subgraph Presentation層
        API[FastAPI Routes\nREST endpoints\n/gateways / /devices / /sched-tune]
        AUTH[Auth / RBAC\nengineering mode 解鎖]
    end

    subgraph Application層
        SVC[Services\nuse-case orchestration\naudit log / revision 管理]
    end

    subgraph Domain層
        ASN[Assignment\nassignment truth\nactive_gateway_id / state / version]
        TUNE[Sched Tune\npreset catalog\nTUNE-VAL validation]
        HA_SVC[HA Service\nfailover / failback\neligibility 判斷]
    end

    subgraph Infrastructure層
        DB[Database\nSQLAlchemy / SQLite/PG\n持久化]
        SYNC[BLE Sync\nCMD_V2 送出 / CMD_RESULT 接收]
    end

    API --> SVC
    AUTH --> SVC
    SVC --> ASN
    SVC --> TUNE
    SVC --> HA_SVC
    ASN --> DB
    TUNE --> DB
    HA_SVC --> DB
    TUNE --> SYNC
    SYNC -->|CMD_RESULT 回傳| SVC
```

**說明**：Presentation 層不直接操作 domain 物件；所有業務邏輯集中在 Domain 層，確保 assignment truth 不被繞過。`TUNE` domain 物件擁有 TUNE-VAL validation 邏輯，與 API route 解耦。

**Reference**：
- Repo: `central-device-metadata/`
- Assignment spec: [`../../feature-assignment-reconciliation.md`](../../feature-assignment-reconciliation.md)
- Sched Tune spec: [`../../feature-gw-qos-scheduler-tuning.md`](../../feature-gw-qos-scheduler-tuning.md)
