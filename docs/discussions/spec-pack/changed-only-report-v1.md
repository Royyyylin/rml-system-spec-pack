# Changed Only Report V1 Draft

Status: discussion
Date: 2026-04-08
Decision: v1 採 `report-first`，不作為 blocking gate。

## Purpose

`changed_only_report` 的任務是根據本次變更檔案，快速指出高信心的同步風險。

它要解的問題是：
- 變更已經發生，但 formal artifacts 沒有一起更新
- 團隊知道有 change rules，卻很難每次手動比對
- review 時間有限，容易漏掉 render-only diff 或跨層 fan-out

它不負責：
- 取代完整 code review
- 理解所有語意差異
- 在 v1 就直接阻擋提交

## Operating Mode

- 模式：`report-only`
- v1 預設不擋提交、不擋 merge
- 有發現風險時輸出 `warn`
- 沒發現風險時輸出 `pass`
- 只有工具本身執行失敗時才回傳非零 exit code

這個決策的理由是：
- 目前 change rules 已成形，但仍在收斂期
- 先量出誤報率，比一開始就上 gate 更穩
- 規則成熟後，再把低誤報項目升格為 gate

## Inputs

v1 最小輸入：
- `changed_files`
- `base_ref` 或等價 diff 邊界
- spec pack root

可選輸入：
- `manual_exceptions`
- `repo_ssot_roots`

`manual_exceptions` v1 預設讀：
- `trace/manual_exceptions.yaml`

CLI 仍可用 `--manual-exception` 臨時覆蓋或補充。

每筆至少包含：
- `rule_id`
- `reason`
- `owner`
- `expires_on`
- `path_glob`

## Outputs

v1 同時支援兩種輸出：
- 給人讀的文字摘要
- 給 CI / 後續工具讀的 JSON 報告

建議 JSON 結構如下：

```json
{
  "version": "1",
  "mode": "report-only",
  "status": "pass",
  "changed_files": [],
  "rule_hits": [
    {
      "rule_id": "CIR-009",
      "severity": "warn",
      "trigger_files": [],
      "required_updates": [],
      "missing_updates": [],
      "notes": ""
    }
  ],
  "changed_requirements": [],
  "changed_states": [],
  "changed_packets": [],
  "manual_exceptions": [],
  "candidate_gate_rules": []
}
```

欄位原則：
- `changed_files`: 本次 diff 涵蓋檔案
- `rule_hits`: 本次命中的 change rules 與缺漏
- `changed_requirements` / `changed_states` / `changed_packets`: 若 v1 無法穩定推導，可留空
- `manual_exceptions`: 這次明確接受的暫時例外
- `candidate_gate_rules`: 已低噪音、可考慮升 gate 的規則

## V1 Rule Set

v1 只做高信心、偏路徑型的規則，不做大量語意推論。

### `CIR-003` `ble_api.yaml` Fan-Out

Trigger:
- `ble_qos_demo_V1.2m/ble_api.yaml`

Required updates:
- `firmware-spec/packet_contract.md`
- `firmware-spec/packet_diagram.d2`

Should review:
- `app-spec/sequence_flows.md`
- `app-spec/acceptance_criteria.md`
- `app-spec/test_cases.md`
- `shared-spec/requirements.md`
- `app-spec/architecture.md`

Report behavior:
- 若 trigger 發生，但連 `packet_contract.md` 與 `packet_diagram.d2` 都沒跟，記 `warn`
- 其他未跟項目先列為 review candidates，不直接當 hard failure

### `CIR-008` Diagram Source Fan-Out

Trigger:
- `app-spec/block_diagram.d2`
- `app-spec/state_diagram.mmd`
- `app-spec/sequence_diagram.mmd`
- `firmware-spec/packet_diagram.d2`

Required updates:
- 對應 prose doc
- 若已有 render pipeline，對應 render artifact

Report behavior:
- source diagram 變更但 prose doc 未動，記 `warn`
- source diagram 變更但尚未有 render pipeline，記 `info`，不視為缺漏

### `CIR-009` Render-Only Diff

Trigger:
- `renders/*`

Required updates:
- matching source artifact
  或
- documented temporary exception

Report behavior:
- 只有 `renders/*` 變更，且沒有對應 source 變更或人工例外，記 `warn`
- 若有 `manual_exceptions`，仍保留命中紀錄，但降為 `info`

## Human Summary Format

文字版輸出至少要有：
- `status`
- `changed files`
- `rule hits`
- `missing updates`
- `manual exceptions`
- `next actions`

若有風險，摘要應優先列：
- 哪條 rule 被命中
- 哪些 formal artifacts 可能漏改
- 哪些項目只是建議 review，不是硬缺漏

## Promotion Path

以下條件成立後，單條規則才考慮從 report 升成 gate：

1. 誤報率低，review 不常需要人工推翻。
2. required updates 可用機械規則穩定判定。
3. 已有例外處理機制，不會逼團隊繞過工具。
4. rule 對應的 formal artifacts 已穩定，不處於搬家期。

目前最可能先升 gate 的候選是：
- `CIR-009`

## Open Items

1. `manual_exceptions.yaml` 長期應維持 trace-local，還是未來演進成跨 repo 例外 registry？
2. `changed_requirements` / `changed_states` / `changed_packets` 要不要在 v1 先留空，等 ID parser 再補？
3. JSON 報告 schema 未來是否需要 versioned migration 規則？
