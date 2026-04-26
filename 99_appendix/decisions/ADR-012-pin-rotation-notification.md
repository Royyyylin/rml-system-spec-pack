# ADR-012: PIN Rotation → Central Notification Mechanism

Status: accepted
Date: 2026-04-26
Decided by: Roy (K4 OQ resolution, resolves F6-OQ2)
Resolves: F6-OQ2 — was: PIN rotation → Central notification mechanism 未定

## Context

When an engineer writes a new PIN via `ENG_PIN_SET` GATT characteristic (`6f8a9c12-...`),
the PIN is stored in NVS via `app_settings_set_eng_pin_async()` (`qos_service.c:1180`).
Central maintains an audit log (`app/api/audit.py`) and needs to be aware of security-
sensitive configuration changes for compliance and incident response.

The open question was: when a PIN rotation occurs on a device, how does Central learn
about it? Two mechanisms were considered:

1. **Synchronous API push (App-triggered)**: The App that performed the ENG_PIN_SET
   write calls a Central API endpoint to log the rotation event immediately after
   the GATT write succeeds.

2. **Async event via CC bridge**: The CC bridge observes the ENG_PIN_SET GATT write
   (via EVT characteristic notification or by subscribing to PIN change events) and
   publishes an event to Central's ingest pipeline asynchronously.

3. **Central polls via ingest reconciliation**: No active notification; Central detects
   PIN rotation only during the next scheduled reconciliation cycle.

Design constraints:
- The PIN value itself must NEVER be sent to Central (it is credential material)
- Central only needs to know: device ID, timestamp, rotation event occurred
- App already has a direct HTTPS channel to Central (alias sync, assignment sync)
- CC bridge path (ADR-009/010) is already used for telemetry, not security events

The App is the initiating actor for PIN rotation (Phone-exclusive write authority per
`qos_service.c:1154`). App has the `gateway_id` / `stable_id` context at the time
of the write and can immediately call Central. The CC bridge path introduces an
additional hop and async delay for a security event where timeliness matters.

## Decision

PIN rotation → Central notification = **synchronous App-side API push**.

After a successful `ENG_PIN_SET` GATT write (ATT response success), the App calls
Central's audit endpoint (`POST /audit/events`) with:
```json
{
  "event_type": "eng_pin_rotated",
  "device_id": "<stable_id>",
  "gateway_id": "<gateway_id>",
  "actor": "app_engineer",
  "timestamp": "<ISO-8601 UTC>"
}
```

The PIN value is NOT included. Central records the audit event for compliance tracking.

The CC bridge async path is explicitly NOT used for this event because:
- Security events must be delivered with App-session context (who rotated, on which session)
- CC bridge may not be connected at the time of PIN rotation
- Async delivery creates audit gaps (event arrives after actor session ends)

If the App's Central POST fails (network partition), the App logs a local warning and
retries on next connection. A failed audit POST does NOT roll back the GATT write
(PIN is already changed in NVS). This is acceptable for SL-1 threat model (best-effort audit).

## Consequences

**Positive:**
- App already has Central auth context (session token from `app/api/auth.py`)
- Synchronous delivery: audit event arrives before App session ends, preserving actor context
- No CC bridge dependency for security event delivery
- PIN value is never transmitted over any network path

**Negative:**
- App must be online at time of PIN rotation for audit event delivery
  (offline rotation is silently unlogged at Central until App reconnects)
- Requires App implementation of `POST /audit/events` call after ENG_PIN_SET
- Central must define and document the `eng_pin_rotated` audit event schema

**Trigger for re-evaluation:**
If App-to-Central connectivity is unreliable in field deployments, consider buffering
audit events in App local storage and bulk-pushing on reconnect (FEA-004 reconciliation
pattern extension). This is Phase K or later work.

## Alternatives

- **CC bridge async event**: Rejected. CC bridge is transport-only (AGENTS.md); giving
  it security event awareness contradicts the authority model. Also CC may be offline.
- **Central polls firmware via CC ingest**: Rejected. Central has no way to distinguish
  PIN rotation from other NVS changes without firmware-level event signaling.
- **No Central notification (PIN stays local)**: Rejected. Audit trail for security
  credential changes is a compliance requirement (IEC 62443 audit logging requirement).
- **EVT characteristic notification on ENG_PIN_SET**: The EVT characteristic (`6f8a9c13`)
  is GW→App direction. Using it to signal Central would require App to intercept EVT and
  re-publish to Central — equivalent to the App-push approach but with extra indirection.

## References

- ENG_PIN_SET firmware: `ble_qos_demo_V1.2m/src/qos_service.c` lines 1138-1187
- Central audit API: `central-device-metadata/app/api/audit.py`
- AGENTS.md: CC bridge transport-only role definition
- ADR-009: CC↔Central Transport (CC bridge relay — NOT used for PIN events)
- ADR-011: ENG_UNLOCK Fail Policy (companion decision for PIN security)
- Security concept doc: `06_crosscutting-integration/concepts/security.md`
