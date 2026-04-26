# Capability Matrix — W26A: Shift Reporting & Dashboard Customization

> Wave: App Wave 26A
> Source: `w26-01-shift-reports.md`, `w26-02-dashboard-customization.md`

## Per-Role Capabilities

| Capability | App | Central | GW Firmware |
|---|---|---|---|
| Shift report data model | **OWNS** — `ShiftReport`, `ReportSection` Dart models | — | — |
| Report aggregation engine | **OWNS** — queries local alert + telemetry DB in isolate | — | — |
| Time window selection UI | **OWNS** — 4h/8h/12h/custom range picker | — | — |
| Top-N alerting device ranking | **OWNS** — count desc, severity, time tie-break | — | — |
| Telemetry highlights (RSSI/PDR/latency/offline duration) | **OWNS** — peak/trough per device per window | — | — |
| Status transition log | **OWNS** — online↔offline timestamps from cache | — | — |
| Plain-text clipboard export | **OWNS** — structured text for messaging apps | — | — |
| Alert event log (data source) | consumes (cached) | **OWNS** — source via REST sync | — |
| Telemetry history DB (data source) | consumes (cached) | **OWNS** — source via REST sync | produces |
| Dashboard widget layout | **OWNS** — local preference, persisted App-side | — | — |
| Custom metric widgets | **OWNS** — add/remove/reorder | — | — |

## Authority Boundaries (W26A)

| ID | Boundary |
|---|---|
| `W26A-BND-001` | App owns report generation logic — Central does not compute or serve pre-built reports in W26A |
| `W26A-BND-002` | Report data sources are locally cached; no direct online query during report generation |
| `W26A-BND-003` | Dashboard layout is App-local preference — not synchronized to Central or shared across devices |
| `W26A-BND-004` | Telemetry metrics included: RSSI / PDR / latency / offline duration only (per W26A §1a1 deterministic output rules) |

## Out of Scope (W26A)

- Cloud sync or Central API upload of reports
- Email or remote delivery of reports
- Scheduled/automatic report generation
- Custom report templates
- Central schema changes for dashboard preferences
