# Page 2 — Peer overview 設計原則

主檔：[README.md](README.md)　Mock：[02-detail-summary.html](02-detail-summary.html)

## 主畫面

- Main：peer operational overview（health / connections / short events）
- 巡視人員看 quick health；Engineer 多看 deeper diagnostics（jitter / throughput / PHY / TX Power / compare gate 摘要）
- Reconciliation 仍是 exception flow，只有 conflict 才浮出 banner
- Role switcher 為 mock 閱讀層，參考 app repo 既有 `normal / maintenance / engineer`，本輪先收斂為兩層
- Page 2 以 Gateway / End Device 為主；`Central Bridge` 僅為 Central-side path 的特殊路徑示意，非一般巡視入口
- Gateway 視角採 overview + expandable members / bridge 結構（accordion），點開才顯示個別 ED 或 bridge 的短摘要

## Update strategy（4 層）

mock 假設不是所有區塊同頻率更新，與現有 app contract / firmware SSOT 對齊：

- **overview**：~2s polling（STATUS）—— Gateway overview / 收合 ED 列
- **expanded detail**：notify-driven，UI ~1s 節流（METRICS_V2）—— 只在「展開中且正在看的項目」發生
- **event/log/alarm**：event-driven（EVT）—— conflict banner、recent events（弱化 collapsible；conflict 時關鍵事件會在 overview 下方先露一條）
- **static / semi-static**：on open 或 30s（DEVICE_INFO）/ 手動 refresh（FW_VERSION / CAPS_V2 / ROSTER / alias）

不把 50–100ms 級的更新搬進手機主 flow。

Runtime 主畫面只顯示 **freshness / quality 結果**（「最後更新 2s 前」/「即時」/「資料較舊」/「目前無法比對」/`Online` / `Alive` / `Degraded` / `Offline`），不在畫面上出現 polling / notify / event-driven / acquisition cycle 這類機制細節——即使收合也不行。

## Freshness 用詞分層

為避免後續頁面混用，Page 2 採以下一致規則（Page 3 / 4 沿用）：

- **最後更新**：runtime / live observation（Gateway、ED page-level health sub）
- **上次同步**：Central / bridge / sync reference（Central Bridge、sync status 類）
- **最後看到**：member item / accordion 內 ED 列
- 時間一律用中文 `X 前`（不用 `X ago`）
