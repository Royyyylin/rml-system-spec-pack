<!-- A2 research dump from 8 sub-agent fan-out, 2026-04-24 -->

# Finding 03 — NCS v3.3.0 新 Opcode + Sample 調查

## Sub-Agent 任務描述

調查 NCS v3.3.0 及 SDC (SoftDevice Controller) 的新 opcode、
新增 sample 程式，評估對 A2 架構的相關性，
並確認 Channel Survey 功能在各版本的支援狀態。

---

## Key Findings

### NCS v3.3.0 新 Opcode

- **0xfd20**（VS_Conn_Event_Extend）：連線事件延伸控制
- **0xfd22**（VS_Conn_Event_Trigger）：連線事件觸發控制
- **A2 相關性**：這兩個 opcode 與 A2 QoS 架構**無直接關係**，屬於 Nordic vendor-specific 低階控制，不在 A2 設計範圍內。

### NCS v3.2.0 新增 Sample（A2 高度相關）

v3.2.0 是 A2 METRICS/CONTROL 層最有價值的版本，新增 3 個關鍵 sample：

#### Sample 1: `rssi_power_control`
- 功能：展示 LE Power Control（BT Core 5.2+）的 RSSI-based TX power 自動調整
- A2 相關性：**高** — METRICS 層 RSSI 量測 + POLICY 層 TX power 決策的參考實作

#### Sample 2: `path_loss_monitoring`
- 功能：展示 Path Loss Monitoring（BT Core 5.2+），基於路徑損耗分區自動切換 TX power zone
- A2 相關性：**高** — A2 POLICY 層 channel quality 評估的直接參考

#### Sample 3: `ble_shorter_conn_intervals`
- 功能：展示 7.5ms 以下（最短至 3ms）連線 interval 的使用
- A2 相關性：**中** — A2 CONTROL 層 interval 調整邊界驗證

### Channel Survey 版本演進

| 版本 | Channel Survey 狀態 | 最小 Interval |
|------|-------------------|--------------|
| v2.9.2 | Experimental | 7.5ms |
| v3.2.0 | **Supported（正式支援）** | **3ms** |
| v3.3.0 | Supported | 3ms |

- **重要**：v3.2.0 將 Channel Survey 從 Experimental 升為正式 Supported，且最小 interval 從 7.5ms 降至 3ms。
- 無 channel survey / event length runtime demo（無可直接複用的完整 sample）。

---

## 業界 Reference

| 文件 | URL |
|------|-----|
| SDC CHANGELOG | https://github.com/nrfconnect/sdk-nrfxlib/blob/main/softdevice_controller/CHANGELOG.rst |
| NCS 3.2.0 Release Notes | https://docs.nordicsemi.com/bundle/ncs-3.2.0/page/nrf/releases_and_maturity/releases/release-notes-3.2.0.html |

---

## 對 A2 架構的影響

- **v3.2.0 是 A2 最佳升級目標**：Channel Survey 正式支援 + 3ms interval + 兩個 QoS 相關 sample。
- v3.3.0 的新 opcode（0xfd20/0xfd22）對 A2 無用，但會帶來額外 breaking change（BC-1/BC-2，見 finding-02）。
- rssi_power_control 和 path_loss_monitoring sample 可直接作為 A2 METRICS/POLICY 層的程式碼參考。

## 對我們系統的影響

- **鎖定 NCS v3.2.0**：取得 Channel Survey 正式支援 + 3ms interval 能力 + 2 個關鍵 sample，同時避免 v3.3.0 的 Zephyr 4.4 breaking change（BC-1/BC-2）。
- Channel Survey 從 Experimental 升為 Supported 是 A2 INGEST 層的關鍵依賴，v3.2.0 是最低安全版本。
