# Event Taxonomy

主檔：[README.md](README.md)　Status：`draft-for-review`

事件分成有限 family。每個 family 定義 event_code 列表（本輪只列 representative，不 freeze 數值）。下游消費者（Page 4 / App debug / Central audit）依 family 過濾與分流。

## Families

### `BOOT`

device 啟動 / 重置 / role 初始化。

| Representative event_code | Severity | Notes |
|---|---|---|
| `BOOT_OK` | INFO | 對應現有 `[EVT] BOOT_OK role=... fw_ver=... profile=...` |
| `BLE_STACK_READY` | INFO | |
| `BOOT_ID_CONFIRMED` | INFO | 寫入 / 讀回 boot_id 後第一條 |
| `RESET_REASON` | INFO/WARN | brownout / watchdog / sw reset |
| `FATAL_INIT_FAIL` | FATAL | bt_enable_fail / NVS init fail |

### `BLE_LINK`

BLE 物理層連線生命週期。

| Representative | Severity | Notes |
|---|---|---|
| `ADV_READY` | INFO | role 開始 advertising |
| `SCAN_FOUND` | DEBUG/INFO | scan 看到候選 peer |
| `BLE_LINK_UP` | INFO | conn_idx, peer 角色 |
| `BLE_LINK_DOWN` | INFO/WARN | reason_code = HCI reason |
| `CONN_PARAM_UPDATE` | INFO | interval / latency / timeout |
| `MTU_UPDATE` / `PHY_CHANGED` | INFO | optional |
| `CONN_FAIL` | WARN | create_fail / disc_fail / conn_err |

### `ROSTER`

GW 端對 ED 的 attach / visibility 觀察。對應 reconciliation Page 4 的 Runtime evidence。

| Representative | Severity | Notes |
|---|---|---|
| `ED_SEEN` | INFO | scan 或 advertising 看到 ED |
| `ATTACH_VISIBLE` | INFO | ED 已掛上 GW slot |
| `ATTACH_NOT_VISIBLE` | INFO | roster 內無此 ED；對應 `Central only` 的 runtime side |
| `ROSTER_ONLINE` / `ROSTER_OFFLINE` | INFO | |
| `SLOT_ASSIGNMENT` | INFO | slot 變更 |

### `FAILOVER`

HA / 角色切換。

| Representative | Severity | Notes |
|---|---|---|
| `HEARTBEAT_LOST` | WARN | peer suspect |
| `HEARTBEAT_RESTORED` | INFO | |
| `PEER_DEAD` | WARN | hold-down 過 |
| `PROMOTE` / `DEMOTE` | WARN | role 升降 |
| `FAILOVER_GENERATION_INC` | WARN | failover_generation +1 |

### `CMD`

CMD_V2 / CMD_RESULT 生命週期。

| Representative | Severity | Notes |
|---|---|---|
| `CMD_RECEIVED` | INFO | correlation_id = txn_id |
| `CMD_ACCEPTED` | INFO | |
| `CMD_APPLIED` | INFO | |
| `CMD_FAILED` | WARN | reason_code |
| `CMD_REJECTED` | WARN | reason_code（含 permission denied）|

### `CC_RELAY`

CC bridge 的 relay / session 行為。**CC 只是 relay，不是 authority**。

| Representative | Severity | Notes |
|---|---|---|
| `CC_SESSION_OPEN` | INFO | App ↔ CC bridge 建立 |
| `CC_SESSION_CLOSE` | INFO | |
| `CC_FORWARDED` | INFO | command 經 CC 轉發 |
| `CC_RELAY_RESULT` | INFO/WARN | upstream 回 ack / error |

### `EVIDENCE_SNAPSHOT` *(future)*

供 Page 4 evidence / Central audit 撈 compact snapshot。本輪不展開，只佔位。

## Family 對應消費者（建議）

| Family | Page 4 evidence | App debug | Central audit |
|---|---|---|---|
| BOOT | optional | yes | partial |
| BLE_LINK | optional | yes | optional |
| ROSTER | yes | yes | yes |
| FAILOVER | yes | yes | yes |
| CMD | yes | yes | yes |
| CC_RELAY | partial | yes | partial |
| EVIDENCE_SNAPSHOT | yes | yes | yes |
