# Context Map — W26A: Shift Reporting & Dashboard Customization

> Wave: App Wave 26A
> Source: `w26-01-shift-reports.md`, `w26-02-dashboard-customization.md`

## Bounded Contexts

```mermaid
C4Context
    title W26A Bounded Contexts

    Person(sup, "Field Supervisor", "8-12 hour shift handoff use case")
    Person(eng, "Engineer", "dashboard customization")

    Enterprise_Boundary(app_ctx, "App Domain") {
        System(report_engine, "Report Aggregation Engine", "isolate-based\nalert + telemetry aggregation")
        System(report_ui, "Report UI", "card-based preview\nplain-text export")
        System(dash, "Dashboard Customization", "widget add/remove/reorder\nApp-local preference")
        System(local_db, "Local Cache DB", "alert event log\n+ telemetry history")
    }

    Enterprise_Boundary(central_ctx, "Central Domain") {
        System(rest, "REST Metadata API", "revision-based sync\n(existing channel)")
    }

    Rel(sup, report_ui, "trigger + view report")
    Rel(eng, dash, "customize dashboard layout")
    Rel(report_engine, local_db, "query time window")
    Rel(report_ui, report_engine, "request generation")
    Rel(rest, local_db, "sync alert + telemetry data")
```

## Context Relationships

| Upstream | Downstream | Relationship | Contract |
|---|---|---|---|
| Central REST API (existing) | App Local Cache | Customer/Supplier | revision-based sync; no W26A changes |
| App Local Cache | Report Aggregation Engine | Internal | DB query by time window + device filter |
| Report Aggregation Engine | Report UI | Internal | `ShiftReport` domain model |
| Report UI | Clipboard | External System | plain-text structured output |

## Anti-Corruption Layers

| Boundary | ACL Description |
|---|---|
| Report Engine → UI Thread | Engine runs in isolate; result is passed as immutable `ShiftReport` object to main thread |
| App → Central | W26A does NOT add Central API endpoints; report data is 100% App-local during generation |

## Dependency on Prior Waves

| Prior Wave | Dependency | Nature |
|---|---|---|
| Wave 25A §1 (alert event log) | W26A report pulls alert summary | Must exist before W26A report can run |
| Wave 25A §2 (telemetry history) | W26A report pulls trend highlights | Must exist before W26A report can run |
