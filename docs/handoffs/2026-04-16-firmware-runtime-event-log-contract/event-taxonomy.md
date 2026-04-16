# Event Taxonomy

主檔：[README.md](README.md)　Status：`draft-for-review`

事件分成有限 family。每個 family 列 representative event_code（本輪不 freeze 數值）。下游消費者依 family / severity 過濾。

## Families

### `BOOT` — device 啟動 / 重置 / role 初始化

| Representative | Severity | Notes |
|---|---|---|
| `BOOT_OK` / `BLE_STACK_READY` | INFO | 對應現有 `[EVT] BOOT_OK ...` / `[EVT] BLE_STACK_READY` |
| `BOOT_ID_CONFIRMED` | INFO | 寫入 / 讀回 boot_id 後第一條 |
| `RESET_REASON` | INFO/WARN | brownout / watchdog / sw reset |
| `FATAL_INIT_FAIL` | FATAL | bt_enable_fail / NVS init fail |

### `BLE_LINK` — BLE 物理層連線生命週期

| Representative | Severity | Notes |
|---|---|---|
| `ADV_READY` | INFO | role 開始 advertising |
| `SCAN_FOUND` | DEBUG/INFO | scan 看到候選 peer |
| `BLE_LINK_UP` | INFO | conn_idx, peer 角色 |
| `BLE_LINK_DOWN` | INFO/WARN | reason_code = HCI reason |
| `CONN_PARAM_UPDATE` | INFO | interval / latency / timeout |
| `MTU_UPDATE` / `PHY_CHANGED` | INFO | optional |
| `CONN_FAIL` | WARN | create_fail / disc_fail / conn_err |

### `ROSTER` — GW 端 ED attach / visibility（Page 4 Runtime evidence 主要來源）

| Representative | Severity | Notes |
|---|---|---|
| `ED_SEEN` | INFO | scan 或 advertising 看到 ED |
| `ATTACH_VISIBLE` / `ATTACH_NOT_VISIBLE` | INFO | 後者對應 `Central only` 的 runtime side |
| `ROSTER_ONLINE` / `ROSTER_OFFLINE` / `SLOT_ASSIGNMENT` | INFO | slot 與成員變更 |
| `TOPOLOGY` / `TOPOLOGY_PEER` | INFO | 既有 `[EVT] TOPOLOGY ...`（GW emits 30s）|
| `TOPOLOGY_BRIDGE` | INFO | CC 端 `[EVT] TOPOLOGY role=CC`；只是 relay 視角，非 authority |

### `FAILOVER` — HA / 角色切換 / link 健康度（**僅限 HA peer 健康度與 role 變更**；不含週期性 QoS metrics）

| Representative | Severity | Notes |
|---|---|---|
| `HEARTBEAT_LOST` / `HEARTBEAT_RESTORED` | WARN/INFO | HA peer suspect / 恢復（不是 QoS rolling metrics）|
| `PEER_DEAD` | WARN | hold-down 過 |
| `PROMOTE` / `DEMOTE` | WARN | role 升降 |
| `FAILOVER_GENERATION_INC` | WARN | failover_generation +1 |

### `CMD` — CMD_V2 / CMD_RESULT 生命週期

| Representative | Severity | Notes |
|---|---|---|
| `CMD_RECEIVED` / `CMD_ACCEPTED` / `CMD_APPLIED` | INFO | correlation_id = txn_id |
| `CMD_FAILED` / `CMD_REJECTED` | WARN | reason_code（含 permission denied）|

### `CC_RELAY` — CC bridge relay / session（CC 只是 relay，不是 authority）

| Representative | Severity | Notes |
|---|---|---|
| `CC_SESSION_OPEN` / `CC_SESSION_CLOSE` | INFO | App ↔ CC bridge |
| `CC_FORWARDED` | INFO | command 經 CC 轉發 |
| `CC_RELAY_RESULT` | INFO/WARN | upstream 回 ack / error |

### `UPLINK` — uplink dispatch / ring buffer / backend drain（對應 reliability Phase 3 `uplink_ring`）

| Representative | Severity | Notes |
|---|---|---|
| `UPLINK_DISPATCH` | INFO | 既有 `[EVT] UPLINK_DISPATCH frame_family=P0/P1 type=0xNN seq=N`；**Phase 0 標準化時把原 `family=` 改名 `frame_family=` 以避免與本 contract `event_family` 同名衝突** |
| `UPLINK_RING_EVICT` *(future)* | WARN | Class C/B 被 eviction |
| `UPLINK_RING_REJECT` *(future)* | ERROR | Class A 拒收 / 滿載 |
| `UPLINK_DRAIN_OK` / `UPLINK_DRAIN_FAIL` *(future)* | INFO/WARN | drain → backend 結果 |

### `EVIDENCE_SNAPSHOT` *(future)* — Page 4 / Central audit compact snapshot；本輪只佔位

## 本輪不收編的 tag（deferred / temporary mapping）

- **`QOS_HEARTBEAT`**（既有 `[EVT] QOS_HEARTBEAT pdr/lat/jit/conn`，gw_qos.c emits rolling QoS metrics）：屬週期性 runtime metrics，與 `role-mapping.md` 「telemetry / measurement 本身不算 event」主軸一致；**不歸 FAILOVER**，本輪也不正式收編到任何 family。後續決策（新增 `RUNTIME_HEALTH` family、改走 STATUS/METRICS_V2 telemetry stream、或拆成「rolling QoS + threshold 違反才升級為 event」）見 [open-questions.md](open-questions.md) Q10

## Family 對應消費者（建議）

| Family | Page 4 evidence | App debug | Central audit |
|---|---|---|---|
| BOOT | optional | yes | partial |
| BLE_LINK | optional | yes | optional |
| ROSTER | yes | yes | yes |
| FAILOVER | yes | yes | yes |
| CMD | yes | yes | yes |
| CC_RELAY | partial | yes | partial |
| UPLINK | partial | yes | partial |
| EVIDENCE_SNAPSHOT | yes | yes | yes |
