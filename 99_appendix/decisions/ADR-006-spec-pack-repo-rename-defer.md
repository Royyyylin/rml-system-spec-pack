# ADR-006: spec-pack Repo Rename Defer (Q3 2026)

Status: accepted
Date: 2026-04-26
Decided by: Roy (post Phase 1 enforcement audit)

## Context

The spec-pack repository is currently named `rml-system-spec-pack`. The `rml-` prefix was a legacy naming convention from early project planning that used `RML-` as a system-wide ID namespace. During the arc42 restructuring (PR#3~PR#5), the canonical vocabulary replaced `RML-FEA-*` with `FEA-NNN-` and scoped `RML-*` IDs to authority boundary rules (RML-AUT-*, RML-SCP-*, RML-CAP-*, etc.) only.

The proposal was to rename the repo to `ble-qos-system-spec-pack` to:
1. Align with the product name (BLE QoS Demo system)
2. Remove the ambiguous `rml-` prefix from the public GitHub URL
3. Match the naming convention of the other 3 repos (`ble_qos_demo_V1.2m`, `ble_qos_app`, `central-device-metadata`)

The Phase 1 audit identified the following blockers for immediate rename:

1. **Cross-repo URL references**: At least 23 cross-repo `@import` and CI script references point to `rml-system-spec-pack` by name (vocabulary-check path, cross-ref linter, CLAUDE.md imports). A rename without updating all 4 repos simultaneously would break CI across the board.

2. **Phase 2a/2b work in flight**: Sub-plans F, G, H are executing against the current repo name. Renaming mid-flight would invalidate worktree paths and branch names in active sub-plans.

3. **GitHub Rulesets scope**: The GitHub Ruleset (ADR-008 Decision 2) is scoped to `rml-system-spec-pack`. A rename requires recreating the ruleset with the new name, which is a separate atomic operation.

The `RML-*` ID namespace (RML-AUT-*, RML-SCP-*, RML-CAP-*, etc.) is retained regardless of repo name — these IDs are content identifiers, not repo-name-derived.

## Decision

Defer the repo rename to Q3 2026 (after Phase 2b and Phase 2c sub-plans complete and CI enforcement is fully green across all 4 repos).

The rename operation, when executed, must be atomic:
1. Rename GitHub repo via `gh api -X PATCH /repos/Royyyylin/rml-system-spec-pack -f name=ble-qos-system-spec-pack`
2. Update all 4 repo CI scripts, CLAUDE.md imports, and cross-ref linter paths in a single coordinated PR
3. Recreate GitHub Ruleset under new repo name
4. Update all `git remote set-url` in local worktrees

Until then, `rml-system-spec-pack` remains the canonical repo name. All documentation must use this name without abbreviation.

## Consequences

**Positive:**
- Active Phase 2 sub-plans are not disrupted
- CI remains stable during enforcement hardening
- GitHub Ruleset scope is not invalidated

**Negative:**
- The `rml-` prefix creates mild naming inconsistency with other repos until Q3 2026
- External links to the repo (if any) will require a GitHub redirect update at rename time
- Engineers must remember the legacy naming convention until rename executes

**Constraint added:**
Any new script, CLAUDE.md import, or CI job added before the rename MUST use the current repo name `rml-system-spec-pack` without soft-coding — to make the eventual grep-and-replace rename operation unambiguous.

## Alternatives

- **Immediate rename**: Rejected — risk of breaking 4-repo CI mid-Phase 2; Phase 2a/2b worktrees would need path updates
- **Alias via GitHub redirect only**: Rejected — GitHub redirects are best-effort and do not update `git remote` URLs in existing clones
- **Rename at Phase 2b completion**: Considered; deferred further to Q3 2026 to allow Phase 2c (sub-plan I) to complete, making the rename a clean Phase 3 entry point
- **Keep rml- prefix permanently**: Rejected — naming inconsistency with product line grows over time; deferred not abandoned

## References

- ADR-008: Task A Completion Strategy (phase gate conditions)
- GitHub repo rename API: `gh api -X PATCH /repos/{owner}/{repo} -f name={new-name}`
- Vocabulary canonical list: CLAUDE.md (deprecated `RML-FEA-*` → `FEA-NNN-`)
- Q3 2026 target: Phase 4 (K) Architecture Foundation Review initiation
