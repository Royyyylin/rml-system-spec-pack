# ADR-002: Wardley Mapping Defer

Status: accepted
Date: 2026-04-26
Decided by: Roy (post Phase 1 enforcement audit)

## Context

Wardley Mapping (Simon Wardley, 2017) was proposed as a strategic tool to visualize component evolution across the four bounded contexts (Canonical Identity / Wire Contract / Runtime Observation / Interaction Semantics) and to inform build-vs-buy decisions for the BLE QoS system.

The proposal arose from Phase 1 audit finding that the spec-pack lacked a strategic evolution view: capability-map.md describes ownership but not maturity trajectory. Wardley Maps would have filled this gap by placing each capability on a genesis→commodity axis.

However, two factors make Wardley Mapping premature at current maturity:

1. **Stabilization prerequisite**: A meaningful Wardley Map requires stable component identification. The feature set (FEA-001~004, F-04) is still in active spec authoring. Mapping unstable components produces maps that are invalidated within the same sprint.

2. **Tooling and skill overhead**: The spec-pack currently uses D2 for all diagrams. Adding Wardley-specific tooling (OnlineWardley, Wardley Maps for VSCode, or raw SVG) introduces a second diagram language without a corresponding CI validation path. The doc-size-limit hook and cross-ref linter would need Wardley-specific extensions.

The quality-goals.md Goal 2 (Spec Traceability) requires that spec artifacts have CI-validated cross-references. A Wardley diagram committed without CI validation support would create a governance gap.

## Decision

Defer Wardley Mapping to Phase 4 (Architecture Foundation Review, per ADR-008), after FEA-001~004 and F-04 implementation is complete and component boundaries are stable.

During the defer period:
- No Wardley Map files are committed to spec-pack
- Strategic evolution analysis is captured informally in ADRs (this file and referenced documents)
- The capability-map.md (arc42 §4) remains the authority for ownership boundaries

Defer conditions to re-evaluate:
- All FEA-NNN and F-NN features have accepted specs AND at least one integration test passing
- D2 CI path is stable and cross-ref linter is in required-status mode

## Consequences

**Positive:**
- Avoids committing strategic maps that would require re-drawing within weeks
- Eliminates second diagram-language dependency in CI
- Allows Phase 4 to produce a Wardley Map that accurately reflects the delivered system

**Negative:**
- No visual strategic evolution view during active development phases
- Build-vs-buy decisions (e.g., Central identity vs. existing CIAM service) must be argued in prose ADRs rather than map coordinates
- Engineering team cannot use Wardley coordinates for sprint prioritization

**Risk mitigation:**
ADR prose in this file captures the key evolution assumptions: BLE GATT contract = genesis/custom; identity management = transitioning toward product; telemetry ingest = custom today.

## Alternatives

- **Immediate Wardley Map in SVG**: Rejected — no CI validation path; any map committed today would be stale by Phase 2b completion
- **Miro/Figma embed link**: Rejected — external tool dependency, not version-controlled, breaks spec-pack self-contained invariant
- **Text-based Wardley (Markdown table)**: Considered; deferred alongside visual map because the table would also need CI cross-ref validation once CI gates are required-status

## References

- ADR-008: Task A Completion Strategy (phase gate conditions)
- capability-map.md: current authority for ownership boundaries
- Wardley Maps: https://learnwardleymapping.com/
- Phase 4 (K) trigger: master plan `~/.claude/plans/task-a-real-enforcement.md`
