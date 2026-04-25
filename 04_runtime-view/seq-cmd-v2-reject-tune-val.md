<!--
AI-DIAGRAM: required
primary_message: TUNE-VAL reject 路徑：App 或 Firmware 偵測到 validation 錯誤，指令被拒絕並告知原因
reader: engineer
template_id: sequence-main-branch
diagram_type: sequenceDiagram
layout: left-to-right
max_nodes: 4
max_groups: 2
keep: TUNE-VAL在App端的前置驗證、Central拒絕、Firmware guard reject、reject code 0x01-0x06
avoid: NVS寫入、busy guard、成功路徑
-->

# CMD_V2 Reject — TUNE-VAL 驗證失敗時序圖

**主訊息**：當 preset/expert override 違反 TUNE-VAL 規則時，App 前置攔截或 Central / Firmware reject，指令不會套用。

```mermaid
sequenceDiagram
    participant App
    participant Central
    participant GW as GW Firmware

    Note over App: 使用者輸入 expert override<br/>cutoff1 >= cutoff2（違反 TUNE-VAL-001）

    alt App 前置驗證攔截
        App->>App: UX validation<br/>偵測 cutoff 順序錯誤
        App->>App: 顯示紅色錯誤提示<br/>Save/Apply 按鈕 disabled
        Note over App: 指令不送出
    else 通過 App UX validation 但違反後端規則
        App->>Central: POST /gateways/:id/sched-tune
        Central->>Central: TUNE-VAL 驗證失敗
        Central-->>App: 400 Bad Request<br/>error: TUNE_VAL_001
        App->>App: 顯示錯誤原因
    else 到達 Firmware 才被拒絕
        App->>Central: POST (通過 Central validation)
        Central->>GW: BLE Write CMD_V2 opcode=0x07
        GW->>GW: Firmware final guard<br/>偵測 invalid config
        GW-->>App: BLE Notify CMD_RESULT<br/>opcode=0x07, status=0x01-0x06
        App->>App: 顯示 reject code 對應訊息
    end
```

**說明**：三層防護（App UX → Central → Firmware）確保 invalid config 不被套用。`TUNE-VAL-004` 要求 App 端必須前置攔截，讓 UX 即時回饋。`TUNE-VAL-005` 要求 Firmware 的 final guard 必須存在，不依賴上層。

**Reference**：
- Validation rules: [`../../feature-gw-qos-scheduler-tuning.md`](../../feature-gw-qos-scheduler-tuning.md) `TUNE-VAL-001~006`
- Success 路徑: [`seq-cmd-v2-success.md`](seq-cmd-v2-success.md)
