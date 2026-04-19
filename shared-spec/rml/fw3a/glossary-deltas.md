# Glossary Deltas — FW-3A: CMD_V2 Per-Opcode Length Guard

> Cross-links master glossary: `shared-spec/glossary.md`
> New terms introduced in FW-3A CMD_V2 Per-Opcode Length Guard.

## New Terms

| Term | Definition | Canonical Location |
|---|---|---|
| `cmd_v2_dispatch` | Codegen-produced dispatch table for CMD_V2 opcodes. Maps opcode → `{valid_lens[], handler}`. Generated from `ble_api.yaml`. | `src/generated/cmd_v2_dispatch.c` |
| `cmd_v2_ops[]` | Array of `struct cmd_v2_op` entries, one per registered opcode. Each entry has `opcode`, `valid_lens[]`, and `handler` function pointer. | `src/generated/cmd_v2_dispatch.c` |
| `valid_lens[]` | Array of valid payload lengths for a CMD_V2 opcode. Defined in `ble_api.yaml` opcodes table. Checked before handler is called. | `ble_api.yaml` → opcodes |
| `BAD_LENGTH 0xFF` | CMD_RESULT reject code sent when received CMD_V2 payload length is not in `valid_lens[]`. | `ble_api.yaml` → cmd_v2_reject_codes |
| `UNKNOWN_OPCODE 0xFE` | CMD_RESULT reject code sent when opcode is not registered or handler is NULL. | `ble_api.yaml` → cmd_v2_reject_codes |
| `NULL handler slot` | An entry in `cmd_v2_ops[]` with `handler=NULL`. Opcode is length-guarded but not yet implemented. `0x07` is NULL at FW-3A end. | `cmd_v2_dispatch.c` (FW-3A state) |
| `FW-3A spec frozen` | Milestone: FW-3A dispatch table + length guard fully implemented and spec document locked. Prerequisite for FW-3B to start. | `fw3b-cmd-v2-0x07-handler-impl.md` §1 |

## Existing Terms Referenced

- `CMD_V2` — transaction-based command characteristic; see `glossary.md`
- `CMD_RESULT` — async response via BLE GATT notify; see `glossary.md`
- `txn_id` — transaction ID field in CMD_V2 payload and CMD_RESULT response; see `ble_api.yaml`
- `ble_api.yaml` — firmware SSOT for wire/GATT contract; see `glossary.md`

## Disambiguation

- `cmd_v2_dispatch.c` is **codegen** — it must not be hand-edited. Edit `ble_api.yaml` to change opcode registration or `valid_lens`.
- FW-3A leaves `0x07` as NULL slot intentionally — FW-3B fills it. The NULL slot is not a bug; it reflects the phased implementation plan.
