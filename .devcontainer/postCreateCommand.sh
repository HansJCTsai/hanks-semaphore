#!/bin/bash
set -e

echo "🚀 開始初始化 Dev Container (Pure Python 3.11)..."

# --- 1. 安裝系統工具 ---
# 新的 Image 已經有 Python/SSL 了，我們只需要裝 DB Client
echo "🐘 Installing PostgreSQL Client..."
sudo apt-get update
sudo apt-get install -y postgresql-client

# --- 2. 前端依賴 ---
# DevContainer Feature 會幫我們裝好 Node.js，這裡直接跑 npm 即可
if [ -d "./web" ]; then
    echo "📦 Installing NPM dependencies..."
    (cd ./web && npm install)
fi

# --- 3. Python 環境設置 ---
echo "🐍 Setting up Python venv..."

# 清除舊環境
rm -rf .venv

# 建立虛擬環境
python3 -m venv .venv

PIP="./.venv/bin/pip"

echo "📦 Installing Python Dependencies..."
$PIP install --upgrade pip

# 安裝 Ansible
$PIP install ansible

# 安裝 FastAPI 後端全家桶
echo "⚡ Installing FastAPI stack..."
$PIP install fastapi uvicorn[standard] sqlalchemy asyncpg alembic pydantic-settings python-multipart requests

# 產生預設 .env
if [ ! -f .env ]; then
    echo "📝 Generating .env for FastAPI..."
    echo "DATABASE_URL=postgresql+asyncpg://semaphore:changeme@db:5432/semaphore" > .env
    echo "SECRET_KEY=dev-secret-key-change-me" >> .env
fi

# ==========================================
# 4. 等待 DB 就緒
# ==========================================
echo "⏳ Waiting for DB to be ready..."
if command -v pg_isready &> /dev/null; then
    until pg_isready -h db -U semaphore; do
      echo "   Waiting for DB (host: db)..."
      sleep 2
    done
else
    echo "⚠️ pg_isready not found, sleeping 5s instead."
    sleep 5
fi

echo "✅ Dev Container Ready!"
echo "👉 Start Python Backend: ./.venv/bin/uvicorn backend.app.main:app --reload --host 0.0.0.0"