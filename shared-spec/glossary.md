# System Glossary

## 角色（Roles）

| Role | Definition | Authority | Owner Repo |
|---|---|---|---|
| ED (End Device) | BLE peripheral sensor node | None | firmware |
| GW (Gateway) | BLE dual-role aggregator | local QoS + roster | firmware |
| CC bridge firmware | BLE-to-Central relay (transport only, NOT authority) | none | firmware |
| Central | Backend system | canonical truth (identity, assignment, metadata) | central-device-metadata |
| Mobile / App | Phone client | local view state + Central offline cache | ble_qos_app |

## 韌體 Role Enum

衍生自韌體 `CLAUDE.md` 「角色系統」區塊（NVS 儲存，手機透過 Config GATT Service 寫入）：

| Constant | Value | Description |
|---|---|---|
| APP_ROLE_UNPROVISIONED | 0 | 尚未配置 |
| APP_ROLE_END_DEVICE | 1 | ED 角色 |
| APP_ROLE_GATEWAY | 2 | GW 角色 |
| APP_ROLE_REPEATER | 3 | reserved |
| APP_ROLE_CC | 4 | CC bridge 角色 |

## Spec ID 命名規範

| Prefix | Meaning | Owner Repo | Example |
|---|---|---|---|
| F-NN | Feature ID（跨 repo） | spec-pack | F-04 GW QoS scheduler tuning |
| FW-NN[A/B] | Firmware spec phase | firmware | FW-3A CMD_V2 length guard |
| A-N | App work item | app | A-1 Dart model schema |
| C-N | Central work item | central | C-1 spec-contract review |
| S-N | System / spec-pack work | spec-pack | S-1 AC catalog |
| X-N | Cross-repo coordination | spec-pack | X-1 wire parity test |
| W##[A-Z] | Wave（per-repo internal planning） | per-repo | W26D F-04 Central API |

## F-04 vs FW-3A 命名澄清

- **F-04** GW QoS scheduler tuning：跨三個 repo 的 feature ID。Owner = spec-pack
  `shared-spec/feature-gw-qos-scheduler-tuning.md`
- **FW-3A** CMD_V2 per-opcode length guard：firmware spec phase，**F-04 韌體工作的子集**。
  Owner = firmware repo。
- 兩者層次不同，**禁止混用**。Documentation 引用時必須使用完整 prefix。

## Wire 名詞

衍生自 `ble_api.yaml`（firmware repo SSOT），下列只列語意說明，數值見原始定義：

| Term | 定義 | 參考 |
|---|---|---|
| CMD_V2 | Transaction-based command characteristic | `ble_api.yaml` → characteristics.CMD_V2 |
| CMD_RESULT | CMD_V2 回應 characteristic（subscribe for async result） | `ble_api.yaml` → characteristics.CMD_RESULT |
| CAPS_V2 | CBOR-encoded capability map（取代 CAP v1） | `ble_api.yaml` → characteristics.CAPS_V2 |
| TUNE-VAL | QoS scheduler preset 參數包（opcode 0x07 payload） | `ble_api.yaml` → opcodes 0x07 + TUNE-VAL rules |
| Preset | BALANCED / AGGRESSIVE / CONSERVATIVE 三種 QoS 排程策略 | `ble_api.yaml` → presets: |
| Zone | NEAR / MID / FAR / EDGE — PHY + TX power 聯動區間 | firmware `.claude/rules/qos-zones.md` |
| MAX_ED | GW 每次最大 ED slot 數（compile-time 上限，runtime 可降） | `ble_api.yaml` → system_constants.MAX_ED |
| CMD_V2_TIMEOUT_MS | App 端 CMD_V2 等待 timeout | `ble_api.yaml` → system_constants.CMD_V2_TIMEOUT_MS |

## 流程詞彙

| Term | 定義 |
|---|---|
| plan → spec → impl → integration | 4-gate acceptance pipeline（見 Phase 2 acceptance pipeline） |
| handoff | Cross-session 工作交接文件，存於 `docs/handoffs/` |
| CURRENT.md | 各 repo 當前狀態 snapshot（`.claude/CURRENT.md`） |
| ADR | Architecture Decision Record，存於 `docs/decisions/` 或 `docs/adr/` |
| SSOT | Single Source of Truth — 數值只能有一個定義來源，其他引用 |

## NCS Version SSOT

NCS（nRF Connect SDK）版本 SSOT = firmware repo `scripts/dev.sh` 中的預設路徑：
```
NCS_HOME:=$HOME/ncs/v2.9.2   # 見 dev.sh line ~32
```
文件引用時請寫「見 `scripts/dev.sh`」，不得硬編碼版本號。
