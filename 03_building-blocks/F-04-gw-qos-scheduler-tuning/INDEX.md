# F-04: GW QoS Scheduler Tuning

> **Legacy firmware-led feature** — uses `F-NN` prefix (not `FEA-NNN`).
> Naming rule: `F-NN` = firmware-initiated AND firmware runtime behavior as primary.
> See naming classification in plan § "命名規範".

## Files

| File | Purpose |
|------|---------|
| [tuning.md](tuning.md) | Feature spec: scheduler tuning parameters, runtime preset (CMD_V2 0x07) |
| [extension-boundary.md](extension-boundary.md) | Extension boundary contract: configurable vs fixed scheduling knobs |

## Summary

F-04 covers **GW QoS scheduler tuning** — the runtime mechanism by which the
Gateway adjusts BLE scheduling parameters (TX interval, priority weight, bandwidth
allocation) per traffic class via CMD_V2 `0x07` preset commands.

## Authority

- Primary owner: `firmware` (runtime behaviour is firmware-led)
- Consumers: `app` (preset selection UI), `central` (scheduling observation)
- ADR reference: `99_appendix/decisions/ADR-000-spec-authority-model.md`
- See [`01_context-scope/authority-map.yaml`](../../01_context-scope/authority-map.yaml)
