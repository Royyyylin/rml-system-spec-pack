# Capability Matrix — W31: Auto-Grouping + WebSocket Refinement + Adaptive Layout

> Wave: App Wave 31A
> Source: `w31-01-auto-grouping.md`, `w31-02-websocket-push.md`, `w31-03-adaptive-layout.md`

## Per-Role Capabilities

| Capability | App | Central | GW Firmware |
|---|---|---|---|
| Auto-group rule definition | read-only consumer | **OWNS** — server-authoritative | — |
| Group membership sync + local cache | **OWNS** — `GroupMembershipCache` | publishes via 29A sync | — |
| Group staleness tracking (>5min badge) | **OWNS** | — | — |
| Group UI (list + detail) | **OWNS** | — | — |
| WebSocket transport (connect/auth/heartbeat) | **OWNS** — `WsTransport` | **OWNS** — WS endpoint | — |
| WS ack handler (command acks <1s) | **OWNS** — `BroadcastAckHandler` | sends acks | — |
| FCM fallback (WS disconnected → 5s poll) | **OWNS** — `BroadcastAckFallback` | — | — |
| FCM → WS migration (prefer WS when available) | **OWNS** — migration logic | — | — |
| Adaptive breakpoint system | **OWNS** — `Breakpoints`, `AdaptiveScaffold` | — | — |
| iPad Split View / Slide Over support | **OWNS** — `IpadSplitScaffold` | — | — |
| Desktop master-detail layout | **OWNS** — expanded breakpoint layout | — | — |
| Phone layout regression gate | **OWNS** — pixel-identical golden-file tests | — | — |

## Authority Boundaries (W31)

| ID | Boundary |
|---|---|
| `W31-BND-001` | Central owns auto-group rules — same as W30; W31 only adds group management UI on top |
| `W31-BND-002` | WS ack uses `correlation_id` — App must not infer ack from sequence number or timing alone |
| `W31-BND-003` | WS events are supplementary to REST — WS disconnect must not block core functionality (FCM fallback must work) |
| `W31-BND-004` | Adaptive layout migration must preserve phone behavior exactly — golden-file regression tests gate migration |
| `W31-BND-005` | State sharing for iPad multi-window via Riverpod global providers — no special IPC; no Central sync for window layout |
