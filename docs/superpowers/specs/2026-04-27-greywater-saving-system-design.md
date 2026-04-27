# Save Tears Greywater Saving System Design

## Status

This document captures the approved product direction for evolving Save Tears from a basic water-data dashboard into a campus greywater saving system. It defines the first implementation scope, backend and database direction, frontend page changes, ThingCloud integration strategy, and LLM-based saving plan behavior.

## Product Positioning

Save Tears is a campus dormitory greywater saving system. The hardware side collects greywater flushing and water-usage data, while the software side receives, stores, analyzes, and visualizes that data. The product goal is to help students understand how much tap water they use, how much greywater replaces tap water, and what actions can reduce waste.

The product is not positioned as a dormitory property management system. It should avoid drifting into unrelated property workflows such as repair tickets, announcements, occupancy management, or general room administration unless those workflows directly support water saving.

## Users

The system serves two user groups.

Students use the system to understand their dormitory's daily water usage, greywater usage, greywater flushing behavior, saving progress, and suggested next actions.

Administrators use the system to understand overall water-saving performance, greywater replacement rate, room-level differences, device data status, and abnormal usage patterns.

## First-Version Scope

The first version focuses on greywater toilet flushing because it is common in dormitory life, easy to understand, and easy to quantify. A single greywater flushing event can be converted into estimated tap-water savings even before the hardware team provides precise flow values.

The system should still support non-flushing greywater usage. For the first version, supported greywater usage categories are:

- `toilet_flush`: the primary scenario.
- `cleaning`: dormitory or public-area cleaning.
- `other`: a flexible category for data that does not fit the first two categories.

The first version should not include irrigation as a primary category because it is unlikely to match the dormitory usage scenario.

## Hardware And Data Source Strategy

The expected hardware direction is:

`sensor / greywater device -> ThingCloud -> Save Tears backend -> database -> frontend`

The frontend should not connect directly to ThingCloud. The backend should be the integration layer because it can protect credentials, normalize unstable hardware payloads, and keep frontend code independent from future hardware-platform changes.

Because the hardware team's final data format is not confirmed, the software design should support multiple data sources:

- `device`: data from ThingCloud or a connected greywater device.
- `manual`: manually entered correction or fallback data.
- `mock`: demonstration data for testing and presentations.

The backend should normalize different hardware payloads into a stable internal greywater usage record. The frontend should depend only on the normalized API, not on raw ThingCloud payloads.

## Data Types To Support

The hardware may eventually provide different kinds of data. The software should be designed to accept:

- Greywater flushing events, such as "device X recorded one greywater flush".
- Greywater volume, such as "this event used 6L of greywater".
- Device status, such as water tank level, online status, last upload time, or abnormal state.

The first version can calculate estimated savings from event count when precise volume is unavailable. When real flow data becomes available, the system should prefer measured volume over estimated volume.

## Core Student Functions

Student-facing functions should emphasize behavior change, not only data display.

- Daily saving overview: tap-water usage, greywater usage, greywater flushing count, estimated water saved, and greywater replacement rate.
- Greywater usage records: records grouped by scenario, with flushing as the default view.
- Trends: tap-water trend, greywater trend, and greywater replacement-rate trend by day, week, or month.
- Saving target: a clear daily or weekly target, such as target flushing count or target replacement rate.
- Ranking and achievement feedback: room-level saving ranking, replacement-rate ranking, and simple progress feedback.
- AI saving plan: a generated plan based on recent water and greywater data.

## Core Admin Functions

Admin-facing functions should show whether the greywater saving system is working across rooms or buildings.

- Overall saving dashboard: total tap-water usage, total greywater usage, estimated water saved, average greywater replacement rate, and total greywater flushing count.
- Room comparison: rooms with strong saving performance, low greywater usage, high tap-water usage, or abnormal behavior.
- Greywater scenario analysis: flushing, cleaning, and other usage distribution.
- Device data status: device identifier, bound room, last upload time, online or offline status, and source health.
- Abnormal reminders: device with no recent data, unusually high tap-water usage, unusually low greywater replacement rate, and sudden drop in greywater flushing count.

## AI Saving Plan Direction

The AI saving plan is a major product feature. It should not be a generic fixed reminder. The backend should calculate structured water-saving context first, then send that summary to an LLM API.

The intended flow is:

`database statistics -> backend saving profile -> LLM API -> saved saving plan -> frontend display`

The frontend must not call the LLM API directly because API keys and prompt logic should remain on the backend.

The LLM should not query the database directly. The backend should pass a structured summary, such as weekly tap-water change, greywater replacement rate, flushing count, cleaning usage, target progress, and anomalies. The LLM's job is to turn this summary into a readable and actionable saving plan.

Example plan content:

- Current weekly tap-water usage compared with the previous week.
- Current greywater replacement rate.
- Recommended greywater flushing target for the next seven days.
- Cleaning-related greywater suggestion when relevant.
- Estimated tap-water savings if the plan is completed.

## Database Design

The existing database should be extended instead of replaced. The current `water_flow` table can continue to represent tap-water usage records. New greywater and AI-plan tables should be added around it.

### `greywater_devices`

Stores hardware devices that may send greywater data through ThingCloud.

- `id`: internal primary key.
- `device_id`: external hardware or ThingCloud device identifier.
- `room_number`: dormitory room bound to the device.
- `device_type`: device category, such as `toilet_flush_sensor`.
- `status`: `online`, `offline`, or `warning`.
- `last_seen_at`: last known upload time.
- `source_platform`: external platform name, such as `thingcloud`.
- `metadata_json`: optional raw device metadata for future fields.

### `greywater_usage`

Stores normalized greywater usage events. All hardware, manual, and mock inputs should be converted into this shape.

- `id`: internal primary key.
- `room_number`: room associated with the event.
- `device_id`: optional hardware device identifier.
- `usage_type`: `toilet_flush`, `cleaning`, or `other`.
- `event_count`: number of usage events, usually flushing count.
- `volume_liters`: greywater volume. If precise flow data is unavailable, this can be estimated.
- `source`: `device`, `manual`, or `mock`.
- `timestamp`: event time.
- `raw_payload_json`: optional original ThingCloud or device payload for debugging.

### `saving_plans`

Stores generated AI or fallback saving plans so the frontend can display stable saved plans instead of regenerating every time.

- `id`: internal primary key.
- `room_number`: room the plan belongs to.
- `period_start`: plan period start.
- `period_end`: plan period end.
- `plan_text`: human-readable saving plan.
- `target_flush_count`: recommended greywater flushing target.
- `target_replacement_rate`: recommended greywater replacement-rate target.
- `estimated_savings_liters`: expected tap-water savings if the plan is completed.
- `model_name`: LLM model used, or `rule_fallback` for rule-based plans.
- `created_at`: generation time.
- `status`: `active` or `archived`.

## Backend API Design

The backend should expose stable saving APIs that hide whether data came from ThingCloud, manual entry, or mock data.

### Greywater APIs

- `POST /greywater_usage`: create a normalized greywater record. This supports manual records, mock records, and device-normalized records.
- `GET /greywater_usage/{room_number}`: list greywater records for one room. Regular users can only access their own room; admins can access any room.
- `GET /greywater_summary/{room_number}`: return greywater totals, flushing count, usage distribution, and recent records.

### Saving Statistics APIs

- `GET /saving_stats/{room_number}`: return tap-water total, greywater total, estimated saved water, greywater replacement rate, flushing count, and trend data.
- Admin users may request room-level comparisons across all rooms through a future dashboard endpoint, but first implementation can compute admin overview from existing room summaries.

### Device APIs

- `POST /devices`: create or update a greywater device binding.
- `GET /devices`: list devices for administrators.
- `GET /devices/{device_id}`: inspect one device's status and latest data.

### ThingCloud Integration APIs

- `POST /integrations/thingcloud/events`: receive pushed ThingCloud or hardware events.
- `POST /integrations/thingcloud/sync`: trigger a backend pull from ThingCloud. In the first version this can be implemented as a mock-compatible integration point until the hardware team confirms real API fields.

### AI Saving Plan APIs

- `POST /saving_plans/{room_number}/generate`: calculate the saving profile, call the LLM when configured, save the generated plan, and return it.
- `GET /saving_plans/{room_number}/latest`: return the active latest plan.
- `GET /saving_plans/{room_number}`: return historical plans.

## Calculation Rules

The first implementation should use clear and explainable formulas.

- Tap-water usage comes from existing `water_flow` records. The current `flow_rate` value should be treated as liters for display and first-version statistics.
- Greywater usage comes from `greywater_usage.volume_liters`.
- If a greywater event has no `volume_liters`, estimate it as `event_count * DEFAULT_GREYWATER_LITERS_PER_FLUSH`.
- `DEFAULT_GREYWATER_LITERS_PER_FLUSH` should default to 6L and be configurable later.
- Estimated tap-water saved equals greywater volume for first-version calculations, because each liter of usable greywater is treated as replacing one liter of tap water.
- Greywater replacement rate is `greywater_liters / (tap_water_liters + greywater_liters)`.
- Daily, weekly, and monthly statistics should be grouped from event timestamps.

## Frontend Page Design

The frontend should be upgraded in place instead of adding many disconnected pages. Existing navigation can remain recognizable, but the wording and content should focus on saving behavior.

### Student Home: Saving Overview

The current "water overview" should become "saving overview". It should show:

- Today's tap-water usage.
- Today's greywater usage.
- Today's greywater flushing count.
- Estimated tap-water saved.
- Greywater replacement rate.
- Daily saving target progress.
- Latest AI saving-plan summary.

### Data Center: Saving Data

The current tabs should expand from water, bill, and water quality into saving-centered views:

- `Tap Water`: existing tap-water usage trend and records.
- `Greywater`: greywater flushing, cleaning, and other records.
- `Trends`: tap-water versus greywater trends and replacement-rate trend.
- `Plan`: AI saving plan, targets, estimated savings, and progress.

Water bills and water quality may remain available if useful, but they should not dominate the first saving workflow.

### Profile

The profile page should keep account identity and logout. The existing reminder toggles should become:

- Saving target reminders.
- Device abnormality reminders.

### Admin Page: Saving Management

The current resident-management page should become a saving-management dashboard with:

- Total tap-water usage.
- Total greywater usage.
- Total estimated savings.
- Average greywater replacement rate.
- Total greywater flushing count.
- Room saving ranking.
- Low replacement-rate rooms.
- Abnormal high tap-water rooms.
- Device status list.
- Device no-data and usage anomaly reminders.

## ThingCloud Integration Strategy

ThingCloud integration should be backend-only. The frontend should never store ThingCloud credentials or call ThingCloud directly.

The expected event payload accepted by the backend should be stable even if ThingCloud's real payload differs:

```json
{
  "device_id": "GW-A101-001",
  "room_number": "A101",
  "event_type": "toilet_flush",
  "event_count": 1,
  "volume_liters": 6,
  "timestamp": "2026-04-27T10:30:00",
  "source": "device"
}
```

If hardware only reports that one flush happened, the payload may omit volume:

```json
{
  "device_id": "GW-A101-001",
  "room_number": "A101",
  "event_type": "toilet_flush",
  "event_count": 1,
  "timestamp": "2026-04-27T10:30:00",
  "source": "device"
}
```

When `volume_liters` is missing, the backend should estimate the volume using a configurable default, such as 6L per flush. When measured flow data becomes available, measured volume should be preferred over estimated volume.

Incoming `event_type` values should be normalized into internal `usage_type` values. For the first version, `toilet_flush` maps to `toilet_flush`; unsupported or unknown values should map to `other` while preserving the original payload in `raw_payload_json`.

## LLM Integration Strategy

The LLM should be an optional backend service, not a frontend dependency.

Before calling the LLM, the backend should build a structured saving profile:

- Recent tap-water usage.
- Recent greywater usage.
- Greywater flushing count.
- Greywater replacement rate.
- Comparison with the previous period.
- Cleaning-related greywater usage.
- Current target progress.
- Detected anomalies.

The prompt should ask the model to produce a short, actionable plan with measurable goals. The generated response should be saved to `saving_plans` before the frontend displays it.

If no LLM API key is configured, or if the LLM request fails, the backend should generate a rule-based fallback plan. This keeps demos stable and prevents a missing external API from breaking the product.

## Fallback And Demo Strategy

The first version must remain demonstrable even if hardware and external APIs are not ready.

- If ThingCloud is unavailable, use `mock` or `manual` greywater records.
- If hardware does not provide volume, estimate volume from `event_count`.
- If LLM is unavailable, generate a rule-based saving plan.
- If there is not enough history, generate a beginner plan instead of week-over-week analysis.
- If a device has no recent data, show a clear device-status warning instead of silently hiding it.

## Implementation Strategy

The project should not be rebuilt from scratch. The current FastAPI backend, Vue/uni-app frontend, user system, admin role, room binding, database setup, and Docker deployment should be retained.

The system should be upgraded in place:

- Keep authentication, user roles, room numbers, existing water-flow data, water-bill data, and water-quality data.
- Add greywater device and greywater usage data models.
- Add saving statistics APIs that combine tap-water and greywater data.
- Add a ThingCloud-compatible integration layer.
- Add AI saving plan storage and generation APIs.
- Update the student pages from "water overview" to "saving overview".
- Update the admin page from "resident management" to "saving management dashboard".

This approach keeps the existing runnable system and redirects the product around the clearer greywater saving goal.
