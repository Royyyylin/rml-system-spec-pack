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
