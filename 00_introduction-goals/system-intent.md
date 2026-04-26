# System Intent

> arc42 §1 — Introduction & Goals.
> **L3 Source-Level Refactor 2026-04-27** (per `~/.claude/plans/task-b-rml-ddd-refactor.md`): RML-INT / RML-OBJ / RML-CST / RML-RSK 等 opaque ID schema 已廢除, 改 name-canonical narrative + chapter-position-canonical (per Backstage / C4 / arc42 reference). Cross-ref by `file.md#section-anchor` (D3).
> Actors + Authority Boundaries + Human Operational Roles + Scope → see [stakeholders.md](./stakeholders.md), [bounded-context-map.md](../01_context-scope/bounded-context-map.md).
> 細部 capability ownership → [capability-map.md](../02_solution-strategy/capability-map.md); stage 模型見 [baseline-target-migration.md](../05_quality-acceptance/baseline-target-migration.md).

## System Intent

BLE QoS Demo 同時承擔三條互相獨立但無法分離的 intent — 任何一條被弱化都會破壞另外兩條的可驗證性。

- **Sustainable-Reference-System** — 系統對外可作為 demo 展示, 對內必須是可持續演進、可驗證、可交接的 reference system, 不是一次性展示品。任何短期性 hack 必須記錄為 risk-and-debt entry (見 [risks-and-debt.md](../99_appendix/risks-and-debt.md)) 而不是隱性堆疊。
- **Cross-Repo-Authority-Boundary** — 系統的真正驗證主題是 App、Firmware、Central 三個 repo 之間的協作模型、能力邊界與產品化路徑, 而不是任一單 repo 的功能性。權威 ownership 由 [bounded-context-map.md](../01_context-scope/bounded-context-map.md) 與 [capability-map.md](../02_solution-strategy/capability-map.md) 雙重定義, 跨層越權必須以 architectural mismatch 處理。
- **Spec-as-Code-Continuity** — cross-repo 控制面、驗收、handoff、queue 與 evidence 必須可被後續 AI / automation layer 穩定接續, 不依賴單一作業者記憶。所有 spec 變更走 [README.md](../README.md) 規定的 upstream→downstream 順序, 由 vocab-check + trace_map CI 強制執行。

## Strategic Goals

下表 6 條為 system-level strategic goal, 對應 [quality-goals.md](./quality-goals.md) 7 條 ISO 25010 operational quality scenario; 兩者層次不同 (strategic intent vs operational quality scenario) 不可混用。Stakeholder 欄位指 primary owner role, 完整 stakeholder map 見 [stakeholders.md#first-level-actors](./stakeholders.md#first-level-actors)。

| Goal Name | Description | Quality Goal Cross-Ref | Stakeholder |
|---|---|---|---|
| **SSOT-Driven-UI-Semantics** | App 顯示的 telemetry、roster、command 結果必須衍生自現行 repo SSOT, 不可自行發明 wire semantics。 | [quality-goals.md#goal-3-wire-contract-stability--gatt-ssot-enforcement](./quality-goals.md#goal-3-wire-contract-stability--gatt-ssot-enforcement) | Mobile / App |
| **Three-Layer-Identity-Separation** | 系統必須同時保留 App `stableId`、Central `central_ref`、BLE MAC 三種身分邊界, 不得混用。 | [quality-goals.md#goal-4-identity-boundary-integrity--three-layer-non-confusion](./quality-goals.md#goal-4-identity-boundary-integrity--three-layer-non-confusion) | Central |
| **Authority-Mismatch-Observability** | 當 Central 權威分配與 firmware runtime attach 不一致時, UI 必須可見且可追查。 | [quality-goals.md#goal-1-observability--telemetry--conflict-visibility](./quality-goals.md#goal-1-observability--telemetry--conflict-visibility) | Mobile / App |
| **AI-Continuable-Traceability** | 規格內容必須可被下一個 AI 或腳本續維護, 並能追蹤需求到驗收與測試。 | [quality-goals.md#goal-2-spec-traceability--requirements-to-acceptance-chain](./quality-goals.md#goal-2-spec-traceability--requirements-to-acceptance-chain) | AI Continuator |
| **Two-Layer-Operating-Model** | cross-repo operating model 必須明確區分 repo-level technical truth 與 project-level orchestration truth, 不得混為同一層。 | [quality-goals.md#goal-7-authority-boundary-enforcement--no-orchestration-overreach](./quality-goals.md#goal-7-authority-boundary-enforcement--no-orchestration-overreach) | All Repos |
| **Tri-Stage-Spec-Lifecycle** | 規格、requirements、queue、acceptance 必須共享 `baseline / target / migration` stage 模型, 避免現況、目標與過渡期混寫。 | [quality-goals.md#goal-6-governance-automation--ai-continuable-spec-lifecycle](./quality-goals.md#goal-6-governance-automation--ai-continuable-spec-lifecycle) | All Repos |

## Feature Tree

| ID | Feature |
| :--- | :--- |
| `FEA-001` | Telemetry & roster visibility ([detail](../03_building-blocks/FEA-001-telemetry-roster-visibility.md)) |
| `FEA-002` | Command execution & feedback ([detail](../03_building-blocks/FEA-002-command-execution-feedback.md)) |
| `FEA-003` | Identity, alias, and metadata display ([detail](../03_building-blocks/FEA-003-identity-alias-metadata-display.md)) |
| `FEA-004` | Assignment reconciliation ([detail](../03_building-blocks/FEA-004-assignment-reconciliation/contract.md)) |

## Engineering Invariants

下表 7 條為 architectural rule, 系統運作前提, 不可被 feature 變更跨越。與 [constraints.md](../02_solution-strategy/constraints.md) (legal / regulatory / hardware constraint) 層次不同 — Engineering Invariants 是系統內部 architectural enforcement, constraints 是 external limitation。

| Invariant Name | Statement | Enforcement Mechanism | Cross-Ref |
|---|---|---|---|
| **Wire-Semantics-From-SSOT** | GATT UUID、wire format、opcode 只可從 firmware repo `ble_api.yaml` 衍生。 | codegen pipeline + CI vocab-check rule | [02_solution-strategy/constraints.md](../02_solution-strategy/constraints.md) |
| **Single-Active-BLE-Connection** | App 採 task-scoped BLE connection; 同一時間只連一台裝置。 | App `connectionState` 狀態機 (IDLE / CONNECTING / CONNECTED / DISCONNECTING) | [01_context-scope/ubiquitous-language.md](../01_context-scope/ubiquitous-language.md), [03_building-blocks/FEA-002-command-execution-feedback.md](../03_building-blocks/FEA-002-command-execution-feedback.md) |
| **Sparse-Telemetry-Is-Normal** | `P0 sparse` 是正常資料狀態, 不得視為錯誤。 | telemetry render rule + reconciliation badge logic | [03_building-blocks/FEA-001-telemetry-roster-visibility.md](../03_building-blocks/FEA-001-telemetry-roster-visibility.md) |
| **Source-Diagram-Authority** | PNG / render artifact 不可直接編修; 原始碼 `.md` / `.mmd` / `.d2` / `.yaml` 才是治理來源。 | pre-commit hook + CI render-only-from-source check | [04_runtime-deployment/diagram-authoring-rules.md](../04_runtime-deployment/diagram-authoring-rules.md) |
| **Base-Dir-Cross-Repo-Only** | `--base-dir` 只承接 cross-repo formal control docs; repo-level technical truth 仍以各 repo SSOT 為準。 | conductor base-dir scoping + per-repo CLAUDE.md authority list | [02_solution-strategy/capability-map.md](../02_solution-strategy/capability-map.md) |
| **AI-Orchestration-Non-Authority** | `Conductor / AI orchestration layer` 可管理 planning 與 governance, 但不得直接取代 Central、Firmware 或 App 的權威邊界。 | authority-map.yaml runtime check + ADR governance rule | [01_context-scope/authority-map.yaml](../01_context-scope/authority-map.yaml), [99_appendix/decisions/](../99_appendix/decisions/) |
| **AI-Diagram-Contract-Mandatory** | 所有 `.d2` / `.mmd` source 必須帶 `AI Diagram Contract` comment block, 並遵守 `diagram-authoring-rules.md` 與 `diagram-templates.md` 的可讀性限制。 | diagram-lint CI + pre-commit hook | [04_runtime-deployment/diagram-authoring-rules.md](../04_runtime-deployment/diagram-authoring-rules.md), [04_runtime-deployment/diagram-templates.md](../04_runtime-deployment/diagram-templates.md) |

## Risks & Recovery

> **Migrated to [risks-and-debt.md](../99_appendix/risks-and-debt.md) per L3 C4** (2026-04-27): risk content 屬於 99_appendix 而非 §1 introduction-goals 章節。下列 6 項 stub 保留 traceability 至 risk-and-debt 完整 statement / recovery rule, 各 entry 改 name-canonical (廢 RSK ID schema)。

- **GATT-Contract-Drift** — 已遷出, 見 [risks-and-debt.md](../99_appendix/risks-and-debt.md)
- **Identity-Drift** — 已遷出, 見 [risks-and-debt.md](../99_appendix/risks-and-debt.md)
- **Authority-Runtime-Mismatch** — 已遷出, 見 [risks-and-debt.md](../99_appendix/risks-and-debt.md)
- **Command-Timeout-Or-Error** — 已遷出, 見 [risks-and-debt.md](../99_appendix/risks-and-debt.md)
- **Project-Vs-Repo-Truth-Mixing** — 已遷出, 見 [risks-and-debt.md](../99_appendix/risks-and-debt.md)
- **AI-Orchestration-Authority-Overreach** — 已遷出, 見 [risks-and-debt.md](../99_appendix/risks-and-debt.md)
