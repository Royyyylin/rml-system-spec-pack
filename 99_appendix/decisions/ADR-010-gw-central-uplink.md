# ADR-010: GW↔Central Uplink — CC Bridge Relay for Prototype

Status: accepted
Date: 2026-04-26
Decided by: Roy (K4 OQ resolution, resolves F7-OQ2)
Resolves: F7-OQ2 — was: USB-serial vs Wi-Fi direct TBD for GW uplink to Central

## Context

GW (Gateway) firmware aggregates BLE telemetry from ED nodes and must deliver that
data to Central for canonical storage. Two architectural paths were under consideration:

1. **CC bridge relay**: GW serves data via GATT (existing QoS Service 0x1820). CC
   bridge firmware connects to GW over BLE, receives GATT notifications, and forwards
   to Central via the USB-serial host bridge (see ADR-009). GW has no direct IP link.

2. **Wi-Fi direct from GW**: GW DK gains Wi-Fi capability (external module or different
   hardware) and POSTs telemetry directly to Central's `/ingest` REST API, bypassing
   CC bridge entirely.

The CC relay path is already implemented in the firmware prototype:
- CC bridge scans for GW by name prefix "FGW" (`cc_bridge.c:23`)
- GW exposes RSSI / STATUS / METRICS / EVT notifications on the QoS GATT service
- Central `/ingest` already accepts `QosStatusIngest`, `P1MetricsIngest`, `HaHeartbeatIngest`

The nRF52833 DK has no onboard Wi-Fi. Adding Wi-Fi requires an external SPI/UART
module (e.g., ESP-AT or nRF7002 EK), which is not in the current prototype BOM and
would require overlay and driver work estimated at > 2 sprint-weeks.

The HA failover sequence (`04_runtime-view/seq-ha-failover.md`) explicitly shows
"CC >> Central: 上報 GW-A unreachable" — confirming the CC relay path is the design
baseline for the HA architecture.

## Decision

GW↔Central uplink = **CC bridge relay** for the prototype phase. GW does not have a
direct IP link to Central. The data path is:

```
GW (BLE GATT notify) → CC bridge firmware (BLE central role)
  → USB-serial → host daemon → Central /ingest REST API
```

Wi-Fi direct from GW is **reserved for production** when hardware includes a wireless
uplink module (nRF7002 or equivalent). At that point the CC relay path becomes
redundant for uplink (CC may still serve the BLE-to-App forwarding function).

The GW's existing GATT service is the uplink data source; no additional GW firmware
changes are required for this decision.

## Consequences

**Positive:**
- Zero GW firmware changes required — existing GATT service is the uplink surface
- CC bridge relay reuses ADR-009 infrastructure (USB-serial host daemon)
- HA failover (`seq-ha-failover.md`) already modeled on this topology
- Allows GW to remain a pure BLE device with single-radio simplicity

**Negative:**
- Uplink path has two hops (GW→CC via BLE, CC→Central via USB-serial) — adds latency
- CC DK must be physically connected to host via USB at all times during operation
- GW uplink bandwidth limited by BLE notification throughput

**Trigger for re-evaluation:**
Production BOM change that adds Wi-Fi or LTE-M to GW hardware. At that point,
GW can POST directly to Central and CC relay is retained only for BLE-to-App path.

## Alternatives

- **Wi-Fi direct from GW (nRF52833 + SPI ESP-AT)**: Rejected for prototype.
  ESP-AT driver integration in NCS requires 2+ sprint-weeks; CC relay is already
  functional and validated by HA failover tests.
- **GW posts over USB to host (no CC)**: Rejected. GW is a field device; USB tether
  to host contradicts the wireless field deployment model. CC bridge is the intended
  aggregation point.
- **BLE mesh GW → CC**: Rejected. Project explicitly does not use BLE Mesh
  (see CLAUDE.md: "不使用 BLE Mesh"). Point-to-point BLE central/peripheral is
  the approved transport.

## References

- HA failover sequence: `04_runtime-view/seq-ha-failover.md` (CC relay shown)
- ADR-009: CC↔Central Transport (USB-serial host bridge — uplink path)
- CC bridge firmware: `ble_qos_demo_V1.2m/src/cc_bridge.c`
- Central ingest API: `central-device-metadata/app/api/ingest.py`
- AGENTS.md: GW role (runtime QoS + roster, local authority)
- Firmware CLAUDE.md: "不使用 BLE Mesh" (BLE Mesh exclusion)
