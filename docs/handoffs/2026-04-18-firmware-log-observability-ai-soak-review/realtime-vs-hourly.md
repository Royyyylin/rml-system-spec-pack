# Realtime Rule Checker vs Hourly AI Review

主檔：[README.md](README.md)

## 為什麼分兩層

| 層 | 工具 | 職責 | 回應時間 |
|---|---|---|---|
| **Realtime** | Rule checker（deterministic script） | 硬規則判錯，立即 alert | 秒級 |
| **Hourly** | AI reviewer（Claude / LLM） | 摘要、歸因、趨勢、疑似問題 | 小時級 |

類似工業 historian + alarm + periodic analytics：alarm 先響，工程師再看報表。

## 為什麼 AI 不應持續 tail raw RTT

| 問題 | 說明 |
|---|---|
| Context 爆 | RTT 每秒數十行，AI context window 數分鐘就滿 |
| 成本高 | 持續佔 context = 持續消耗 token |
| Noise 高 | 大部分 log 是正常 heartbeat / topology，不需 AI 看 |
| 長跑不穩 | Claude Code Monitor 最長 1 小時，soak test 要跑數天 |
| 硬規則更穩 | event_seq gap、FATAL 這類用 grep/script 判更可靠 |

## Realtime Rule Checker Scope

| Rule | 觸發條件 | Alert 等級 |
|---|---|---|
| Parse failure | `[EVT]` 行格式錯誤 | WARN |
| Missing required field | family / code / role / event_seq 缺失 | WARN |
| `event_seq` gap | 同 device 同 boot 內 seq 不連續 | ERROR |
| Unexpected reboot | `boot_id` 變更但前一 boot 無 graceful shutdown event | ERROR |
| FATAL / ERROR severity | 任何 `severity=FATAL` 或 `severity=ERROR` | CRITICAL / ERROR |
| BLE_LINK_DOWN storm | 同一 peer 在 N 分鐘內斷線 > M 次 | WARN |
| CMD timeout | CMD_RECEIVED 後 T 秒未出 CMD_APPLIED / CMD_FAILED | WARN |
| CC subscribe timeout | CC_GW_FOUND 後 T 秒未出 CC_SUBSCRIBE_OK | WARN |
| QOS_HEARTBEAT gap | heartbeat 間隔 > 2× expected interval | WARN |
| Topology inconsistency | GW peers count 與實際 BLE_LINK_UP 數量不符 | WARN |
| RTT collector down | 某 board 的 log 停止輸入超過 threshold | ERROR |

## Hourly AI Reviewer Scope

- 讀 rule checker 產出的 metrics / anomalies + parsed events
- 判斷：本時段整體是否正常
- 歸因：異常的可能原因
- 趨勢：與前幾小時比較（error rate 上升？reconnect 增加？）
- 建議：需不需要人工介入
- **不重複做 rule checker 已做的硬判斷**
