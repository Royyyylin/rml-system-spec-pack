# Spec Pack Governance Session Notes

Status: discussion
Date: 2026-04-08
Scope: 記錄本輪對 `rml-system-spec-pack` 的治理架構討論，避免上下文流失。

## Purpose

這份文件不是正式規格，而是本輪討論記錄。
用途是保留：
- 已定方向
- 暫定治理原則
- 待定問題
- 後續升格為 formal spec 的候選內容

## Confirmed Direction

### 1. 規格治理骨架

採用 5 層治理骨架：
- 上游意圖層
- 下游工程層
- traceability
- change governance
- acceptance / test

### 2. 規劃視角

正式採用三個規劃視角：
- `baseline`
- `target`
- `migration`

這三者是全 pack 共用的 `stage` 概念。

### 3. 正式與討論分流

- `formal`：正式規格，可被引用、追蹤、檢查、連動更新
- `discussion`：研究與未定案內容，不可直接當正式真相來源

### 4. 文件與目錄分工

預期結構朝這個方向收斂：

```text
project/
├─ docs/
├─ diagrams/
├─ schemas/
├─ trace/
├─ renders/
└─ tools/
```

目錄分工原則：
- `docs/`：人類可讀的正式正文
- `diagrams/`：圖原始碼
- `schemas/`：結構化 SSOT
- `trace/`：追蹤與治理規則
- `renders/`：渲染產物
- `tools/`：render / lint / changed_only_report

### 5. README 定位

`docs/README.md` 應為 formal 入口文件，負責：
- 讀取順序
- 目錄用途
- SSOT 說明
- formal / discussion 關係
- 治理流程

README 不應重複詳細規格正文。

## Confirmed Content Strategy

### 1. RML-lite

`docs/rml_lite.md` 定位為上游控制面，不只是需求摘要。
至少包含：
- system intent
- stakeholders / roles
- boundaries / authority
- constraints
- migration principles
- risks / recovery

### 2. Requirements

`docs/requirements.md` 採正式需求表 + 短說明：
- 穩定 `REQ-*`
- 可 trace
- 不承載討論過程

需求討論另放：
- `docs/discussions/requirements/`
或更一般化的：
- `docs/discussions/`

### 3. Architecture / State / Sequence / Packet

以下文件採 `Baseline / Target / Migration`：
- `docs/architecture.md`
- `docs/state_machine.md`
- `docs/sequence_flows.md`
- `docs/packet_contract.md`

### 4. Acceptance / Test

`AC / TC` 維持單份收斂文件，不拆成三份。
每條項目以 `stage` 標示它屬於：
- `baseline`
- `target`
- `migration`

### 5. 大檔拆分

若單檔超過 `300` 行：
- 必須改成主文件 + `@IMPORT`
- 拆分單位必須是完整主題
- 不可為了壓行數機械切割

## Confirmed Source Strategy

### 1. schema-first vs doc-first

正式採用原則：
- 結構化內容：`schema-first`
- 敘事型內容：`doc-first`

#### schema-first 候選
- `packet_schema.yaml`
- `pin_map.yaml`
- `enum_definitions.yaml`

#### doc-first 候選
- `rml_lite.md`
- `requirements.md`
- `architecture.md`
- `change_rules.md`
- `source_of_truth.md`
- `README.md`

### 2. pin_map

`pin_map` 三種形式都要有，但只能有一個 SSOT：
- `schemas/pin_map.yaml`：SSOT
- `docs/pin_map.md`：人類說明
- `diagrams/pin_map.d2`：圖原始碼
- `renders/pin_map.png`：渲染結果

### 3. packet_contract

也採相同策略：
- `schemas/packet_schema.yaml`：結構化 SSOT
- `docs/packet_contract.md`：人類可讀敘事與治理說明

## Confirmed Governance Strategy

### 1. changed_only_report

正式定位為每次變更的必跑治理檢查，而不是可選工具。

責任拆分：
- `source_of_truth.md`：定權威來源
- `change_rules.md`：定理論上應更新哪些檔
- `changed_only_report`：比對 git diff，找出實際缺漏

### 2. tools 分類

`tools/` 至少分兩類：
- `render_*`：產生衍生產物
- `lint_*`：檢查同步與治理規則

建議分階段：
- `v1`：先做 `diagrams -> renders`
- `v2`：再做 `schemas -> docs fragments / diagrams`

### 3. formal source vs derived artifacts

`formal source artifacts`
- `docs/` 中的 formal 文件
- `schemas/*`
- `trace/*`
- `diagrams/*` 的 `.d2` / `.mmd`

`derived artifacts`
- `renders/*`
- generated outputs

原則：
- source 要過 formal gate
- derived 不過 formal gate

## Confirmed Enum Strategy

預計集中於 `schemas/enum_definitions.yaml`。

### stage
- `baseline`
- `target`
- `migration`

### v2 item status
- `idea`
- `evaluating`
- `drafted`
- `promoted`

### artifact_kind
- `docs`
- `diagrams`
- `schemas`
- `trace`
- `renders`
- `tools`

### doc_kind
- `formal`
- `discussion`

## V2 Direction Notes

V2 方向先記在 discussion，不直接升格 formal。

已整理到：
- `docs/discussions/spec-pack/v2-direction.md`
- `docs/discussions/spec-pack/changed-only-report-v1.md`

建議結構：
1. Why V2
2. V1 Known Gaps
3. Non-Negotiable Principles
4. V2 Target Directions
5. Open Questions
6. Promotion Criteria

### 擬建 V2 Governance Principles

1. 不可覆蓋 baseline truth
2. 不可混用 repo SSOT 邊界
3. discussion 不可直接升格為正式 spec
4. render artifact 不是 source of truth
5. 沒有 trace / AC / TC 的內容不可進正式包

### V2 item metadata

每個 V2 方向項目應至少有：
- `status`
- `impacts`

其中 `impacts` 應至少指出：
- `docs`
- `diagrams`
- `schemas`
- `trace`
- `AC`
- `TC`

## Formal Gate Draft

`formal` 第一版最小門檻：
1. 有明確用途與範圍
2. 有穩定可引用結構
3. 已納入治理
4. 可連動更新

## Resolved Decision

已定案：
- `renders/` 為 derived artifacts，原則上禁止手改
- render 變更應由 `docs/`、`schemas/`、`diagrams/` 或 render tool 產生
- 若因展示阻塞或工具缺口必須手改，必須明確標記為暫時性例外，並補回對應 source / tool 變更
- 手改後的 render 不得被視為 source of truth

已同步到：
- `trace/source_of_truth.md`
- `trace/change_rules.md`
- `README.md`
