# Hanks-Semaphore (Python Backend Rewrite)

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/DevContainer-Ready-2496ED.svg?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

這是一個將 [Semaphore UI](https://github.com/semaphoreui/semaphore) 後端從 Go 語言遷移至 **Python (FastAPI)** 的現代化重構專案。
本專案保留了原版強大的 Ansible/Terraform/Shell 自動化任務執行能力，並改寫為 Python 生態系架構，以提升開發效率與擴充性。

## 🏗️ 架構與技術決策 (Architecture)

本專案由 **小go (架構師)** 與 **小py (開發)** 共同規劃，主要技術變更如下：

| 元件 | 原版 Semaphore (Go) | 新版 Hanks-Semaphore (Python) | 決策原因 |
| :--- | :--- | :--- | :--- |
| **Web Framework** | Gin (Go) | **FastAPI** (Python) | 原生非同步支援 (AsyncIO)、自動生成 OpenAPI 文件。 |
| **Concurrency** | Goroutines | **Celery / ARQ** + **Redis** | Python 需要獨立的 Task Queue 來處理長時間運行的 Ansible 任務，避免阻塞 API。 |
| **Database** | MySQL / BoltDB / Postgres | **PostgreSQL** (推薦) / MySQL | 使用 **SQLAlchemy (Async)** 作為 ORM，搭配 **Alembic** 管理遷移。 |
| **Real-time Logs** | Websockets (Go Channels) | **Websockets** + **Redis Pub/Sub** | 支援多 Worker 擴展，讓任務日誌能跨行程推送到前端。 |
| **Environment** | Binary / Docker | **Docker** + **DevContainers** | 統一開發與部署環境，解決 Python 依賴管理問題。 |

## 📂 專案結構 (Project Structure)

```text
hanks-semaphore/
├── .devcontainer/        # 你現有的 Dev Container 設定
├── backend/
│   ├── alembic/          # [新增] 資料庫遷移腳本 (取代 Go 的 migrations)
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   ├── auth.py       # 登入與認證
│   │   │       │   ├── projects.py   # 對應 Go 的 Project 邏輯
│   │   │       │   ├── users.py      # 你現有的 user 邏輯
│   │   │       │   └── tasks.py      # 觸發 Ansible 任務的接口
│   │   │       └── router.py
│   │   ├── core/
│   │   │   ├── config.py     # Pydantic Settings (環境變數管理)
│   │   │   ├── security.py   # JWT 處理, Password Hashing (Passlib)
│   │   │   └── celery_app.py # [新增] Celery 設定 (非同步任務核心)
│   │   ├── crud/             # 資料庫操作 (Create, Read, Update, Delete)
│   │   │   ├── base.py
│   │   │   └── crud_user.py
│   │   ├── db/
│   │   │   ├── base.py       # SQLAlchemy Base
│   │   │   └── session.py    # Async Session 設定
│   │   ├── models/           # SQLAlchemy ORM 模型
│   │   │   ├── user.py
│   │   │   └── project.py
│   │   ├── schemas/          # Pydantic Schemas (資料驗證/序列化)
│   │   │   ├── user.py
│   │   │   └── token.py
│   │   ├── services/         # [核心] 複雜業務邏輯層
│   │   │   ├── ansible/      # 封裝 Ansible 命令執行邏輯
│   │   │   └── socket_mgr.py # WebSocket 管理器
│   │   ├── worker/           # [新增] Celery Tasks 實作
│   │   │   └── runner_tasks.py # 實際執行 Ansible 的 worker
│   │   ├── main.py           # FastAPI 入口
│   │   └── initial_data.py   # 初始化腳本
│   ├── tests/                # [新增] Pytest 測試
│   ├── alembic.ini           # Alembic 設定檔
│   ├── pyproject.toml        # 現代化依賴管理 (Poetry 或 setuptools)
│   └── requirements.txt
└── docker-compose.yml        # 需新增 Redis 與 Celery Worker 服務
```