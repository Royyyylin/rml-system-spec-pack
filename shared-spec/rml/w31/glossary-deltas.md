# Glossary Deltas — W31: Auto-Grouping + WebSocket Refinement + Adaptive Layout

> Cross-links master glossary: `shared-spec/glossary.md`
> New terms introduced in App Wave 31A.

## New Terms

| Term | Definition | Canonical Location |
|---|---|---|
| `WsTransport` | Flutter service managing persistent WebSocket connection to Central. Handles JWT auth, 30s heartbeat, exponential backoff, and FCM fallback activation. | `lib/services/transport/ws_transport.dart` |
| `WsMessage` | Message envelope for WebSocket events. Fields: `type`, `payload`, `correlation_id`. | `lib/services/transport/ws_message.dart` |
| `WsReconnectPolicy` | Exponential backoff policy for WS reconnects: 1s→2s→4s→8s→16s→30s cap; after 5 failures activates FCM fallback. | `lib/services/transport/ws_reconnect_policy.dart` |
| `BroadcastAckHandler` | App service that processes WS ack events and updates `FleetCommand` per-device status using `correlation_id`. Must achieve <1s update. | `lib/services/fleet/broadcast_ack_handler.dart` |
| `BroadcastAckFallback` | App service that polls Central REST for missed acks at 5s interval when WS is disconnected. Auto-deactivates on WS reconnect. | `lib/services/fleet/broadcast_ack_fallback.dart` |
| `correlation_id` | Unique identifier in WS ack message linking response to original broadcast command. Must be used for ack matching; sequence number is insufficient. | `WsMessage` field |
| `AdaptiveScaffold` | Flutter widget that selects `NavigationBar` / `NavigationRail` / `NavigationDrawer` based on M3 breakpoint. Wraps existing screens without refactoring. | `lib/core/layout/adaptive_scaffold.dart` |
| `Breakpoints` | M3 window size classes: compact (<600dp), medium (600–840dp), expanded (>840dp). SSOT for all responsive layout decisions. | `lib/core/layout/breakpoints.dart` |
| `ResponsiveBuilder` | Flutter widget that provides per-screen layout variants by breakpoint. | `lib/core/layout/responsive_builder.dart` |
| `IpadSplitScaffold` | Layout widget for iPad medium/expanded breakpoint: master-detail (roster left, device detail right). | `lib/features/shell/ipad_split_scaffold.dart` |
| `FCM → WS migration` | W31 architecture change: FCM push is demoted to fallback-only for background/offline; WS becomes primary for latency-sensitive operations. | `w31-02-websocket-push.md` §2c |
| `phone layout regression gate` | Golden-file widget tests at compact (400dp) that must pass pixel-identically after adaptive layout migration. | `w31-03-adaptive-layout.md` §3a |

## Existing Terms Referenced

- `FleetCommand` / `FleetCommandStatus` — from W30; W31 WS ack updates these
- `GroupMembershipCache` — from W30; W31 adds group management UI
- `SyncEngine` — from Wave 29A; W31 reuses for group sync
- `FCM push` — from Wave 28A; W31 demotes to fallback
- `correlation_id` — introduced in W30 broadcast; formalized in W31 WS ack protocol

## Disambiguation

- `WS ack` vs `FCM ack` — WS ack is real-time (<1s); FCM fallback polls at 5s. Both use `correlation_id`. Do not conflate.
- `auto-group rules` in W31 are identical to W30 — W31 adds management UI but does not add new rule types. Server authority unchanged.
