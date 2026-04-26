# Bounded Context Map

> arc42 §3 — System Scope and Context (DDD Bounded Context).
> split source: rml-lite.md lines 46-55 (Authority Boundaries) + lines 65-72 (Scope).
> Machine-readable boundary → [authority-map.yaml](authority-map.yaml) (commit 3/8).
> Actors → [stakeholders.md](../00_introduction-goals/stakeholders.md).

## Authority Boundaries

| ID | Boundary Rule |
| :--- | :--- |
| `RML-AUT-001` | Operator 可查看與執行已授權的低風險操作，但不得單獨定義 canonical identity、assignment truth 或 system policy。 |
| `RML-AUT-002` | Engineer 可執行高權限診斷與維護流程，但不得繞過 Central authority 或直接改寫 repo SSOT。 |
| `RML-AUT-003` | Gateway / Edge Nodes 擁有 runtime measurement、local QoS、local failover 觸發與 radio behavior 的第一手 truth；Central 與 App 不得假裝擁有這層 truth。 |
| `RML-AUT-004` | Central System 擁有 global truth / system-of-record authority；App、Firmware、Conductor 不得自行重定 canonical identity、assignment 或 auth truth。 |
| `RML-AUT-005` | Conductor / AI orchestration layer 只管理規劃、派工、驗收、handoff 與治理，不直接介入 real-time control loop，也不覆寫 runtime truth。 |
| `RML-AUT-006` | project-level orchestration truth 與 repo-level technical truth 必須分層；`--base-dir` 只承接 cross-repo control docs，不承接 repo-level technical SSOT。 |

## Scope

| ID | Statement |
| :--- | :--- |
| `RML-SCP-001` | In scope: device list/detail、telemetry 顯示、roster 顯示、alias precedence、assignment reconciliation、command feedback。 |
| `RML-SCP-002` | Out of scope: OTA、歷史分析、desktop 專屬 UI 規格、本輪未提供來源的新 Central API。 |
| `RML-SCP-003` | In scope: cross-repo orchestration、queue / gate governance、handoff、evidence index、project-level acceptance model。 |
| `RML-SCP-004` | Out of scope: 讓 AI orchestration layer 直接成為 runtime control authority，或在 `--base-dir` 複製 repo-level technical SSOT。 |

## Bounded Context Diagram

Diagram source: [system-actors.d2](system-actors.d2)

The four bounded contexts in this system:

| Context | Authority Owner | Bounded Concern |
| :--- | :--- | :--- |
| **Canonical Identity** | Central | global identity、assignment、auth、metadata truth |
| **Wire Contract** | Firmware | GATT UUID、opcode、payload semantics |
| **Runtime Observation** | Firmware / Gateway | telemetry、QoS measurement、failover execution |
| **Interaction Semantics** | App | human-facing UX、view state、role-gated UI |
| **Orchestration** | Conductor | cross-repo planning、dispatch、evidence index |

## DDD Strategic Design — Context Relationships (Evans 2003)

> Annotations per Eric Evans, _Domain-Driven Design_ (2003), Chapter 14: Maintaining Model Integrity.
> Each relationship describes how the downstream context consumes the upstream context's model.

### Relationship Map

| Upstream Context | Downstream Context | Evans Pattern | Rationale |
| :--- | :--- | :--- | :--- |
| **Wire Contract** (Firmware) | **Canonical Identity** (Central) | Anti-Corruption Layer | Central translates incoming GATT wire events (raw BLE MAC, opcode payloads) into its own domain model (`stableId`, `assignment_state`) via an explicit translation layer — never importing Firmware domain objects directly. This prevents Firmware's low-level GATT vocabulary from leaking into Central's identity domain. |
| **Canonical Identity** (Central) | **Interaction Semantics** (App) | Open-Host Service (OHS) | Central publishes a stable REST API (identity, assignment, metadata endpoints) as a well-defined Open-Host Service. App is a consumer of this published service; Central's API is versioned and documented independently of App's internal model. Multiple downstream consumers (App, future monitoring dashboards) can consume the same OHS without Central coupling to any one consumer. |
| **Canonical Identity** (Central) | **Interaction Semantics** (App) | Customer-Supplier | In addition to the OHS relationship, App acts as Customer and Central as Supplier for the assignment reconciliation flow (FEA-004). App drives the reconciliation use case requirements; Central prioritizes its API surface to satisfy App's assignment-conflict visibility needs (quality-goals.md Goal 1). This Customer-Supplier relationship is formalized in the FEA-004 feature spec and AC catalog. |
| **Wire Contract** (Firmware) | **Orchestration** (Conductor) | Conformist | The Conductor / AI orchestration layer must accept Firmware's `ble_api.yaml` wire contract as-is, without attempting to influence its design. Conductor is Conformist: it derives its understanding of wire semantics from `ble_api.yaml` (cross-repo-trace-strategy.md) and adapts its governance artifacts to match, not the reverse. This enforces RML-AUT-005 (Conductor does not override runtime truth). |

### Pattern Definitions (Reference)

| Evans Pattern | Definition |
| :--- | :--- |
| **Anti-Corruption Layer** | A translation layer that insulates a downstream bounded context from an upstream model, converting upstream concepts into downstream domain objects. Prevents upstream vocabulary from polluting the downstream model. |
| **Open-Host Service (OHS)** | An upstream context publishes a well-defined, versioned API (the "published language") for multiple downstream consumers. Changes to the upstream internal model do not break consumers as long as the OHS contract is preserved. |
| **Customer-Supplier** | Downstream (Customer) drives requirements; upstream (Supplier) commits to delivering an API surface that satisfies Customer needs. Requires explicit negotiation and prioritization. |
| **Conformist** | Downstream context accepts the upstream model as-is, without translation. Used when the upstream is authoritative and the downstream has no leverage to change the upstream design. |

### Notes

- **Runtime Observation → Interaction Semantics**: App ingests telemetry from Firmware via GW uplink. This is also a Conformist relationship (App adapts to Firmware telemetry schema, defined in `ble_api.yaml`). Not listed separately above to avoid duplication with the Wire Contract → Orchestration Conformist entry; both share the same upstream SSOT.
- **Orchestration → all contexts**: Conductor is Conformist to all four upstream bounded contexts. It cannot modify any upstream model; it can only read, reference, and govern.
- Evans relationships are annotations on existing authority boundaries (RML-AUT-001~006); they do not change authority ownership.
