# Diagrams INDEX — BLE QoS Demo Spec-Pack

> 所有圖以 Mermaid 撰寫（GitHub native render）。每張圖只表達一個主訊息（`DAR-001`）。
> 圖種選用規則見 [`../diagram-authoring-rules.md`](../diagram-authoring-rules.md)。

---

## Flow（流程圖）— 4 張

| 檔案 | 主訊息 | 對應 Spec |
|------|--------|-----------|
| [`flow/flow-f04-end-to-end.md`](flow/flow-f04-end-to-end.md) | App 改 preset → Central audit → CMD_V2 → GW apply → App update | [`../feature-gw-qos-scheduler-tuning.md`](../feature-gw-qos-scheduler-tuning.md) |
| [`flow/flow-cap-discovery.md`](flow/flow-cap-discovery.md) | App 讀 CAPS_V2 → parse opcode bitmap → enable/disable UI | [`../requirements.md`](../requirements.md) REQ-002 |
| [`flow/flow-failback.md`](flow/flow-failback.md) | Operator POST failback → Central eligibility check → execute / reject | [`../feature-assignment-reconciliation.md`](../feature-assignment-reconciliation.md) W26A.1 |
| [`flow/flow-ble-conn-lifecycle.md`](flow/flow-ble-conn-lifecycle.md) | scan → connect → discover → subscribe → idle / disconnect | [`../requirements.md`](../requirements.md) REQ-006 |

---

## Sequence（時序圖）— 6 張

| 檔案 | 主訊息 | 對應 Spec |
|------|--------|-----------|
| [`sequence/seq-cmd-v2-success.md`](sequence/seq-cmd-v2-success.md) | CMD_V2 成功路徑：handler 執行 + NVS 寫入 + CMD_RESULT SUCCESS | [`../feature-gw-qos-scheduler-tuning.md`](../feature-gw-qos-scheduler-tuning.md) |
| [`sequence/seq-cmd-v2-reject-tune-val.md`](sequence/seq-cmd-v2-reject-tune-val.md) | TUNE-VAL reject：App 前置攔截或 Central / Firmware 拒絕 | [`../feature-gw-qos-scheduler-tuning.md`](../feature-gw-qos-scheduler-tuning.md) TUNE-VAL |
| [`sequence/seq-cmd-v2-reject-busy.md`](sequence/seq-cmd-v2-reject-busy.md) | 第一個 CMD in-flight → 第二個 reject 0xFD BUSY | [`../feature-gw-qos-scheduler-tuning.md`](../feature-gw-qos-scheduler-tuning.md) CMD_V2 timeout |
| [`sequence/seq-cache-invalidation-3tier.md`](sequence/seq-cache-invalidation-3tier.md) | GW 重啟 → Service Changed / DB Hash / FW version 三層快取失效 | `ble_api.yaml` |
| [`sequence/seq-ha-failover.md`](sequence/seq-ha-failover.md) | GW-A 心跳超時 → CC bridge → Central 決策 → GW-B promotion | [`../feature-assignment-reconciliation.md`](../feature-assignment-reconciliation.md) |
| [`sequence/seq-ed-reconnect.md`](sequence/seq-ed-reconnect.md) | ED 斷線 → scan → network_id 匹配 → reconnect + backoff | [`../requirements.md`](../requirements.md) REQ-006 |

---

## State（狀態機）— 4 張

| 檔案 | 主訊息 | 對應 Spec |
|------|--------|-----------|
| [`state/state-role-machine.md`](state/state-role-machine.md) | UNPROVISIONED → ED / GW / CC，NVS role 轉換，requires_reboot | `ble_api.yaml` NVS roles (S6) |
| [`state/state-cmd-v2-dispatcher.md`](state/state-cmd-v2-dispatcher.md) | idle → dispatching → response_pending → idle，0xFD BUSY guard | [`../feature-gw-qos-scheduler-tuning.md`](../feature-gw-qos-scheduler-tuning.md) |
| [`state/state-failback-eligibility.md`](state/state-failback-eligibility.md) | pending → eligible / hold_down_active / not_assigned / no_history | [`../feature-assignment-reconciliation.md`](../feature-assignment-reconciliation.md) W26A.1 |
| [`state/state-ed-conn.md`](state/state-ed-conn.md) | idle → scanning → connecting → connected → idle，含 retry backoff | [`../requirements.md`](../requirements.md) REQ-006 |

---

## Architecture（架構圖）— 5 張

| 檔案 | 主訊息 | 對應 Spec |
|------|--------|-----------|
| [`architecture/arch-system-overview.md`](architecture/arch-system-overview.md) | Mobile App / CC bridge / GW / ED / Central / Cloud 系統全景 | [`../system-actors-and-authority.d2`](../system-actors-and-authority.d2) |
| [`architecture/arch-firmware-modules.md`](architecture/arch-firmware-modules.md) | ble_port / qos_service / role_* / nvs / ha / uplink / cmd_v2_dispatch 分層 | `ble_qos_demo_V1.2m` |
| [`architecture/arch-central-layers.md`](architecture/arch-central-layers.md) | presentation / application / domain / infrastructure 四層 | `central-device-metadata/` |
| [`architecture/arch-app-layers.md`](architecture/arch-app-layers.md) | UI / state(Riverpod) / domain / data(BLE+HTTP) 四層 | `ble_qos_app/` |
| [`architecture/arch-ble-wire.md`](architecture/arch-ble-wire.md) | `ble_api.yaml` → codegen → Firmware / Central / App，x1 drift check | [`../x1-cross-repo-wire-parity-spec.md`](../x1-cross-repo-wire-parity-spec.md) |

---

## 讀圖建議

- 第一次了解系統 → 先讀 [`architecture/arch-system-overview.md`](architecture/arch-system-overview.md)
- 理解 F-04 指令流程 → [`flow/flow-f04-end-to-end.md`](flow/flow-f04-end-to-end.md) → [`sequence/seq-cmd-v2-success.md`](sequence/seq-cmd-v2-success.md)
- 理解 HA failover → [`sequence/seq-ha-failover.md`](sequence/seq-ha-failover.md) → [`state/state-failback-eligibility.md`](state/state-failback-eligibility.md)
- 理解 wire parity → [`architecture/arch-ble-wire.md`](architecture/arch-ble-wire.md)
