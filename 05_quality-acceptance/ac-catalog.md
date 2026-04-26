# AC Catalog — Cross-Repo Acceptance Criteria Index

> Status: active
> Last updated: 2026-04-19
> Owner: spec-pack (system level)
> Source repos: ble_qos_demo_V1.2m (firmware), ble_qos_app (app), central-device-metadata (central)

## Purpose

Central index of all acceptance criteria across repositories.
Machine-greppable: each AC row maps to exactly one REQ and one owner repo.
AC IDs follow the pattern `AC-<DOMAIN>-<FEATURE>-<NNN>`.

## Domain Prefix Registry

| Prefix | Domain | Owner Repo | REQ prefix |
|---|---|---|---|
| `FW` | Firmware (NCS/Zephyr) | `ble_qos_demo_V1.2m` | `REQ-FW-*` |
| `A` | App (Flutter/Dart) | `ble_qos_app` | `REQ-A-*` |
| `C` | Central (FastAPI/Python) | `central-device-metadata` | `REQ-C-*` |
| `S` | System/Spec-pack (cross-repo contract) | `rml-system-spec-pack` | `REQ-S-*` |
| `X` | Cross-repo (multiple owners) | — | `REQ-X-*` |

## AC Catalog

### Firmware — FW-3A CMD_V2 Length Guard

Spec ref: `--base-dir/docs/specs/fw-3a-cmd-v2-length-guard.md`

| AC ID | REQ | Description | Owner Repo | Status | TC count |
|---|---|---|---|---|---|
| AC-FW-3A-001 | REQ-FW-3A-001 | Valid opcode + matching len dispatches and returns SUCCESS v0=0x00 | firmware | active | 1 |
| AC-FW-3A-002 | REQ-FW-3A-001 | Mismatched len returns REJECTED v0=0xFF, no dispatch | firmware | active | 1 |
| AC-FW-3A-003 | REQ-FW-3A-002 | L1 ATT: len < 2 returns BT_ATT_ERR_INVALID_ATTRIBUTE_LEN, no CMD_RESULT | firmware | active | 1 |
| AC-FW-3A-004 | REQ-FW-3A-002 | L2 Dispatcher: unknown opcode returns REJECTED v0=0xFE | firmware | active | 1 |
| AC-FW-3A-005 | REQ-FW-3A-003 | Codegen: re-running gen_cmd_v2_dispatch.py produces identical header (idempotent); string total_bytes causes pipeline fail | firmware | active | 2 |
| AC-FW-3A-006 | REQ-FW-3A-004 | App reads CAPS_V2 on connect and triggers re-read on Service Changed indication | app | active | 1 |
| AC-FW-3A-007 | REQ-FW-3A-004 | App triggers re-read on DB hash mismatch or FW version change | app | active | 2 |
| AC-FW-3A-008 | REQ-FW-3A-005 | Second async CMD_V2 while first in-flight returns REJECTED v0=0xFD (BUSY) | firmware | active | 1 |
| AC-FW-3A-009 | REQ-FW-3A-006 | Stale txn_id in CMD_RESULT discarded by App without UI update | app | active | 1 |
| AC-FW-3A-010 | REQ-FW-3A-007 | App times out after 10 000 ms; 1 retry with dedup on same txn_id | app | active | 2 |

### Firmware — F-04 GW QoS Scheduler Tuning (Firmware Side)

Spec ref: `rml-system-spec-pack/03_building-blocks/F-04-gw-qos-scheduler-tuning/tuning.md`

| AC ID | REQ | Description | Owner Repo | Status | TC count |
|---|---|---|---|---|---|
| AC-F-04-001 | REQ-F-04-001 | Valid preset index via CMD_V2 0x07 applied within 1 scan cycle | firmware | active | 1 |
| AC-F-04-002 | REQ-F-04-001 | Out-of-range preset index returns REJECTED v0=0xFF, policy unchanged | firmware | active | 1 |
| AC-F-04-003 | REQ-F-04-002 | Invalid TUNE-VAL expert override rejected by Firmware final guard; last-known-good preserved | firmware | pending_impl | 0 |
| AC-F-04-004 | REQ-F-04-002 | TUNE-VAL-001 violation (cutoffs not strictly increasing) → REJECTED v0=rule_idx=1 | firmware | pending_impl | 0 |
| AC-F-04-005 | REQ-F-04-002 | TUNE-VAL-003 violation (interval out of BLE range 6–3200) → REJECTED v0=rule_idx=3 | firmware | pending_impl | 0 |
| AC-F-04-006 | REQ-F-04-003 | Boot with no valid config → fallback to balanced preset without panic | firmware | pending_impl | 0 |

### App — A-1 QoS Telemetry Schema

Spec ref: `rml-system-spec-pack/03_building-blocks/F-04-gw-qos-scheduler-tuning/extension-boundary.md`

| AC ID | REQ | Description | Owner Repo | Status | TC count |
|---|---|---|---|---|---|
| AC-A-1-001 | REQ-A-1-001 | QosTelemetryModel parses valid BLE notify payload with all telemetry fields | app | pending_impl | 0 |
| AC-A-1-002 | REQ-A-1-001 | QosTelemetryModel uses null/default for missing optional fields without throwing | app | pending_impl | 0 |

### App — App-Spec RML Functional Requirements

Spec ref: `rml-system-spec-pack/app-spec/acceptance_criteria.md`

| AC ID | REQ | Description | Owner Repo | Status | TC count |
|---|---|---|---|---|---|
| AC-APP-001 | REQ-001 | Telemetry display: sparse→`--`, stale→last value + hint, unknown→`--` | app | active | 2 |
| AC-APP-002 | REQ-002 | Capability gate: CAPS_V2 present → CAPS_V2; absent → CAP fallback; undeclared capabilities not operable | app | active | 1 |
| AC-APP-003 | REQ-003 | stableId as primary key; MAC labelled as transport identity; Central requests use central_ref | app | active | 1 |
| AC-APP-004 | REQ-004, REQ-008 | Assignment reconciliation: dual gateway + badge on mismatch; badge clears on convergence; conflict only when can_compare=true | app | active | 2 |
| AC-APP-005 | REQ-005 | Alias precedence: local_pending > central > cached > DEVICE_ALIAS > adv_name; 409 does not overwrite pending | app | active | 2 |
| AC-APP-006 | REQ-006 | CMD_V2 round-trip: non-zero txn_id; SUCCESS/REJECTED mapped to UI; timeout after configured duration; no silent retry on REJECTED | app | active | 3 |
| AC-APP-007 | REQ-007 | Freshness evidence traceable to owner repo source_timestamp or equivalent; no fake freshness when evidence unavailable | app | active | 0 |

### Central — W26A Failback Command Service

Spec ref: `central-device-metadata/docs/specs/failback-command-service-spec.md`

| AC ID | REQ | Description | Owner Repo | Status | TC count |
|---|---|---|---|---|---|
| AC-W26A-001 | REQ-W26A-001 | hold_down_active raises FailbackIneligibleError with reason, original_gw_id, hold_down_remaining_seconds | central | active | 1 |
| AC-W26A-002 | REQ-W26A-001 | original_gw_unhealthy also raises FailbackIneligibleError | central | active | 1 |
| AC-W26A-003 | REQ-W26A-001 | orchestrator.assign_override() NOT called when ineligible | central | active | 1 |
| AC-W26A-004 | REQ-W26A-001 | Eligible device calls orchestrator with decision_type="failback", target_gw_id, ed_id, initiated_by | central | active | 1 |
| AC-W26A-005 | REQ-W26A-001 | Returns dict with outcome="failback_executed", ed_id, original_gw_id, decision_id | central | active | 1 |
| AC-W26A-006 | REQ-W26A-002 | viewer role → HTTP 403 | central | active | 1 |
| AC-W26A-007 | REQ-W26A-002 | FailbackIneligibleError → HTTP 422 with "ineligible" body | central | active | 1 |
| AC-W26A-008 | REQ-W26A-002 | hold_down 422 body includes hold_down_remaining_seconds | central | active | 1 |
| AC-W26A-009 | REQ-W26A-002 | Eligible device → HTTP 200 with outcome="failback_executed", ed_id, decision_id | central | active | 1 |
| AC-W26A-010 | REQ-W26A-002 | admin role → HTTP 200 | central | active | 1 |

### Central — C-2 QoS Tuning Integration Tests

Spec ref: `central-device-metadata/docs/specs/c2-integration-test-qos-tuning.md`

| AC ID | REQ | Description | Owner Repo | Status | TC count |
|---|---|---|---|---|---|
| AC-C2-001 | REQ-C-04-001 | TUNE-VAL-001 hard reject (cutoffs not increasing) → 422, rule_id=TUNE-VAL-001, DB row not created | central | active | 1 |
| AC-C2-002 | REQ-C-04-001 | TUNE-VAL-003 hard reject (interval out of BLE range) → 422, DB row not created | central | active | 1 |
| AC-C2-003 | REQ-C-04-001 | TUNE-VAL-006 warning save (non-decreasing violation) → 200, warnings list in response, DB row saved | central | active | 1 |
| AC-C2-004 | REQ-C-04-001 | Cross-GW isolation: PUT on GW-A does not affect GW-B row | central | active | 1 |
| AC-C2-005 | REQ-C-04-001 | Concurrent PUT race condition: final revision=2 after two simultaneous PUTs (FOR UPDATE serialised) | central | active | 1 |
| AC-C2-006 | REQ-C-04-001 | Audit log written in same transaction as PUT; revision incremented | central | active | 1 |
| AC-C2-007 | REQ-C-04-001 | Unknown gw_id → 404 (Postgres, not SQLite) | central | active | 1 |
| AC-C2-008 | REQ-C-04-001 | GET with no tuning row → 200 with preset="balanced", effective_table matches PRESET_TABLES["balanced"] | central | active | 1 |

## Summary Statistics

### By Repo

| Repo | Active | Pending impl | Total |
|---|---|---|---|
| firmware (`ble_qos_demo_V1.2m`) | 10 | 6 | 16 |
| app (`ble_qos_app`) | 8 | 2 | 10 |
| central (`central-device-metadata`) | 18 | 0 | 18 |
| **Total** | **36** | **8** | **44** |

### Coverage Gap

| Category | Count |
|---|---|
| AC with TC (covered) | 32 |
| AC without TC (gap) | 12 |
| AC w/o TC rate | 27% |

**ACs without TC (gap list):**
- AC-F-04-003, AC-F-04-004, AC-F-04-005, AC-F-04-006 (firmware F-04 pending_impl)
- AC-A-1-001, AC-A-1-002 (app telemetry model pending_impl)
- AC-APP-007 (freshness evidence — TC pending)
- AC-FW-3A-003, AC-FW-3A-004 (FW-3A L1/L2 reject — TC IDs defined in spec, not yet in trace_map.yaml)
- AC-FW-3A-005 (codegen idempotent — TC IDs defined in spec, not yet in trace_map.yaml)
- AC-FW-3A-006, AC-FW-3A-007 (CAPS_V2 cache — TC IDs defined in spec, not yet in trace_map.yaml)

> Note: AC-FW-3A-003 through AC-FW-3A-010 have TC IDs in the FW-3A spec's trace map section
> but are not yet entered in `--base-dir/docs/trace_map.yaml`. Phase B trace integration
> sub-agent should populate those entries.

## References

- FW-3A spec: `--base-dir/docs/specs/fw-3a-cmd-v2-length-guard.md`
- F-04 spec: `rml-system-spec-pack/03_building-blocks/F-04-gw-qos-scheduler-tuning/tuning.md`
- App-spec ACs: `rml-system-spec-pack/app-spec/acceptance_criteria.md`
- W26A failback spec: `central-device-metadata/docs/specs/failback-command-service-spec.md`
- C-2 integration spec: `central-device-metadata/docs/specs/c2-integration-test-qos-tuning.md`
- Trace map: `--base-dir/docs/trace_map.yaml`
- TC matrix: `rml-system-spec-pack/05_quality-acceptance/tc-matrix.md`
- Trace strategy: `rml-system-spec-pack/06_crosscutting-integration/cross-repo-trace-strategy.md`
