# GW QoS Scheduler Tuning — Downstream Tasks

**Status**：handoff note　**Date**：2026-04-17

## 本輪做了什麼

在 `shared-spec/feature-gw-qos-scheduler-tuning.md` 定義了 GW QoS scheduler interval table 的 deployment tuning contract：
- 3 個 preset（conservative / balanced / aggressive）
- Expert override schema（cutoff1-3 + interval1-4）
- 6 條 validation rules（TUNE-VAL-001~006）
- Ownership boundary：spec-pack = contract; Central = runtime config SSOT; App = editor UX; Firmware = executor + guard

## Downstream Tasks by Repo

### Central (`central-device-metadata`)

1. **Schema**：新增 GW scheduler tuning table/model（preset enum + optional override JSON）
2. **API**：CRUD endpoint for per-GW tuning config，含 validation enforcement
3. **Validation**：implement TUNE-VAL-001~005 server-side；reject invalid save
4. **Audit**：record preset/override changes with actor, timestamp, previous/new value
5. **Sync**：當 GW 上線時 push active config（待 wire protocol 決定）

### App (`ble_qos_app`)

1. **Preset selector**：normal mode 顯示 conservative / balanced / aggressive
2. **Expert override**：engineering/admin mode 展開 cutoff/interval 欄位
3. **Validation UX**：client-side validate TUNE-VAL-001~006；invalid → red error + Save/Apply disabled
4. **Role gating**：normal user 不可見 expert override

### Firmware (`ble_qos_demo_V1.2m`)

1. **Wire protocol**：決定 apply path（CMD_V2 extension / new GATT char / Central sync）
2. **Apply logic**：`gw_qos_calc_interval()` 改為讀 runtime config 而非 hardcoded table
3. **Final guard**：firmware-side validate TUNE-VAL-001~005；reject invalid + report reason
4. **Fallback**：invalid config → reject + reason + keep last-known-good；boot 時無有效 config → `balanced` preset
5. **Update `ble_api.yaml`**：若走 GATT path，需新增 characteristic entry

## Gates

- Central API schema + validation 落地後，App 才能開始 editor UX
- Firmware wire protocol 決定後，才能對接 Central sync
- 三端 validation 必須一致（同一組 TUNE-VAL rules）

## 不在本輪 scope

- Firmware code 修改
- Central DB schema / API 實作
- App UI 實作
- Wire encoding 設計
- Acceptance criteria / test cases（待 contract review 通過後補）

## Future Independent Domain — Telemetry Profiling

PER / channel interference detection / telemetry field selection 是獨立 domain，不可塞進 F-04 CMD_V2 0x07。App 選欄位必須從 Central catalog predefined fields 勾選，Firmware 只接受 known profile_id / bitmask。詳見 `shared-spec/feature-gw-qos-extension-boundary.md`。
