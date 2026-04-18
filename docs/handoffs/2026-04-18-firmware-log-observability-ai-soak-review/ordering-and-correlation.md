# Ordering & Correlation Model

主檔：[README.md](README.md)

## Single-Device Ordering（硬規則）

- 同一 device 內保證 `(role, device_id, boot_id, event_seq)` 單調遞增
- 同一 boot 內 `event_seq` 單調 +1
- `boot_id` 變更後 `event_seq` 從 0 重新計
- `uptime_ms / uptime_s` 是 device local elapsed time，**不是 wall-clock**

## Cross-Device Ordering（無保證）

- **GW / ED / CC 之間不保證全域順序**
- 不可直接比較不同 device 的 `uptime_ms`（獨立 clock，值不同步）
- `app_received_at` / `central_received_at` 是**接收時間**，不是 device 發生時間
- 只能用來標「收到的順序」，不可逆推 device 順序

## Correlation Patterns

| Lifecycle | Correlation ID | 關聯 Events |
|---|---|---|
| Command | `txn_id` | CMD_RECEIVED → CMD_ACCEPTED → CMD_APPLIED / CMD_FAILED |
| Failover | `failover_generation` | HEARTBEAT_LOST → PEER_DEAD → PROMOTE → FAILOVER_GEN_INC |
| CC Relay | `relay_id` | CC_SESSION_OPEN → CC_FORWARDED → CC_RELAY_RESULT |
| BLE Link | future `link_session_id` | BLE_LINK_UP (GW) ↔ BLE_LINK_UP (ED) |

## CC Bridge 限制

- CC 出的 event 都標 `source_path = Central-side bridge`
- CC 是 relay，不是 authority
- AI reviewer 不可把 CC 的 relay event 當成 first-hand observation
- CC 的 BLE_LINK event 跟 GW 的 BLE_LINK event 是不同 link（CC↔GW vs GW↔ED）

## AI Reviewer 排序規則

- **單一 device log**：可按 `event_seq` 排序，判斷 sequence gap
- **跨 device**：只能用 `correlation_id` 配對，不可用 time proximity
- **probable pairing**（peer_addr + receive-time 近似）：標為 probable，不可寫成 confirmed
- **AI report 不可宣稱跨 device ordering certainty**
