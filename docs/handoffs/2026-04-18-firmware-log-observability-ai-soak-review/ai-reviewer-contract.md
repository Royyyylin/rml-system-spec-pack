# AI Hourly Reviewer Contract

主檔：[README.md](README.md)

## AI Input（每小時接收）

| File | 內容 | 來源 |
|---|---|---|
| `events.jsonl` | 該時段所有 parsed events（三板合併，標 board_id） | parser |
| `timeline.jsonl` | 跨 event 的 lifecycle 序列（CMD / failover / CC relay） | parser |
| `metrics.json` | 統計摘要：event counts by family/severity、error rate、reconnect count | rule checker |
| `anomalies.jsonl` | rule checker 判定的異常列表 + alert level | rule checker |
| `raw_excerpt.log` | 異常附近的 raw RTT 片段（前後 N 行） | collector |

AI **不直接讀** hourly full raw log（可能數萬行）。只讀整理後的 bundle。

## AI Output

`ai-report.md` 必須包含：

| Section | 內容 |
|---|---|
| Overall Status | HEALTHY / DEGRADED / CRITICAL |
| Critical Findings | 需立即處理的問題 |
| Warnings | 值得注意但不緊急 |
| Timeline Summary | 本時段重要 event 序列摘要 |
| Suspected Root Cause | 若有異常，推測原因 |
| Trend vs Previous Hour | 與前一小時比較（error rate、reconnect 頻率） |
| Recommended Next Action | 需不需要人工介入、建議做什麼 |
| Raw Evidence References | 引用具體 event_seq / board_id / timestamp |

## AI 硬性限制

| 禁止 | 原因 |
|---|---|
| 把 probable pairing 寫成 confirmed truth | 跨 device 無法精確配對 |
| 宣稱跨 device ordering certainty | 無全域順序保證 |
| 把 CC relay event 當成 first-hand observation | CC 是 bridge，不是 authority |
| 自行發明未定義的 event family / code | 必須對齊 event-taxonomy.md |
| 在 report 中嵌入 raw log 全文 | 只引用 event_seq / 片段 |
| 修改 rule checker 判定結果 | AI 可補充，不可覆蓋 |

## AI Reviewer 不負責

- 不做 realtime alert（那是 rule checker 的事）
- 不修改 firmware config
- 不直接操作板子
- 不產生 wire/BLE command
- 不替代 HIL deterministic test
