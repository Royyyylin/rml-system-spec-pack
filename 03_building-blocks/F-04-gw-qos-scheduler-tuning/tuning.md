# Feature Spec — GW QoS Scheduler Deployment Tuning

Status: draft
Primary Stage: `target`

## Purpose

定義 GW QoS scheduler connection interval table 的**部署調校模型**。GW 依據連線 ED 數量動態決定 BLE connection interval；本 spec 規範這張 interval table 如何被 preset / expert override 管理，以及跨 repo 的 ownership boundary。

本 spec 不是 `FEA-004`（Assignment Reconciliation），而是 firmware executor-side 的 scheduler tuning contract。

## Background

Firmware 的 `gw_qos_calc_interval()` 用 step table 把 ED 數量對應到 connection interval（BLE units, 1.25ms）。目前 step table 硬編碼在 firmware，無法從 Central 或 App 調整。

Current hardcoded table（`balanced` preset baseline）：

| ED count | Interval (BLE units) | Interval (ms) |
|---|---|---|
| 1–3 | 80 | 100 |
| 4–5 | 160 | 200 |
| 6–8 | 400 | 500 |
| 9+ | 800 | 1000 |

## Tuning Model

### Presets

| Preset | Cutoffs (c1/c2/c3) | Intervals (i1/i2/i3/i4) | 語意 |
|---|---|---|---|
| `conservative` | 2 / 4 / 6 | 80 / 80 / 160 / 400 | 優先連線品質，犧牲併發容量 |
| `balanced` | 3 / 5 / 8 | 80 / 160 / 400 / 800 | **預設**，保持現行行為 |
| `aggressive` | 4 / 6 / 10 | 80 / 160 / 400 / 400 | 優先併發容量，犧牲低端回應速度 |

Decision logic：`if n <= c1: i1; elif n <= c2: i2; elif n <= c3: i3; else: i4`

### Expert Override

Engineering / admin mode 可開放自訂 table：

```
{ cutoff1: int, cutoff2: int, cutoff3: int,
  interval1: int, interval2: int, interval3: int, interval4: int }
```

## Validation Rules

| ID | Rule |
|---|---|
| `TUNE-VAL-001` | Cutoffs must be strictly increasing: `cutoff1 < cutoff2 < cutoff3` |
| `TUNE-VAL-002` | All cutoffs must be positive integers (`>= 1`) |
| `TUNE-VAL-003` | All intervals must be within firmware BLE timing constraints: `6 <= interval <= 3200`（BLE spec range for connection interval） |
| `TUNE-VAL-004` | Invalid override **cannot be saved** in App or Central — App must show red error, Save/Apply disabled |
| `TUNE-VAL-005` | Firmware must **reject** invalid applied config and report reason via `CMD_RESULT` or equivalent feedback |
| `TUNE-VAL-006` | Intervals should be non-decreasing (`i1 <= i2 <= i3 <= i4`）— warning if violated, not hard reject |

## Design Rationale & Use Case

### Motivation（為什麼要做）

本 spec 的起點是 2026-04-17 的 hardcode audit（`findings-missing-config.md` finding #4）。`gw_qos_calc_interval()` 在 `src/gw_qos.c:425-428` 的 step table 硬編碼如下：`n<=3→80, n<=5→160, n<=8→400, else→800`。

核心問題不是「值錯了」，而是 **config coupling**：`n <= 8` 邊界默默假設 `CONFIG_BLE_QOS_MAX_ED = 8`。若 MAX_ED 被改成 12，step table 不會跟著調整，第 9–12 台 ED 會直接落進 800（1 秒 interval）而不觸發任何 warning。

初始分析（AQ3）建議 Option A（BUILD_ASSERT + document）。F-04 升級成 Option B（runtime preset），根本原因是：同一批 firmware 需部署到不同 site，不同 site 對 BLE 回應速度與併發容量有不同的 tradeoff，BUILD_ASSERT 解不了現場調校需求。決策詳見 `--base-dir/docs/decisions/2026-04-18-f04-runtime-preset-over-build-assert.md`。

### Use Case Narrative（使用情境）

Engineer 部署完某 site，實際運行後從 telemetry 發現某台 GW 的 QoS 不理想（ED 短斷線重連、延遲偏高、radio overload）。Engineer 判斷現有的 `balanced` preset 不適合這個 site 的 ED 密度或無線環境，於是用 App 連上該 GW、PIN ENG_UNLOCK 解鎖，切換到 `aggressive` 或 `conservative`。

App 做即時 UX validation（順序錯、範圍錯就顯示紅字並鎖定 Save 按鈕），送得出去的 config 由 Central 記錄 audit + revision，Firmware 收到後做 final guard validation 才真的套用。Engineer 再觀察 telemetry 確認改善。

**目標使用者**：field engineer（L3），需 PIN ENG_UNLOCK 解鎖；L1 巡視人員完全不碰此功能。

### Preset 語意（三個完整 tradeoff）

| Preset | Cutoffs (c1/c2/c3) | Intervals (i1/i2/i3/i4, BLE units) | 適用場景 |
|---|---|---|---|
| `balanced` | 3 / 5 / 8 | 80 / 160 / 400 / 800 | 預設值；保持現行 hardcode 行為；boot fallback |
| `conservative` | 2 / 4 / 6 | 80 / 80 / 160 / 400 | 連線品質優先，短 interval 為主；ED 少、回應要快 |
| `aggressive` | 4 / 6 / 10 | 80 / 160 / 400 / 400 | 併發容量優先；最高 tier 壓到 400，犧牲少量 ED 低端回應速度 |

### Preset + Expert Override 兩層設計

- **Preset 層**：給不熟悉 BLE scheduling 細節的 engineer 用。三個完整 tradeoff 涵蓋多數現場情境，降低操作錯誤風險
- **Expert override 層**：給熟悉 domain 的 engineer 用，可自訂 cutoff + interval。但受 App UX validation、Central authority validation、Firmware final guard 三層保護，不會因手誤搞壞系統

### Defense-in-depth 三層（TUNE-VAL-001~006 各層獨立跑）

| 層 | 職責 | 觸發時機 |
|---|---|---|
| App | UX validation（紅字 + 鎖定 Save） | 使用者輸入當下 |
| Central | authority validation + audit + revision | PUT API 進來時 |
| Firmware | final guard + last-known-good fallback | CMD_V2 0x07 write 進來時 |

同一組 TUNE-VAL 規則在三層各跑一次（defense-in-depth）。

## Ownership Boundary

| Owner | Responsibility |
|---|---|
| **Spec-pack** | Cross-repo contract: preset definitions, expert override schema, validation rules, ownership boundary |
| **Central** | Canonical runtime deployment value: stores active preset or override per GW; validation enforcement; audit log |
| **App** | Role-gated editor UX: preset selector in normal mode, expert override in engineering/admin mode; red error display for invalid config; disabled Save/Apply on validation failure |
| **Firmware** | Safe application: applies received config to scheduler; final validation guard; rejects invalid values with reason and keeps last-known-good config; falls back to `balanced` preset only at boot when no valid config has ever been received |

### Role Model

- **Normal mode**：顯示 preset selector（conservative / balanced / aggressive），不暴露 expert override
- **Engineering / Admin mode**：可展開 expert override table，可看到 cutoff / interval 欄位

### What Each Must Not Do

| Owner | Must Not |
|---|---|
| App | Save/apply invalid override; bypass validation with local workaround |
| Central | Accept invalid override values into DB; allow save without validation |
| Firmware | Silently apply invalid config; skip validation because "Central already validated" |
| Spec-pack | Dictate firmware-internal scheduling algorithm beyond the interval table interface |

## Audit Expectation

Preset / override changes record actor, timestamp, previous/new value, reason。Audit canonical owner: **Central**（consistent with [`Canonical-Identity-Authority`](../../02_solution-strategy/capability-map.md)）。

## Wire / Apply Protocol

Firmware owner 決定走 CMD_V2 opcode 0x07 SET_SCHED_TUNE（radio-minimal apply）。Wire SSOT：`ble_api.yaml`。詳見 firmware handoff `f-04-fw-apply-protocol-decision/`。

## Extension Boundary

F-04 限於 scheduler tuning config apply。Telemetry profiling（可選 field / experiment）是獨立 domain。App 只能選 Central catalog predefined fields，Firmware 只接受 known profile_id / bitmask。詳見 [feature-gw-qos-extension-boundary.md](feature-gw-qos-extension-boundary.md)。

## CMD_V2 Timeout Contract

App-side timeout when waiting for CMD_V2 opcode 0x07 SET_SCHED_TUNE `CMD_RESULT` notify:

| Parameter | Value | SSOT |
|---|---|---|
| Wait timeout | 10 000 ms | `ble_api.yaml:system_constants.CMD_V2_TIMEOUT_MS` |
| Retry count | 1 | `ble_api.yaml:system_constants.CMD_V2_RETRY_COUNT` |
| Retry backoff | 500 ms | `ble_api.yaml:system_constants.CMD_V2_RETRY_BACKOFF_MS` |

Rationale: async operations (CONNECT_ED, DISCONNECT_ED) complete in < 5 s under normal BLE conditions. 10 s provides headroom for congested radio environments. 1 retry covers transient BLE stack glitches. Firmware dedup (per F-04 RAN) prevents duplicate applies when App retries.

Do not hardcode timeout values in App or Central — always reference the generated constants derived from `ble_api.yaml`.

## References

- Firmware audit: `ble_qos_demo_V1.2m/docs/handoffs/2026-04-17-config-ssot-hardcode-audit/`
- Capability ownership: [capability-ownership.md](capability-ownership.md)
- SSOT: `ble_qos_demo_V1.2m/ble_api.yaml` sections `system_constants`, `presets`, `tune_val_rules`
