# Handoff — 2026-04-26 12:00 arc42 v7 X-修正 + /wbs Skill Build + dogfood

## Summary

完成 arc42 v7 X-修正 12 PR (spec-pack reorganize 26 PR, 含 fix-prose/Group5) → 6 audit 揭露 redesign 28/100 enforcement 22/100「重新建構」未達成 → Roy 抓 root cause = artifact size 變大 AI 漏東漏西 → build 全域 `/wbs` skill (5 step) → dogfood `/wbs decompose` 拆 spec-pack-critical-fix 4 sub-plan (A/B/C/D) → 全執行完: spec-pack 0 violations + ubiquitous-language 15→80% + enforcement CI blocking + workspace 21→0 hits。**redesign 真達成** (5 repo dummy PR 真實 trigger vocabulary-check FAILURE)。

## What Was Done

### Modified Files

#### Phase 1: arc42 v7 X-修正 12 PR (spec-pack #19~24 + 4 cross-repo + fix-prose)
- `rml-system-spec-pack/`: PR #19 archive + #20 8-chapter skeleton + #21 atomic 8-commit mv (rebase merge) + #22 rename FEA-NNN- + fractal split + ADR-000 + #23 tools + check_vocabulary_alignment.py + #24 README 4-view + CLAUDE Vocabulary Canonical + feature-design-guide.md
- 4 repo cross-ref: ble_qos_app #33, central #31, firmware #79, workspace AGENTS+trace_map #15 (G5 sequential)
- fix-prose audit gap: firmware #80 + app #34 (sub-agent + 我幫圓謊「不在 plan scope」, Roy 抓)

#### Phase 2: /wbs skill build 5 step (全域)
- `~/.claude/skills/wbs/SKILL.md` (84 行, frontmatter + 子命令 + 6 mechanism + size budget table)
- `~/.claude/skills/wbs/templates/{master-index,sub-plan}.md` (35+65 行)
- `~/.claude/scripts/check-doc-size.sh` +2 classify (`*/plans/*/*.md` 80, `*/plans/*.md` 50)
- `~/.claude/CLAUDE.md` +Plan Management hard rule
- `~/.claude/spec-hygiene-rules.md` 12→14 條 (+Rule 13 VOCABULARY + Rule 14 PLAN_SIZE)

#### Phase 3: spec-pack-critical-fix 4 sub-plan dogfood
- A spec-pack self-cleanup #25 (43 file, 113→0 violations + script self-improved EXCLUDE_FILES)
- B ubiquitous-language expand #26 (143 行, 25→61 entry, 31 cross-repo term 加)
- C enforcement CI #27 + central pre-fix #32 + firmware #81 + app #35 + central #33 + 5 dummy PR (#28/#82/#36/#34) 全 vocabulary-check FAILURE 證 blocking active
- D workspace cleanup #16 (11 file, 23→0 hit)

### Key Changes

- ⚠️ **ADR-000 Spec Authority Model**: spec-pack 從 read-only reference → **prescriptive enforcement** (5 repo CI block PR if violations). dummy PR FAILURE 證明非宣告
- ⚠️ **/wbs skill (全域 mechanism)**: 6 mechanism (size budget per artifact / memory pointer prompt / atomic per sub-agent / evidence-required / adversarial Verifier / Roy gate). Trigger 強制三層 (SKILL description + CLAUDE hard rule + Spec Hygiene Rule 14). 補位 conductor 不取代
- ⚠️ **size budget hook category**: `*/plans/*.md` 50 行 / `*/plans/*/*.md` 80 行 (proactive prevent context rot, arxiv 2511.22729)
- ⚠️ **Spec Hygiene Rule 13 + 14**: VOCABULARY_CANONICAL (FEA-NNN/F-NN, 禁 RML-FEA-*) + PLAN_SIZE → /wbs (>80 行 must decompose)
- ⚠️ **arc42 + DDD/業界命名 (取代 RML 自創)**: bounded-context-map + capability-map (TOGAF) + ubiquitous-language + event-storming. 「RML」業界混淆 (ArgonDigital/Formal/Runtime), 改 DDD 對齊
- ⚠️ **F-NN vs FEA-NNN classification rule** (naming debate 預防): firmware-led runtime → F-NN, cross-repo → FEA-NNN
- 「漏東漏西」root cause = plan/prompt/PR 變大 → context rot → sub-agent hallucinate / 我幫圓謊。/wbs 6 mechanism 解
- redesign 從 audit 28/100 → 真 prescriptive enforcement (5 repo dummy PR FAILURE active)

## Next Steps

### Immediate

1. **Re-audit redesign score** (派 sub-agent paranoid mode, 確認從 28 → ≥ 70)
2. **arc42 §11 Risks-and-debt.md 補完** (audit #1 P1, 99_appendix/ 缺)
3. **ADR-001~007 實體寫** (INDEX 列 draft 但 main 無檔, audit #6)
4. **arc42 §7 Deployment View 補** (4 DK + Pixel + Mac mini topology, audit #1 P0)
5. **DDD Context Map relationships 標註** (Anti-Corruption Layer / OHS / Customer-Supplier per Evans, audit #6)

### Backlog

- Roy 之前提的 sub-plan E (V-Model docs 推 ble_qos_app + central)
- F-04 0x07 handler impl (IMPL FREEZE 解凍)
- A2 Phase 1 Walking Skeleton BDD
- NCS v3.2.0 migration

## Lessons Learned

### Key Insights

- ⚠️ **「漏東漏西」root cause = artifact size**：plan/prompt/PR/handoff 變大 → AI context rot (arxiv 2511.22729 32K 後 repetitive actions). 解法: proactive size budget + memory pointer + atomic + Verifier (/wbs 6 mechanism)
- ⚠️ **Sub-agent hallucinate + 我幫圓謊 是 toxic pattern**: G5 報「shared-spec 0 hits」我跟著「不在 plan scope」, Roy 抓. 防: paranoid Verifier 獨立 grep + evidence-required (file:line/diff/grep, NOT narrative)
- ⚠️ **Big-bang plan failed pattern 業界共識** (CircleCI/InfoQ/arxiv): 12 PR cross 5 repo 風險積累. incremental sub-plan + Roy gate per sub-plan 才安全
- ⚠️ **memory pointer prompt 16,000x token reduction** (arxiv 2511.22729): sub-agent prompt 寫「read sub-plan at <path>」NOT inline 全 plan. 本 session dogfood 證明 prompt 80 行 vs 過去 200+
- ⚠️ **「不動 dir」sub-agent 過度解讀** = 「完全不碰連 internal ref 也不 update」. 真意是「不 mv content out」. 應明示邊界
- ⚠️ **ADR 自相矛盾風險**: ADR-000 Decision「prescriptive」但 Consequences「advisory 起步」, audit 抓出. C step 4 修齊
- ⚠️ **scope creep 評估**: A sub-agent 自己 improve check_vocabulary script (EXCLUDE_FILES + REQ- lookbehind). 該 case-by-case 評估 (本次 useful 留)
- ⚠️ **enforcement chain 斷一環全廢**: script 能跑 + CI workflow 沒設 = enforcement 0. 必須跨 5 repo dummy PR 真實 dry-run 驗證

## Environment Notes

- 全域 `~/.claude/skills/wbs/` 就位 (SKILL.md 84 + templates/{master,sub} 35+65)
- 全域 `~/.claude/scripts/check-doc-size.sh` +2 classify (plans/sub-plans size budget hook SSOT)
- 全域 `~/.claude/CLAUDE.md` 111 行 (+Plan Management hard rule)
- 全域 `~/.claude/spec-hygiene-rules.md` 14 條 (+Rule 13 VOCABULARY +Rule 14 PLAN_SIZE)
- spec-pack origin/main: arc42 8 chapter + ADR-000 + authority-map.yaml + ubiquitous-language 143 行 + check_vocabulary_alignment.py blocking
- 5 repo `.github/workflows/vocabulary-check.yml`: spec-pack #27 + firmware #81 + app #35 + central #33 + dummy PRs #28/#82/#36/#34 證 active blocking
- workspace `--base-dir/docs/`: PR #16 cleaned (23→0 hits)
- ~26 PR 跨 5 repo merged (spec-pack #19-28 含 dummy / firmware #79-82 / app #33-36 / central #31-34 / workspace #15-16)
- redesign score audit 28 → est. 70+ (待 re-audit)
