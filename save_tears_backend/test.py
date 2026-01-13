# test.py
import uvicorn
from fastapi import FastAPI

print("--- 1. Python 正在运行 ---")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "测试成功！环境没问题！"}

print("--- 2. 代码加载完毕，准备启动 ---")

if __name__ == "__main__":
    # 强制让它只跑简单的 Web 服务
    uvicorn.run(app, host="127.0.0.1", port=8001)