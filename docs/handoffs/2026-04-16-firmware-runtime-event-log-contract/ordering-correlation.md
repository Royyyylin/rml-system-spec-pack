# Ordering & Correlation

主檔：[README.md](README.md)　Status：`draft-for-review`

## 順序保證（hard rules）

- **單一 device 內**只保證 `(role, device_id, boot_id, event_seq)` 的單調遞增；
  - 同一 boot 內 `event_seq` 單調 +1
  - boot_id 變更後 event_seq 從 0 重新計
- **跨 GW / ED / CC** **不保證真全域順序**；除非未來導入 synchronized clock 或全域 event broker
- `uptime_ms / uptime_s` 只能表示 device local elapsed time，**不是 wall-clock**；不能跨 device 比較絕對時間
- `central_received_at` / `app_received_at` 是接收時間，**不是 device 發生時間**；只能用來標收到順序，不可逆推 device 順序

## 既有 wire 的限制

- `EVT.seq`（GATT char `6f8a9c13`）目前是 `uint8_t per-type, for drop detection`：
  - per type 計數（ALARM / INFO 各自）
  - **8-bit wrap**（255 後 0）
  - **per-type 不是全域**：跨 family 不共序
  - **不可誤當全域 event order**；只能用作 drop detection
- `msg_seq` 在 `feature-assignment-reconciliation.md` / `data-model.md` 出現，但**目前 firmware 尚未實作**（見 `2026-04-15-upstream-evidence-audit.md`）；本 contract 不假設它已存在
- 若日後正式 wire 改成 `event_seq`（per-device 全 family 共用），需明文標示與 `EVT.seq` 並存或取代

## Correlation patterns

- **同一個 command lifecycle** ：`CMD_RECEIVED` / `CMD_ACCEPTED` / `CMD_APPLIED` / `CMD_FAILED` 共用 `correlation_id = txn_id`
- **同一個 failover episode**：`HEARTBEAT_LOST` / `PEER_DEAD` / `PROMOTE` / `FAILOVER_GENERATION_INC` 共用 `correlation_id = failover_episode_id`（建議用 `failover_generation` 序號）
- **同一個 CC relay**：`CC_SESSION_OPEN` → `CC_FORWARDED` → `CC_RELAY_RESULT` 共用 `correlation_id = relay_id`
- **roster 觀察與 reconciliation**：`ATTACH_VISIBLE` / `ATTACH_NOT_VISIBLE` 在 Page 4 evidence 引用時，App 端用 `peer_id (ed)` 串接 Central assignment evidence；不需要 firmware 端統一 correlation_id

### BLE_LINK lifecycle correlation（target / draft）

**現況**：firmware 兩端 (GW / ED) 各自 emit 自己的 `BLE_LINK_UP` / `BLE_LINK_DOWN` / `CONN_PARAM_UPDATE`。**目前沒有共享的 `link_session_id`**；每側只看得到自己的 `conn_idx` / `conn_handle`，對端的 handle 不可見。

**Target rule（draft，待 firmware 確認後鎖定）**：

- 同一條 BLE 連線兩端的 BLE_LINK family event 應共享 `correlation_id = link_session_id`
- 候選組成方式（待選一個）：
  1. `(initiator_role, peer_addr, central_conn_handle, link_open_uptime_ms)` 拼湊 hash
  2. GW 側生成、寫入連線早期 GATT exchange，由 ED 端記入後續 event
  3. 由 App / Central 端在收到兩側 event 後做 best-effort 對齊（fallback；不算共享 id）
- 在 `link_session_id` 落地前，**App / Central 端 best-effort 對齊**：用 `peer_addr` + `event_seq` 接近 + `uptime_ms` 接近做 heuristic match；明標為「probable pairing」，不可作為 audit 真相
- BLE_LINK_DOWN 必須帶 `reason_code`（HCI reason）以利兩側對端互相比對

**Open question**：見 [open-questions.md](open-questions.md) Q9（已從原 7 題擴增）。

## 斷線/重連 debug 預期可組出的 trace

依 `event_seq` 排序，應能看出（以 ED 為例）：

```
ADV_READY → SCAN_FOUND → BLE_LINK_UP → (subscribe / discover) →
ROSTER 對應端 ATTACH_VISIBLE → CMD lifecycle →
HEARTBEAT_LOST → PEER_DEAD → FAILOVER_GENERATION_INC →
BLE_LINK_DOWN（reason） → ADV_READY → ...
```

跨 GW / ED 的順序對齊**靠 correlation_id**，不靠時間。

## 不在本輪保證

- 真實全域 wall-clock
- 跨 device 的精確 happens-before（B happened after A on different devices）
- guaranteed delivery（dropped event 必須由消費者察覺；建議 firmware 端報 `dropped_count`）
- replay / resume after disconnect（屬 wire / uplink layer 設計，見 implementation-phases.md Phase 2）
