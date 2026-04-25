# app-spec

> App-side spec (Flutter, ble_qos_app). Consumer of cross-repo FEA-NNN contracts.
> Authority: ble_qos_app repo. This dir is spec-pack's view of app-side contracts.

## 內容

| 檔案 | 說明 |
|---|---|
| `architecture.md` | App architecture (bounded context view, SSOT: ble_qos_app) |
| `state_machine.md` | App state machine prose |
| `state_diagram.mmd` | App state diagram (Mermaid, AI Diagram Contract validated) |
| `sequence_flows.md` | App sequence flows prose |
| `sequence_diagram.mmd` | App sequence diagram (Mermaid) |
| `block_diagram.d2` | App block diagram (D2, AI Diagram Contract validated) |
| `acceptance_criteria.md` | App-level AC (cross-ref to 05_quality-acceptance/ac-catalog.md) |
| `test_cases.md` | App-level TC (cross-ref to 05_quality-acceptance/tc-matrix.md) |

## Cross-ref

- Feature contracts: `../03_building-blocks/FEA-NNN-*/`
- Canonical AC: `../05_quality-acceptance/ac-catalog.md`
- Canonical TC: `../05_quality-acceptance/tc-matrix.md`
- Wire SSOT: `ble_qos_demo_V1.2m/ble_api.yaml`
