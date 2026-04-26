@../AGENTS.md

@01_context-scope/ubiquitous-language.md

## Vocabulary Canonical List

> Spec Hygiene Rule 13: AI sessions MUST use canonical terms below.
> New terms must be registered in `01_context-scope/ubiquitous-language.md` before use.

| Deprecated | Canonical | Notes |
|---|---|---|
| `shared-spec/` prefix paths | `NN_<chapter>/<file>` | Use arc42 chapter path (legacy dir migrated PR#3) |
| `RML-FEA-*` | `FEA-NNN-` | FEA-NNN mandatory, non-archive contexts |
| `S-N` | `F-NN` or `FEA-NNN` | Use feature ID prefix |
| `X-N` | chapter-scoped ID (e.g. `x1-`) | Use chapter-scoped naming |
| `glossary.md` | `01_context-scope/ubiquitous-language.md` | DDD canonical vocabulary |
| `rml-lite.md` | `00_introduction-goals/system-intent.md` | System intent SSOT |
| `capability-ownership.md` | `02_solution-strategy/capability-map.md` | TOGAF capability map |
| `s1-ac-catalog.md` | `05_quality-acceptance/ac-catalog.md` | AC catalog |
| `s2-tc-matrix.md` | `05_quality-acceptance/tc-matrix.md` | TC matrix |
| `s3-cross-repo-trace-strategy.md` | `06_crosscutting-integration/cross-repo-trace-strategy.md` | Trace strategy |

## F-NN vs FEA-NNN Classification Rule

- **`FEA-NNN`** (default): cross-repo feature, App-led / Central-led / 4-owner equal.
  Examples: FEA-001 telemetry, FEA-002 cmd feedback, FEA-003 identity, FEA-004 reconciliation.
- **`F-NN`** (firmware-led): firmware runtime behavior is primary concern.
  Examples: F-04 GW QoS scheduler tuning.
- Rule: firmware-initiated AND firmware runtime behavior primary → use `F-NN`.
  Everything else (cross-repo / App-led / Central-led) → use `FEA-NNN`.

## Fractal Split Rule

Apply fractal split (`<feature>/{INDEX.md, ...}`) when EITHER:
- Feature has >= 3 sub-artifacts (spec + contract + states + ...), OR
- Feature contains a state diagram

Examples: `FEA-004-assignment-reconciliation/` (contract + context.d2 + states.d2),
`F-04-gw-qos-scheduler-tuning/` (tuning + extension-boundary).
