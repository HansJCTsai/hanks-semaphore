from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.app.api.v1.router import api_router
from backend.app.core.config import settings
from backend.app.db.base_class import Base
from backend.app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 應用程式啟動時：建立資料庫表
    print("Creating database tables...")
    async with engine.begin() as conn:
        # 這裡會建立所有繼承自 Base 的模型資料表 (如果表已存在則會跳過)
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created.")
    yield
    # 應用程式關閉時 (如果有的話)


# [修改] 加入 lifespan 參數
app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.include_router(api_router, prefix=settings.API_V1_STR)
