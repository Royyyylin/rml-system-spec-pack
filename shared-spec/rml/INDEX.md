# RML Wave Diagram Index — Master MOC

> Cross-repo RML (Rich Modeling Language) documents per wave.
> Format follows `shared-spec/rml-lite.md` actors/authority/scope model.
> Each wave has 5 documents: ecosystem-map / capability-matrix / event-storming / context-map / glossary-deltas.

## Wave Inventory

| Wave | Scope | Repo Focus | Documents |
|---|---|---|---|
| [Wave 1](#wave-1) | Firmware Phase 3 Wave 1: Data Classification + Uplink Buffer | Firmware | 5 docs |
| [Wave 2](#wave-2) | Firmware Phase 3 Wave 2: Replay + Event Coverage | Firmware | 5 docs |
| [Wave 3](#wave-3) | Firmware Phase 3 Wave 3: Verification + Convergence | Firmware + Central | 5 docs |
| [F-04](#f-04) | GW QoS Scheduler Deployment Tuning (cross-repo feature) | Firmware + App + Central + Spec-Pack | 5 docs |
| [FW-3A](#fw-3a) | CMD_V2 Per-Opcode Length Guard (firmware spec phase) | Firmware | 5 docs |
| [W26A](#w26a) | Shift Reporting + Dashboard Customization | App | 5 docs |
| [W30](#w30) | Fleet Broadcast + WebSocket Push + Auto-Grouping | App + Central | 5 docs |
| [W31](#w31) | Auto-Grouping Refinement + WebSocket + Adaptive Layout | App + Central | 5 docs |

**Total: 8 waves × 5 documents = 40 RML documents**

---

## Wave 1

**Firmware Phase 3 Wave 1: Data Classification + Uplink Buffer**
Tasks 3.1–3.5. Class A/B/C classification, `uplink_ring`, NVS persist, profile auto-switch.

| Document | Link | Key Content |
|---|---|---|
| Ecosystem Map | [wave-1/ecosystem-map.md](wave-1/ecosystem-map.md) | GW ring buffer + Central dedup actors |
| Capability Matrix | [wave-1/capability-matrix.md](wave-1/capability-matrix.md) | Class A/B/C ownership; wire byte invariant |
| Event Storming | [wave-1/event-storming.md](wave-1/event-storming.md) | Frame push/evict/persist events |
| Context Map | [wave-1/context-map.md](wave-1/context-map.md) | QoS → dispatch → ring → Central boundary |
| Glossary Deltas | [wave-1/glossary-deltas.md](wave-1/glossary-deltas.md) | UL_CLASS_A/B/C, uplink_ring, P0/P1 profile |

Cross-links: `firmware-phase3-reliability.md` Tasks 3.1–3.5 | `dispatch-wire-contract.md`

---

## Wave 2

**Firmware Phase 3 Wave 2: Replay + Event Coverage**
Tasks 3.6–3.8. Backhaul reconnect replay, INFO family, structured failover uplink.

| Document | Link | Key Content |
|---|---|---|
| Ecosystem Map | [wave-2/ecosystem-map.md](wave-2/ecosystem-map.md) | Replay path + HA failover actors |
| Capability Matrix | [wave-2/capability-matrix.md](wave-2/capability-matrix.md) | Replay / INFO / failover ownership |
| Event Storming | [wave-2/event-storming.md](wave-2/event-storming.md) | BackhaulReady → drain; failover P0/P1 |
| Context Map | [wave-2/context-map.md](wave-2/context-map.md) | HA → ring → ingest boundaries |
| Glossary Deltas | [wave-2/glossary-deltas.md](wave-2/glossary-deltas.md) | backhaul replay, ed_hash=0 sentinel, INFO family |

Cross-links: `firmware-phase3-reliability.md` Tasks 3.6–3.8 | `dispatch-wire-p1-families.md` Path 7

---

## Wave 3

**Firmware Phase 3 Wave 3: Verification + Convergence**
Tasks 3.9–3.10. boot_id real-device verify, E2E path, R1–R6 gate, Phase 4 unblock.

| Document | Link | Key Content |
|---|---|---|
| Ecosystem Map | [wave-3/ecosystem-map.md](wave-3/ecosystem-map.md) | Verify harness + Central E2E path |
| Capability Matrix | [wave-3/capability-matrix.md](wave-3/capability-matrix.md) | HIL / unit test / E2E ownership; gate criteria |
| Event Storming | [wave-3/event-storming.md](wave-3/event-storming.md) | 4 reset scenarios; Phase3GatePassed |
| Context Map | [wave-3/context-map.md](wave-3/context-map.md) | Firmware ↔ Central parser alignment |
| Glossary Deltas | [wave-3/glossary-deltas.md](wave-3/glossary-deltas.md) | HIL, golden vector, spec sync, E2E path |

Cross-links: `phase3-verification-checklist.md` | `firmware-phase3-reliability.md` §Minimum Reliability Criteria

---

## F-04

**GW QoS Scheduler Deployment Tuning (cross-repo feature)**
Feature owner: spec-pack. Sub-phases: FW-3A/3B/4/5 (firmware), A-1~A-6 (App), C-1 (Central).

| Document | Link | Key Content |
|---|---|---|
| Ecosystem Map | [f04/ecosystem-map.md](f04/ecosystem-map.md) | 4-actor tuning flow: App → GW → NVS → Central |
| Capability Matrix | [f04/capability-matrix.md](f04/capability-matrix.md) | TUNE-VAL owners; must-not-violate table |
| Event Storming | [f04/event-storming.md](f04/event-storming.md) | preset select → CMD_V2 0x07 → accept/reject → NVS |
| Context Map | [f04/context-map.md](f04/context-map.md) | Spec-Pack schema → App editor → Firmware handler |
| Glossary Deltas | [f04/glossary-deltas.md](f04/glossary-deltas.md) | TUNE-VAL, preset, CMD_V2 0x07, NVS LKG, config coupling |

Cross-links: `feature-gw-qos-scheduler-tuning.md` | `capability-ownership.md` RML-CAP-006 | ADR `2026-04-18-f04-runtime-preset-over-build-assert.md`

---

## FW-3A

**CMD_V2 Per-Opcode Length Guard (firmware spec phase)**
Prerequisite for FW-3B (0x07 handler). Part of F-04 firmware implementation chain.

| Document | Link | Key Content |
|---|---|---|
| Ecosystem Map | [fw3a/ecosystem-map.md](fw3a/ecosystem-map.md) | GATT → dispatch → length guard → CMD_RESULT |
| Capability Matrix | [fw3a/capability-matrix.md](fw3a/capability-matrix.md) | valid_lens[], NULL slot, codegen source |
| Event Storming | [fw3a/event-storming.md](fw3a/event-storming.md) | BAD_LENGTH flow; FW-3A frozen milestone |
| Context Map | [fw3a/context-map.md](fw3a/context-map.md) | ble_api.yaml → codegen → dispatch boundary |
| Glossary Deltas | [fw3a/glossary-deltas.md](fw3a/glossary-deltas.md) | cmd_v2_dispatch, valid_lens[], BAD_LENGTH 0xFF |

Cross-links: `fw3b-cmd-v2-0x07-handler-impl.md` §1 | `ble_api.yaml` opcodes table | `glossary.md` §F-04 vs FW-3A

---

## W26A

**App Wave 26A: Shift Reporting + Dashboard Customization**
App-local report generation from cached data. No Central reporting contracts added.

| Document | Link | Key Content |
|---|---|---|
| Ecosystem Map | [w26a/ecosystem-map.md](w26a/ecosystem-map.md) | App cache → aggregation engine → export |
| Capability Matrix | [w26a/capability-matrix.md](w26a/capability-matrix.md) | Report generation ownership; out-of-scope list |
| Event Storming | [w26a/event-storming.md](w26a/event-storming.md) | ReportRequested → aggregation → clipboard export |
| Context Map | [w26a/context-map.md](w26a/context-map.md) | App-local isolation; Wave 25A dependencies |
| Glossary Deltas | [w26a/glossary-deltas.md](w26a/glossary-deltas.md) | ShiftReport, ReportAggregationEngine, regeneration_params |

Cross-links: `ble_qos_app/docs/plans/sections/w26-01-shift-reports.md` | `w26-02-dashboard-customization.md`

---

## W30

**App Wave 30: Fleet Broadcast + WebSocket Push + Auto-Grouping**
Cross-repo: App + Central. Dependencies: Wave 24A groups, Wave 29A sync engine.

| Document | Link | Key Content |
|---|---|---|
| Ecosystem Map | [w30/ecosystem-map.md](w30/ecosystem-map.md) | App batch dispatch → Central → GW command |
| Capability Matrix | [w30/capability-matrix.md](w30/capability-matrix.md) | Broadcast / group / WS ownership; truth boundary |
| Event Storming | [w30/event-storming.md](w30/event-storming.md) | FleetCommand state machine; per-device ack |
| Context Map | [w30/context-map.md](w30/context-map.md) | App ↔ Central broadcast + group + WS |
| Glossary Deltas | [w30/glossary-deltas.md](w30/glossary-deltas.md) | FleetCommand, BroadcastEngine, per-device acked, AutoGroupRule |

Cross-links: `ble_qos_app/docs/plans/sections/w30-*.md` | `capability-ownership.md` RML-CAP-001

---

## W31

**App Wave 31A: Auto-Grouping + WebSocket Refinement + Adaptive Layout**
Cross-repo: App + Central. Upgrades W30 WS; adds M3 adaptive layout.

| Document | Link | Key Content |
|---|---|---|
| Ecosystem Map | [w31/ecosystem-map.md](w31/ecosystem-map.md) | WS transport + FCM fallback + adaptive layout |
| Capability Matrix | [w31/capability-matrix.md](w31/capability-matrix.md) | WS/FCM ownership; phone regression gate |
| Event Storming | [w31/event-storming.md](w31/event-storming.md) | WS heartbeat/backoff; ack correlation_id |
| Context Map | [w31/context-map.md](w31/context-map.md) | WS → REST ACL; W28A/29A/30A dependencies |
| Glossary Deltas | [w31/glossary-deltas.md](w31/glossary-deltas.md) | WsTransport, BroadcastAckHandler, AdaptiveScaffold, Breakpoints |

Cross-links: `ble_qos_app/docs/plans/sections/w31-*.md` | W30 glossary | W29A SyncEngine

---

## Cross-Wave Conflict / Overlap Register

| Overlap | Waves | Resolution |
|---|---|---|
| `uplink_ring` push API | Wave 1 (defines) / Wave 2 (uses) | Wave 2 depends on Wave 1 completion; no conflict |
| `uplink_class_of()` function | Wave 1 (defines) / Wave 2 (reuses for INFO + failover) | Same function; Wave 2 adds call sites only |
| `FleetCommand` entity | Wave 30 (defines) / Wave 31 (WS ack updates status) | W31 updates are additive; no model change |
| `GroupMembershipCache` | Wave 30 (defines) / Wave 31 (adds UI) | W31 UI layer on top of W30 cache; no conflict |
| `FCM push` | Wave 30 (uses) / Wave 31 (demotes to fallback) | W31 explicitly supersedes W30 FCM role; documented in W31 glossary |
| `auto-group rules` | Wave 30 (defines) / Wave 31 (adds mgmt UI) | W31 does not add new rule types; Central authority unchanged |
| CMD_V2 dispatch table | FW-3A (defines) / FW-3B (fills 0x07 slot) | Sequential phases; FW-3A must freeze before FW-3B starts |
| TUNE-VAL schema | F-04 (defines) / FW-3A+3B+4+5 (implement) | Spec-pack is schema owner; firmware phases are implementation |

No terminology conflicts detected across all 8 waves.
