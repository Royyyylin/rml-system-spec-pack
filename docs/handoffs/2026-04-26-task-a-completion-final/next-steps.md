---
title: "Task A — Post-Phase K Next Steps"
date: 2026-04-26
---

## Phase K Closure Statement

Phase K (Foundation Review) is COMPLETE. All 9 K sub-deliverables verified on
origin/main. Score: 96/100 (threshold 95). Master signal: PASS.

## Remaining Backlog (priority order)

| Priority | Action | Repo | Addresses |
|---|---|---|---|
| 1 | Enroll staleness check as Ruleset required_status_checks on firmware/app/central | firmware, app, central | Gap 3 |
| 2 | Upgrade workspace staleness script to exit 1 on drift | workspace | Gap 3 |
| 3 | Elevate trace reconcile CI to blocking OR consolidate trace_map SSOT | spec-pack + workspace | Gap 2 |
| 4 | Firmware Issue #88 (a): `.clang-format` adoption decision | firmware | Gap 1 |
| 5 | Firmware Issue #88 (b): fix 30+ function-length violations | firmware | Gap 1 |
| 6 | Firmware Issue #88 (c): `docs/archive/` dead-link triage | firmware | Gap 1 |

## Pre-existing Baseline (out of scope)

These were NOT in Task A scope and remain as separate tracks:
- FEA-001~004 IMPL FREEZE lift (blocked on OQ resolution — OQs now have owners)
- FW-3B-5 / W26A.1 impl (frozen per spec-only mandate)
- NCC / FCC / BLE SIG certification testing

## Key Lessons (Phase K additions)

1. **Ruleset bypass_actors=[] is the correct admin bypass fix** — prior gap was
   legacy branch protection `enforce_admins=false`; Rulesets bypass none by default.
2. **Exit 1 ≠ Ruleset required** — script enforcement and Ruleset enforcement are
   two independent layers; both are needed for true mechanical blocking.
3. **ADR OQ resolution (ADR-009~012) closes V-model gates** — 4 OQs that stalled
   V-model sign-off now have canonical decisions on main.
4. **arc42 §2 is a frequently missed chapter** — constraints are often scattered
   across repos; centralizing in spec-pack provides single audit point.

## Environment (unchanged)

- Spec-pack: `/Users/create94520/Projects/ble_qos_demo/rml-system-spec-pack`
- Firmware: `/Users/create94520/Projects/ble_qos_demo/ble_qos_demo_V1.2m`
- App: `/Users/create94520/Projects/ble_qos_demo/ble_qos_app`
- Central: `/Users/create94520/Projects/ble_qos_demo/central-device-metadata`
- Workspace: `/Users/create94520/Projects/ble_qos_demo/--base-dir`
