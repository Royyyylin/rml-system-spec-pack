# Crosscutting Concept: HA Failover & Uplink Reliability

> arc42 §6 Crosscutting Concepts — Failover
> Status: active
> Owner: spec-pack (system level)
> Last updated: 2026-04-26
> SSOT for uplink class: `ble_qos_demo_V1.2m/src/uplink_frame_v2.h` → `enum uplink_class`
> SSOT for HA state: `ble_qos_demo_V1.2m/src/ha_persist.h`, `ha_runtime.h`
> SSOT for GATT wire: `ble_qos_demo_V1.2m/ble_api.yaml` → `HA_HB` characteristic

---

## Purpose

Defines the cross-repo failover architecture: the GW chain HA topology,
`uplink_ring` buffering strategy, A/B/C uplink class priority, and the
reconciliation event flow triggered by GW role transitions.

This concept governs firmware-side HA behavior and its observable effects
on App and Central.

---

## HA Failover Topology (GW Chain)

The system supports a GW-pair high-availability model:

- **ACTIVE GW**: currently handling ED roster, QoS arbitration, and uplink relay.
- **STANDBY GW**: monitors ACTIVE via periodic heartbeats; ready to promote on failure detection.

```
  ED₁  ED₂  ED₃
   \    |    /
    [  ACTIVE GW  ]──────────── uplink (UART/GATT) ──→ Central/App
         ↕  HA_HB (21-byte heartbeat via BLE GATT HA_HB char)
    [ STANDBY GW  ]             (also manages an ED sub-roster)
```

Both nodes share the `HA_HB` GATT characteristic (UUID `6f8a9c17-...`) as the
heartbeat transport wire. CC bridge may relay HA_HB frames between GW pairs
when they are not directly BLE-connected.

**Invariant**: At any time, at most one GW is in ACTIVE role per HA domain.
Role state is persisted atomically in NVS (`ha/` namespace) as a packed
`role + epoch` blob to prevent split-brain after power loss.

---

## HA State Machine

GW HA roles are managed by the `gw_ha` module (firmware). The `ha_runtime`
integration layer drives the state machine at 100ms tick cadence.

| HA Role | Description |
|---------|-------------|
| `ACTIVE` | Owns the ED roster; handling QoS; uplink active |
| `STANDBY` | Monitoring ACTIVE peer; uplink in warm-standby |
| `CANDIDATE` | Ephemeral during initial election (not NVS-persisted) |

### Peer Health Detection

| Event | Trigger Condition | Runtime Action |
|-------|-------------------|----------------|
| `HA_EVT_PEER_SUSPECT` | Peer missed 3 consecutive heartbeats | Log warning; no role change |
| `HA_EVT_PEER_DEAD` | Peer missed 5 consecutive heartbeats | Optional auto-promote (if enabled with holdoff) |
| `HA_EVT_PEER_RECOVERED` | Peer heartbeat returns | Clear suspect/dead flag; emit recovery log |
| `HA_EVT_PROMOTED` | This node transitions STANDBY → ACTIVE | Start ED roster scan; force P0 uplink for 30s |
| `HA_EVT_DEMOTED` | This node transitions ACTIVE → STANDBY | Yield ED roster; force P0 uplink for 30s |

**Auto-promote holdoff**: configurable delay (default: disabled in Phase 2) after
`PEER_DEAD` before promotion. Prevents split-brain during transient BLE disruptions.

---

## uplink_ring Strategy

The `uplink_ring` module provides a priority-aware ring buffer for GW-to-Central
uplink frames. It operates independently of the HA state machine but interacts
at failover boundaries.

### Ring Properties

| Property | Value |
|---|---|
| Slot size | 30 bytes (26B max frame + 1B class + 1B len + 2B pad) |
| Thread safety | k_spinlock (ISR-safe) |
| Ordering | FIFO pop; class-aware eviction on push |
| Persistence | Class A entries persisted to NVS across reboot |

### Uplink Class Priority

Three classes govern buffering priority and eviction:

| Class | Enum | Data Types | Eviction |
|-------|------|-----------|----------|
| **A** | `UL_CLASS_A = 0` | Disconnect, reconnect, ALARM events | **Never evicted** |
| **B** | `UL_CLASS_B = 1` | Metrics, heartbeat, INFO events | Evicted after all Class C consumed |
| **C** | `UL_CLASS_C = 2` | Future P2 diagnostic types | First evicted when ring full |

**Eviction policy** (ring full, incoming push):
1. Evict oldest Class C slot → accept incoming
2. If no Class C: evict oldest Class B slot → accept incoming
3. If no Class B: reject (return `-ENOMEM`); Class A incoming always rejected instead of evicting Class A

### NVS Persistence for Class A

Class A frames are snapshot-saved to NVS on every push and restored on reboot.
This ensures disconnect/reconnect/ALARM events survive power cycles and are
replayed to Central after the GW comes back online.

Drain worker (`uplink_drain_kick`) detects backend not-ready → ready transitions
and automatically replays buffered frames in Class A priority order.

---

## A/B/C Uplink Class Priority (Cross-Repo View)

| Layer | Class A (Critical) | Class B (Operational) | Class C (Diagnostic) |
|-------|-------------------|----------------------|---------------------|
| **Firmware** | Failover events, ALARM | Periodic metrics, HA heartbeat | Future diagnostics |
| **Wire format** | P0 (8B survival) | P1 (26B standard) | P2 (reserved) |
| **Buffering** | NVS-persisted, never dropped | Ring-buffered, evictable | Best-effort |
| **App impact** | Must reach Central for triage | High-value telemetry; tolerable loss | Optional enrichment |
| **Central impact** | Required for device state reconciliation | Feeds historical analytics | Future |

---

## Reconciliation Event Flow (on GW Failover)

When a GW transitions from STANDBY → ACTIVE (promotion), the following
reconciliation event sequence occurs:

```
STANDBY GW (promoting)         ACTIVE GW (failed/demoted)   Central / App
      |                                |                          |
      |← HA_EVT_PEER_DEAD              |                          |
      |   (5 missed heartbeats)        |                          |
      |                                |                          |
      |── uplink P0: GW_FAILOVER ─────────────────────────────→  |
      |   (UL_CLASS_A, immediate)      |                          |
      |                                |                          |
      |── ha_runtime_promote() ──→ ACTIVE role                   |
      |── ha_force_p0() = true         |                          |
      |   (30s force P0 window)        |                          |
      |                                |                          |
      |── Scan ED roster ──────────→ adopt ED connections         |
      |                                |                          |
      |── uplink P0: GW_FAILOVER_SELF ─────────────────────────→ |
      |   (UL_CLASS_A, new ACTIVE)     |                          |
      |                                |                          |
      |   [after backend ready]                                   |
      |── Drain uplink_ring (Class A first) ──────────────────→  |
      |                                |                          |
      |   [Central receives GW_FAILOVER events]                  |
      |── Central reconciles device assignments ──────────────→  |
```

### Force P0 Window

On either promote or demote, `ha_force_p0()` activates for 30 seconds.
During this window, `gw_qos` ignores zone-based profile selection and forces
the most reliable QoS profile (P0: ROBUST / Coded PHY / max TX power).
This protects the ED fleet during GW transition instability.

---

## HA Persistence Across Reboot

The `ha_persist` module saves minimal HA state to NVS under the `ha/` namespace:

| NVS Key | Content | Notes |
|---------|---------|-------|
| `ha/node_id` | `uint8_t` node_id | Immutable after first provision |
| `ha/role_epoch` | `struct ha_persist_role_epoch` (5B packed) | Role + epoch; atomic write prevents split-brain |
| `ha/ed_parent` | `struct ha_persist_ed_parent` | ED parent slot tracking (lease NOT persisted — expires on reboot) |

Recovery priority on boot: `node_id` → `role+epoch` → `ed_parent`.
Missing or corrupt keys default to safe state: STANDBY, epoch 0, no parent.

All NVS writes go through `app_settings_wq` (dedicated work queue) per
firmware architecture rules — never directly in GATT callbacks or interrupt
context.

---

## Cross-Repo Responsibilities

| Repo | Failover Responsibility |
|------|------------------------|
| Firmware (`ble_qos_demo_V1.2m`) | HA state machine (`gw_ha`), `ha_runtime` tick, `ha_persist` NVS, `uplink_ring` buffering, HA_HB GATT transport |
| App (`ble_qos_app`) | Display current GW identity; react to uplink GW_FAILOVER events for UX indicators |
| Central (`central-device-metadata`) | Receive GW_FAILOVER uplink events; reconcile device assignment state (`assignment_state`) after GW change |
| Spec-pack | Failover topology definition (this document); `ble_api.yaml` HA_HB wire SSOT |

---

## Trace

- `REQ-FW-HA-001` — STANDBY GW detects ACTIVE failure within 5 missed heartbeats
- `REQ-FW-HA-002` — Class A uplink frames persisted to NVS across power cycle
- `REQ-FW-HA-003` — Force P0 window of 30s activates on promote/demote transitions
- `REQ-X-HA-001` — GW_FAILOVER uplink event reaches Central within drain cycle

---

## Open Questions

- Q1: Multi-GW (>2) HA chain topology — not defined in current spec; uplink_ring
  supports it structurally but election protocol is undefined beyond 2-node pair.
- Q2: ED sub-roster handoff on failover — current implementation does NOT hand off
  roster across GW promotion (known Phase 3+ non-goal per `ha_runtime.h`).
