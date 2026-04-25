# Feature Design Guide

How to design a new cross-repo feature — 7 steps.

Reference examples: FEA-001~004, F-04.

---

## Step 1: Bounded Context

Which bounded context owns this feature?

- **Firmware BC**: runtime QoS, radio, device-side recovery → use `F-NN` prefix
- **App BC**: human-facing interaction, presentation → feature likely `FEA-NNN` (App-led)
- **Central BC**: canonical identity, assignment, metadata → feature likely `FEA-NNN` (Central-led)
- **Cross-BC**: 3+ repo owners → use `FEA-NNN` prefix

Register the bounded context in `01_context-scope/bounded-context-map.md`.

## Step 2: Authority

Which repo is canonical for this feature's contract?

Check `01_context-scope/authority-map.yaml` (machine-readable boundary).
Check `02_solution-strategy/capability-map.md` (TOGAF capability ownership).

A feature may have ONE canonical authority repo even if multiple repos consume it.

## Step 3: Contract Surface

What is the wire/API contract?

- **BLE wire** (GATT opcodes, characteristics): defined in `ble_qos_demo_V1.2m/ble_api.yaml`
- **HTTP API** (Central endpoints): defined in `central-device-metadata/` OpenAPI
- **App events / state**: defined in `app-spec/`
- **Feature spec**: create `03_building-blocks/FEA-NNN-<name>/contract.md` or flat `.md`

Apply fractal split (subdirectory) if >= 3 sub-artifacts or contains state diagram.

## Step 4: Acceptance Criteria

Write Gherkin scenarios in `05_quality-acceptance/ac-catalog.md`.

Format:
```
AC-NNN: <title>
Feature: FEA-NNN or F-NN
Given / When / Then
```

## Step 5: Test Cases

Add TC entries to `05_quality-acceptance/tc-matrix.md`.

Each TC must reference: acceptance criterion, requirement, evidence type.

## Step 6: Trace Map Entry

Add feature entry to `trace/trace_map.yaml`:

```yaml
FEA-NNN:
  spec: 03_building-blocks/FEA-NNN-<name>/contract.md
  diagram_sources: [03_building-blocks/FEA-NNN-<name>/<name>.d2]
  requirements: [REQ-NNN]
```

## Step 7: Propagate to Consumer Repos

1. Open PRs in each consumer repo to update CLAUDE.md `@import` paths if vocabulary changed
2. Run `python3 tools/check_vocabulary_alignment.py` — must exit 0
3. Reference `06_crosscutting-integration/cross-repo-trace-strategy.md` for trace propagation rules

New term? Register in `01_context-scope/ubiquitous-language.md` BEFORE using cross-repo.
