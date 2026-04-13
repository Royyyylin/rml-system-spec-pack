# STEP 3 — 文件骨架與示例內容 (Part 3)

## 7. docs/acceptance_criteria.md
```markdown
# 驗收標準 (Acceptance Criteria)

| ID | Related REQ | Preconditions | Trigger | Observable Result | Timing Bound | Pass Condition | Fail Condition | Measurement Method |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AC-001** | REQ-001 | App 已連線至 GW。 | GW 發送 STATUS 封包。 | L2 詳情頁顯示正確 RSSI 與 Zone。 | 500ms | 顯示值與封包內容一致。 | 顯示值為空或與封包不符。 | 封包模擬器比對 UI。 |
| **AC-002** | REQ-002 | 裝置處於 Active 狀態。 | 點擊 Enter Maintenance。 | 狀態變更為 Maintenance。 | 5s | 狀態成功轉移且 UI 更新。 | 狀態未轉移或 UI 顯示錯誤。 | 手動操作測試。 |
```

## 8. docs/test_cases.md
```markdown
# 測試案例 (Test Cases)

| ID | Related AC | Test Type | Setup | Steps | Expected Result | Logs / Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-001** | AC-001 | Normal | App 連線至模擬 GW。 | 1. 模擬器發送 RSSI -56dBm, Zone MID。<br>2. 觀察 App L2 頁面。 | L2 顯示 `-56 dBm` 與 `MID`。 | App Log: `Received STATUS 0x2A1D: RSSI=-56, Zone=1` |
| **TC-002** | AC-002 | Fault Injection | App 連線至模擬 GW。 | 1. 點擊 Enter Maintenance。<br>2. 模擬器不回傳 ACK。<br>3. 觀察 App 重試行為。 | App 重試 3 次後顯示 `Sync Failed`。 | App Log: `Retry 1/3... Retry 2/3... Retry 3/3... Timeout` |
```

## 9. trace/trace_map.yaml
```yaml
# Traceability Map (REQ -> Artifacts -> AC -> TC)

requirement_to_artifacts:
  REQ-001: [BLK-001, PKT-001]
  REQ-002: [STA-001, SEQ-001]

requirement_to_acceptance:
  REQ-001: [AC-001]
  REQ-002: [AC-002]

requirement_to_tests:
  REQ-001: [TC-001]
  REQ-002: [TC-002]

state_to_sequences:
  STA-001: [SEQ-001]
  STA-003: [SEQ-002]

packet_to_sequences:
  PKT-001: [SEQ-001]

change_impact_rules_reference:
  - trace/change_rules.md
```
