# RML-lite

> 細部 capability ownership 與 cross-repo handoff boundary 見 [capability-ownership.md](capability-ownership.md)；stage 模型見 [baseline-target-migration.md](baseline-target-migration.md)；diagram authoring contract 見 [diagram-authoring-rules.md](diagram-authoring-rules.md) 與 [diagram-templates.md](diagram-templates.md)。

## System Intent

| ID | Statement |
| :--- | :--- |
| `RML-INT-001` | BLE QoS Demo 對外可作為 demo 展示，但其內部工程定位必須是可持續演進、可驗證、可交接的 reference system。 |
| `RML-INT-002` | 本系統的目標不是一次性展示品，而是驗證 App、Firmware、Central 之間的協作模型、能力邊界與產品化路徑。 |
| `RML-INT-003` | cross-repo 控制面、驗收、handoff、queue 與 evidence 必須可被後續 AI / automation layer 穩定接續。 |

## System Goals

| ID | Statement |
| :--- | :--- |
| `RML-OBJ-001` | App 顯示的 telemetry、roster、command 結果必須衍生自現行 repo SSOT，不可自行發明 wire semantics。 |
| `RML-OBJ-002` | 系統必須同時保留 App `stableId`、Central `central_ref`、BLE MAC 三種身分邊界，不得混用。 |
| `RML-OBJ-003` | 當 Central 權威分配與 firmware runtime attach 不一致時，UI 必須可見且可追查。 |
| `RML-OBJ-004` | 規格內容必須可被下一個 AI 或腳本續維護，並能追蹤需求到驗收與測試。 |
| `RML-OBJ-005` | cross-repo operating model 必須明確區分 repo-level technical truth 與 project-level orchestration truth，不得混為同一層。 |
| `RML-OBJ-006` | RML、requirements、queue、acceptance 必須共享 `baseline / target / migration` stage 模型，避免現況、目標與過渡期混寫。 |

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

## Authority Boundaries

| ID | Boundary Rule |
| :--- | :--- |
| `RML-AUT-001` | Operator 可查看與執行已授權的低風險操作，但不得單獨定義 canonical identity、assignment truth 或 system policy。 |
| `RML-AUT-002` | Engineer 可執行高權限診斷與維護流程，但不得繞過 Central authority 或直接改寫 repo SSOT。 |
| `RML-AUT-003` | Gateway / Edge Nodes 擁有 runtime measurement、local QoS、local failover 觸發與 radio behavior 的第一手 truth；Central 與 App 不得假裝擁有這層 truth。 |
| `RML-AUT-004` | Central System 擁有 global truth / system-of-record authority；App、Firmware、Conductor 不得自行重定 canonical identity、assignment 或 auth truth。 |
| `RML-AUT-005` | Conductor / AI orchestration layer 只管理規劃、派工、驗收、handoff 與治理，不直接介入 real-time control loop，也不覆寫 runtime truth。 |
| `RML-AUT-006` | project-level orchestration truth 與 repo-level technical truth 必須分層；`--base-dir` 只承接 cross-repo control docs，不承接 repo-level technical SSOT。 |

## Human Operational Roles

| ID | Role | Responsibility |
| :--- | :--- | :--- |
| `RML-ROL-001` | Operator | 查看 fleet / device 基本狀態，不做高風險操作。 |
| `RML-ROL-002` | Installer / Maintainer | 執行一般維護操作、查看 detail、處理現場更換；屬於 human operational role，不改變第一級 actor 分層。 |
| `RML-ROL-003` | Engineer | 使用工程診斷、進階命令、衝突與例外排查。 |

## Scope

| ID | Statement |
| :--- | :--- |
| `RML-SCP-001` | In scope: device list/detail、telemetry 顯示、roster 顯示、alias precedence、assignment reconciliation、command feedback。 |
| `RML-SCP-002` | Out of scope: OTA、歷史分析、desktop 專屬 UI 規格、本輪未提供來源的新 Central API。 |
| `RML-SCP-003` | In scope: cross-repo orchestration、queue / gate governance、handoff、evidence index、project-level acceptance model。 |
| `RML-SCP-004` | Out of scope: 讓 AI orchestration layer 直接成為 runtime control authority，或在 `--base-dir` 複製 repo-level technical SSOT。 |

## Feature Tree

| ID | Feature |
| :--- | :--- |
| `RML-FEA-001` | Telemetry & roster visibility ([detail](feature-telemetry-roster-visibility.md)) |
| `RML-FEA-002` | Command execution & feedback ([detail](feature-command-execution-feedback.md)) |
| `RML-FEA-003` | Identity, alias, and metadata display ([detail](feature-identity-alias-metadata-display.md)) |
| `RML-FEA-004` | Assignment reconciliation ([detail](feature-assignment-reconciliation.md)) |

## Constraints

| ID | Constraint |
| :--- | :--- |
| `RML-CST-001` | GATT UUID、wire format、opcode 只可從 firmware repo `ble_api.yaml` 衍生。 |
| `RML-CST-002` | App 採 task-scoped BLE connection；同一時間只連一台裝置。 |
| `RML-CST-003` | `P0 sparse` 是正常資料狀態，不得視為錯誤。 |
| `RML-CST-004` | PNG / render artifact 不可直接編修；原始碼 `.md` / `.mmd` / `.d2` / `.yaml` 才是治理來源。 |
| `RML-CST-005` | `--base-dir` 只承接 cross-repo formal control docs；repo-level technical truth 仍以各 repo SSOT 為準。 |
| `RML-CST-006` | `Conductor / AI orchestration layer` 可管理 planning 與 governance，但不得直接取代 Central、Firmware 或 App 的權威邊界。 |
| `RML-CST-007` | 所有 `.d2` / `.mmd` source 必須帶 `AI Diagram Contract` comment block，並遵守 `diagram-authoring-rules.md` 與 `diagram-templates.md` 的可讀性限制。 |

## Risks & Recovery

| ID | Risk | Recovery Rule |
| :--- | :--- | :--- |
| `RML-RSK-001` | GATT contract drift | 以 `ble_api.yaml` 回寫 packet / sequence / AC / TC。 |
| `RML-RSK-002` | Identity drift | 保持 `stableId`、`central_ref`、MAC 分層，UI 必須標示來源。 |
| `RML-RSK-003` | Central 與 runtime 分配不一致 | UI 顯示雙來源 + reconciliation badge，不可靜默合併。 |
| `RML-RSK-004` | Command timeout / error | 進入可重試或失敗狀態，保留 txn 與 evidence。 |
| `RML-RSK-005` | project-level orchestration truth 與 repo-level SSOT 混線 | 以 authority boundary 回寫：repo 技術真相回 repo、cross-repo 控制面回 `--base-dir`。 |
| `RML-RSK-006` | AI orchestration 越權成為 runtime authority | 保持 `Conductor` 只做規劃 / 派工 / 驗收 / handoff，禁止直接扮演 control loop 權威。 |
