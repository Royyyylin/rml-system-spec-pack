# Feature Spec — GW QoS Scheduler Deployment Tuning

Status: draft
Primary Stage: `target`

## Purpose

定義 GW QoS scheduler connection interval table 的**部署調校模型**。GW 依據連線 ED 數量動態決定 BLE connection interval；本 spec 規範這張 interval table 如何被 preset / expert override 管理，以及跨 repo 的 ownership boundary。

本 spec 不是 `RML-FEA-004`（Assignment Reconciliation），而是 firmware executor-side 的 scheduler tuning contract。

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

## Ownership Boundary

| Owner | Responsibility |
|---|---|
| **Spec-pack** | Cross-repo contract: preset definitions, expert override schema, validation rules, ownership boundary |
| **Central** | Canonical runtime deployment value: stores active preset or override per GW; validation enforcement; audit log |
| **App** | Role-gated editor UX: preset selector in normal mode, expert override in engineering/admin mode; red error display for invalid config; disabled Save/Apply on validation failure |
| **Firmware** | Safe application: applies received config to scheduler; final validation guard; rejects invalid values with reason; falls back to `balanced` preset if no config received |

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

Preset / override changes should record：
- Actor（who initiated the change）
- Timestamp
- Previous value（preset name or full override table）
- New value
- Reason / comment（if available）

Audit canonical owner: **Central**（consistent with `RML-CAP-001`）。

## Wire / Apply Protocol

目前 firmware 的 interval table 無 wire apply path。當 wire protocol 落地時：
- Wire SSOT 仍為 `ble_qos_demo_V1.2m/ble_api.yaml`
- 可能走 `CMD_V2` extension 或新增 dedicated GATT characteristic
- 本 spec 不預定 wire encoding — 留給 firmware owner 設計

## References

- Firmware audit: `ble_qos_demo_V1.2m/docs/handoffs/2026-04-17-config-ssot-hardcode-audit/`
- Current implementation: `ble_qos_demo_V1.2m/src/gw_qos.c` `gw_qos_calc_interval()`
- Capability ownership: [capability-ownership.md](capability-ownership.md)
