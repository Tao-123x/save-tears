# Save Tears Backend

FastAPI backend for the Save Tears campus greywater saving system.

## Core Responsibilities

- User registration, login, signed session tokens, and room-based authorization.
- Tap-water records through the existing `water_flow` API.
- Greywater device records and greywater usage records.
- ThingCloud-compatible device event ingestion.
- ThingSpeak backend-only read/write proxy and feed synchronization.
- Saving statistics that combine tap-water and greywater usage.
- Rule-based saving-plan fallback for demos and local development.

## Local Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

The backend defaults to `sqlite:///./save_tears.db`. Set `SAVE_TEARS_DB_URL` to use another SQLAlchemy-supported database URL.

## Important Environment Variables

```bash
SAVE_TEARS_DB_URL=sqlite:///./save_tears.db
SAVE_TEARS_SECRET=replace-with-a-long-random-secret
SAVE_TEARS_THINGCLOUD_WEBHOOK_SECRET=replace-with-a-different-long-random-secret
SAVE_TEARS_GREYWATER_LITERS_PER_FLUSH=6
SAVE_TEARS_ADMIN_USERNAME=admin
SAVE_TEARS_ADMIN_PASSWORD=replace-with-a-strong-admin-password
SAVE_TEARS_ADMIN_ROOM=HQ
SAVE_TEARS_THINGSPEAK_CHANNEL_ID=replace-with-channel-id
SAVE_TEARS_THINGSPEAK_READ_API_KEY=replace-with-read-api-key
SAVE_TEARS_THINGSPEAK_WRITE_API_KEY=replace-with-write-api-key
SAVE_TEARS_THINGSPEAK_ROOM_NUMBER=A101
```

Set `SAVE_TEARS_ENV=production` in production. The service rejects the local default auth secret in production mode.

Use server environment variables for ThingSpeak keys. Do not place ThingSpeak API keys in mini-program or browser code.

## Greywater Event Ingestion

ThingCloud or a hardware gateway can send events to:

```text
POST /integrations/thingcloud/events
```

Use one of these authentication methods:

- `Authorization: Bearer <admin-token>` for local testing.
- `X-ThingCloud-Secret: <secret>` for hardware integration when `SAVE_TEARS_THINGCLOUD_WEBHOOK_SECRET` is configured.

Example payload:

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

If `volume_liters` is omitted, toilet flushing is estimated as `event_count * SAVE_TEARS_GREYWATER_LITERS_PER_FLUSH`. Unknown event types are normalized to `other`.

## ThingSpeak Integration

ThingSpeak is exposed through backend admin endpoints:

```text
GET  /integrations/thingspeak/feeds?results=2
GET  /integrations/thingspeak/fields/1?results=2
GET  /integrations/thingspeak/status?results=2
POST /integrations/thingspeak/write
POST /integrations/thingspeak/sync?results=2
GET  /greywater_quality/<room_number>
```

`POST /integrations/thingspeak/write` accepts fields such as `field1` through `field8` and writes them to ThingSpeak using `SAVE_TEARS_THINGSPEAK_WRITE_API_KEY`.

`POST /integrations/thingspeak/sync` reads the latest ThingSpeak feeds and maps this channel layout into internal records:

- `field1` / Tap Water Flow -> `water_flow.flow_rate`
- `field2` / Grey Water Flow -> `greywater_usage.volume_liters`
- `field3` / Grey Water pH -> `greywater_quality.ph_value`
- `field4` / Grey Water Turbidity -> `greywater_quality.turbidity_value` and the legacy turbidity table

Synced ThingSpeak entries are tracked by entry ID so calling the sync endpoint repeatedly does not duplicate the same feed entry.

## Tests

```bash
python -m unittest test_authz.py test_production_basics.py test_greywater.py -v
```
