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