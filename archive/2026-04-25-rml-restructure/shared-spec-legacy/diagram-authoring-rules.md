# Diagram Authoring Rules

Status: formal

## Purpose

把 `.d2` / `.mmd` 的產出規則固定成可被人與 AI 共用的契約，避免圖只對產生它的模型有意義，卻不利於後續閱讀、review、維護與重畫。

## Scope

- 適用於 `rml-system-spec-pack/shared-spec/`、`app-spec/`、`firmware-spec/` 內的 `.d2` / `.mmd`
- `renders/` 仍是 derived artifact；正式治理來源是 source diagram
- 本規則約束的是 diagram source 與其 prompt contract，不直接約束 render 版面細節

## Core Rules

| ID | Rule |
| :--- | :--- |
| `DAR-001` | 每張圖只表達一個 primary message；若同時有兩個主訊息，必須拆圖。 |
| `DAR-002` | 每張圖都必須先指定 `reader`，再決定節點、詞彙與圖種。 |
| `DAR-003` | 圖種必須刻意選擇；流程用 flow / sequence，狀態用 state，靜態結構用 block / context。 |
| `DAR-004` | label 應短且可掃讀；優先 3 到 5 個字詞，不把完整規格句子塞進節點。 |
| `DAR-005` | 若 major nodes 超過 8 個，或 major groups 超過 5 組，應拆成兩張圖，不硬塞一張。 |
| `DAR-006` | 規則與限制優先集中成 2 到 3 個 callout，不把所有限制寫在每條線上。 |
| `DAR-007` | diagram source 開頭必須有 `AI Diagram Contract` comment block，讓後續 AI 可直接續寫。 |
| `DAR-008` | 每張圖都必須選用已登記的 `template_id`；若模板不適用，先補模板 spec，不直接自由發明新版型。 |
| `DAR-009` | feature markdown 以 render 作為閱讀入口；source diagram 仍是治理來源，不得省略。 |

## AI Diagram Contract

每個 `.d2` / `.mmd` 檔案開頭都必須有 comment block，至少包含：

| Field | Meaning |
| :--- | :--- |
| `AI-DIAGRAM` | 固定填 `required`，表示此圖受本契約約束 |
| `primary_message` | 這張圖只想讓讀者記住的一句話 |
| `reader` | 主要讀者，例如 `newcomer`、`engineer`、`reviewer` |
| `template_id` | 必須對應 `diagram-templates.md` 裡已登記的模板 |
| `diagram_type` | 圖種，例如 `d2-context`、`sequenceDiagram`、`stateDiagram-v2` |
| `layout` | 版面方向，例如 `left-to-right`、`top-to-bottom` |
| `max_nodes` | 作者希望控制的 major node 上限 |
| `max_groups` | 作者希望控制的 group / cluster 上限 |
| `keep` | 必須保留的資訊重點 |
| `avoid` | 明確不要塞進圖裡的內容 |

備註：
- `.d2` 可用 `#` 或 `//` 註解
- `.mmd` 用 `%%` 註解
- `max_nodes` / `max_groups` 是 authoring intent，不是 render engine 保證值
- `template_id` 定義見 [diagram-templates.md](diagram-templates.md)

## Prompt Templates

### D2

```text
請依下列 Diagram Contract 產生或重寫 `.d2`，目標是給人類快速閱讀，而不是把所有細節塞滿。

primary_message: <一句話主訊息>
reader: <newcomer / engineer / reviewer>
template_id: <diagram-templates.md 中的合法值>
diagram_type: <d2-context / d2-block / d2-flow>
layout: <left-to-right / top-to-bottom>
max_nodes: <數字>
max_groups: <數字>
keep: <必保留重點>
avoid: <不要塞進圖裡的內容>

要求：
- 每張圖只表達一個主訊息
- 先選 template，再填內容
- label 短，不寫完整規格句
- 規則集中成 2 到 3 個 callout
- 若內容超過上限，拆成兩張圖
- 輸出只要合法 `.d2`
```

### Mermaid

```text
請依下列 Diagram Contract 產生或重寫 `.mmd`，優先讓新人與 reviewer 看懂主流程。

primary_message: <一句話主訊息>
reader: <newcomer / engineer / reviewer>
template_id: <diagram-templates.md 中的合法值>
diagram_type: <flowchart / sequenceDiagram / stateDiagram-v2>
layout: <left-to-right / top-to-bottom>
max_nodes: <數字>
max_groups: <數字>
keep: <必保留重點>
avoid: <不要塞進圖裡的內容>

要求：
- 先選正確圖種
- 先選 template，再填內容
- 每張圖只畫一條主敘事
- timeout / retry / conflict 只保留最重要的 2 到 3 個
- 用短 label；必要時拆圖，不硬塞
- 輸出只要合法 `.mmd`
```

## Review Checklist

- 新人是否能在 10 秒內說出這張圖的主訊息
- 是否符合對應 `template_id` 的 shape，而不是把第二張圖硬塞回同一張
- 是否一眼看得出 authority owner / primary flow / state boundary
- 是否有把 feature spec 已經寫清楚的長句重複塞進圖裡
- 是否把 source of truth、runtime truth、UI truth 混成同一層
- 是否需要拆成兩張圖才更清楚

## Enforcement

- 修改 `.d2` / `.mmd` 時，必須同步維護檔頭的 `AI Diagram Contract`
- 新圖必須先選 `template_id`；若沒有對應模板，先更新 `diagram-templates.md`
- 若 diagram source 改動，仍須遵守 `CIR-008`
- 最小檢查入口：
  `python3 rml-system-spec-pack/tools/check_diagram_contract.py`
