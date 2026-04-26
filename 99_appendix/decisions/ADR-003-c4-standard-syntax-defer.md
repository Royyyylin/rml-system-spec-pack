# ADR-003: C4 Standard Syntax Defer (D2 Already Sufficient)

Status: accepted
Date: 2026-04-26
Decided by: Roy (post Phase 1 enforcement audit)

## Context

C4 Model (Simon Brown, 2018) provides a standardized hierarchy for architecture diagrams: Context → Container → Component → Code. The spec-pack Phase 1 audit evaluated whether all arc42 §3 (System Scope) and §5 (Building Blocks) diagrams should be migrated to strict C4 syntax (using Structurizr DSL or C4-PlantUML).

The current state: the spec-pack uses D2 for all architecture diagrams (`system-actors.d2`, component diagrams in `03_building-blocks/`). D2 was chosen in PR#3 for its:
- Native CI rendering via `d2 --watch` and `d2 --theme` flags
- No external server dependency (unlike Structurizr Cloud)
- Self-contained `.d2` source files version-controlled alongside Markdown

The C4 migration proposal was motivated by two arguments:
1. C4 is a widely understood standard; external reviewers familiar with Structurizr could read diagrams without learning D2 syntax
2. Structurizr DSL supports workspace-level validation and architecture-as-code export

However, the Phase 1 audit found that:
- D2 already renders Context and Container-level views at sufficient fidelity for the 4-bounded-context system
- Structurizr would introduce a second rendering pipeline (or cloud dependency) without adding new information
- The AI Diagram Contract comment block already enforces semantic consistency in D2 files
- quality-goals.md Goal 6 (Governance Automation) requires that spec PRs pass CI without manual intervention; adding Structurizr CLI to CI would require Docker image updates across all 4 repos

## Decision

Retain D2 as the sole diagram language for the spec-pack. Do not migrate to Structurizr DSL or C4-PlantUML.

C4 nomenclature (Context / Container / Component / Code levels) MAY be used informally in diagram titles and comments within D2 files, but no Structurizr DSL or C4-PlantUML files will be committed.

This decision is bounded: if D2 CI support degrades (upstream project abandonment or incompatible breaking change), the decision to adopt C4-standard tooling should be revisited as a new ADR.

## Consequences

**Positive:**
- Single diagram language reduces CI complexity
- D2 files remain self-contained and offline-renderable
- No external service dependency (Structurizr Cloud) for CI rendering
- Existing D2 diagrams are not invalidated

**Negative:**
- Engineers familiar with Structurizr DSL must learn D2 syntax
- No automatic C4 workspace-level consistency validation
- External architecture reviews expecting Structurizr exports must use D2 renders instead

**Constraint added:**
All new D2 diagram files MUST include the AI Diagram Contract comment block (AGENTS.md rule) and label their C4 level in the file header comment (e.g., `# C4 Level: Context`).

## Alternatives

- **Structurizr DSL + Structurizr CLI in CI**: Rejected — Docker image size increase, external rendering dependency, duplicates existing D2 CI path
- **PlantUML with C4-PlantUML extension**: Rejected — PlantUML requires Java runtime; CI already excludes Java from spec-pack toolchain
- **D2 + Structurizr DSL dual-source**: Rejected — two sources of truth for the same diagram violates SSOT principle (RML-OWN-001)
- **Mermaid C4 diagrams**: Evaluated — GitHub renders Mermaid natively, but Mermaid C4 support is limited to Context level only; insufficient for Building Blocks (§5) component views

## References

- ADR-008: Task A Completion Strategy
- D2 Language: https://d2lang.com/
- C4 Model: https://c4model.com/
- AGENTS.md: AI Diagram Contract rule
- capability-map.md: authority for bounded context ownership
