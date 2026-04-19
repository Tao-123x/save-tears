Save Tears 项目启动手册
本手册将指导你如何启动 后端、Web 前端 和 微信小程序。

前提条件

- Python 3.8+ (用于后端)
- Node.js 14+ (用于前端和小程序)
- 微信开发者工具 (用于预览小程序)

---

1. 启动后端 (Backend)

后端提供 API 服务，必须首先启动。
步骤
1. **进入后端目录**
   ```bash
   cd save_tears_backend
   ```

2. **创建并激活虚拟环境**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **启动服务**
   ```bash
   python main.py
   ```

**成功标志**: 终端显示 `Uvicorn running on http://0.0.0.0:8000`。

默认情况下，后端会使用当前目录下的 `save_tears.db` SQLite 数据库文件。
如果你想改用 MySQL，请在启动前设置 `SAVE_TEARS_DB_URL`。

---

##  2. 启动 Web 前端 (Frontend)

这是用于浏览器的管理后台或用户界面。

### 步骤
1. **进入前端目录**
   ```bash
   cd save_tears_frontend
   ```

2. **安装依赖 (仅首次需要)**
   ```bash
   npm install
   ```

3. **启动开发服务器**
   ```bash
   npm run serve
   ```

**成功标志**: 终端显示访问地址，通常是 `http://localhost:8080`。

---

##  3. 启动微信小程序 (Mini Program)

这是基于 uni-app 开发的小程序项目。

### 步骤
1. **进入小程序目录**
   ```bash
   cd save_tears_miniprogram
   ```

2. **安装依赖 (仅首次需要)**
   ```bash
   npm install
   ```

3. **编译为微信小程序**
   ```bash
   npm run build:mp-weixin
   ```

4. **导入微信开发者工具**
   - 打开 **微信开发者工具**。
   - 点击 **导入项目**。
   - 选择目录：`save_tears_miniprogram/dist/build/mp-weixin`。
   - **AppID**: 使用测试号或你自己的 AppID。

**成功标志**: 微信开发者工具中能正常显示页面预览。

---

## 常见问题排查

**Q: 后端想改用 MySQL**
A: 启动前设置环境变量 `SAVE_TEARS_DB_URL`，例如：
```bash
export SAVE_TEARS_DB_URL="mysql+pymysql://root:你的密码@127.0.0.1:3306/save_tears"
```

**Q: 端口被占用 `Address already in use`**
A: 之前的服务没关掉。
- 查找占用端口的进程：`lsof -i :8000` (后端) 或 `lsof -i :8080` (前端)。
- 杀掉进程：`kill -9 <PID>`。

**Q: 小程序图表不显示**
A: 确保已运行 `npm install` 安装了 `@qiun/ucharts`，并且重新运行了编译命令。

---
---

# Save Tears Project Startup Guide

This guide will walk you through how to start the **Backend**, **Web Frontend**, and **WeChat Mini Program**.

## Prerequisites

- **Python 3.8+** (for the backend)
- **Node.js 14+** (for frontend and mini program)
- **WeChat Developer Tools** (for previewing the mini program)

---

## 1. Start the Backend

The backend provides API services and must be started first.

### Steps
1. **Enter the Backend Directory**
   ```bash
   cd save_tears_backend
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the Service**
   ```bash
   python main.py
   ```

**Success Indicator**: The terminal displays `Uvicorn running on http://0.0.0.0:8000`.

By default, the backend uses a local SQLite database file named `save_tears.db`.
If you want to use MySQL instead, set `SAVE_TEARS_DB_URL` before starting the server.

---

##  2. Start the Web Frontend

This is the management dashboard or user interface for the browser.

### Steps
1. **Enter the Frontend Directory**
   ```bash
   cd save_tears_frontend
   ```

2. **Install Dependencies (First time only)**
   ```bash
   npm install
   ```

3. **Start the Development Server**
   ```bash
   npm run serve
   ```

**Success Indicator**: The terminal shows the access URL, usually `http://localhost:8080`.

---

## 3. Start the WeChat Mini Program

This is the mini-program project developed based on uni-app.

### Steps
1. **Enter the Mini Program Directory**
   ```bash
   cd save_tears_miniprogram
   ```

2. **Install Dependencies (First time only)**
   ```bash
   npm install
   ```

3. **Compile for WeChat Mini Program**
   ```bash
   npm run build:mp-weixin
   ```

4. **Import into WeChat Developer Tools**
   - Open **WeChat Developer Tools**.
   - Click **Import Project**.
   - Select the directory: `save_tears_miniprogram/dist/build/mp-weixin`.
   - **AppID**: Use a test AppID or your own AppID.

**Success Indicator**: The pages can be previewed normally in WeChat Developer Tools.

---

##  Troubleshooting

**Q: I want to use MySQL instead of SQLite**
A: Set the `SAVE_TEARS_DB_URL` environment variable before starting the backend, for example:
```bash
export SAVE_TEARS_DB_URL="mysql+pymysql://root:YOUR_PASSWORD@127.0.0.1:3306/save_tears"
```

**Q: Port already in use `Address already in use`**
A: A previous service was not shut down properly.
- Find the process occupying the port: `lsof -i :8000` (for backend) or `lsof -i :8080` (for frontend).
- Kill the process: `kill -9 <PID>`.

**Q: Mini program charts are not displaying**
A: Ensure you have run `npm install` to install `@qiun/ucharts`, and then rerun the compile command.
