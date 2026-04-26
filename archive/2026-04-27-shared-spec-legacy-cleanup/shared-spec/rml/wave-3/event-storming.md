# Event Storming — Wave 3: Verification + Convergence

> Wave: Firmware Phase 3 Wave 3
> Source: `firmware-phase3-reliability.md` Wave 3, `phase3-verification-checklist.md`

## Domain Events

| Event | Trigger | Actor | Outcome |
|---|---|---|---|
| `NormalRebootOccurred` | `sys_reboot()` | GW firmware | `reset_count` +1 in NVS |
| `WatchdogResetOccurred` | watchdog timeout | GW firmware | `reset_count` +1 expected |
| `PowerCycleOccurred` | USB power removed/restored | Physical DK | `reset_count` +1 expected |
| `BrownoutOccurred` | USB flash / unstable power | Physical DK | `reset_count` +1 or unchanged (under investigation) |
| `BootIdVerified` | 4 real-device scenarios confirmed | Firmware + HIL | Task 3.9 DoD met |
| `E2EPathVerified` | FW → UART → Central parser roundtrip | Firmware + Central | Task 3.10 DoD met |
| `Phase3GatePassed` | R1–R6 + 83 tests + boot_id + E2E all confirmed | All actors | Wave 3 complete, Phase 4 unblocked |

## Commands (Verification)

| Command | Actor | Effect |
|---|---|---|
| `bash scripts/dev.sh build --gw` | Engineer | Build GW firmware for HIL |
| `bash scripts/dev.sh flash` | Engineer | Flash DK for real-device test |
| `bash scripts/dev.sh log` | Engineer | RTT streaming to observe boot_id |
| `docker run ... bash scripts/run_unit_tests.sh` | CI | Run 83+ unit tests |
| `nrfjprog --reset` / power-cycle | Engineer | Trigger reset scenarios |

## Verification Matrix

| Scenario | Expected boot_id | Verified |
|---|---|---|
| Normal reboot (`sys_reboot()`) | +1 | Task 3.9 |
| Watchdog reset | +1 | Task 3.9 |
| Power cycle (USB remove/restore) | +1 | Task 3.9 |
| Brownout (USB flash) | +1 or unchanged | Task 3.9 (open) |

## Aggregates

| Aggregate | State | Role in Wave 3 |
|---|---|---|
| `reset_count` (NVS `qos/rst_cnt`) | `uint16_t` | boot_id source; verified across all 4 reset scenarios |
| Unit test suite | 83+ assertions | CI gate; must all pass before Phase 4 |
| E2E verification path | 1 confirmed path | Cross-repo Central + Firmware alignment |
