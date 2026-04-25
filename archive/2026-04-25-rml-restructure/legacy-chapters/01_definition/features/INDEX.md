# features — Cross-Repo Feature Contracts

6 個 cross-repo feature contract。每個 feature 有 4-owner Authority Boundary 表，
**不能搬到 single product repo**（會 break per-repo 自治）。

## Feature 清單

| ID | 目錄/檔案 | 說明 |
|---|---|---|
| RML-FEA-001 | [RML-FEA-001-telemetry-roster-visibility.md](RML-FEA-001-telemetry-roster-visibility.md) | Telemetry roster 可視性（← feature-telemetry-roster-visibility.md） |
| RML-FEA-002 | [RML-FEA-002-command-execution-feedback.md](RML-FEA-002-command-execution-feedback.md) | 指令執行 feedback（← feature-command-execution-feedback.md） |
| RML-FEA-003 | [RML-FEA-003-identity-alias-metadata-display.md](RML-FEA-003-identity-alias-metadata-display.md) | Identity alias metadata 顯示（← feature-identity-alias-metadata-display.md） |
| RML-FEA-004 | [RML-FEA-004-assignment-reconciliation/](RML-FEA-004-assignment-reconciliation/) | Assignment reconciliation（含 contract + context.d2 + states.d2） |
| F-04 | [F-04-gw-qos-scheduler-tuning/](F-04-gw-qos-scheduler-tuning/) | GW QoS scheduler tuning（含 tuning + extension-boundary） |
| — | [session-topology.d2](session-topology.d2) | Session topology diagram（shared context） |

## Cross-ref hint

- AC catalog → [02_acceptance/ac-catalog.md](../../02_acceptance/ac-catalog.md)
- Feature owner → [../capability-ownership.md](../capability-ownership.md)

> 本 dir 由 PR #2 skeleton 建立，PR #4 rename 填內容。
