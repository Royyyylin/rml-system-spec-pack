# ADR-000: Spec Authority Model

Status: accepted
Date: 2026-04-25
Decided by: Roy (X-修正 strategic choice post-3-review)

## Context

3 strategic review (重新架構 vs reorganize / 第一性原理 / 業界 alternative) 共識:
spec-pack 純 reorganize 不足。
Roy 選 X-修正: 保留 9 PR refactor + 加 4 個 P0 artefact 升 active enforcement layer。

## Decision

spec-pack 是 **prescriptive enforcement** authority, 而非純 descriptive reference:

- 命名 violation (FEA-NNN-/F-NN- prefix, ubiquitous-language deprecated 詞) → CI block PR
- authority-map.yaml machine-readable (AI/CI 可 yaml.load() query)
- check_vocabulary_alignment.py 跨 4 repo 自動 detect drift
- Feature ID 規則: `F-NN` = firmware-led, `FEA-NNN` = cross-repo (App-led / Central-led / 4-owner)

## Consequences

+ AI agent / CI 自動 enforce vocabulary alignment, 防 drift
+ 跨 repo 改 spec 必先 register canonical list (ubiquitous-language.md)
+ 4 P0 artefact (本 ADR + authority-map.yaml + feature-design-guide + check_vocabulary): half-redesign 起點
- 工程量 +3-4 hr vs 純 reorganize
- 4 repo CI vocabulary check 是 advisory 起步, 後升 blocking

## Alternatives

- **Y (incremental)**: 砍 80% scope, 但 redesign element 完全失去 → 拒
- **X-原 (純 reorganize)**: vocabulary drift 無 enforcement → 拒

## References

- Plan: `~/.claude/plans/ancient-discovering-pillow.md` § "P0 Redesign Augmentation"
- Feature naming rule: § "命名規範" F-NN vs FEA-NNN classification
- authority-map.yaml: `01_context-scope/authority-map.yaml`
- vocabulary check (PR#5a-tools): `tools/check_vocabulary_alignment.py`
