# Capability Matrix — Wave 2: Replay + Event Coverage

> Wave: Firmware Phase 3 Wave 2
> Source: `capability-ownership.md`, `firmware-phase3-reliability.md` Wave 2 Tasks 3.6–3.8

## Per-Role Capabilities

| Capability | GW | ED | CC | App | Central |
|---|---|---|---|---|---|
| Backhaul reconnect replay | **OWNS** — drain work on ready transition | — | — | — | receives idempotently |
| INFO family dispatch (`0x21`) | **OWNS** — `uplink_dispatch_p0_ed_info()` | event source | — | — | — |
| HA failover detection | **OWNS** — ha_runtime state machine | — | **OWNS** — heartbeat timeout detect | — | — |
| Structured failover uplink (P0 ALARM) | **OWNS** — `uplink_dispatch_p0_gw_failover()` | — | triggers | — | consumes, updates assignment |
| Structured failover uplink (P1 full) | **OWNS** — `uplink_dispatch_p1_gw_failover()` | — | — | — | consumes, canonical record |
| Idempotent replay dedup | — | — | — | — | **OWNS** — dedup by `(gw_mac, boot_id, msg_seq)` |
| Assignment update after failover | — | — | — | — | **OWNS** — `active_gateway_id`, `failover_generation` |
| Failover event display | — | — | — | **OWNS** — UI badge + reconciliation | — |

## Authority Boundaries (Wave 2)

| ID | Boundary |
|---|---|
| `W2-BND-001` | GW owns failover detection + local promotion — Central reconciles after receiving P0/P1 uplink |
| `W2-BND-002` | Central Ingest must be idempotent — replayed Class A frames must not cause double-count |
| `W2-BND-003` | Failover P0 `ed_hash=0` is GW-self sentinel — Central parser must not interpret as ED identity |
| `W2-BND-004` | INFO family dispatch is best-effort Class B — loss during ring full is acceptable |
