# Upstream Evidence Audit (2026-04-15)

Scope: 確認 owner repo SSOT 到底提供哪些 age evidence，支撐 `REQ-007`（freshness basis）與 `REQ-008`（can_compare gate）。

Audit 來源：
- `ble_qos_demo_V1.2m/ble_api.yaml` (F1)
- `ble_qos_demo_V1.2m/docs/specs/data-model.md` (F2)
- `central-device-metadata/docs/specs/data-model.md` (F3)
- `ble_qos_app/docs/specs/app-scope/04-local-state.md` (F4)
- `ble_qos_app/docs/specs/app-scope/05-interface-contract.md` (F5)

詳細欄位盤點見子檔：[fields-detail.md](2026-04-15-upstream-evidence-audit/fields-detail.md)

---

## 1. 可直接用（已實作並可引用）

| 欄位 | Owner | 類型 | freshness | can_compare |
|------|-------|------|-----------|-------------|
| `updated_at` | Central | authoritative ts | yes | partial |
| `revision` | Central | version marker | partial | yes |
| `assignment_version` | Central | version marker | partial | yes |
| `last_switch_at` / `last_failover_at` | Central | authoritative ts | yes | partial |
| `failover_generation` | Firmware | version marker | partial | yes |
| `assignment_sync_state` | App | enum (existing) | partial | yes |

**REQ-007 / REQ-008 所需 age evidence 在 Central 與 Firmware 都有足夠候選欄位。** App 不需要等 upstream 新增欄位就能做保守 can_compare 判定。

## 2. 可暫用但有風險

| 欄位 | Owner | 風險 |
|------|-------|------|
| `lease_expire_at` | Central | default 超時值 open question（deferred to failover-policy.md）|
| `uptime_s` | Firmware | weak proxy；uint32 秒，~49.7 天 wrap |
| `reset_count` | Firmware | uint16 wrap；無法區分同秒 reboot |
| `GW_CFG_VERSION` | Firmware | 範圍僅限 GW_CFG 變更 |
| `profile_since` / `last_failover_generation` | App | local-only 或複本，無 threshold |

## 3. 缺欄位，需 owner repo 補 contract

**Firmware 側**（Phase 2 deferred）：
- `ts_device` / `ts_gateway` — schema 有但無 GATT 實作（F3:225-226）
- `boot_id` — 實作法 deferred（F2:244 建議複用 `reset_count`）
- `msg_seq` — 明文「尚未實作」（F2:245）

**App 側**（derived semantics 全 missing）：
- `central_reference_is_fresh` / `runtime_observation_is_fresh`
- `can_compare` / `last_synced`
- freshness window / stale_threshold（僅 prose 提到，無數值）

**一致性修補**：`updated_at` 類型分叉（F3:85 vs F3:274）、`revision` nullable 分叉、`stale_flags` 無 schema — 見子檔。

---

## Verdict

| 主題 | 現況 |
|------|------|
| Central authoritative age evidence | ✅ 足夠 |
| Firmware observation age evidence | ✅ version-based（failover_generation）；❌ wall-clock ts 等 Phase 2 |
| App derived compare semantics | ❌ 全 missing，需 App repo 補 contract |
| Freshness window 數值 | ❌ missing，需 owner 決定 |

**現有 spec-pack 文字（REQ-007 migration / REQ-008 target / AC-007）與 audit 結果一致，本輪無須再修 spec-pack wording**。

## Follow-ups（非本輪 scope）

1. **App repo**：`ble_qos_app/docs/specs/app-scope/04-local-state.md` 正式定義 `central_reference_is_fresh` / `runtime_observation_is_fresh` / `can_compare` / `last_synced`，標出 upstream 依賴
2. **Firmware repo**：Phase 2 `telemetry-schema.md` 決定 `ts_*` / `boot_id` / `msg_seq` wire 實作；在此之前 App 以 `failover_generation` + `updated_at` 為保守基準
3. **Central repo**：若 freshness window server-driven，需在 Central contract 明確聲明

## References

- `shared-spec/requirements.md` (REQ-007 / REQ-008)
- `shared-spec/feature-assignment-reconciliation.md` (FEA-004-BND-006、Comparison Evidence)
- `shared-spec/feature-telemetry-roster-visibility.md` (FEA-001-BND-007)
- `app-spec/acceptance_criteria.md` (AC-004、AC-007)
- `app-spec/test_cases.md` (TC-009、TC-012)
