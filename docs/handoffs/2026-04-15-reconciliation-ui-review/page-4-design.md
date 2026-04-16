# Page 4 — Evidence panel 設計原則

主檔：[README.md](README.md)　Mock：[04-evidence-panel.html](04-evidence-panel.html)

## 定位

- Page 4 是 evidence detail 層，不是主操作頁
- 由 Page 3「View evidence」進入；raw timestamp / revision / observed_at 在這裡可以攤開
- 仍維持 Central canonical vs Runtime observed 邊界，不做等權合併

## 資訊分層

1. **Summary card**：state badge + 一句結論 + compare gate（Can compare / Cannot compare）+ recommended action
2. **Central evidence card**（藍底）：assigned gateway / source / owner / sync age / revision / updated_at
3. **Runtime evidence card**（橘底）：observed gateway / source path / observed age / observed_at / event source
4. **Compare gate card**（中性灰）：可顯示 internal key（`can_compare` / `reason` / `mismatch_field`）— evidence 層允許
5. **Recent evidence timeline**：限 3–5 條短事件（時間 + src + 摘要），不做 full log viewer
6. **Action confirmation hint**：說明 Page 3 的 dangerous action 在實際執行時需要 Engineer role / confirmation / reason / audit

## 切換情境

- Conflict：兩側 fresh、值不同；can_compare = true；建議 Recover runtime
- Not compared：Central reference stale；can_compare = false；建議 Refresh Central
- Central only：Runtime evidence 缺；can_compare = true 但 mismatch_field = —；建議 Wait for runtime / Send check command

## 不在本頁做

- 不做 full log viewer / JSON dump
- 不串真正動作 / 真正 modal；本輪是 mock
- 不發明 wire field 或新 protocol
