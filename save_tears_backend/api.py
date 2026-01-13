from fastapi import FastAPI, HTTPException, Depends, APIRouter
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# ==================== 1. 基础配置 ====================
# 连接数据库
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@127.0.0.1:3306/save_tears"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

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

# ==================== 4. 辅助函数 ====================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== 5. API 路由 ====================
api_router = APIRouter()

@api_router.get("/users")
def read_users(db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    return users

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
@api_router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    # 1. 查找用户
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="用户名或密码错误")

    # 2. 验证密码 (直接比较明文密码)
    if db_user.password_hash != user.password:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    return {"msg": "登录成功 (无加密模式)", "username": db_user.username, "room_number": db_user.room_number, "role": db_user.role}

# 提交水流量数据接口
@api_router.post("/water_flow")
def create_water_flow(data: WaterFlowData, db: Session = Depends(get_db)):
    new_flow = WaterFlowDB(room_number=data.room_number, flow_rate=data.flow_rate, timestamp=data.timestamp)
    db.add(new_flow)
    db.commit()
    db.refresh(new_flow)
    return {"msg": "水流量数据提交成功", "data": new_flow}

# 获取水流量数据接口
@api_router.get("/water_flow/{room_number}")
def get_water_flow(room_number: str, db: Session = Depends(get_db)):
    flows = db.query(WaterFlowDB).filter(WaterFlowDB.room_number == room_number).all()
    return flows

# 提交污水浊度数据接口
@api_router.post("/sewage_turbidity")
def create_sewage_turbidity(data: SewageTurbidityData, db: Session = Depends(get_db)):
    new_turbidity = SewageTurbidityDB(room_number=data.room_number, turbidity_value=data.turbidity_value, timestamp=data.timestamp)
    db.add(new_turbidity)
    db.commit()
    db.refresh(new_turbidity)
    return {"msg": "污水浊度数据提交成功", "data": new_turbidity}

# 获取污水浊度数据接口
@api_router.get("/sewage_turbidity/{room_number}")
def get_sewage_turbidity(room_number: str, db: Session = Depends(get_db)):
    turbidity_data = db.query(SewageTurbidityDB).filter(SewageTurbidityDB.room_number == room_number).all()
    return turbidity_data

# 提交水费数据接口
@api_router.post("/water_bill")
def create_water_bill(data: WaterBillData, db: Session = Depends(get_db)):
    new_bill = WaterBillDB(room_number=data.room_number, amount=data.amount, month=data.month)
    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)
    return {"msg": "水费数据提交成功", "data": new_bill}

# 获取水费数据接口
@api_router.get("/water_bill/{room_number}")
def get_water_bill(room_number: str, db: Session = Depends(get_db)):
    bills = db.query(WaterBillDB).filter(WaterBillDB.room_number == room_number).all()
    return bills
