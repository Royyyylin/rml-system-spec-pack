# Capability Matrix — W30: Fleet Broadcast + WebSocket Push

> Wave: App Wave 30
> Source: `w30-01-fleet-broadcast.md`, `w30-02-auto-grouping.md`, `w30-03-websocket-push.md`

## Per-Role Capabilities

| Capability | App | Central | GW Firmware |
|---|---|---|---|
| Fleet command domain model | **OWNS** — `FleetCommand`, `FleetCommandStatus` Dart models | — | — |
| Broadcast batch dispatch (≤100 pages) | **OWNS** — `BroadcastEngine` | routes to GW | executes |
| Per-device ack tracking | **OWNS** — in-flight milestone display | provides ack data | sends ack |
| Rate-limit enforcement (1/30s/user) | blocked by | **OWNS** — server-side | — |
| Rollback command generation | **OWNS** — auto-generated for profile_switch | — | — |
| Auto-group rule definition | read-only consumer | **OWNS** — server-authoritative | — |
| Auto-group rule types (zone/fw-version/alert) | consumes | **OWNS** — defines criteria | — |
| Group membership sync + local cache | **OWNS** — `GroupMembershipCache` | publishes | — |
| Group cache staleness tracking (>5min) | **OWNS** — `last_sync` badge | — | — |
| WebSocket push event consumer | **OWNS** — `WebSocketClient` | — | — |
| WebSocket push server | — | **OWNS** — event source | — |
| Command execution (profile switch / reboot) | sends command | routes | **OWNS** — runtime |

## Authority Boundaries (W30)

| ID | Boundary |
|---|---|
| `W30-BND-001` | Central owns auto-group rules — App must not define or edit rules; read-only display only |
| `W30-BND-002` | Per-device `acked` is a transport milestone — App must not display as "final state applied" without authoritative confirmation |
| `W30-BND-003` | Rate limit is server-enforced — App cannot bypass by batching or replaying |
| `W30-BND-004` | Group membership cache is a read-only projection — App must not mutate membership without round-trip to Central |
| `W30-BND-005` | WebSocket events are informational push — App must validate against Central REST data before treating as authoritative |
