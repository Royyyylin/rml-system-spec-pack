---
title: "Task B L3 — Residual Gaps (post C5 lock-in)"
date: 2026-04-27
---

## Residual Gaps (2 entries, ≤ 2 per J3 expectation)

### Gap 1: Trace reconcile + Workspace staleness CI 仍 advisory mode

**Status**: Phase K6 backlog defer (NOT in L3 scope)

**Detail**:
- `tools/check_trace_reconcile.py` (spec-pack) 永遠 exit 0 (advisory by design per docstring); 雙 trace_map (spec-pack upstream + workspace downstream) divergence 顯示 `::warning::` 但不 block merge。
- Workspace `scripts/check-spec-staleness.sh` exits 0 (advisory-only); 4 consumer repo 中只 firmware/app/central 升 exit 1; workspace 仍 advisory。
- 兩個 staleness 都 NOT enrolled as Ruleset `required_status_checks`; CI 出 fail signal 但 Ruleset 不 gate merge。

**Why deferred**:
- L3 主題是 spec source-level refactor (廢 RML opaque ID schema), 不動 enforcement layer Ruleset config。
- 升級 workspace + Ruleset gating 屬 enforcement maturity, 應由 Phase K6 (Architecture Foundation Review 2.0) 處理, 跟 V-Model + Living Doc 一起。

**Impact**:
- 短期: 沒 worsen, 跟 J FINAL 同狀態。
- 長期: 若 trace_map drift 或 staleness 失同步 不會自動 block, 需人工 review CI warning。

### Gap 2: `capability-map.md` whole-file EXCLUDE_FILES (vs section-level exclusion)

**Status**: Tooling enhancement defer (low priority)

**Detail**:
- `tools/check_vocabulary_alignment.py` EXCLUDE_FILES 整檔豁免 `capability-map.md`, 因為 `## ID Schema Migration Mapping` table 內 14 RML-CAP/OWN/HOF entry 是 intentional Legacy ID column (audit trail per ADR-013)。
- 整檔豁免代價: 若未來有人在 capability-map.md 其他 section (Ownership Rules / Cross-Repo Capability Matrix etc.) 誤用 `RML-CAP-NNN`, vocab-check 不會 catch。
- 較精細方案: section-level pragma (e.g. `<!-- vocab-check: ignore-block -->...<!-- vocab-check: end -->`) 或 line-range 排除。

**Why deferred**:
- 目前 capability-map.md 內容已 frozen post-C3 + C5 — 非 hot file, 誤用 risk 低。
- 加 pragma 邏輯需 tool refactor + 跨 file pattern 一致性, 屬 tooling improvement, 不在 L3 spec refactor scope。

**Impact**:
- 短期: 0 (audit trail 完整, 無 active violation)。
- 長期: 若有人改 capability-map.md 其他 section 加 RML- ID, 不會被 catch。Manual review 可 backstop。

## Why ≤ 2 (NOT 0)

J3 plan 預期 "residual gap ≤ 2"。L3 達 2 entries:
- 兩 gap 都是 carryover (J FINAL 既有 deduction) 或 tooling defer, **NOT L3 introduce 新 gap**。
- L3 真 closure 0 leftover (paranoid grep 確認), enforcement verified (dummy PR #49)。
- 若 K6 解 staleness Ruleset → score 從 98 推 99+。

## Phase K6 Backlog (next phase scope)

詳見 `next-steps.md`:
1. Trace reconcile blocking mode + Ruleset enrollment
2. Workspace staleness exit 1 + Ruleset enrollment
3. (optional) capability-map.md section-level vocab exclusion
4. C4 dynamic view diagrams (architectural runtime view)
5. Strategic Domain integration (DDD higher-level)
6. Living Doc HTML publish (per ADR-001 deferred decision)
