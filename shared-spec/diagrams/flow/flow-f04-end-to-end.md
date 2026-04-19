<!--
AI-DIAGRAM: required
primary_message: App 更改 preset → Central 記錄 → CMD_V2 送 GW → Firmware 套用 → 結果回 App
reader: engineer
template_id: flow-linear-gate
diagram_type: flowchart
layout: top-to-bottom
max_nodes: 9
max_groups: 3
keep: preset選擇、Central audit、CMD_V2 dispatch、NVS寫入、CMD_RESULT回傳
avoid: validation細節、reject codes展開、BLE wire encoding
-->

# F-04 End-to-End 流程圖

**主訊息**：Operator 在 App 選擇 QoS preset，經 Central 記錄後透過 CMD_V2 送到 GW，Firmware 套用並回報結果。

```mermaid
flowchart TD
    A[App\nEngineering Mode] -->|POST /gateways/:id/sched-tune\n選擇 preset or expert override| B[Central API]
    B -->|驗 TUNE-VAL 規則\n記錄 audit log| C{Central\nValidation}
    C -->|REJECT 0x01-0x06| D[回傳 400 Bad Request\nApp 顯示紅字錯誤]
    C -->|PASS| E[Central\n儲存設定 + revision++]
    E -->|BLE CMD_V2 opcode 0x07\n4/16-byte payload| F[GW Firmware\ncmd_v2_dispatch]
    F -->|gw_qos_apply_tune\nNVS 寫入| G{Firmware\nValidation}
    G -->|REJECT invalid config| H[CMD_RESULT REJECT\n0x01-0x06]
    G -->|PASS| I[套用新 step table\nQoS 生效]
    I -->|CMD_RESULT SUCCESS 0x00| J[Central 更新狀態]
    H --> J
    J -->|App 收到 notification\nor polling| K[App UI 更新\n顯示 confirmed / error]
```

**說明**：流程展示 F-04 scheduler tuning 的端對端路徑。Central 是第一道驗證關卡（TUNE-VAL），Firmware 是最終 guard。CMD_RESULT 成功後 App UI 才轉為 `confirmed` 狀態。Busy guard（0xFD reject）見 [`seq-cmd-v2-reject-busy.md`](../sequence/seq-cmd-v2-reject-busy.md)。

**Reference**：
- Spec: [`../../../shared-spec/feature-gw-qos-scheduler-tuning.md`](../../feature-gw-qos-scheduler-tuning.md)
- Validation rules: `TUNE-VAL-001` ~ `TUNE-VAL-006`
- ADR: `--base-dir/docs/decisions/2026-04-18-f04-runtime-preset-over-build-assert.md`
