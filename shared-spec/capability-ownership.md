# Capability / Ownership Boundary

> 本文件把 `rml-lite.md` 的 actor / authority boundary 往下一層收斂成 cross-repo capability ownership。原則只有一個：每種能力只允許一個 authority owner；其他 repo 可以消費、呈現、快取、索引，但不得重寫真相。

## Core Rules

| ID | Rule |
| :--- | :--- |
| `RML-OWN-001` | 每種 capability 必須有且只有一個 authority owner。 |
| `RML-OWN-002` | non-owner 可以 render、cache、index、validate upstream output，但不得重定 truth。 |
| `RML-OWN-003` | repo-level technical truth 留在各 repo SSOT；project-level orchestration truth 留在 `--base-dir`。 |
| `RML-OWN-004` | 任何跨 owner 變更，若未同步更新 owner repo 的 formal spec / evidence，不得宣告 `cross-repo done`。 |

## Cross-Repo Capability Matrix

| ID | Capability | Authority Owner | Other Repos May | Other Repos Must Not |
| :--- | :--- | :--- | :--- | :--- |
| `RML-CAP-001` | Canonical identity、assignment、metadata、auth、audit、sync truth | `Central` | consume、cache、display、validate | 自行重定 `gw_id` / `ed_id`、assignment truth、RBAC policy |
| `RML-CAP-002` | Runtime telemetry、QoS measurement、failover execution、radio behavior、device-side recovery | `Firmware` | ingest、display、diagnose、correlate | 假裝擁有第一手 runtime truth，或重寫 device observation |
| `RML-CAP-003` | Human-facing interaction、presentation semantics、pending/error UX、local view state | `App` | publish backend data、execute device command、expose policy result | 把 backend / firmware truth 直接等同 UI truth，或把 local UI state 升格成 system truth |
| `RML-CAP-004` | GATT / wire contract、opcode、payload field semantics | `Firmware repo SSOT` | derive docs、build parser / UI / ingest logic | 自行發明 wire enum、UUID、opcode、payload meaning |
| `RML-CAP-005` | Cross-repo planning、dispatch、queue / gate governance、handoff、evidence index | `Conductor` | reference、review、execute repo-local work | 取代 repo SSOT、重寫 repo technical truth、直接擔任 runtime authority |
| `RML-CAP-006` | GW QoS scheduler deployment tuning（preset / expert override） | `Central`（runtime deployment config truth） | Firmware: execute + final validation guard; App: role-gated editor UX; Spec-pack: contract/schema semantics | App: save invalid config; Central: skip validation; Firmware: silently apply invalid values or self-originate config truth |

> `Conductor` 為 `Conductor / AI Orchestration Layer`（RML-ACT-005）的 shorthand。

## Repo Obligations

### Central Must Own

- canonical identity 與 `central_ref` 規則
- assignment / lease / active gateway truth
- metadata、auth、audit、sync publication
- system-of-record 等級的 state / enum / contract naming

### Central Must Not Own

- device-side QoS measurement 與 radio behavior
- UI wording、pending state、presentation precedence
- project-level queue / handoff / evidence index

### Firmware Must Own

- `ble_api.yaml` 與其衍生 wire / GATT contract
- runtime telemetry、link metrics、heartbeat、failover execution
- device-side buffering / replay / retry / reconnect behavior
- runtime attachment 與 local recovery observation

### Firmware Must Not Own

- canonical identity format 的最終定義
- global assignment inventory / auth policy / audit truth
- UI interaction semantics 與 display precedence
- project-level governance 狀態

### App Must Own

- operator / engineer interaction flow
- screen-level presentation semantics、role-aware UI gating
- local cache、draft / pending / retry / error view-state
- rename / alias interaction handling 與 human-facing explanation

### App Must Not Own

- canonical identity / assignment / auth truth
- first-hand runtime telemetry truth
- wire contract semantics 的最終定義
- cross-repo promote / gate 決策

### Conductor Must Own

- cross-repo CURRENT、plans、handoffs、decisions、evidence index
- queue promote / gate bookkeeping 與 project-level acceptance tracking
- cross-repo impact analysis、dispatch、continuity 與 review flow

### Conductor Must Not Own

- repo-level technical SSOT
- runtime control loop、QoS decision、device command authority
- canonical identity / assignment / auth truth
- human-facing product semantics

## Handoff Rules

| ID | Rule |
| :--- | :--- |
| `RML-HOF-001` | `Firmware` 改 `ble_api.yaml` 或 runtime payload semantics 時，必須通知 `Central` 與 `App` 更新 ingest / parser / UI / docs。 |
| `RML-HOF-002` | `Central` 改 identity、assignment、auth、sync contract 時，必須通知 `App` 與 `Firmware` 更新 consumer logic 與 acceptance evidence。 |
| `RML-HOF-003` | `App` 改 interaction semantics、role gating、display contract 時，必須回寫 human-facing acceptance 與必要的 upstream assumption。 |
| `RML-HOF-004` | `Conductor` 只維護 cross-repo coordination records；若發現 repo SSOT 缺漏，必須回寫 owner repo，不得在 `--base-dir` 補一份替代 truth。 |

## Acceptance Hooks

- 牽涉單一 owner 的變更，只能宣告對應 repo `repo done`，不能自動升格成 `cross-repo done`。
- 牽涉多個 owners 的變更，必須同時更新 owner repo formal docs、consumer evidence 與 `--base-dir` handoff / gate 狀態。
- 若某一層 truth 被 non-owner 手改，必須回寫 authority owner，否則視為 drift。

## References

- [rml-lite.md](rml-lite.md)
- [app-scope.md](../../ble_qos_app/docs/specs/app-scope.md)
- [central-scope.md](../../central-device-metadata/docs/specs/central-scope.md)
- [firmware-scope.md](../../ble_qos_demo_V1.2m/docs/spec/00_canonical/boundaries.md)
- [data-model.md](../../ble_qos_demo_V1.2m/docs/spec/04_protocol/data-model.md)
