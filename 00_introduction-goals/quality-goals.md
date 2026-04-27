# Quality Goals

> arc42 §1.2 — Quality Goals.
> ISO 25010 category reference: https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
> **L3 Name-Canonical Refactor 2026-04-27** (per `~/.claude/plans/task-b-rml-ddd-refactor.md`): RML-OBJ / RML-INT / RML-ACT / RML-CST / RML-RSK opaque IDs廢除, 改 name-canonical cross-ref by `system-intent.md#strategic-goals`. Goal N: numbering prefix removed; descriptive section names retained.
> Cross-ref: [system-intent.md](system-intent.md) | [stakeholders.md](stakeholders.md)
> Feature traces: FEA-001 / FEA-002 / FEA-003 / FEA-004 / F-04

## Priority Ordering

Quality goals are ordered by architectural priority (arc42 convention: top = most influential on design decisions).
Eight ISO 25010 categories are used as the structuring framework, mapped from this system's 8 quality scenarios.

---

## Functional Suitability — Identity Boundary Integrity

| Attribute | Value |
|---|---|
| **ISO 25010 Category** | Functional Suitability (Functional Correctness sub-characteristic) |
| **Priority** | 4 |
| **Feature Traces** | FEA-003, FEA-004 |
| **Strategic Goal Cross-Ref** | [Three-Layer-Identity-Separation](system-intent.md#strategic-goals) |

**Scenario:** An operator views a device list. The App must simultaneously and unambiguously display `stableId` (Central-assigned), `central_ref`, and BLE MAC — never conflating them — even when all three refer to the same physical node.

**Metric:** FEA-003 integration tests assert all three identity layers present and distinct on every device row. No UI path silently promotes BLE MAC to device identity.

**Motivation:** [Three-Layer-Identity-Separation](system-intent.md#strategic-goals) requires three-layer identity preservation as a fundamental correctness invariant. Conflation has caused identity drift bugs in earlier prototypes; this is a functional correctness matter, not merely a presentation concern.

---

## Performance Efficiency — Command Latency & Telemetry Throughput

| Attribute | Value |
|---|---|
| **ISO 25010 Category** | Performance Efficiency (Time Behaviour sub-characteristic) |
| **Priority** | 8 |
| **Feature Traces** | FEA-001, FEA-002, F-04 |
| **Strategic Goal Cross-Ref** | [SSOT-Driven-UI-Semantics](system-intent.md#strategic-goals) |

**Scenario:** Under normal operating conditions (≥ 3 EDs attached, GW within NEAR/MID zone), telemetry updates must reach the App display within 2 seconds of the firmware measurement. CMD_V2 command round-trip (issue → RESULT notification) must complete within `CMD_V2_TIMEOUT_MS` (see `ble_api.yaml → system_constants.CMD_V2_TIMEOUT_MS`).

**Metric:** P95 telemetry display latency ≤ 2 s under nominal load; CMD_V2 timeout transitions to explicit retry/failed state (never silent drop). Measured by FEA-001 and FEA-002 performance acceptance criteria.

**Motivation:** [SSOT-Driven-UI-Semantics](system-intent.md#strategic-goals) requires that App display derives from live firmware truth. Stale or delayed display undermines the demo's reference value and operator trust.

---

## Compatibility — Wire Contract Stability (GATT SSOT Enforcement)

| Attribute | Value |
|---|---|
| **ISO 25010 Category** | Compatibility (Interoperability sub-characteristic) |
| **Priority** | 3 |
| **Feature Traces** | FEA-002, F-04 |
| **Strategic Goal Cross-Ref** | [SSOT-Driven-UI-Semantics](system-intent.md#strategic-goals) |

**Scenario:** When a new opcode or characteristic is added to firmware, the App must not silently invent its own wire semantics. All GATT UUID, wire format, and opcode values are derived exclusively from `ble_api.yaml`.

**Metric:** Zero App-side hardcoded GATT UUIDs or opcode literals not generated from `ble_api.yaml`. Enforced by codegen + CI lint gate (see FEA-002 contract).

**Motivation:** GATT contract drift is a leading cause of cross-repo integration failures in BLE systems. [SSOT-Driven-UI-Semantics](system-intent.md#strategic-goals) mandates single-source wire semantics. SSOT enforcement prevents drift structurally.

---

## Usability — Observability (Telemetry & Conflict Visibility)

| Attribute | Value |
|---|---|
| **ISO 25010 Category** | Usability (Operability sub-characteristic) |
| **Priority** | 1 |
| **Feature Traces** | FEA-001, FEA-003, FEA-004 |
| **Strategic Goal Cross-Ref** | [Authority-Mismatch-Observability](system-intent.md#strategic-goals) |

**Scenario:** When Central assignment and firmware runtime roster diverge (e.g., ED reconnects after GW failover), the App must surface a visible reconciliation badge within 5 seconds of detecting the discrepancy. Operators and Engineers (see [stakeholders.md](stakeholders.md)) must never need to guess device state by inspection.

**Metric:** 100% of assignment conflicts visible in UI within 5 s of detection; zero silent state merges confirmed by FEA-004 contract tests.

**Motivation:** Invisible state drift is the primary cause of operational errors in multi-hop BLE systems. [Authority-Mismatch-Observability](system-intent.md#strategic-goals) defines explicit discrepancy surfacing as a hard invariant, not a nice-to-have.

---

## Reliability — Command Reliability (End-to-End Transaction Integrity)

| Attribute | Value |
|---|---|
| **ISO 25010 Category** | Reliability (Fault Tolerance sub-characteristic) |
| **Priority** | 5 |
| **Feature Traces** | FEA-002, F-04 |
| **Strategic Goal Cross-Ref** | [SSOT-Driven-UI-Semantics](system-intent.md#strategic-goals) |

**Scenario:** A CMD_V2 command is issued while the BLE connection is marginal. The system must: (a) surface a retryable or failed state, (b) preserve the transaction record and evidence, and (c) never silently drop the command as if it succeeded.

**Metric:** CMD_V2 timeout always transitions to a user-visible retry/failed state; transaction evidence retained ≥ 1 session for Engineer review. See FEA-002 for AC detail.

**Motivation:** Silent command drop leaves devices in unknown state. Explicit failure + evidence retention is required for both operational trust and AI handoff continuity, supporting [AI-Continuable-Traceability](system-intent.md#strategic-goals).

---

## Security — Authority Boundary Enforcement (No Orchestration Overreach)

| Attribute | Value |
|---|---|
| **ISO 25010 Category** | Security (Integrity sub-characteristic) |
| **Priority** | 7 |
| **Feature Traces** | FEA-004 |
| **Strategic Goal Cross-Ref** | [Two-Layer-Operating-Model](system-intent.md#strategic-goals) |

**Scenario:** The Conductor / AI orchestration layer dispatches a plan task. The task execution must not directly modify firmware runtime state, Central canonical data, or App wire semantics — only governance artifacts (spec, plan, queue, evidence).

**Metric:** Conductor actions are limited to spec-pack write + PR open + queue update; any direct repo SSOT mutation by orchestration layer is blocked at CI gate and logged.

**Motivation:** [Two-Layer-Operating-Model](system-intent.md#strategic-goals) defines the Conductor authority boundary. Overreach would corrupt the clean-room engineering boundary and undermine auditability for FEA-004 and all cross-repo features.

---

## Maintainability — Spec Traceability (Requirements-to-Acceptance Chain)

| Attribute | Value |
|---|---|
| **ISO 25010 Category** | Maintainability (Analysability sub-characteristic) |
| **Priority** | 2 |
| **Feature Traces** | FEA-001, FEA-002, FEA-003, FEA-004, F-04 |
| **Strategic Goal Cross-Ref** | [AI-Continuable-Traceability](system-intent.md#strategic-goals) |

**Scenario:** A new AI agent or engineer onboards and must locate the acceptance criterion, test case, and wire-contract for any feature within 10 minutes, using only the spec-pack as entry point.

**Metric:** Every feature in the Feature Tree (system-intent.md) has a traceable path: spec → AC entry → TC entry → `ble_api.yaml` wire reference. Verified by `cross-repo-trace-strategy.md` linter in CI.

**Motivation:** [AI-Continuable-Traceability](system-intent.md#strategic-goals) mandates that cross-repo control surfaces must be stably handoff-able to AI or automation layers. Untraceable specs break this invariant.

---

## Portability — Governance Automation (AI-Continuable Spec Lifecycle)

| Attribute | Value |
|---|---|
| **ISO 25010 Category** | Portability (Adaptability sub-characteristic) |
| **Priority** | 6 |
| **Feature Traces** | FEA-001, FEA-002, FEA-003, FEA-004 |
| **Strategic Goal Cross-Ref** | [Tri-Stage-Spec-Lifecycle](system-intent.md#strategic-goals) |

**Scenario:** The spec-pack is updated by an automated AI agent between human sessions. The update must pass vocabulary-check, doc-size, and cross-ref CI gates without human intervention before being merge-eligible.

**Metric:** All spec PRs pass vocab-check + doc-size-limit + cross-ref linter gates in CI; zero manual override required for compliant updates.

**Motivation:** [Tri-Stage-Spec-Lifecycle](system-intent.md#strategic-goals) positions this system as a continuously evolvable reference platform. Manual governance is a bottleneck that contradicts this intent. Governance automation enables the spec lifecycle to be portable across AI sessions and human contributors without bespoke intervention.
