# SDLC Pipeline — BLE QoS Demo 系統規範

> arc42 §4 — Solution Strategy (SDLC pipeline).
> renamed from: shared-spec/sdlc.md (git mv).
> 本文定義從行為需求到硬體驗證的七階段開發流程。
> 數值（timeout、門檻）以引用方式指向 SSOT，不硬編碼。

---

## Section 1：Pipeline Overview

```mermaid
flowchart LR
  BDD([BDD\n行為場景]) --> CONTRACT([Contract\nWire 格式])
  CONTRACT --> SDD([SDD\n模組設計])
  SDD --> TDD([TDD\n測試向量])
  TDD --> CODE([Code\n實作])
  CODE --> INTEG([Integration\n跨系統])
  INTEG --> HIL([HIL\n硬體驗證])
```

每階段有明確 **輸入 → 輸出 → 完成定義（DoD）→ Gate**，不跨 gate 進下一階段。

---

## Section 2：各階段規格

### Stage 1：BDD（行為驅動設計）通用 ✅

| 欄位 | 說明 |
|------|------|
| **Stage** | BDD |
| **Input** | Feature ID（如 F-04）+ `shared-spec/requirements.md` REQ 清單 |
| **Output** | Gherkin scenarios + `bdd/` 下 sequence / state / use-case `.mmd` |
| **DoD** | 所有 actor 覆蓋 + 每 scenario 至少 trace 到 1 個 REQ |
| **Gate** | Roy smart review（人工確認場景語意正確） |
| **Tool** | `/spec-bdd <FEATURE-ID>` |

---

### Stage 2：Contract（Wire 格式規約）通用 ✅

| 欄位 | 說明 |
|------|------|
| **Stage** | Contract |
| **Input** | BDD scenarios + `ble_qos_demo_V1.2m/ble_api.yaml`（SSOT） |
| **Output** | `ble_api.yaml` diff + `contract/` 下 packet `.d2` + schema `.mmd` |
| **DoD** | Spectral schema lint pass + cross-repo codegen diff empty |
| **Gate** | Spectral CI（自動） |
| **Tool** | `/spec-contract` |

---

### Stage 3：SDD（模組設計文件）通用 ✅

| 欄位 | 說明 |
|------|------|
| **Stage** | SDD |
| **Input** | Contract spec + BDD scenarios |
| **Output** | `sdd/` 下 module-block `.d2` + state-detailed `.mmd` + `AC.md`（Acceptance Criteria） |
| **DoD** | trace 覆蓋率 100%（每個 REQ 至少一條 AC） |
| **Gate** | `check-trace-coverage.py`（自動） |
| **Tool** | `/spec-sdd` |

---

### Stage 4：TDD（測試向量先行）通用 ✅

| 欄位 | 說明 |
|------|------|
| **Stage** | TDD |
| **Input** | SDD AC.md + BDD scenarios |
| **Output** | 測試向量（golden file）+ unit test skeleton（全部 RED） |
| **DoD** | 失敗測試數 = BDD scenario 數（確保 RED 完整） |
| **Gate** | test fail count = scenario count（CI 自動驗證） |
| **Tool** | conductor（自動派發 TDD phase） |

---

### Stage 5：Code（實作）通用 ✅

| 欄位 | 說明 |
|------|------|
| **Stage** | Code |
| **Input** | TDD 測試向量 + SDD 模組邊界 |
| **Output** | 通過所有 unit test 的實作程式碼，含 `[REQ-ID]` impl tag |
| **DoD** | GREEN（所有 unit test pass）+ impl tag 標注 |
| **Gate** | lint / `check-impl-tags.py`（CI 自動） |
| **Tool** | conductor |

---

### Stage 6：Integration（跨系統整合測試）通用 ✅

| 欄位 | 說明 |
|------|------|
| **Stage** | Integration |
| **Input** | 三 repo（Firmware / App / Central）均完成 Code stage |
| **Output** | cross-system test vector + conformance test result |
| **DoD** | cross-repo conformance test vector 全 pass |
| **Gate** | cross-repo conformance CI（自動） |
| **Tool** | conductor |

---

### Stage 7：HIL（Hardware-in-the-Loop 硬體驗證）BLE-specific ⚠️

| 欄位 | 說明 |
|------|------|
| **Stage** | HIL |
| **Input** | Integration pass + 4-board nRF52833 DK 環境就緒 |
| **Output** | Zephyr Twister 測試報告（4-board green） |
| **DoD** | `hil-check.sh` pass，全板 green |
| **Gate** | `hil-check.sh`（自動，需實體硬體） |
| **Tool** | conductor |

---

## Section 3：適用範圍

### 完全適用

- **BLE / IoT 系統**（本專案主場景）
- **工業 stateful 多端系統**（OPC UA / Modbus 類）
- 有嚴格 wire protocol 版本管理需求的場景

### 部分適用

- **純 Web / SaaS 系統**：
  - 移除 Stage 7（HIL）
  - Stage 2 Contract 改用 OpenAPI / AsyncAPI 取代 `ble_api.yaml`
  - Stage 4 TDD 測試工具換用 Jest / Pytest

### 不適用

- **純 ML pipeline**（訓練 → 評估 → 部署）：
  沒有明確的 wire protocol 和 actor 邊界，BDD scenario 不適用此格式

---

*版本：2026-04-23 | 適用 feature：所有 F-NN 跨 repo feature*
