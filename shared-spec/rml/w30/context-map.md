# Context Map — W30: Fleet Broadcast + WebSocket Push

> Wave: App Wave 30
> Source: `w30-01-fleet-broadcast.md`, `w30-02-auto-grouping.md`, `w30-03-websocket-push.md`

## Bounded Contexts

```mermaid
C4Context
    title W30 Bounded Contexts

    Person(eng, "Field Engineer / Admin", "fleet operation authority")

    Enterprise_Boundary(app_ctx, "App Domain") {
        System(broad_eng, "Broadcast Engine", "batch dispatch + ack tracking")
        System(group_cache, "Group Membership Cache", "read-only projection + staleness")
        System(ws_client, "WebSocket Client", "push event consumer")
    }

    Enterprise_Boundary(central_ctx, "Central Domain") {
        System(broad_api, "Broadcast API", "command routing + rate limit")
        System(group_api, "Auto-Group API", "server-authoritative rule engine")
        System(ws_server, "WebSocket Push Server", "device state + alert events")
    }

    Enterprise_Boundary(fw_ctx, "Firmware Domain") {
        System(gw_cmd, "GW Command Receiver", "profile switch / reboot / config push")
    }

    Rel(eng, broad_eng, "create + confirm + dispatch")
    Rel(broad_eng, broad_api, "REST batch dispatch")
    Rel(broad_api, gw_cmd, "forward command")
    Rel(gw_cmd, broad_api, "ack uplink")
    Rel(broad_api, broad_eng, "per-device ack status")
    Rel(group_api, group_cache, "rules + assignments sync")
    Rel(ws_server, ws_client, "WebSocket push events")
```

## Context Relationships

| Upstream | Downstream | Relationship | Contract |
|---|---|---|---|
| Central Broadcast API | App Broadcast Engine | Customer/Supplier | REST batch dispatch; per-device ack status |
| Central Auto-Group API | App Group Cache | Published Language | Rule model: criterion_type, value, target_group_id |
| Central WS Push Server | App WS Client | Event-Driven | WS event schema (device state + alert) |
| App Broadcast Engine | GW Firmware | Mediated (via Central) | Central routes; App does not directly reach GW |

## Anti-Corruption Layers

| Boundary | ACL Description |
|---|---|
| App ↔ auto-group rules | App treats rules as read-only; server authority not delegated to App |
| Per-device `acked` | Displayed as in-flight milestone; App must not upgrade to "final state applied" without separate authoritative confirmation |
| WS events ↔ REST data | WS push triggers UI refresh but does not replace REST as authoritative source for conflict resolution |

## Dependencies on Prior Waves

| Prior Wave | Dependency |
|---|---|
| Wave 24A (device groups model) | Group entity model reused by broadcast target selection and auto-group display |
| Wave 29A (sync engine) | Auto-group membership sync uses 29A `SyncEngine` integration point |
