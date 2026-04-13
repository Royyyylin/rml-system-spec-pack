# Impact Summary

## Changed Files

- `README.md`
- `shared-spec/rml-lite.md`
- `shared-spec/baseline-target-migration.md`
- `shared-spec/capability-ownership.md`
- `shared-spec/diagram-authoring-rules.md`
- `shared-spec/feature-telemetry-roster-visibility.md`
- `shared-spec/feature-telemetry-roster-visibility.d2`
- `shared-spec/feature-command-execution-feedback.md`
- `shared-spec/feature-command-execution-feedback.d2`
- `shared-spec/feature-identity-alias-metadata-display.md`
- `shared-spec/feature-identity-alias-metadata-display.d2`
- `shared-spec/feature-assignment-reconciliation.md`
- `shared-spec/feature-assignment-reconciliation.d2`
- `renders/feature-telemetry-roster-visibility.svg`
- `renders/feature-command-execution-feedback.svg`
- `renders/feature-identity-alias-metadata-display.svg`
- `renders/feature-assignment-reconciliation.svg`
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
- `trace/change_rules.md`
- `trace/trace_map.yaml`
- `tools/check_diagram_contract.py`
- `app-spec/acceptance_criteria.md`
- `app-spec/test_cases.md`

## Impacted Requirements / States / Packets

- Requirements: `REQ-001`..`REQ-006`
- States: `STA-001`..`STA-004`
- Packets: `PKT-001`..`PKT-006`

## Upstream Feature Additions

- `RML-FEA-001` 已補成 formal feature spec，並新增 source diagram `shared-spec/feature-telemetry-roster-visibility.d2`
- `RML-FEA-002` 已補成 formal feature spec，並新增 source diagram `shared-spec/feature-command-execution-feedback.d2`
- `RML-FEA-003` 已補成 formal feature spec，並新增 source diagram `shared-spec/feature-identity-alias-metadata-display.d2`
- `RML-FEA-004` 已補成 formal feature spec，並新增 source diagram `shared-spec/feature-assignment-reconciliation.d2`

## Role Vocabulary Alignment (2026-04-12)

- `rml-lite.md`: 新增 Firmware Runtime Roles 段落，記錄既有 CC bridge / GW / ED 三角色定義
- `feature-assignment-reconciliation.md`: BND-005 合併 CC bridge session 描述、統一 Gateway 全稱、Conductor 命名修正
- `feature-command-execution-feedback.md`: Firmware / GW → Firmware / Gateway
- `capability-ownership.md`: Conductor 命名修正
- 不變更任何 RML-* ID、不變更 requirements.md

## Formal Traceability Gap Closure (2026-04-13)

### acceptance_criteria.md
- AC-003: `edId/gwId` → `stableId/central_ref`；補 CC bridge relayed-view 條件
- AC-004: 補 `not compared` / `last synced` 條件（無 Central 即時資料時不得顯示 conflict）
- AC-006: 補 permission-denied / REJECTED 顯示條件

### test_cases.md
- TC-004: 補 CC bridge session 步驟與 stableId 對齊
- TC-009 (new): 覆蓋 AC-004 的 not-compared branch
- TC-010 (new): 覆蓋 AC-005 的 no-pending precedence branch
- TC-011 (new): 覆蓋 AC-006 的 permission-denied / reject branch

### trace_map.yaml
- REQ-004 / AC-004: 新增 TC-009
- REQ-005 / AC-005: 新增 TC-010
- REQ-006 / AC-006: 新增 TC-011
- TC-009 / TC-010 / TC-011: 完整 acceptance / requirement / feature / evidence 欄位

### Deferred
- `feature-assignment-reconciliation.d2` line 17: `pending` → `pending_reconciliation` (Low severity, deferred to vocabulary consistency pass)

## Render Updates

- `d2` 已安裝，本輪開始允許由 source diagram 產生衍生 SVG render
- render 仍屬 derived artifact，不可覆蓋 formal source
- 已產生 `feature-telemetry-roster-visibility.svg`、`feature-command-execution-feedback.svg`、`feature-identity-alias-metadata-display.svg` 與 `feature-assignment-reconciliation.svg`

## Diagram Governance Updates

- 所有正式 `.d2` / `.mmd` source 現在都要求有 `AI Diagram Contract` comment block
- 新增 `shared-spec/diagram-authoring-rules.md`，把 prompt contract 與人類可讀限制正式化
- 新增 `tools/check_diagram_contract.py` 作為最小 lint 入口

## Problems Found in Original Description Style

- 舊稿把 `0x2A1E` / `0x2A1F` 誤當 error / action；現行 SSOT 實際是 `MODE` / `ROLE`
- 舊稿把 service 寫成 `0xFF01`；現行 SSOT 是 `0x1820`
- 舊稿把 `device_identity` 與 MAC 綁太緊；現行 app / Central 已分成 `stableId`、`central_ref`、MAC 三層
- 舊稿缺少 Central truth、assignment reconciliation、alias precedence、`CMD_V2` / `CMD_RESULT`
- 舊稿 trace 曾殘留 TODO；本輪已改成完整可追蹤映射

## Missing Updates

- `desktop-spec/` 尚未建立正式內容；缺少 desktop 來源文件
- 尚未產生 PNG；目前先維持 SVG render

## Evidence Gaps

- 尚未附上真機 / HIL capture
- `CMD_V2` timeout 常數仍需以 app timeout matrix 再確認
- `CAPS_V2` fallback 到 `CAP` 的實機矩陣仍需補完整證據

## Desync Risks

- 若 `ble_api.yaml` 更新而 packet / sequence 未回寫，最容易先失同步
- 若 Central assignment policy 更新但 `STA-002` / `SEQ-002` 未回寫，UI 會誤導操作員
- 若 alias precedence 改動但 `AC-005` / `TC-006` 未同步，使用者衝突處理會失真

## Assumptions

- 本 pack 只涵蓋 app-facing display contract，不額外定義 desktop 專屬行為
- Async command timeout 暫以 `30s` 作為驗收假設
- `ROSTER_LIST` 足以支撐 runtime attach 對映；若 firmware schema 擴充，需回寫 `PKT-004`

## TODOs

- 導入 desktop 正式來源後補 `desktop-spec/`
- 若要進 CI，需再補 trace lint script 與 changed-only report schema
- 若要產生 PNG，再補 batch render/export 流程
