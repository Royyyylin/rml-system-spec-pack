# Risks and Technical Debt

> arc42 §11 — Risk register and known technical debt.
> Owner: spec-pack. Last updated: 2026-04-26.

---

## Risk Register

Each entry has 5 dimensions: likelihood / impact / mitigation / owner / status.

---

### RISK-001 — Tech Debt: Phase K Issue (firmware #88)

| Dimension | Value |
|---|---|
| **Likelihood** | med |
| **Impact** | high — unresolved firmware issue may block FW-3B / F-04 acceptance gate |
| **Mitigation** | Track firmware issue #88 in firmware repo; block impl merge until closed; add AC in `05_quality-acceptance/ac-catalog.md` referencing issue #88 |
| **Owner** | firmware repo maintainer |
| **Status** | open — blocked until firmware issue resolved |

**Risk description**: Phase K (FW-3A CMD_V2 length guard) has an open issue (#88) in the firmware repo. Failure to close this before Phase 3B merge creates a spec-to-impl divergence, invalidating the AC-catalog entries for FW-3A.

---

### RISK-002 — Vocabulary Drift (vocab-check ruleset gap)

| Dimension | Value |
|---|---|
| **Likelihood** | med |
| **Impact** | high — deprecated terms (`RML-FEA-*`, `S-N`, `X-N`) leaking into spec files create cross-repo confusion and break traceability |
| **Mitigation** | vocab-check CI ruleset enforces canonical terms mechanically; `CLAUDE.md` Vocabulary Canonical List provides a session-level guard; run `grep -r "RML-FEA-\|S-[0-9]\|X-[0-9]" .` periodically as sanity check |
| **Owner** | spec-pack maintainer (vocab-check CI) |
| **Status** | partially mitigated — vocab-check CI deployed; human review still required for semantic drift not caught by regex |

**Risk description**: As spec evolves, authors may use deprecated ID formats or renamed files (e.g. `glossary.md` instead of `ubiquitous-language.md`). Mechanical enforcement reduces but does not eliminate risk.

---

### RISK-003 — Spec Authority Enforcement Gap

| Dimension | Value |
|---|---|
| **Likelihood** | low |
| **Impact** | high — if impl repos make wire-semantic changes without updating spec-pack, SSOT drifts silently |
| **Mitigation** | ADR-000 establishes prescriptive spec authority model; cross-repo cascade check referenced in `06_crosscutting-integration/cross-repo-trace-strategy.md`; CONSUMER_IMPACT gate in PR template |
| **Owner** | spec-pack maintainer + repo tech leads |
| **Status** | mitigated by process — no tooling auto-block yet; manual gate enforced in PR description |

**Risk description**: Wire semantics must flow from `ble_api.yaml` → spec-pack → impl repos. A direct firmware change to `ble_api.yaml` without corresponding spec-pack PR breaks the authority chain defined in ADR-000.

---

### RISK-004 — Cross-Repo Sync Friction

| Dimension | Value |
|---|---|
| **Likelihood** | high |
| **Impact** | med — parallel PRs across 4 repos risk merge conflicts in shared vocabulary and trace-map entries |
| **Mitigation** | Spec-pack merge gates (Phase 2a → 2b → 3 order enforced by master gate); `06_crosscutting-integration/cross-repo-trace-strategy.md` defines sync protocol; sub-plan F11-12 (this document) is an ADD-only operation to minimize conflict surface |
| **Owner** | master gate reviewer (Roy) |
| **Status** | active risk — managed by serialized merge order; each sub-plan branch is ADD-only where possible |

**Risk description**: 4 repos with overlapping vocabulary and shared trace identifiers (FEA-NNN, F-NN) create a high-frequency merge conflict surface. Parallel feature work without coordinated spec-pack updates amplifies this risk.

---

### RISK-005 — NCS SDK Upgrade Risk

| Dimension | Value |
|---|---|
| **Likelihood** | low |
| **Impact** | high — NCS API surface changes (BLE stack, Zephyr scheduler) may invalidate F-04 tuning presets and FW-3A length guard assumptions |
| **Mitigation** | Pin NCS version in `scripts/dev.sh` (see `ubiquitous-language.md` → NCS Version SSOT section); upgrade only on explicit milestone; run full DTM + HIL suite post-upgrade before updating spec references |
| **Owner** | firmware repo maintainer |
| **Status** | low urgency — current pin is stable; risk activates on any NCS upgrade decision |

**Risk description**: All firmware spec ACs assume current NCS SDK version. SDK upgrade changes scheduler semantics, BLE stack timing, or GATT API surface may require re-validation of FW-3A, FW-3B, and F-04 presets.

---

### RISK-006 — Glossary / Ubiquitous Language Rename Incomplete Propagation

| Dimension | Value |
|---|---|
| **Likelihood** | med |
| **Impact** | med — stale references to `glossary.md` in cross-repo docs or CI scripts cause 404s and confusion |
| **Mitigation** | `CLAUDE.md` Vocabulary Canonical List maps `glossary.md → ubiquitous-language.md`; grep-based audit in vocab-check; `glossary-deltas.md` (this repo) records the rename event for traceability |
| **Owner** | spec-pack maintainer |
| **Status** | partially mitigated — rename completed PR#3; residual risk in external docs and wiki links not yet audited |

**Risk description**: `glossary.md` was renamed to `01_context-scope/ubiquitous-language.md` in PR#3. Any external documentation, bookmark, or CI script referencing the old path breaks silently.

---

### GATT-Contract-Drift — GATT Contract Drift (Migrated from system-intent.md C1)

| Dimension | Value |
|---|---|
| **Likelihood** | med |
| **Impact** | high — GATT UUID / opcode / packet format divergence between `ble_api.yaml` and impl repos causes silent wire-semantic breakage |
| **Mitigation** | `ble_api.yaml` is SSOT; any wire-semantic change must backpropagate to packet spec / sequence diagrams / AC / TC in spec-pack; codegen pipeline enforces derivation; CI vocab-check blocks undeclared opcodes |
| **Owner** | firmware repo maintainer (ble_api.yaml) + spec-pack maintainer (cascade) |
| **Status** | Migrated from system-intent.md C1 |

**Risk description**: If firmware, app, or central independently evolve their interpretation of GATT UUIDs, wire formats, or opcodes without updating `ble_api.yaml` first, the shared wire contract drifts. Recovery requires coordinated re-sync across all 4 repos.

---

### Identity-Drift — Identity Layer Confusion (Migrated from system-intent.md C1)

| Dimension | Value |
|---|---|
| **Likelihood** | med |
| **Impact** | high — mixing `stableId` / `central_ref` / MAC causes incorrect device matching, phantom roster entries, and unrecoverable identity collisions |
| **Mitigation** | Three-layer separation enforced in `ubiquitous-language.md`; App UI must label MAC as transport identity; Central owns `stableId` assignment; `identity-boundary-rules.md` codifies non-confusion rules |
| **Owner** | central-device-metadata (stableId authority) + ble_qos_app (UI labeling) |
| **Status** | Migrated from system-intent.md C1 |

**Risk description**: The system maintains three distinct identity layers: App `stableId`, Central `central_ref`, and BLE MAC (transport). Collapsing any two layers — especially presenting MAC as a stable device identity — breaks cross-session traceability and Central reconciliation.

---

### Authority-Runtime-Mismatch — Central Authority vs Runtime Inconsistency (Migrated from system-intent.md C1)

| Dimension | Value |
|---|---|
| **Likelihood** | med |
| **Impact** | high — if Central assignment authority diverges from firmware runtime attach state, UI shows contradictory gateway ownership without a resolution path |
| **Mitigation** | App must show dual-source gateway display + `assignmentSyncState` reconciliation badge; `FEA-004` defines the reconciliation flow; `can_compare` gate guards conflict derivation |
| **Owner** | ble_qos_app (UI reconciliation) + central-device-metadata (assignment authority) |
| **Status** | Migrated from system-intent.md C1 |

**Risk description**: Central assigns devices to gateways authoritatively. Firmware runtime may attach differently (e.g. after failover or power cycle). When these diverge, the UI must surface the mismatch rather than silently presenting either source as definitive.

---

### Command-Timeout-Or-Error — CMD_V2 Transaction Failure Recovery (Migrated from system-intent.md C1)

| Dimension | Value |
|---|---|
| **Likelihood** | med |
| **Impact** | med — unrecovered command transactions leave the system in an ambiguous state; user sees no feedback and may retry blindly |
| **Mitigation** | App must model retryable / failed states explicitly; transaction record + evidence must be preserved for audit; CMD_V2_TIMEOUT_MS enforced; UI must show observable state for success / failure / timeout / retry |
| **Owner** | ble_qos_app (state machine) + firmware (CMD_RESULT characteristic) |
| **Status** | Migrated from system-intent.md C1 |

**Risk description**: BLE command execution via `CMD_V2` / `CMD_RESULT` is inherently unreliable at the transport layer. Without explicit retry/failure state modeling in the App, timeouts silently swallow user intent and the device state becomes unobservable.

---

### Project-Vs-Repo-Truth-Mixing — Project-Level vs Repo-Level Truth Confusion (Migrated from system-intent.md C1)

| Dimension | Value |
|---|---|
| **Likelihood** | low |
| **Impact** | high — conflating cross-repo orchestration truth (base-dir) with per-repo technical truth (each repo SSOT) causes authority boundary violations and spec drift |
| **Mitigation** | `Base-Dir-Cross-Repo-Only` invariant enforced: `--base-dir` carries only cross-repo formal control docs; per-repo technical truth (firmware `ble_api.yaml`, Central schema, App models) stays in each repo SSOT; `capability-map.md` codifies ownership |
| **Owner** | spec-pack maintainer + all repo tech leads |
| **Status** | Migrated from system-intent.md C1 |

**Risk description**: The conductor/orchestration layer manages planning and cross-repo governance via `--base-dir`. Allowing implementation truth (wire semantics, DB schemas, App models) to live in base-dir instead of the owning repo breaks the repo-as-authority model defined in ADR-000.

---

### AI-Orchestration-Authority-Overreach — AI Conductor Acting as Domain Authority (Migrated from system-intent.md C1)

| Dimension | Value |
|---|---|
| **Likelihood** | med |
| **Impact** | high — if Conductor directly controls Central assignment, firmware flashing, or App state without going through repo authority owners, cross-repo governance collapses |
| **Mitigation** | `AI-Orchestration-Non-Authority` invariant: Conductor role is planning / delegation / acceptance / handoff only; direct control loops (e.g. auto-assigning gateways, auto-pushing firmware) are prohibited; authority-map.yaml encodes the prohibition |
| **Owner** | spec-pack maintainer (governance) + Roy (orchestration operator) |
| **Status** | Migrated from system-intent.md C1 |

**Risk description**: AI orchestration layers (Conductor, sub-agents) have broad write access to spec and can issue commands across repos. Without a hard boundary that keeps Conductor in planning/governance and out of domain authority, it can silently take over decisions that belong to Central, Firmware, or App owners.

---

## Known Technical Debt

| Debt Item | Severity | Target Resolution |
|---|---|---|
| firmware issue #88 (Phase K) | high | before FW-3B impl merge |
| vocab-check: regex-only, no semantic check | med | Phase 3 — add NLP-based drift detector |
| CONSUMER_IMPACT gate: manual only, no tooling block | med | Phase 3 — auto-block PR if `ble_api.yaml` changed without spec-pack update |
| `decisions/` ADR-001 through ADR-007 stubs not written | low | deferred per ADR-008 |
| NCS SDK version not pinned in CI matrix | low | add `west.yml` SDK pin to CI on next firmware milestone |

---

*See also: [ADR-000](decisions/ADR-000-spec-authority-model.md) (spec authority model) | [ubiquitous-language.md](../01_context-scope/ubiquitous-language.md) (canonical vocabulary)*
