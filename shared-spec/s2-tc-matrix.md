# S-2 TC Matrix — Cross-Repo Test Case Mapping

> Status: active
> Last updated: 2026-04-19
> Owner: spec-pack (system level)
> Companion: S-1 AC Catalog (`s1-ac-catalog.md`), Trace map (`--base-dir/docs/trace_map.yaml`)

## Purpose

Maps every test case to its AC, test file, test function name, runner, and current status.
Machine-greppable: TC IDs follow pattern `TC-<DOMAIN>-<FEATURE>-<NNN><letter>`.

## Runner Legend

| Runner | Description | Trigger |
|---|---|---|
| unit-twister | Zephyr Twister C unit tests | `west twister` in CI |
| unit-pytest | Python pytest unit tests | `pytest tests/unit/` in CI |
| integration-pytest | Python pytest integration tests (real Postgres) | `pytest -m integration` when `TEST_DATABASE_URL` set |
| e2e-maestro | Android Maestro UI tests on Pixel 7a | `maestro test` in CI |
| hil-twister | Hardware-in-loop Twister (mac-mini-hil-runner) | manual / scheduled HIL CI |
| manual | Manual test (no automated runner yet) | human execution |

## Status Legend

| Status | Meaning |
|---|---|
| GREEN | Test exists and passes in CI |
| RED | Test exists but fails (spec_pending or impl bug) |
| spec_pending | Test written as RED, waiting for impl to turn GREEN |
| not_implemented | TC defined in spec but test file not yet created |
| TBD | TC placeholder — test design not yet started |

## TC Matrix

### Firmware — FW-3A CMD_V2 Length Guard

Source spec: `--base-dir/docs/specs/fw-3a-cmd-v2-length-guard.md`

| TC ID | AC | Test File (repo-relative) | Test Name | Runner | Status |
|---|---|---|---|---|---|
| TC-FW-3A-001a | AC-FW-3A-001 | `ble_qos_demo_V1.2m/tests/unit/uplink_dispatch/src/test_dispatch_drain.c` | `test_drain_basic` | unit-twister | TBD |
| TC-FW-3A-001b | AC-FW-3A-002 | `ble_qos_demo_V1.2m/tests/unit/uplink_dispatch/src/test_dispatch_drain.c` | `test_drain_overrun_rejected` | unit-twister | TBD |
| TC-FW-3A-002a | AC-FW-3A-003 | `ble_qos_demo_V1.2m/tests/unit/cmd_v2/test_dispatch.c` | `test_att_len_too_short_no_cmd_result` | unit-twister | not_implemented |
| TC-FW-3A-002b | AC-FW-3A-004 | `ble_qos_demo_V1.2m/tests/unit/cmd_v2/test_dispatch.c` | `test_unknown_opcode_rejected_0xfe` | unit-twister | not_implemented |
| TC-FW-3A-002c | AC-FW-3A-002 | `ble_qos_demo_V1.2m/tests/unit/cmd_v2/test_dispatch.c` | `test_length_mismatch_rejected_0xff` | unit-twister | not_implemented |
| TC-FW-3A-003a | AC-FW-3A-005 | `ble_qos_demo_V1.2m/tools/codegen/tests/test_gen_cmd_v2_dispatch.py` | `test_codegen_idempotent` | unit-pytest | not_implemented |
| TC-FW-3A-003b | AC-FW-3A-005 | `ble_qos_demo_V1.2m/tools/codegen/tests/test_gen_cmd_v2_dispatch.py` | `test_string_total_bytes_rejected` | unit-pytest | not_implemented |
| TC-FW-3A-004a | AC-FW-3A-006 | `ble_qos_app/test/ble/caps_v2_service_test.dart` | `test_service_changed_triggers_caps_reread` | e2e-maestro | not_implemented |
| TC-FW-3A-004b | AC-FW-3A-007 | `ble_qos_app/test/ble/caps_v2_service_test.dart` | `test_db_hash_mismatch_triggers_reread` | e2e-maestro | not_implemented |
| TC-FW-3A-004c | AC-FW-3A-007 | `ble_qos_app/test/ble/caps_v2_service_test.dart` | `test_fw_version_change_triggers_reread` | e2e-maestro | not_implemented |
| TC-FW-3A-005a | AC-FW-3A-008 | `ble_qos_demo_V1.2m/tests/unit/cmd_v2/test_dispatch.c` | `test_concurrent_async_rejected_0xfd` | unit-twister | not_implemented |
| TC-FW-3A-006a | AC-FW-3A-009 | `ble_qos_app/test/ble/cmd_v2_service_test.dart` | `test_stale_txn_id_discarded` | e2e-maestro | not_implemented |
| TC-FW-3A-007a | AC-FW-3A-010 | `ble_qos_app/test/ble/cmd_v2_service_test.dart` | `test_cmd_v2_timeout_10s` | e2e-maestro | not_implemented |
| TC-FW-3A-007b | AC-FW-3A-010 | `ble_qos_app/test/ble/cmd_v2_service_test.dart` | `test_dedup_on_retry_same_txn_id` | e2e-maestro | not_implemented |

### Firmware — F-04 GW QoS Scheduler Tuning

Source spec: `rml-system-spec-pack/shared-spec/feature-gw-qos-scheduler-tuning.md`
Trace map: `--base-dir/docs/trace_map.yaml`

| TC ID | AC | Test File (repo-relative) | Test Name | Runner | Status |
|---|---|---|---|---|---|
| TC-F-04-001a | AC-F-04-001 | `ble_qos_demo_V1.2m/tests/unit/gw_qos/src/test_gw_qos.c` | `test_preset_apply` | unit-twister | TBD |
| TC-F-04-002a | AC-F-04-002 | `ble_qos_demo_V1.2m/tests/unit/gw_qos/src/test_gw_qos.c` | `test_preset_out_of_range_rejected` | unit-twister | TBD |
| TC-F-04-003a | AC-F-04-003 | `ble_qos_demo_V1.2m/tests/unit/gw_qos/src/test_gw_qos.c` | `test_invalid_override_rejected_last_known_good_preserved` | unit-twister | not_implemented |
| TC-F-04-004a | AC-F-04-004 | `ble_qos_demo_V1.2m/tests/unit/gw_qos/src/test_gw_qos.c` | `test_tune_val_001_cutoffs_not_increasing` | unit-twister | not_implemented |
| TC-F-04-005a | AC-F-04-005 | `ble_qos_demo_V1.2m/tests/unit/gw_qos/src/test_gw_qos.c` | `test_tune_val_003_interval_out_of_range` | unit-twister | not_implemented |
| TC-F-04-006a | AC-F-04-006 | `ble_qos_demo_V1.2m/tests/unit/gw_qos/src/test_gw_qos.c` | `test_boot_no_config_fallback_balanced` | unit-twister | not_implemented |

### App — A-1 QoS Telemetry Model

Source spec: `rml-system-spec-pack/shared-spec/feature-gw-qos-extension-boundary.md`

| TC ID | AC | Test File (repo-relative) | Test Name | Runner | Status |
|---|---|---|---|---|---|
| TC-A-1-001a | AC-A-1-001 | `ble_qos_app/test/models/qos_telemetry_model_test.dart` | `test_parse_valid_ble_notify_payload` | unit-flutter | not_implemented |
| TC-A-1-002a | AC-A-1-002 | `ble_qos_app/test/models/qos_telemetry_model_test.dart` | `test_missing_optional_fields_use_defaults` | unit-flutter | not_implemented |

### App — RML Functional Requirements

Source spec: `rml-system-spec-pack/app-spec/test_cases.md`

| TC ID | AC | Test File (repo-relative) | Test Name | Runner | Status |
|---|---|---|---|---|---|
| TC-APP-001 | AC-APP-001 | `ble_qos_app/maestro/telemetry_display.yaml` | `TC-001 telemetry display` | e2e-maestro | TBD |
| TC-APP-002 | AC-APP-001 | `ble_qos_app/maestro/telemetry_display.yaml` | `TC-002 sparse stale injection` | e2e-maestro | TBD |
| TC-APP-003 | AC-APP-002 | `ble_qos_app/maestro/capability_gate.yaml` | `TC-003 caps gate` | e2e-maestro | TBD |
| TC-APP-004 | AC-APP-003 | `ble_qos_app/maestro/identity_boundary.yaml` | `TC-004 identity boundary` | e2e-maestro | TBD |
| TC-APP-005 | AC-APP-004 | `ble_qos_app/maestro/assignment_reconciliation.yaml` | `TC-005 reconciliation dual gateway` | e2e-maestro | TBD |
| TC-APP-006 | AC-APP-005 | `ble_qos_app/maestro/alias_precedence.yaml` | `TC-006 alias precedence` | e2e-maestro | TBD |
| TC-APP-007 | AC-APP-006 | `ble_qos_app/maestro/cmd_v2_roundtrip.yaml` | `TC-007 cmd round trip success error rejected` | e2e-maestro | TBD |
| TC-APP-008 | AC-APP-006 | `ble_qos_app/maestro/cmd_v2_roundtrip.yaml` | `TC-008 cmd timeout and retry` | e2e-maestro | TBD |
| TC-APP-009 | AC-APP-004 | `ble_qos_app/maestro/assignment_reconciliation.yaml` | `TC-009 not compared when no central data` | e2e-maestro | TBD |
| TC-APP-010 | AC-APP-005 | `ble_qos_app/maestro/alias_precedence.yaml` | `TC-010 alias no pending` | e2e-maestro | TBD |
| TC-APP-011 | AC-APP-006 | `ble_qos_app/maestro/cmd_v2_roundtrip.yaml` | `TC-011 explicit reject no silent retry` | e2e-maestro | TBD |
| TC-APP-012 | AC-APP-004 | `ble_qos_app/maestro/assignment_reconciliation.yaml` | `TC-012 can_compare false stale reference` | e2e-maestro | TBD |

### Central — W26A Failback Command Service

Source spec: `central-device-metadata/docs/specs/failback-command-service-spec.md`

| TC ID | AC | Test File (repo-relative) | Test Name | Runner | Status |
|---|---|---|---|---|---|
| TC-W26A-001 | AC-W26A-001 | `central-device-metadata/tests/unit/test_failback_command_service.py` | `test_given_ineligible_device_hold_down_when_execute_then_raises_failback_ineligible_error` | unit-pytest | RED (spec_pending) |
| TC-W26A-002 | AC-W26A-002 | `central-device-metadata/tests/unit/test_failback_command_service.py` | `test_given_ineligible_device_unhealthy_gw_when_execute_then_raises_failback_ineligible_error` | unit-pytest | RED (spec_pending) |
| TC-W26A-003 | AC-W26A-003 | `central-device-metadata/tests/unit/test_failback_command_service.py` | `test_given_ineligible_device_when_execute_then_orchestrator_not_called` | unit-pytest | RED (spec_pending) |
| TC-W26A-004 | AC-W26A-004 | `central-device-metadata/tests/unit/test_failback_command_service.py` | `test_given_eligible_device_when_execute_then_calls_orchestrator_with_failback_decision_type` | unit-pytest | RED (spec_pending) |
| TC-W26A-005 | AC-W26A-005 | `central-device-metadata/tests/unit/test_failback_command_service.py` | `test_given_eligible_device_when_execute_then_returns_failback_executed_outcome` | unit-pytest | RED (spec_pending) |
| TC-W26A-006 | AC-W26A-006 | `central-device-metadata/tests/integration/test_failback_route.py` | `test_given_viewer_role_when_post_failback_then_403` | integration-pytest | RED (spec_pending) |
| TC-W26A-007 | AC-W26A-007 | `central-device-metadata/tests/integration/test_failback_route.py` | `test_given_ineligible_device_when_post_failback_then_422` | integration-pytest | RED (spec_pending) |
| TC-W26A-008 | AC-W26A-008 | `central-device-metadata/tests/integration/test_failback_route.py` | `test_given_ineligible_device_hold_down_when_post_failback_then_422_with_remaining_seconds` | integration-pytest | RED (spec_pending) |
| TC-W26A-009 | AC-W26A-009 | `central-device-metadata/tests/integration/test_failback_route.py` | `test_given_eligible_device_when_post_failback_then_200_failback_executed` | integration-pytest | RED (spec_pending) |
| TC-W26A-010 | AC-W26A-010 | `central-device-metadata/tests/integration/test_failback_route.py` | `test_given_eligible_device_when_post_failback_as_admin_then_200` | integration-pytest | RED (spec_pending) |

### Central — C-2 QoS Tuning Integration Tests

Source spec: `central-device-metadata/docs/specs/c2-integration-test-qos-tuning.md`

| TC ID | AC | Test File (repo-relative) | Test Name | Runner | Status |
|---|---|---|---|---|---|
| TC-C2-001 | AC-C2-001 | `central-device-metadata/tests/integration/test_qos_tuning_integration.py` | `test_tune_val_001_cutoffs_not_increasing_422` | integration-pytest | not_implemented |
| TC-C2-002 | AC-C2-002 | `central-device-metadata/tests/integration/test_qos_tuning_integration.py` | `test_tune_val_003_interval_out_of_range_422` | integration-pytest | not_implemented |
| TC-C2-003 | AC-C2-003 | `central-device-metadata/tests/integration/test_qos_tuning_integration.py` | `test_tune_val_006_warning_save_200` | integration-pytest | not_implemented |
| TC-C2-004 | AC-C2-004 | `central-device-metadata/tests/integration/test_qos_tuning_integration.py` | `test_cross_gw_isolation` | integration-pytest | not_implemented |
| TC-C2-005 | AC-C2-005 | `central-device-metadata/tests/integration/test_qos_tuning_integration.py` | `test_concurrent_put_race_condition_revision_2` | integration-pytest | not_implemented |
| TC-C2-006 | AC-C2-006 | `central-device-metadata/tests/integration/test_qos_tuning_integration.py` | `test_audit_log_written_same_transaction` | integration-pytest | not_implemented |
| TC-C2-007 | AC-C2-007 | `central-device-metadata/tests/integration/test_qos_tuning_integration.py` | `test_unknown_gw_returns_404` | integration-pytest | not_implemented |
| TC-C2-008 | AC-C2-008 | `central-device-metadata/tests/integration/test_qos_tuning_integration.py` | `test_get_no_row_returns_balanced_default` | integration-pytest | not_implemented |

## Summary Statistics

### By Status

| Status | Count |
|---|---|
| GREEN | 0 |
| TBD | 18 |
| RED (spec_pending) | 10 |
| not_implemented | 22 |
| **Total TC** | **50** |

### By Runner

| Runner | Count |
|---|---|
| unit-twister | 10 |
| unit-pytest | 5 |
| integration-pytest | 18 |
| e2e-maestro | 15 |
| unit-flutter | 2 |
| **Total** | **50** |

### Coverage by AC

| Metric | Count |
|---|---|
| ACs in S-1 catalog | 44 |
| ACs with at least 1 TC | 34 |
| ACs without TC (gap) | 10 |
| Total TCs | 50 |

## References

- S-1 AC catalog: `rml-system-spec-pack/shared-spec/s1-ac-catalog.md`
- Trace map SSOT: `--base-dir/docs/trace_map.yaml`
- S-3 trace strategy: `rml-system-spec-pack/shared-spec/s3-cross-repo-trace-strategy.md`
- FW-3A spec trace map section: `--base-dir/docs/specs/fw-3a-cmd-v2-length-guard.md#trace-map-req--ac--tc--impl`
