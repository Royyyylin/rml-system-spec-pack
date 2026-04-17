# RML System Spec Pack

本目錄將原本偏提案式的架構描述，改寫成「規格治理式規劃」。

## 讀取順序

1. `shared-spec/rml-lite.md`
2. `shared-spec/baseline-target-migration.md`
3. `shared-spec/capability-ownership.md`
4. `shared-spec/diagram-authoring-rules.md`
5. `shared-spec/diagram-templates.md`
6. `shared-spec/feature-telemetry-roster-visibility.md`
7. `shared-spec/feature-command-execution-feedback.md`
8. `shared-spec/feature-identity-alias-metadata-display.md`
9. `shared-spec/feature-assignment-reconciliation.md`
10. `shared-spec/feature-gw-qos-scheduler-tuning.md`
11. `shared-spec/requirements.md`
12. `app-spec/architecture.md`
13. `app-spec/state_machine.md`
14. `app-spec/sequence_flows.md`
15. `firmware-spec/packet_contract.md`
16. `trace/source_of_truth.md`
17. `trace/trace_map.yaml`
18. `trace/change_rules.md`
19. `app-spec/acceptance_criteria.md`
20. `app-spec/test_cases.md`
21. `trace/impact-summary.md`

## 這次改動影響的正式檔案

- `shared-spec/rml-lite.md`
- `shared-spec/baseline-target-migration.md`
- `shared-spec/capability-ownership.md`
- `shared-spec/diagram-authoring-rules.md`
- `shared-spec/diagram-templates.md`
- `shared-spec/feature-telemetry-roster-visibility.md`
- `shared-spec/feature-telemetry-roster-visibility.d2`
- `shared-spec/feature-command-execution-feedback.md`
- `shared-spec/feature-command-execution-feedback.d2`
- `shared-spec/feature-identity-alias-metadata-display.md`
- `shared-spec/feature-identity-alias-metadata-display.d2`
- `shared-spec/feature-assignment-reconciliation.md`
- `shared-spec/feature-assignment-reconciliation.d2`
- `shared-spec/feature-gw-qos-scheduler-tuning.md`
- `shared-spec/requirements.md`
- `app-spec/architecture.md`
- `app-spec/state_machine.md`
- `app-spec/sequence_flows.md`
- `app-spec/block_diagram.d2`
- `app-spec/state_diagram.mmd`
- `app-spec/sequence_diagram.mmd`
- `firmware-spec/packet_contract.md`
- `firmware-spec/packet_diagram.d2`
- `trace/source_of_truth.md`
- `trace/trace_map.yaml`
- `trace/change_rules.md`
- `app-spec/acceptance_criteria.md`
- `app-spec/test_cases.md`
- `trace/impact-summary.md`

## 修改流程

1. 先改上游：`rml-lite.md`、feature spec、`requirements.md`
2. 再改 diagram source：shared-spec / app-spec / firmware-spec，並維護 `AI Diagram Contract`
3. 再改下游：block / state / sequence / packet
4. 再改 trace：`source_of_truth.md`、`trace_map.yaml`、`change_rules.md`
5. 再改驗收：`acceptance_criteria.md`
6. 再改測試：`test_cases.md`
7. 最後更新：`trace/impact-summary.md`

## 規則

- PNG 不是 source of truth
- 所有 `.d2` / `.mmd` source 都必須帶 `AI Diagram Contract` comment block
- `renders/` 為 derived artifacts，原則上禁止手改；若因展示或工具缺口暫時手改，必須補回對應 source / tool 變更
- 若本 spec pack 與 repo SSOT 衝突，以 repo SSOT 為準
- `desktop-spec/` 目前沒有足夠來源，本輪不建立正式內容
