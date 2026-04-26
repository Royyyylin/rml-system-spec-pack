# ADR-011: ENG_UNLOCK Fail Policy — Immediate Lock on Wrong PIN

Status: accepted
Date: 2026-04-26
Decided by: Roy (K4 OQ resolution, resolves F6-OQ1)
Resolves: F6-OQ1 — was: repeated ENG_UNLOCK_FAIL → connection drop policy 未定

## Context

The `ENG_UNLOCK` GATT characteristic (`6f8a9c11-...`) allows a Phone-exclusive write
of a PIN string to temporarily unlock engineer access on GW/ED firmware. The unlock
window is `QOS_ENG_UNLOCK_TIMEOUT_MS` (5 minutes, `qos_service.c:130`).

The current firmware implementation (`qos_service.c:1080-1136`) has the following
behavior on wrong PIN:
- Calls `eng_lock()` (line 1133) — clears unlock state
- Returns `BT_ATT_ERR_AUTHORIZATION` (line 1135)
- No retry counter, no lockout, no connection drop

The open question was: should repeated wrong PINs trigger:
1. **Immediate lock only** (current behavior): each wrong PIN locks and returns error
2. **N-attempt lockout with timed reset**: after N wrong attempts, block further
   attempts for T seconds, preventing brute force via BLE write loop
3. **Connection drop**: disconnect the BLE link after M consecutive failures,
   forcing attacker to re-scan and reconnect

The security threat model for this prototype is:
- Attacker is within BLE range (≤ 100m) with a BLE scanner
- PIN is 4-16 digit numeric (`isdigit` check, `qos_service.c:1174`)
- Minimum 4-digit PIN = 10,000 combinations; max 16-digit = 10^16
- BLE GATT write round-trip: ~50-200ms on 2M PHY → brute force 4-digit in ~500s

For a field engineering tool (not a consumer product), and given the prototype scope
(IEC 62443 SL-1 target per `06_crosscutting-integration/concepts/security.md`), the
defense priority is:
1. No persistent state changes without unlock (already enforced — ENG_PIN_SET checks `eng_is_unlocked()`)
2. Measurable resistance to casual brute force (no automation-friendly write loop)

## Decision

ENG_UNLOCK fail policy = **immediate lock on each wrong PIN** (preserving current
firmware behavior), with the following spec-level mandate:

1. **Immediate lock**: every wrong PIN write calls `eng_lock()` and returns
   `BT_ATT_ERR_AUTHORIZATION`. No state persisted between attempts.
2. **No connection drop**: the BLE connection is NOT dropped on wrong PIN. Dropping the
   connection would break the App UX (re-scan + reconnect required for legitimate users
   who mistyped) with minimal security benefit given 5-minute unlock window expiry.
3. **No timed lockout counter**: a retry counter in firmware requires NVS state or
   volatile counter with power-cycle reset vulnerability. For prototype SL-1 threat
   model, the cost/benefit does not justify the complexity.

A minimum PIN length of 6 digits (10^6 combinations) is RECOMMENDED when deploying
beyond the lab bench to increase brute force time to ~50,000 seconds (>13 hours).

**Production escalation path**: if threat model upgrades to SL-2 (authenticated remote
access), introduce a 3-attempt lockout with 60-second timed reset implemented in the
host-side CC daemon (not firmware), which can maintain state across BLE reconnects.

## Consequences

**Positive:**
- Zero firmware changes required — current behavior is the spec-compliant policy
- No NVS write or counter to manage — no persistent state corruption risk
- Clean UX: mistyped PIN returns error immediately without disconnecting App

**Negative:**
- Automated BLE write tool can attempt ~6000 4-digit PINs per 10-minute window
  before the engineer's 5-minute unlock window expires (mitigated by min PIN length recommendation)
- No audit log of failed attempts in firmware (host-side daemon can log at Central)
- Production SL-2 escalation deferred to host daemon layer, not firmware

**Trigger for re-evaluation:**
Threat model upgrade to IEC 62443 SL-2, OR deployment outside controlled lab with
remote access (VPN tunnel to Central). At that point, 3-attempt lockout in CC daemon.

## Alternatives

- **3-attempt lockout in firmware with timed reset**: Rejected. Requires NVS counter
  that resets on power cycle (easy circumvention) and adds volatile state machine to
  `write_eng_unlock`. SL-1 threat model does not require this.
- **Connection drop after 3 failures**: Rejected. Breaks legitimate App UX (mistype
  once → forced re-scan). Attacker can reconnect in <5s, providing minimal protection.
- **Rate limiting at GATT layer**: Rejected. NCS BLE stack does not expose per-characteristic
  write rate limiting; would require application-level timer adding complexity.

## References

- ENG_UNLOCK firmware: `ble_qos_demo_V1.2m/src/qos_service.c` lines 1080-1136
- Security concept doc: `06_crosscutting-integration/concepts/security.md`
- GATT service reference: `ble_qos_demo_V1.2m/docs/current/gatt_services.md`
- IEC 62443 SL target: `~/.claude/standards/_core/compliance-security-iec62443.md`
- ADR-008: Task A Completion Strategy (F6 security crosscutting context)
