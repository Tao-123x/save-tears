import importlib
import os
import sys
import tempfile
import unittest
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent


class GreywaterBackendTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "greywater.db"
        self.original_env = {
            key: os.environ.get(key)
            for key in [
                "SAVE_TEARS_DB_URL",
                "SAVE_TEARS_THINGSPEAK_CHANNEL_ID",
                "SAVE_TEARS_THINGSPEAK_READ_API_KEY",
                "SAVE_TEARS_THINGSPEAK_WRITE_API_KEY",
                "SAVE_TEARS_THINGSPEAK_ROOM_NUMBER",
                "SAVE_TEARS_THINGSPEAK_DEVICE_ID",
            ]
        }
        os.environ["SAVE_TEARS_DB_URL"] = f"sqlite:///{self.db_path}"
        for key in self.original_env:
            if key != "SAVE_TEARS_DB_URL":
                os.environ.pop(key, None)

        if str(BACKEND_DIR) not in sys.path:
            sys.path.insert(0, str(BACKEND_DIR))
        sys.modules.pop("api", None)
        self.api = importlib.import_module("api")
        self.api.initialize_database()

        self.db = self.api.SessionLocal()
        self.user = self.api.UserDB(username="alice", password_hash="pw", room_number="A101", role="user")
        self.admin = self.api.UserDB(username="admin", password_hash="secret", room_number="HQ", role="admin")
        self.db.add_all(
            [
                self.user,
                self.admin,
                self.api.WaterFlowDB(room_number="A101", flow_rate=10, timestamp="2026-04-27T08:00:00"),
                self.api.WaterFlowDB(room_number="A101", flow_rate=20, timestamp="2026-04-27T09:00:00"),
            ]
        )
        self.db.commit()
        self.db.refresh(self.user)
        self.db.refresh(self.admin)

    def tearDown(self):
        self.db.close()
        for key, value in self.original_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        sys.modules.pop("api", None)
        self.temp_dir.cleanup()

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

        stats = self.api.calculate_saving_stats("A101", self.db)
        self.assertEqual(stats["tap_water_liters"], 30)
        self.assertEqual(stats["greywater_liters"], 12)
        self.assertEqual(stats["estimated_savings_liters"], 12)
        self.assertEqual(stats["flush_count"], 2)
        self.assertAlmostEqual(stats["replacement_rate"], 12 / 42)

    def test_thingcloud_event_creates_usage_and_updates_device(self):
        response = self.api.receive_thingcloud_event(
            {
                "device_id": "GW-A101-001",
                "room_number": "A101",
                "event_type": "toilet_flush",
                "event_count": 1,
                "timestamp": "2026-04-27T10:30:00",
                "source": "device",
            },
            db=self.db,
        )

        self.assertEqual(response["data"].volume_liters, 6)
        device = self.db.query(self.api.GreywaterDeviceDB).filter_by(device_id="GW-A101-001").first()
        self.assertIsNotNone(device)
        self.assertEqual(device.room_number, "A101")
        self.assertEqual(device.status, "online")
        self.assertEqual(device.last_seen_at, "2026-04-27T10:30:00")

    def test_thingcloud_unknown_event_type_maps_to_other_and_preserves_payload(self):
        response = self.api.receive_thingcloud_event(
            {
                "device_id": "GW-A101-002",
                "room_number": "A101",
                "event_type": "unexpected_sensor_event",
                "event_count": 1,
                "timestamp": "2026-04-27T10:45:00",
                "source": "device",
            },
            db=self.db,
        )

        usage = response["data"]
        self.assertEqual(usage.usage_type, "other")
        self.assertEqual(usage.volume_liters, 0)
        self.assertIn("unexpected_sensor_event", usage.raw_payload_json)

    def test_thingcloud_duplicate_event_reuses_existing_usage_record(self):
        payload = {
            "event_id": "evt-001",
            "device_id": "GW-A101-003",
            "room_number": "A101",
            "event_type": "toilet_flush",
            "event_count": 1,
            "timestamp": "2026-04-27T11:00:00",
            "source": "device",
        }

        first = self.api.receive_thingcloud_event(payload, db=self.db)
        second = self.api.receive_thingcloud_event(payload, db=self.db)

        self.assertEqual(first["data"].id, second["data"].id)
        usage_count = self.db.query(self.api.GreywaterUsageDB).filter_by(device_id="GW-A101-003").count()
        self.assertEqual(usage_count, 1)

    def test_thingcloud_invalid_numeric_payload_returns_400(self):
        with self.assertRaises(self.api.HTTPException) as context:
            self.api.receive_thingcloud_event(
                {
                    "device_id": "GW-A101-004",
                    "room_number": "A101",
                    "event_type": "toilet_flush",
                    "event_count": "not-a-number",
                    "timestamp": "2026-04-27T11:05:00",
                    "source": "device",
                },
                db=self.db,
            )

        self.assertEqual(context.exception.status_code, 400)

    def test_thingcloud_invalid_device_status_does_not_create_usage_record(self):
        with self.assertRaises(self.api.HTTPException):
            self.api.receive_thingcloud_event(
                {
                    "device_id": "GW-A101-003",
                    "room_number": "A101",
                    "event_type": "toilet_flush",
                    "event_count": 1,
                    "timestamp": "2026-04-27T11:00:00",
                    "source": "device",
                    "status": "broken",
                },
                db=self.db,
            )

        usage_count = self.db.query(self.api.GreywaterUsageDB).filter_by(device_id="GW-A101-003").count()
        self.assertEqual(usage_count, 0)

    def test_rule_based_saving_plan_does_not_require_llm(self):
        self.api.create_greywater_usage(
            self.api.GreywaterUsageData(
                room_number="A101",
                usage_type="toilet_flush",
                event_count=1,
                volume_liters=6,
                timestamp="2026-04-27T10:00:00",
                source="manual",
            ),
            db=self.db,
            current_user=self.user,
        )

        plan = self.api.generate_rule_based_saving_plan("A101", self.db)

        self.assertEqual(plan.model_name, "rule_fallback")
        self.assertGreaterEqual(plan.target_flush_count, 1)
        self.assertGreater(plan.target_replacement_rate, 0)
        self.assertGreater(plan.estimated_savings_liters, 0)
        self.assertIn("A101", plan.plan_text)

    def test_thingspeak_sync_requires_backend_configuration(self):
        with self.assertRaises(self.api.HTTPException) as context:
            self.api.sync_thingspeak_events(db=self.db, _=self.admin)

        self.assertEqual(context.exception.status_code, 503)

    def test_thingspeak_sync_maps_channel_fields_to_internal_records(self):
        os.environ["SAVE_TEARS_THINGSPEAK_CHANNEL_ID"] = "3415864"
        os.environ["SAVE_TEARS_THINGSPEAK_READ_API_KEY"] = "read-key"
        os.environ["SAVE_TEARS_THINGSPEAK_ROOM_NUMBER"] = "A101"

        captured = []

        def fake_request(path, params=None, method="GET"):
            captured.append((path, params, method))
            return {
                "channel": {"id": 3415864, "field1": "Greywater flushes"},
                "feeds": [
                    {
                        "created_at": "2026-06-24T09:00:00Z",
                        "entry_id": 101,
                        "field1": "35",
                        "field2": "12",
                        "field3": "7.2",
                        "field4": "18",
                    }
                ],
            }

        original_request = self.api.request_thingspeak_json
        self.api.request_thingspeak_json = fake_request
        try:
            response = self.api.sync_thingspeak_events(db=self.db, _=self.admin)
        finally:
            self.api.request_thingspeak_json = original_request

        self.assertEqual(response["synced"], 1)
        self.assertEqual(captured[0][0], "/channels/3415864/feeds.json")
        self.assertEqual(captured[0][1]["api_key"], "read-key")

        tap_flow = self.db.query(self.api.WaterFlowDB).filter_by(room_number="A101", timestamp="2026-06-24T09:00:00Z").first()
        self.assertIsNotNone(tap_flow)
        self.assertEqual(tap_flow.flow_rate, 35)

        usage = self.db.query(self.api.GreywaterUsageDB).filter_by(device_id="thingspeak-3415864").first()
        self.assertIsNotNone(usage)
        self.assertEqual(usage.volume_liters, 12)
        self.assertEqual(usage.event_count, 1)
        self.assertEqual(usage.usage_type, "other")
        self.assertEqual(usage.source, "device")
        self.assertIn("thingspeak-101", usage.raw_payload_json)
        self.assertIn("tap_water_flow", usage.raw_payload_json)

        quality = self.db.query(self.api.GreywaterQualityDB).filter_by(device_id="thingspeak-3415864").first()
        self.assertIsNotNone(quality)
        self.assertEqual(quality.room_number, "A101")
        self.assertAlmostEqual(quality.ph_value, 7.2)
        self.assertEqual(quality.turbidity_value, 18)

        turbidity = self.db.query(self.api.SewageTurbidityDB).filter_by(room_number="A101", timestamp="2026-06-24T09:00:00Z").first()
        self.assertIsNotNone(turbidity)
        self.assertEqual(turbidity.turbidity_value, 18)

        device = self.db.query(self.api.GreywaterDeviceDB).filter_by(device_id="thingspeak-3415864").first()
        self.assertIsNotNone(device)
        self.assertEqual(device.room_number, "A101")
        self.assertEqual(device.source_platform, "thingspeak")

    def test_thingspeak_sync_is_idempotent_for_same_entry_id(self):
        os.environ["SAVE_TEARS_THINGSPEAK_CHANNEL_ID"] = "3415864"
        os.environ["SAVE_TEARS_THINGSPEAK_READ_API_KEY"] = "read-key"
        os.environ["SAVE_TEARS_THINGSPEAK_ROOM_NUMBER"] = "A101"

        def fake_request(path, params=None, method="GET"):
            return {
                "feeds": [
                    {
                        "created_at": "2026-06-24T09:00:00Z",
                        "entry_id": 101,
                        "field1": "35",
                        "field2": "12",
                        "field3": "7.2",
                        "field4": "18",
                    }
                ],
            }

        original_request = self.api.request_thingspeak_json
        self.api.request_thingspeak_json = fake_request
        try:
            first = self.api.sync_thingspeak_events(db=self.db, _=self.admin)
            second = self.api.sync_thingspeak_events(db=self.db, _=self.admin)
        finally:
            self.api.request_thingspeak_json = original_request

        self.assertEqual(first["synced"], 1)
        self.assertEqual(second["synced"], 0)
        usage_count = self.db.query(self.api.GreywaterUsageDB).filter_by(device_id="thingspeak-3415864").count()
        tap_flow_count = self.db.query(self.api.WaterFlowDB).filter_by(room_number="A101", timestamp="2026-06-24T09:00:00Z").count()
        quality_count = self.db.query(self.api.GreywaterQualityDB).filter_by(device_id="thingspeak-3415864").count()
        self.assertEqual(usage_count, 1)
        self.assertEqual(tap_flow_count, 1)
        self.assertEqual(quality_count, 1)

    def test_thingspeak_write_uses_backend_write_key(self):
        os.environ["SAVE_TEARS_THINGSPEAK_WRITE_API_KEY"] = "write-key"
        captured = []

        def fake_request(path, params=None, method="GET"):
            captured.append((path, params, method))
            return {"entry_id": 321, "field1": "7"}

        original_request = self.api.request_thingspeak_json
        self.api.request_thingspeak_json = fake_request
        try:
            response = self.api.write_thingspeak_feed({"field1": 7}, _=self.admin)
        finally:
            self.api.request_thingspeak_json = original_request

        self.assertEqual(response["data"]["entry_id"], 321)
        self.assertEqual(captured[0][0], "/update.json")
        self.assertEqual(captured[0][1]["api_key"], "write-key")
        self.assertEqual(captured[0][1]["field1"], 7)
        self.assertEqual(captured[0][2], "POST")

    def test_room_user_can_read_own_greywater_quality_records(self):
        self.db.add(
            self.api.GreywaterQualityDB(
                room_number="A101",
                device_id="thingspeak-3415864",
                ph_value=7.2,
                turbidity_value=18,
                source="device",
                timestamp="2026-06-24T09:00:00Z",
            )
        )
        self.db.commit()

        records = self.api.get_greywater_quality("A101", db=self.db, current_user=self.user)

        self.assertEqual(len(records), 1)
        self.assertAlmostEqual(records[0].ph_value, 7.2)
        self.assertEqual(records[0].turbidity_value, 18)


if __name__ == "__main__":
    unittest.main()
