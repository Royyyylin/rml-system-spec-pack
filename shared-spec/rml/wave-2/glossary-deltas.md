# Glossary Deltas — Wave 2: Replay + Event Coverage

> Cross-links master glossary: `01_context-scope/ubiquitous-language.md`
> New terms introduced in Firmware Phase 3 Wave 2.

## New Terms

| Term | Definition | Canonical Location |
|---|---|---|
| `backhaul reconnect replay` | When uplink backend transitions `not-ready → ready`, GW automatically drains ring buffer (Class A first, then B). | `src/uplink.c`, `firmware-phase3-reliability.md` Task 3.6 |
| `INFO family` | Uplink event type `0x21` (`ULF_T_EVENT_INFO`). Class B. `value0=info_id`, `value1=info_data`. | `src/uplink_dispatch.c` |
| `failover P0 ALARM` | `type=0x20`, `ed_hash=0` (GW-self sentinel), `value0=reason`, `value1=new_role`. Class A. | `src/uplink_dispatch.c` |
| `failover P1` | 24B P1 frame with repurposed tail: `ed_slot=new_role`, `rssi=reason`, `lat_ms=(peer<<8|old_role)`. Class A. | `src/uplink_dispatch.c` |
| `ha_runtime` | GW firmware state machine managing active/standby HA role transitions. | `src/ha_runtime.c` |
| `s_backend_was_ready` | Flag in `uplink.c` tracking previous backend ready state; used to detect `not-ready → ready` transition. | `src/uplink.c` |
| `drain batch limit` | Maximum 4 frames popped per drain work tick; remainder immediately rescheduled. Prevents monopolizing workqueue. | `firmware-phase3-reliability.md` Task 3.6 |
| `ed_hash=0 sentinel` | When `ed_hash=0` appears in P0 ALARM, it indicates a GW-self event (not an ED). | `dispatch-wire-contract.md` |

## Existing Terms Referenced

- `failover_generation` — incremented per HA promotion; see `glossary.md`
- `Class A/B/C` — uplink frame classes from Wave 1; see `rml/wave-1/glossary-deltas.md`
- `boot_id` — `reset_count` from NVS; used in P1 dedup key; see `glossary.md`

## Disambiguation

- `ha_runtime` ≠ `CC bridge` — `ha_runtime` is a GW state machine. CC bridge is a relay firmware. CC detects heartbeat timeout and triggers ha_runtime state change in GW.
- `failover P0` ≠ `ed alarm P0` — Both use type `0x20`, but `ed_hash=0` indicates GW-self; non-zero `ed_hash` indicates an ED alarm.
