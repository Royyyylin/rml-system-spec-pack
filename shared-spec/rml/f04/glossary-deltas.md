# Glossary Deltas — F-04: GW QoS Scheduler Tuning

> Cross-links master glossary: `shared-spec/glossary.md`
> New terms introduced in F-04 GW QoS Scheduler Deployment Tuning.

## New Terms

| Term | Definition | Canonical Location |
|---|---|---|
| `TUNE-VAL` | QoS scheduler preset parameter validation rule set (TUNE-VAL-001~006). Enforced by App (client guard) and Firmware (final guard). | `shared-spec/feature-gw-qos-scheduler-tuning.md` §Validation Rules |
| `preset` | Named QoS scheduler configuration: `balanced` / `conservative` / `aggressive`. Each has defined cutoff and interval values. | `ble_api.yaml` → presets |
| `balanced preset` | Default preset; matches current hardcode baseline. Used as boot fallback. `cutoffs: 3/5/8`, `intervals: 80/160/400/800 BLE units`. | `ble_api.yaml` → presets |
| `conservative preset` | Connection quality priority. `cutoffs: 2/4/6`, `intervals: 80/80/160/400 BLE units`. | `ble_api.yaml` → presets |
| `aggressive preset` | Concurrency priority. `cutoffs: 4/6/10`, `intervals: 80/160/400/400 BLE units`. | `ble_api.yaml` → presets |
| `expert override` | Custom cutoff/interval table provided by engineer. 16-byte CMD_V2 payload. Validated by TUNE-VAL-001~003. | `feature-gw-qos-scheduler-tuning.md` §Expert Override |
| `CMD_V2 0x07 SET_SCHED_TUNE` | BLE GATT CMD_V2 opcode for sending preset or expert override to GW. 4B (preset) or 16B (override). | `ble_api.yaml` → opcodes.0x07 |
| `TUNE-VAL reject code` | CMD_RESULT status code sent by Firmware when TUNE-VAL final guard rejects config. | `ble_api.yaml` → cmd_v2_reject_codes |
| `NVS last-known-good (LKG)` | NVS key `qos/sched_tune`: persists last accepted preset/override. Restored on boot. Falls back to balanced if corrupt. | `ble_qos_demo_V1.2m/docs/02_sdd/firmware-fw4-impl.md` |
| `gw_qos_calc_interval()` | GW firmware function computing BLE connection interval from ED count using preset step table. Hardcode audit finding #4 origin. | `src/gw_qos.c` |
| `config coupling` | Root cause of F-04: `gw_qos_calc_interval()` step table implicitly assumed `MAX_ED=8`; changing `MAX_ED` would silently break scheduling. | `feature-gw-qos-scheduler-tuning.md` §Design Rationale |

## Existing Terms Referenced

- `CMD_V2` — transaction-based command characteristic; see `glossary.md`
- `CMD_RESULT` — async result notification; see `glossary.md`
- `ENG_UNLOCK` — GATT write + PIN required for engineer mode; see `gatt_services.md`
- `FW-3A`, `FW-3B`, `FW-4`, `FW-5` — firmware spec phases; see `glossary.md` Spec ID naming

## Disambiguation

- `F-04` (feature) ≠ `FW-3A/3B/4/5` (firmware phases) — F-04 is the cross-repo feature ID; FW-3A~5 are implementation phases within firmware. See `glossary.md` §F-04 vs FW-3A disambiguation.
