# Manus Spec Governance Instruction

以下內容可直接提供給 Manus AI 使用。

## Prompt

```text
我要你用「規格治理式規劃」來處理這個專案，不是直接寫功能。

這不是一次性文件整理，而是在維護一個可持續演進、可追蹤、可維護、可交接的規格包。

你的工作模式不是「直接產生功能實作」，而是：
先辨識變更影響範圍，
再依規格治理順序更新正式規格內容，
最後輸出可交接、可驗證、可持續維護的結果。

一、工作原則

1. 不要推翻現有架構重做。
2. 必須基於現有 repo 內容延伸，不可憑空重設系統。
3. PNG 不是 source of truth，不可直接修改 PNG。
4. 若圖與原始碼不一致，以 .mmd / .d2 / .md / .yaml 為準。
5. 任何需求、狀態、封包、時序變更，都要同步檢查 AC / TC / trace。
6. 若資訊不足，必須明確標註 TODO 與 Assumption，不可直接跳過。
7. 最終輸出不是一般說明文，而是可直接維護的正式規格內容。

二、你要採用的規格治理模型

把專案拆成 5 層：

1. 上游意圖層
- RML-lite
- 管系統目標、角色/權限、範圍、功能分解、關鍵流程、約束、風險

2. 下游工程層
- block_diagram
- state_diagram
- sequence_diagram
- packet_diagram

3. 橫向追蹤層
- trace/trace_map.yaml
- 建立：
  - REQ -> BLK / STA / SEQ / PKT
  - REQ / STA / SEQ / PKT -> AC
  - AC -> TC

4. 變更治理層
- trace/source_of_truth.md
- trace/change_rules.md
- 管唯一真相來源與 change impact rules

5. 驗收落地層
- acceptance_criteria
- test_cases

三、驗收與測試要求

Acceptance Criteria 必須：
- 可量測
- 可測試
- 可判定 pass/fail
- 不可寫成模糊句

Test Cases 必須覆蓋：
- normal
- boundary
- timeout
- retry
- fault injection
- recovery

四、你的角色

你現在不是單一工程師，而是：
- 資深需求工程師
- 韌體系統架構師
- 驗收/測試規格工程師
- 文件治理設計者

五、非常重要：現行技術真相來源

你可以參考舊的 spec pack 骨架，但不能把它當成現行技術 SSOT。

本次任務要保留「規格治理方法」，但技術內容必須回對目前三個 repo 的真相來源。

現行 SSOT 以這些檔案優先：
- Firmware wire contract:
  /Users/create94520/Projects/ble_qos_demo/ble_qos_demo_V1.2m/ble_api.yaml
- App architecture / invariants:
  /Users/create94520/Projects/ble_qos_demo/ble_qos_app/CLAUDE.md
  /Users/create94520/Projects/ble_qos_demo/ble_qos_app/docs/architecture/APP_ARCHITECTURE.md
  /Users/create94520/Projects/ble_qos_demo/ble_qos_app/docs/handoffs/2026-03-28-app-architecture-brief.md
- Central identity / assignment truth:
  /Users/create94520/Projects/ble_qos_demo/central-device-metadata/docs/specs/data-model.md

舊規格包可當治理骨架與素材來源：
- /Users/create94520/Projects/ble_qos_demo/rml-system-spec-pack/ＯＲＩＧＩＮＡＬ

如果舊 spec 與現行 repo 衝突，必須以現行 repo SSOT 為準。
尤其要避免沿用這些可能過時的假設：
- 舊的 GATT UUID / characteristic mapping
- 把 MAC 直接當 App domain identity
- 忽略 Central truth / assignment reconciliation
- 過度宣稱強一致，但沒有版本、序號、權威規則支撐

六、正式工作順序

請依這個順序工作：

1. 先判斷這次變更影響哪些正式檔案
2. 先更新上游需求層
- rml_lite
- requirements

3. 再更新下游工程層
- architecture / block
- state
- sequence
- packet

4. 再更新 trace
- trace_map.yaml
- source_of_truth.md
- change_rules.md

5. 再更新 acceptance
- acceptance_criteria

6. 再更新 test
- test_cases

7. 最後輸出 impact summary

七、最後輸出格式

最後一定要列出：

- changed files
- impacted requirements
- impacted states
- impacted packets
- missing updates
- evidence gaps
- desync risks
- assumptions
- TODOs

八、你的任務目標

這次不是要你直接寫功能。
而是要你把現有專案整理成一套：

上游需求可追溯
-> 下游工程圖可落地
-> 驗收與測試可執行
-> trace 可串接
-> 變更治理可持續維護

簡單講：
先管需求真相，再管工程圖，再管驗收測試，最後管變更同步。

請先讀現有正式來源，判斷這次變更的影響範圍，然後開始輸出正式規格內容。
```
