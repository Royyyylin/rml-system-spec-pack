# 01_context-scope

> arc42 §3 — 系統邊界、外部角色與統一語言
> Status: active (content migrated to arc42 structure PR#3)

## 內容

| 檔案 | 說明 |
|---|---|
| `bounded-context-map.md` | DDD Bounded Context 地圖 (5 contexts) + Authority Boundaries (6 boundary names) + ## System Actors (Gateway / Central / Conductor entity subsections) |
| `system-actors.d2` | 角色關係圖 (D2 diagram, AI Diagram Contract validated, source: bounded-context-map.md) |
| `ubiquitous-language.md` | DDD canonical vocabulary (← glossary.md) — AI session auto-loaded |
| `authority-map.yaml` | Machine-readable boundary per capability domain (schema v2.0, name-canonical, 6 capabilities ↔ 6 actor boundaries via maps_to_boundary field) |

## SSOT Pair (Backstage `kind` pattern)

The `bounded-context-map.md` (actor-axis) and `authority-map.yaml` (capability-axis) are SSOT pair across two complementary dimensions per Backstage `kind` pattern: actor "WHO" surface owns it (boundary names like `Central-Global-Truth-Authority`), capability "WHAT" capability domain (capability id like `canonical-identity-authority`)。Cross-link via `authority-map.yaml` `maps_to_boundary` field pointing to a boundary in `bounded-context-map.md` `## Authority Boundaries` table。

## 對應業界 reference

- arc42 §3 System Scope and Context
- DDD: Bounded Context Map, Ubiquitous Language
- C4: System Context diagram (Level 1)
- Backstage: `kind: System` + entity name (per ADR-013 reference)

## Cross-ref

- 上層: README.md
- 下層: bounded-context-map.md, system-actors.d2, ubiquitous-language.md, authority-map.yaml
- 鄰章: 00_introduction-goals/ (why), 03_building-blocks/ (what inside)
