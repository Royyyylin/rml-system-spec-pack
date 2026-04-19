# Context Map — FW-3A: CMD_V2 Per-Opcode Length Guard

> Wave: FW-3A (firmware spec phase)
> Source: `fw3b-cmd-v2-0x07-handler-impl.md`, `ble_api.yaml`

## Bounded Contexts

```mermaid
C4Context
    title FW-3A Bounded Contexts

    Enterprise_Boundary(fw, "Firmware Domain") {
        System(gatt, "GATT Write Handler\n(qos_service.c)", "receives CMD_V2 writes")
        System(dispatch, "cmd_v2_dispatch\n(codegen from ble_api.yaml)", "opcode lookup + length guard")
        System(result, "CMD_RESULT notifier", "BAD_LENGTH / UNKNOWN_OPCODE responses")
    }

    Enterprise_Boundary(spec, "Spec-Pack / SSOT") {
        System(yaml, "ble_api.yaml\nopcodes table", "valid_lens per opcode; source of truth")
    }

    Enterprise_Boundary(app_ctx, "App Domain") {
        System(ble, "BLE GATT Client", "writes CMD_V2; receives CMD_RESULT")
    }

    Rel(yaml, dispatch, "codegen: valid_lens per opcode")
    Rel(ble, gatt, "BLE GATT write")
    Rel(gatt, dispatch, "buf + len")
    Rel(dispatch, result, "reject decision")
    Rel(result, ble, "BLE notify CMD_RESULT")
```

## Context Relationships

| Upstream | Downstream | Relationship | Contract |
|---|---|---|---|
| `ble_api.yaml` opcodes table | `cmd_v2_dispatch.c` (codegen) | Published Language / codegen source | `valid_lens[]` per opcode; reject codes |
| `cmd_v2_dispatch.c` | `cmd_v2_ops[].handler` | Internal | Length guard must pass before handler called |
| `cmd_v2_dispatch.c` | CMD_RESULT notifier | Internal | `BAD_LENGTH 0xFF` on len mismatch |
| FW-3A dispatch infrastructure | FW-3B `0x07` handler | Prerequisite | FW-3B fills NULL slot in `cmd_v2_ops[]` |

## Anti-Corruption Layers

| Boundary | ACL Description |
|---|---|
| ble_api.yaml → codegen | Dispatch table is generated; hand-editing `cmd_v2_dispatch.c` is forbidden — edit `ble_api.yaml` only |
| GATT → dispatch | Raw GATT payload never reaches handler without length guard; guards are centralized in dispatch, not duplicated in handlers |

## Naming Disambiguation

FW-3A is a **firmware spec phase** (firmware-internal planning), not a cross-repo feature ID.
- `FW-3A` = CMD_V2 length guard infrastructure (this document)
- `FW-3B` = `0x07` SET_SCHED_TUNE handler (fills the NULL slot)
- `F-04` = cross-repo feature (GW QoS Scheduler Tuning); owner = spec-pack

See `glossary.md` §F-04 vs FW-3A disambiguation.
