# BDD Scenarios — BLE QoS Demo 系統行為場景

> **Status: deferred** — Gherkin scenarios (arc42 §10 / BDD). NOT event-storming (Brandolini EventStorming ≠ Gherkin).
> renamed from: bdd-flows.md (semantic correction per Reconciliation Table, PR#3).
> 本文定義 8 個核心 BDD 場景（Given/When/Then），供 `/spec-bdd` 執行時對照驗證。
> 角色定義見 [../01_context-scope/ubiquitous-language.md](../01_context-scope/ubiquitous-language.md)；REQ 編號見 [requirements.md](requirements.md)。

---

## Scenario 1：配對 / 綁定

```gherkin
Scenario: 首次配對並綁定 ED 到 GW
  Given App 尚未完成任何 BLE pairing
    And 目標 nRF52833 DK 處於 UNPROVISIONED 狀態
  When App 掃描並選擇目標裝置，完成 BLE Pairing（LESC）
    And App 透過 Config GATT Service 寫入 role = APP_ROLE_END_DEVICE
  Then Firmware 將 role 寫入 NVS 並重啟
    And App 收到 role 確認後顯示「綁定成功」
    And Central 建立裝置身份記錄
```

**Trace**: REQ-001（裝置身份建立）

---

## Scenario 2：斷線重連

```gherkin
Scenario: ED 斷線後自動重連 GW
  Given ED 已連線至 GW（network_id 已匹配）
    And ED 處於 connected 狀態
  When 無線干擾導致 BLE link loss（超過 supervision timeout）
  Then ED 進入 scanning 狀態，以 exponential backoff 重試
    And ED 掃描到 network_id 匹配的 GW advertisement
    And ED 重新建立連線並回復 connected 狀態
    And GW 更新 ED roster 連線狀態
```

**Trace**: REQ-006（BLE 連線生命週期）

---

## Scenario 3：OTA 韌體升級（F-05 placeholder）

```gherkin
Scenario: 透過 App 對 ED 執行 OTA 韌體升級
  Given ED 已連線至 GW
    And Central 已驗證 OTA image 簽章
  When App 觸發 OTA update flow
    And GW 轉發 DFU packet 至目標 ED
  Then ED 接收完整 image 並驗證 CRC
    And ED 重啟進入新韌體，版本號更新
    And App 顯示升級成功
```

**Trace**: [TBD-link-to-future-REQ]（F-05 OTA，尚未建立 REQ）

---

## Scenario 4：GW Failover（HA Promotion）

```gherkin
Scenario: GW-A 心跳超時後 GW-B 接管
  Given GW-A 為 active GW，GW-B 為 standby
    And Central 正常接收 GW-A 心跳
  When GW-A 停止心跳超過 holddown threshold
    And CC bridge 偵測到 GW-A 連線中斷
  Then Central 評估 GW-B 的 failover eligibility
    And Central 發送 promotion 指令至 GW-B
    And GW-B 接管 ED roster 並成為 active GW
    And App 顯示 active GW 切換通知
```

**Trace**: REQ-007（HA failover 及 assignment reconciliation）

---

## Scenario 5：Telemetry 上報

```gherkin
Scenario: ED 持續上報 telemetry 至 Central
  Given ED 已連線至 GW（connected 狀態）
    And GW 已建立 Central uplink
  When ED 的 telemetry timer 觸發（週期由 ble_api.yaml 定義）
  Then ED 透過 GATT notification 發送 telemetry packet 至 GW
    And GW 聚合並透過 uplink 轉發至 Central
    And Central 寫入資料庫並更新時間戳
```

**Trace**: REQ-003（Telemetry roster visibility）

---

## Scenario 6：告警觸發

```gherkin
Scenario: ED 量測值超過閾值後觸發告警
  Given ED 正常上報 telemetry
    And Central 已設定 ED 的告警閾值
  When ED 量測值連續超過閾值（次數由配置決定，非硬編碼）
  Then Central 產生 alert event 並寫入 audit log
    And App 收到 push notification 顯示告警內容
    And 告警狀態在 App 介面高亮顯示
```

**Trace**: [TBD-link-to-future-REQ]（Alert threshold，尚未建立 REQ）

---

## Scenario 7：Role 切換

```gherkin
Scenario: 操作員將已配對裝置從 ED 切換為 GW
  Given 裝置目前 NVS role = APP_ROLE_END_DEVICE
    And App 已獲得 Engineering unlock 授權
  When App 透過 Config GATT Service 寫入 role = APP_ROLE_GATEWAY
  Then Firmware 將新 role 寫入 NVS（requires_reboot = true）
    And 裝置重啟後以 GW 角色啟動 BLE advertising
    And Central 更新裝置 capability 記錄
    And App 顯示 role 切換完成
```

**Trace**: REQ-001（裝置身份建立 / role 管理）

---

## Scenario 8：Engineering Unlock

```gherkin
Scenario: 操作員透過 Engineering unlock 進入進階調整模式
  Given App 處於一般操作員模式
    And 裝置已完成配對
  When 操作員輸入正確的 engineering unlock code
  Then App 解鎖進階功能（role 切換 / QoS preset 手動覆蓋）
    And Central audit log 記錄 unlock 事件（含 operator ID 與時間戳）
    And Unlock session 在逾時後自動失效
```

**Trace**: [TBD-link-to-future-REQ]（Engineering unlock，授權機制待定 REQ）

---

## 附錄：場景對應矩陣

| # | Scenario | Trace REQ | Stage Gate |
|---|----------|-----------|------------|
| 1 | 配對 / 綁定 | REQ-001 | Roy smart review |
| 2 | 斷線重連 | REQ-006 | Roy smart review |
| 3 | OTA 升級 | TBD (F-05) | 等 F-05 REQ 建立 |
| 4 | GW Failover | REQ-007 | Roy smart review |
| 5 | Telemetry 上報 | REQ-003 | Roy smart review |
| 6 | 告警觸發 | TBD | 等 alert REQ 建立 |
| 7 | Role 切換 | REQ-001 | Roy smart review |
| 8 | Engineering Unlock | TBD | 等 unlock REQ 建立 |

---

*版本：2026-04-23 | 適用 SDLC Stage：BDD（Stage 1）*
