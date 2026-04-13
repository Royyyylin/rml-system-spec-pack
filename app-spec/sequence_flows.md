# Sequence Flows

## `SEQ-001` Detail Hydration and Telemetry Refresh

1. App 讀 `CAPS_V2`，若缺失則 fallback `CAP`
2. App 讀 `ROSTER_LIST` 建立 slot / MAC / `ed_id` 對映
3. App 讀或訂閱 `STATUS` / `METRICS_V2`
4. App 將缺欄位轉成 `TelemetryValueState`，而不是直接顯示錯誤

## `SEQ-002` Assignment Reconciliation

1. App 從 Central snapshot 取得 `authoritativeGatewayId`
2. App 從 firmware roster / runtime telemetry 取得 `runtimeGatewayId`
3. App 計算 `assignmentSyncState`
4. 若不一致，detail / roster 同時顯示 Central 與 Runtime gateway

## `SEQ-003` Alias Rename Sync

1. 使用者修改 alias
2. App 先寫 local pending op 並樂觀更新本地顯示
3. App 向 Central 送 metadata update
4. `200` 清 pending；`409` 進 `conflicted`；network error 保持 `pending`

## `SEQ-004` Command Round Trip

1. 使用者在 detail 觸發 action
2. App 先看 current live peer，決定合法 path
3. 若當前 session 是 `CC bridge`，App 走 `Central-side path`，送出 command request 並進入 `in_flight`
4. `Central-side path` 收到 accepted 時可進 `accepted`，但仍須等待 metadata / sync confirmation 才算 `succeeded`
5. 若當前 session 是 `Gateway` / `End Device`，App 走 `Firmware-side path`，送出 `CMD_V2(txn_id, opcode, payload)` 並等待 `CMD_RESULT`
6. `Firmware-side path` 收到 `CMD_RESULT.SUCCESS` 則 `succeeded`；`ERROR / REJECTED` 則 `failed`
7. 任一路徑若逾時未收到 terminal result 則 `timed_out`
8. retry 必須保留同一個 command intent，不得假裝成新的 live command
