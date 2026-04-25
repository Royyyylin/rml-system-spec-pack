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
| GW QoS scheduler tuning — contract semantics | `rml-system-spec-pack/03_building-blocks/F-04-gw-qos-scheduler-tuning/tuning.md` |
| GW QoS scheduler tuning — runtime config truth | `central-device-metadata` DB/API（canonical deployment value per GW） |
| GW QoS scheduler tuning — wire/GATT apply protocol | `ble_qos_demo_V1.2m/ble_api.yaml`（CMD_V2 opcode 0x07 decided；pending `ble_api.yaml` formal entry） |
| GW QoS extension boundary（config apply vs telemetry profiling） | `rml-system-spec-pack/03_building-blocks/F-04-gw-qos-scheduler-tuning/extension-boundary.md` |
| Telemetry Profiling catalog / schema（future） | 未定義 — 未來需獨立 SSOT，不歸 F-04 |

## Pack Sources

| Layer | Source |
| :--- | :--- |
| Upstream intent | `00_introduction-goals/system-intent.md`, `05_quality-acceptance/baseline-target-migration.md`, `02_solution-strategy/capability-map.md`, `03_building-blocks/FEA-001-telemetry-roster-visibility.md`, `03_building-blocks/FEA-002-command-execution-feedback.md`, `03_building-blocks/FEA-003-identity-alias-metadata-display.md`, `03_building-blocks/FEA-004-assignment-reconciliation/contract.md`, `03_building-blocks/F-04-gw-qos-scheduler-tuning/tuning.md`, `05_quality-acceptance/requirements.md` |
| App downstream | `app-spec/architecture.md`, `app-spec/state_machine.md`, `app-spec/sequence_flows.md` |
| Diagram sources | `03_building-blocks/FEA-001-telemetry-roster-visibility.d2`, `03_building-blocks/FEA-002-command-execution-feedback.d2`, `03_building-blocks/FEA-003-identity-alias-metadata-display.d2`, `03_building-blocks/FEA-004-assignment-reconciliation/context.d2`, `03_building-blocks/FEA-004-assignment-reconciliation/states.d2`, `app-spec/block_diagram.d2`, `app-spec/state_diagram.mmd`, `app-spec/sequence_diagram.mmd`, `firmware-spec/packet_diagram.d2` |
| Packet mapping | `firmware-spec/packet_contract.md` |
| Governance | `trace/trace_map.yaml`, `trace/change_rules.md`, `trace/manual_exceptions.yaml`, `trace/impact-summary.md` |
| Verification | `05_quality-acceptance/ac-catalog.md`, `05_quality-acceptance/tc-matrix.md` |

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

1. `00_introduction-goals/system-intent.md`
2. `05_quality-acceptance/requirements.md`
3. Arc42 chapter dirs (`00_*` ~ `06_*`)、`app-spec/*` 與 `firmware-spec/*` 原始碼 / 圖 source
4. `trace/trace_map.yaml`
5. `trace/change_rules.md`
6. `05_quality-acceptance/ac-catalog.md`
7. `05_quality-acceptance/tc-matrix.md`
8. `trace/impact-summary.md`
