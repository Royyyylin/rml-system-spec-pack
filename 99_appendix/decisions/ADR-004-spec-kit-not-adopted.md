# ADR-004: spec-kit Not Adopted

Status: accepted
Date: 2026-04-26
Decided by: Roy (post Phase 1 enforcement audit)

## Context

`spec-kit` is a third-party specification management framework (npm package: `@spec-kit/core`) that provides opinionated templates for feature specs, AC catalogs, and test case matrices, with built-in linting and a CLI for cross-reference validation.

The spec-pack Phase 1 audit evaluated spec-kit as a potential replacement or supplement for the hand-rolled arc42 + Nygard ADR + vocabulary-check pipeline. The evaluation was triggered by audit finding that the existing spec pipeline required significant manual governance (vocabulary-check script, doc-size-limit hook, cross-ref linter) that could potentially be unified under a single framework.

The evaluation revealed three disqualifying factors:

1. **Arc42 chapter structure incompatibility**: spec-kit assumes a flat spec-per-feature hierarchy (one directory per feature, one `spec.md` file). The arc42 §1-§9 chapter structure is fundamentally different and cannot be expressed as spec-kit feature directories without losing the arc42 cross-reference model that quality-goals.md Goal 2 (Spec Traceability) requires.

2. **Cross-repo trace strategy conflict**: spec-kit's cross-reference model is file-based within a single repo. The cross-repo trace strategy (`06_crosscutting-integration/cross-repo-trace-strategy.md`) requires trace links across 4 repos with external SSOT validation. spec-kit has no mechanism for cross-repo trace validation.

3. **Dependency chain risk**: The spec-pack CI must be minimal (vocabulary-check script = 50-line Python; doc-size-limit = 80-line bash) to remain auditable and portable. Adding an npm dependency chain (spec-kit pulls 47 transitive dependencies) introduces supply-chain risk that contradicts the clean-room engineering boundary (quality-goals.md Goal 7).

## Decision

Do not adopt spec-kit. The hand-rolled pipeline (vocabulary-check + doc-size-limit hook + cross-ref linter + arc42 chapter structure) remains the authoritative governance mechanism for the spec-pack.

The scripts in `tools/` (vocabulary-check, doc-size-limit) are the spec-kit equivalent for this project. They are owned, auditable, and have no external npm dependency.

Future spec tooling decisions must pass the same evaluation criteria:
- Compatible with arc42 §1-§9 chapter structure
- Supports cross-repo trace validation
- Adds zero npm/pip transitive dependencies to the spec-pack CI

## Consequences

**Positive:**
- Zero new npm dependency risk
- Existing vocabulary-check + cross-ref linter scripts remain the SSOT for spec governance
- arc42 chapter structure preserved without mapping/translation layer
- All spec tooling is auditable: < 200 lines per script

**Negative:**
- No out-of-box spec template generation; each new feature spec must be authored manually per `00_introduction-goals/feature-design-guide.md`
- No spec-kit community or ecosystem to draw from
- Cross-repo trace validation must be maintained by the project team, not delegated to a framework

**Guard condition:**
If the vocabulary-check or cross-ref linter scripts exceed 300 lines (doc-size-limit threshold), they must be split or refactored before a spec-kit re-evaluation is considered.

## Alternatives

- **Adopt spec-kit with arc42 adapter**: Evaluated — no adapter exists; estimated 2-3 sprint effort to build one, higher than maintaining existing scripts
- **Adopt spec-kit for feature specs only (§3 level)**: Rejected — creates dual-track spec governance; violates SSOT principle
- **Adopt Backstage TechDocs + catalog-info.yaml**: Evaluated — Backstage requires a running portal service; incompatible with spec-pack's offline-first, git-native constraint
- **Keep status quo (current scripts)**: Accepted — this decision formalizes the existing approach

## References

- ADR-008: Task A Completion Strategy
- quality-goals.md Goal 7 (Authority Boundary Enforcement)
- cross-repo-trace-strategy.md: cross-repo trace validation design
- feature-design-guide.md: manual feature spec authoring guide
- tools/README.md: existing spec tooling inventory
