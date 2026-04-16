# Event Record Schema (minimum viable)

主檔：[README.md](README.md)　Status：`draft-for-review`

每個 firmware runtime event 至少帶以下欄位。**bounded size**；不允許無限長 log string。命名為 contract 用，不是 wire bit layout。

## 必要欄位

| Field | Type | Required | Source / Owner | Notes |
|---|---|---|---|---|
| `event_seq` | uint32 monotonic per (role, device_id, boot_id) | yes | Firmware | 同 device 同 boot 內單調遞增；用於本機排序與偵測缺漏。**不保證跨 device 全域順序** |
| `boot_id` | uint32 | yes | Firmware（NVS） | Phase 0 可暫對應現有 `reset_count`（uint16）；命名差異與 wrap 風險見 open-questions |
| `uptime_ms` 或 `uptime_s` | uint32 | yes | Firmware | device local elapsed time；**不是 wall-clock** |
| `role` | enum `GW / ED / CC` | yes | Firmware | 對齊 RML actor |
| `device_id` 或 `local_id` | string / hex | yes | Firmware | 短 stable id；MAC 等 transport id 是 fallback |
| `peer_id` | string / hex / slot | optional | Firmware | 視 family 而定（GW peer / ED slot / ed_hash / conn_handle）|
| `event_family` | enum | yes | 見 [event-taxonomy.md](event-taxonomy.md) |
| `event_code` | enum / id | yes | 見 [event-taxonomy.md](event-taxonomy.md) |
| `severity` | enum `DEBUG / INFO / WARN / ERROR / FATAL` | yes | Firmware | 不要混入 ALARM 業務語意；ALARM 應由 family/code 表達 |
| `state_before` | string / enum | optional | Firmware | 適用於有狀態變化的 event（連線、failover）|
| `state_after` | string / enum | optional | Firmware | 同上 |
| `reason_code` | enum / id | optional | Firmware | 對應 BLE HCI reason、CMD reject 等 |
| `source_path` | enum `Firmware-side / Central-side bridge` | optional | Firmware | 對應 reconciliation `session topology` 用詞 |
| `correlation_id` | string / hex | optional | Firmware | command id / msg_seq / EVT.seq / relay id；用於關聯多 event |
| `human_message` | bounded string（≤ 80 bytes 建議）| yes | Firmware | UI fallback；非 i18n 鍵；不放 PII |
| `payload` | bounded key-value（≤ 8 keys，每 value ≤ 32 bytes 建議）| optional | Firmware | 不允許巢狀任意結構 |

## Receive-side 欄位（接收者加註，不算 firmware 原始 event 的一部分）

| Field | Owner | Notes |
|---|---|---|
| `central_received_at` | Central | 接收時間，**不是 device 發生時間** |
| `app_received_at` | App | 同上 |

## 不在 schema 內

- Wall-clock timestamp 來源（device 端目前無；見 open-questions Q3）
- 全域 sequence（跨 device）
- 任意長度 log message
- 任意巢狀 JSON payload
- i18n 用 message key（先用人話 `human_message`）
- App / Central derived state（如 `can_compare` / `recommended_action`）— 這些屬 App layer，不是 firmware event

## Severity 對應

| Severity | 範例 | 是否進 Central audit |
|---|---|---|
| DEBUG | scan tick | no |
| INFO | BLE_LINK_UP / ROSTER 更新 / 已收 CMD | optional |
| WARN | CONN_FAIL / TX_EAGAIN / heartbeat suspect | recommended |
| ERROR | bt_enable_fail / NVS write fail / failover trigger | yes |
| FATAL | system halt | yes |
