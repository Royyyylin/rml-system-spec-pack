# Market Compliance Matrix — Cross-Repo Responsibility Split

> Firmware profile Kconfig SSOT: firmware repo `Kconfig` —
> `menu "Market Compliance Profile"`.
> Firmware spec detail: `ble_qos_demo_V1.2m/docs/05_verification/compliance/market-profiles/market-compliance-profiles.md`.

This file defines **which repo owns which compliance obligation** for each
standard across the three-repo system (firmware / central / app).

## Responsibility Legend

| Symbol | Meaning |
|--------|---------|
| **OWN** | Repo owns the implementation and test gate |
| **SUP** | Repo supplies data / API that another repo consumes |
| **PROC** | Company-process obligation; no code change required |
| **N/A** | Standard does not apply to this repo |

---

## Process Industry (ISA-18.2 + OPC UA A&C + ISA-62443 SL2)

| Obligation | Firmware | Central | App |
|------------|----------|---------|-----|
| Alarm priority 4-tier in data payload | **OWN** (EVT characteristic) | SUP (pass-through) | SUP (display) |
| Alarm acknowledge round-trip | **OWN** (EVT indicate + GATT ack) | **OWN** (persistence) | **OWN** (UI ack button) |
| OPC UA A&C server translation | SUP (EVT data) | **OWN** (OPC UA server) | N/A |
| ISA-62443 SL2 authenticated BLE session | **OWN** | N/A | **OWN** (pairing flow) |
| ISA-62443 SL2 audit log (event timestamps) | **OWN** (NVS ring) | **OWN** (persist + query) | SUP (display) |
| Alarm rationalization (company SOP) | PROC | PROC | PROC |

---

## Power Substation (+ IEC 61850 + IEC 62351)

| Obligation | Firmware | Central | App |
|------------|----------|---------|-----|
| IEC 61850 LN-compatible data naming | **OWN** (field naming in EVT/METRICS) | **OWN** (LN mapping layer) | N/A |
| IEC 61850 conformance test | PROC | **OWN** (server under test) | N/A |
| IEC 62351 RBAC — PEER_ROLE values | **OWN** (GATT PEER_ROLE encoding) | **OWN** (role enforcement) | **OWN** (role selection UI) |
| IEC 62351 penetration test | PROC | PROC | PROC |

---

## Railway SIL 2 (EN 50128 + EN 50155)

| Obligation | Firmware | Central | App |
|------------|----------|---------|-----|
| EN 50128 SIL 2 — requirements traceability (RTM) | **OWN** (RTM — see `--base-dir/docs/trace_map.yaml`) | **OWN** | **OWN** |
| EN 50128 — MISRA-C:2012 compliance | **OWN** (CI scan gate) | N/A | N/A |
| EN 50128 — unit test coverage ≥ 80% | **OWN** (CI coverage gate) | **OWN** | **OWN** |
| EN 50155 — watchdog + recovery | **OWN** | N/A | N/A |
| Independent Safety Assessor (ISA) | PROC | PROC | PROC |
| NSA type approval | PROC | PROC | PROC |

---

## Automotive Aftermarket (ISO 21434 + UNECE R155)

| Obligation | Firmware | Central | App |
|------------|----------|---------|-----|
| FOTA signature verification | **OWN** | SUP (key distribution) | N/A |
| Build hash in GATT DEVICE_INFO | **OWN** (already impl.) | N/A | N/A |
| Event log (CSMS audit export) | **OWN** (NVS ring) | **OWN** (CSMS API) | N/A |
| BLE session idle timeout | **OWN** (GW_CFG timeout field) | N/A | **OWN** (enforce in pairing) |
| TARA (Threat Analysis and Risk Assessment) | PROC | PROC | PROC |
| CSMS documentation for UNECE R155 | PROC | PROC | PROC |

---

## Medical Class B (IEC 62304 + IEC 60601-1 + ISO 14971)

| Obligation | Firmware | Central | App |
|------------|----------|---------|-----|
| IEC 62304 Class B — anomaly log in NVS | **OWN** | N/A | N/A |
| IEC 62304 — version traceability (git hash) | **OWN** (FW_VERSION char.) | **OWN** (fleet record) | SUP (display) |
| IEC 62304 — unit test coverage gate | **OWN** | **OWN** | **OWN** |
| ISO 14971 — risk file update per change | PROC | PROC | PROC |
| IEC 60601-1 — electrical safety (HW test) | PROC | N/A | N/A |
| ISO 13485 QMS | PROC | PROC | PROC |
| FDA 510(k) / CE MDR submission | PROC | PROC | PROC |

---

## Aerospace DAL D (DO-178C + DO-160)

| Obligation | Firmware | Central | App |
|------------|----------|---------|-----|
| DO-178C DAL D — RTM maintenance | **OWN** | **OWN** | **OWN** |
| DO-178C — code review checklist (PR gate) | **OWN** | **OWN** | **OWN** |
| DO-178C — Software Accomplishment Summary (SAS) | PROC | PROC | PROC |
| DO-160 — watchdog + power-loss-safe NVS | **OWN** (already impl.) | N/A | N/A |
| DO-160 — HW environmental qualification | PROC | N/A | N/A |
| DER / EASA DOA engagement | PROC | PROC | PROC |
| Airline LFA / STC | PROC | N/A | N/A |

---

## Semiconductor Fab (SECS/GEM + SEMI E10/E30/E37 + ISO 14644)

| Obligation | Firmware | Central | App |
|------------|----------|---------|-----|
| E10 RAM state codes in EVT payload | **OWN** (EVT characteristic payload structure) | **OWN** (GEM CEID mapping layer) | N/A |
| GEM SVID-compatible METRICS field naming | **OWN** (field naming in METRICS characteristic) | **OWN** (HSMS translation) | N/A |
| SECS-II / HSMS (E37) host connectivity | SUP (data source) | **OWN** (protocol gateway) | N/A |
| GEM conformance test (E30) | SUP (EVT/METRICS data) | **OWN** (GEM server under test) | N/A |
| ISO 14644 low-outgassing BOM review | PROC | N/A | N/A |
| ESD packaging and handling SOP | PROC | N/A | N/A |
| ISA/IEC 62443 SL 1 — authenticated pairing | **OWN** | N/A | **OWN** (pairing flow) |
| Firmware version → GEM EC SoftRev | **OWN** (FW_VERSION characteristic) | **OWN** (fleet record) | SUP (display) |

---

## Pharma GMP (FDA 21 CFR Part 11 + GAMP 5 + ISO 13485)

| Obligation | Firmware | Central | App |
|------------|----------|---------|-----|
| 21 CFR Part 11 — tamper-evident audit log (append-only) | **OWN** (NVS ring buffer, append-only) | **OWN** (persist + immutable export) | SUP (display) |
| 21 CFR Part 11 — operator ID in audit log | **OWN** (ENG_UNLOCK PIN as operator token) | **OWN** (full e-signature workflow) | **OWN** (two-factor UI) |
| 21 CFR Part 11 — timestamp synchronization audit | **OWN** (clock drift anomaly log) | **OWN** (NTP authority) | N/A |
| 21 CFR Part 11 — e-signature (reason + meaning) | PROC (hook via ENG_UNLOCK PIN) | PROC | **OWN** (full CFR workflow in UI) |
| Cold-chain excursion alert (EVT indicate) | **OWN** (already supported by EVT alarm path) | **OWN** (persist + notify) | **OWN** (excursion UI + push) |
| GAMP 5 — FRS / DS document artefacts | PROC | PROC | PROC |
| GAMP 5 — IQ / OQ / PQ validation | PROC (supplier DS + test records) | PROC | PROC |
| EU GMP Annex 11 — supplier assessment | PROC | PROC | PROC |
| ISO 14644 cleanroom class 5-8 packaging | PROC | N/A | N/A |
| Calibration records (NIST-traceable sensors) | PROC | N/A | N/A |

---

## Oil & Gas ATEX (IECEx Zone 1/2 + ATEX Cat 2/3G + API RP)

| Obligation | Firmware | Central | App |
|------------|----------|---------|-----|
| ATEX profile marker in FW_VERSION | **OWN** (version string encoding) | **OWN** (fleet gate: reject non-ATEX build to Zone 1 devices) | N/A |
| TX power cap within IECEx certified energy limit | **OWN** (QoS Zone TX power cap for ATEX build) | N/A | N/A |
| Safe-state on fatal error (TX off ≤ 100 ms) | **OWN** | N/A | N/A |
| FOTA rejection in Zone 1 (hot-work permit gate) | **OWN** (deferred; Kconfig flag only in this release) | **OWN** (hot-work permit API) | **OWN** (permit UI workflow) |
| ISA/IEC 62443 SL 1 — authenticated pairing | **OWN** | N/A | **OWN** (pairing flow) |
| ATEX-certified HW module selection | PROC | N/A | N/A |
| IECEx / ATEX Notified Body assessment | PROC | N/A | N/A |
| API RP 500 / RP 14C area classification | PROC | N/A | N/A |
| Intrinsically safe barrier (associated apparatus) | PROC | N/A | N/A |
