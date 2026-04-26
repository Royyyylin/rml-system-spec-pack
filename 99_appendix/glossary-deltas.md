# Glossary Deltas

> arc42 §12 — Chronological log of vocabulary changes across all 4 repos.
> Canonical vocabulary SSOT: [ubiquitous-language.md](../01_context-scope/ubiquitous-language.md)
> Owner: spec-pack. Last updated: 2026-04-26.

---

## Purpose

This file records cross-repo vocabulary changes, renames, and classification rule additions in
chronological order. It is NOT the canonical vocabulary — use
[ubiquitous-language.md](../01_context-scope/ubiquitous-language.md) for current definitions.

---

## Changelog

### 2026-04-25 — `glossary.md` renamed to `ubiquitous-language.md` (PR#3)

- **Change type**: RENAME + RELOCATE
- **From**: `glossary.md` (legacy filename, located in the old chapter-less directory — now migrated)
- **To**: `01_context-scope/ubiquitous-language.md` (arc42 §3 canonical location)
- **Rationale**: Aligns with arc42 §3 (Context and Scope), DDD Ubiquitous Language pattern, and
  spec-pack directory convention (`NN_<chapter>/`). The old name "glossary" implied a static
  dictionary; "ubiquitous-language" signals the DDD intent of shared, enforced vocabulary.
- **Consumer impact**: Any external doc or CI script referencing the old `glossary.md`
  filename must update to `01_context-scope/ubiquitous-language.md`. CLAUDE.md Vocabulary Canonical List
  now maps `glossary.md → ubiquitous-language.md` as a session-level guard.
- **Cross-link**: [ubiquitous-language.md](../01_context-scope/ubiquitous-language.md) — header
  notes `renamed from: glossary.md (git mv to arc42 location, PR#3)`.

---

### 2026-04-26 — Added `mac`, `syncState`, `connectionState` (PR#33)

- **Change type**: ADD (3 new terms)
- **Terms added** (canonical forms):

| Term | Section in ubiquitous-language.md | Notes |
|---|---|---|
| `mac` | BLE 協定詞彙 | BLE hardware MAC address; NOT stable identity (may be randomized) |
| `syncState` | 身份識別詞彙 | Generic sync-state umbrella term; domain-specific `assignmentSyncState` takes precedence |
| `connectionState` | BLE 協定詞彙 | App BLE lifecycle state machine (IDLE / CONNECTING / CONNECTED / DISCONNECTING) |

- **Rationale**: Cross-repo discussions used these terms informally; adding them to
  [ubiquitous-language.md](../01_context-scope/ubiquitous-language.md) establishes canonical
  casing (camelCase / snake_case) and owner-repo attribution.
- **Consumer impact**: App team must use `connectionState` (not `bleState` or `connState`);
  firmware team must treat `mac` as non-stable identifier only.

---

### 2026-04-26 — F-NN vs FEA-NNN Classification Rule codified (CLAUDE.md update)

- **Change type**: ADD (classification rule, not a new term)
- **Rule summary**:
  - `FEA-NNN` (default): cross-repo feature, App-led / Central-led / 4-owner equal
  - `F-NN` (firmware-led): firmware runtime behavior is the primary concern
  - Decision gate: firmware-initiated AND firmware runtime primary → `F-NN`; everything else → `FEA-NNN`
- **Canonical examples**: `FEA-001` telemetry, `FEA-002` cmd feedback, `FEA-003` identity,
  `FEA-004` reconciliation; `F-04` GW QoS scheduler tuning.
- **Deprecated patterns (forbidden)**: `RML-FEA-*`, bare `S-N`, bare `X-N`
- **Recorded in**: CLAUDE.md Vocabulary Canonical List + `01_context-scope/ubiquitous-language.md`
  Spec ID 命名規範 section.
- **Cross-link**: [ubiquitous-language.md §Spec ID 命名規範](../01_context-scope/ubiquitous-language.md)

---

## Future Deltas (Placeholder)

New vocabulary changes must be appended here in chronological order with the format:

```
### YYYY-MM-DD — <short description> (PR#NN or commit hash)

- **Change type**: ADD / RENAME / DEPRECATE / REMOVE
- **Terms affected**: ...
- **Rationale**: ...
- **Consumer impact**: ...
- **Cross-link**: [ubiquitous-language.md](../01_context-scope/ubiquitous-language.md)
```

Planned future entries:
- Assignment domain terms (FEA-004 reconciliation state machine finalization)
- Telemetry field canonical names (FEA-001 profiling architecture, after spec freeze)

---

*See also: [risks-and-debt.md](risks-and-debt.md) (RISK-006 rename propagation risk) | [ubiquitous-language.md](../01_context-scope/ubiquitous-language.md)*
