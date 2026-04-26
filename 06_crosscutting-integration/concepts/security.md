# Crosscutting Concept: Security & Engineer Access Control

> arc42 §6 Crosscutting Concepts — Security
> Status: active
> Owner: spec-pack (system level)
> Last updated: 2026-04-26
> SSOT for GATT characteristics: `ble_qos_demo_V1.2m/ble_api.yaml`
> SSOT for GATT service definition: `ble_qos_demo_V1.2m/docs/current/gatt_services.md`

---

## Purpose

Defines the security architecture for the BLE QoS demo system: the ENG_UNLOCK PIN
flow, key-handling boundary, PIN rotation policy, and threat model scope.
This concept governs all repos' expectations around authentication and
access control over the GATT interface.

---

## Engineer Access Control — ENG_UNLOCK Flow

The system uses a PIN-based engineer mode unlock mechanism over BLE GATT.
Two GATT characteristics govern engineer authentication:

| Characteristic | UUID | Properties | Description |
|---|---|---|---|
| `ENG_UNLOCK` | `6f8a9c11-2c1a-4b6f-8a11-8ddc1f4e7b25` | write, write_without_response | Write PIN to request ENGINEER mode |
| `ENG_PIN_SET` | `6f8a9c12-2c1a-4b6f-8a11-8ddc1f4e7b25` | write, write_without_response | Set a new PIN (requires active ENGINEER mode) |

### Unlock Flow

```
App                         Firmware (GW/ED)
 |                               |
 |--- write ENG_UNLOCK (PIN) --->|
 |                               |-- compare PIN vs NVS "qos/pin"
 |                               |-- success: set ENGINEER mode, start 5-min timer
 |<-- (implicit: next ops succeed)|
 |                               |
 |--- write ENG_PIN_SET (newPIN)|  [only while ENGINEER mode active]
 |                               |-- validate length (4-16 ASCII digits)
 |                               |-- persist to NVS "qos/pin"
 |                               |
```

### ENGINEER Mode Session Properties

- **Expiry**: 5-minute sliding window from last authenticated write
- **Scope**: Per-connection; ENGINEER mode does NOT persist across BLE disconnect or reboot
- **Gating**: Any opcode marked `requires_eng_unlock: true` in `ble_api.yaml` checks ENGINEER mode before execution
- **Revocation**: BLE disconnect, reboot, or timeout immediately revokes ENGINEER mode

---

## PIN Specification

| Property | Value |
|---|---|
| Format | ASCII decimal digits only (0-9) |
| Length | 4 to 16 characters inclusive |
| NVS key | `qos/pin` |
| Default | Factory-set value (not hardcoded in spec — defined in firmware provisioning process) |
| Validation | Firmware rejects PIN writes where len < 4 or len > 16 or non-digit characters present |

PIN rotation requires active ENGINEER mode (chicken-and-egg solved by factory PIN).
After rotation, the new PIN is immediately effective for subsequent unlocks.

---

## Key Handling Boundary

The PIN is stored in NVS plaintext under the `qos/pin` key (Zephyr settings
subsystem, AES-CCM encrypted at-rest by the SoftDevice security manager if
`CONFIG_BT_SMP` is active).

**In-scope protections**:
- PIN never transmitted in plaintext over an unauthenticated BLE link by design
  (BLE pairing / bonding is a separate layer; see Out-of-Scope below)
- NVS key isolated from application code by Zephyr settings subsystem APIs
- PIN comparison performed in firmware only; App never receives the stored PIN

**Out-of-scope (explicit non-goals)**:
- BLE link-layer encryption (no `CONFIG_BT_SMP` enforced in demo; demo assumes
  controlled lab environment)
- PIN complexity rules beyond length (no dictionary / entropy checks)
- Central-side PIN management (Central does not know the device PIN)
- Remote PIN reset without physical access (must re-flash or boot to factory)

---

## Threat Model Edges

### In-Scope Threats

| Threat | Mitigation |
|---|---|
| Unauthorized access to engineer opcodes over BLE | ENG_UNLOCK PIN gate; 5-min session expiry |
| PIN brute-force over BLE | BLE connection drop after multiple failed writes (firmware-level rate limit, not spec-mandated count) |
| Accidental ENG opcode write by App | `requires_eng_unlock` flag in `ble_api.yaml` gated at firmware GATT handler |
| Stale ENGINEER mode after App disconnect | Mode auto-revokes on BLE disconnect |
| PIN persistence across reboot enabling offline attack | PIN persists in NVS (intentional — device needs PIN across power cycles); attack surface is physical NVS readout |

### Out-of-Scope Threats

| Threat | Rationale |
|---|---|
| BLE eavesdropping / MITM | Demo context; BLE SMP not enforced |
| Physical Flash readout | Hardware security boundary; outside BLE QoS demo scope |
| Central compromise → device PIN extraction | Central does not store or relay device PIN |
| Replay attacks on PIN write | BLE connection-layer sequence numbers; out of scope for demo |
| Multi-device PIN reuse | Devices are individually provisioned; Central does not coordinate PIN namespaces |

---

## Category F Events (SECURITY/ADMIN)

Security-related LOG events fall under Category F (SECURITY/ADMIN) in the
13-dimension event schema (see `concepts/logging.md`).

Typical Category F events from firmware:
- `ENG_UNLOCK_OK` — engineer mode granted
- `ENG_UNLOCK_FAIL` — PIN mismatch
- `ENG_SESSION_EXPIRED` — 5-min timer fired
- `PIN_CHANGED` — PIN rotation succeeded

These events are emitted at INFO severity (event_id ≤ 250) by default; repeated
`ENG_UNLOCK_FAIL` bursts escalate to WARN (event_id 251-500) at implementation
discretion.

---

## Cross-Repo Responsibilities

| Repo | Security Responsibility |
|------|------------------------|
| Firmware (`ble_qos_demo_V1.2m`) | PIN storage, ENG_UNLOCK gate, ENGINEER mode session, Category F event emission |
| App (`ble_qos_app`) | PIN entry UI, write to ENG_UNLOCK characteristic, obfuscate PIN in transit UI |
| Central (`central-device-metadata`) | No direct role; does not store or relay device PIN |
| Spec-pack | Security boundary definition (this document); `ble_api.yaml` GATT contract authority |

---

## Trace

- `REQ-FW-SEC-001` — ENG_UNLOCK gate enforced on all `requires_eng_unlock` opcodes
- `REQ-FW-SEC-002` — ENGINEER mode expires within 5 minutes of last authenticated write
- `REQ-FW-SEC-003` — ENG_PIN_SET only accepted while ENGINEER mode is active

---

## Open Questions

- Q1: Should repeated `ENG_UNLOCK_FAIL` trigger a connection drop? Currently implementation-defined; may need AC if BLE SMP is enabled in future milestones.
- Q2: PIN rotation notification to Central? Currently out of scope; Central has no PIN awareness.
