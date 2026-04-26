# ADR-009: CC↔Central Transport — USB-Serial Host Bridge

Status: accepted
Date: 2026-04-26
Decided by: Roy (K4 OQ resolution, resolves F7-OQ1)
Resolves: F7-OQ1 — was: USB-serial vs host-side BLE relay TBD

## Context

The CC bridge firmware (NVS_ROLE_CC = 0x04) runs on nRF52833 DK. Its role is purely
transport: it scans for GW by name prefix "FGW", connects via BLE, subscribes to
GATT notifications (RSSI / STATUS / METRICS / EVT), and forwards received data to a
registered `cc_bridge_data_cb_t` callback.

The open question was: how does the CC-side host process deliver that callback data to
Central? Two candidates were identified:

1. **USB-serial (UART over USB-CDC)**: CC DK sends raw structured bytes over USB-serial
   to a host process (Python/Go daemon on Mac mini). The host process decodes the wire
   format and POSTs JSON to Central's `/ingest` REST API.

2. **Host-side BLE relay**: The host machine itself runs a BLE GATT client (no CC DK
   involved), relays data directly to Central over TCP/HTTP. No dedicated CC hardware.

Central's existing API already has a REST `/ingest` surface (`app/api/ingest.py`)
receiving `QosStatusIngest`, `QosEventIngest`, `HaHeartbeatIngest`, `P1MetricsIngest`,
and `FailoverEventIngest` schemas. The gateway auth path uses `get_current_gateway`.

The CC bridge source (`src/cc_bridge.c`, `src/cc_bridge.h`) implements the BLE central
role as a **strategy-pattern injectable backend** — explicitly designed for testability
without a real BLE stack. This design assumes there is a host-side process decoding
the CC output, not that the host runs BLE directly.

For prototype stage (4× nRF52833 DK on lab bench, Mac mini host), USB-serial provides:
- Zero host BLE driver dependency (macOS BlueZ limitations avoided)
- Shared hardware with RTT log debugger (same USB connection)
- Simple framing: SLIP or length-prefix over CDC-ACM

## Decision

CC↔Central transport = **USB-serial host bridge** (CDC-ACM UART over USB), with a
host-side daemon that decodes CC output frames and POSTs to Central `/ingest` REST API
using the existing `gateway_id`-authenticated endpoint.

The CC DK outputs structured frames via USB-serial (SLIP-framed or length-prefixed
binary matching `cc_bridge_data_cb_t` payload types). The host daemon maps these to
Central ingest schema and POST to `http://localhost:<port>/ingest/*`.

Wi-Fi direct from CC DK is deferred to a future production variant when the hardware
platform includes a wireless uplink module. It is NOT adopted in the prototype.

## Consequences

**Positive:**
- No new host BLE driver dependency — USB-CDC works out of the box on macOS/Linux
- Consistent with existing CC firmware architecture (cc_bridge injectable backend)
- Reuses Central's authenticated `/ingest` REST surface with no schema changes
- Host daemon can be a single Python script alongside Central's FastAPI process

**Negative:**
- Requires USB cable between CC DK and host — not wireless in prototype
- Host daemon is an additional process to manage (startup, crash recovery)
- USB-serial framing protocol must be specified in a follow-on spec task (F7 scope)

**Trigger for re-evaluation:**
When CC hardware platform gains Wi-Fi module (production BOM change), revisit
transport to eliminate USB dependency. This ADR covers prototype only.

## Alternatives

- **Host-side BLE relay (no CC DK)**: Rejected. macOS BlueZ not available;
  CoreBluetooth is sandboxed for non-App-Store apps; Central runs on Mac mini
  without guaranteed BLE adapter. Also removes ability to test CC firmware behavior.
- **Wi-Fi direct from CC DK**: Rejected for prototype. nRF52833 has no Wi-Fi radio.
  Would require nRF9160 SiP or external ESP32 module — not in current BOM.
- **WebSocket tunnel over USB**: Over-engineered for prototype. REST POST per event
  is simpler and already validated by Central's test suite.

## References

- CC bridge firmware: `ble_qos_demo_V1.2m/src/cc_bridge.c`, `cc_bridge.h`
- Central ingest API: `central-device-metadata/app/api/ingest.py`
- AGENTS.md: CC bridge role definition (transport only, NOT authority)
- F7 deployment topology: `04_runtime-view/deployment-topology.md`
- ADR-008: Task A Completion Strategy (Phase 4 K scope)
