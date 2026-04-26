---
title: "Task A — Phase K Hand-Off Next Steps"
date: 2026-04-26
---

## Phase K Action List (priority order)

| Priority | Action | Repo | Blocks |
|---|---|---|---|
| 1 | Merge ADR-008 PR #29 | spec-pack | Gap 2 |
| 2 | Close firmware #88 sub-task (a): adopt `.clang-format` | firmware | Gap 1 |
| 3 | Close firmware #88 sub-task (b): fix 30+ function-length violations | firmware | Gap 1 |
| 4 | Close firmware #88 sub-task (c): `docs/archive/` triage | firmware | Gap 1 |
| 5 | Resolve dual trace_map ownership ADR | spec-pack + workspace | Gap 3 |
| 6 | Promote staleness check to blocking Ruleset (firmware + central) | firmware, central | Gap 4 |
| 7 | Add staleness check to workspace repo | workspace | Gap 4 |
| 8 | Create GitHub Rulesets for firmware/app/central | firmware, app, central | Gap 5 |
| 9 | Close V-Model OQs (app + central) before IMPL FREEZE lift | app, central | Gap 6 |
| 10 | Add `01_context-scope/constraints.md` (arc42 §2) | spec-pack | Gap 7 |

## Lessons from Task A

1. **Sub-plan atomicity works**: each PR was small, reviewable, and independently
   mergeable. No rollbacks required across 16 sub-plan rows.
2. **Adversarial auditing finds gaps missed by self-Verifier**: admin bypass path,
   advisory-only staleness, workspace missing governance — all missed in prior reviews.
3. **Dual trace_map sources create invisible divergence**: single SSOT is preferred;
   enforce via CI rather than convention.
4. **V-model OQ sections must be populated**: empty sections give false completion signal.
5. **Ruleset scope must match governance intent**: deploying to one repo while 3 others
   remain unprotected leaves the enforcement chain incomplete.

## Environment Notes

- Local spec-pack: `/Users/create94520/Projects/ble_qos_demo/rml-system-spec-pack`
- Firmware: `/Users/create94520/Projects/ble_qos_demo/ble_qos_demo_V1.2m`
  - Remote: `git@github.com:Royyyylin/ble_qos_demo_V1.2m-openclaw.git`
- App: `/Users/create94520/Projects/ble_qos_demo/ble_qos_app`
  - Remote: `git@github.com:Royyyylin/ble_qos_app-openclaw.git`
- Central: `/Users/create94520/Projects/ble_qos_demo/central-device-metadata`
  - Remote: `git@github.com:Royyyylin/central-device-metadata-openclaw.git`
- Workspace: `/Users/create94520/Projects/ble_qos_demo/--base-dir`
  - Remote: `git@github.com:Royyyylin/ble-qos-demo-workspace.git`
- ADR-008 PR #29: https://github.com/Royyyylin/rml-system-spec-pack/pull/29 (OPEN)
- Enforcement Ruleset: id=15563210 on rml-system-spec-pack (spec-pack only)
- Phase J worktree: `docs/handoff-task-a-final` branch
