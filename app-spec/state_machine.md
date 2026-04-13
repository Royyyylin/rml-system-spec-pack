# State Machine

## `STA-001` TelemetryValueState

| State | Meaning | Display Rule |
| :--- | :--- | :--- |
| `present` | 來自完整 payload 的有效值 | 顯示數值 |
| `sparse` | P0 profile 刻意省略欄位 | 顯示 `--` + `sparse` hint |
| `stale` | 曾有值，但已超出 freshness window | 顯示最後值 + `stale` hint |
| `unknown` | 裝置尚未收到該欄位 | 顯示 `--` |
| `not_synced` | Central 尚未完成該裝置同步 | 顯示 `--` + `not synced` |

## `STA-002` AssignmentSyncState

| State | Meaning |
| :--- | :--- |
| `confirmed` | Central 與 firmware 指向相同 active gateway |
| `pending_reconciliation` | runtime 已變，Central 尚未追上 |
| `conflict` | 兩端皆有 active gateway，但值不同 |
| `orphaned` | 無 Central assignment，亦無 runtime attach |
| `central_only` | Central 有 assignment，但 runtime 尚未可見 |

## `STA-003` Alias Sync Op State

| State | Meaning |
| :--- | :--- |
| `clean` | 無 local pending op |
| `pending` | local optimistic update 已建立，待 Central push |
| `conflicted` | Central 回 `409 Conflict` |
| `failed` | 非 conflict 的 network / auth / server failure |

## `STA-004` Command Execution State

| State | Meaning |
| :--- | :--- |
| `idle` | 尚未送出操作 |
| `in_flight` | command 已送出，等待 path-specific 第一個回饋 |
| `accepted` | `Central-side path` 已 accepted，但尚未看到 final authoritative confirmation |
| `succeeded` | path-specific final success 已到位；`Firmware-side path` 對應 `CMD_RESULT.status=SUCCESS`，`Central-side path` 對應 metadata / sync confirmation |
| `failed` | `CMD_RESULT.status=ERROR/REJECTED`、API reject、permission denied、或 authoritative failure |
| `timed_out` | 超過 timeout 仍未取得 path-specific terminal result |
| `retrying` | App 以同一個 command intent 重試，之後回到 `in_flight` |

## Transition Notes

- `STA-001` 由 payload completeness 與 freshness 決定，不由 UI 猜測
- `STA-002` 由 `authoritativeGatewayId` 對 `runtimeGatewayId` 比對決定
- `STA-003` 由 local pending queue 與 Central response 決定
- `STA-004` 先由 current live peer 決定合法 path：`CC bridge -> Central-side path`；`Gateway / End Device -> Firmware-side path`
- `accepted` 只代表上游已收單，不等於 final state applied
- `STA-004` 由 `txn_id` 與 path-specific feedback 決定；retry 保留同一個 command intent
