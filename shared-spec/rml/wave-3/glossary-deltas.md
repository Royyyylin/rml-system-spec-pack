# Glossary Deltas — Wave 3: Verification + Convergence

> Cross-links master glossary: `01_context-scope/ubiquitous-language.md`
> New terms introduced in Firmware Phase 3 Wave 3.

## New Terms

| Term | Definition | Canonical Location |
|---|---|---|
| `boot_id` brownout scenario | Power instability (USB flash) causing uncertain `reset_count` increment. Status under investigation in Wave 3 Task 3.9. | `firmware-phase3-reliability.md` Task 3.9 |
| `reset_count` | NVS key `qos/rst_cnt`: `uint16_t` monotonically incremented on each reboot. Used as `boot_id` source. | `src/` (NVS key), `firmware-phase3-reliability.md` |
| `HIL (Hardware-in-Loop)` | Testing methodology using real nRF52833 DK hardware; required for reset scenario verification. | `hil-test-plan.md` |
| `golden vector test` | Unit test asserting exact byte output from dispatch functions matches a pre-recorded hex snapshot. | `phase3-verification-checklist.md` |
| `spec sync` | Process of aligning `dispatch-wire-contract.md` specification with actual firmware implementation output. | Wave 3 Task 3.10 |
| `E2E path (firmware → Central)` | End-to-end verify chain: GW firmware produces P0/P1 frame → UART transport → Central Ingest parser decodes → `ed_id` derivation correct. | `firmware-phase3-reliability.md` Task 3.10 |
| `Phase 4` | Next firmware implementation phase (wire finalization + E2E readiness); unblocked by Wave 3 completion gate. | `docs/plans/archive/current-wave.md` |

## Existing Terms Referenced

- `R1–R6` — minimum reliability criteria; see `firmware-phase3-reliability.md`
- `boot_id` = `reset_count`; see `glossary.md`
- `dedup key` = `(gw_mac, boot_id, msg_seq)`; see `glossary.md`
