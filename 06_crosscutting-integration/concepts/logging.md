# Crosscutting Concept: Logging & Observability

> arc42 §6 Crosscutting Concepts — Logging
> Status: active
> Owner: spec-pack (system level)
> Last updated: 2026-04-26
> SSOT for event schema: `ble_qos_demo_V1.2m/docs/features/firmware-log-observability/events.md`
> SSOT for wire format: `ble_qos_demo_V1.2m/ble_api.yaml` → `LOG_STREAM` characteristic

---

## Purpose

Defines the cross-repo logging architecture: the 13-dimension LOG event schema,
wire format convention, category bitmap, and multi-layer retention policy.
All repos must align to this contract when producing or consuming LOG events.

---

## 13-Dimension LOG Event Schema

Each LOG event carries exactly 13 semantic dimensions. The schema is
taxonomy-primary (Category-first, following OPC UA / Memfault / ISA-18.2 pattern).

| Dim | Name | Wire Field | Values / Notes |
|-----|------|-----------|----------------|
| 1 | **Category** | `category` (uint8, offset 12) | A=1 DEVICE / B=2 CONNECTION / C=3 CONTROL / D=4 METRICS / E=5 COORDINATION / F=6 SECURITY/ADMIN / G=7 OPERATIONS |
| 2 | **Phase** | `key_val` (metadata) | `boot_time` / `runtime` / `terminate` |
| 3 | **Trigger** | `key_val` (metadata) | `linear` / `loop` / `edge` |
| 4 | **Severity** | `severity` (uint16, offset 6) | OPC UA 1-1000: ≤250 INFO / 251-500 WARN / 501-999 ALARM / 1000 FATAL |
| 5 | **Ack model** | `key_val` (metadata) | `no-ack` / `auto-ack` / `ack-only` / `ack+confirm` |
| 6 | **Rate-limit** | `key_val` (metadata) | `per-event` / `aggregate` / `edge-only` / `shelvable` |
| 7 | **SECS/GEM** | `key_val` (metadata) | CEID / SVID / ECID / DVID / Stream 5 Alarm (optional) |
| 8 | **Roles** | `roles` (uint8, offset 13) | Bitmask: GW=bit0, ED=bit1, CC=bit2 |
| 9 | **Cause** | `key_val` (metadata) | WARN/ALARM required; blank for INFO |
| 10 | **Consequence** | `key_val` (metadata) | WARN/ALARM required; blank for INFO |
| 11 | **Operator Action** | `key_val` (metadata) | WARN/ALARM required; blank for INFO |
| 12 | **Time-to-Respond** | `key_val` (metadata) | WARN/ALARM required; blank for INFO |
| 13 | **Classification** | `key_val` (metadata) | safety / env / quality / process / security / network (ISA-18.2) |

> Dimensions 9-12 are blank for INFO events (severity ≤ 250). Required for WARN/ALARM.

---

## Wire Format (64-byte Fixed Entry)

Source of truth: `ble_api.yaml` → `LOG_STREAM.entry_format`

```
offset  size  field       type         note
 0      2     event_id    uint16_le    monotonic per-boot sequence number
 2      4     timestamp   uint32_le    Zephyr uptime_ms() at event time
 6      2     severity    uint16_le    OPC UA scale 1-1000 (see Dim 4)
 8      4     chip_id     uint32_le    nRF52833 DEVICEID[0]
12      1     category    uint8        A-G categories (see Dim 1)
13      1     roles       uint8        GW/ED/CC bitmask (see Dim 8)
14      2     reserved    uint16_le    zero-pad
16     48     key_val     uint8[48]    null-terminated key=value pairs, zero-padded
```

Fixed 64-byte size ensures atomic SDC write granularity and deterministic flash paging.

---

## Category Bitmap (Runtime Filter)

The category bitmap controls which LOG categories are persisted to the flash ring
buffer. It does NOT affect RTT live-stream output.

- **NVS key**: `qos/log_bitmap`
- **Fallback**: `0x0000007F` (categories A-G all on, no optional bits)
- **Runtime override**: CMD_V2 opcode `0x09 SET_LOG_EVENT_BITMAP`
- **Bit layout**: bits 0-6 = categories A-G; bits 7-10 = optional (GATT_OP/CCC_DETAIL/PAIRING/BATTERY); bits 11-31 reserved (must be zero; firmware rejects with BAD_BITMAP 0x10 if set)

See `ble_api.yaml` → `opcodes.0x09` for full contract.

---

## Multi-Layer Retention Policy

| Layer | Medium | Capacity | Retention | Scope |
|-------|--------|----------|-----------|-------|
| RTT live | JTAG RTT RAM buffer (~4 KB) | Rolling | Power-cycle | ALL severities |
| RAM circular | Static ring buffer | 100 events | Boot-cycle | ALL severities |
| Flash ring buffer | Dedicated partition @ `0x00080000` (32 KB) | 512 events | Ring-overwrite oldest; ~14-year endurance at 10 WARN/day rate | WARN + ALARM only |
| Coredump partition | Dedicated partition @ `0x00088000` (12 KB) | 1 crash | Overwrites previous | FATAL only |
| App SQLite | Mobile local DB | 30-day rolling | Per-device | Pulled via LOG_STREAM |
| Central | Future / out of scope | — | — | Reserved |

Severity-to-layer mapping:

| Severity range | RTT | RAM circular | Flash ring | Coredump |
|----------------|-----|--------------|------------|----------|
| 1-250 INFO | Yes | Yes | No | No |
| 251-500 WARN | Yes | Yes | Yes | No |
| 501-999 ALARM | Yes | Yes | Yes | No |
| 1000 FATAL | Yes | Yes | Yes | Yes |

---

## Format Convention

All log messages follow key=value ASCII encoding in the `key_val` field:

```
role=GW rssi=-72 zone=FAR reason=PHY_CHANGE
```

Rules:
- Fields separated by single space; key=value pairs, no quotes
- UTF-8, null-terminated within 48 bytes; remainder zero-padded
- Keys use `snake_case`; canonical key names defined in firmware event catalogue
- SSOT for event-level key names: `docs/features/firmware-log-observability/events.md`

---

## Cross-Repo Responsibilities

| Repo | Role in Logging |
|------|----------------|
| Firmware (`ble_qos_demo_V1.2m`) | Event production, flash ring buffer, RTT, LOG_STREAM GATT characteristic |
| App (`ble_qos_app`) | Pull via LOG_STREAM, store in SQLite 30-day rolling, present to user |
| Central (`central-device-metadata`) | Future relay / aggregation (out of scope this phase) |
| Spec-pack | Schema authority (this document); wire format SSOT in `ble_api.yaml` |

---

## Trace

- `REQ-LOG-001` — runtime category bitmap persists across reboot (NVS)
- `REQ-LOG-002` — WARN/ALARM written to flash ring buffer while offline
- `AC-LOG-001` through `AC-LOG-011` — see `docs/features/log-storage-spec.md`

---

## Open Questions

None. All dimensions resolved via events.md + log-storage-spec.md + F-LOG-BITMAP contract (2026-04-24).
