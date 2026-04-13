=== FILE: docs/README.md ===
# App Display Contract 規格包入口文件

## 專案概述
本規格包定義了工業級 BLE 裝置監控 App 與 Gateway (GW) 之間的通訊合約、狀態機邏輯與驗收標準。本系統專為高利潤工業市場設計，強調高可靠性與強一致性。

## 角色導讀
- **PM / 產品經理**: 優先閱讀 `rml_lite.md` (目標與範圍) 與 `requirements.md` (功能需求)。
- **Firmware / 韌體工程師**: 優先閱讀 `state_machine.md` (狀態機)、`sequence_flows.md` (時序) 與 `packet_contract.md` (封包格式)。
- **App / 應用開發工程師**: 優先閱讀 `architecture.md` (架構) 與 `packet_contract.md` (封包解析)。
- **QA / 測試工程師**: 優先閱讀 `acceptance_criteria.md` (驗收標準) 與 `test_cases.md` (測試案例)。

## 修改流程
1. **需求變更**: 先修改 `rml_lite.md` 或 `requirements.md`，然後根據 `trace/change_rules.md` 更新下游文件。
2. **圖表變更**: 禁止直接修改 PNG。必須先修改 `trace/source_of_truth.md` 中定義的原始碼 (.mmd, .d2)，再重新渲染。
3. **追蹤更新**: 任何 ID 變更後，必須同步更新 `trace/trace_map.yaml`。

## AI 接手指南
若要讓 AI (如 Claude, ChatGPT) 接手維護，請務必同時提供以下檔案：
- `docs/rml_lite.md`
- `docs/requirements.md`
- `trace/trace_map.yaml`
- `trace/source_of_truth.md`
- `trace/change_rules.md`
