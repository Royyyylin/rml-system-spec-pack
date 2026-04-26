# Glossary Deltas — Wave 1: Data Classification + Uplink Buffer

> Cross-links master glossary: `01_context-scope/ubiquitous-language.md`
> New terms introduced in Firmware Phase 3 Wave 1.

## New Terms

| Term | Definition | Canonical Location |
|---|---|---|
| `UL_CLASS_A` | Uplink frame class: disconnect / reconnect / alarm events. Must buffer, must replay, never evicted. | `src/uplink_frame_v2.h` |
| `UL_CLASS_B` | Uplink frame class: metrics / heartbeat / info. High reliability, profile-aware sparsification allowed. | `src/uplink_frame_v2.h` |
| `UL_CLASS_C` | Uplink frame class: future P2 diagnostic types. Can be dropped when ring is full. | `src/uplink_frame_v2.h` (reserved) |
| `uplink_ring` | Fixed-depth ring buffer for uplink frames in GW firmware. Supports priority eviction (C→B, Class A protected). Thread-safe via `k_spinlock`. | `src/uplink_ring.c` |
| `uplink_drain_work` | `k_work_delayable` that pops frames from ring and sends via UART backend. Triggered on backhaul-ready transition. | `src/uplink.c` |
| `P0 profile` | Compact 8-byte uplink frame. Used in degraded link / Coded PHY. Approximate identity only (`ed_hash`). | `dispatch-wire-contract.md` |
| `P1 profile` | Standard 24-byte uplink frame. Full MAC + boot_id + msg_seq + ts_device. Canonical identity. | `dispatch-wire-contract.md` |
| `profile auto-switch` | GW QoS zone change automatically selects P0 or P1 uplink profile. NEAR/MID → P1; FAR/EDGE → P0. | `firmware-phase3-reliability.md` Task 3.4 |
| `uplink_class_of(type_byte)` | Pure function mapping type byte → UL_CLASS_A/B/C. | `src/uplink_frame_v2.h` |

## Existing Terms Referenced (see master glossary)

- `MSG_SEQ` — per-GW monotonic counter; used as dedup key component; see `glossary.md`
- `boot_id` — = `reset_count` from NVS `qos/rst_cnt`; see `firmware-phase3-reliability.md` Task 3.9
- `P0 sparse` — normal data state (not an error); see `glossary.md` `RML-CST-003`

## Disambiguation

- `gw_buffer` ≠ `uplink_ring` — `gw_buffer` is a governance / P0-payload buffer (20B entry). `uplink_ring` is the transport-layer uplink frame queue (28B slot). Do not conflate.
