# Data Layout & Phases

主檔：[README.md](README.md)

## Data Layout

```
logs/
├── raw/{board_id}/{YYYY-MM-DDTHH}.log       ← hourly rotated raw RTT
├── parsed/{YYYY-MM-DDTHH}/
│   ├── events.jsonl                          ← all boards merged, tagged
│   └── timeline.jsonl                        ← lifecycle sequences
└── analysis/{YYYY-MM-DDTHH}/
    ├── metrics.json                          ← counts, rates, stats
    ├── anomalies.jsonl                       ← rule checker output
    └── ai-report.md                          ← AI reviewer output
```

`board_id` 建議用 `gw-{snr}` / `ed-{snr}` / `cc-{snr}`，其中 `snr` 為 J-Link serial number。

## Event Format Requirement（Phase 1 目標）

每條 `[EVT]` 必須包含：

| Field | Required | 說明 |
|---|---|---|
| `family` | yes | BOOT / BLE_LINK / ROSTER / FAILOVER / CMD / CC_RELAY / UPLINK |
| `code` | yes | e.g. BLE_LINK_UP / BOOT_OK |
| `role` | yes | GW / ED / CC |
| `device_id` | yes | stable short id |
| `boot_id` | yes | NVS reset_count or equivalent |
| `uptime_ms` | yes | device local elapsed |
| `event_seq` | yes | per-device per-boot monotonic |
| `severity` | yes | DEBUG / INFO / WARN / ERROR / FATAL |
| `peer_id` | optional | peer addr / slot |
| `reason_code` | optional | HCI reason / CMD reject |
| `correlation_id` | optional | txn_id / relay_id / failover_generation |
| `payload` | optional | bounded key-value（≤ 8 keys） |

Bounded payload — 不允許任意長 JSON 或 free-form dump。

## Phases

| Phase | 名稱 | 內容 | 改 firmware？ |
|---|---|---|---|
| **0** | Spec / Plan Freeze | 本文件 + 邊界定義 | 否 |
| **1** | Structured `[EVT]` | 33 條 tag 改 key=value + 必要欄位 | 是（小改） |
| **2** | Multi-board Collector | 同時收 GW/ED/CC RTT，hourly rotation | 否（host script） |
| **3** | Parser + Rule Checker | raw → JSONL，硬規則判錯 | 否（host script） |
| **4** | AI Hourly Reviewer | 讀 bundle，輸出 ai-report.md | 否（AI prompt） |
| **5** | App / Central Integration | 事件接進 App view / Central audit | 之後再定 |

## Open Questions

| # | Question |
|---|---|
| 1 | `board_id` / `device_id` mapping 怎麼管理？手動 config 還是 auto-detect from RTT？ |
| 2 | 多 J-Link serial number 如何配置？同時 3 板需要 3 個 `rtt_log.py` process |
| 3 | AI reviewer 用 Claude Code / Codex / local model？ |
| 4 | Hourly window 是 30m / 60m / 2h？ |
| 5 | Raw log retention 保留幾天？ |
| 6 | Alert 輸出到 Telegram / file / Central API？ |
| 7 | Phase 1 structured `[EVT]` 是否等 event-log-contract Phase 0 一起做？ |
