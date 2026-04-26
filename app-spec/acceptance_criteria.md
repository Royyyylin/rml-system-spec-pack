# Acceptance Criteria

## `AC-001` Telemetry Display

Requirement: `REQ-001`
Feature: `FEA-001`

- 對 `STATUS` / `METRICS_V2` 解析出的數值，`present` / `stale` 顯示數值，`sparse` / `unknown` / `not_synced` 顯示 `--`
- `sparse` 必須顯示為正常資料狀態，不得顯示為 error
- `stale` 必須保留最後值並顯示 `stale` hint
- `stale` 判定必須依據 owner repo 提供的 `source_timestamp` 或等價 age evidence；freshness window 數值以 owner contract 為準，若未定義則標為 migration dependency

## `AC-002` Capability Gate

Requirement: `REQ-002`
Feature: `FEA-002`

- `CAPS_V2` 存在時，功能 gating 必須以 `CAPS_V2` 為準
- `CAPS_V2` 不存在時，App 必須 fallback `CAP`
- 未宣告 capability 的功能不可在 UI 可操作

## `AC-003` Identity Boundary

Requirement: `REQ-003`
Feature: `FEA-003`

- App 內部裝置主鍵顯示與儲存以 `stableId` 為主；`central_ref` 僅作 Central metadata 對應鍵
- 若畫面顯示 MAC，必須標示它是 transport identity
- Central metadata / sync 請求必須以 `central_ref` 對應，不得以 MAC 直接當 app PK
- 若當前只連到 `CC bridge`，顯示 `Gateway` / `End Device` 名稱時，必須標示為 relayed / cached，不得視為第一手 BLE observation

## `AC-004` Assignment Reconciliation

Requirement: `REQ-004`, `REQ-008`
Feature: `FEA-004`

- Central 與 runtime gateway 一致時，不顯示 reconciliation badge
- 不一致時，detail / roster 必須可見 `assignmentSyncState`
- `pending_reconciliation` / `conflict` 時，畫面必須同時顯示 Central Gateway 與 Runtime Gateway
- 若當前 session 無可比較的 Central 即時資料，不得顯示 `conflict`；應顯示 `not compared` 或 `last synced` 語意
- `conflict` 僅在 `can_compare == true`（兩側皆有值且皆 fresh）時可導出；任一側為 stale / unknown / not_synced 或來自 last-synced reference，均不得顯示 `conflict`

## `AC-005` Alias Precedence

Requirement: `REQ-005`
Feature: `FEA-003`

- 有 pending op 時：`local_pending > central > cached > DEVICE_ALIAS > adv_name`
- 無 pending op 時：`central > cached > DEVICE_ALIAS > adv_name`
- `409 Conflict` 不可靜默覆蓋 local pending 結果

## `AC-006` Command Round Trip

Requirement: `REQ-006`
Feature: `FEA-002`

- current live peer 必須先決定合法 command path：`CC bridge -> Central-side path`；`Gateway / End Device -> Firmware-side path`
- `Firmware-side path` 的新 app action 必須透過 `CMD_V2` 送出非零 `txn_id`
- `Firmware-side path` 收到 `CMD_RESULT` `SUCCESS` 時進成功狀態；`ERROR` / `REJECTED` 時進失敗狀態
- `Central-side path` 收到 accepted 時不可直接視為完成；必須等 metadata / sync / authoritative confirmation 才可視為 final success
- `Firmware-side path` 收到 `REJECTED` 或 `Central-side path` 回覆 permission denied 時，App 顯示明確拒絕，不得靜默重試
- 若超過 configured timeout 未收到 path-specific terminal result，必須進 `timed_out`
- Assumption: 本 pack 暫以 async command `30s` 為驗收 timeout；若 app timeout matrix 有更新，以 repo SSOT 回寫本條

## `AC-007` Comparison Evidence Visibility

Requirement: `REQ-007`
Feature: `FEA-004`

- 使用者在 detail / debug / evidence-visible surface 上必須可檢視 Central 與 Firmware 兩側的 freshness hint（例如「fresh」/「stale」/「last synced Xs ago」）
- 當 App 顯示 `not compared` / `last synced` 時，必須可檢視 last-synced reference 的來源與相對時間
- 主畫面不必永遠攤開 raw timestamp；「可檢視 evidence」為 surface-level 要求，不規範固定 UI layout
- 若 owner repo 尚未提供 age evidence，App 可僅顯示「freshness unknown」語意，不得偽裝精確 freshness 判定
