# Acceptance Criteria

## `AC-001` Telemetry Display

Requirement: `REQ-001`
Feature: `RML-FEA-001`

- 對 `STATUS` / `METRICS_V2` 解析出的數值，`present` / `stale` 顯示數值，`sparse` / `unknown` / `not_synced` 顯示 `--`
- `sparse` 必須顯示為正常資料狀態，不得顯示為 error
- `stale` 必須保留最後值並顯示 `stale` hint

## `AC-002` Capability Gate

Requirement: `REQ-002`
Feature: `RML-FEA-002`

- `CAPS_V2` 存在時，功能 gating 必須以 `CAPS_V2` 為準
- `CAPS_V2` 不存在時，App 必須 fallback `CAP`
- 未宣告 capability 的功能不可在 UI 可操作

## `AC-003` Identity Boundary

Requirement: `REQ-003`
Feature: `RML-FEA-003`

- App 內部裝置主鍵顯示與儲存以 `stableId` 為主；`central_ref` 僅作 Central metadata 對應鍵
- 若畫面顯示 MAC，必須標示它是 transport identity
- Central metadata / sync 請求必須以 `central_ref` 對應，不得以 MAC 直接當 app PK
- 若當前只連到 `CC bridge`，顯示 `Gateway` / `End Device` 名稱時，必須標示為 relayed / cached，不得視為第一手 BLE observation

## `AC-004` Assignment Reconciliation

Requirement: `REQ-004`
Feature: `RML-FEA-004`

- Central 與 runtime gateway 一致時，不顯示 reconciliation badge
- 不一致時，detail / roster 必須可見 `assignmentSyncState`
- `pending_reconciliation` / `conflict` 時，畫面必須同時顯示 Central Gateway 與 Runtime Gateway
- 若當前 session 無可比較的 Central 即時資料，不得顯示 `conflict`；應顯示 `not compared` 或 `last synced` 語意

## `AC-005` Alias Precedence

Requirement: `REQ-005`
Feature: `RML-FEA-003`

- 有 pending op 時：`local_pending > central > cached > DEVICE_ALIAS > adv_name`
- 無 pending op 時：`central > cached > DEVICE_ALIAS > adv_name`
- `409 Conflict` 不可靜默覆蓋 local pending 結果

## `AC-006` Command Round Trip

Requirement: `REQ-006`
Feature: `RML-FEA-002`

- current live peer 必須先決定合法 command path：`CC bridge -> Central-side path`；`Gateway / End Device -> Firmware-side path`
- `Firmware-side path` 的新 app action 必須透過 `CMD_V2` 送出非零 `txn_id`
- `Firmware-side path` 收到 `CMD_RESULT` `SUCCESS` 時進成功狀態；`ERROR` / `REJECTED` 時進失敗狀態
- `Central-side path` 收到 accepted 時不可直接視為完成；必須等 metadata / sync / authoritative confirmation 才可視為 final success
- `Firmware-side path` 收到 `REJECTED` 或 `Central-side path` 回覆 permission denied 時，App 顯示明確拒絕，不得靜默重試
- 若超過 configured timeout 未收到 path-specific terminal result，必須進 `timed_out`
- Assumption: 本 pack 暫以 async command `30s` 為驗收 timeout；若 app timeout matrix 有更新，以 repo SSOT 回寫本條
