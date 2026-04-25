# Stakeholders

> arc42 §1 — Stakeholders.
> split source: rml-lite.md lines 24-43 (First-Level Actors) + lines 57-63 (Human Operational Roles).
> Authority Boundaries → see [bounded-context-map.md](../01_context-scope/bounded-context-map.md).

## First-Level Actors

| ID | Actor | Responsibility |
| :--- | :--- | :--- |
| `RML-ACT-001` | Operator | 執行日常操作、查看 fleet / device 狀態、處理低風險操作流程。 |
| `RML-ACT-002` | Engineer | 執行工程診斷、進階命令、衝突與例外排查，承接較高權限維護流程。 |
| `RML-ACT-003` | Gateway / Edge Nodes | 產生 runtime truth，執行 QoS、uplink、HA、local coordination 與裝置側行為。 |
| `RML-ACT-004` | Central System | 維護 canonical identity、assignment、metadata、auth、audit、sync 與 global truth。 |
| `RML-ACT-005` | Conductor / AI Orchestration Layer | 管理 planning、dispatch、handoff、queue、evidence 與 cross-repo governance，不直接擔任 runtime control authority。 |

### Firmware Runtime Roles

以下記錄 `RML-ACT-003` 涵蓋的既有韌體角色定義：

| Role | Command Path | Responsibility |
| :--- | :--- | :--- |
| Gateway (GW) | Firmware-side path | runtime QoS、local failover、uplink、End Device coordination |
| End Device (ED) | Firmware-side path | runtime measurement、device-side behavior |
| CC bridge | Central-side path | BLE-to-Central bridge/relay — 不擁有 authority ownership |

> App 連到 CC bridge 時走 Central-side path，連到 Gateway / End Device 時走 Firmware-side path。

## Human Operational Roles

| ID | Role | Responsibility |
| :--- | :--- | :--- |
| `RML-ROL-001` | Operator | 查看 fleet / device 基本狀態，不做高風險操作。 |
| `RML-ROL-002` | Installer / Maintainer | 執行一般維護操作、查看 detail、處理現場更換；屬於 human operational role，不改變第一級 actor 分層。 |
| `RML-ROL-003` | Engineer | 使用工程診斷、進階命令、衝突與例外排查。 |
