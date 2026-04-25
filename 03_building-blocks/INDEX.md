# 03_building-blocks

> arc42 §5 — Cross-repo feature contracts 與 session topology
> Status: active (content moved + renamed PR#3+4)

## 內容

| 檔案/目錄 | Feature | 說明 |
|---|---|---|
| `FEA-001-telemetry-roster-visibility.md` | FEA-001 | Telemetry roster visibility contract |
| `FEA-001-telemetry-roster-visibility.d2` | FEA-001 | Context diagram |
| `FEA-002-command-execution-feedback.md` | FEA-002 | Command execution feedback contract |
| `FEA-002-command-execution-feedback.d2` | FEA-002 | Context diagram |
| `FEA-003-identity-alias-metadata-display.md` | FEA-003 | Identity alias metadata display contract |
| `FEA-003-identity-alias-metadata-display.d2` | FEA-003 | Context diagram |
| `FEA-004-assignment-reconciliation/` | FEA-004 | Assignment reconciliation (fractal split) |
| `F-04-gw-qos-scheduler-tuning/` | F-04 | GW QoS scheduler tuning (firmware-led, fractal split) |
| `session-topology.d2` | — | BLE session topology |

## 命名規則

- FEA-NNN: cross-repo feature (App-led / Central-led / 平等 4-owner)
- F-NN: firmware-initiated AND firmware runtime behavior 為主 (legacy F-04)

## 對應業界 reference

- arc42 §5 Building Block View
- C4: Component diagram (Level 3)
- DDD: Aggregate, Domain Service

## Cross-ref

- 上層: README.md
- 下層: FEA-NNN-*.md, F-04-*/INDEX.md, session-topology.d2
- 鄰章: 02_solution-strategy/ (strategy), 04_runtime-view/ (sequence)
