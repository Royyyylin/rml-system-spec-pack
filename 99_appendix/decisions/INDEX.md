# decisions — Architecture Decision Records

> arc42 §9 — Design Decisions. Nygard format ADR: Context → Decision → Consequences.
> ADR-000 is foundational (prescriptive enforcement model) — content created in PR#4.
> ADR-001~007 are PR#4 drafts per plan review synthesis.

## ADR 清單

| ADR | 主題 | Status |
|---|---|---|
| ADR-000 | Spec Authority Model — prescriptive enforcement (機器可執行) | proposed (PR#4 content) |
| ADR-001 | Living Doc HTML publish defer | accepted (2026-04-26) |
| ADR-002 | Wardley Mapping defer | accepted (2026-04-26) |
| ADR-003 | C4 standard syntax defer (D2 already sufficient) | accepted (2026-04-26) |
| ADR-004 | spec-kit 不採用 | accepted (2026-04-26) |
| ADR-005 | ble_api.yaml 不轉 AsyncAPI | accepted (2026-04-26) |
| ADR-006 | spec-pack repo rename defer (Q3 2026) | accepted (2026-04-26) |
| ADR-007 | AC ID naming defer (AC-FW-3A-001 vs AC-001) | accepted (2026-04-26) |
| ADR-008 | Task A Completion Strategy — Real Enforcement Activation | accepted (2026-04-26) |
| ADR-009 | CC↔Central Transport — USB-Serial Host Bridge (resolves F7-OQ1) | accepted (2026-04-26) |
| ADR-010 | GW↔Central Uplink — CC Bridge Relay for Prototype (resolves F7-OQ2) | accepted (2026-04-26) |
| ADR-011 | ENG_UNLOCK Fail Policy — Immediate Lock on Wrong PIN (resolves F6-OQ1) | accepted (2026-04-26) |
| ADR-012 | PIN Rotation → Central Notification — Synchronous App-Side Push (resolves F6-OQ2) | accepted (2026-04-26) |
| ADR-013 | RML Opaque ID Schema Cleanup — L3 Source-Level Refactor (廢 11 RML prefix, name-canonical + chapter-position-canonical) | accepted (2026-04-27) |

## 格式規範

每個 ADR 用 Nygard format:
- Context: 決策背景
- Decision: 採用方案
- Consequences: 影響與代價

## Cross-ref

- 上層: 99_appendix/INDEX.md
- 全域 ADR: ~/.claude/adr/ (跨 repo 架構決策)
