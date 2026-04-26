# Spec Pack V2 Direction

Status: discussion
Date: 2026-04-08
Scope: 定義 `rml-system-spec-pack` 下一階段治理方向，作為後續討論與升格 formal 的承接點。

## Why V2

V1 已經把這個 spec pack 拉回到正確方向：
- 以三個 repo 的現行 SSOT 為準
- 有 formal / discussion 分流
- 有 trace / change rules / AC / TC 的治理骨架

但 V1 仍偏人工治理，還沒有把規則完全落到結構與工具。
V2 的目的不是重做 spec pack，而是補齊以下能力：
- artifact 類型分層更清楚
- schema-first 領域有正式落點
- changed-only governance 可執行
- render / lint / promotion 流程可檢查

## V1 Known Gaps

1. 目前主結構（v1 時期）仍偏領域切分（`app-spec/`、`firmware-spec/`），尚未真正收斂到 arc42 章節切分（`00_introduction-goals/`~`06_crosscutting-integration/`）。
2. `changed_only_report` 目前是治理要求，不是已存在的工具。
3. `schema-first` 候選已提出，但 `packet_schema.yaml`、`enum_definitions.yaml`、`pin_map.yaml` 尚未成為正式內容。
4. `renders/` 已定義為 derived artifacts，且原則上禁止手改，但例外註記與檢查流程仍未具體化。
5. `desktop-spec/` 目前沒有正式來源，仍停在保留位置，不應假裝已有可維護內容。
6. render、lint、evidence 收斂仍靠人工判斷，沒有穩定的 promotion gate。

## Non-Negotiable Principles

1. 不可覆蓋 baseline truth。
2. 不可混用 repo SSOT 邊界。
3. discussion 不可直接升格為正式 spec。
4. render artifact 不是 source of truth。
5. 沒有 trace / AC / TC 的內容不可進正式包。
6. 工具只能產生或檢查 artifact，不可反向改寫 repo SSOT。
7. V2 不得推翻 V1 已對齊的 repo truth，只能在其上加治理能力。

## V2 Target Directions

### `V2-001` Artifact-Oriented Layout

- `status`: drafted
- `impacts`: `docs`, `diagrams`, `schemas`, `trace`, `tools`
- 方向：逐步把 pack 收斂到 artifact-oriented layout，而不是長期維持 domain-first 混排。
- 約束：不能一次性大搬家；若要搬移，必須先有 migration plan 與引用相容策略。

### `V2-002` Schema-First Core Contracts

- `status`: evaluating
- `impacts`: `schemas`, `docs`, `trace`, `AC`, `TC`
- 方向：把高結構化內容正式收斂到 schema，例如：
  - `packet_schema.yaml`
  - `enum_definitions.yaml`
  - `pin_map.yaml`
- 約束：schema 成為 SSOT 前，必須先定欄位責任、版本策略與 doc 對應規則。

### `V2-003` Governance Automation

- `status`: drafted
- `impacts`: `tools`, `trace`, `docs`
- 方向：把目前口頭治理變成可執行工具，至少包括：
  - `render_*`
  - `lint_*`
  - `changed_only_report`
- v1 決策：先採 `report-first`，不直接作為 blocking gate
- 草案位置：`docs/discussions/spec-pack/changed-only-report-v1.md`
- 最低要求：能抓出 render-only diff、缺漏 trace fan-out、formal source 未同步等問題。

### `V2-004` Stage And Enum Normalization

- `status`: evaluating
- `impacts`: `schemas`, `docs`, `trace`, `AC`, `TC`
- 方向：集中管理 `stage`、`artifact_kind`、`doc_kind`、`v2 item status` 等 enum，避免多份文件各自定義。
- 目標：讓 trace、lint、promotion rule 能讀同一套語意。

### `V2-005` Promotion Gate

- `status`: idea
- `impacts`: `docs`, `trace`, `AC`, `TC`, `tools`
- 方向：把「什麼可以從 discussion 升格 formal」寫成最小可檢查門檻。
- 最低門檻應包含：
  - 有用途與範圍
  - 有穩定引用結構
  - 已納入 source of truth / change rules
  - 有 trace / AC / TC 連動

### `V2-006` Desktop Admission Rule

- `status`: idea
- `impacts`: `docs`, `trace`
- 方向：在 desktop repo 有正式 SSOT 前，不將 `desktop-spec/` 升格為正式內容。
- 目的：避免用想像中的 desktop 行為污染目前 formal pack。

## Open Questions

1. V2 要不要真的搬到 artifact-oriented layout，還是先維持現有目錄，只在內容與工具層收斂？
2. 哪些 `changed_only_report` 規則在量過誤報率後，適合升成 gate？
3. `trace/manual_exceptions.yaml` 長期要維持 trace-local，還是未來提升為跨 repo registry？
4. schema-first 的導入順序是 `packet` 先，還是 `enum` / `pin_map` 先？
5. discussion 升格 formal 時，最小 evidence bar 要求到什麼程度？

## Promotion Criteria

以下條件成立時，V2 方向中的項目才適合升格 formal：

1. 已有明確 owner 與對應 repo SSOT。
2. 已定義影響範圍，不再只是概念提案。
3. 已明確列出要更新的 formal artifacts。
4. 已補上 trace / AC / TC 的連動規則。
5. 已說明 migration path，不會破壞現有 pack 可讀性與引用。
6. 若涉及工具，至少已有可重跑的最小實作或明確執行入口。

## Current Working Rule

在 V2 未升格前：
- 現行 formal pack 仍以 V1 文件為準
- 新治理想法先記錄在 discussion
- 只有在 repo truth、trace、驗收與測試都能接住時，才進 formal
