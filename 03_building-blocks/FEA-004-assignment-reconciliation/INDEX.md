# FEA-004: Assignment Reconciliation

> Cross-repo feature — 4-owner (App / Central / Firmware / spec-pack).
> Fractal split: 3 sub-artifacts (contract + 2 diagrams).

## Files

| File | Purpose |
|------|---------|
| [contract.md](contract.md) | Feature contract: AC, wire contract, reconciliation protocol |
| [context.d2](context.d2) | Context diagram — components and data flow |
| [states.d2](states.d2) | State machine — reconciliation state transitions |

## Summary

FEA-004 defines the **assignment reconciliation** protocol between App and Central.
When App-derived assignment state diverges from Central evidence, a reconciliation
flow is triggered to restore consistency.

## Authority

- Canonical owner: `spec-pack` (cross-repo coordination layer)
- Wire contract SSOT: `firmware/ble_api.yaml`
- See [`01_context-scope/authority-map.yaml`](../../01_context-scope/authority-map.yaml)
