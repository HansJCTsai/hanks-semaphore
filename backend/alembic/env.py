import asyncio
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# ----------------- [關鍵修改 1] 加入路徑以便匯入 app -----------------
# 將 backend 目錄加入 python path，這樣才能 import app
sys.path.append(str(Path(__file__).parent.parent))

# ----------------- [關鍵修改 2] 匯入您的設定與 Models -----------------
from backend.app.core.config import settings  # 匯入您剛剛給我的 config.py
from backend.app.models import Base  # 匯入所有的 Models

# --------------------------------------------------------------------

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 設定 target_metadata，讓 Alembic 知道要比對哪些 Table
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # 直接使用 config.py 裡的連線字串
    url = settings.SQLALCHEMY_DATABASE_URI
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.
    """

    # ----------------- [關鍵修改 3] 使用 config.py 的連線字串 -----------------
    # 覆蓋 alembic.ini 裡的設定，直接用 Python 算出來的 URL
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.SQLALCHEMY_DATABASE_URI
    # ------------------------------------------------------------------------

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
