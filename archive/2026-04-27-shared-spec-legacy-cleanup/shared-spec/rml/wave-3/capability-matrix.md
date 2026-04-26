# Capability Matrix — Wave 3: Verification + Convergence

> Wave: Firmware Phase 3 Wave 3
> Source: `phase3-verification-checklist.md`, `firmware-phase3-reliability.md` Wave 3

## Per-Role Capabilities

| Capability | GW Firmware | Central | Verification Harness |
|---|---|---|---|
| boot_id brownout real-device test | **OWNS** — 4 reset scenarios on real DK | — | HIL test runner |
| `reset_count` NVS increment verification | **OWNS** — NVS `qos/rst_cnt` | — | RTT log reader |
| P0 wire byte E2E decode | produces | **OWNS** — parser decode verify | unit test golden vector |
| P1 wire byte E2E decode | produces | **OWNS** — parser decode verify | unit test golden vector |
| `ed_id` derivation from P1 `ed_mac[6]` | produces | **OWNS** — `ed:{mac}` format | cross-repo verify |
| boot_id + msg_seq dedup key verify | produces | **OWNS** — dedup contract | E2E path test |
| Class A replay dedup (no double-count) | replays | **OWNS** — idempotent dedup | — |
| 28-test unit suite pass | firmware builds | — | CI runner |
| 6 invariant checkpoints | firmware runtime | — | checklist gate |

## Wave 3 Gate Criteria

| Gate | Owner | Status Reference |
|---|---|---|
| All 83+ unit tests pass | Firmware + CI | `phase3-verification-checklist.md` |
| boot_id all 4 reset scenarios resolved | Firmware real-device | Task 3.9 DoD |
| At least 1 E2E path (FW → UART → Central parser) verified | Central + Firmware | Task 3.10 DoD |
| R1–R6 minimum reliability criteria met | Firmware | `firmware-phase3-reliability.md` §Minimum Reliability Criteria |
