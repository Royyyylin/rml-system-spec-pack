# Context Map — Wave 3: Verification + Convergence

> Wave: Firmware Phase 3 Wave 3
> Source: `phase3-verification-checklist.md`, `firmware-phase3-reliability.md`

## Bounded Contexts

```mermaid
C4Context
    title Wave 3 Bounded Contexts

    Enterprise_Boundary(fw, "Firmware Domain") {
        System(gw_rt, "GW Runtime", "boot_id NVS, reset_count, P0/P1 output")
    }

    Enterprise_Boundary(central, "Central Domain") {
        System(ingest_parser, "Ingest Parser", "P0/P1 decode, ed_id derivation")
    }

    Enterprise_Boundary(verify, "Verification Domain") {
        System(unit, "Unit Test Suite", "83+ golden vector assertions")
        System(hil, "HIL (Hardware in Loop)", "real DK reset scenario tests")
        System(checklist, "Phase 3 Checklist", "R1–R6 criteria, 6 invariants")
    }

    Rel(gw_rt, ingest_parser, "UART P0/P1 frames (E2E verify)")
    Rel(unit, gw_rt, "golden vector: hexdump diff=0")
    Rel(hil, gw_rt, "4 real-device reset scenarios")
    Rel(checklist, gw_rt, "R1–R6 gate enforcement")
    Rel(checklist, ingest_parser, "Task 3.10 E2E contract alignment")
```

## Context Relationships

| Upstream | Downstream | Relationship | Contract |
|---|---|---|---|
| Firmware Runtime | Central Ingest Parser | Published Language | P0/P1 wire format; `ed:{mac}` identity derivation |
| Unit Test Suite | Firmware | Conformist | golden hex vectors; must match exactly |
| HIL | Firmware | External Test | 4 reset scenarios with RTT log verification |
| Phase 3 Checklist | All | Governance | 28 tests + 6 invariants; gate to Phase 4 |

## Wave 3 Completion Gate

Wave 3 is complete when ALL of the following pass:
1. 83+ unit tests passing in CI docker environment
2. boot_id behavior confirmed for all 4 reset scenarios (real DK)
3. At least 1 E2E path: firmware → UART → Central parser → `ed_id` derivation verified
4. R1–R6 minimum reliability criteria all confirmed
5. `dispatch-wire-contract.md` spec sync complete (no drift between spec and implementation)
