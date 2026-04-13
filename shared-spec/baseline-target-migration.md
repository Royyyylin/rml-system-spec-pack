# Baseline / Target / Migration Model

> 本文件定義整個 BLE QoS Demo shared-spec 使用的 `stage` 概念。每個 requirement、queue item、acceptance decision、migration exception，都應可被歸類為 `baseline`、`target`、或 `migration`。

## Stage Definitions

| ID | Stage | Meaning | Required Question |
| :--- | :--- | :--- | :--- |
| `RML-STG-001` | `baseline` | 現況已存在、必須被忠實描述與保護的 working truth。 | 我們今天實際在哪裡？ |
| `RML-STG-002` | `target` | 希望穩定收斂到的 steady-state architecture / contract / acceptance model。 | 我們要到哪裡？ |
| `RML-STG-003` | `migration` | 介於 baseline 與 target 之間，為了安全過渡而暫時允許的 bridge、dual-track、fallback 或例外。 | 過渡期允許什麼？ |

## Stage Rules

| ID | Rule |
| :--- | :--- |
| `RML-STG-004` | `baseline` 不是過時資料夾，而是目前 installed-base reality；不得用 target 敘事覆蓋 baseline truth。 |
| `RML-STG-005` | `target` 必須描述穩態，不得把暫時 workaround、人工例外、硬編碼路徑包裝成 target。 |
| `RML-STG-006` | `migration` 必須有 owner、entry condition、exit condition、fallback；沒有退出條件的 migration 視為 drift。 |
| `RML-STG-007` | 同一條 requirement 或 queue item 可以跨 stage 演進，但每一刻只能有一個主 stage。 |

## Baseline Snapshot

> 以下 baseline snapshot 代表 **2026-04-09** 時點的正式判斷，用來回答「系統現在在哪裡」。

| ID | Baseline Statement |
| :--- | :--- |
| `RML-BAS-001` | 本專案是 brownfield-style 的多 repo 系統，不是 greenfield；規劃必須從現有 App、Firmware、Central 與既有 spec 出發。 |
| `RML-BAS-002` | repo-level truth 已分層：`Firmware` 是 runtime truth、`Central` 是 global truth、`App` 是 human-facing truth。 |
| `RML-BAS-003` | `ble_qos_demo_V1.2m/ble_api.yaml` 是目前 wire / GATT / opcode semantics 的技術 SSOT。 |
| `RML-BAS-004` | `--base-dir` 已被定義為 cross-repo orchestration layer / common document center，但它只承接 control-plane formal docs，不複製 repo technical SSOT。 |
| `RML-BAS-005` | cross-repo governance 目前採 `report-first` 路線；`changed_only_report` 已存在，但還不是全面 blocking gate。 |
| `RML-BAS-006` | `Conductor` 在概念上已被承認為 orchestration actor，但 plugin implementation 仍有硬編碼路徑，尚未完全符合 project contract。 |
| `RML-BAS-007` | 現況允許部分人工 handoff、manual exception registry 與 queue promote decision；這些尚未全面腳本化。 |

## Target State

| ID | Target Statement |
| :--- | :--- |
| `RML-TGT-001` | 所有 cross-repo formal artifacts 必須可從 RML → requirements → acceptance → evidence → queue trace 回來。 |
| `RML-TGT-002` | 每種 truth 只允許一個 authority owner；non-owner 只能 render、cache、index、validate，不得重寫真相。 |
| `RML-TGT-003` | `Conductor` 必須依 `--base-dir/CURRENT.md`、project contract、repo CURRENT / SSOT 有固定 intake，並把結果回寫到 formal control-plane 路徑。 |
| `RML-TGT-004` | `cross-repo done` 只能在 owner repo docs / code / tests 與 `--base-dir` handoff / gate / evidence index 都對齊時成立。 |
| `RML-TGT-005` | repo-level technical truth 與 project-level orchestration truth 必須長期分層；`--base-dir` 不得變成第四份技術 SSOT。 |
| `RML-TGT-006` | 重大 wire / identity / assignment / auth 變更都必須有明確 migration path，而不是要求 consumer repo 同步瞬切。 |

## Migration Rules

| ID | Rule |
| :--- | :--- |
| `RML-MIG-001` | migration 的目的不是偷渡 target，而是讓 baseline 能安全收斂到 target。 |
| `RML-MIG-002` | 任何 dual-track、fallback、manual exception，都必須被明文標記為 `migration`，不得偽裝成 steady-state。 |
| `RML-MIG-003` | 若 owner repo 尚未 ready，consumer repo 可先做 shim / adapter / fallback，但必須保留回寫 owner repo 的 queue / handoff。 |
| `RML-MIG-004` | `Conductor` plugin 的硬編碼路徑、舊輸出位置、與新 project contract 不一致之處，只能視為 migration debt，不得視為 target。 |
| `RML-MIG-005` | render artifact、generated docs、report-first checks、manual exception registry 都可在 migration 期存在，但不得反客為主成為 authority truth。 |
| `RML-MIG-006` | 若 migration 需要 parallel path，必須說明哪一條是 baseline path、哪一條是 target path、何時關閉舊路。 |

## Allowed Migration Patterns

| ID | Pattern | Allowed When |
| :--- | :--- | :--- |
| `RML-MIG-007` | `report-first` governance | 規則已知有價值，但 gate 誤報率或 owner coverage 尚未穩定。 |
| `RML-MIG-008` | adapter / compatibility shim | owner contract 已變更，但 consumer repo 尚未同日收斂完成。 |
| `RML-MIG-009` | manual exception registry | 工具有缺口、展示阻塞、或存在明確暫時性例外，且後續修補路徑已落檔。 |
| `RML-MIG-010` | dual documentation path | 新 formal 路徑已建立，但舊路徑仍需短期維持引用相容。 |

## Forbidden Migration Patterns

| ID | Pattern |
| :--- | :--- |
| `RML-MIG-011` | 直接用 target 用語覆蓋 baseline reality，導致隊列、驗收與風險判斷失真。 |
| `RML-MIG-012` | 在 `--base-dir` 補寫一份 repo technical truth，藉此迴避 owner repo 更新。 |
| `RML-MIG-013` | 沒有 exit condition 的長期 dual-write / dual-truth。 |
| `RML-MIG-014` | 把 discussion、handoff、render 或 report 當成正式 steady-state authority。 |

## Acceptance Hooks

| Stage | Acceptance Meaning |
| :--- | :--- |
| `baseline` | 證明現況 truth 已被忠實描述，可被下一輪 AI / 工程師辨識與接手。 |
| `target` | 證明 steady-state owner、contract、acceptance 與 evidence model 已被定案。 |
| `migration` | 證明過渡期例外有邊界、有 owner、有退出條件，且不污染 target。 |

## Queue / Planning Hooks

- `baseline` 任務：盤點現況、補 formal truth、補 evidence、補 owner map。
- `target` 任務：建立穩態 contract、acceptance、queue governance、plugin 正式 intake / output 行為。
- `migration` 任務：adapter、compatibility、shim、promote、deprecation、exit criteria 收斂。

## References

- [rml-lite.md](rml-lite.md)
- [capability-ownership.md](capability-ownership.md)
- [requirements.md](requirements.md)
- [conductor-project-contract.md](../../--base-dir/docs/specs/conductor-project-contract.md)
- [acceptance-model.md](../../--base-dir/docs/specs/acceptance-model.md)
