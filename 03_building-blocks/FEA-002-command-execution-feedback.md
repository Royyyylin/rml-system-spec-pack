# Feature Spec — RML-FEA-002 Command Execution & Feedback

Status: formal
Feature ID: `RML-FEA-002`
Primary Stage: `target`

## Purpose

定義 BLE QoS Demo 中「command execution 與 feedback」這個 cross-repo feature 的上游意圖、authority boundary、成功語意與 retry 規則。

Diagram render: [feature-command-execution-feedback.svg](/Users/create94520/Projects/ble_qos_demo/rml-system-spec-pack/renders/feature-command-execution-feedback.svg)

本 feature 回答的是：
- App 如何發送 command intent
- `CMD_V2` / `CMD_RESULT` 與 Central command API 各自扮演什麼角色
- accepted、failed、timeout、retry、final state applied 如何區分
- 哪些 command 只是 device-side execution，哪些同時會影響 authoritative state

## Feature Intent

| ID | Statement |
| :--- | :--- |
| `FEA-002-INT-001` | 使用者操作必須走明確 command path，且結果必須可觀測，不可 fire-and-forget。 |
| `FEA-002-INT-002` | command feedback 必須區分「已接受處理」與「最終狀態已套用」，避免 UI 誤導。 |
| `FEA-002-INT-003` | retry、timeout、permission denied、rejected 等情境必須有一致語意。 |
| `FEA-002-INT-004` | App 採 `single active session`；當前 connected peer 必須先決定合法 command path，再解釋 feedback。 |

## Command Paths

| Path | Primary Owner | Use Cases | Final Confirmation |
| :--- | :--- | :--- | :--- |
| App -> Gateway / End Device firmware (`CMD_V2` / `CMD_RESULT`) | `Firmware` | connect / disconnect, roster ops, reboot,近端維護 | `CMD_RESULT` + 後續 runtime observation |
| App -> `CC bridge` -> Central | `Central` | manual failover, assignment/config mutation, register/remove device | 後續 metadata / sync / assignment state |
| App local pending / retry UI | `App` | in-flight, timeout, retry, pending banner, UX wording | App local state + 上游結果回寫 |

## Authority Boundary

| ID | Rule |
| :--- | :--- |
| `FEA-002-BND-001` | App 擁有 command intent 與 human-facing feedback，但不擁有 authoritative mutation truth。 |
| `FEA-002-BND-002` | Central 擁有 auth/RBAC、command API acceptance 與 authoritative state mutation；App 不得以本地成功提示取代 Central truth。 |
| `FEA-002-BND-003` | Firmware 包含 `CC bridge`、`Gateway` 與 `End Device` 三種角色；其中 `CC bridge` 只負責 bridge / relay，`Gateway` / `End Device` 擁有 device-side command execution 與 `CMD_RESULT` / runtime observation。Central 與 App 不得假裝直接控制 runtime loop。 |
| `FEA-002-BND-004` | 任何會改 assignment / metadata / config 的 command，最終真相必須回到 Central metadata / sync；`CMD_RESULT` 不自動等於 system truth。 |
| `FEA-002-BND-005` | 若當前 session 連的是 `CC bridge`，App 走 `Central-side path`；`CC bridge` 是 bridge firmware，不是 Central authority owner。若連的是 `Gateway` / `End Device`，App 走 `Firmware-side path`。不得把同一個 live command 假裝同時走兩條路徑。 |

## Path Gate

- App 先看目前連到哪個 BLE peer，再決定 command 要送到哪條 live path
- 連到 `CC bridge` 時，合法路徑是 `CC bridge -> Command API accepted -> Authoritative mutation -> Metadata / sync confirmation`
- 連到 `Gateway` / `End Device` 時，合法路徑是 `CMD_V2 -> CMD_RESULT -> Runtime observation`
- `Pending / retry UI` 屬 App local feedback layer；它可以跨兩條 path 共用，但不能改寫上游 authority owner

## Success Semantics

| State | Meaning | Must Not Be Interpreted As |
| :--- | :--- | :--- |
| `accepted` | request 已被上游接受處理 | final state applied |
| `succeeded` | device-side execution 或 command result 成功 | Central truth 已收斂 |
| `failed` | command 明確失敗、拒絕或權限不符 | timeout |
| `timed_out` | 在預期時間窗內未取得結果 | 永久失敗 |
| `retrying` | App 正在重送或等待下一次嘗試 | 新 command |

## Baseline / Target / Migration

### Baseline

- App 已有 `pending_connect`、`pending_roster_ops` 等 in-flight state。
- Central 已明文定義 command API success 只代表 accepted，不等於 final state applied。
- Firmware / Gateway 已有 `CMD_V2` / `CMD_RESULT` 路徑與近端 maintenance 操作；`CC bridge` 則負責把 BLE live session 橋接到電腦端 `Central`。

### Target

- App 對 command path 有清楚的 in-flight / success / failed / timeout / retry UX。
- `CMD_RESULT` 與後續 metadata / sync confirmation 被明確分層，不互相冒充。
- command evidence 可追回 request、result 與最終 authoritative state。

### Migration

- 某些 authoritative mutation 目前仍需以後續 delta sync 確認 final state，這屬 migration reality。
- 若 `CC bridge` relay semantics、Central command API、firmware `CMD_RESULT`、或 App retry policy 尚未完全對齊，應以 handoff / evidence 明文標示差距。

## Failure / Retry Cases

| Case | Required Behavior |
| :--- | :--- |
| permission denied | App 顯示權限不足；Central 為最終 enforcement owner。 |
| command accepted but final state not yet visible | App 保持 pending / in-flight 語意，等待 sync / observation 確認。 |
| `CMD_RESULT` error / rejected | App 顯示 failed，保留 txn / request evidence。 |
| timeout | App 進入 `timed_out`，允許 retry 或引導使用者確認上游狀態。 |
| retry | App 不得假裝是新真相；需保留與原 command 的關聯。 |

## Downstream Mappings

| Kind | IDs |
| :--- | :--- |
| Primary requirement | `REQ-006` |
| Adjacent requirement | `REQ-002` |
| App formal docs | `app-scope/01-must-own.md`, `app-scope/04-local-state.md`, `app-scope/05-interface-contract.md` |
| Central formal docs | `central-auth-sync-contract.md` |
| Firmware formal docs | `central-auth-sync-contract.md` |

## References

- [rml-lite.md](rml-lite.md)
- [requirements.md](requirements.md)
- [baseline-target-migration.md](baseline-target-migration.md)
- [app must own](../../ble_qos_app/docs/specs/app-scope/01-must-own.md)
- [app local state](../../ble_qos_app/docs/specs/app-scope/04-local-state.md)
- [app interface contract](../../ble_qos_app/docs/specs/app-scope/05-interface-contract.md)
- [central auth sync contract](../../central-device-metadata/docs/specs/central-auth-sync-contract.md)
- [firmware auth sync contract](../../ble_qos_demo_V1.2m/docs/01_definition/02_contract/central-auth-sync-contract.md)
