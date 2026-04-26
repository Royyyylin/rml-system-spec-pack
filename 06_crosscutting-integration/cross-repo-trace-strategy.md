# Cross-Repo Trace Strategy

> Status: active
> Last updated: 2026-04-19
> Owner: spec-pack (system level)
> SSOT for trace tooling: `--base-dir/docs/trace_map.yaml`
> Trace coverage script: `--base-dir/tools/check-trace-coverage.py`

## Purpose

Defines the naming convention, semantics, and tooling for cross-repo
REQ → AC → TC → impl traceability. This doc governs how the trace map YAML
(`--base-dir/docs/trace_map.yaml`) is authored and validated.

This doc is a strategy spec only. The live trace data lives in `trace_map.yaml`.
Phase B trace integration sub-agent is responsible for populating missing entries.

## REQ Naming Convention

All requirement IDs use the pattern: `REQ-<DOMAIN>-<FEATURE>-<NNN>`

### Domain Prefix Registry

| Prefix | Domain | Owner Repo | Example |
|---|---|---|---|
| `FW` | Firmware (NCS/Zephyr, C) | `ble_qos_demo_V1.2m` | `REQ-FW-3A-001` |
| `A` | App (Flutter/Dart) | `ble_qos_app` | `REQ-A-1-001` |
| `C` | Central (FastAPI/Python) | `central-device-metadata` | `REQ-C-04-001` |
| `S` | System/Spec-pack contract | `rml-system-spec-pack` | `REQ-S-001` |
| `X` | Cross-repo (multi-owner) | multiple | `REQ-X-001` |
| `LOG` | Logging/Observability | any | `REQ-LOG-001` |

### Feature Segment Convention

The `<FEATURE>` segment uses short alphanumeric codes matching the spec/wave designation:
- Firmware: `3A`, `3B`, `4`, `5` (FW phase codes)
- App: `1`, `2` etc. (App wave codes)
- Central: `04`, `W26A`, `W26D` etc. (Central wave codes)
- System: plain number `001`, `002`

### Sequence Number

`<NNN>` is a 3-digit zero-padded integer. Never reuse a retired ID; mark it `deprecated`.

## AC Naming Convention

All acceptance criteria IDs use the pattern: `AC-<DOMAIN>-<FEATURE>-<NNN>`

- Domain and Feature segments mirror the REQ they trace to.
- One AC maps to exactly one REQ (many ACs per REQ is allowed; many REQs per AC is not).
- AC-APP-* is an exception: uses `APP` for the app-spec RML functional requirements
  that predate the per-feature AC naming scheme.

## TC Naming Convention

All test case IDs use the pattern: `TC-<DOMAIN>-<FEATURE>-<NNN><letter>`

- `<NNN>` matches the REQ serial number.
- `<letter>` (a, b, c...) disambiguates multiple TCs for one AC.
- Example: `TC-FW-3A-001a` = first TC for AC-FW-3A-001 / REQ-FW-3A-001.

## owner_repo and status Semantics

### owner_repo Field

In `trace_map.yaml`, `owner_repo` is the relative directory path from
`/Users/create94520/Projects/ble_qos_demo/`:

| Value | Repo |
|---|---|
| `ble_qos_demo_V1.2m` | Firmware |
| `ble_qos_app` | App |
| `central-device-metadata` | Central |
| `rml-system-spec-pack` | Spec-pack |

The `check-trace-coverage.py` tool uses `owner_repo` to resolve impl file paths
for existence checks.

### status Field (per REQ)

| Value | Meaning |
|---|---|
| `active` | Spec frozen, impl started or done, ACs and TCs defined |
| `pending_impl` | Spec frozen, implementation not yet started |
| `blocked` | Blocked on external dependency (noted in `blocked_by` field) |
| `deprecated` | REQ retired; ID not reused |

### TC status (in TC matrix)

See TC matrix for TC-level status semantics (GREEN / RED / spec_pending / not_implemented / TBD).

## Trace Coverage Formula

**Full chain**: A REQ is "fully traced" when ALL of the following exist:
1. At least one AC (`ac_id`) entry in trace_map.yaml
2. At least one TC (`tc_id`) entry in each AC's `tcs` list
3. At least one impl file (`file`) in the REQ's `impls` list

**Coverage percentage**:

```
coverage = (REQs with full chain) / (total active REQs) * 100
```

Pending_impl REQs are excluded from the denominator (they have no impl yet by definition).
Blocked REQs are included but noted separately.

**Gap categories**:
- AC gap: REQ has no AC entries
- TC gap: AC has no TC entries (`tcs: []` or missing)
- Impl gap: REQ has no impl entries (`impls: []` or missing)

## Tooling

### check-trace-coverage.py

Location: `--base-dir/tools/check-trace-coverage.py`

Reads `--base-dir/docs/trace_map.yaml` and reports:
1. Per-REQ trace status (full / partial / gap)
2. Coverage percentage by repo
3. ACs without TCs (TC gap list)
4. Impl files listed but not present on disk (stale impl references)

Usage:
```bash
python3 --base-dir/tools/check-trace-coverage.py
# or with verbose output:
python3 --base-dir/tools/check-trace-coverage.py --verbose
```

Exit code 0 = all active REQs fully traced. Non-zero = gaps exist (for CI gate).

### Authoring trace_map.yaml

The trace_map.yaml schema version 2.0 structure:

```yaml
schema_version: "2.0"
last_updated: "YYYY-MM-DD"

requirements:
  - req_id: REQ-<DOMAIN>-<FEATURE>-<NNN>
    description: <one-line description>
    spec_ref: <repo-relative path to spec file>
    owner_repo: <repo directory name>
    status: active | pending_impl | blocked | deprecated
    acs:
      - ac_id: AC-<DOMAIN>-<FEATURE>-<NNN>
        description: |
          Given <precondition>
          When <action>
          Then <expected result>
        tcs:
          - tc_id: TC-<DOMAIN>-<FEATURE>-<NNN><letter>
            file: <repo-relative path to test file>
            symbol: <test function name>
    impls:
      - file: <repo-relative path to implementation file>
        symbol: <function or class name>
        generator: <optional: codegen script if generated>
```

### Phase B Trace Integration Responsibility

The trace_map.yaml currently has entries for:
- REQ-FW-3A-001 (partial — AC-FW-3A-001/002 with 2 TCs, AC-FW-3A-003 through 010 missing)
- REQ-F-04-001 (AC-F-04-001/002 with 2 TCs)
- REQ-A-1-001 (ACs defined, no TCs)

Phase B trace integration sub-agent must add:
1. REQ-FW-3A-002 through REQ-FW-3A-007 entries (from FW-3A spec trace map section)
2. REQ-W26A-001, REQ-W26A-002 (central failback command service)
3. REQ-C-04-001 (central C-2 QoS integration)
4. REQ-APP-001 through REQ-APP-008 (app-spec RML requirements)
5. impl file entries for all REQs where impl is done (firmware dispatchers, central services)

## Cross-Repo Dependency Map

```
ble_api.yaml (firmware SSOT)
  ↓ codegen
  ├── ble_qos_demo_V1.2m/src/generated/cmd_v2_dispatch.h
  ├── ble_qos_demo_V1.2m/src/generated/presets.c
  ├── central-device-metadata/app/generated/presets.py
  └── central-device-metadata/app/generated/tune_val_rules.py

rml-system-spec-pack/03_building-blocks/F-04-gw-qos-scheduler-tuning/tuning.md (cross-repo contract)
  ↓ owns
  ├── TUNE-VAL-001~006 rules (validated by all three layers)
  └── Preset table definitions (SSOT for preset names and parameter ranges)

--base-dir/docs/trace_map.yaml (system-level trace SSOT)
  ↓ checked by
  └── --base-dir/tools/check-trace-coverage.py (coverage gate)
```

## Governance Rules

1. Every new REQ added to any repo spec MUST get a corresponding entry in `trace_map.yaml`
   within the same PR (or a follow-up PR in the same wave).
2. ACs and TCs MUST be added before marking a REQ `active`.
3. `pending_impl` REQs MUST have ACs. TCs may be `tcs: []` initially.
4. Spec-pack owner reviews trace_map.yaml updates from all repos via cross-repo PR review.
5. `check-trace-coverage.py` is run in CI (non-blocking warning until coverage > 80%).

## Dual-Layer TC Location

TC files live in two complementary locations; both are canonical for their respective scope:

| Layer | Location | Purpose |
| :--- | :--- | :--- |
| **System-level TC matrix** | `05_quality-acceptance/tc-matrix.md` (this repo) | cross-repo acceptance requirements, single source of system-wide TC IDs |
| **Repo-local TC impl** | `<each-repo>/docs/specs/` or `/tests/` | per-repo implementation-level test code; references TC IDs from system layer |

Rules:
- TC IDs are **assigned in `05_quality-acceptance/tc-matrix.md`** — repo-local files must use the same ID
- A TC is `repo_done` when repo-local impl passes; `cross_repo_done` only when all consumer repos pass
- `check-trace-coverage.py` validates that every system TC ID has at least one repo-local reference

## References

- AC catalog: [../05_quality-acceptance/ac-catalog.md](../05_quality-acceptance/ac-catalog.md)
- TC matrix: [../05_quality-acceptance/tc-matrix.md](../05_quality-acceptance/tc-matrix.md)
- Trace map SSOT: `--base-dir/docs/trace_map.yaml`
- FW-3A spec trace map: `--base-dir/docs/specs/fw-3a-cmd-v2-length-guard.md#trace-map-req--ac--tc--impl`
- Coverage tool: `--base-dir/tools/check-trace-coverage.py`
