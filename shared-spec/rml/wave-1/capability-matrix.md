# Capability Matrix — Wave 1: Data Classification + Uplink Buffer

> Wave: Firmware Phase 3 Wave 1
> Source: `capability-ownership.md` RML-CAP-001~006, `firmware-phase3-reliability.md` Wave 1 Tasks 3.1–3.5

## Per-Role Capabilities

| Capability | GW | ED | CC | App | Central |
|---|---|---|---|---|---|
| Uplink data class classification | **OWNS** — `uplink_class_of()` | — | — | — | consumes class label |
| Ring buffer push/pop/eviction | **OWNS** — `uplink_ring` module | — | — | — | — |
| Class A frame protection (no-evict) | **OWNS** — eviction guard | — | — | — | — |
| NVS persist Class A across reboot | **OWNS** — `uplink_ring_persist()` | — | — | — | — |
| Profile auto-switch (P0/P1 select) | **OWNS** — QoS zone → profile | — | — | — | — |
| P0/P1 wire format production | **OWNS** — `uplink_dispatch` | — | — | — | — |
| P0/P1 wire frame decoding | — | — | — | — | **OWNS** — Ingest API |
| Dedup by `(gw_mac, boot_id, msg_seq)` | — | — | — | — | **OWNS** — Ingest dedup |
| Runtime RSSI/PDR telemetry | **OWNS** — qos_monitor 1Hz | **OWNS** — GATT notify source | — | display only | stores canonical |
| HA heartbeat relay | — | — | **OWNS** — HA_HB GATT | — | — |

## Authority Boundaries (Wave 1)

| ID | Boundary |
|---|---|
| `W1-BND-001` | GW owns uplink classification truth — Central must not re-classify frames |
| `W1-BND-002` | Ring buffer eviction order is firmware-internal — App/Central do not observe eviction decisions |
| `W1-BND-003` | Wire byte layout is frozen at `dispatch-wire-contract.md` — Wave 1 ring buffer does NOT change wire bytes |
| `W1-BND-004` | NVS persist is a local durability concern — Central dedup handles replay idempotency |
