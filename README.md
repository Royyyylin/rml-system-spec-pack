# System Spec Pack

Cross-repo system SSOT for the BLE QoS 4-repo workspace (firmware / app / central / spec-pack).
Structure: arc42 selective + DDD element naming.

> Naming note: "RML" in the repo name is a legacy label. Content uses DDD/arc42 industry terminology.

## arc42 Chapter Map

| Chapter | arc42 | Contents |
|---|---|---|
| `00_introduction-goals/` | §1+§2 | System intent, goals, constraints, risks, stakeholders |
| `01_context-scope/` | §3 | Bounded context map, system actors, ubiquitous language (DDD) |
| `02_solution-strategy/` | §4 | Capability map (TOGAF), SDLC pipeline |
| `03_building-blocks/` | §5 | FEA-001~004 feature contracts + F-04 (firmware-led) |
| `04_runtime-view/` | §6 | 6 sequence diagrams (CMD_V2, cache, HA, reconnect) |
| `05_quality-acceptance/` | §10 | Requirements, AC catalog, TC matrix, BDD scenarios |
| `06_crosscutting-integration/` | §8 | Cross-repo trace strategy, wire parity, compliance matrix |
| `99_appendix/` | §9+§11 | ADRs (decisions/), glossary deltas, risks and debt |

## Use-Case Entry Points

### (a) New engineer — sequential reading

`00_introduction-goals/system-intent.md` → `01_context-scope/ubiquitous-language.md`
→ `02_solution-strategy/capability-map.md` → `03_building-blocks/` → `05_quality-acceptance/`

### (b) AI session — cross-repo impact

Jump to `06_crosscutting-integration/cross-repo-trace-strategy.md`
then `trace/trace_map.yaml` for machine-readable feature-to-artifact mapping.

### (c) Compliance audit

`05_quality-acceptance/` (AC catalog + TC matrix + BDD scenarios)
+ `06_crosscutting-integration/market-compliance-matrix.md`
+ `06_crosscutting-integration/x1-wire-parity-spec.md`

### (d) Dispute resolution (who owns what)

`03_building-blocks/FEA-NNN-*/` or `03_building-blocks/F-04-*/` per feature
+ `02_solution-strategy/capability-map.md` (TOGAF capability ownership)
+ `01_context-scope/authority-map.yaml` (machine-readable boundary)

## Feature ID Classification

| Prefix | Meaning | Examples |
|---|---|---|
| `FEA-NNN` | Cross-repo feature (App-led / Central-led / 4-owner) | FEA-001~004 |
| `F-NN` | Firmware-led feature (firmware runtime behavior primary) | F-04 |

## Modification Order

1. `00_introduction-goals/system-intent.md` (upstream intent)
2. `05_quality-acceptance/requirements.md`
3. Arc42 chapter docs + diagram sources (`.d2` / `.mmd`)
4. `trace/trace_map.yaml` + `trace/change_rules.md`
5. `05_quality-acceptance/ac-catalog.md` + `tc-matrix.md`
6. `trace/impact-summary.md`

## Rules

- Repo SSOT wins over spec-pack if conflict
- All `.d2` / `.mmd` sources must carry `AI Diagram Contract` comment block
- `renders/` are derived artifacts — do not edit directly
- The legacy `shared-spec` directory (content migrated to arc42 chapters, PR#3); navigate via chapter paths above
