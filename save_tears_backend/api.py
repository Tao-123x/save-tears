import os
import json
import time
import hmac
import base64
import hashlib

from fastapi import HTTPException, Depends, APIRouter, Header
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
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
TOKEN_TTL_SECONDS = int(os.getenv("SAVE_TEARS_TOKEN_TTL", "86400"))

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
    
    # 2. 直接使用明文密码 (跳过加密步骤) 🚀
    fake_hashed_password = user.password 
    
    # 3. 创建用户
    new_user = UserDB(
        username=user.username,
        password_hash=fake_hashed_password,
        room_number=user.room_number,
        role="user"
    )
    
    # 4. 写入数据库
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"msg": "注册成功 (无加密模式)", "username": new_user.username}

# 登录接口 (无加密版)
@api_router.post("/login", response_model=LoginResponse)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    # 1. 查找用户
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="用户名或密码错误")

    # 2. 验证密码 (直接比较明文密码)
    if db_user.password_hash != user.password:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
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
