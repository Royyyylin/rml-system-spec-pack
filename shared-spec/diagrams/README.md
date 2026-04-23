# Diagrams 三層目錄規範

> 本目錄依**語意層次**區分圖種，各子目錄對應不同關注點。
> 既有 19 張圖（`architecture/` / `flow/` / `sequence/` / `state/`）**保留原位不遷移**，
> 新 diagram 一律進對應層目錄（Lazy Migration 規則）。

---

## 目錄分工

### `bdd/` — Actor 視角（行為場景層）

聚焦於**可被外部觀察的行為**，不涉及內部模組實作。

| 圖種 | 副檔名 | 用途 |
|------|--------|------|
| Sequence（高層時序） | `.mmd` | 跨系統角色互動，對應 BDD scenario |
| State（高層狀態機） | `.mmd` | 對 actor 可見的狀態轉換（非內部 dispatcher） |
| Use Case | `.mmd` | 角色意圖與系統邊界，用於 BDD 入場白 |

**生成時機**：執行 `/spec-bdd <FEATURE-ID>` 後輸出。

---

### `contract/` — Wire 細節層

聚焦於**跨系統邊界的資料格式**，與 `ble_api.yaml` SSOT 強綁定。

| 圖種 | 副檔名 | 用途 |
|------|--------|------|
| Packet layout | `.d2` | Opcode / field / byte offset / size 佈局 |
| Schema hierarchy | `.mmd` | CBOR / JSON schema 結構層次 |

**生成時機**：執行 `/spec-contract` 後輸出；Spectral CI lint 通過為 DoD。

---

### `sdd/` — 內部模組層

聚焦於**實作細節**，供開發者 cross-reference 程式碼。

| 圖種 | 副檔名 | 用途 |
|------|--------|------|
| Module block | `.d2` | 模組邊界 / 介面 / 相依關係 |
| State detailed | `.mmd` | dispatcher 或 subsystem 完整狀態機 |
| Sequence detailed | `.mmd` | 含函式名稱 / 回傳值 / 錯誤碼的詳細時序 |

**生成時機**：執行 `/spec-sdd` 後輸出；`check-trace-coverage.py` 100% 為 DoD。

---

## Lazy Migration 規則

1. **既有 19 張圖**（`architecture/` / `flow/` / `sequence/` / `state/`）**不移動**，
   保留在原目錄以維持現有 spec cross-reference 的連結正確性。
2. **新圖**建立時，依上表選擇正確層目錄後直接放入，不放舊目錄。
3. 若遷移舊圖有明確需求（如 refactor spec），在 PR 中明示並更新所有引用連結。

---

## 圖種選用原則

**Mermaid 優先，D2 次選**：

| 優先 | 情境 |
|------|------|
| Mermaid (`.mmd`) | 時序 / 狀態機 / 流程 / Use Case / Schema — GitHub native render |
| D2 (`.d2`) | Packet layout / Module block — 需要精確空間控制或 box/edge 語意 |

---

## AI Diagram Contract 規範

所有 `.d2` / `.mmd` 檔案頂部必須帶 `AI Diagram Contract` comment block，格式如下：

**Mermaid（`.mmd`）：**

```
%%{
  AI Diagram Contract:
  - purpose: <一句話說明此圖的主訊息>
  - layer: bdd | contract | sdd
  - ssot: <對應 spec 檔或 ble_api.yaml 段落>
  - trace: <REQ-XXX-NNN 或 FEATURE-ID>
  - author: <AI agent ID 或 human>
  - last_reviewed: <YYYY-MM-DD>
}%%
```

**D2（`.d2`）：**

```
# AI Diagram Contract
# purpose: <一句話說明此圖的主訊息>
# layer: bdd | contract | sdd
# ssot: <對應 spec 檔或 ble_api.yaml 段落>
# trace: <REQ-XXX-NNN 或 FEATURE-ID>
# author: <AI agent ID 或 human>
# last_reviewed: <YYYY-MM-DD>
```

此規則衍生自 `~/Projects/ble_qos_demo/AGENTS.md` → Rules for AI Agents。

---

## 既有目錄對照表（Legacy）

| 舊目錄 | 新層對應 | 備註 |
|--------|----------|------|
| `architecture/` | `sdd/` 或 `bdd/`（依圖種） | 保留不動，新圖不放此 |
| `flow/` | `bdd/`（高層）/ `sdd/`（詳細） | 保留不動 |
| `sequence/` | `bdd/`（高層）/ `sdd/`（詳細） | 保留不動 |
| `state/` | `bdd/`（actor 可見）/ `sdd/`（dispatcher） | 保留不動 |

---

*版本：2026-04-23 | 生效範圍：所有新建 diagram*
