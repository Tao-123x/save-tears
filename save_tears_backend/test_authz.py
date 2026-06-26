import importlib
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent


def find_free_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


class BackendAuthzTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.db_path = Path(cls.temp_dir.name) / "test.db"
        cls.port = find_free_port()
        cls.base_url = f"http://127.0.0.1:{cls.port}"
        cls.original_db_url = os.environ.get("SAVE_TEARS_DB_URL")
        cls.original_webhook_secret = os.environ.get("SAVE_TEARS_THINGCLOUD_WEBHOOK_SECRET")
        os.environ["SAVE_TEARS_DB_URL"] = f"sqlite:///{cls.db_path}"
        os.environ["SAVE_TEARS_THINGCLOUD_WEBHOOK_SECRET"] = "test-webhook-secret"

        if str(BACKEND_DIR) not in sys.path:
            sys.path.insert(0, str(BACKEND_DIR))

        sys.modules.pop("api", None)
        sys.modules.pop("main", None)
        cls.api = importlib.import_module("api")
        cls.api.Base.metadata.create_all(bind=cls.api.engine)
        cls._seed_data()

        env = os.environ.copy()
        cls.server = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", str(cls.port)],
            cwd=str(BACKEND_DIR),
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        cls._wait_for_server()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "server"):
            cls.server.terminate()
            try:
                cls.server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                cls.server.kill()
        if cls.original_db_url is None:
            os.environ.pop("SAVE_TEARS_DB_URL", None)
        else:
            os.environ["SAVE_TEARS_DB_URL"] = cls.original_db_url
        if cls.original_webhook_secret is None:
            os.environ.pop("SAVE_TEARS_THINGCLOUD_WEBHOOK_SECRET", None)
        else:
            os.environ["SAVE_TEARS_THINGCLOUD_WEBHOOK_SECRET"] = cls.original_webhook_secret
        cls.temp_dir.cleanup()

    @classmethod
    def _seed_data(cls):
        db = cls.api.SessionLocal()
        try:
            db.add_all(
                [
                    cls.api.UserDB(username="admin", password_hash="secret", room_number="HQ", role="admin"),
                    cls.api.UserDB(username="alice", password_hash="pw", room_number="A101", role="user"),
                    cls.api.UserDB(username="bob", password_hash="pw", room_number="B202", role="user"),
                    cls.api.WaterFlowDB(room_number="A101", flow_rate=12, timestamp="2026-03-26T10:00:00"),
                    cls.api.WaterFlowDB(room_number="B202", flow_rate=88, timestamp="2026-03-26T11:00:00"),
                ]
            )
            db.commit()
        finally:
            db.close()

    @classmethod
    def _wait_for_server(cls):
        deadline = time.time() + 10
        while time.time() < deadline:
            if cls.server.poll() is not None:
                raise RuntimeError("backend server exited before tests could start")
            try:
                status, _ = cls.request_json("GET", "/")
                if status == 200:
                    return
            except Exception:
                time.sleep(0.2)
        raise RuntimeError("backend server did not become ready in time")

    @classmethod
    def request_json(cls, method: str, path: str, payload=None, headers=None):
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(f"{cls.base_url}{path}", data=data, method=method)
        request.add_header("Content-Type", "application/json")
        for key, value in (headers or {}).items():
            request.add_header(key, value)

        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

        try:
            with opener.open(request, timeout=5) as response:
                body = response.read().decode("utf-8")
                return response.status, json.loads(body) if body else None
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8")
            return error.code, json.loads(body) if body else None

    @classmethod
    def auth_headers(cls, username: str, password: str):
        status, body = cls.request_json("POST", "/login", {"username": username, "password": password})
        if status != 200:
            raise AssertionError((status, body))
        token = (body or {}).get("token")
        return {"Authorization": f"Bearer {token}"} if token else {}

    def test_login_returns_signed_token(self):
        status, body = self.request_json("POST", "/login", {"username": "alice", "password": "pw"})
        self.assertEqual(status, 200)
        self.assertIn("token", body)

    def test_regular_user_cannot_list_users(self):
        status, _ = self.request_json("GET", "/users", headers=self.auth_headers("alice", "pw"))
        self.assertEqual(status, 403)

    def test_regular_user_cannot_read_another_room_data(self):
        status, _ = self.request_json("GET", "/water_flow/B202", headers=self.auth_headers("alice", "pw"))
        self.assertEqual(status, 403)

    def test_regular_user_cannot_read_other_room_greywater(self):
        status, _ = self.request_json("GET", "/greywater_usage/B202", headers=self.auth_headers("alice", "pw"))
        self.assertEqual(status, 403)

    def test_regular_user_cannot_access_other_room_saving_endpoints(self):
        headers = self.auth_headers("alice", "pw")
        for method, path in [
            ("GET", "/greywater_summary/B202"),
            ("GET", "/saving_stats/B202"),
            ("POST", "/saving_plans/B202/generate"),
            ("GET", "/saving_plans/B202/latest"),
            ("GET", "/saving_plans/B202"),
        ]:
            with self.subTest(path=path):
                status, _ = self.request_json(method, path, headers=headers)
                self.assertEqual(status, 403)

    def test_thingcloud_event_creates_usage_and_updates_device(self):
        status, body = self.request_json(
            "POST",
            "/integrations/thingcloud/events",
            {
                "device_id": "GW-A101-001",
                "room_number": "A101",
                "event_type": "toilet_flush",
                "event_count": 1,
                "timestamp": "2026-04-27T10:30:00",
                "source": "device",
            },
            headers=self.auth_headers("admin", "secret"),
        )
        self.assertEqual(status, 200)
        self.assertEqual(body["data"]["volume_liters"], 6)

    def test_thingcloud_event_accepts_webhook_secret_without_admin_bearer(self):
        status, body = self.request_json(
            "POST",
            "/integrations/thingcloud/events",
            {
                "device_id": "GW-A101-002",
                "room_number": "A101",
                "event_type": "toilet_flush",
                "event_count": 1,
                "timestamp": "2026-04-27T10:45:00",
                "source": "device",
            },
            headers={"X-ThingCloud-Secret": "test-webhook-secret"},
        )
        self.assertEqual(status, 200)
        self.assertEqual(body["data"]["source"], "device")

    def test_thingcloud_event_rejects_wrong_webhook_secret_without_admin_bearer(self):
        status, _ = self.request_json(
            "POST",
            "/integrations/thingcloud/events",
            {
                "device_id": "GW-A101-003",
                "room_number": "A101",
                "event_type": "toilet_flush",
                "event_count": 1,
                "timestamp": "2026-04-27T11:00:00",
                "source": "device",
            },
            headers={"X-ThingCloud-Secret": "wrong"},
        )
        self.assertEqual(status, 401)

    def test_admin_user_list_omits_password_hash(self):
        status, body = self.request_json("GET", "/users", headers=self.auth_headers("admin", "secret"))
        self.assertEqual(status, 200)
        self.assertTrue(body)
        self.assertTrue(all("password_hash" not in item for item in body), body)


if __name__ == "__main__":
    unittest.main()
