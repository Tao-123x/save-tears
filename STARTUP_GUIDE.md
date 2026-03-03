Save Tears 项目启动手册
本手册将指导你如何启动 后端、Web 前端 和 微信小程序。

前提条件

- Python 3.8+ (用于后端)
- Node.js 14+ (用于前端和小程序)
- MySQL 8.0+ (数据库)
- 微信开发者工具 (用于预览小程序)

---

1. 启动后端 (Backend)

后端提供 API 服务，必须首先启动。
步骤
1. 启动 MySQL 服务
   如果不确定是否已启动，运行：
   ```bash
   brew services start mysql
   ```
   注意: 本项目配置为使用 `root` 用户且**无密码**连接。如果你的数据库有密码，请修改 `save_tears_backend/main.py` 和 `api.py` 中的 `SQLALCHEMY_DATABASE_URL`。

2. **进入后端目录**
   ```bash
   cd save_tears_backend
   ```

3. **激活虚拟环境**
   ```bash
   source venv/bin/activate
   ```

4. **启动服务**
   ```bash
   python main.py
   ```

**成功标志**: 终端显示 `Uvicorn running on http://0.0.0.0:8000`。

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
   npm run dev:mp-weixin
   ```
   *保持此终端窗口开启，它会实时监听修改并重新编译。*

4. **导入微信开发者工具**
   - 打开 **微信开发者工具**。
   - 点击 **导入项目**。
   - 选择目录：`save_tears_miniprogram/dist/dev/mp-weixin`。
   - **AppID**: 使用测试号或你自己的 AppID。

**成功标志**: 微信开发者工具中能正常显示页面预览。

---

## 常见问题排查

**Q: 后端报错 `Access denied for user 'root'@'localhost'`**
A: 数据库密码错误。
- 检查 MySQL 是否运行。
- 确认你的 MySQL root 密码。如果是无密码，代码已配置好。如果有密码，请在 `main.py` 中更新连接字符串：`mysql+pymysql://root:你的密码@127.0.0.1:3306/save_tears`。

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
- **MySQL 8.0+** (database)
- **WeChat Developer Tools** (for previewing the mini program)

---

## 1. Start the Backend

The backend provides API services and must be started first.

### Steps
1. **Start MySQL Service**
   If you're unsure if it's running, execute:
   ```bash
   brew services start mysql
   ```
   > **Note**: This project is configured to connect using the `root` user with **no password**. If your database has a password, please modify the `SQLALCHEMY_DATABASE_URL` in `save_tears_backend/main.py` and `api.py`.

2. **Enter the Backend Directory**
   ```bash
   cd save_tears_backend
   ```

3. **Activate the Virtual Environment**
   ```bash
   source venv/bin/activate
   ```

4. **Start the Service**
   ```bash
   python main.py
   ```

**Success Indicator**: The terminal displays `Uvicorn running on http://0.0.0.0:8000`.

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
   npm run dev:mp-weixin
   ```
   *Keep this terminal window open; it will listen for changes and recompile in real-time.*

4. **Import into WeChat Developer Tools**
   - Open **WeChat Developer Tools**.
   - Click **Import Project**.
   - Select the directory: `save_tears_miniprogram/dist/dev/mp-weixin`.
   - **AppID**: Use a test AppID or your own AppID.

**Success Indicator**: The pages can be previewed normally in WeChat Developer Tools.

---

## ❓ Troubleshooting

**Q: Backend reports `Access denied for user 'root'@'localhost'`**
A: Incorrect database password.
- Check if MySQL is running.
- Verify your MySQL root password. If there is no password, the code is already configured correctly. If you have a password, update the connection string in `main.py`: `mysql+pymysql://root:YOUR_PASSWORD@127.0.0.1:3306/save_tears`.

**Q: Port already in use `Address already in use`**
A: A previous service was not shut down properly.
- Find the process occupying the port: `lsof -i :8000` (for backend) or `lsof -i :8080` (for frontend).
- Kill the process: `kill -9 <PID>`.

**Q: Mini program charts are not displaying**
A: Ensure you have run `npm install` to install `@qiun/ucharts`, and then rerun the compile command.
