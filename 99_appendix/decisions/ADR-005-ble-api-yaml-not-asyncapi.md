# ADR-005: ble_api.yaml Not Converted to AsyncAPI

Status: accepted
Date: 2026-04-26
Decided by: Roy (post Phase 1 enforcement audit)

## Context

`ble_api.yaml` is the firmware-repo SSOT for all GATT wire contracts (UUID, opcode, payload field semantics) in the BLE QoS system. It is a hand-authored YAML file with a project-specific schema covering: characteristics (CMD_V2, CMD_RESULT, CAPS_V2, TUNE-VAL), opcodes, presets, NVS roles, and system constants.

AsyncAPI 3.0 is an open standard (https://www.asyncapi.com/) for describing event-driven and message-passing APIs. It has native support for BLE-style pub/sub patterns and is toolchain-compatible with codegen (asyncapi-generator) and documentation (asyncapi-studio).

The conversion proposal was motivated by:
1. AsyncAPI would give `ble_api.yaml` a machine-readable, community-standard format that external tools could validate
2. asyncapi-generator could auto-generate Dart (App) and Python (Central) parser stubs from the GATT spec

The Phase 1 audit found three blockers:

1. **BLE GATT semantics not covered by AsyncAPI channels**: AsyncAPI channels map to message brokers (Kafka topics, MQTT topics, WebSocket paths). GATT characteristics with read/write/notify properties do not map cleanly to AsyncAPI channel + operation semantics. The `CMD_V2` characteristic is simultaneously: a write target (command), a notification source (result via CMD_RESULT), and a CBOR-encoded payload. No AsyncAPI binding for BLE/GATT exists in the official binding registry as of 2026-04-26.

2. **Codegen coverage gap**: Even if a BLE AsyncAPI binding were written manually, asyncapi-generator's Dart template is community-maintained and does not produce NCS/Zephyr-compatible C output for the firmware side. The firmware codegen (`src/generated/nvs_roles.h`) uses a project-specific Jinja2 template that cannot be replaced by asyncapi-generator without complete rewrite.

3. **SSOT migration risk**: Moving `ble_api.yaml` from firmware repo to an AsyncAPI file would require all 4 repos to update their CI codegen pipelines simultaneously. Any schema drift during migration would violate quality-goals.md Goal 3 (Wire Contract Stability).

## Decision

Retain `ble_api.yaml` in its current project-specific YAML format in the firmware repo. Do not convert to AsyncAPI 3.0.

The spec-pack's role with respect to `ble_api.yaml` is: reference and derive documentation. The firmware repo is the sole SSOT authority (RML-CAP-004). The spec-pack `06_crosscutting-integration/x1-wire-parity-spec.md` documents the derived wire contract view without duplicating the source.

Re-evaluate if: an official GATT/BLE binding for AsyncAPI is merged into the AsyncAPI specification repository, or if a new codegen tool emerges that supports both Dart and NCS/Zephyr C output from AsyncAPI source.

## Consequences

**Positive:**
- No migration risk to existing 4-repo codegen pipelines
- `ble_api.yaml` schema remains under full project control (no upstream breaking changes)
- Firmware repo CI codegen is not disrupted

**Negative:**
- `ble_api.yaml` is not discoverable by standard AsyncAPI tooling (asyncapi-studio, event catalog)
- External developers cannot use community AsyncAPI parsers to validate wire contracts
- No automatic Dart/Python stub generation from AsyncAPI source (stubs must be maintained manually or via project-specific codegen)

**Compensating control:**
The `x1-wire-parity-spec.md` and cross-repo-trace-strategy.md provide a human-readable derived view of the wire contract that covers the documentation use case that AsyncAPI would have served.

## Alternatives

- **AsyncAPI 3.0 with custom BLE binding**: Rejected — no official BLE binding; custom binding maintenance cost exceeds benefit
- **Protobuf / gRPC**: Rejected — incompatible with BLE GATT transport layer; Protobuf does not model GATT characteristics or notification channels
- **OpenAPI 3.1 (REST-style overlay)**: Evaluated — OpenAPI does not model binary/CBOR payloads or BLE notification patterns; rejected
- **Keep ble_api.yaml as-is**: Accepted — formalizes the existing SSOT decision

## References

- ADR-008: Task A Completion Strategy
- quality-goals.md Goal 3 (Wire Contract Stability)
- x1-wire-parity-spec.md: derived wire contract documentation
- ble_api.yaml SSOT: `ble_qos_demo_V1.2m/ble_api.yaml` (firmware repo)
- AsyncAPI specification: https://www.asyncapi.com/docs/reference/specification/v3.0.0
- RML-CAP-004: Wire contract authority boundary (capability-map.md)
