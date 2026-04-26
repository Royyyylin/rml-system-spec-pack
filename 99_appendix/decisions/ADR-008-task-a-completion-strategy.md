# ADR-008: Task A Completion Strategy — Real Enforcement Activation

Status: accepted
Date: 2026-04-26
Decided by: Roy (post 4 audit + 4 sub-agent review)

## Context

ADR-000 (X-修正) 宣告 spec-pack prescriptive enforcement, sub-plan A/B/C/D 完成後宣稱 redesign 28→70+. 4 paranoid audit 揭露真完成度 **50-55%**: branch protection 沒設 (CI cosmetic, dummy PR `RML-FEA-XYZ` 仍 mergeable) / firmware live symlink 仍指 deprecated / @import 本機絕對路徑 / 漏 ADR 實體 / V-Model docs empty.

4 sub-agent review (Phased / Scope / Risk / Alt) 揭露額外結構問題: F+G hidden dep (F§1→G), I 該升 Phase 2c, 「主 repo 沒裝 vocab-check」真因是 local pull stale + 2 INDEX hard ref miss + central CLAUDE @shared-spec/glossary.md miss; Step 5 "branch protection" 該升 GitHub Rulesets (2025).

## Decision

Task A 完成採 4 strategic choice:

1. **Phased delivery via /wbs decompose** — Phase 1 sub-plan E (enforcement real, 6 atomic step blocker) → 2a (F§1+§6+§7 ‖ H) → 2b (G ‖ F§11+§12) → 2c I → Phase 3 J (incremental Verifier per sub-plan, NOT big-bang) → Phase 4 K (Architecture Foundation Review: C4 + Strategic Domain + Spec-as-code + Living Doc, maturity 2.3 → 4.0)
2. **GitHub Rulesets (2025) 取代 legacy branch protection** — required_status_checks `vocabulary-check` + pull_request rule (no direct push main). 4 repo 一致 config, bypass none, reversible via `gh api -X DELETE /rulesets/<id>`.
3. **Portable @import = copy + staleness check** — NOT git-relative (CI 不支援 cross-repo relative path). 4 repo 各自 mirror spec-pack `01_context-scope/ubiquitous-language.md` + `scripts/check-spec-pack-staleness.sh` md5 compare warns drift.
4. **Plan storage = ephemeral global + durable ADR (混合)** — execution detail (size-budgeted sub-plan) 留 `~/.claude/plans/` (CC plan mode 預設), 設計 rationale crystallize 進 spec-pack ADR. Plan 完成即 archive, ADR 永久查閱.

## Consequences

+ enforcement 真 active (dummy PR mergeable=false 驗證, NOT 只 CI red)
+ Phase 1 E blocker → 防 F/G/H/I 建在錯地基
+ Phase 4 K 把 maturity 從 ad-hoc reorganize 升 Living Doc level (industry alignment)
+ ADR durable, plan 死後 rationale 不消失 (符合知識捕獲三層架構)
- Step 4 portable copy 引入 4 repo content duplication, 須 staleness script 機械防漂
- Phase 2a/2b 拆 micro 增加 Roy gate 次數 (vs single Phase 2)
- Plan 路徑改 `task-a-real-enforcement` 取代 CC random slug (`ancient-discovering-pillow`)

## Alternatives

- **Big-bang Phase 2 (F+G+H+I 同跑)**: F§1→G hidden dep 會 silent break, 拒 (Review #1)
- **Legacy branch protection (gh api branches/<>/protection)**: GitHub 2025 已 deprecated, Rulesets 取代, 拒 (Review #4)
- **Git-relative cross-repo @import**: CI runner 不 mount sibling repo, silent fail, 拒 (Review #3)
- **Plan 全留 spec-pack docs/plans/**: cross-repo 無 home repo, 且 ephemeral plan 污染 git history, 拒 (本 session Roy ack)

## References

- Master plan: `~/.claude/plans/task-a-real-enforcement.md`
- Sub-plan E: `~/.claude/plans/task-a-real-enforcement/E.md` (6 step + Verifier)
- Audit findings: spec-pack `docs/handoffs/2026-04-26-12-arc42-x-mod-wbs-build.md`
- ADR-000 (foundation): `99_appendix/decisions/ADR-000-spec-authority-model.md`
- /wbs skill: `~/.claude/skills/wbs/SKILL.md` (7 mechanism, context rot prevention)
