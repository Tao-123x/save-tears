Save Tears 项目启动手册
本手册将指导你如何启动 后端、Web 前端 和 微信小程序。

前提条件

- Python 3.8+ (用于后端)
- Node.js 14+ (用于前端和小程序)
- Docker Desktop / Docker Engine + Docker Compose (用于容器化启动，可选)
- 微信开发者工具 (用于预览小程序)

---

0. 一条命令启动前后端（Docker，可选）

如果你只是想在干净环境里把项目跑起来，推荐直接使用 Docker。

```bash
docker compose up --build
```

启动后可访问：
- H5 前端：`http://localhost:5173`
- 后端接口：`http://localhost:8000`

说明：
- 容器版后端使用独立的 Docker volume 保存 SQLite 数据。
- 第一次启动时数据库通常是空的，如果没有现成账号，请先注册再登录。

---

0.1 服务器生产部署（域名 + HTTPS）

生产环境推荐使用 `docker-compose.prod.yml`。它会让：
- `https://你的域名/` 访问 H5 前端
- `https://你的域名/api/` 转发到后端
- 后端 `8000` 和前端容器 `80` 不直接暴露到公网

服务器前置条件：
- 域名 DNS 的 `A` 记录已指向服务器公网 IP
- 腾讯云轻量服务器防火墙已放行 `80` 和 `443`
- 服务器已安装 Docker 和 Docker Compose

部署步骤：

```bash
git clone https://github.com/Tao-123x/save-tears.git
cd save-tears
git checkout taox/save-tears-project-upload

cp .env.production.example .env.production
nano .env.production

docker compose --env-file .env.production -f docker-compose.prod.yml up -d --build
```

`.env.production` 至少需要填写：

```bash
DOMAIN=你的域名
ACME_EMAIL=你的邮箱
SAVE_TEARS_SECRET=一串足够长的随机密钥
SAVE_TEARS_TOKEN_TTL=86400
SAVE_TEARS_ADMIN_USERNAME=admin
SAVE_TEARS_ADMIN_PASSWORD=一个强管理员密码
SAVE_TEARS_ADMIN_ROOM=HQ
```

成功后访问：
- 前端：`https://你的域名/`
- 后端健康检查：`https://你的域名/api/health`

说明：
- `SAVE_TEARS_ADMIN_USERNAME` 和 `SAVE_TEARS_ADMIN_PASSWORD` 只用于首次创建管理员账号。
- 如果管理员已存在，默认不会覆盖密码；确实需要重置时，把 `SAVE_TEARS_ADMIN_RESET_PASSWORD=1` 后重启一次，再改回 `0`。
- 后端会把新注册用户密码保存为哈希；旧的明文密码账号在成功登录后会自动升级为哈希。

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

##  2. 启动 H5 前端 (Frontend)

当前仓库里的可运行浏览器前端是 `save_tears_miniprogram` 的 H5 模式。

### 步骤
1. **进入前端目录**
   ```bash
   cd save_tears_miniprogram
   ```

2. **安装依赖 (仅首次需要)**
   ```bash
   npm install
   ```

3. **启动开发服务器**
   ```bash
   npm run dev:h5
   ```

**成功标志**: 终端显示访问地址，通常是 `http://localhost:5173`。

H5 本地开发默认请求 `http://<当前浏览器主机>:8000`。如果需要连接到别的后端地址，请在启动前设置 `VITE_API_BASE_URL`。

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
- 查找占用端口的进程：`lsof -i :8000` (后端) 或 `lsof -i :5173` (前端)。
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
- **Docker Desktop / Docker Engine + Docker Compose** (optional, for containerized startup)
- **WeChat Developer Tools** (for previewing the mini program)

---

## 0. Start the H5 frontend and backend with Docker (Optional)

If you want a clean collaborator-friendly environment, run the project from the repository root:

```bash
docker compose up --build
```

After startup:
- H5 frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`

Notes:
- The containerized backend stores SQLite data in a Docker volume.
- A fresh environment usually has no users yet, so register an account before trying to log in.

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

The runnable browser frontend in this repository is the H5 mode of `save_tears_miniprogram`.

### Steps
1. **Enter the Frontend Directory**
   ```bash
   cd save_tears_miniprogram
   ```

2. **Install Dependencies (First time only)**
   ```bash
   npm install
   ```

3. **Start the Development Server**
   ```bash
   npm run dev:h5
   ```

**Success Indicator**: The terminal shows the access URL, usually `http://localhost:5173`.

For H5 local development, the frontend defaults to `http://<current-browser-host>:8000`.
If you need another backend address, set `VITE_API_BASE_URL` before startup.

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
- Find the process occupying the port: `lsof -i :8000` (for backend) or `lsof -i :5173` (for frontend).
- Kill the process: `kill -9 <PID>`.

**Q: Mini program charts are not displaying**
A: Ensure you have run `npm install` to install `@qiun/ucharts`, and then rerun the compile command.
