from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from api import api_router # 导入 api_router

# ==================== 1. 基础配置 ====================
# 连接数据库
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@127.0.0.1:3306/save_tears"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==================== 2. 数据库模型 ====================
# 这些模型也需要在api.py中定义，这里只是为了Base.metadata.create_all(bind=engine)
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

# 确保所有数据库模型都已创建
Base.metadata.create_all(bind=engine)

# ==================== 3. 主程序 ====================
app = FastAPI(title="Save Tears Backend", version="Day 2 - Lite")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "System Online (Lite Mode)"}

app.include_router(api_router)

# 启动入口
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)