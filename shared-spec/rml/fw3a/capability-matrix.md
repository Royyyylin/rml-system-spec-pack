# Capability Matrix — FW-3A: CMD_V2 Per-Opcode Length Guard

> Wave: FW-3A (firmware spec phase)
> Source: `fw3b-cmd-v2-0x07-handler-impl.md` §2 Architecture, `ble_api.yaml`

## Per-Role Capabilities

| Capability | GW Firmware | App | Central | Spec-Pack |
|---|---|---|---|---|
| CMD_V2 dispatch table codegen | **OWNS** — `src/generated/cmd_v2_dispatch.c` | — | — | — |
| Per-opcode `valid_lens[]` definition | **OWNS** — reads from `ble_api.yaml` | — | — | — |
| Length guard enforcement | **OWNS** — before any handler call | — | — | — |
| `BAD_LENGTH 0xFF` reject response | **OWNS** — via CMD_RESULT | receives | — | — |
| `UNKNOWN_OPCODE 0xFE` response | **OWNS** — for NULL handler slots | receives | — | — |
| CMD_V2 opcode registry (SSOT) | reads/derives | reads/derives | — | **OWNS** — `ble_api.yaml` opcodes table |
| 0x07 handler stub (NULL slot) | **OWNS** — placeholder for FW-3B | — | — | — |

## Guard Rules

| Opcode | Valid Lengths | Guard Action on Mismatch |
|---|---|---|
| `0x07` SET_SCHED_TUNE | 4 (preset form), 16 (expert override) | `BAD_LENGTH 0xFF` in CMD_RESULT |
| All other opcodes | per `ble_api.yaml` | `BAD_LENGTH 0xFF` |
| Any unregistered opcode | — | `UNKNOWN_OPCODE 0xFE` |

## Prerequisite Relationship

| Phase | Depends On | Provides |
|---|---|---|
| FW-3A | `ble_api.yaml` opcodes table (frozen) | dispatch table + length guard infrastructure |
| FW-3B | FW-3A (spec frozen) | 0x07 handler filling NULL slot |
| FW-4 | FW-3B (handler done) | NVS LKG + balanced boot fallback |
| FW-5 | FW-3B + FW-4 | HIL apply/reject/fallback test suite |
