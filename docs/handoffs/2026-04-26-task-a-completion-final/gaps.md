---
title: "Task A — Residual Gaps for Phase K"
date: 2026-04-26
---

## Residual Gap List (7 entries)

### Gap 1: Firmware Issue #88 — 3 Sub-Tasks Unresolved

`.clang-format` adoption decision, 30+ function-length violations (≥40L per structural
budget), and `docs/archive/` dead-link root-cure are all OPEN. The `code-lint.yml`
paths filter (PR #86) gates on `.clang-format` existence — adoption is currently off.

**Why it matters**: C Lint CI is not fully enforced; structural violations accumulate.
**Phase K action**: Close #88 in order: (a) adopt `.clang-format`, (b) enumerate +
fix function-length violations per module via separate PRs, (c) archive triage.

### Gap 2: ADR-008 PR #29 Still Open (mergeStateStatus=UNKNOWN)

ADR-008 (Task A Completion Strategy) is not on origin/main. Decisions INDEX shows 7
accepted ADRs; the self-referential decision that authorized Phase J is not canonical.

**Why it matters**: The governance rationale for Task A is unauditable from main.
**Phase K action**: Merge PR #29 as first Phase K gate; update INDEX to accepted=8.

### Gap 3: Dual trace_map Divergence — No Reconciliation CI

`spec-pack/trace/trace_map.yaml` and `workspace/docs/trace_map.yaml` are separate files
with overlapping SEQ- semantics. A SEQ entry added to one will not appear in the other;
CI does not detect the discrepancy.

**Why it matters**: Traceability chain becomes unreliable; invisible spec drift.
**Phase K action**: Define canonical owner (spec-pack upstream); add CI check in
workspace ensuring `docs/trace_map.yaml` SEQ entries match spec-pack's, or consolidate.

### Gap 4: Staleness Check Advisory — No Blocking Gate

All 3 downstream repos have `spec-staleness-check.yml` as advisory only. A stale
ubiquitous-language.md mirror does not block merge. Workspace has no staleness check.

**Why it matters**: Governance intent exists but has no mechanical teeth downstream.
**Phase K action**: Promote staleness check to blocking required status check (via
Ruleset) for firmware and central. Add staleness check to workspace repo.

### Gap 5: Enforcement Chain Not Extended to Downstream Repos

Only spec-pack has a GitHub Ruleset (id=15563210). Firmware/app/central have no
rulesets; deprecated terms (`RML-FEA-*`, bare `S-N`, `X-N`) can merge without block.

**Why it matters**: Vocab enforcement is single-repo; cross-repo term drift is possible.
**Phase K action**: Create GitHub Rulesets for firmware/app/central requiring their
respective CI checks (impl-tag lint, C structural check) as blocking status checks.

### Gap 6: V-Model Open Questions Unresolved

App `03_impl.md` has empty OQ section. Central has 2 unresolved OQs (FEA-004
reconciliation state machine + telemetry staleness threshold) with no owner or timeline.
These gate `05_acceptance.md` sign-off.

**Why it matters**: IMPL FREEZE cannot be lifted until OQs are closed with evidence.
**Phase K action**: Schedule OQ resolution sessions; close with spec-pack cross-links
before any FEA-001~004 IMPL FREEZE lift is attempted.

### Gap 7: arc42 §2 Constraints Chapter Absent

No dedicated constraints document (arc42 §2) exists. Technical, organizational, and
regulatory constraints (BLE SIG, NCC, FCC, IEC 62443 SL-1, clean-room boundary) are
scattered or undocumented.

**Why it matters**: New contributors cannot find system boundary constraints; audit risk.
**Phase K action**: Add `01_context-scope/constraints.md` covering all 4 constraint
categories; link from arc42 chapter INDEX.
