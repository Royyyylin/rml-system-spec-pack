# Packet Contract

本文件是 system-spec 對 app-visible packet 的治理映射，不取代 `ble_api.yaml`。

## Rules

- 欄位 offset、UUID、opcode 真相來源只認 `ble_qos_demo_V1.2m/ble_api.yaml`
- 本文件只整理 app / Central / trace 需要追蹤的 packet family
- 若本文件與 `ble_api.yaml` 不一致，以 `ble_api.yaml` 為準

## Packets

| ID | Firmware Source | App Use | Notes |
| :--- | :--- | :--- | :--- |
| `PKT-001` | `STATUS` `0x2A1D` | baseline QoS telemetry | `rssi/pdr/lat/jit/profile/phy/tx_power/connected/interval` |
| `PKT-002` | `METRICS_V2` `0x2A23` | extended telemetry | 與 `TelemetryValueState` 一起處理 sparse / stale |
| `PKT-003` | `CAPS_V2` / `CAP` | capability gate | `CAPS_V2` 優先；缺失時 fallback `CAP` |
| `PKT-004` | `ROSTER_LIST` `6f8a9c20` | runtime roster / attach context | 提供 slot、MAC、online state；供 `ed_id` 映射與 reconciliation |
| `PKT-005` | `CMD_V2` / `CMD_RESULT` | user action transaction | 新 app 只用 transaction-based command，不用 legacy `CMD` |
| `PKT-006` | `DEVICE_ALIAS`, `FW_VERSION`, `DEVICE_INFO` | metadata / diagnostics | `DEVICE_ALIAS` 只做 fallback，canonical alias 在 Central |

## Packet Governance Notes

- `MODE` `0x2A1E` 與 `ROLE` `0x2A1F` 不是 error / action packet
- service UUID 是 `0x1820`，不是舊版 spec 的 `0xFF01`
- `DEVICE_ALIAS` 不可當 canonical metadata truth
