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
