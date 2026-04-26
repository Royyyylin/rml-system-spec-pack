# ADR-007: AC ID Naming Defer (AC-FW-3A-001 vs AC-001)

Status: accepted
Date: 2026-04-26
Decided by: Roy (post Phase 1 enforcement audit; plan Decision 2)

## Context

The acceptance criteria (AC) catalog (`05_quality-acceptance/ac-catalog.md`) currently uses a hierarchical ID scheme: `AC-FW-3A-001` (format: `AC-<owner>-<spec-phase>-<seq>`). An alternative flat scheme was proposed: `AC-001`, `AC-002`, etc., with no owner/phase prefix.

The debate arose because:

1. **Hierarchical IDs encode coupling**: `AC-FW-3A-001` embeds the firmware spec phase (`FW-3A`) into the AC ID. If the spec phase is re-scoped or renamed, all AC IDs referencing it must be updated — a cascading rename that affects the TC matrix, BDD scenarios, and cross-repo trace entries simultaneously.

2. **Flat IDs lose traceability**: `AC-001` is opaque — a reviewer cannot infer from the ID alone whether the AC belongs to firmware, app, central, or a cross-repo feature. The cross-repo-trace-strategy requires that trace entries identify their owning domain.

3. **FEA-NNN prefix pattern**: The canonical vocabulary established `FEA-NNN-` for cross-repo features and `F-NN` for firmware-led features. There is no established canonical for AC IDs. A decision here creates a vocabulary precedent.

The Phase 1 audit (plan Decision 2) flagged this as an active conflict in the AC catalog with 47 existing IDs — too many to rename without a clear canonical decision and an automated migration script. Making a premature choice and then reversing it would create a second cascading rename.

The quality-goals.md Goal 2 (Spec Traceability) requires a stable trace chain from spec → AC → TC → wire ref. Changing AC ID format mid-chain breaks existing trace entries in `06_crosscutting-integration/cross-repo-trace-strategy.md`.

## Decision

Defer AC ID naming standardization until Phase 2c (sub-plan I), after FEA-001~004 and F-04 AC catalogs are fully authored and the cross-repo trace linter is in required-status CI mode.

The deferred decision will be made as: **the AC ID format that the cross-repo trace linter can validate automatically wins**. If the linter can validate both formats equally, the hierarchical format (`AC-<domain>-<seq>`) is preferred for human readability.

During the defer period:
- New ACs MUST use the existing hierarchical format (`AC-FW-3A-001` style) to avoid introducing a second format before the decision is made
- No mass-rename of existing AC IDs is permitted
- This ADR is the single blocker record preventing premature standardization

## Consequences

**Positive:**
- Avoids a premature cascading rename of 47+ AC IDs
- Defers until cross-repo trace linter can validate the chosen format automatically
- Maintains current trace chain integrity for FEA-001~004 in-flight specs

**Negative:**
- AC ID format inconsistency between features authored before and after the Phase 2c decision
- Reviewers cannot assume a stable AC ID format during Phase 2
- The Phase 2c sub-plan I must include an AC ID migration script as a required deliverable

**Constraint added:**
Phase 2c sub-plan I must deliver:
1. Final AC ID naming ADR (superseding this defer)
2. Migration script: `tools/migrate-ac-ids.py` — validates current IDs, produces rename mapping, updates ac-catalog.md + tc-matrix.md + cross-repo-trace-strategy.md atomically
3. Cross-repo trace linter rule for the chosen AC ID format

## Alternatives

- **Immediate flat `AC-NNN` rename**: Rejected — 47 existing IDs, no linter, high cascading risk
- **Immediate hierarchical standardization (keep current)**: Partially accepted — keep current format for new ACs, but defer formal standardization; this is the minimum viable consistency action
- **Domain-scoped flat IDs (`AC-FW-001`, `AC-APP-001`)**: Considered as a Phase 2c candidate; does not embed spec-phase, reduces coupling; held for Phase 2c evaluation
- **No standardization (free-form)**: Rejected — quality-goals.md Goal 2 requires a stable, linter-validatable trace chain

## References

- ADR-008: Task A Completion Strategy (plan Decision 2)
- quality-goals.md Goal 2 (Spec Traceability)
- ac-catalog.md: `05_quality-acceptance/ac-catalog.md` (current AC inventory)
- cross-repo-trace-strategy.md: trace chain requirements
- Phase 2c (sub-plan I) scope: master plan `~/.claude/plans/task-a-real-enforcement.md`
