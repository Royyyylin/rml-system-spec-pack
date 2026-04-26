# ADR-001: Living Doc HTML Publish Defer

Status: accepted
Date: 2026-04-26
Decided by: Roy (post Phase 1 enforcement audit)

## Context

The initial spec-pack design included a goal to publish all arc42 chapters as a human-browsable HTML Living Document, following the arc42 Living Documentation pattern (Gernot Starke, 2023). Several tooling options were evaluated: arc42-tools, Docusaurus, mkdocs-material, and direct GitHub Pages with a lightweight D2 + Markdown pipeline.

Two blockers were identified during Phase 1:

1. **CI gate not fully enforced**: The vocabulary-check + doc-size-limit + cross-ref linter gates were not yet blocking merges at PR time (dummy `RML-FEA-XYZ` PR was still mergeable). Publishing live HTML before enforcement is active would propagate unvalidated spec content to a public surface.

2. **Premature stabilization cost**: arc42 chapters §4 (Runtime View) and §5 (Quality/Acceptance) are still under active authoring (FEA-001~004, F-04). Freezing HTML rendering templates before these chapters stabilize would create continuous rework overhead with no immediate user value.

The quality-goals.md Goal 2 (Spec Traceability) and Goal 6 (Governance Automation) explicitly require that spec artifacts are CI-gated before being surfaced to consumers. Publishing HTML without this gate active contradicts both goals.

## Decision

Defer Living Doc HTML publish pipeline until Phase 4 (Architecture Foundation Review, per ADR-008 Decision 1). The defer boundary condition is: all 4 CI enforcement gates (vocab-check, doc-size-limit, cross-ref linter, impl-tag linter) are in required-status mode on all 4 repos.

During the defer period:
- Spec content remains Markdown-only, browsable via GitHub UI
- No Docusaurus / mkdocs-material template is committed
- D2 diagrams continue to be rendered on-demand (not auto-published)
- This ADR is the single record that HTML publish is deferred, not forgotten

## Consequences

**Positive:**
- Eliminates rework risk from publishing unstable arc42 chapters
- Enforcement gates can be validated independently without HTML pipeline complexity
- Simplifies CI: no multi-stage build, no GitHub Pages deploy job

**Negative:**
- External stakeholders cannot browse a rendered spec without running mkdocs locally
- DDD diagram embeds (D2 SVG) are not rendered inline in GitHub Markdown
- Arc42 chapter navigation (sidebar, cross-links) must be done manually via INDEX files

**Trigger for re-evaluation:**
ADR-008 Phase 4 (K) initiation, or when Goal 6 CI gates are all in `required` mode.

## Alternatives

- **Immediate mkdocs deploy**: Rejected — would publish spec with unvalidated vocabulary and broken cross-refs visible in CI but not blocking
- **GitHub Pages from main, branch protection only**: Rejected — enforcement is Ruleset-level (ADR-008 Decision 2), not legacy branch protection; GitHub Pages jobs would need separate validation
- **Docusaurus static export**: Rejected for same timing reason; adds Node.js build dependency without current benefit

## References

- ADR-008: Task A Completion Strategy (acceptance gate conditions)
- quality-goals.md Goal 2 (Spec Traceability), Goal 6 (Governance Automation)
- arc42 §9 Living Documentation: https://docs.arc42.org/tips/9-1/
- Phase 4 (K) trigger: master plan `~/.claude/plans/task-a-real-enforcement.md`
