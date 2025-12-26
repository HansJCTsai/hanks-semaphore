from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from backend.app.core.config import settings

# 建立非同步引擎
# echo=True 會印出 SQL 語句，方便開發時除錯，正式環境建議關閉
engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)

# 建立 Session 工廠
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# Dependency (依賴注入函數)
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
