---
title: "Task A — Residual Gaps (post-Phase 4 K)"
date: 2026-04-26
---

## Newly Closed Gaps (was 7, now 3 closed)

| Gap | Was | Status | Closed by |
|---|---|---|---|
| Gap 2: ADR-008 PR #29 open | ADR not on main | CLOSED | spec-pack PR#29 merged; INDEX accepted=13 |
| Gap 5: Enforcement not extended to downstream | Only spec-pack had Ruleset | CLOSED | K1: Rulesets on firmware/app/central/workspace, bypass_actors=[] |
| Gap 6: V-Model OQ unresolved | Empty OQ sections | CLOSED | K4-β/γ: Owner+Timeline tables on app PR#40 + central PR#38 |
| Gap 7: arc42 §2 absent | No constraints.md | CLOSED | K2: `02_solution-strategy/constraints.md` 146L on main |
| ADR-009~012 OQs unresolved | F7/F6 OQs had no decision | CLOSED | K4-α: spec-pack PR#38 merged |

## Residual Gaps (3 remaining)

### Gap 1: Firmware Issue #88 — 3 Sub-Tasks Unresolved

`.clang-format` adoption decision, 30+ function-length violations (≥40L per
structural budget), and `docs/archive/` dead-link root-cure remain OPEN.

**Why it matters**: C Lint CI paths filter gates on `.clang-format` existence —
adoption off; structural violations accumulate unchecked.
**Action**: Close #88 in sequence: (a) `.clang-format` adoption decision,
(b) enumerate + fix function-length violations per module, (c) archive triage.

### Gap 2 (formerly Gap 3 partial): Trace Reconcile CI Advisory-Only

`tools/check_trace_reconcile.py` exits 0 always. SEQ- divergence between spec-pack
and workspace trace_map is detected and warned but does not block merge. The dual
trace_map structure remains unresolved at the consolidation level.

**Why it matters**: Traceability chain can silently diverge; automation surfaces
the warning but cannot prevent it.
**Action**: Elevate trace reconcile to blocking in spec-pack Ruleset required status
checks, OR consolidate to single SSOT trace_map with workspace referencing spec-pack.

### Gap 3 (formerly Gap 4 partial): Staleness Not Ruleset-Required

K1 promoted scripts to exit 1 on drift for 3 consumer repos (firmware/app/central).
However, the staleness check is not enrolled as a Ruleset `required_status_checks`
entry. A stale mirror can still merge if reviewer approves and vocab-check passes.
Workspace staleness still exits 0 (advisory-only).

**Why it matters**: Mechanical enforcement requires both (a) script exit 1 AND
(b) Ruleset status check required. Currently only (a) is satisfied on 3/4 repos.
**Action**: Add `Spec staleness check` to Ruleset required_status_checks for
firmware/app/central; upgrade workspace script to exit 1.
