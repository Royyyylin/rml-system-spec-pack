---
title: "Task A — 25 Sub-Plan Independent Re-Audit (post-Phase 4 K)"
date: 2026-04-26
---

> Verified via `git show origin/main:<path>`, `git ls-tree`, `gh pr view`, `gh api`.
> NO REVIEW.md file read. Independent grep on artifact content.

## Original 16 Sub-Plans

| Sub-plan | PR | Result | Evidence |
|---|---|---|---|
| E firmware symlink rm | #83 | PASS | `shared/` blob gone; INDEX redirect to spec-pack/README.md |
| E firmware portable | #85 | PASS | `docs/external-spec/ubiq-lang.md` 150L + sync-spec.sh + spec-staleness-check.yml |
| E app portable | #37 | PASS | `docs/external-spec/ubiquitous-language.md` 150L + scripts + workflow |
| E central portable | #35 | PASS | Same 4 artifacts confirmed on central origin/main |
| E firmware #86 lint paths | #86 | PASS | `paths:[src/**/*.c, src/**/*.h, .clang-format, ...]` confirmed |
| E firmware #87 mlc-config archive | #87 | PASS | `sections-pre-wave-1/`, 30+ ignorePatterns |
| E firmware #89 authority-map ignore | #89 | PASS | `^authority-map\\.yaml$` in ignorePatterns |
| F1 quality-goals | #31 | PASS | 129L; Goals 1-7; ISO 25010 + FEA-NNN traces |
| F6 crosscutting concepts | #34 | PASS | logging=138L, security=155L, failover=211L; INDEX updated |
| F7 deployment topology | #32 | PASS | md existed; see K2 expansion (now 216L) |
| H-α ubiq + F-04 trace | #33 | PASS | mac/syncState/connectionState rows; F-04 count=15 in trace_map |
| H-β workspace SEQ- | #17 | PASS | 7 SEQ- entries; 04_runtime-view links verified |
| G ADR-001~007 + Evans BCM | #36 | PASS | 7 ADR Nygard format; ACL/OHS/Customer-Supplier/Conformist in BCM |
| F11-12 risks + glossary | #35 | PASS | RISK-001~006 (5-dim); glossary-deltas 3 dated entries |
| Ia app V-Model | #38 | PASS | 5 stages + INDEX + IMPL FREEZE in 03_impl.md |
| Ib central V-Model | #36 | PASS | 5 stages + INDEX + IMPL FREEZE in 03_impl.md |

## Phase K Sub-Plans (9 new rows)

| Sub-plan | PR | Result | Evidence |
|---|---|---|---|
| ADR-008 (PR #29) | spec-pack #29 | PASS | On origin/main `99_appendix/decisions/ADR-008-task-a-completion-strategy.md`; INDEX accepted=13 |
| K1 workspace ruleset | admin | PASS | id=15567076, enforcement=active, bypass_actors=[], required: vocab-check |
| K1 staleness blocking (firmware/app/central) | #90/#39/#37 | PARTIAL | Script exits 1 on drift (MERGED); workflow name still "advisory"; NOT Ruleset required status check |
| K2 arc42 §2 constraints.md | spec-pack #40 | PASS | `02_solution-strategy/constraints.md` 146L on main; 4 constraint categories |
| K2 deployment-topology expand | spec-pack #40 | PASS | `04_runtime-view/deployment-topology.md` 216L (was 58L) |
| K3-α workspace mirror | workspace #18 | PASS | `docs/external-spec/ubiq-lang.md` + scripts/sync-spec.sh + check-spec-staleness.sh; CLAUDE.md @import |
| K3-β trace reconcile CI | spec-pack #39 | PASS | `tools/check_trace_reconcile.py` + `trace-map-reconcile-check.yml` on main; advisory mode |
| K4-α ADR-009~012 | spec-pack #38 | PASS | All 4 on main; INDEX shows accepted=13; resolves F7-OQ1/OQ2 + F6-OQ1/OQ2 |
| K4-β app V-Model OQ | app #40 | PASS | 03_impl.md §7 "Open Questions" with Owner+Timeline table merged |
| K4-γ central V-Model OQ | central #38 | PASS | v-model files have OQ Owner+Timeline (confirmed via gh pr MERGED 2026-04-26) |

All 25 rows: 24 PASS + 1 PARTIAL (K1 staleness not Ruleset-required)
