# Change Rules

| Rule ID | Trigger | Must Update | Should Review |
| :--- | :--- | :--- | :--- |
| `CIR-001` | `RML-*` changed | `shared-spec/requirements.md` | `app-spec/architecture.md`, `app-spec/acceptance_criteria.md` |
| `CIR-002` | `REQ-*` changed | related block / state / sequence / packet docs, `trace_map.yaml`, AC, TC | `impact-summary.md` |
| `CIR-003` | `ble_api.yaml` changed | `firmware-spec/packet_contract.md`, packet diagram, affected sequence / AC / TC | `shared-spec/requirements.md`, `app-spec/architecture.md` |
| `CIR-004` | identity boundary changed (`stableId` / `central_ref` / MAC) | `rml-lite.md`, `requirements.md`, `architecture.md`, `trace_map.yaml` | AC / TC / impact summary |
| `CIR-005` | assignment or Central ownership policy changed | `architecture.md`, `state_machine.md`, `sequence_flows.md`, AC / TC | `rml-lite.md`, `trace_map.yaml` |
| `CIR-006` | alias precedence changed | `requirements.md`, `architecture.md`, AC / TC | `state_machine.md`, `trace_map.yaml` |
| `CIR-007` | command opcode / timeout / result semantics changed | `packet_contract.md`, `state_machine.md`, `sequence_flows.md`, AC / TC | `impact-summary.md` |
| `CIR-008` | diagram source changed | matching prose doc + render artifact if available | `trace_map.yaml` |
| `CIR-009` | `renders/*` changed | matching source artifact or exception recorded in `trace/manual_exceptions.yaml` | `trace/source_of_truth.md`, owning formal doc |

## Governance Notes

- `renders/` 原則上禁止手改；若因展示或工具缺口必須暫時手改，需在 `trace/manual_exceptions.yaml` 記錄例外並補回對應 source / tool 變更
- 所有 `.d2` / `.mmd` source 應保留 `AI Diagram Contract` comment block；若缺少，應先補契約再調整圖內容
- 若 diff 只出現 `renders/*`，但沒有對應 source 變更或 `trace/manual_exceptions.yaml` 例外，`changed_only_report` 應報警
- 若發現 trace 與實際文件不一致，先修 trace，再補 impact summary
- `desktop-spec/` 目前沒有正式輸入來源；若未來補齊，需新增對應 `CIR-*`
