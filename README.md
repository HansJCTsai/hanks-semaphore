# hanks-semaphore

backend/
├── alembic/                # [DB] 資料庫遷移腳本 (對應 db/sql/migrations)
├── alembic.ini             # [DB] Alembic 設定檔
├── requirements.txt        # [Env] Python 套件清單
├── app/
│   ├── __init__.py
│   ├── main.py             # [App] 程式入口 (FastAPI App 初始化)
│   │
│   ├── core/               # [Config] 核心設定
│   │   ├── __init__.py
│   │   ├── config.py       # 環境變數與全域設定 (對應 util/config.go)
│   │   └── security.py     # 密碼加密、JWT Token (對應 util/encryption.go)
│   │
│   ├── db/                 # [DB] 資料庫連線
│   │   ├── __init__.py
│   │   ├── base.py         # 用於 Alembic 匯入所有 Models
│   │   ├── base_class.py   # SQLAlchemy Base 類別
│   │   └── session.py      # DB Session/Engine 設定 (對應 db/sql/SqlDb.go)
│   │
│   ├── models/             # [Model] 資料庫表結構 (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── user.py         # User Table (對應 db/User.go)
│   │   ├── project.py      # Project Table (對應 db/Project.go)
│   │   ├── task.py         # Task Table
│   │   └── ...
│   │
│   ├── schemas/            # [Schema] API 資料驗證模型 (Pydantic)
│   │   # 這是 Go 裡面的 Struct Tag (json:"...") 的替代品
│   │   ├── __init__.py
│   │   ├── user.py         # User Create/Update/Response
│   │   ├── project.py
│   │   └── token.py        # Login Token Schema
│   │
│   ├── crud/               # [CRUD] 資料庫操作邏輯
│   │   # 把 SQL 邏輯從 API 層抽離出來 (對應 db/sql/*.go)
│   │   ├── __init__.py
│   │   ├── crud_user.py    # 建立、查詢使用者的 SQL 邏輯
│   │   ├── crud_project.py
│   │   └── base.py         # 通用的 CRUD 基礎類別
│   │
│   ├── api/                # [Web] API 路由層
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py         # 註冊所有路由
│   │       └── endpoints/        # 各個功能模組的 Controller
│   │           ├── login.py      # 登入 API (對應 api/login.go)
│   │           ├── users.py      # 使用者 API (對應 api/users.go)
│   │           ├── projects.py   # 專案 API (對應 api/projects.go)
│   │           └── ws.py         # WebSocket (對應 api/sockets/)
│   │
│   └── services/           # [Service] 複雜商業邏輯
│       ├── __init__.py
│       └── task_runner/    # 任務執行核心 (對應 services/tasks/)
│           ├── __init__.py
│           ├── runner.py   # 呼叫 Ansible 的核心邏輯
│           └── logger.py   # 處理 Log 串流
│
└── tests/                  # 測試代碼