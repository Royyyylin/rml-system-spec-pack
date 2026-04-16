# Page 4 — Evidence panel 設計原則

主檔：[README.md](README.md)　Mock：[04-evidence-panel.html](04-evidence-panel.html)

## 定位

- Page 4 是 evidence detail 層，但**第一屏先給人話結論與建議**，不是工程 dump
- raw / internal 欄位（`updated_at` / `observed_at` / `revision` / `can_compare` / `mismatch_field`）一律下移到 Engineering details 折疊區
- 仍維持 Central canonical vs Runtime observed 邊界，不做等權合併

## 第一屏（human-first）

每個情境都顯示這幾件事：

1. **狀態**：`Conflict` / `Not compared` / `Central only`
2. **一句結論**（中文）
3. **建議處理**（一句）
4. **三條「為什麼」**：
   - Central：幾秒前確認 / 上次同步 / 缺資料
   - Runtime：幾秒前觀測 / 尚未回報
   - 比對結果：可比對 / 不可比對 + 短原因

## 後段資訊分層

5. **Central evidence card**（藍底）：上層人話一句；下層折疊 Engineering details rows
6. **Runtime evidence card**（橘底）：同樣上層人話；下層折疊 raw rows
7. **Engineering details · Compare gate**（紫色 ENG tag，預設收合）：露 internal `can_compare` / `reason` / `mismatch_field`
8. **Recent evidence**：3 條短句（時間 + 人話），不再用 internal key 主導
9. **Action confirmation hint**：簡化成一句，「執行高風險動作前，會要求工程師確認、填寫原因，並留下 audit record。」

## Compare gate 在各情境的真值

| 情境 | can_compare | reason | mismatch_field |
|------|-------------|--------|----------------|
| Conflict | true | both sides fresh | gateway |
| Not compared | false | stale Central reference | — |
| Central only | **false** | missing runtime evidence | — |

修正：Central only 缺 Runtime 證據，**沒有兩側可比，所以 cannot compare**；之前 mock 寫成 Can compare 是錯的。

## 不在本頁做

- 不做 full log viewer / JSON dump
- 不串真正動作 / 真正 modal；本輪是 mock
- 不發明 wire field 或新 protocol
- 不在第一屏放 raw key
