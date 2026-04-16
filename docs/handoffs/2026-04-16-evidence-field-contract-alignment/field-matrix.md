# Evidence Field Matrix

主檔：[README.md](README.md)　Status：`draft-for-review`

Status legend：
- `available` — owner SSOT 已實作 / 已宣告，可直接引用
- `candidate` — schema 有但 implementation 仍 deferred / 待選擇
- `missing` — owner SSOT 尚未提供
- `derived` — App 在本機計算，**不上 wire**

## Central side（authoritative）

| UI concept | Page 4 mock | proposed contract | owner | source / file | raw vs derived | freshness role | status | notes |
|---|---|---|---|---|---|---|---|---|
| assigned gateway | `assigned_gateway` | `active_gateway_id` | Central | `central-device-metadata/docs/specs/data-model.md` (EdAssignment) | raw | identity | available | 已存在 |
| assignment source | `source` (Central Assignment API) | （描述用，非欄位）| Central | Assignment API spec | label | — | available | UI label |
| owner | `owner` (Central) | （描述用）| Central | RML | label | — | available | 顯示用 |
| sync age | `sync_age` (e.g. `3s 前`) | `central.age = now − updated_at` | App derived | derived from `updated_at` | derived | freshness 計算 | derived | UI 字串，不上 wire |
| revision | `revision` | `revision` | Central | F3:84 DeviceMetadata | raw | version marker | available | 也用於 `409 Conflict` |
| assignment_version | — | `assignment_version` | Central | F3:108 / F2:116 | raw | version marker | available | 防 stale write |
| updated_at | `updated_at` | `updated_at` | Central | F3:85, 115, 139, 153 | raw | authoritative ts | available | 型別精度未鎖（timestamp vs integer epoch ms）|
| last_synced_at（App→Central）| —（未顯示）| `last_synced_at` | App derived | App pull-time | derived | App 端追蹤 | missing | App repo 應補 |
| central_reference_is_fresh | （隱含）| `central_reference_is_fresh` | App derived | derived from `updated_at` + window | derived | compare gate input | missing | App 應 formalize |

## Runtime side（observed）

| UI concept | Page 4 mock | proposed contract | owner | source / file | raw vs derived | freshness role | status | notes |
|---|---|---|---|---|---|---|---|---|
| observed gateway | `observed_gateway` | `runtimeGatewayId` | Firmware → App | F2:95 (`failover_generation` ↔ `ha_ctx.role_epoch`)；roster | raw | observation | available | App-local mirror = `last_failover_generation` |
| runtime attach visibility | `gw = —（attach not visible）` | （derived label）| App derived | derived from roster / no-attach | derived | central_only 區分 | derived | 不是 wire 欄位 |
| source path | `source_path` (Firmware-side · notify / roster) | （描述用）| App | METRICS_V2 / EVT / ROSTER_LIST | label | — | available | UI label |
| observed age | `observed_age` (`5s 前`) | `runtime.age = now − observed_at_proxy` | App derived | derived | derived | freshness 計算 | derived | proxy 來源見下 |
| observed_at | `observed_at` (Phase 2) | `observed_at` | Firmware | F3:225 TelemetryEnvelope (Phase 2 deferred) | raw | wall-clock ts | candidate | 目前**無 GATT 實作**；用 proxy 過渡 |
| age proxy（過渡）| —（隱含）| `failover_generation` + `uptime_s` + `EVT.seq` | Firmware | F1:182 / F1:277 / F2:95 | raw | freshness proxy | available | Phase 2 ts 出來前的過渡組合 |
| event source | `event_source` (METRICS_V2 + EVT) | （描述用）| App | F1 各 characteristic | label | — | available | UI label |
| boot_id | — | `boot_id` | Firmware | F2:184 / F2:244 (`reset_count` 提案) | raw | session 區分 | candidate | 實作方式 deferred |
| msg_seq | — | `msg_seq` | Firmware | F2:185 | raw | dedup | missing | 明文「尚未實作」|
| GW_CFG_VERSION | — | `GW_CFG_VERSION` | Firmware | F1:282 | raw | gw config 版本 | available | 範圍限 GW_CFG，非通用 |
| runtime_observation_is_fresh | （隱含）| `runtime_observation_is_fresh` | App derived | derived from age proxy + window | derived | compare gate input | missing | App 應 formalize |

## App derived（compare gate / reconciliation state / action）

| UI concept | Page 4 mock | proposed contract | owner | source / file | raw vs derived | role | status | notes |
|---|---|---|---|---|---|---|---|---|
| can_compare | `can_compare` | `can_compare` | App | App local | derived | gate result | missing | 對齊 spec：`true` 才進 FSM |
| compare reason | `reason` | `compare_reason` | App | App local | derived | gate diagnostic | missing | UI 顯示用 |
| mismatch_field | `mismatch_field` | `mismatch_field` | App | App local | derived | diff key | missing | conflict = `gateway`；其他 = `—` |
| reconciliation state | （summary state）| `assignmentSyncState` | App | F4:68 (4-value enum) | derived | FSM state | available | 既有 4-value enum；UI 加 `Not compared`（pre-FSM gate）/ `Pending sync`（label of `pending_reconciliation`）|
| Not compared / last synced | UI label | `Not compared` | App | App local | derived | pre-FSM gate result | missing | 不在 4-value enum 內，需 App 補 |
| Central only | UI label | `central_only` | App | F4:68 enum | derived | FSM state | available | 對齊 spec：`can_compare = true`，attach not visible |
| Conflict | UI label | `conflict` | App | F4:68 enum | derived | FSM state | available | both fresh + 值不同 |
| recommended action | Page 3 strip | `recommended_action` | App | App local | derived | UI hint | missing | 5 個情境各對應一組 |
| action risk level | `danger / primary` | `action_risk_level` | App + Central | mock | derived + spec | UI weight | missing | spec 未定 |
| Engineer confirmation | hint | （流程要求）| Central + App | mock | spec rule | gate before write | missing | 需 Central 或 App spec 寫 |
| reason（變更原因）| hint | `reason` | Central API | mock | raw | audit payload | missing | 需 Central API 寫 |
| audit record | hint | `audit_record` | Central | mock | raw | audit log | missing | 需 Central audit spec |
