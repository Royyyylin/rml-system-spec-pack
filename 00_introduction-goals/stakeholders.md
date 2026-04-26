# Stakeholders

> arc42 §1 — Stakeholders.
> **L3 Source-Level Refactor 2026-04-27** (per `~/.claude/plans/task-b-rml-ddd-refactor.md`): `RML-ACT-*` / `RML-ROL-*` opaque ID schema 已廢除，改 name-canonical unified role table (per D1). Cross-ref by `file.md#section-anchor` (per D3).
> System Actors (Gateway / Edge Nodes / Central / Conductor) → see [bounded-context-map.md#system-actors](../01_context-scope/bounded-context-map.md#system-actors).
> Authority Boundaries → see [bounded-context-map.md](../01_context-scope/bounded-context-map.md).

## Roles

Unified role table covering human and AI agent roles. System-type actors (Gateway / Edge Nodes, Central System, Conductor) are defined in [bounded-context-map.md#system-actors](../01_context-scope/bounded-context-map.md#system-actors).

| Role Name | Type | Responsibility | Permission Scope | Bounded Context Cross-Ref |
| :--- | :--- | :--- | :--- | :--- |
| Operator | Human | 查看 fleet / device 基本狀態，執行日常操作，處理低風險操作流程。 | 查看 + 已授權低風險操作；不得單獨定義 canonical identity、assignment truth 或 system policy。 | [bounded-context-map.md#authority-boundaries](../01_context-scope/bounded-context-map.md#authority-boundaries) |
| Installer / Maintainer | Human | 執行一般維護操作、查看 detail、處理現場更換；屬於 human operational role，不改變第一級 actor 分層。 | 維護操作 + detail 查看；不得繞過 Central authority。 | [bounded-context-map.md#authority-boundaries](../01_context-scope/bounded-context-map.md#authority-boundaries) |
| Engineer | Human | 執行工程診斷、進階命令、衝突與例外排查，承接較高權限維護流程。 | 高權限診斷 + 維護流程；不得繞過 Central authority 或直接改寫 repo SSOT。 | [bounded-context-map.md#authority-boundaries](../01_context-scope/bounded-context-map.md#authority-boundaries) |
| AI Continuator | AI Agent | 接續 cross-repo spec 維護、trace 驗證、handoff 管理，確保 AI-Continuable-Traceability 目標達成。 | Read spec + propose changes（不直接 override runtime truth）。 | [bounded-context-map.md#system-actors](../01_context-scope/bounded-context-map.md#system-actors) |
