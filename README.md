# Save Tears (Water Conservation Management System)

Welcome to the **Save Tears** project repository! This is a comprehensive water conservation and management system aimed at tracking, analyzing, and optimizing water usage. Developed to promote sustainability, the system is designed with a modern architecture spanning a robust backend, an intuitive web dashboard, and a convenient mobile mini-program.

---

## 🌟 Features
- **Multi-Platform Support**: Includes both a complete mobile mini-program and a Web-based management dashboard.
- **Modern Architecture**: Adopts a front-end and back-end separation architecture, utilizing the popular Vue 3 and FastAPI frameworks.
- **Data Visualization**: Employs charting libraries like `@qiun/ucharts` to provide intuitive statistics on water usage data.
- **Automated Deployment**: Provides a comprehensive deployment script (`deploy.sh`) for one-click server deployment and configuration.

---

## 🛠 Tech Stack

### 1. Backend Service (`save_tears_backend`)
- **Core Framework**: Python 3.8+, **FastAPI**
- **ORM & Database**: SQLAlchemy
- **Supported Databases**: MySQL / MariaDB
- **Server**: Uvicorn

### 2. Mini Program (`save_tears_miniprogram`)
- **Framework**: **uni-app** (with Vue 3)
- **Charts**: `@qiun/ucharts`
- **Build Tool**: Vite

### 3. Web Dashboard (`save_tears_frontend`)
- **Core Framework**: **Vue.js 3**
- **Routing**: Vue Router 4
- **Responsive Layout**: Adapts to desktop and some mobile layouts, providing clear data charts and usage dashboards.

### 4. DevOps (Deployment)
- **Recommended OS**: Huawei Cloud EulerOS / CentOS
- **Reverse Proxy & Static Hosting**: Nginx
- **Process Management**: Systemd
- **Automation Tools**: Shell scripts (`deploy.sh` and `setup_ssh.exp`)

---

## 📁 Project Structure

```text
save_tears/
├── save_tears_backend/       # FastAPI backend source code (models & APIs)
├── save_tears_frontend/      # Vue 3 web dashboard source code
├── save_tears_miniprogram/   # uni-app mini-program source code
├── deployment/               # Deployment configurations and extra resources
├── DEVELOPMENT_LOG.md        # Detailed development and refactoring log
├── IMAGE_ASSETS_LIST.md      # List of static assets used in the project
├── STARTUP_GUIDE.md          # Startup and installation guide
├── deploy.sh                 # Core script for one-click deployment & environment setup
├── start_public_access.sh    # Script for quick network and public access configuration
└── walkthrough.md            # System demonstration and feature verification guide
```

---

## 🚀 Quick Start Guide

*(For more detailed startup steps and environment variable configurations, please refer to the `STARTUP_GUIDE.md`)*

### Running Everything with Docker
1. From the repository root, run `docker compose up --build`
2. Open the H5 frontend at `http://localhost:5173`
3. The backend API will be available at `http://localhost:8000`

The Docker setup uses a named volume for the backend SQLite database, so a fresh collaborator environment starts with an empty database. Register a new account first if no users exist yet.

### Production Deployment
Use the production compose file when deploying to a server with a domain name:

```bash
cp .env.production.example .env.production
nano .env.production
docker compose --env-file .env.production -f docker-compose.prod.yml up -d --build
```

The production stack serves:
- H5 frontend at `https://<DOMAIN>/`
- Backend API through `https://<DOMAIN>/api/`

Open ports `80` and `443` in the server firewall before starting the stack. Keep backend port `8000` private.

### Running the Backend
1. Navigate to the directory: `cd save_tears_backend`
2. Create a virtual environment: `python3 -m venv .venv && source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Start the service: `python main.py`

The backend now defaults to a local SQLite database file for local development. If you want to use MySQL instead, set `SAVE_TEARS_DB_URL` before starting the server.

### Running the Web Frontend
1. Navigate to the directory: `cd save_tears_miniprogram`
2. Install dependencies: `npm install`
3. Run the project: `npm run dev:h5`

For H5 local development, the frontend now defaults to `http://<current-host>:8000`.
If you need to point the mini program or another device to a different backend host, set `VITE_API_BASE_URL` before startup or configure `api_base_url` in local storage.

### Running the Mini Program
1. Navigate to the directory: `cd save_tears_miniprogram`
2. Install dependencies: `npm install`
3. Run `npm run build:mp-weixin`
4. Import `save_tears_miniprogram/dist/build/mp-weixin` into WeChat Developer Tools.

---

## 🌐 Production Environment
The project is currently deployed to a production environment for testing. In local development, the H5 frontend talks to the backend on port `8000` using the current browser host.

For automated system deployment, you can execute the `deploy.sh` script in the root directory. It includes Nginx installation, Systemd daemon registration, and Python environment setup.

For local cross-machine validation, prefer the Docker setup above so collaborators can run the same frontend/backend stack without relying on host-specific Node or Python environments.

---

## 📝 Maintenance & Contributors
The project underwent a comprehensive tech stack upgrade in 2026. If you encounter any code quality or deployment issues during testing or development, please submit an Issue or refer to the historical development document `DEVELOPMENT_LOG.md`.

---
**Built with ❤️ for Water Conservation**
