# Test Cases

| ID | Covers | Requirement | Feature | Preconditions | Steps | Expected | Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TC-001` | `AC-001` | `REQ-001` | `RML-FEA-001` | 已連線 Gateway；可讀 `STATUS` / `METRICS_V2` | 開啟 detail，刷新 telemetry | RSSI / PDR / latency / jitter 依 payload 顯示 | screenshot, parsed log |
| `TC-002` | `AC-001` | `REQ-001` | `RML-FEA-001` | 注入 P0 sparse payload 與 stale snapshot | 先顯示完整值，再送 sparse / stale | sparse 顯示 `--`；stale 保留最後值 + hint | capture, screenshot |
| `TC-003` | `AC-002` | `REQ-002` | `RML-FEA-002` | 一組裝置有 `CAPS_V2`；另一組只有 `CAP` | 讀 capability 後查看 UI action | 有 capability 才可操作；fallback 成功 | caps payload, screenshot |
| `TC-004` | `AC-003` | `REQ-003` | `RML-FEA-003` | device detail 可見 `stableId`、MAC、Central metadata；可切換到 CC bridge session | 開 detail 與 metadata sync；再切換 session 到 CC bridge，確認 Gateway / End Device 名稱有 relayed 標示 | UI 以 `stableId` 為主；MAC 有來源標示；Central 請求用 `central_ref`；CC bridge session 下名稱標示 relayed / cached | screenshot, API log |
| `TC-005` | `AC-004` | `REQ-004` | `RML-FEA-004` | 建立 Central 與 runtime gateway 不一致 fixture | 開 detail / roster，再讓兩端收斂 | 先顯示 dual gateway + badge；收斂後 badge 消失 | screenshot before/after |
| `TC-006` | `AC-005` | `REQ-005` | `RML-FEA-003` | local pending queue 啟用；Central 可回 `200` 與 `409` | 先 rename 成功，再重做一次 conflict | success 清 pending；conflict 保留 pending 並提示 | pending log, 409 fixture |
| `TC-007` | `AC-006` | `REQ-006` | `RML-FEA-002` | 可連 `Gateway / End Device` 與 `CC bridge`；Central path 有 command API / sync fixture | 分別在 `Firmware-side path` 與 `Central-side path` 送 action；前者回 `SUCCESS`、`ERROR`、`REJECTED`，後者先回 accepted 再回 final confirmation | UI 依 path 顯示正確狀態；`accepted` 不冒充完成 | cmd write log, result capture, API/sync log |
| `TC-008` | `AC-006` | `REQ-006` | `RML-FEA-002` | 可抑制 `CMD_RESULT` 或 Central-side final confirmation | 送 action 不回 terminal result 直到 timeout，再 retry 並回成功 | 先進 `timed_out`，retry 後成功；retry 保留同一個 command intent | timeout log, retry log |
| `TC-009` | `AC-004` | `REQ-004`, `REQ-008` | `RML-FEA-004` | 只連近端 Gateway，無 Central 即時資料；Central reference 欄位（`updated_at` / `revision`）不存在或顯示為過期 | 開 detail；觀察 reconciliation state | 顯示 `not compared` 或 `last synced`；不出現 `conflict`；freshness hint 可見 | screenshot, stale_reference_fixture |
| `TC-010` | `AC-005` | `REQ-005` | `RML-FEA-003` | 無 pending rename；Central 有 alias | 開 detail | 顯示順序為 `central > cached > DEVICE_ALIAS > adv_name` | screenshot |
| `TC-011` | `AC-006` | `REQ-006` | `RML-FEA-002` | Firmware-side path 回 `REJECTED`；或 Central-side path 回 permission denied | 送 command；觀察 UI feedback | App 顯示明確拒絕；不允許靜默重試 | cmd_result_capture, permission_error_log |
| `TC-012` | `AC-004` | `REQ-008` | `RML-FEA-004` | 建立 Central 與 runtime 皆有 active gateway 且值不同，但 Central reference 為 stale / last synced，不在 freshness window 內 | 開 detail；觀察 reconciliation state | `can_compare == false`；不得顯示 `conflict`；必須顯示 `not compared` 或 `last synced` + freshness hint | screenshot, not_compared_screenshot, stale_reference_fixture |

## Coverage Check

- normal: `TC-001`, `TC-004`, `TC-006`
- boundary: `TC-002`, `TC-003`
- timeout: `TC-008`
- retry: `TC-008`
- fault injection: `TC-007`
- recovery: `TC-005`, `TC-008`
- not-compared: `TC-009`
- no-pending-precedence: `TC-010`
- permission-denied: `TC-011`
- cc-bridge-relayed: `TC-004`
- can-compare-gate: `TC-012`
