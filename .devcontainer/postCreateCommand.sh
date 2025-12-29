#!/bin/bash
# ==================================================================================
# 專案初始化腳本 (Dev Container)
# 維護者: Hanks Jc Tsai
# 用途: 
#   1. 安裝系統級依賴 (DB Client, Redis Tools)
#   2. 初始化前端 (NPM)
#   3. 同步設定檔與安裝後端依賴 (Python, Ansible, Celery)
#   4. 產生開發用環境變數 (.env)
# ==================================================================================
set -e

echo "🚀 [Start] 開始初始化 Dev Container (Pure Python 3.11)..."

# ----------------------------------------------------------------------------------
# 1. 安裝系統工具 (System Dependencies)
# ----------------------------------------------------------------------------------
echo "🐘 [Step 1] Installing System Tools..."
sudo apt-get update

# 安裝清單：
# - postgresql-client: 用於 pg_isready 檢查資料庫狀態
# - redis-tools: 提供 redis-cli，方便除錯 Redis 佇列
# - libpq-dev: Python 的 psycopg2 套件編譯時需要此函式庫 (重要!)
sudo apt-get install -y postgresql-client redis-tools libpq-dev

# ----------------------------------------------------------------------------------
# 2. 前端依賴 (Frontend)
# ----------------------------------------------------------------------------------
# 檢查 web 目錄是否存在，避免在純後端模式下報錯
if [ -d "./web" ]; then
    echo "📦 [Step 2] Installing NPM dependencies (Frontend)..."
    # DevContainer Features 已經幫我們裝好 Node.js，直接跑 npm install 即可
    (cd ./web && npm install)
fi

# ----------------------------------------------------------------------------------
# 3. 同步設定檔 (Config Sync)
# ----------------------------------------------------------------------------------
# 將 .devcontainer 中的設定檔同步到 backend 目錄，確保開發環境一致性
echo "📂 [Step 3] Syncing config files to backend/..."

# (A) 同步 config.json (Semaphore 核心設定)
if [ -f ".devcontainer/config.json" ]; then
    cp .devcontainer/config.json backend/config.json
    echo "   ✅ Copied config.json"
else
    echo "   ⚠️ Notice: .devcontainer/config.json not found, skipping."
fi

# (B) 同步 requirements.txt (Python 依賴清單)
if [ -f ".devcontainer/requirements.txt" ]; then
    cp .devcontainer/requirements.txt backend/requirements.txt
    echo "   ✅ Copied requirements.txt"
else
    echo "   ⚠️ Notice: .devcontainer/requirements.txt not found, skipping."
fi

# ----------------------------------------------------------------------------------
# 4. Python 環境設置 (Backend Setup)
# ----------------------------------------------------------------------------------
echo "🐍 [Step 4] Setting up Python Virtual Environment..."

# 重建虛擬環境，確保乾淨
rm -rf .venv
python3 -m venv .venv
PIP="./.venv/bin/pip"

# 升級 pip 本身
$PIP install --upgrade pip

# (A) 安裝 Ansible [關鍵修改: 鎖定版本]
# 使用 Ansible 9.x (包含 ansible-core 2.16)，這是目前長期支援且穩定的版本
echo "   📦 Installing Ansible (Fixed Version)..."
$PIP install ansible==9.6.1 ansible-lint

# (B) 安裝後端依賴
if [ -f "backend/requirements.txt" ]; then
    echo "   📜 Installing dependencies from requirements.txt..."
    $PIP install -r backend/requirements.txt
else
    # 備援方案：如果沒有 requirements.txt，則手動安裝核心套件
    echo "   ⚡ requirements.txt missing, installing default stack manually..."
    # fastapi: Web 框架
    # celery/redis/flower: 非同步任務與監控
    # sqlalchemy/asyncpg/psycopg2-binary: 資料庫驅動
    $PIP install fastapi uvicorn[standard] sqlalchemy asyncpg alembic \
                 pydantic-settings python-multipart requests \
                 celery redis flower passlib[bcrypt] email-validator \
                 psycopg2-binary
fi

# ----------------------------------------------------------------------------------
# 5. 產生環境變數 (.env)
# ----------------------------------------------------------------------------------
# 如果 .env 不存在，自動產生一份預設的開發用設定
if [ ! -f .env ]; then
    echo "📝 [Step 5] Generating default .env file..."
    
    # 資料庫連線 (PostgreSQL)
    echo "DATABASE_URL=postgresql+asyncpg://semaphore:changeme@db:5432/semaphore" > .env
    
    # Celery 任務佇列連線 (Redis)
    # 使用 redis:6379 是因為 docker-compose 裡的 service name 叫 'redis'
    # 格式：redis://:密碼@主機:Port/DB
    echo "CELERY_BROKER_URL=redis://:Redi$_P@ssw0rd@redis:6379/0" >> .env
    echo "CELERY_RESULT_BACKEND=redis://:Redi$_P@ssw0rd@redis:6379/0" >> .env
    
    # 安全性密鑰 (開發用)
    echo "SECRET_KEY=dev-secret-key-change-me" >> .env
fi

# ----------------------------------------------------------------------------------
# 6. 等待服務就緒 (Health Check)
# ----------------------------------------------------------------------------------
echo "⏳ [Step 6] Waiting for Database to be ready..."

# 使用 pg_isready 迴圈檢查 DB 是否啟動
if command -v pg_isready &> /dev/null; then
    until pg_isready -h db -U semaphore; do
      echo "   ... waiting for host: db"
      sleep 2
    done
else
    # 如果沒裝 client (極端情況)，就用 sleep 盲等
    echo "   ⚠️ pg_isready not found, sleeping 5s instead."
    sleep 5
fi

# ==================================================================================
# 完成
# ==================================================================================
echo "✅ Dev Container Ready! Happy Coding!"
echo "------------------------------------------------------------------"
echo "👉 Start API Server : ./.venv/bin/uvicorn backend.app.main:app --reload --host 0.0.0.0"
echo "👉 Start Worker     : ./.venv/bin/celery -A backend.app.worker worker --loglevel=info"
echo "👉 Start Monitor    : ./.venv/bin/celery -A backend.app.worker flower"
echo "------------------------------------------------------------------"