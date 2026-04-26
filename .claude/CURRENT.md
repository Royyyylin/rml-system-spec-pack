# CURRENT — rml-system-spec-pack

最後更新：2026-04-26

## 進度快照

- **arc42 v7 X-修正 全 12 PR merged** (#19~#28 spec-pack + 4 cross-repo PR for vocabulary CI)
  - 8 chapter (00_introduction-goals / 01_context-scope / 02_solution-strategy / 03_building-blocks / 04_runtime-view / 05_quality-acceptance / 06_crosscutting-integration / 99_appendix)
  - DDD/業界命名 (取代 RML 自創): bounded-context-map / capability-map (TOGAF) / ubiquitous-language / event-storming
  - FEA-NNN- prefix + F-04 fractal split (FEA-001~004 + F-04 + extension-boundary)
  - ADR-000 Spec Authority Model (prescriptive enforcement)
  - authority-map.yaml (machine-readable, P0 X-修正 #2)
  - feature-design-guide.md (P0 X-修正 #3)
  - check_vocabulary_alignment.py blocking exit 1 (P0 X-修正 #4)
- **spec-pack-critical-fix 4 sub-plan 全完成** (`/wbs decompose` dogfood):
  - A spec-pack self-cleanup #25 (113→0 violations)
  - B ubiquitous-language expand #26 (15→80% canonical, 25→61 entry)
  - C enforcement CI #27 (5 repo dummy PR FAILURE 證 active blocking)
  - D workspace cleanup #16 (23→0 hits)
- **/wbs skill 全域 build** (`~/.claude/skills/wbs/`, 6 mechanism, 補位 conductor)

## 下一步（按優先序）

1. **Re-audit redesign score** (從 28/100 → ≥ 70 確認)
2. arc42 §11 risks-and-debt.md 補完 (99_appendix/)
3. ADR-001~007 實體寫 (INDEX 列 draft 但 main 無檔)
4. arc42 §7 Deployment View 補 (4 DK + Pixel + Mac mini topology)
5. DDD Context Map relationships 標註 (Anti-Corruption Layer / OHS / Customer-Supplier per Evans)
6. sub-plan E V-Model docs 推 ble_qos_app + central
7. F-04 0x07 handler impl / A2 Phase 1 BDD / NCS v3.2.0

## 已知問題 / 待回收

- redesign 從 audit 28/100 升 (預估 ≥70, 待 re-audit verify)
- ADR-001~007 INDEX 列但實體未寫 (P1 backlog)
- §7 Deployment View / §11 Risks 完全跳 (audit P0)
- sub-agent hallucinate + AI 幫圓謊 toxic pattern → /wbs 6 mechanism 已解
- App / Firmware / Central V-Model 5 章 docs 未推 (sub-plan E backlog)

## 環境備註

- 全域 `~/.claude/skills/wbs/` 就位 (SKILL.md 84 + templates/{master,sub})
- 全域 `~/.claude/scripts/check-doc-size.sh` +2 classify (plans/sub-plans size budget)
- 全域 `~/.claude/CLAUDE.md` 111 行 +Plan Management hard rule
- 全域 `~/.claude/spec-hygiene-rules.md` 14 條 (+Rule 13 VOCABULARY +Rule 14 PLAN_SIZE)
- 5 repo `.github/workflows/vocabulary-check.yml` 全 active blocking
- spec-pack origin/main commit `1bb8cdd` (vocabulary blocking active)

## 主要 handoff 入口

- `docs/handoffs/2026-04-26-12-arc42-x-mod-wbs-build.md` — 本次 EOD (arc42 v7 + /wbs + sub-plan A/B/C/D)
- `docs/handoffs/2026-04-15-upstream-evidence-audit.md` — 較早 SSOT evidence 盤點
