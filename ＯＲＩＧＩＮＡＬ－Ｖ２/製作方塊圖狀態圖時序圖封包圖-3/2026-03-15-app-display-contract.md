---
title: App Display Contract — 三層欄位規格
status: detailed design spec
created: 2026-03-15
---

## 1. 目的

定義 Phone App 在裝置列表、裝置詳情、工程診斷三個層級應顯示的欄位與語意。
本文件是 UI contract，不是 UI 設計稿 — 只定「顯示什麼」，不定「長什麼樣」。

> 決策來源：device-inventory-and-sync-policy §7, architecture-decision-summary §2.3, sourced-resolution §3.6

---

## 2. 三層架構

| Layer | 對象 | 用途 |
|-------|------|------|
| **L1 — Device List** | 一般使用者 / 巡視者 | 快速掃一眼知道站點狀態 |
| **L2 — Device Detail** | Installer / 維護人員 | 查看單點詳情、執行操作 |
| **L3 — Engineer Debug** | Engineer / 開發者 | 底層 mapping、診斷、identity tracing |

---

## 3. L1 — Device List（列表卡片）

### GW 卡片

| Field | Source | Example |
|-------|--------|---------|
| `gw_name` | GW BLE name or user-set | `FGWAF37FD` |
| HA role | active / standby | `Active` |
| ED count | `gw_ed_roster_online_count()` / `gw_ed_roster_registered_count()` | `3/4 online` |
| Health | connectivity summary | `Online` / `Offline` |

### Registered ED 卡片

| Field | Source | Example |
|-------|--------|---------|
| `point_name` | roster entry | `泵房溫度點` |
| `operational_state` | `gw_point_state_name()` | `active` |
| Zone | last QoS zone | `MID` |
| RSSI | last RSSI value | `-56 dBm` |
| Connectivity | online / offline | `Online` |

### Unknown / New ED 卡片

| Field | Source | Example |
|-------|--------|---------|
| Device identity (partial) | BLE addr last 4 chars | `...74:11` |
| RSSI | scan RSSI | `-72 dBm` |
| Status | 固定標籤 | `未註冊` |

### 分組規則

已註冊 ED 依 `operational_state` 分組顯示：
1. **Online** — `active` + connectivity=online
2. **Offline** — `active` + connectivity=offline
3. **Maintenance** — `maintenance`
4. **Disabled** — `disabled`
5. **Other** — `retire_requested`, `commissioning`, etc.

---

## 4. L2 — Device Detail（詳情頁）

點擊 L1 卡片進入。

### Registered ED Detail

| Field | Source | Editable | Notes |
|-------|--------|----------|-------|
| `point_name` | roster | Yes (Installer+) | 同一 GW 下唯一 |
| `logical_slot` | roster | No | 固定，建立後不改 |
| `operational_state` | `gw_point_state` | Via actions | 不直接改，透過 action 觸發 |
| `sync_state` | `gw_ack` | No | `pending_sync` / `synced` / `needs_review` / ... |
| Zone | gw_qos | No | NEAR / MID / FAR / EDGE |
| RSSI | gw_qos | No | 即時更新 |
| Profile | gw_qos | No | FAST / BALANCED / ROBUST |
| PHY | gw_qos | No | 1M / 2M / Coded |
| TX Power | gw_qos | No | -8 ~ +8 dBm |
| Last seen | roster `last_seen_ms` | No | 相對時間 |

### Available Actions（依 operational_state + 權限）

| Action | Required State | Required Role | Description |
|--------|---------------|---------------|-------------|
| Enter Maintenance | `active` | Installer | → `maintenance` |
| Exit Maintenance | `maintenance` | Installer | → `active` |
| Disable | `active` / `maintenance` | Engineer | → `disabled` |
| Re-enable | `disabled` | Engineer | → `active` |
| Replace | `active` / `maintenance` | Installer | 換設備，保留 point identity |
| Request Retire | `active` / `maintenance` / `disabled` | Engineer | → `retire_requested` |
| Cancel Retire | `retire_requested` | Engineer | → `disabled` |

### sync_state Badge

| State | Badge Text | Color |
|-------|-----------|-------|
| `pending_sync` | Pending Sync | Amber |
| `synced` | Synced | Green |
| `sync_failed` | Sync Failed | Red |
| `needs_review` | Needs Review | Orange |
| `rejected` | Rejected | Red outline |

### needs_review 鎖定規則

當 `sync_state == needs_review` 時：
- **鎖定**：Replace, Rebind, Request Retire, Decommission
- **保留**：查看, 診斷, 備註, Retry Sync, Escalate

---

## 5. L3 — Engineer Debug（工程診斷頁）

從 L2 的隱藏入口進入（例如長按標題或 ENG_UNLOCK 後顯示）。

| Field | Source | Notes |
|-------|--------|-------|
| `point_uid` | system-generated | 不可變內部 ID |
| `logical_slot` | roster | 固定編號 |
| `conn_slot` | roster `conn_slot` | 動態 BLE conn index，offline 時顯示 `—` |
| `device_identity` | BLE addr full | `D7:AF:CB:1A:35:05 (random)` |
| `operational_state` (raw) | enum value | `OP_STATE_ACTIVE (3)` |
| `sync_state` (raw) | enum value | `SYNC_STATE_PENDING_SYNC (0)` |
| `ack_stage` | internal | `LOCAL_ACCEPTED` / `EDGE_RECEIVED` / ... |
| `reason_code` | if applicable | `BINDING_MISMATCH` |
| `retry_count` | roster | 連續重連失敗次數 |
| `last_seen` | roster `last_seen_ms` | absolute uptime |
| `roster_state` | roster state | `ONLINE` / `OFFLINE` / `RECONNECTING` / `EVICTED` |
| `base_revision` | if applicable | 最後一次治理變更依附的 revision |
| Binding history | if available | 先前綁定過的 device_identity 列表 |

### Mapping Trace

```text
point_name: "泵房溫度點"
  → point_uid: 0x0001
  → logical_slot: 0
  → conn_slot: 1 (dynamic)
  → device_identity: D7:AF:CB:1A:35:05 (random)
  → roster_state: ONLINE
  → operational_state: active
  → sync_state: synced
```

---

## 6. 語意一致性規則

以下語意在 GW / App / CC / Central 之間 **不允許漂移**：

| Term | 統一定義 | 禁止替代 |
|------|---------|---------|
| `logical_slot` | 固定點位編號 | ❌ `node_index`, `slot_id` |
| `conn_slot` | 動態 BLE conn index | ❌ `connection_id`, `link_id` |
| `operational_state` | 8 狀態 enum | ❌ 重新命名任何狀態 |
| `sync_state` | 5 狀態 enum | ❌ `synced/unsynced` 二分法 |
| `point_name` | 人類可讀名稱 | ❌ `device_name`, `node_name` |
| `device_identity` | 硬體身分 | ❌ `mac_address`（它不只是 MAC） |
| online / offline | connectivity state | ❌ `connected/disconnected`（那是 BLE 層） |

---

## 7. 資料來源對照

| App Field | GW Source | GATT Path | Notes |
|-----------|-----------|-----------|-------|
| point_name | gw_ed_roster | TBD (new GATT char or CMD response) | Phase 2 |
| operational_state | gw_point_state | TBD | Phase 2 |
| sync_state | gw_ack | TBD | Phase 2 |
| Zone / RSSI / PHY / TX | gw_qos → STATUS char | `0x2A1D` STATUS notify | 已有 |
| Online/Offline | gw_ed_roster | TBD | Phase 2 需新 GATT 暴露 |
| logical_slot / conn_slot | gw_ed_roster | TBD | Phase 2 |

Phase 1（目前）：App 只能透過 GW 的現有 GATT chars 讀 STATUS/RSSI/METRICS。
Phase 2：新增 GATT characteristics 或 CMD 子命令暴露 roster / state / identity 資訊。

---

## 8. 未決事項

- roster / state 資訊的 GATT 暴露方式（新 char vs CMD 子命令 vs composite response）
- `point_name` 的 GATT 寫入 / 讀取 protocol
- App 與 GW 之間的 inventory sync 頻率
- `needs_review` 的 UI 鎖定行為是否需要 GW 端配合
- Binding history 的儲存與傳輸格式
