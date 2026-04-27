# Greywater Saving System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade Save Tears from a water dashboard into a greywater toilet-flushing saving system with hardware-ready data ingestion, saving statistics, student views, admin views, and AI saving plans.

**Architecture:** Extend the current FastAPI + SQLAlchemy backend in place, keeping existing authentication and room authorization. Add normalized greywater/device/plan models and APIs, then update the uni-app frontend so pages consume stable saving APIs instead of raw hardware payloads. External ThingCloud and LLM dependencies must be optional, with mock/manual/rule-based fallbacks.

**Tech Stack:** FastAPI, SQLAlchemy, SQLite/MySQL-compatible models, Python unittest, Vue 3/uni-app, TypeScript, Node test runner.

---

## File Structure

- Modify `save_tears_backend/api.py`: add database models, Pydantic models, saving calculations, greywater/device/plan/integration APIs.
- Modify `save_tears_backend/test_authz.py`: add authorization coverage for greywater and saving endpoints.
- Create `save_tears_backend/test_greywater.py`: cover greywater normalization, calculations, device APIs, ThingCloud-compatible ingestion, and fallback plan generation.
- Modify `save_tears_miniprogram/src/api/index.ts`: add frontend API wrappers and types for greywater, saving stats, devices, and saving plans.
- Modify `save_tears_miniprogram/src/utils/insights.ts`: add saving-stat helpers used by pages and unit tests.
- Modify `save_tears_miniprogram/tests/app-logic.test.mts`: add frontend logic tests for replacement-rate and plan fallback display helpers.
- Modify `save_tears_miniprogram/src/pages/home/index.vue`: convert from water overview to saving overview.
- Modify `save_tears_miniprogram/src/pages/data/index.vue`: expand data center tabs to tap water, greywater, trends, and plan.
- Modify `save_tears_miniprogram/src/pages/profile/index.vue`: rename reminder preferences to saving target and device abnormality reminders.
- Modify `save_tears_miniprogram/src/pages/admin/index.vue`: convert resident list page into saving management dashboard.
- Modify `save_tears_miniprogram/src/utils/preferences.ts`: rename preference keys while preserving defaults.

## Task 1: Backend Greywater Models And Calculations

**Files:**
- Modify: `save_tears_backend/api.py`
- Create: `save_tears_backend/test_greywater.py`

- [ ] **Step 1: Write failing backend model/calculation tests**

Create `save_tears_backend/test_greywater.py` with tests that use a temporary SQLite database, import `api`, call `initialize_database()`, seed a user and water records, then assert:

```python
def test_greywater_event_without_volume_uses_default_flush_estimate(self):
    response = self.api.create_greywater_usage(
        self.api.GreywaterUsageData(
            room_number="A101",
            usage_type="toilet_flush",
            event_count=2,
            timestamp="2026-04-27T10:00:00",
            source="manual",
        ),
        db=self.db,
        current_user=self.user,
    )
    self.assertEqual(response["data"].volume_liters, 12)
```

Also assert `calculate_saving_stats("A101", db)` returns:

```python
self.assertEqual(stats["tap_water_liters"], 30)
self.assertEqual(stats["greywater_liters"], 12)
self.assertEqual(stats["estimated_savings_liters"], 12)
self.assertAlmostEqual(stats["replacement_rate"], 12 / 42)
```

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
cd save_tears_backend
python -m unittest test_greywater.py -v
```

Expected: FAIL because `GreywaterUsageData`, `create_greywater_usage`, and `calculate_saving_stats` do not exist.

- [ ] **Step 3: Implement minimal models and calculation helpers**

In `api.py`, add:

```python
DEFAULT_GREYWATER_LITERS_PER_FLUSH = int(os.getenv("SAVE_TEARS_GREYWATER_LITERS_PER_FLUSH", "6"))
GREYWATER_USAGE_TYPES = {"toilet_flush", "cleaning", "other"}
GREYWATER_SOURCES = {"device", "manual", "mock"}
```

Add SQLAlchemy models:

```python
class GreywaterDeviceDB(Base):
    __tablename__ = "greywater_devices"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(80), unique=True, index=True)
    room_number = Column(String(20), index=True)
    device_type = Column(String(50), default="toilet_flush_sensor")
    status = Column(String(20), default="offline")
    last_seen_at = Column(String(50))
    source_platform = Column(String(50), default="thingcloud")
    metadata_json = Column(String)


class GreywaterUsageDB(Base):
    __tablename__ = "greywater_usage"
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(20), index=True)
    device_id = Column(String(80), index=True)
    usage_type = Column(String(30), default="toilet_flush")
    event_count = Column(Integer, default=1)
    volume_liters = Column(Integer)
    source = Column(String(20), default="manual")
    timestamp = Column(String(50))
    raw_payload_json = Column(String)
```

Add Pydantic model:

```python
class GreywaterUsageData(BaseModel):
    room_number: str
    usage_type: str = "toilet_flush"
    event_count: int = 1
    volume_liters: int | None = None
    timestamp: str
    source: str = "manual"
    device_id: str | None = None
    raw_payload: dict | None = None
```

Add helpers `normalize_usage_type`, `normalize_source`, `estimate_greywater_volume`, and `calculate_saving_stats`.

- [ ] **Step 4: Run tests and verify GREEN**

Run:

```bash
cd save_tears_backend
python -m unittest test_greywater.py -v
```

Expected: PASS.

## Task 2: Backend APIs, Authorization, And Fallback Saving Plans

**Files:**
- Modify: `save_tears_backend/api.py`
- Modify: `save_tears_backend/test_authz.py`
- Modify: `save_tears_backend/test_greywater.py`

- [ ] **Step 1: Write failing API tests**

Add tests for:

```python
def test_regular_user_cannot_read_other_room_greywater(self):
    status, _ = self.request_json("GET", "/greywater_usage/B202", headers=self.auth_headers("alice", "pw"))
    self.assertEqual(status, 403)

def test_thingcloud_event_creates_usage_and_updates_device(self):
    status, body = self.request_json("POST", "/integrations/thingcloud/events", {
        "device_id": "GW-A101-001",
        "room_number": "A101",
        "event_type": "toilet_flush",
        "event_count": 1,
        "timestamp": "2026-04-27T10:30:00",
        "source": "device",
    }, headers=self.auth_headers("admin", "secret"))
    self.assertEqual(status, 200)
    self.assertEqual(body["data"]["volume_liters"], 6)
```

Add a direct unit test that `generate_rule_based_saving_plan("A101", db)` returns a plan with `model_name == "rule_fallback"` and measurable targets.

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
cd save_tears_backend
python -m unittest test_authz.py test_greywater.py -v
```

Expected: FAIL because routes and plan helper are missing.

- [ ] **Step 3: Implement routes**

Add authenticated endpoints:

```python
@api_router.post("/greywater_usage")
@api_router.get("/greywater_usage/{room_number}")
@api_router.get("/greywater_summary/{room_number}")
@api_router.get("/saving_stats/{room_number}")
@api_router.post("/devices")
@api_router.get("/devices")
@api_router.get("/devices/{device_id}")
@api_router.post("/integrations/thingcloud/events")
@api_router.post("/integrations/thingcloud/sync")
@api_router.post("/saving_plans/{room_number}/generate")
@api_router.get("/saving_plans/{room_number}/latest")
@api_router.get("/saving_plans/{room_number}")
```

Rules:
- Use `ensure_room_access` for room-scoped user data.
- Use `get_admin_user` for device listing and ThingCloud sync.
- Normalize `event_type` to `usage_type`.
- Preserve unknown raw payload in JSON text.
- Implement `SavingPlanDB` and rule fallback generation before LLM API wiring.

- [ ] **Step 4: Run backend tests**

Run:

```bash
cd save_tears_backend
python -m unittest test_authz.py test_production_basics.py test_greywater.py -v
```

Expected: PASS.

## Task 3: Frontend API Types And Insight Helpers

**Files:**
- Modify: `save_tears_miniprogram/src/api/index.ts`
- Modify: `save_tears_miniprogram/src/utils/insights.ts`
- Modify: `save_tears_miniprogram/tests/app-logic.test.mts`

- [ ] **Step 1: Write failing frontend logic tests**

Add tests that import new helpers from `src/utils/insights.ts`:

```ts
test('buildSavingOverview computes replacement rate and savings', () => {
  const overview = buildSavingOverview({
    tapWaterLiters: 30,
    greywaterLiters: 12,
    flushCount: 2,
  });
  assert.equal(overview.estimatedSavingsLiters, 12);
  assert.equal(overview.replacementRateLabel, '29%');
});
```

Also test empty data returns `0%` and safe labels.

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
cd save_tears_miniprogram
npm run test:unit
```

Expected: FAIL because `buildSavingOverview` and new API types do not exist.

- [ ] **Step 3: Implement API wrappers and helpers**

Add TypeScript interfaces:

```ts
export interface GreywaterUsageRecord { id?: number; room_number?: string; device_id?: string; usage_type: 'toilet_flush' | 'cleaning' | 'other'; event_count: number; volume_liters: number; source: 'device' | 'manual' | 'mock'; timestamp: string; }
export interface SavingStats { tap_water_liters: number; greywater_liters: number; estimated_savings_liters: number; replacement_rate: number; flush_count: number; trends?: Array<{ label: string; tap_water_liters: number; greywater_liters: number; replacement_rate: number }>; }
export interface SavingPlan { plan_text: string; target_flush_count: number; target_replacement_rate: number; estimated_savings_liters: number; model_name: string; created_at?: string; status?: string; }
```

Add wrappers:

```ts
export const getGreywaterUsage = (roomNumber: string) => callApi(`/greywater_usage/${roomNumber}`);
export const getSavingStats = (roomNumber: string) => callApi(`/saving_stats/${roomNumber}`) as Promise<SavingStats>;
export const generateSavingPlan = (roomNumber: string) => callApi(`/saving_plans/${roomNumber}/generate`, 'POST');
export const getLatestSavingPlan = (roomNumber: string) => callApi(`/saving_plans/${roomNumber}/latest`) as Promise<SavingPlan>;
export const getDevices = () => callApi('/devices');
```

Add `buildSavingOverview`.

- [ ] **Step 4: Run frontend unit tests and typecheck**

Run:

```bash
cd save_tears_miniprogram
npm run test:unit
npm run type-check
```

Expected: PASS.

## Task 4: Student Frontend Saving Experience

**Files:**
- Modify: `save_tears_miniprogram/src/pages/home/index.vue`
- Modify: `save_tears_miniprogram/src/pages/data/index.vue`
- Modify: `save_tears_miniprogram/src/pages/profile/index.vue`
- Modify: `save_tears_miniprogram/src/utils/preferences.ts`

- [ ] **Step 1: Write or update frontend tests for tab and preference helpers**

Extend `tests/app-logic.test.mts` to cover saving overview helpers and preference defaults:

```ts
test('saving reminder preferences default to enabled', () => {
  const prefs = normalizeResidentPreferences({});
  assert.equal(prefs.savingTargetRemindersEnabled, true);
  assert.equal(prefs.deviceAbnormalityAlertsEnabled, true);
});
```

- [ ] **Step 2: Run tests and verify RED**

Run `npm run test:unit`; expected failure for missing helper/preference names.

- [ ] **Step 3: Update pages**

Update page copy and data loading:
- Home title becomes `节水概览`.
- Load `getSavingStats` and `getLatestSavingPlan` with existing tap-water/water-quality fallbacks if APIs fail.
- Data center tabs become `自来水`, `灰水`, `趋势`, `计划`.
- Profile toggles become `节水目标提醒` and `设备异常提醒`.

- [ ] **Step 4: Verify frontend**

Run:

```bash
cd save_tears_miniprogram
npm run test:unit
npm run type-check
```

Expected: PASS.

## Task 5: Admin Saving Management Dashboard

**Files:**
- Modify: `save_tears_miniprogram/src/pages/admin/index.vue`
- Modify: `save_tears_miniprogram/src/api/index.ts`
- Modify: `save_tears_miniprogram/src/utils/insights.ts`

- [ ] **Step 1: Write failing admin overview helper tests**

Add `buildSavingAdminOverview` tests for total tap water, total greywater, average replacement rate, low replacement-rate rooms, and offline devices.

- [ ] **Step 2: Run tests and verify RED**

Run `npm run test:unit`; expected failure for missing helper.

- [ ] **Step 3: Implement admin dashboard**

Use existing admin auth behavior, but change content from resident list to:
- total tap-water usage,
- total greywater usage,
- estimated savings,
- average replacement rate,
- total flushing count,
- room ranking,
- low-use warnings,
- device status list.

First implementation may compose from available `/users`, `/saving_stats/{room}`, and `/devices` calls.

- [ ] **Step 4: Verify frontend**

Run:

```bash
cd save_tears_miniprogram
npm run test:unit
npm run type-check
```

Expected: PASS.

## Task 6: End-To-End Verification And Documentation Update

**Files:**
- Modify: `README.md`
- Modify: `save_tears_backend/README.md`

- [ ] **Step 1: Run full backend verification**

Run:

```bash
cd save_tears_backend
python -m unittest test_authz.py test_production_basics.py test_greywater.py -v
```

Expected: PASS.

- [ ] **Step 2: Run full frontend verification**

Run:

```bash
cd save_tears_miniprogram
npm run test:unit
npm run type-check
```

Expected: PASS.

- [ ] **Step 3: Update docs**

Document:
- greywater positioning,
- mock/manual/device data sources,
- ThingCloud payload shape,
- LLM fallback behavior,
- new local demo flow.

- [ ] **Step 4: Final status check**

Run:

```bash
git status --short
```

Expected: only intentional implementation and documentation files are modified.
