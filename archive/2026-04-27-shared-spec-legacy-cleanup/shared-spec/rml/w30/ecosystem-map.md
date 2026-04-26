# Ecosystem Map — W30: Fleet Broadcast + WebSocket Push

> Wave: App Wave 30 (Fleet Command Broadcast + Auto-Grouping + WebSocket Push)
> Source: `ble_qos_app/docs/plans/sections/w30-01-fleet-broadcast.md`, `w30-02-auto-grouping.md`, `w30-03-websocket-push.md`
> Dependencies: Wave 24A (device groups), Wave 29A (sync engine), Central broadcast + auto-group API

```mermaid
flowchart TB
    subgraph App["Mobile App (Flutter)"]
        BROAD["Fleet Broadcast Engine\nbatch dispatch + ack tracking\n≤100 device pages"]
        GROUPS["Auto-Group Sync\nread-only projection\nstaleness tracking"]
        WS["WebSocket Client\npush event receiver"]
        UI["Broadcast Status UI\nprogress + retry + rollback"]
    end

    subgraph Central["Central (FastAPI + PostgreSQL)"]
        BROAD_API["Broadcast API\nfleet command endpoint\nrate-limit: 1 per 30s per user"]
        GROUP_API["Auto-Group API\nserver-authoritative rules\nzone/fw-version/alert criteria"]
        WS_SERVER["WebSocket Push Server\ndevice state + alert push"]
    end

    subgraph FW["Firmware (nRF52833-DK)"]
        GW_CMD["GW Command Receiver\nprofile switch / reboot / config push"]
    end

    BROAD -- "REST batch dispatch\n≤100 devices/page" --> BROAD_API
    BROAD_API -- "forward to GW" --> GW_CMD
    GW_CMD -- "ack uplink" --> BROAD_API
    BROAD_API -- "per-device ack status" --> BROAD
    BROAD -- "display progress" --> UI

    GROUP_API -- "rules + assignments" --> GROUPS
    GROUPS -- "read-only projection\nstaleness tracking" --> App

    WS_SERVER -- "device state events\nalert push" --> WS
    WS -- "real-time update\nUI refresh" --> App
```

## Cross-Repo Actor Responsibilities (W30)

| Actor | W30 Role | Authority |
|---|---|---|
| App | fleet broadcast UX; batch dispatch; ack tracking; auto-group display; WebSocket event consumer | UX + local state |
| Central | broadcast API authority; rate-limit enforcement; auto-group rule engine (server-authoritative) | **OWNS** — command routing + group rules + push server |
| GW Firmware | command receiver; executes profile switch / reboot / config push | runtime execution |

## Key Invariants (W30)

- `confirmed` / `dispatched` / per-device `acked` are workflow milestones, **not** final-state-applied (per §1a Truth Boundary Note)
- Auto-group rules are read-only in App; server (Central) is the sole authority
- Rate limit: 1 broadcast per 30s per user; second broadcast returns error (not silently queued)
- Timeout per device: 30s; unacked devices marked as `timeout`
- Rollback command auto-generated for `profile_switch` type
