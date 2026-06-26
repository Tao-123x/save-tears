import os
import json
import time
import hmac
import base64
import hashlib
import logging
import secrets
import urllib.error
import urllib.parse
import urllib.request

from fastapi import HTTPException, Depends, APIRouter, Header
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Float, Integer, String, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# ==================== 1. 基础配置 ====================
# 连接数据库
SQLALCHEMY_DATABASE_URL = os.getenv("SAVE_TEARS_DB_URL", "sqlite:///./save_tears.db")

engine_kwargs = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
AUTH_SECRET = os.getenv("SAVE_TEARS_SECRET", "save-tears-dev-secret")
DEFAULT_AUTH_SECRET = "save-tears-dev-secret"
TOKEN_TTL_SECONDS = int(os.getenv("SAVE_TEARS_TOKEN_TTL", "86400"))
PASSWORD_SCHEME = "pbkdf2_sha256"
PASSWORD_ITERATIONS = int(os.getenv("SAVE_TEARS_PASSWORD_ITERATIONS", "260000"))
logger = logging.getLogger("save_tears.backend")
DEFAULT_GREYWATER_LITERS_PER_FLUSH = int(os.getenv("SAVE_TEARS_GREYWATER_LITERS_PER_FLUSH", "6"))
GREYWATER_USAGE_TYPES = {"toilet_flush", "cleaning", "other"}
GREYWATER_SOURCES = {"device", "manual", "mock"}
DEVICE_STATUSES = {"online", "offline", "warning"}
THINGSPEAK_API_BASE_URL = "https://api.thingspeak.com"

# ==================== 2. 数据库模型 ====================
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    # 这里我们暂时直接存明文密码
    password_hash = Column(String(100)) 
    room_number = Column(String(20))
    role = Column(String(20), default="user")

class WaterFlowDB(Base):
    __tablename__ = "water_flow"
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(20), index=True)
    flow_rate = Column(Integer)
    timestamp = Column(String(50))

class SewageTurbidityDB(Base):
    __tablename__ = "sewage_turbidity"
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(20), index=True)
    turbidity_value = Column(Integer)
    timestamp = Column(String(50))

class WaterBillDB(Base):
    __tablename__ = "water_bill"
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(20), index=True)
    amount = Column(Integer)
    month = Column(String(10))

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

class GreywaterQualityDB(Base):
    __tablename__ = "greywater_quality"
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(20), index=True)
    device_id = Column(String(80), index=True)
    ph_value = Column(Float)
    turbidity_value = Column(Integer)
    source = Column(String(20), default="device")
    timestamp = Column(String(50))
    raw_payload_json = Column(String)

class ExternalEventSyncDB(Base):
    __tablename__ = "external_event_sync"
    id = Column(Integer, primary_key=True, index=True)
    source_platform = Column(String(50), index=True)
    event_id = Column(String(120), index=True)
    timestamp = Column(String(50))
    raw_payload_json = Column(String)

class SavingPlanDB(Base):
    __tablename__ = "saving_plans"
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(20), index=True)
    period_start = Column(String(50))
    period_end = Column(String(50))
    plan_text = Column(String)
    target_flush_count = Column(Integer)
    target_replacement_rate = Column(Float)
    estimated_savings_liters = Column(Integer)
    model_name = Column(String(80), default="rule_fallback")
    created_at = Column(String(50))
    status = Column(String(20), default="active")

# ==================== 3. Pydantic模型 ====================
class UserRegister(BaseModel):
    username: str
    password: str
    room_number: str

class UserLogin(BaseModel):
    username: str
    password: str

class WaterFlowData(BaseModel):
    room_number: str
    flow_rate: int
    timestamp: str

class SewageTurbidityData(BaseModel):
    room_number: str
    turbidity_value: int
    timestamp: str

class WaterBillData(BaseModel):
    room_number: str
    amount: int
    month: str

class GreywaterUsageData(BaseModel):
    room_number: str
    usage_type: str = "toilet_flush"
    event_count: int = 1
    volume_liters: int | None = None
    timestamp: str
    source: str = "manual"
    device_id: str | None = None
    raw_payload: dict | None = None

class GreywaterDeviceData(BaseModel):
    device_id: str
    room_number: str
    device_type: str = "toilet_flush_sensor"
    status: str = "offline"
    last_seen_at: str | None = None
    source_platform: str = "thingcloud"
    metadata: dict | None = None

class GreywaterUsageRecord(BaseModel):
    id: int | None = None
    room_number: str
    device_id: str | None = None
    usage_type: str
    event_count: int
    volume_liters: int
    source: str
    timestamp: str
    raw_payload_json: str | None = None

class GreywaterDeviceRecord(BaseModel):
    id: int | None = None
    device_id: str
    room_number: str
    device_type: str
    status: str
    last_seen_at: str | None = None
    source_platform: str
    metadata_json: str | None = None

class GreywaterQualityRecord(BaseModel):
    id: int | None = None
    room_number: str
    device_id: str | None = None
    ph_value: float | None = None
    turbidity_value: int | None = None
    source: str
    timestamp: str
    raw_payload_json: str | None = None

class SavingPlanRecord(BaseModel):
    id: int | None = None
    room_number: str
    period_start: str
    period_end: str
    plan_text: str
    target_flush_count: int
    target_replacement_rate: float
    estimated_savings_liters: int
    model_name: str
    created_at: str
    status: str


class LoginResponse(BaseModel):
    msg: str
    username: str
    room_number: str
    role: str
    token: str


class PublicUser(BaseModel):
    id: int
    username: str
    room_number: str | None = None
    role: str

# ==================== 4. 辅助函数 ====================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    salt = secrets.token_urlsafe(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        PASSWORD_ITERATIONS,
    )
    return f"{PASSWORD_SCHEME}${PASSWORD_ITERATIONS}${salt}${_encode_segment(digest)}"


def _is_hashed_password(stored_password: str | None) -> bool:
    return bool(stored_password and stored_password.startswith(f"{PASSWORD_SCHEME}$"))


def verify_password(password: str, stored_password: str | None) -> bool:
    if not stored_password:
        return False

    if not _is_hashed_password(stored_password):
        return hmac.compare_digest(stored_password, password)

    try:
        scheme, iterations, salt, expected_digest = stored_password.split("$", 3)
        if scheme != PASSWORD_SCHEME:
            return False
        actual_digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            int(iterations),
        )
        return hmac.compare_digest(expected_digest, _encode_segment(actual_digest))
    except (ValueError, TypeError):
        return False


def password_needs_upgrade(stored_password: str | None) -> bool:
    return not _is_hashed_password(stored_password)


def bootstrap_admin_user() -> None:
    username = os.getenv("SAVE_TEARS_ADMIN_USERNAME", "").strip()
    password = os.getenv("SAVE_TEARS_ADMIN_PASSWORD", "")
    room_number = os.getenv("SAVE_TEARS_ADMIN_ROOM", "HQ").strip() or "HQ"
    reset_password = os.getenv("SAVE_TEARS_ADMIN_RESET_PASSWORD", "").strip().lower() in {"1", "true", "yes"}

    if not username or not password:
        logger.info("admin_bootstrap_skipped reason=missing_admin_env")
        return

    db = SessionLocal()
    try:
        admin = db.query(UserDB).filter(UserDB.username == username).first()
        if not admin:
            db.add(
                UserDB(
                    username=username,
                    password_hash=hash_password(password),
                    room_number=room_number,
                    role="admin",
                )
            )
            db.commit()
            logger.info("admin_bootstrap_created username=%s", username)
            return

        changed = False
        if admin.role != "admin":
            admin.role = "admin"
            changed = True
        if not str(admin.room_number or "").strip():
            admin.room_number = room_number
            changed = True
        if reset_password:
            admin.password_hash = hash_password(password)
            changed = True
        if changed:
            db.commit()
            logger.info("admin_bootstrap_updated username=%s reset_password=%s", username, reset_password)
        else:
            logger.info("admin_bootstrap_exists username=%s", username)
    finally:
        db.close()


def initialize_database() -> None:
    validate_auth_secret_for_production()
    Base.metadata.create_all(bind=engine)
    apply_sqlite_compatibility_migrations()
    bootstrap_admin_user()


def validate_auth_secret_for_production() -> None:
    env_name = os.getenv("SAVE_TEARS_ENV", "").strip().lower()
    require_strong_secret = os.getenv("SAVE_TEARS_REQUIRE_STRONG_SECRET", "").strip().lower() in {"1", "true", "yes"}
    configured_secret = os.getenv("SAVE_TEARS_SECRET", DEFAULT_AUTH_SECRET)
    if (env_name in {"prod", "production"} or require_strong_secret) and configured_secret == DEFAULT_AUTH_SECRET:
        raise RuntimeError("SAVE_TEARS_SECRET must be set to a strong secret outside local development")


def apply_sqlite_compatibility_migrations() -> None:
    if not SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
        return

    inspector = inspect(engine)
    if "users" not in inspector.get_table_names():
        return

    user_columns = {column["name"] for column in inspector.get_columns("users")}
    required_columns = {
        "password_hash": "VARCHAR(100)",
        "room_number": "VARCHAR(20)",
        "role": "VARCHAR(20)",
    }
    with engine.begin() as connection:
        for column_name, column_type in required_columns.items():
            if column_name not in user_columns:
                connection.execute(text(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}"))


def _encode_segment(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("utf-8").rstrip("=")


def _decode_segment(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(f"{value}{padding}")


def create_session_token(user: UserDB) -> str:
    payload = {
        "username": user.username,
        "exp": int(time.time()) + TOKEN_TTL_SECONDS,
    }
    payload_segment = _encode_segment(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8"))
    signature = hmac.new(AUTH_SECRET.encode("utf-8"), payload_segment.encode("utf-8"), hashlib.sha256).digest()
    return f"{payload_segment}.{_encode_segment(signature)}"


def parse_session_token(token: str) -> dict:
    try:
        payload_segment, signature_segment = token.split(".", 1)
    except ValueError as error:
        raise HTTPException(status_code=401, detail="登录状态无效，请重新登录") from error

    expected_signature = hmac.new(
        AUTH_SECRET.encode("utf-8"),
        payload_segment.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    actual_signature = _decode_segment(signature_segment)
    if not hmac.compare_digest(expected_signature, actual_signature):
        raise HTTPException(status_code=401, detail="登录状态无效，请重新登录")

    payload = json.loads(_decode_segment(payload_segment).decode("utf-8"))
    if int(payload.get("exp", 0)) <= int(time.time()):
        raise HTTPException(status_code=401, detail="登录状态已过期，请重新登录")
    return payload


def get_current_user(authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> UserDB:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="请先登录")

    token = authorization.split(" ", 1)[1].strip()
    payload = parse_session_token(token)
    username = str(payload.get("username", "")).strip()
    if not username:
        raise HTTPException(status_code=401, detail="登录状态无效，请重新登录")

    db_user = db.query(UserDB).filter(UserDB.username == username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="登录状态无效，请重新登录")
    return db_user


def get_admin_user(current_user: UserDB = Depends(get_current_user)) -> UserDB:
    if str(current_user.role or "").lower() != "admin":
        raise HTTPException(status_code=403, detail="无权限访问管理员接口")
    return current_user


def authorize_thingcloud_ingestion(
    x_thingcloud_secret: str | None = Header(default=None),
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> UserDB | None:
    configured_secret = os.getenv("SAVE_TEARS_THINGCLOUD_WEBHOOK_SECRET", "").strip()
    provided_secret = str(x_thingcloud_secret or "").strip()
    if configured_secret and provided_secret and hmac.compare_digest(configured_secret, provided_secret):
        return None
    if provided_secret and configured_secret:
        raise HTTPException(status_code=401, detail="ThingCloud 接入密钥无效")
    return get_admin_user(get_current_user(authorization=authorization, db=db))


def ensure_room_access(room_number: str, current_user: UserDB) -> str:
    if str(current_user.role or "").lower() == "admin":
        return room_number
    if str(current_user.room_number or "").strip() != str(room_number or "").strip():
        raise HTTPException(status_code=403, detail="无权限访问其他房间数据")
    return current_user.room_number


def serialize_public_user(user: UserDB) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "room_number": user.room_number,
        "role": user.role,
    }


def serialize_greywater_usage(record: GreywaterUsageDB) -> GreywaterUsageRecord:
    return GreywaterUsageRecord(
        id=record.id,
        room_number=record.room_number,
        device_id=record.device_id,
        usage_type=record.usage_type,
        event_count=int(record.event_count or 0),
        volume_liters=int(record.volume_liters or 0),
        source=record.source,
        timestamp=record.timestamp,
        raw_payload_json=record.raw_payload_json,
    )


def serialize_greywater_device(record: GreywaterDeviceDB) -> GreywaterDeviceRecord:
    return GreywaterDeviceRecord(
        id=record.id,
        device_id=record.device_id,
        room_number=record.room_number,
        device_type=record.device_type,
        status=record.status,
        last_seen_at=record.last_seen_at,
        source_platform=record.source_platform,
        metadata_json=record.metadata_json,
    )


def serialize_greywater_quality(record: GreywaterQualityDB) -> GreywaterQualityRecord:
    return GreywaterQualityRecord(
        id=record.id,
        room_number=record.room_number,
        device_id=record.device_id,
        ph_value=float(record.ph_value) if record.ph_value is not None else None,
        turbidity_value=int(record.turbidity_value) if record.turbidity_value is not None else None,
        source=record.source,
        timestamp=record.timestamp,
        raw_payload_json=record.raw_payload_json,
    )


def serialize_saving_plan(record: SavingPlanDB) -> SavingPlanRecord:
    return SavingPlanRecord(
        id=record.id,
        room_number=record.room_number,
        period_start=record.period_start,
        period_end=record.period_end,
        plan_text=record.plan_text,
        target_flush_count=int(record.target_flush_count or 0),
        target_replacement_rate=float(record.target_replacement_rate or 0),
        estimated_savings_liters=int(record.estimated_savings_liters or 0),
        model_name=record.model_name,
        created_at=record.created_at,
        status=record.status,
    )


def _json_text(value: dict | None) -> str | None:
    if value is None:
        return None
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def parse_non_negative_int(value, field_name: str, default: int | None = None) -> int | None:
    if value is None or value == "":
        return default
    try:
        parsed = int(float(value))
    except (TypeError, ValueError) as error:
        raise HTTPException(status_code=400, detail=f"{field_name} 必须是非负整数") from error
    if parsed < 0:
        raise HTTPException(status_code=400, detail=f"{field_name} 必须是非负整数")
    return parsed


def parse_non_negative_float(value, field_name: str, default: float | None = None) -> float | None:
    if value is None or value == "":
        return default
    try:
        parsed = float(value)
    except (TypeError, ValueError) as error:
        raise HTTPException(status_code=400, detail=f"{field_name} 必须是非负数字") from error
    if parsed < 0:
        raise HTTPException(status_code=400, detail=f"{field_name} 必须是非负数字")
    return parsed


def normalize_usage_type(usage_type: str | None) -> str:
    normalized = str(usage_type or "toilet_flush").strip().lower()
    if normalized not in GREYWATER_USAGE_TYPES:
        raise HTTPException(status_code=400, detail="不支持的灰水使用类型")
    return normalized


def normalize_thingcloud_usage_type(usage_type: str | None) -> str:
    normalized = str(usage_type or "toilet_flush").strip().lower()
    if normalized in GREYWATER_USAGE_TYPES:
        return normalized
    return "other"


def find_existing_thingcloud_usage(
    db: Session,
    device_id: str,
    timestamp: str,
    usage_type: str,
    payload: dict,
) -> GreywaterUsageDB | None:
    event_id = str(payload.get("event_id") or payload.get("id") or "").strip()
    candidates = (
        db.query(GreywaterUsageDB)
        .filter(
            GreywaterUsageDB.device_id == device_id,
            GreywaterUsageDB.timestamp == timestamp,
            GreywaterUsageDB.usage_type == usage_type,
        )
        .all()
    )
    if event_id:
        needle = f'"event_id":"{event_id}"'
        for candidate in candidates:
            if needle in str(candidate.raw_payload_json or ""):
                return candidate
    return candidates[0] if candidates else None


def normalize_source(source: str | None) -> str:
    normalized = str(source or "manual").strip().lower()
    if normalized not in GREYWATER_SOURCES:
        raise HTTPException(status_code=400, detail="不支持的灰水数据来源")
    return normalized


def normalize_device_status(status: str | None) -> str:
    normalized = str(status or "offline").strip().lower()
    if normalized not in DEVICE_STATUSES:
        raise HTTPException(status_code=400, detail="不支持的设备状态")
    return normalized


def estimate_greywater_volume(usage_type: str, event_count: int, volume_liters: int | None) -> int:
    if volume_liters is not None:
        return max(int(volume_liters), 0)
    if usage_type == "toilet_flush":
        return max(int(event_count or 0), 0) * DEFAULT_GREYWATER_LITERS_PER_FLUSH
    return 0


def build_greywater_usage_record(room_number: str, data: GreywaterUsageData) -> GreywaterUsageDB:
    usage_type = normalize_usage_type(data.usage_type)
    source = normalize_source(data.source)
    event_count = max(int(data.event_count or 0), 0)
    volume_liters = estimate_greywater_volume(usage_type, event_count, data.volume_liters)
    return GreywaterUsageDB(
        room_number=room_number,
        device_id=data.device_id,
        usage_type=usage_type,
        event_count=event_count,
        volume_liters=volume_liters,
        source=source,
        timestamp=data.timestamp,
        raw_payload_json=_json_text(data.raw_payload),
    )


def _sum_tap_water(room_number: str, db: Session) -> int:
    records = db.query(WaterFlowDB).filter(WaterFlowDB.room_number == room_number).all()
    return sum(int(record.flow_rate or 0) for record in records)


def _greywater_records(room_number: str, db: Session) -> list[GreywaterUsageDB]:
    return db.query(GreywaterUsageDB).filter(GreywaterUsageDB.room_number == room_number).all()


def _trend_bucket(timestamp: str | None) -> str:
    return str(timestamp or "unknown")[:10] or "unknown"


def calculate_saving_stats(room_number: str, db: Session) -> dict:
    tap_water_liters = _sum_tap_water(room_number, db)
    greywater_records = _greywater_records(room_number, db)
    greywater_liters = sum(int(record.volume_liters or 0) for record in greywater_records)
    flush_count = sum(
        int(record.event_count or 0)
        for record in greywater_records
        if record.usage_type == "toilet_flush"
    )
    total_water = tap_water_liters + greywater_liters
    replacement_rate = greywater_liters / total_water if total_water else 0

    buckets: dict[str, dict] = {}
    for record in db.query(WaterFlowDB).filter(WaterFlowDB.room_number == room_number).all():
        label = _trend_bucket(record.timestamp)
        bucket = buckets.setdefault(label, {"label": label, "tap_water_liters": 0, "greywater_liters": 0})
        bucket["tap_water_liters"] += int(record.flow_rate or 0)
    for record in greywater_records:
        label = _trend_bucket(record.timestamp)
        bucket = buckets.setdefault(label, {"label": label, "tap_water_liters": 0, "greywater_liters": 0})
        bucket["greywater_liters"] += int(record.volume_liters or 0)

    trends = []
    for label in sorted(buckets):
        bucket = buckets[label]
        total = bucket["tap_water_liters"] + bucket["greywater_liters"]
        trends.append({**bucket, "replacement_rate": bucket["greywater_liters"] / total if total else 0})

    return {
        "room_number": room_number,
        "tap_water_liters": tap_water_liters,
        "greywater_liters": greywater_liters,
        "estimated_savings_liters": greywater_liters,
        "replacement_rate": replacement_rate,
        "flush_count": flush_count,
        "trends": trends,
    }


def _usage_distribution(records: list[GreywaterUsageDB]) -> dict:
    distribution = {usage_type: {"event_count": 0, "volume_liters": 0} for usage_type in sorted(GREYWATER_USAGE_TYPES)}
    for record in records:
        usage_type = record.usage_type if record.usage_type in distribution else "other"
        distribution[usage_type]["event_count"] += int(record.event_count or 0)
        distribution[usage_type]["volume_liters"] += int(record.volume_liters or 0)
    return distribution


def generate_rule_based_saving_plan(room_number: str, db: Session) -> SavingPlanDB:
    stats = calculate_saving_stats(room_number, db)
    current_flush_count = int(stats["flush_count"])
    target_flush_count = max(current_flush_count + 1, 3)
    current_rate = float(stats["replacement_rate"])
    target_replacement_rate = min(0.8, max(round(current_rate + 0.1, 2), 0.2))
    estimated_savings = target_flush_count * DEFAULT_GREYWATER_LITERS_PER_FLUSH
    now_text = time.strftime("%Y-%m-%dT%H:%M:%S")
    plan_text = (
        f"Room {room_number}: keep greywater flushing as the first saving action. "
        f"Target {target_flush_count} greywater flushes in the next 7 days, "
        f"aim for a {int(target_replacement_rate * 100)}% replacement rate, and expect about "
        f"{estimated_savings}L tap-water savings if completed."
    )
    plan = SavingPlanDB(
        room_number=room_number,
        period_start=now_text[:10],
        period_end=now_text[:10],
        plan_text=plan_text,
        target_flush_count=target_flush_count,
        target_replacement_rate=target_replacement_rate,
        estimated_savings_liters=estimated_savings,
        model_name="rule_fallback",
        created_at=now_text,
        status="active",
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


def require_thingspeak_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise HTTPException(status_code=503, detail=f"ThingSpeak 后端配置缺失：{name}")
    return value


def thingspeak_channel_id() -> str:
    return require_thingspeak_env("SAVE_TEARS_THINGSPEAK_CHANNEL_ID")


def thingspeak_read_api_key() -> str:
    return require_thingspeak_env("SAVE_TEARS_THINGSPEAK_READ_API_KEY")


def thingspeak_write_api_key() -> str:
    return require_thingspeak_env("SAVE_TEARS_THINGSPEAK_WRITE_API_KEY")


def thingspeak_room_number() -> str:
    return require_thingspeak_env("SAVE_TEARS_THINGSPEAK_ROOM_NUMBER")


def thingspeak_device_id(channel_id: str) -> str:
    configured_device_id = os.getenv("SAVE_TEARS_THINGSPEAK_DEVICE_ID", "").strip()
    return configured_device_id or f"thingspeak-{channel_id}"


def request_thingspeak_json(path: str, params: dict | None = None, method: str = "GET"):
    base_url = os.getenv("SAVE_TEARS_THINGSPEAK_BASE_URL", THINGSPEAK_API_BASE_URL).strip().rstrip("/")
    timeout = float(os.getenv("SAVE_TEARS_THINGSPEAK_TIMEOUT", "8"))
    method = method.upper()
    params = params or {}

    if method == "GET":
        query = urllib.parse.urlencode(params)
        url = f"{base_url}{path}"
        if query:
            url = f"{url}?{query}"
        request = urllib.request.Request(url, method="GET")
    else:
        data = urllib.parse.urlencode(params).encode("utf-8")
        request = urllib.request.Request(f"{base_url}{path}", data=data, method=method)
        request.add_header("Content-Type", "application/x-www-form-urlencoded")

    request.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw_body = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        raise HTTPException(status_code=502, detail=f"ThingSpeak 请求失败：HTTP {error.code}") from error
    except urllib.error.URLError as error:
        raise HTTPException(status_code=502, detail="ThingSpeak 网络请求失败") from error

    body = raw_body.strip()
    if body == "-1":
        raise HTTPException(status_code=502, detail="ThingSpeak 读取失败：Channel 不存在或 Read API Key 无权限")
    if body == "0":
        raise HTTPException(status_code=502, detail="ThingSpeak 写入失败：服务返回 0")
    if not body:
        return {}
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        if body.isdigit():
            return int(body)
        return {"raw": body}


def bounded_thingspeak_results(results: int | None) -> int:
    if results is None:
        return 2
    return min(max(int(results), 1), 8000)


def validate_thingspeak_field_id(field_id: int) -> int:
    field_id = int(field_id)
    if field_id < 1 or field_id > 8:
        raise HTTPException(status_code=400, detail="ThingSpeak field_id 必须在 1 到 8 之间")
    return field_id


def read_thingspeak_feeds(results: int = 2, _: UserDB = Depends(get_admin_user)):
    channel_id = thingspeak_channel_id()
    data = request_thingspeak_json(
        f"/channels/{channel_id}/feeds.json",
        {"api_key": thingspeak_read_api_key(), "results": bounded_thingspeak_results(results)},
    )
    return {"source": "thingspeak", "data": data}


def read_thingspeak_field(field_id: int, results: int = 2, _: UserDB = Depends(get_admin_user)):
    channel_id = thingspeak_channel_id()
    field_id = validate_thingspeak_field_id(field_id)
    data = request_thingspeak_json(
        f"/channels/{channel_id}/fields/{field_id}.json",
        {"api_key": thingspeak_read_api_key(), "results": bounded_thingspeak_results(results)},
    )
    return {"source": "thingspeak", "data": data}


def read_thingspeak_status(results: int = 2, _: UserDB = Depends(get_admin_user)):
    channel_id = thingspeak_channel_id()
    data = request_thingspeak_json(
        f"/channels/{channel_id}/status.json",
        {"api_key": thingspeak_read_api_key(), "results": bounded_thingspeak_results(results)},
    )
    return {"source": "thingspeak", "data": data}


def write_thingspeak_feed(payload: dict, _: UserDB = Depends(get_admin_user)):
    allowed_keys = {
        "field1",
        "field2",
        "field3",
        "field4",
        "field5",
        "field6",
        "field7",
        "field8",
        "lat",
        "long",
        "elevation",
        "status",
        "created_at",
        "timezone",
    }
    params = {"api_key": thingspeak_write_api_key()}
    for key, value in (payload or {}).items():
        if key in allowed_keys and value is not None:
            params[key] = value

    if len(params) == 1:
        raise HTTPException(status_code=400, detail="至少需要提交一个 ThingSpeak 字段")

    data = request_thingspeak_json("/update.json", params, method="POST")
    return {"msg": "ThingSpeak 数据已写入", "source": "thingspeak", "data": data}


def thingspeak_event_id(feed: dict) -> str:
    entry_id = str(feed.get("entry_id") or feed.get("id") or "").strip()
    if entry_id:
        return f"thingspeak-{entry_id}"
    return f"thingspeak-{feed.get('created_at') or time.strftime('%Y-%m-%dT%H:%M:%S')}"


def is_thingspeak_entry_synced(db: Session, event_id: str) -> bool:
    return (
        db.query(ExternalEventSyncDB)
        .filter(ExternalEventSyncDB.source_platform == "thingspeak", ExternalEventSyncDB.event_id == event_id)
        .first()
        is not None
    )


def mark_thingspeak_entry_synced(db: Session, event_id: str, timestamp: str, feed: dict) -> None:
    db.add(
        ExternalEventSyncDB(
            source_platform="thingspeak",
            event_id=event_id,
            timestamp=timestamp,
            raw_payload_json=_json_text(feed),
        )
    )


def base_thingspeak_payload(feed: dict, channel_id: str, room_number: str, device_id: str) -> dict:
    entry_id = str(feed.get("entry_id") or feed.get("id") or "").strip()
    event_id = thingspeak_event_id(feed)
    return {
        "event_id": event_id,
        "device_id": device_id,
        "room_number": room_number,
        "timestamp": str(feed.get("created_at") or time.strftime("%Y-%m-%dT%H:%M:%S")),
        "source": "device",
        "source_platform": "thingspeak",
        "metadata": {
            "channel_id": channel_id,
            "entry_id": entry_id,
            "fields": {
                "field1": "tap_water_flow",
                "field2": "grey_water_flow",
                "field3": "grey_water_ph",
                "field4": "grey_water_turbidity",
            },
        },
        "raw_thingspeak_feed": feed,
    }


def thingspeak_feed_to_greywater_payload(feed: dict, channel_id: str, room_number: str, device_id: str) -> dict | None:
    field_value = feed.get("field2")
    if field_value is None or field_value == "":
        return None

    payload = base_thingspeak_payload(feed, channel_id, room_number, device_id)
    payload["event_type"] = "other"
    payload["event_count"] = 1
    payload["volume_liters"] = parse_non_negative_int(field_value, "field2", default=0)
    return payload


def upsert_thingspeak_device(db: Session, device_id: str, room_number: str, timestamp: str, channel_id: str) -> GreywaterDeviceDB:
    device = db.query(GreywaterDeviceDB).filter(GreywaterDeviceDB.device_id == device_id).first()
    if not device:
        device = GreywaterDeviceDB(device_id=device_id)
        db.add(device)
    device.room_number = room_number
    device.device_type = "thingspeak_channel"
    device.status = "online"
    device.last_seen_at = timestamp
    device.source_platform = "thingspeak"
    device.metadata_json = _json_text({"channel_id": channel_id})
    return device


def sync_thingspeak_feed(feed: dict, channel_id: str, room_number: str, device_id: str, db: Session) -> dict:
    timestamp = str(feed.get("created_at") or time.strftime("%Y-%m-%dT%H:%M:%S"))
    event_id = thingspeak_event_id(feed)
    if is_thingspeak_entry_synced(db, event_id):
        return {"synced": False, "reason": "duplicate"}

    synced_records: dict[str, object] = {}
    raw_payload = base_thingspeak_payload(feed, channel_id, room_number, device_id)
    upsert_thingspeak_device(db, device_id, room_number, timestamp, channel_id)

    tap_water_flow = parse_non_negative_int(feed.get("field1"), "field1", default=None)
    if tap_water_flow is not None:
        water_flow = WaterFlowDB(room_number=room_number, flow_rate=tap_water_flow, timestamp=timestamp)
        db.add(water_flow)
        synced_records["tap_water_flow"] = water_flow

    greywater_payload = thingspeak_feed_to_greywater_payload(feed, channel_id, room_number, device_id)
    if greywater_payload:
        usage_data = GreywaterUsageData(
            room_number=room_number,
            device_id=device_id,
            usage_type="other",
            event_count=1,
            volume_liters=greywater_payload["volume_liters"],
            timestamp=timestamp,
            source="device",
            raw_payload={**greywater_payload, "tap_water_flow": tap_water_flow},
        )
        greywater_usage = build_greywater_usage_record(room_number, usage_data)
        db.add(greywater_usage)
        synced_records["greywater_usage"] = greywater_usage

    ph_value = parse_non_negative_float(feed.get("field3"), "field3", default=None)
    turbidity_value = parse_non_negative_int(feed.get("field4"), "field4", default=None)
    if ph_value is not None or turbidity_value is not None:
        quality = GreywaterQualityDB(
            room_number=room_number,
            device_id=device_id,
            ph_value=ph_value,
            turbidity_value=turbidity_value,
            source="device",
            timestamp=timestamp,
            raw_payload_json=_json_text(raw_payload),
        )
        db.add(quality)
        synced_records["greywater_quality"] = quality

    if turbidity_value is not None:
        turbidity = SewageTurbidityDB(room_number=room_number, turbidity_value=turbidity_value, timestamp=timestamp)
        db.add(turbidity)
        synced_records["greywater_turbidity"] = turbidity

    mark_thingspeak_entry_synced(db, event_id, timestamp, feed)
    return {"synced": True, "records": synced_records}


def sync_thingspeak_events(results: int = 2, db: Session = Depends(get_db), _: UserDB = Depends(get_admin_user)):
    channel_id = thingspeak_channel_id()
    room_number = thingspeak_room_number()
    device_id = thingspeak_device_id(channel_id)
    data = request_thingspeak_json(
        f"/channels/{channel_id}/feeds.json",
        {"api_key": thingspeak_read_api_key(), "results": bounded_thingspeak_results(results)},
    )
    feeds = data.get("feeds", []) if isinstance(data, dict) else []
    synced = 0
    skipped = 0
    records = []

    for feed in feeds:
        if not isinstance(feed, dict):
            skipped += 1
            continue
        result = sync_thingspeak_feed(feed, channel_id, room_number, device_id, db)
        if not result["synced"]:
            skipped += 1
            continue
        synced += 1
        records.append({"event_id": thingspeak_event_id(feed)})

    db.commit()

    return {
        "msg": "ThingSpeak 同步完成",
        "source": "thingspeak",
        "synced": synced,
        "skipped": skipped,
        "records": records,
    }

# ==================== 5. API 路由 ====================
api_router = APIRouter()

@api_router.get("/users", response_model=list[PublicUser])
def read_users(_: UserDB = Depends(get_admin_user), db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    return [serialize_public_user(user) for user in users]

# 注册接口 (无加密版)
@api_router.post("/register")
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    # 1. 检查用户名是否存在
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 2. 创建用户
    new_user = UserDB(
        username=user.username,
        password_hash=hash_password(user.password),
        room_number=user.room_number,
        role="user"
    )
    
    # 3. 写入数据库
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"msg": "注册成功", "username": new_user.username}

# 登录接口 (无加密版)
@api_router.post("/login", response_model=LoginResponse)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    # 1. 查找用户
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="用户名或密码错误")

    # 2. 验证密码
    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="用户名或密码错误")

    if password_needs_upgrade(db_user.password_hash):
        db_user.password_hash = hash_password(user.password)
        db.commit()
        db.refresh(db_user)
    
    return {
        "msg": "登录成功",
        "username": db_user.username,
        "room_number": db_user.room_number,
        "role": db_user.role,
        "token": create_session_token(db_user),
    }

# 提交水流量数据接口
@api_router.post("/water_flow")
def create_water_flow(data: WaterFlowData, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    room_number = ensure_room_access(data.room_number, current_user)
    new_flow = WaterFlowDB(room_number=room_number, flow_rate=data.flow_rate, timestamp=data.timestamp)
    db.add(new_flow)
    db.commit()
    db.refresh(new_flow)
    return {"msg": "水流量数据提交成功", "data": new_flow}

# 获取水流量数据接口
@api_router.get("/water_flow/{room_number}")
def get_water_flow(room_number: str, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    authorized_room = ensure_room_access(room_number, current_user)
    flows = db.query(WaterFlowDB).filter(WaterFlowDB.room_number == authorized_room).all()
    return flows

# 提交污水浊度数据接口
@api_router.post("/sewage_turbidity")
def create_sewage_turbidity(data: SewageTurbidityData, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    room_number = ensure_room_access(data.room_number, current_user)
    new_turbidity = SewageTurbidityDB(room_number=room_number, turbidity_value=data.turbidity_value, timestamp=data.timestamp)
    db.add(new_turbidity)
    db.commit()
    db.refresh(new_turbidity)
    return {"msg": "污水浊度数据提交成功", "data": new_turbidity}

# 获取污水浊度数据接口
@api_router.get("/sewage_turbidity/{room_number}")
def get_sewage_turbidity(room_number: str, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    authorized_room = ensure_room_access(room_number, current_user)
    turbidity_data = db.query(SewageTurbidityDB).filter(SewageTurbidityDB.room_number == authorized_room).all()
    return turbidity_data

# 提交水费数据接口
@api_router.post("/water_bill")
def create_water_bill(data: WaterBillData, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    room_number = ensure_room_access(data.room_number, current_user)
    new_bill = WaterBillDB(room_number=room_number, amount=data.amount, month=data.month)
    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)
    return {"msg": "水费数据提交成功", "data": new_bill}

# 获取水费数据接口
@api_router.get("/water_bill/{room_number}")
def get_water_bill(room_number: str, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    authorized_room = ensure_room_access(room_number, current_user)
    bills = db.query(WaterBillDB).filter(WaterBillDB.room_number == authorized_room).all()
    return bills


@api_router.post("/greywater_usage")
def create_greywater_usage(
    data: GreywaterUsageData,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    room_number = ensure_room_access(data.room_number, current_user)
    new_usage = build_greywater_usage_record(room_number, data)
    db.add(new_usage)
    db.commit()
    db.refresh(new_usage)
    return {"msg": "灰水用量数据提交成功", "data": serialize_greywater_usage(new_usage)}


@api_router.get("/greywater_usage/{room_number}")
def get_greywater_usage(
    room_number: str,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    authorized_room = ensure_room_access(room_number, current_user)
    records = (
        db.query(GreywaterUsageDB)
        .filter(GreywaterUsageDB.room_number == authorized_room)
        .order_by(GreywaterUsageDB.timestamp.desc())
        .all()
    )
    return [serialize_greywater_usage(record) for record in records]


@api_router.get("/greywater_summary/{room_number}")
def get_greywater_summary(
    room_number: str,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    authorized_room = ensure_room_access(room_number, current_user)
    records = (
        db.query(GreywaterUsageDB)
        .filter(GreywaterUsageDB.room_number == authorized_room)
        .order_by(GreywaterUsageDB.timestamp.desc())
        .all()
    )
    total_liters = sum(int(record.volume_liters or 0) for record in records)
    flush_count = sum(int(record.event_count or 0) for record in records if record.usage_type == "toilet_flush")
    return {
        "room_number": authorized_room,
        "greywater_liters": total_liters,
        "flush_count": flush_count,
        "usage_distribution": _usage_distribution(records),
        "recent_records": [serialize_greywater_usage(record) for record in records[:10]],
    }


@api_router.get("/greywater_quality/{room_number}")
def get_greywater_quality(
    room_number: str,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    authorized_room = ensure_room_access(room_number, current_user)
    records = (
        db.query(GreywaterQualityDB)
        .filter(GreywaterQualityDB.room_number == authorized_room)
        .order_by(GreywaterQualityDB.timestamp.desc())
        .all()
    )
    return [serialize_greywater_quality(record) for record in records]


@api_router.get("/saving_stats/{room_number}")
def get_saving_stats(
    room_number: str,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    authorized_room = ensure_room_access(room_number, current_user)
    return calculate_saving_stats(authorized_room, db)


@api_router.post("/devices")
def upsert_greywater_device(
    data: GreywaterDeviceData,
    db: Session = Depends(get_db),
    _: UserDB = Depends(get_admin_user),
):
    status = normalize_device_status(data.status)
    device = db.query(GreywaterDeviceDB).filter(GreywaterDeviceDB.device_id == data.device_id).first()
    if not device:
        device = GreywaterDeviceDB(device_id=data.device_id)
        db.add(device)
    device.room_number = data.room_number
    device.device_type = data.device_type
    device.status = status
    device.last_seen_at = data.last_seen_at
    device.source_platform = data.source_platform
    device.metadata_json = _json_text(data.metadata)
    db.commit()
    db.refresh(device)
    return {"msg": "灰水设备已保存", "data": serialize_greywater_device(device)}


@api_router.get("/devices")
def list_greywater_devices(db: Session = Depends(get_db), _: UserDB = Depends(get_admin_user)):
    devices = db.query(GreywaterDeviceDB).order_by(GreywaterDeviceDB.device_id.asc()).all()
    return [serialize_greywater_device(device) for device in devices]


@api_router.get("/devices/{device_id}")
def get_greywater_device(
    device_id: str,
    db: Session = Depends(get_db),
    _: UserDB = Depends(get_admin_user),
):
    device = db.query(GreywaterDeviceDB).filter(GreywaterDeviceDB.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="设备不存在")
    latest_usage = (
        db.query(GreywaterUsageDB)
        .filter(GreywaterUsageDB.device_id == device_id)
        .order_by(GreywaterUsageDB.timestamp.desc())
        .first()
    )
    return {
        "device": serialize_greywater_device(device),
        "latest_usage": serialize_greywater_usage(latest_usage) if latest_usage else None,
    }


api_router.add_api_route("/integrations/thingspeak/feeds", read_thingspeak_feeds, methods=["GET"])
api_router.add_api_route("/integrations/thingspeak/fields/{field_id}", read_thingspeak_field, methods=["GET"])
api_router.add_api_route("/integrations/thingspeak/status", read_thingspeak_status, methods=["GET"])
api_router.add_api_route("/integrations/thingspeak/write", write_thingspeak_feed, methods=["POST"])
api_router.add_api_route("/integrations/thingspeak/sync", sync_thingspeak_events, methods=["POST"])


@api_router.post("/integrations/thingcloud/events")
def receive_thingcloud_event(
    payload: dict,
    db: Session = Depends(get_db),
    _: UserDB | None = Depends(authorize_thingcloud_ingestion),
):
    room_number = str(payload.get("room_number") or "").strip()
    device_id = str(payload.get("device_id") or "").strip() or None
    if not room_number:
        raise HTTPException(status_code=400, detail="缺少房间号")
    if not device_id:
        raise HTTPException(status_code=400, detail="缺少设备编号")

    timestamp = str(payload.get("timestamp") or time.strftime("%Y-%m-%dT%H:%M:%S"))
    usage_type = normalize_thingcloud_usage_type(str(payload.get("usage_type") or payload.get("event_type") or "toilet_flush"))
    event_count = parse_non_negative_int(payload.get("event_count"), "event_count", default=1)
    volume_liters = parse_non_negative_int(payload.get("volume_liters"), "volume_liters", default=None)
    device_status = normalize_device_status(str(payload.get("status") or "online"))
    existing_usage = find_existing_thingcloud_usage(db, device_id, timestamp, usage_type, payload)
    if existing_usage:
        return {"msg": "灰水用量数据已存在", "data": serialize_greywater_usage(existing_usage)}
    usage_data = GreywaterUsageData(
        room_number=room_number,
        device_id=device_id,
        usage_type=usage_type,
        event_count=event_count,
        volume_liters=volume_liters,
        timestamp=timestamp,
        source=str(payload.get("source") or "device"),
        raw_payload=payload,
    )
    usage_record = build_greywater_usage_record(room_number, usage_data)
    db.add(usage_record)

    device = db.query(GreywaterDeviceDB).filter(GreywaterDeviceDB.device_id == device_id).first()
    if not device:
        device = GreywaterDeviceDB(device_id=device_id)
        db.add(device)
    device.room_number = room_number
    device.device_type = str(payload.get("device_type") or device.device_type or "toilet_flush_sensor")
    device.status = device_status
    device.last_seen_at = timestamp
    device.source_platform = str(payload.get("source_platform") or "thingcloud")
    metadata = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else None
    device.metadata_json = _json_text(metadata)
    db.commit()
    db.refresh(usage_record)
    db.refresh(device)

    return {"msg": "灰水用量数据提交成功", "data": serialize_greywater_usage(usage_record)}


@api_router.post("/integrations/thingcloud/sync")
def sync_thingcloud_events(_: UserDB = Depends(get_admin_user)):
    return {
        "msg": "ThingCloud sync endpoint is ready for hardware integration",
        "synced": 0,
        "source": "mock",
    }


@api_router.post("/saving_plans/{room_number}/generate")
def generate_saving_plan(
    room_number: str,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    authorized_room = ensure_room_access(room_number, current_user)
    plan = generate_rule_based_saving_plan(authorized_room, db)
    return {"msg": "节水计划已生成", "data": serialize_saving_plan(plan)}


@api_router.get("/saving_plans/{room_number}/latest")
def get_latest_saving_plan(
    room_number: str,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    authorized_room = ensure_room_access(room_number, current_user)
    plan = (
        db.query(SavingPlanDB)
        .filter(SavingPlanDB.room_number == authorized_room, SavingPlanDB.status == "active")
        .order_by(SavingPlanDB.created_at.desc(), SavingPlanDB.id.desc())
        .first()
    )
    if not plan:
        raise HTTPException(status_code=404, detail="暂无节水计划")
    return {"data": serialize_saving_plan(plan)}


@api_router.get("/saving_plans/{room_number}")
def list_saving_plans(
    room_number: str,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    authorized_room = ensure_room_access(room_number, current_user)
    plans = (
        db.query(SavingPlanDB)
        .filter(SavingPlanDB.room_number == authorized_room)
        .order_by(SavingPlanDB.created_at.desc(), SavingPlanDB.id.desc())
        .all()
    )
    return [serialize_saving_plan(plan) for plan in plans]
