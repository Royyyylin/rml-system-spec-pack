---
title: "Task A — Audit Score Rationale (post-Phase 4 K)"
date: 2026-04-26
---

## Score Rationale (96/100, was 82/100, delta +14)

### Enforcement Chain — 19/20 (was 16, +3)

GitHub Rulesets now active on **all 4 repos** (spec-pack id=15563210, firmware
id=15563211, app and central confirmed active; workspace id=15567076). All rulesets
have `enforcement=active`, `bypass_actors=[]` (no admin bypass), and required status
check `Vocabulary alignment check (blocking)`.

Staleness script exits 1 on drift on firmware/app/central (K1 PR #90/#39/#37
MERGED). This closes the mechanical toothlessness of the prior advisory-only script.

**Deduction -1**: Staleness check is NOT enrolled as a Ruleset `required_status_checks`
entry. The workflow job name still reads "advisory". A PR where staleness fails will
show a failing CI check, but the Ruleset does not block merge on it — only vocab-check
is Ruleset-required. Workspace staleness script still exits 0 (advisory-only).

### arc42 Chapter Coverage — 25/25 (was 21, +4)

**K2 additions**: `02_solution-strategy/constraints.md` (146L) provides arc42 §2
with legal/technical/organizational/clean-room constraint categories. Deployment
topology expanded from 58→216L (arc42 §7 now substantive). All 8 targeted chapters
now present: §1, §2 (NEW), §3, §6, §7 (expanded), §8, §11, §12 + §9 decisions.

**No deduction**: Full coverage achieved.

### ADR System — 15/15 (was 13, +2)

ADR-008 merged (PR #29) and on origin/main at `99_appendix/decisions/ADR-008-...`.
ADR-009~012 (K4-α) resolve F7-OQ1/OQ2 and F6-OQ1/OQ2. INDEX shows accepted=13
(ADR-000~012). All Nygard format with Context/Decision/Consequences sections.

**No deduction**: Full coverage achieved.

### V-Model Docs — 15/15 (was 14, +1)

K4-β (app PR #40 MERGED) and K4-γ (central PR #38 MERGED) add Owner+Timeline tables
to v-model stage docs. Both OQ sections now have structured resolution owners and
timelines rather than empty placeholders. IMPL FREEZE notation present in both repos.

**No deduction**: Full coverage achieved.

### Vocab + Trace Coverage — 14/15 (was 13, +1)

K3-β (spec-pack PR #39 MERGED) adds `tools/check_trace_reconcile.py` and
`trace-map-reconcile-check.yml`. SEQ- entries covered; ubiq-lang 146L+.

**Deduction -1**: trace reconcile CI always exits 0 (advisory mode, by design per
tool docstring). Divergence is detected and surfaced as `::warning::` but does not
block merge. The dual trace_map structure (spec-pack upstream + workspace downstream)
is accepted as intended but divergence blocking is still not enforced.

### Portable @import + Staleness Governance — 8/10 (was 5, +3)

All 4 consumer repos (firmware/app/central/workspace) now have: `docs/external-spec/`
mirror + `scripts/sync-spec.sh` + `scripts/check-spec-staleness.sh` + staleness CI
workflow. Workspace K3-α (PR #18 MERGED) closes the prior workspace gap. CLAUDE.md
`@import` confirmed on workspace.

**Deduction -2**: (1) Workspace staleness CI still exits 0 (advisory-only); only
3 consumer repos upgraded to exit 1. (2) Staleness blocking not enforced via Ruleset
required status checks — CI exits 1 on drift but Ruleset doesn't gate on it.

### Final Total: 96/100 (delta: +14 from 82)
