# Upstream Evidence Audit — Field Detail

逐欄位盤點。主檔見 [../2026-04-15-upstream-evidence-audit.md](../2026-04-15-upstream-evidence-audit.md)。

## Central side

| Field | File:line | Type | Declaration | Notes |
|-------|-----------|------|-------------|-------|
| `updated_at` | F3:85, 115, 139, 153, 274 | authoritative ts | `updated_at: timestamp` | 無 tz 或 format；App local cache 為 `integer`（drift）|
| `revision` | F3:84, 243-245, 260 | version marker | `revision: integer` | optimistic concurrency；App 複本 nullable |
| `assignment_version` | F3:108、F2:116 | version marker | `uint32`，每次 +1 | 兩檔同意，防 stale write |
| `last_switch_at` | F3:109、F2:93 | authoritative ts | `timestamp?` nullable | 非 failover，僅切換 |
| `last_failover_at` | F3:114、F2:170 | authoritative ts | `timestamp?` nullable | canonical failover event ts |
| `lease_expire_at` | F3:150、F2:115 | authoritative ts | `timestamp?` (null=永不過期) | default timeout open question |
| `created_at` | F3:87, 261, 273 | authoritative ts | `timestamp` (DeviceMetadata)；`integer` (App local) | 無 freshness 用途；型別分叉 |

## Firmware side

| Field | File:line | Type | Status |
|-------|-----------|------|--------|
| `ts_device` | F3:225、F2:225 | observation ts | **ambiguous** — schema 有，無 GATT 實作（Phase 2）|
| `ts_gateway` | F3:226 | observation ts | **ambiguous** — 同上 |
| `ts_central` | F3:227 | observation ts | **ambiguous** — Central-side 生成可行但未定義 |
| `failover_generation` | F2:95, 125, 141, 171, 242 | version marker | exists → `ha_ctx.role_epoch` |
| `role_epoch` | F2:242 | version marker | firmware 內部名，對應 `failover_generation` |
| `uptime_s` | F1:277 | weak proxy | `uint32_t`，~49.7 天 wrap |
| `reset_count` | F1:278 | version marker | `uint16_t`，NVS persistent，wrap 65535 |
| `boot_id` | F2:184, 244 | version marker | **ambiguous** — 建議複用 `reset_count`，但方法 deferred |
| `msg_seq` | F2:185 | version marker | **ambiguous** — 明文「尚未實作」(F2:245) |
| `EVT.seq` | F1:182 | version marker | `uint8_t` per-type，wrap 255，僅 event drop detection |
| `GW_CFG_VERSION` | F1:282 | version marker | `uint32_t`，僅 GW_CFG 變更 |
| `FW_VERSION` | F1:257 | version marker | 靜態編譯期值，無 freshness 用途 |
| `PING.ed_ms` | F1:123 | weak proxy | ED-side uptime ms，僅 round-trip 用 |

## App side

| Field | File:line | Type | Status |
|-------|-----------|------|--------|
| `last_failover_generation` | F4:69 | version marker | App-local copy of firmware value |
| `profile_since` | F4:56 | authoritative ts | App-local only，無 threshold |
| `stale_flags` | F4:85 | weak proxy | **ambiguous** — 欄名存在，無 type/bit 定義 |
| `assignment_sync_state` | F4:68 | enum | 4-value：confirmed / pending_reconciliation / conflict / orphaned |
| `is_fresh` / `can_compare` | — | — | **missing** — 5 檔案全無 |
| `freshness window` / `stale_threshold` | F4:45 | — | **missing** — 僅 prose 提到，無數值 |
| `last_synced` / `not_compared` | — | — | **missing** — 無欄位或 state |

## Cross-file drift（需 owner repo 修）

1. **`updated_at` 型別分叉**：F3:85 為 `timestamp`，F3:274 App local cache 為 `integer`（推測 epoch ms）— 未記錄轉換規則
2. **`revision` nullable 分叉**：F3:84 非 null，F3:260 App local cache 為 `integer?` — 未命名該狀態
3. **`stale_flags` 無 schema**：F4:85 只有欄名，無 type/bit 定義
4. **`failover_generation` 在 F2 雙宣告**（lines 95 和 171）— canonical owner table 未釐清
5. **`boot_id` 實作分叉**：F2:244「可複用」`reset_count`，F2:222 又列為 open question
