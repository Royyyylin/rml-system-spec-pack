# ADR-013: RML Opaque ID Schema Cleanup — L3 Source-Level Refactor

Status: accepted
Date: 2026-04-27
Decided by: Roy (post Task A J FINAL 96/100 audit + L1/L2 plan rejection)

## Context

Task A J FINAL 96/100 re-audit 漏抓 `rml-system-spec-pack` 內 27 RML schema reference + 10 inbound cross-pack ref。2 paranoid Explore agent 確認: schema source 全在 spec-pack (跨 4 consumer repo 0 hit) — spec-pack 是 sole authority 也是 sole defender。

`RML-(OBJ|INT|CST|RSK|ACT|ROL|CAP|OWN|HOF|AUT|SCP)-NNN` 11 prefix 為 v0/v1 階段引入的 opaque ID schema, 設計目的是 machine-traceability。實際運行下發現:

- **業界 reference 對齊不足**: Backstage `kind: System` + entity name / C4 person/system 靠 name / arc42 prose narrative — 全是 name-canonical, NO opaque ID layer。RML 11 prefix 是過度工程 (over-engineered) 的私有 schema, 沒對應任何業界框架。
- **Cross-ref 認知負擔**: reader 需先解析 ID 到 name (查表), 再讀 narrative。Markdown 原生 `file.md#section-anchor` 已支援精確跨檔錨點, 不需自定 ID。
- **AI continuator 維護成本**: 新 AI 接手須先學 11 prefix 命名規範 + 反查表; name-canonical zero learning cost。
- **重複維護**: ID 與 name 雙 SSOT, drift 風險高 (name 改 ID 沒改 / 反之亦然)。

L1 surface rename plan (RML-OBJ-001 → OBJ-001) 與 L2 mid-rename plan 都被 Roy 拒, 因為這只是換 prefix 不解決 schema 本身的 over-engineering。

## Decision

採 **L3 source-level refactor** — 廢 11 RML opaque ID schema, 改:

1. **Name-canonical primary key** (D1): 概念 (intent / goal / invariant / risk / role / capability / ownership / handoff) 用 short descriptive name 作 primary identifier, 例:
   - `RML-OBJ-001` → `SSOT-Driven-UI-Semantics`
   - `RML-INT-002` → `Cross-Repo-Authority-Boundary`
   - `RML-CAP-004` → `Wire-Contract-Authority`
   - `RML-RSK-001` → `GATT-Contract-Drift`
2. **Chapter-position-canonical** (D2): arc42 章節檔 (`00_introduction-goals/system-intent.md` etc) 自身為 SSOT location, 不需額外 ID 層級。
3. **Cross-ref by `file.md#section-anchor`** (D3): Markdown native anchor (GitHub kramdown rule), NOT custom ID prefix。trace_map.yaml 用 file:section position。

Refactor 分 5 atomic sub-plan (C1 cornerstone → wave1 C2/C3/C4 parallel → C5 lock-in):
- C1: `system-intent.md` narrative rewrite (起點)
- C2: `stakeholders.md` + `bounded-context-map.md` actor refactor
- C3: `quality-goals.md` + `capability-map.md` name-canonical (含 ID Schema Migration Mapping 保留歷史)
- C4: `constraints.md` + `risks-and-debt.md` + `requirements.md` cross-ref
- C5: `trace_map.yaml` ID-less + `check_vocabulary_alignment.py` 加 6 deprecated pattern + ADR-013 (本檔) + Spec Hygiene Rule 13 update

L3 master plan: `~/.claude/plans/task-b-rml-ddd-refactor.md` (5 sub-plans)。

## Consequences

**Positive:**

- 業界對齊 — Backstage / C4 / arc42 全 name-canonical, refactor 後 spec-pack 同框架
- AI continuator zero learning cost — 不用學 RML 命名規範, 直接讀 narrative
- 認知負擔下降 — name 即內容, 不需 ID→name 反查
- Cross-ref 用 Markdown native anchor — 編輯器原生支援, 不需自定工具
- vocab-check enforce 防復發 — 6 RML deprecated pattern 進 CI blocking, dummy PR 驗證 mergeStateStatus=BLOCKED
- ADR + Migration Mapping table 保留 audit trail — 歷史 ID 仍可追溯

**Negative:**

- 一次性 disruption — 4 PR (C1-C4) + cleanup PR (#47) 共 5 PR landed 2026-04-26~27, 期間下游 reader 需切換認知
- ADR-013 + capability-map.md migration table 成為文件記憶 — 法 retire (但體積很小)
- vocab-check 增 6 regex pattern — 微量 CI 時間增加 (< 5% scan time)

**Compensating control:**

- `02_solution-strategy/capability-map.md` `## ID Schema Migration Mapping` 保留 11 legacy ID → canonical name 對照, 任一未來 reader 遇到舊 ID 可一查到名。
- `99_appendix/decisions/ADR-013` (本檔) 保留 decision rationale + alternatives, 跨 session AI 不會重新發起同樣 debate。

## Alternatives

- **L1 surface rename** (RML-OBJ-001 → OBJ-001): Rejected — 只換 prefix, schema over-engineering 未解決, 業界對齊還是不足
- **L2 mid-rename + schema 保留**: Rejected (Roy explicit) — 同 L1 問題, 補丁式重構
- **Keep RML legacy schema unchanged**: Rejected — 業界對齊不夠, AI continuator 維護成本持續累積
- **Generate name from ID via tooling**: Rejected — 雙 SSOT drift 風險, 違反 no-hardcoding 原則 (id + name 兩個都要維護)
- **Per-prefix piecemeal migration over months**: Rejected — context rot 風險, 半新半舊狀態下 cross-ref 不一致更糟

## References

- L3 master plan: `~/.claude/plans/task-b-rml-ddd-refactor.md`
- C1 PR: #43 (system-intent narrative rewrite)
- C2 PR: #44 (stakeholders + bounded-context)
- C3 PR: #46 (quality-goals + capability-map)
- C4 PR: #45 (constraints + risks + requirements)
- Wave 1 cleanup PR: #47 (5 file cross-pack inbound refs)
- Spec Hygiene Rule 13: `~/.claude/spec-hygiene-rules.md` (VOCABULARY_CANONICAL)
- Industry references: [Backstage System catalog](https://backstage.io/docs/features/software-catalog/descriptor-format) / [C4 model](https://c4model.com/) / [arc42 template](https://arc42.org/overview)
- ADR-008: Task A Completion Strategy (parent context — J FINAL 96/100 audit driver)
- vocab-check tool: `tools/check_vocabulary_alignment.py` (DEPRECATED_PATTERNS list)
