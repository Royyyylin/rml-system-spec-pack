# Firmware Runtime Log Observability / AI Soak Review

**Status**：`phase-0-plan`（不寫 code，只定 spec/plan）
**Date**：2026-04-18

## Purpose

用 GW / ED / CC 三塊板子的 structured firmware log 驗證韌體是否正常運作。支援 long-running soak test（數小時至數天）+ AI hourly review。不取代 deterministic rule checker — 規則先判硬錯，AI 做摘要、歸因、趨勢。

## Architecture

```
GW RTT ─┐
ED RTT ─┼─> multi-board collector ─> hourly raw logs ─> parser
CC RTT ─┘                                                 ↓
                                              events.jsonl / timeline.jsonl
                                                           ↓
                                                    rule checker
                                                           ↓
                                       metrics.json / anomalies.jsonl / alerts
                                                           ↓
                                                AI hourly reviewer
                                                           ↓
                                                    ai-report.md
```

## Three-Board Responsibilities

| Board | Event Families | 重要性 |
|---|---|---|
| **GW** | BOOT / BLE_LINK / ROSTER / FAILOVER / CMD / UPLINK | runtime QoS + ED coordination 主要來源 |
| **ED** | BOOT / BLE_LINK / CMD / optional FAILOVER observation | device-side measurement + own link 來源 |
| **CC** | BOOT / BLE_LINK / CC_RELAY / CC-side CMD relay | Central-side bridge — App ↔ GW path evidence |

CC 不可宣稱 assignment / runtime truth；CC 只是 bridge/relay evidence。

## Relationship to F-04

- **獨立 domain** — 不是 F-04 scheduler tuning 的一部分
- F-04 之後可用 CMD family event 驗證 `SET_SCHED_TUNE` lifecycle
- 不得因本文件阻塞 FW-2 `ble_api.yaml`
- 不得把 scheduler tuning payload 和 log observability payload 混在一起

## Detail Files

- [ordering-and-correlation.md](ordering-and-correlation.md)
- [realtime-vs-hourly.md](realtime-vs-hourly.md)
- [ai-reviewer-contract.md](ai-reviewer-contract.md)
- [data-layout-and-phases.md](data-layout-and-phases.md)
