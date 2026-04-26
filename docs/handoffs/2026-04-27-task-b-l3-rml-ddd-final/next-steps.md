---
title: "Task B L3 — Phase K6 Backlog (defer items)"
date: 2026-04-27
---

## Phase K6 Backlog (Architecture Foundation Review 2.0)

Task B L3 closure 後 maturity 從 96 → 98。要進 99+ / 100 需動 staleness enforcement + advanced architecture deliverables。Phase K6 候補項目按 priority 排序:

### P1 — Enforcement Maturity (close last 2 deduction)

#### K6-001: Trace reconcile CI blocking mode

- **Goal**: `tools/check_trace_reconcile.py` 從 advisory `exit 0` → `exit 1` on divergence
- **Effort**: tool docstring + return code change + CI workflow exit-on-fail
- **Score impact**: +0 (Vocab+Trace 已 15/15)
- **Side benefit**: 真強制 trace_map upstream/downstream sync

#### K6-002: Workspace staleness exit 1 + Ruleset gate

- **Goal**: 4th consumer repo (workspace) 也升 `scripts/check-spec-staleness.sh` exit 1; 加 Ruleset `required_status_checks` 含 staleness check
- **Effort**: workspace script change + CI + Ruleset config update (4 repo 一致)
- **Score impact**: +1 (Portable+Staleness 9 → 10)
- **Side benefit**: 真 gate spec drift, no advisory escape hatch

#### K6-003: Staleness Ruleset enforcement (cross 4 repo)

- **Goal**: 4 repo Ruleset 加 staleness 為 required (currently only vocab-check required)
- **Effort**: GitHub API config across 4 repo Ruleset
- **Score impact**: +1 (Enforcement Chain 19 → 20)
- **Side benefit**: 真 lock-down spec drift, 完整 Ruleset enforcement matrix

完成 K6-001/002/003 → Score 98 → **100/100** (rubric ceiling)。

### P2 — Architecture Maturity (post-rubric improvement)

#### K6-004: C4 model dynamic view diagrams

- **Goal**: 既有 D2 system context + container view 加 C4 dynamic view (sequence-overlay) for FEA-001 / FEA-004 主流程
- **Why**: arc42 §5 (building blocks) + §6 (runtime) 互補, 目前只 static
- **Effort**: 2-3 .d2 source + AI Diagram Contract block

#### K6-005: Strategic Domain integration (DDD higher-level)

- **Goal**: 既有 bounded context map (4 context) 升 DDD strategic design — Core / Supporting / Generic subdomain classification + strategic alignment to business priority
- **Why**: arc42 §3 完整 DDD 三層 (Tactical / Strategic / Vision)
- **Effort**: 1 new doc `01_context-scope/strategic-domain-classification.md`

#### K6-006: Living Doc HTML publish (per ADR-001 deferred)

- **Goal**: arc42 chapter 自動 build to static HTML site (Docusaurus / Material for MkDocs)
- **Why**: ADR-001 既有 deferred 決議, 進 K6 啟用
- **Effort**: build pipeline + GH Pages deploy + ADR-001 status update

### P3 — Tooling Polish

#### K6-007: Section-level vocab-check pragma

- **Goal**: `tools/check_vocabulary_alignment.py` 支援 inline pragma (`<!-- vocab-check: ignore-block -->...<!-- vocab-check: end -->`) 取代整檔 EXCLUDE_FILES
- **Why**: capability-map.md migration table 是 section, 不是整檔。Section-level 更精確, 防誤用。
- **Effort**: tool refactor + migration mapping table 加 pragma marker + EXCLUDE_FILES 移除 capability-map.md

#### K6-008: Sparse-Telemetry-Is-Normal invariant CI test

- **Goal**: 為 `Sparse-Telemetry-Is-Normal` engineering invariant (system-intent.md `## Engineering Invariants` 段) 加入 App ViewModel render unit test, currently no CI enforcement (P0 sparse 不視為 error 是 UI 渲染 rule, 沒 CI test backstop)。
- **Why**: 該 invariant statement 目前只靠 honest naming (`App ViewModel render rule (ble_qos_app — no CI test enforcement; K6-008 backlog)`) 標示, 沒實際 CI gate 防 regression。
- **Effort**: ble_qos_app `lib/.../viewmodel/` 加 unit test for sparse telemetry rendering; CI 跑該 test on PR; 完成後 update system-intent.md Sparse-Telemetry row enforcement mechanism 移除 K6-008 backlog 標。

## EOD Recommendation

- 短期 (this session 後): Roy `/eod` 寫 final handoff doc, J3 score 98 + Task B L3 closed
- 中期 (next session): K6-002 + K6-003 (close enforcement matrix → score 99-100)
- 長期: K6-005 / K6-006 (DDD + Living Doc 業界對齊提升)

## Cross-ref

- L3 master plan: `~/.claude/plans/task-b-rml-ddd-refactor.md`
- ADR-013 lock-in decision: `99_appendix/decisions/ADR-013-rml-schema-cleanup-l3.md`
- J FINAL handoff (baseline 96): `docs/handoffs/2026-04-26-task-a-completion-final/`
- J3 audit plan: `~/.claude/plans/task-b-rml-ddd-refactor/J3.md`
