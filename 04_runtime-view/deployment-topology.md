# Deployment Topology — arc42 §7

> arc42 §7 Deployment View: physical hardware, runtime environments, BLE/IP communication paths.
> Diagram source: [`deployment-topology.d2`](deployment-topology.d2)
>
> **NCS SDK version SSOT**: `ble_qos_demo_V1.2m/scripts/dev.sh` (`NCS_HOME` default, line ~32).
> Do NOT hardcode version here; always cite `scripts/dev.sh`.

## 1. Hardware Inventory

| Node | Device | Role | Qty | Notes |
|------|--------|------|-----|-------|
| GW | nRF52833 DK | Gateway (BLE dual-role: central to ED, peripheral to App) | 1 | Flashed via `scripts/dev.sh build --gw` |
| ED-1 | nRF52833 DK | End Device (BLE peripheral sensor) | 1 | Flashed via `scripts/dev.sh build` |
| ED-2 | nRF52833 DK | End Device (BLE peripheral sensor) | 1 | Flashed via `scripts/dev.sh build` |
| CC | nRF52833 DK | Central-to-App BLE bridge | 1 | Flashed via `scripts/dev.sh build --cc` |
| App | Pixel 7a (Android 16) | Mobile client — human-facing UI | 1 | ADB SN `3A271JEHN05259` |
| Central | Mac mini (host) | Backend — FastAPI + PostgreSQL | 1 | NCS SDK path: see `scripts/dev.sh` |

### 1.1 Hardware Resource Summary

| Node | SoC | Flash | RAM | Role Constraints |
|------|-----|-------|-----|-----------------|
| GW | nRF52833 | 512 KB internal + SPI ext. | 128 KB | Dual BLE role (Central→ED, Peripheral→App); LOG ring on SPI Flash (ADR-009) |
| ED-1 / ED-2 | nRF52833 | 512 KB internal | 128 KB | Single BLE Peripheral role only |
| CC | nRF52833 | 512 KB internal | 128 KB | Single BLE Peripheral role (bridge); USB-serial to Central |

> Flash and RAM figures are hardware maximums for nRF52833 (PCA10100 DK).
> Available to application code = total − BLE stack − Zephyr kernel overhead.
> See `02_solution-strategy/constraints.md §2.2` for derived architectural limits.

---

## 2. IP Topology

### 2.1 Network Segments

```
[BLE RF segment — 2.4 GHz ISM]
  ED-1  ---BLE Coded/2M/1M---> GW
  ED-2  ---BLE Coded/2M/1M---> GW
  App   ---BLE 1M (GATT)-----> GW   (App acts as BLE central)
  App   ---BLE 1M (GATT)-----> CC   (CC bridge path)

[USB-serial segment — local, Mac mini host]
  CC    ---USB-serial (TBD)---> Mac mini / Central process
  GW    ---USB-serial (TBD)---> Mac mini / Central process

[IP segment — Wi-Fi / LTE]
  App   ---HTTPS/WebSocket----> Central (Mac mini: localhost or LAN IP)
  GW    ---HTTPS/WebSocket----> Central (Wi-Fi uplink, TBD vs USB)
```

### 2.2 IP Address Allocation (Dev Lab)

| Node | Interface | Address | Notes |
|------|-----------|---------|-------|
| Central | Wi-Fi (en0) | DHCP — dynamic (LAN) | FastAPI binds `0.0.0.0:8000` by default |
| App | Wi-Fi | DHCP — dynamic (same LAN as Central) | Must reach Central; mDNS or hardcoded LAN IP in dev |
| GW | (USB-serial, no IP) | N/A | IP uplink path TBD (OQ-2) |
| CC | (USB-serial, no IP) | N/A | Relayed via Central process (OQ-1) |

> **Dev Lab constraint**: all IP nodes must be on the same LAN subnet.
> Central's LAN IP is not fixed; App discovery relies on mDNS or manual config.
> Production topology (Wi-Fi module for GW/CC) is out of scope for this demo.

### 2.3 Protocol Stack per Link

| Link | L4 | L7 / Format | Auth |
|------|----|------------|------|
| App ↔ Central (identity / assignment) | TCP (HTTPS / TLS 1.3) | REST JSON | JWT (TBD) |
| App ↔ Central (real-time) | TCP (WebSocket) | JSON / CBOR event stream | JWT (TBD) |
| GW ↔ Central (telemetry uplink) | TCP (WebSocket) | JSON telemetry batch | mTLS (TBD) |
| CC ↔ Central (bridge relay) | USB-serial or TCP | raw BLE PDU relay (TBD) | session token (TBD) |
| ED ↔ GW (BLE) | BLE LL | GATT over ATT; CMD_V2, STATUS, METRICS, EVT | BLE SMP pairing |
| App ↔ GW (BLE GATT) | BLE LL | GATT over ATT; CMD_V2, CAPS_V2, STATUS | BLE SMP pairing |

---

## 3. Communication Links

### 3.1 BLE Physical Layer

| Link | PHY Modes | Topology | Notes |
|------|-----------|----------|-------|
| ED ↔ GW | 1M / 2M / Coded (S8/S2) | BLE Central (GW) + Peripheral (ED) | PHY selected by QoS Zone (NEAR/MID/FAR/EDGE) |
| App ↔ GW | 1M (default) | BLE Peripheral GATT — GW is peripheral, App is central | App reads STATUS, METRICS, RSSI; writes CMD_V2 |
| App ↔ CC | 1M (default) | BLE Peripheral GATT — CC is peripheral, App is central | CC bridges App commands to Central via USB/IP |

### 3.2 IP / Transport Layer

| Link | Protocol | Transport | Notes |
|------|----------|-----------|-------|
| CC ↔ Central | WebSocket or HTTP | USB-serial or host BLE (TBD: see Open Questions §6) | CC relays App BLE session to Central |
| App ↔ Central | HTTPS / WebSocket | Mobile data or Wi-Fi | App reconciliation, assignment sync, alias sync |
| GW ↔ Central | HTTPS / WebSocket | Wi-Fi or USB-to-host (TBD) | Telemetry uplink, roster sync |

---

## 4. Build Environment

### 4.1 NCS Toolchain

**NCS SDK version SSOT**: `ble_qos_demo_V1.2m/scripts/dev.sh` — `NCS_HOME` default, line ~32.

The dev script (`scripts/dev.sh`) manages the full NCS toolchain lifecycle:

| Function | `dev.sh` sub-command | What it does |
|----------|---------------------|--------------|
| Build firmware | `scripts/dev.sh build [--gw\|--cc]` | Runs `west build` with board `nrf52833dk_nrf52833`; role set via Kconfig overlay |
| Flash DK | `scripts/dev.sh flash [--gw\|--cc]` | Invokes `nrfjprog --program` with correct hex, then reset |
| RTT logging | `scripts/dev.sh rtt [--gw\|--cc]` | Opens JLinkRTTClient for live kernel log stream |
| Clean build | `scripts/dev.sh clean` | Removes `build/` directory |
| Toolchain check | `scripts/dev.sh check-env` | Verifies `NCS_HOME`, `ZEPHYR_BASE`, and toolchain bundle hash |

> `ZEPHYR_BASE` is derived from `NCS_HOME` by `scripts/dev.sh` (`$NCS_HOME/zephyr`).
> The toolchain bundle hash for the current NCS version is resolved at runtime by `dev.sh`.
> **Never hardcode the bundle hash or NCS version in any other file.**

### 4.2 Toolchain Bundle Resolution

`scripts/dev.sh` maps the NCS installation path to a Zephyr SDK toolchain bundle ID at runtime
(see the `case` statement inside `dev.sh` for the version-to-bundle mapping).
This means: (a) adding a new NCS version only requires updating `dev.sh`, not any doc;
(b) docs MUST cite `scripts/dev.sh`, not copy bundle hash values.

### 4.3 Unit Test Sandbox

| Tool | Command | Purpose |
|------|---------|---------|
| Docker | `scripts/run_unit_tests.sh` | Hermetic C unit tests — no DK required |
| Image | `ble-qos-test` (local build) | Zephyr native POSIX target + Unity framework |
| Coverage | `gcov` + `lcov` | Line coverage gate (≥ 80% for Railway / Medical profiles) |

### 4.4 Mobile Automation

| Tool | Target | Notes |
|------|--------|-------|
| `mobile-mcp` | Pixel 7a — ADB SN `3A271JEHN05259` | Automated UI interaction and screenshot verification |
| `adb` | Android 16 | Must be in PATH; `mobile-mcp` wraps it |
| Flutter SDK | `ble_qos_app/pubspec.yaml` | Version SSOT; `dev.sh` does NOT manage Flutter |

---

## 5. DK Boot and Flash Procedure

### 5.1 First-Time Setup

1. Install NCS SDK to `$HOME/ncs/` — version per `scripts/dev.sh` `NCS_HOME` default.
2. Verify environment: `scripts/dev.sh check-env` (must print `OK` for all checks).
3. Connect all 4 DK boards via USB; verify with `nrfjprog --ids` (should list 4 SNs).

### 5.2 Per-Role Flash Sequence

```
# GW (1x board)
scripts/dev.sh build --gw
scripts/dev.sh flash --gw

# ED-1 and ED-2 (2x boards — repeat for each)
scripts/dev.sh build
scripts/dev.sh flash

# CC (1x board)
scripts/dev.sh build --cc
scripts/dev.sh flash --cc
```

> Role assignment is baked in at build time via Kconfig overlay;
> runtime role can be read from NVS (`NVS_ROLE_*` enum — see ubiquitous-language.md).

### 5.3 RTT Logging

RTT (Real-Time Transfer) is the primary debug channel for all DK boards during development:

```
# Open RTT log for GW
scripts/dev.sh rtt --gw

# Open RTT log for ED (first detected board)
scripts/dev.sh rtt
```

The RTT client connects via J-Link OB (on-board debugger, PCA10100); no external J-Link needed.
Output includes Zephyr kernel log (`LOG_MODULE_REGISTER` output) and BLE stack events.

### 5.4 Post-Flash Verification

| Check | Method | Expected result |
|-------|--------|----------------|
| GW advertising | RTT (`scripts/dev.sh rtt --gw`) | RTT shows `BLE adv started` |
| ED connecting | RTT (GW side) | `ED peer connected` log entry |
| App pairing | App UI | "Connected" status on device list screen |
| Central API | `curl http://localhost:8000/health` | `{"status":"ok"}` |

---

## 6. Open Questions

| # | Question | Owner |
|---|----------|-------|
| OQ-1 | CC↔Central transport: USB-serial vs host-side BLE relay — final decision pending | firmware + central |
| OQ-2 | GW↔Central uplink path: USB-serial vs Wi-Fi direct — final decision pending | firmware + central |
| OQ-3 | Central LAN IP discovery: mDNS vs manual config vs env var — affects App build config | app + central |

---

## 7. Cross-references

- Building blocks: `03_building-blocks/`
- Wire / GATT: `ble_qos_demo_V1.2m/ble_api.yaml` (SSOT)
- Ubiquitous language: `01_context-scope/ubiquitous-language.md`
- QoS Zones: `ble_qos_demo_V1.2m/.claude/rules/qos-zones.md`
- Runtime sequences: `04_runtime-view/seq-*.md`
- Architecture constraints (hardware limits): `02_solution-strategy/constraints.md §2.2`
- NCS SDK version SSOT: `ble_qos_demo_V1.2m/scripts/dev.sh` (`NCS_HOME` line ~32)
