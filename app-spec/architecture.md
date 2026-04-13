# App Architecture

## Authoritative Inputs

| Source | Purpose |
| :--- | :--- |
| `ble_qos_demo_V1.2m/ble_api.yaml` | GATT UUID、wire format、opcode、packet semantics SSOT |
| `ble_qos_app/docs/architecture/APP_ARCHITECTURE.md` | App 架構 invariants、identity、lifecycle、timeout 原則 |
| `ble_qos_app/docs/handoffs/2026-03-28-app-architecture-brief.md` | Assignment reconciliation、TelemetryValueState、責任邊界 |
| `central-device-metadata/docs/specs/data-model.md` | `central_ref`、assignment truth、identity / ownership / routing 分層 |
| `central-device-metadata/docs/specs/alias-sync-spec.md` | alias precedence 與 Central sync flow |

## Blocks

| ID | Block | Responsibility |
| :--- | :--- | :--- |
| `BLK-001` | Identity & Metadata Resolver | 管 `stableId`、`central_ref`、MAC、alias precedence、FW/version/info 標示。 |
| `BLK-002` | Telemetry Pipeline | 解析 `STATUS` / `METRICS_V2`，轉成 `TelemetryValueState` 後餵 UI。 |
| `BLK-003` | Assignment Reconciliation | 比對 Central 權威 assignment 與 firmware runtime attach，產生 badge / dual rows。 |
| `BLK-004` | Command Orchestrator | 依 current live peer 選擇 `Central-side path` 或 `Firmware-side path`，封裝 `CMD_V2` / Central command API，並分離 accepted、`CMD_RESULT`、sync confirmation、timeout / retry / failure。 |
| `BLK-005` | Capability & Role Gate | 依 `CAPS_V2` / `CAP` 與 session role 決定可見頁面與可用 action。 |

## App Surfaces

| Surface | Reads From | Must Not Do |
| :--- | :--- | :--- |
| L1 Device List | `BLK-001`, `BLK-002`, `BLK-003` | 不可自創 packet 欄位或重命名 assignment truth |
| L2 Device Detail | `BLK-001`..`BLK-005` | 不可把 sparse 當錯誤 |
| L3 Engineer / Sync | `BLK-001`, `BLK-003`, `BLK-004` | 不可把 MAC 當 app domain PK |

## Architecture Rules

- App 是 human-facing interaction owner，不是 system-wide truth authority
- Central 是 assignment / metadata 權威來源
- Firmware 是 GATT / runtime telemetry / roster truth
- App 顯示 runtime 與 authoritative 差異，但不在 UI 層偷偷合併兩者
- `CC bridge` 是 bridge / relay，不是 authority owner
- command feedback 必須分開 `accepted`、device-side result、與 final authoritative confirmation

## Current TODO

- `desktop-spec/` 仍無正式來源，本輪不導入 desktop 專屬 block
- command timeout 常數仍以 app timeout policy 為準；本 pack 在 AC / TC 先用暫定假設標註
