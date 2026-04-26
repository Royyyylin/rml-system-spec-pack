# 06_crosscutting-integration

> arc42 §6 — 跨 repo trace 策略、Wire Parity、合規矩陣與 Crosscutting Concepts
> Status: active (content migrated to arc42 structure PR#3)

## 內容

| 檔案 | 說明 |
|---|---|
| `cross-repo-trace-strategy.md` | 跨 repo trace 策略 + dual-layer TC 段 (← s3-cross-repo-trace-strategy.md) |
| `x1-wire-parity-plan.md` | X1 Wire Parity plan (← x1-cross-repo-wire-parity-plan.md) |
| `x1-wire-parity-spec.md` | X1 Wire Parity spec (← x1-cross-repo-wire-parity-spec.md) |
| `market-compliance-matrix.md` | 市場合規矩陣 BT/FCC/CE/NCC (← market-compliance-matrix.md) |

## arc42 §6 Crosscutting Concepts

| 檔案 | 說明 |
|---|---|
| `concepts/logging.md` | LOG event 13-dim schema、wire format、category bitmap、multi-layer retention policy |
| `concepts/security.md` | ENG_UNLOCK PIN flow、key handling boundary、PIN rotation policy、threat model edges |
| `concepts/failover.md` | GW chain HA topology、uplink_ring strategy、A/B/C uplink class priority、reconciliation event flow |

## 對應業界 reference

- arc42 §6 Crosscutting Concepts
- arc42 §8 Crosscutting Concepts
- IEC 62443: Security compliance tracing
- BT SIG / FCC / CE RED: market compliance
- OPC UA / ISA-18.2: LOG event taxonomy

## Cross-ref

- 上層: README.md
- 下層: cross-repo-trace-strategy.md, x1-wire-parity-{plan,spec}.md, market-compliance-matrix.md
- Concepts: concepts/logging.md, concepts/security.md, concepts/failover.md
- 鄰章: 05_quality-acceptance/ (AC/TC), trace/trace_map.yaml (SSOT trace)
