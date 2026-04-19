# Capability Matrix — F-04: GW QoS Scheduler Tuning

> Feature: F-04 GW QoS Scheduler Deployment Tuning
> Source: `capability-ownership.md` RML-CAP-006, `feature-gw-qos-scheduler-tuning.md`

## Per-Role Capabilities

| Capability | GW | ED | CC | App | Central | Spec-Pack |
|---|---|---|---|---|---|---|
| TUNE-VAL schema definition | consumes | — | — | consumes | consumes | **OWNS** |
| Preset definitions (balanced/conservative/aggressive) | **executes** | — | — | displays | stores | **DEFINES** |
| CMD_V2 0x07 wire encoding | **OWNS** — opcode handler | — | — | sends | — | defines contract |
| Client-side TUNE-VAL validation | — | — | — | **OWNS** — UX guard | — | — |
| Final TUNE-VAL validation guard | **OWNS** — reject + CMD_RESULT | — | — | — | — | — |
| Config storage + audit + revision | — | — | — | — | **OWNS** | — |
| ENG_UNLOCK role gating | **verifies** — PEER_ROLE | — | — | **OWNS** — PIN UX | — | — |
| NVS last-known-good fallback | **OWNS** — FW-4 | — | — | — | — | — |
| Balanced preset boot fallback | **OWNS** — FW-4 | — | — | — | — | — |
| CMD_RESULT feedback to App | **OWNS** — sends | — | — | displays | — | — |
| HIL apply/reject/fallback tests | **target** — FW-5 | — | — | — | — | — |

## TUNE-VAL Rules (Schema Cross-Ref)

| Rule ID | Description | Enforcer |
|---|---|---|
| `TUNE-VAL-001` | Cutoffs strictly increasing: `c1 < c2 < c3` | App (UX) + Firmware (final guard) |
| `TUNE-VAL-002` | All cutoffs positive integers (≥ 1) | App (UX) + Firmware |
| `TUNE-VAL-003` | All intervals within BLE spec range: `6 ≤ interval ≤ 3200` | App (UX) + Firmware |
| `TUNE-VAL-004` | Invalid override cannot be saved — App red error, Save disabled | App only |
| `TUNE-VAL-005` | Firmware must reject invalid config via CMD_RESULT with reason | Firmware only |
| `TUNE-VAL-006` | Intervals non-decreasing (`i1 ≤ i2 ≤ i3 ≤ i4`) — warning, not hard reject | App warning |

## Must Not Violate

| Actor | Prohibited Action |
|---|---|
| App | Save/Apply without TUNE-VAL validation passing |
| Central | Persist invalid config without validation |
| GW Firmware | Silently apply invalid values or self-originate config truth |
| Any | Treat Central config truth as first-hand runtime truth |
