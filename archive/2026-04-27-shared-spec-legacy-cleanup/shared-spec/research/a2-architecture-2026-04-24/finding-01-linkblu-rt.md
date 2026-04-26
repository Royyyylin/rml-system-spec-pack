<!-- A2 research dump from 8 sub-agent fan-out, 2026-04-24 -->

# Finding 01 — LinkBlu RT 真實性深查

## Sub-Agent 任務描述

驗證「LinkBlu RT」是否為現實存在的產品或技術。對該名稱進行 8 輪 WebSearch，
並找出最可能的真實對應參考。

---

## Key Findings

- **8 輪 WebSearch 零命中**：無任何結果顯示「LinkBlu RT」作為 BLE 即時調度產品存在。
- **名稱不存在**：不存在對應的公司、產品頁、datasheet、GitHub repo 或學術論文以「LinkBlu RT」為名。
- **3 個最可能的真實來源**（名稱相似或功能描述吻合）：

### 真實參考 1 — RT-BLE（IEEE Infocom 2023，學術論文）

- 特徵完全吻合：即時 BLE 調度、多連線 QoS、干擾躲避
- 論文作者：Rui Li et al.，發表於 IEEE INFOCOM 2023
- 最可能是「LinkBlu RT」的學術原型來源
- **Source**: https://www.liborui.cn/publication/12-infocom23-rt-ble/12-infocom23-rt-ble.pdf

### 真實參考 2 — Blecon（Nordic 官方合作夥伴，商業產品）

- 定位：工業 deterministic BLE，Nordic 官方 partner 認證
- 功能：BLE 確定性傳輸，類似「RT BLE」定位
- 與 nRF 生態系深度整合
- **Source**: https://www.blecon.net/partners/nordic-semiconductor

### 真實參考 3 — LinkBluCon（Ambrosia Systems，醫療 CGM）

- 產品：連續血糖監測（CGM）BLE 橋接器
- 命名混淆來源：「Link」+「Blu」組合巧合相符
- 與 A2 QoS 架構無關，僅為名稱混淆
- **Source**: https://www.ambrosiasys.com

---

## 業界 Reference

| 名稱 | 類型 | URL |
|------|------|-----|
| RT-BLE (IEEE Infocom 2023) | 學術論文 | https://www.liborui.cn/publication/12-infocom23-rt-ble/12-infocom23-rt-ble.pdf |
| Blecon (Nordic partner) | 商業產品 | https://www.blecon.net/partners/nordic-semiconductor |
| LinkBluCon (Ambrosia) | 醫療 CGM | https://www.ambrosiasys.com |

---

## 對 A2 架構的影響

- A2 無法從「LinkBlu RT」借鑑實作，因為該產品不存在。
- RT-BLE 論文可作為 A2 POLICY 層演算法設計的學術參考。
- Blecon 的商業模式（deterministic BLE-as-a-service）可作為 A2 定位的競品分析參考。

## 對我們系統的影響

- **報告中的 LinkBlu RT 引用需被修正**：應改引 RT-BLE 論文或 Blecon，避免引用不存在的產品。
- 無法參考 LinkBlu RT 的實作細節，A2 須從頭設計或以 RT-BLE 論文為出發點。
- 確認 A2 為業界首個多維度 BLE QoS 即時調度開源實作（見 finding-04）。
