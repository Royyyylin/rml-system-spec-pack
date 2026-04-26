# 04_runtime-view

> arc42 §6 — Runtime 行為：CMD_V2 / cache / HA / reconnect 時序圖
> Status: active (6 sequence diagrams migrated to arc42 structure PR#3)

## 內容

| 檔案 | 說明 |
|---|---|
| `seq-cmd-v2-success.md` | CMD_V2 success path sequence |
| `seq-cmd-v2-reject-tune-val.md` | CMD_V2 reject (TUNE-VAL violation) sequence |
| `seq-cmd-v2-reject-busy.md` | CMD_V2 reject (busy) sequence |
| `seq-cache-invalidation-3tier.md` | 3-tier cache invalidation sequence |
| `seq-ha-failover.md` | HA failover sequence |
| `seq-ed-reconnect.md` | ED reconnect sequence |

Note: BDD/Gherkin scenarios → `05_quality-acceptance/bdd-scenarios.md` (NOT this chapter).

## 對應業界 reference

- arc42 §6 Runtime View
- C4: Dynamic diagram

## Cross-ref

- 上層: README.md
- 鄰章: 03_building-blocks/ (structure), 05_quality-acceptance/ (acceptance)
