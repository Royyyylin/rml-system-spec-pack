# 03_building-blocks

> arc42 §5 — Cross-repo feature contracts 與 session topology
> Status: skeleton (PR #3 填內容, PR #4 rename/fractal split)

## 預期內容 (PR #3 fill + PR #4 rename)

- FEA-001-*.md: Feature contract (cross-repo, app-led)
- FEA-002-*.md: Feature contract (cross-repo, central-led)
- FEA-003-*.md: Feature contract (cross-repo)
- FEA-004-*/: Feature contract (fractal split, ≥3 sub-artifacts)
- F-04-*/: Feature contract (firmware-led, fractal split)
- session-topology.d2: BLE session topology diagram

## 命名規則

- FEA-NNN: cross-repo feature (App-led / Central-led / 平等 4-owner)
- F-NN: firmware-initiated AND firmware runtime behavior 為主 (legacy F-04)

## 對應業界 reference

- arc42 §5 Building Block View
- C4: Component diagram (Level 3)
- DDD: Aggregate, Domain Service

## Cross-ref

- 上層: README.md
- 下層: FEA-NNN-*.md, F-04-*/INDEX.md, session-topology.d2
- 鄰章: 02_solution-strategy/ (strategy), 04_runtime-view/ (sequence)
