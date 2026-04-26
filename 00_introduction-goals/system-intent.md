# System Intent

> arc42 §1 — Introduction & Goals.
> split source: rml-lite.md (System Intent lines 5-11, System Goals lines 13-22, Feature Tree lines 74-81, Constraints lines 83-93, Risks & Recovery lines 95-105).
> Actors + Authority Boundaries + Human Operational Roles + Scope → see 01_context-scope/ (stakeholders.md, bounded-context-map.md).
> 細部 capability ownership → [capability-map.md](../02_solution-strategy/capability-map.md)；stage 模型見 [baseline-target-migration.md](../05_quality-acceptance/baseline-target-migration.md)。

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

## Feature Tree

| ID | Feature |
| :--- | :--- |
| `FEA-001` | Telemetry & roster visibility ([detail](../03_building-blocks/FEA-001-telemetry-roster-visibility.md)) |
| `FEA-002` | Command execution & feedback ([detail](../03_building-blocks/FEA-002-command-execution-feedback.md)) |
| `FEA-003` | Identity, alias, and metadata display ([detail](../03_building-blocks/FEA-003-identity-alias-metadata-display.md)) |
| `FEA-004` | Assignment reconciliation ([detail](../03_building-blocks/FEA-004-assignment-reconciliation/contract.md)) |

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
