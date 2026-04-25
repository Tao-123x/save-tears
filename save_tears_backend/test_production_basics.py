import importlib
import os
import sys
import tempfile
import unittest
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent


class BackendProductionBasicsTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "prod_basics.db"
        self.original_env = {
            key: os.environ.get(key)
            for key in [
                "SAVE_TEARS_DB_URL",
                "SAVE_TEARS_SECRET",
                "SAVE_TEARS_ADMIN_USERNAME",
                "SAVE_TEARS_ADMIN_PASSWORD",
                "SAVE_TEARS_ADMIN_ROOM",
                "SAVE_TEARS_ADMIN_RESET_PASSWORD",
            ]
        }
        os.environ["SAVE_TEARS_DB_URL"] = f"sqlite:///{self.db_path}"
        os.environ["SAVE_TEARS_SECRET"] = "test-production-secret"
        os.environ["SAVE_TEARS_ADMIN_USERNAME"] = "ops-admin"
        os.environ["SAVE_TEARS_ADMIN_PASSWORD"] = "StrongAdminPass123!"
        os.environ["SAVE_TEARS_ADMIN_ROOM"] = "HQ"
        os.environ.pop("SAVE_TEARS_ADMIN_RESET_PASSWORD", None)

        if str(BACKEND_DIR) not in sys.path:
            sys.path.insert(0, str(BACKEND_DIR))
        sys.modules.pop("api", None)
        sys.modules.pop("main", None)
        self.api = importlib.import_module("api")
        self.main = importlib.import_module("main")

    def tearDown(self):
        for key, value in self.original_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        sys.modules.pop("api", None)
        sys.modules.pop("main", None)
        self.temp_dir.cleanup()

    def test_initialize_database_creates_hashed_admin_from_environment(self):
        self.api.initialize_database()

        db = self.api.SessionLocal()
        try:
            admin = db.query(self.api.UserDB).filter(self.api.UserDB.username == "ops-admin").first()
            self.assertIsNotNone(admin)
            self.assertEqual(admin.role, "admin")
            self.assertEqual(admin.room_number, "HQ")
            self.assertNotEqual(admin.password_hash, "StrongAdminPass123!")
            self.assertTrue(self.api.verify_password("StrongAdminPass123!", admin.password_hash))
        finally:
            db.close()

    def test_legacy_plaintext_password_is_upgraded_after_successful_login(self):
        self.api.initialize_database()
        db = self.api.SessionLocal()
        try:
            legacy_user = self.api.UserDB(username="legacy", password_hash="pw", room_number="A101", role="user")
            db.add(legacy_user)
            db.commit()

            response = self.api.login_user(self.api.UserLogin(username="legacy", password="pw"), db=db)

            db.refresh(legacy_user)
            self.assertEqual(response["username"], "legacy")
            self.assertNotEqual(legacy_user.password_hash, "pw")
            self.assertTrue(self.api.verify_password("pw", legacy_user.password_hash))
        finally:
            db.close()

    def test_health_reports_database_status(self):
        self.api.initialize_database()
        db = self.api.SessionLocal()
        try:
            health = self.main.read_health(db=db)
            self.assertEqual(health["status"], "ok")
            self.assertEqual(health["database"], "ok")
            self.assertEqual(health["service"], "save-tears-backend")
        finally:
            db.close()


if __name__ == "__main__":
    unittest.main()
