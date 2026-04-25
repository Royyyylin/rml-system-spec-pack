# firmware-spec

> Firmware-side spec (nRF52833, ble_qos_demo_V1.2m). Authority for wire/GATT contracts.
> Wire SSOT: ble_qos_demo_V1.2m/ble_api.yaml (canonical; this dir contains derived view).

## 內容

| 檔案 | 說明 |
|---|---|
| `packet_contract.md` | BLE packet contract prose (derived from ble_api.yaml) |
| `packet_diagram.d2` | Packet structure diagram (D2, AI Diagram Contract validated) |

## Cross-ref

- Wire SSOT: `ble_qos_demo_V1.2m/ble_api.yaml` (canonical — firmware wins on conflict)
- F-04 feature: `../03_building-blocks/F-04-gw-qos-scheduler-tuning/`
- Wire parity: `../06_crosscutting-integration/x1-wire-parity-spec.md`
