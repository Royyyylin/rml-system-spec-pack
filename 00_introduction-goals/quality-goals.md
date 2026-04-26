# Quality Goals

> arc42 §1.2 — Quality Goals.
> ISO 25010 category reference: https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
> Cross-ref: [system-intent.md](system-intent.md) | [stakeholders.md](stakeholders.md)
> Feature traces: FEA-001 / FEA-002 / FEA-003 / FEA-004 / F-04

## Priority Ordering

Quality goals are ordered by architectural priority (arc42 convention: top = most influential on design decisions).

---

## Goal 1: Observability — Telemetry & Conflict Visibility

| Attribute | Value |
|---|---|
| **ISO 25010 Category** | Operability (Usability sub-characteristic) |
| **Priority** | 1 — Highest architectural influence |
| **Feature Traces** | FEA-001, FEA-003, FEA-004 |
| **system-intent.md Anchor** | `RML-OBJ-003`, `RML-OBJ-001` |

**Scenario:** When Central assignment and firmware runtime roster diverge (e.g., ED reconnects after GW failover), the App must surface a visible reconciliation badge within 5 seconds of detecting the discrepancy. Operators and Engineers (see [stakeholders.md](stakeholders.md) `RML-ACT-001`, `RML-ACT-002`) must never need to guess device state by inspection.

**Metric:** 100% of assignment conflicts visible in UI within 5 s of detection; zero silent state merges confirmed by FEA-004 contract tests.

**Motivation:** Invisible state drift is the primary cause of operational errors in multi-hop BLE systems. Explicit discrepancy surfacing (system-intent.md `RML-OBJ-003`) is a hard invariant, not a nice-to-have.

---

## Goal 2: Spec Traceability — Requirements-to-Acceptance Chain

| Attribute | Value |
|---|---|
| **ISO 25010 Category** | Maintainability (Analysability sub-characteristic) |
| **Priority** | 2 |
| **Feature Traces** | FEA-001, FEA-002, FEA-003, FEA-004, F-04 |
| **system-intent.md Anchor** | `RML-OBJ-004`, `RML-INT-003` |

**Scenario:** A new AI agent or engineer onboards and must locate the acceptance criterion, test case, and wire-contract for any feature within 10 minutes, using only the spec-pack as entry point.

**Metric:** Every feature in the Feature Tree (system-intent.md) has a traceable path: spec → AC entry → TC entry → `ble_api.yaml` wire reference. Verified by `cross-repo-trace-strategy.md` linter in CI.

**Motivation:** system-intent.md `RML-INT-003` mandates that cross-repo control surfaces must be stably handoff-able to AI or automation layers. Untraceable specs break this invariant.

---

## Goal 3: Wire Contract Stability — GATT SSOT Enforcement

| Attribute | Value |
|---|---|
| **ISO 25010 Category** | Compatibility (Interoperability sub-characteristic) |
| **Priority** | 3 |
| **Feature Traces** | FEA-002, F-04 |
| **system-intent.md Anchor** | `RML-OBJ-001`, `RML-CST-001` |

**Scenario:** When a new opcode or characteristic is added to firmware, the App must not silently invent its own wire semantics. All GATT UUID, wire format, and opcode values are derived exclusively from `ble_api.yaml` (system-intent.md `RML-CST-001`).

**Metric:** Zero App-side hardcoded GATT UUIDs or opcode literals not generated from `ble_api.yaml`. Enforced by codegen + CI lint gate (see FEA-002 contract).

**Motivation:** GATT contract drift (system-intent.md `RML-RSK-001`) has been observed as a leading cause of cross-repo integration failures in BLE systems; SSOT enforcement prevents it structurally.

---

## Goal 4: Identity Boundary Integrity — Three-Layer Non-Confusion

| Attribute | Value |
|---|---|
| **ISO 25010 Category** | Reliability (Integrity sub-characteristic) |
| **Priority** | 4 |
| **Feature Traces** | FEA-003, FEA-004 |
| **system-intent.md Anchor** | `RML-OBJ-002`, `RML-RSK-002` |

**Scenario:** An operator views a device list. The App must simultaneously and unambiguously display `stableId` (Central-assigned), `central_ref`, and BLE MAC — never conflating them — even when all three refer to the same physical node.

**Metric:** FEA-003 integration tests assert all three identity layers present and distinct on every device row. No UI path silently promotes BLE MAC to device identity.

**Motivation:** system-intent.md `RML-OBJ-002` explicitly requires three-layer identity preservation. Conflation has caused identity drift bugs in earlier prototypes (see system-intent.md `RML-RSK-002`).

---

## Goal 5: Command Reliability — End-to-End Transaction Integrity

| Attribute | Value |
|---|---|
| **ISO 25010 Category** | Reliability (Fault Tolerance sub-characteristic) |
| **Priority** | 5 |
| **Feature Traces** | FEA-002, F-04 |
| **system-intent.md Anchor** | `RML-RSK-004` |

**Scenario:** A CMD_V2 command is issued while the BLE connection is marginal. The system must: (a) surface a retryable or failed state, (b) preserve the transaction record and evidence, and (c) never silently drop the command as if it succeeded.

**Metric:** CMD_V2 timeout always transitions to a user-visible retry/failed state; transaction evidence retained ≥ 1 session for Engineer review. See FEA-002 for AC detail.

**Motivation:** Silent command drop (system-intent.md `RML-RSK-004`) leaves devices in unknown state. Explicit failure + evidence retention is required for both operational trust and AI handoff continuity.

---

## Goal 6: Governance Automation — AI-Continuable Spec Lifecycle

| Attribute | Value |
|---|---|
| **ISO 25010 Category** | Maintainability (Modifiability sub-characteristic) |
| **Priority** | 6 |
| **Feature Traces** | FEA-001, FEA-002, FEA-003, FEA-004 |
| **system-intent.md Anchor** | `RML-INT-002`, `RML-INT-003`, `RML-OBJ-005` |

**Scenario:** The spec-pack is updated by an automated AI agent between human sessions. The update must pass vocabulary-check, doc-size, and cross-ref CI gates without human intervention before being merge-eligible.

**Metric:** All spec PRs pass vocab-check + doc-size-limit + cross-ref linter gates in CI; zero manual override required for compliant updates.

**Motivation:** system-intent.md `RML-INT-002` / `RML-INT-003` positions this system as a continuously evolvable reference platform. Manual governance is a bottleneck that contradicts this intent.

---

## Goal 7: Authority Boundary Enforcement — No Orchestration Overreach

| Attribute | Value |
|---|---|
| **ISO 25010 Category** | Security (Integrity sub-characteristic) |
| **Priority** | 7 |
| **Feature Traces** | FEA-004 |
| **system-intent.md Anchor** | `RML-CST-006`, `RML-RSK-006`, `RML-OBJ-005` |

**Scenario:** The Conductor / AI orchestration layer (`RML-ACT-005`) dispatches a plan task. The task execution must not directly modify firmware runtime state, Central canonical data, or App wire semantics — only governance artifacts (spec, plan, queue, evidence).

**Metric:** Conductor actions are limited to spec-pack write + PR open + queue update; any direct repo SSOT mutation by orchestration layer is blocked at CI gate and logged.

**Motivation:** system-intent.md `RML-CST-006` / `RML-RSK-006` define the Conductor authority boundary. Overreach would corrupt the clean-room engineering boundary and undermine auditability for FEA-004 and all cross-repo features.
