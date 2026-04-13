# Diagram Templates

Status: formal

## Purpose

把常用 diagram 版型固定成少數幾個 `template_id`，避免每次都從零設計版面，導致圖雖然正確卻越畫越難讀。

## Rules

- 每個正式 `.d2` / `.mmd` 都必須宣告一個 `template_id`
- 若現有模板放不下內容，優先拆圖，不新增臨時模板
- 新模板必須先寫進本文件，再可被其他圖採用

## Templates

| Template ID | Diagram Types | Shape | Max Nodes | Max Groups | Use When |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ctx-owner-merge-state` | `d2-context` | 2 個 truth sources + 1 個 app/merge + 1 個 state/output + 1 個 rule callout | 5 | 3 | feature 要表達「兩個來源如何進入同一個 human-facing 狀態」 |
| `ctx-owner-fallback` | `d2-context` | 2 個 sources + 1 個 app merge + 1 個 precedence/output + 1 個 rule callout | 5 | 3 | feature 要表達「多個名稱/來源如何依優先序顯示」 |
| `flow-dual-path-feedback` | `d2-flow` | 2 條輸入路徑 + 1 個 app feedback node + 1 個 rule callout | 5 | 3 | feature 要表達「兩條 command / control path 最後回到同一個 UX 結果」 |
| `flow-linear-gate` | `d2-flow` | 1 條主流程 + 1 個 review gate + 1 個 revise loop + 1 個 current-state callout | 9 | 3 | 規劃流程圖要表達「按部就班往下走，review 未過就回修」 |
| `map-source-surface` | `d2-block` | 1 個 source cluster + 1 個 processing cluster + 1 個 UI/output cluster | 8 | 5 | block / architecture 圖要表達資料從來源到畫面的映射 |
| `map-service-use` | `d2-map` | 1 個 service / source + 1 個 packet / element cluster + 1 個 use cluster | 8 | 3 | packet / service 圖要表達規格元素與用途對應 |
| `state-dual-fsm` | `stateDiagram-v2` | 1 到 2 個 top-level FSM | 10 | 2 | state 圖只需表達少數核心狀態機 |
| `sequence-main-branch` | `sequenceDiagram` | 3 到 4 個 actors + 1 條主流程 + 1 個重要 branch | 8 | 3 | sequence 圖重點在主流程，不是完整協定追蹤 |

## Selection Guide

- 如果圖的主訊息是「誰擁有 truth、App 怎麼合併」：
  用 `ctx-owner-merge-state`
- 如果圖的主訊息是「名稱 / metadata / fallback 怎麼排序」：
  用 `ctx-owner-fallback`
- 如果圖的主訊息是「兩條命令路徑最後怎麼回到 UX」：
  用 `flow-dual-path-feedback`
- 如果圖的主訊息是「規劃流程怎麼往下走、卡在哪個 review gate」：
  用 `flow-linear-gate`
- 如果一張圖想同時講 ownership、state、flow、packet：
  不要找新模板，拆圖

## Golden Examples

- `ctx-owner-merge-state`:
  `shared-spec/feature-telemetry-roster-visibility.d2`
- `flow-dual-path-feedback`:
  `shared-spec/feature-command-execution-feedback.d2`
- `ctx-owner-fallback`:
  `shared-spec/feature-identity-alias-metadata-display.d2`
- `state-dual-fsm`:
  `app-spec/state_diagram.mmd`

## Review Gate

- 新人是否 10 秒內說得出圖的主訊息
- 是否符合對應模板的 shape，而不是偷偷把第二張圖塞回同一張
- 是否用 template 先限制資訊量，而不是靠 reviewer 事後砍圖
