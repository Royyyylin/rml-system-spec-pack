# Event Storming — W31: Auto-Grouping + WebSocket Refinement + Adaptive Layout

> Wave: App Wave 31A
> Source: `w31-01-auto-grouping.md`, `w31-02-websocket-push.md`, `w31-03-adaptive-layout.md`

## Domain Events

### Auto-Grouping Events

| Event | Trigger | Actor | Outcome |
|---|---|---|---|
| `AutoGroupRulesFetched` | App sync runs | App | `AutoGroupRule` entities cached locally |
| `GroupMembershipSynced` | 29A SyncEngine runs | App | Incremental membership diff applied |
| `GroupCacheStale` | >5min since last sync | App | Staleness badge shown in group list/detail |
| `OrgSwitched` | User changes organization | App | All group caches invalidated |
| `GroupDetailViewed` | Engineer taps group | App UI | Device list + per-device status shown |

### WebSocket Events

| Event | Trigger | Actor | Outcome |
|---|---|---|---|
| `WebSocketConnected` | App enters foreground | App | WS connection established with JWT auth |
| `HeartbeatSent` | 30s timer fires | App | Heartbeat message sent to Central WS |
| `HeartbeatMissed` | 3 consecutive heartbeats missed | App | Reconnect triggered |
| `WebSocketReconnecting` | Reconnect triggered | App | Exponential backoff applied (1s→30s) |
| `WebSocketFallbackActivated` | 5 reconnect failures | App | Switch to FCM polling at 5s interval |
| `CommandAckReceived` | Central sends ack via WS | App | Per-device status updated <1s |
| `MissedAcksQueried` | WS reconnects after disconnect | App | REST query for any missed acks during outage |
| `SyncHintReceived` | Central pushes sync hint | App | Triggers 29A SyncEngine incremental sync |

### Adaptive Layout Events

| Event | Trigger | Actor | Outcome |
|---|---|---|---|
| `BreakpointChanged` | Window size changes | App | `AdaptiveScaffold` re-renders nav component |
| `CompactLayoutActive` | width <600dp | App | `NavigationBar` shown (phone mode) |
| `MediumLayoutActive` | width 600–840dp | App | `NavigationRail` shown (tablet mode) |
| `ExpandedLayoutActive` | width >840dp | App | `NavigationDrawer` + master-detail shown |
| `IPadSplitViewDetected` | iPad split view activated | App | `IpadSplitScaffold` renders master-detail |

## Commands

| Command | Actor | Effect |
|---|---|---|
| `WsTransport.connect(url, jwtToken)` | App (foreground) | Establish WebSocket, start heartbeat |
| `WsTransport.disconnect()` | App (background) | Battery-aware disconnect |
| `BroadcastAckHandler.handleAck(correlationId, deviceId, status)` | App WS consumer | Update `FleetCommand` per-device status |
| `BroadcastAckFallback.startPolling()` | App (WS failed) | FCM 5s poll for acks |
| `GroupSyncService.sync()` | App (29A engine) | Incremental group membership sync |
| `AdaptiveScaffold.build(context)` | Flutter framework | Render correct nav by breakpoint |

## Aggregates

| Aggregate | State | Invariant |
|---|---|---|
| `WsTransport` | connection state + heartbeat timer + backoff state | Always falls back to FCM after 5 failures; never blocks offline flow |
| `BroadcastAckHandler` | `correlationId → deviceId` in-flight map | Uses correlation_id; not sequence number |
| `GroupMembershipCache` | members + last_sync per group | Invalidated on org switch; stale >5min shows badge |
| `AdaptiveScaffold` | breakpoint + nav component | Phone layout is pixel-identical (golden-file gate) |
