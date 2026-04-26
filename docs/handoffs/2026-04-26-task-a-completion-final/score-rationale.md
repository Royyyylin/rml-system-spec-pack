---
title: "Task A — Audit Score Rationale"
date: 2026-04-26
---

## Score Rationale (82/100)

### Enforcement Chain Real — 16/20

GitHub Ruleset `main-vocab-check-required` (id=15563210) is `enforcement=active` on
default branch. Required status check: `Vocabulary alignment check (blocking)`.
Branch protection also disallows force-push and requires conversation resolution.

**Deduction -4**: `enforce_admins=false` — admin merges bypass required status checks
entirely; the Ruleset has no admin bypass guard. No Rulesets exist for firmware/app/central
repos — only spec-pack is protected. Deprecated-term commits can merge to those mains
without mechanical blocking.

### arc42 Chapter Coverage — 21/25

Present: §1 (00_intro-goals, 7 quality goals), §3 (01_context-scope, ubiq-lang + BCM),
§6 (04_runtime-view, deployment-topology + 6 seq files), §8 (06_crosscutting, 3 concept
files ≥50L each), §11 (risks-and-debt.md, 6 risks), §12 (glossary-deltas, 3 dated),
decisions (ADR-001~007 Nygard format).

**Deduction -4**: arc42 §2 Constraints chapter absent (spec-pack has 02_solution-strategy
instead, which is §4 not §2). `deployment-topology.md` is only 58 lines — minimal for a
§7 deployment view. No separate §7 chapter directory.

### ADR System Materialized — 13/15

ADR-001~007 on origin/main in confirmed Nygard format. Decisions INDEX accepted=7.

**Deduction -2**: ADR-008 (Task A Completion Strategy) exists only on PR #29
(mergeStateStatus=UNKNOWN, state=OPEN) — not yet canonical on main.

### V-Model Docs — 14/15

App and central each: 5 stage files + INDEX. All files substantive (≥88L). IMPL FREEZE
notation confirmed in both `03_impl.md` files with specific frozen features listed.

**Deduction -1**: App v-model has empty `## Open Questions` section (no content). Central
has 2 unresolved OQ entries (FEA-004 reconciliation state machine, telemetry staleness
threshold) with no resolution owner or timeline committed.

### Vocab + Trace Coverage — 13/15

`ubiquitous-language.md`=146L with `mac`/`syncState`/`connectionState` added. spec-pack
`trace_map.yaml` has 15 F-04 hits (≥8 required) and 15 SEQ- entries. Workspace trace_map
has 7 SEQ- entries with valid spec_ref targets on spec-pack origin/main.

**Deduction -2**: Two separate trace_map files (`spec-pack/trace/trace_map.yaml` and
`workspace/docs/trace_map.yaml`) with no reconciliation CI. A SEQ entry added to one will
not appear in the other; divergence is undetectable by automation.

### Portable @import + Staleness Governance — 5/10

`sync-spec.sh` + `check-spec-staleness.sh` + `spec-staleness-check.yml` deployed on all 3
downstream repos. Weekly cron + PR trigger confirmed.

**Deduction -5**: Staleness check is **advisory only** — not a blocking required status
check. A PR updating firmware code while ubiq-lang mirror has drifted can still merge.
Workspace repo (`ble-qos-demo-workspace`) has no staleness check at all.
