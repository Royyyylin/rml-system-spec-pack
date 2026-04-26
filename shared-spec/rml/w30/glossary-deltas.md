# Glossary Deltas — W30: Fleet Broadcast + WebSocket Push

> Cross-links master glossary: `01_context-scope/ubiquitous-language.md`
> New terms introduced in App Wave 30.

## New Terms

| Term | Definition | Canonical Location |
|---|---|---|
| `FleetCommand` | App domain entity for a fleet-wide command. Fields: type (profile_switch/reboot/config_push), target group, params, status. | `lib/domain/fleet/fleet_command.dart` |
| `FleetCommandStatus` | Enum: `draft → confirmed → dispatched → partial → complete → failed`. No skipping transitions allowed. | `lib/domain/fleet/fleet_command_status.dart` |
| `BroadcastEngine` | App service that takes a confirmed command + target group, paginates into ≤100-device batches, dispatches via Central API, and tracks per-device ack. | `lib/services/fleet/broadcast_engine.dart` |
| `BroadcastRateLimiter` | App + server guard: max 1 broadcast per 30s per user. Second broadcast within 30s returns error. | `lib/services/fleet/broadcast_rate_limiter.dart` |
| `per-device acked` | Transport/workflow milestone indicating a device acknowledged the broadcast command. NOT equivalent to "final state applied". | W30 §1a Truth Boundary Note |
| `rollback command` | Auto-generated undo command for `profile_switch` type broadcast. One-tap rollback available after complete. | `BroadcastEngine` auto-generation |
| `AutoGroupRule` | Domain entity: server-defined rule that assigns devices to groups by zone, firmware version, or alert status. Read-only in App. | `lib/domain/groups/auto_group_rule.dart` |
| `GroupMembershipCache` | App-local read-only projection of group assignments. Tracks `last_sync` timestamp; shows staleness badge if >5min. Invalidated on org switch. | `lib/data/groups/group_membership_cache.dart` |
| `GroupSyncService` | App service that integrates auto-group membership sync with 29A SyncEngine. Incremental: only changed memberships transferred. | `lib/services/groups/group_sync_service.dart` |
| `WebSocket push` | Real-time event channel from Central to App. Used for device state changes and alert events. Does not replace REST as authoritative source for conflicts. | `w30-03-websocket-push.md` |

## Existing Terms Referenced

- `device groups` — group model from Wave 24A; prerequisite for W30 broadcast target selection
- `SyncEngine` — from Wave 29A; reused for auto-group membership sync
- `canonical truth` — Central's assignment/identity authority; `acked` status is NOT canonical truth (per W30 boundary rule)
