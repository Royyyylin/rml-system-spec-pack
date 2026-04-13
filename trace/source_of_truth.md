# Source of Truth

## Priority Order

1. Repo SSOT
2. 本 spec pack 的衍生整合內容
3. Render artifacts

## Repo SSOT

| Layer | Source |
| :--- | :--- |
| Firmware contract | `ble_qos_demo_V1.2m/ble_api.yaml` |
| App architecture | `ble_qos_app/docs/architecture/APP_ARCHITECTURE.md` |
| App cross-repo boundary | `ble_qos_app/docs/handoffs/2026-03-28-app-architecture-brief.md` |
| Central identity / assignment | `central-device-metadata/docs/specs/data-model.md` |
| Central alias precedence | `central-device-metadata/docs/specs/alias-sync-spec.md` |

## Pack Sources

| Layer | Source |
| :--- | :--- |
| Upstream intent | `shared-spec/rml-lite.md`, `shared-spec/baseline-target-migration.md`, `shared-spec/capability-ownership.md`, `shared-spec/diagram-authoring-rules.md`, `shared-spec/diagram-templates.md`, `shared-spec/feature-telemetry-roster-visibility.md`, `shared-spec/feature-command-execution-feedback.md`, `shared-spec/feature-identity-alias-metadata-display.md`, `shared-spec/feature-assignment-reconciliation.md`, `shared-spec/requirements.md` |
| App downstream | `app-spec/architecture.md`, `app-spec/state_machine.md`, `app-spec/sequence_flows.md` |
| Diagram sources | `shared-spec/feature-telemetry-roster-visibility.d2`, `shared-spec/feature-command-execution-feedback.d2`, `shared-spec/feature-identity-alias-metadata-display.d2`, `shared-spec/feature-assignment-reconciliation.d2`, `app-spec/block_diagram.d2`, `app-spec/state_diagram.mmd`, `app-spec/sequence_diagram.mmd`, `firmware-spec/packet_diagram.d2` |
| Packet mapping | `firmware-spec/packet_contract.md` |
| Governance | `trace/trace_map.yaml`, `trace/change_rules.md`, `trace/manual_exceptions.yaml`, `trace/impact-summary.md` |
| Verification | `app-spec/acceptance_criteria.md`, `app-spec/test_cases.md` |

## Render Artifacts

- PNG / SVG / exported screenshots 不是 source of truth
- 若未渲染，原始碼仍可作為正式內容
- `renders/` 內檔案原則上禁止手改；應由 `docs/`、`schemas/`、`diagrams/` 或 render tool 產生
- 若因展示阻塞或工具缺口必須手改，必須在 `trace/manual_exceptions.yaml` 記錄暫時性例外，並補回對應 source / tool 變更
- 手改後的 render 不得被視為正式依據，也不得覆蓋 repo SSOT 或 formal source artifact

## Conflict Rule

- 若本 spec pack 與 repo SSOT 衝突，repo SSOT 優先
- 修復順序：repo SSOT -> packet / sequence / architecture -> trace -> AC -> TC

## Required Update Order

1. `shared-spec/rml-lite.md`
2. `shared-spec/requirements.md`
3. `shared-spec/*`、`app-spec/*` 與 `firmware-spec/*` 原始碼 / 圖 source
4. `trace/trace_map.yaml`
5. `trace/change_rules.md`
6. `app-spec/acceptance_criteria.md`
7. `app-spec/test_cases.md`
8. `trace/impact-summary.md`
