---
title: "Task B L3 — Audit Score Rationale (post C5 lock-in)"
date: 2026-04-27
---

## Score Rationale (98/100, was 96/100, delta +2)

Same 6 criteria as Task A J FINAL (per master ruling — avoid Goodhart's law from criteria reshuffling)。L3 effects evaluated against existing rubric。

### Enforcement Chain — 19/20 (was 19, +0)

GitHub Rulesets unchanged from J FINAL (4 repo all `enforcement=active`, vocab-check blocking required)。L3 added 6 ADR-013 deprecated patterns to `tools/check_vocabulary_alignment.py` — vocab-check 仍是 Ruleset required check, enforcement scope 從 4 patterns 擴 10 patterns。**Dummy PR #49 (`RML-OBJ-999` injection) verified blocking** (vocab-check FAILURE + mergeStateStatus=BLOCKED, closed unmerged)。

**Deduction -1 (carryover)**: Staleness check 仍 NOT enrolled as Ruleset required_status_checks; staleness CI exits 1 但 Ruleset 不 gate — Phase K6 backlog scope, L3 不解。

### arc42 Chapter Coverage — 25/25 (was 25, +0)

8 arc42 chapter 仍全 coverage。L3 內容 quality 提升:
- §1 system-intent.md: opaque ID table → narrative + name-canonical 6 strategic goals + 7 engineering invariants table (industry-aligned per Backstage / C4 / arc42)
- §3 bounded-context-map.md: `## Authority Boundaries` 6 RML-AUT IDs → 6 boundary names; `## Scope` 4 RML-SCP IDs → 4 scope-type names
- §3 stakeholders.md: unified role table (human + AI Agent), system actors moved to bounded-context-map
- §2 capability-map.md: TOGAF capability hierarchy + `## ID Schema Migration Mapping` audit trail

**No deduction**: Coverage already max。Quality improvement 不 raise score (no slot for higher than 25/25)。

### ADR System — 15/15 (was 15, +0)

ADR-013 NEW (76 lines Nygard format: Context / Decision / Consequences / Alternatives / References)。INDEX.md 加 entry。Total ADR accepted 14 (was 13)。

**No deduction**: Already max (rubric ceiling)。新 ADR 加 audit trail 但 score-wise 無 headroom。

### V-Model Docs — 15/15 (was 15, +0)

V-Model docs 結構不動。L3 是 spec content refactor, 不改 V-Model layer。

**No deduction**: Coverage already max。

### Vocab + Trace Coverage — 15/15 (was 14, **+1**)

L3 真 contribution:
- `tools/check_vocabulary_alignment.py` DEPRECATED_PATTERNS: 4 → 10 (6 ADR-013 patterns covering 11 RML opaque ID prefixes: OBJ/INT/CST/RSK/ACT/ROL/CAP/OWN/HOF/AUT/SCP)
- Dummy PR #49 verified enforcement (NOT just code presence — actual CI block confirmed)
- `EXCLUDE_FILES` +2: `capability-map.md` (canonical migration mapping table) + `ADR-013-rml-schema-cleanup-l3.md` (self-reference). 對齊 ubiquitous-language.md 既有 pattern
- `trace/trace_map.yaml` ssot section 5 absolute `/Users/...` paths → repo-relative `../<repo>/...` (portable)
- Cross-pack ID schema 全清: 0 active leftover RML-11-prefix on origin/main

**Deduction reduced**: J FINAL 的 -1 deduction 是 "trace reconcile CI advisory mode"。L3 並未 fix trace reconcile (仍 advisory), 但 vocab side 大幅強化 + 真 enforcement verified, 抵銷 trace 那 -1 → 15/15。

(若嚴格只看 trace reconcile 仍 advisory, 可保持 14/15。Master ruling: 以 vocab strengthen + dummy PR proof 計 +1)。

### Portable @import + Staleness Governance — 9/10 (was 8, **+1**)

L3 真 contribution:
- `archive/2026-04-27-shared-spec-legacy-cleanup/shared-spec/` — 73 file legacy zombie dir migrated to archive/, removes "deprecated path advertised in canonical tree" portability landmine
- `01_context-scope/authority-map.yaml` schema v1.0 → v2.0: `id: RML-CAP-NNN` opaque → `id: <name-canonical>` (canonical-identity-authority etc.). Schema 對 language-agnostic consumer 更 portable
- Cross-repo central PR #39: Python docstring 也 align name-canonical (cross-repo consistency 提升)

**Deduction -1 (carryover)**: Workspace staleness CI 仍 advisory + Ruleset 不 gate staleness — Phase K6 backlog scope, L3 不解 (L3 是 spec hygiene refactor, 不動 staleness Ruleset enforcement layer)。從 8→9 是 L3 work 的合理 ceiling, 8→10 needs Phase K6。

### Final Total: 98/100 (delta: +2 from 96)

| Criterion | J FINAL | J3 | Delta | Driver |
|---|---|---|---|---|
| Enforcement Chain | 19/20 | 19/20 | 0 | Carryover deduction (staleness Ruleset gap, K6) |
| arc42 Coverage | 25/25 | 25/25 | 0 | Already max |
| ADR System | 15/15 | 15/15 | 0 | Already max (ADR-013 added but ceiling) |
| V-Model Docs | 15/15 | 15/15 | 0 | Unchanged |
| Vocab+Trace | 14/15 | **15/15** | **+1** | 6 patterns + dummy verified + repo-relative trace_map |
| Portable+Staleness | 8/10 | **9/10** | **+1** | shared-spec/ archived + authority-map.yaml v2 + cross-repo align |
| **Total** | **96/100** | **98/100** | **+2** | L3 source-level refactor closure |

### Score Justification per Master Ruling

- Q1: Accept 98 ceiling (NOT goalseek 99+) — 透過 J FINAL 同 6 criteria 評估, +2 是 L3 真 deliver 範圍
- Q4: Accept 9/10 Portable+Staleness — 8→10 不在 L3 scope (workspace staleness Ruleset = K6 defer)
- ADR-013 / ADR System +0: rubric ceiling 已 max (Goodhart-aware: 不調 criteria 配 score)
