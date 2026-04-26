# Deployment Topology — arc42 §7

> arc42 §7 Deployment View: physical hardware, runtime environments, BLE/IP communication paths.
> Diagram source: [`deployment-topology.d2`](deployment-topology.d2)

## 1. Hardware Inventory

| Node | Device | Role | Qty | Notes |
|------|--------|------|-----|-------|
| GW | nRF52833 DK | Gateway (BLE dual-role: central to ED, peripheral to App) | 1 | Flashed via `scripts/dev.sh build --gw` |
| ED | nRF52833 DK | End Device (BLE peripheral sensor) | 2 | Flashed via `scripts/dev.sh build` |
| CC | nRF52833 DK | Central-to-App BLE bridge | 1 | Flashed via `scripts/dev.sh build --cc` |
| App | Pixel 7a (Android 16) | Mobile client — human-facing UI | 1 | ADB SN 3A271JEHN05259 |
| Central | Mac mini (host) | Backend — FastAPI + PostgreSQL | 1 | NCS SDK path: see `scripts/dev.sh` |

**NCS SDK version SSOT**: `scripts/dev.sh` (`NCS_HOME` default, line ~32). Do NOT hardcode version here.

## 2. Communication Links

### BLE Physical Layer

| Link | PHY Modes | Topology | Notes |
|------|-----------|----------|-------|
| ED ↔ GW | 1M / 2M / Coded (S8/S2) | BLE Central (GW) + Peripheral (ED) | PHY selected by QoS Zone (NEAR/MID/FAR/EDGE) |
| App ↔ GW | 1M (default) | BLE Peripheral GATT — GW is peripheral, App is central | App reads STATUS, METRICS, RSSI; writes CMD_V2 |
| App ↔ CC | 1M (default) | BLE Peripheral GATT — CC is peripheral, App is central | CC bridges App commands to Central via USB/IP |

### IP / Transport Layer

| Link | Protocol | Transport | Notes |
|------|----------|-----------|-------|
| CC ↔ Central | WebSocket or HTTP | USB-serial or host BLE (TBD: see Open Questions §4) | CC relays App BLE session to Central |
| App ↔ Central | HTTPS / WebSocket | Mobile data or Wi-Fi | App reconciliation, assignment sync, alias sync |
| GW ↔ Central | HTTPS / WebSocket | Wi-Fi or USB-to-host (TBD) | Telemetry uplink, roster sync |

## 3. Dev Environment

| Tool | Purpose | Reference |
|------|---------|-----------|
| `scripts/dev.sh` | Build / flash / RTT log — ALWAYS use this, never direct cmake/ninja | `ble_qos_demo_V1.2m/scripts/dev.sh` |
| Docker (unit tests) | `docker run --rm -v $(pwd):/workspace ble-qos-test` | `scripts/run_unit_tests.sh` |
| mobile-mcp (Android) | Automated App UI control and screenshot verification | ADB SN `3A271JEHN05259` |
| nrfjprog / nrfutil | Flash and RTT — invoked by `dev.sh`, not directly | Auto-detected by `dev.sh` |

## 4. Open Questions

| # | Question | Owner |
|---|----------|-------|
| OQ-1 | CC↔Central transport: USB-serial vs host-side BLE relay — TBD | firmware + central |
| OQ-2 | GW↔Central uplink path: USB-serial vs Wi-Fi direct — TBD | firmware + central |

## 5. Cross-references

- Building blocks: `03_building-blocks/`
- Wire / GATT: `ble_qos_demo_V1.2m/ble_api.yaml` (SSOT)
- Ubiquitous language: `01_context-scope/ubiquitous-language.md`
- QoS Zones: `ble_qos_demo_V1.2m/.claude/rules/qos-zones.md`
- Runtime sequences: `04_runtime-view/seq-*.md`
