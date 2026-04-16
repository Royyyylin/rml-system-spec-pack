# Role Mapping

主檔：[README.md](README.md)　Status：`draft-for-review`

GW / ED / CC 各自負責吐哪些 family。**App / Central 是消費者或 audit owner，不是 firmware event source**。

## GW（Gateway）

GW 是 ED coordination + uplink 的 owner。負責：

| Family | 必要性 | Notes |
|---|---|---|
| BOOT | required | role=GW，含 BLE_STACK_READY、BOOT_OK |
| BLE_LINK | required | GW 端的 conn / disconn / param update |
| ROSTER | **required** | ED 觀察、attach visibility、slot 變更 — Page 4 Runtime evidence 主要來源 |
| FAILOVER | **required** | heartbeat / peer suspect / promote / demote / `failover_generation` 變更 |
| CMD | required | GW 收到 / 轉發 / 套用的 command 結果 |
| CC_RELAY | n/a | GW 不擔任 CC bridge |

## ED（End Device）

ED 是 measurement + own BLE link 的 owner。負責：

| Family | 必要性 | Notes |
|---|---|---|
| BOOT | required | role=ED |
| BLE_LINK | required | ED 自己的 conn / disconn |
| ROSTER | n/a | ED 不維護 roster；attach visibility 由 GW 觀察並紀錄 |
| FAILOVER | optional | ED 端對 GW 失聯的觀察 |
| CMD | required | ED 收到的 command apply 結果（`CMD_APPLIED` / `CMD_FAILED`）|
| CC_RELAY | n/a | |

ED 端的 telemetry / measurement 本身**不算 event**（屬 STATUS / METRICS_V2），但 measurement-driven 的異常（QoS event）可走 BLE_LINK 或新增 family。

## CC（Bridge）

CC 是 BLE-to-Central 的 relay。**不是 authority owner**。負責：

| Family | 必要性 | Notes |
|---|---|---|
| BOOT | required | role=CC |
| BLE_LINK | required | CC 對 App 的 BLE link |
| ROSTER | n/a | CC 不維護 roster |
| FAILOVER | n/a | CC 不參與 HA |
| CMD | optional | 經 CC 轉發的 CMD 結果（也可由 CC_RELAY family 表達）|
| CC_RELAY | **required** | session / forwarded / relay_result — 唯一 owner |

**CC 不可用 event 宣稱 assignment / runtime truth**；CC 出的 event 都標 `source_path = Central-side bridge`，下游 App / Central 端清楚這只是 relay 視角。

## App / Central 的角色

- **App**：消費 firmware event，做 Page 4 Engineering details 顯示、Recent events、本機 debug；也加註 App-side derived state（`can_compare` / `recommended_action` / `app_received_at`）— 這些**不會反向寫回 firmware event**
- **Central**：消費高 severity / 指定 family 的 event 寫進 audit；也加註 `central_received_at`、`audit_record_id`；不會把自己的 derived state 假裝成 firmware event

## 不允許的事

- App / Central 端產生的 event **不可標 `role = GW/ED/CC`**；要另立 source 標籤（如 `app_event` / `central_event`），不混入本 contract
- CC 不可發 ROSTER / FAILOVER family event
- ED 不可發 ROSTER family event（ED 不維護 roster）
- 任何角色不可用 firmware event 直接覆寫 Central canonical assignment 或 App display state
