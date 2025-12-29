from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db import session

router = APIRouter()


@router.get(
    "/ping", summary="心跳檢測", response_description="回傳 'pong' 表示服務存活"
)
async def ping(db: AsyncSession = Depends(session.get_db)):
    """
    用於 Health Check 的端點。
    回傳純文字 "pong" 以相容原版 Semaphore 行為。
    """
    try:
        db.execute("SELECT 1")
        return Response(
            content="pong", status_code=200, media_type="text/plain; charset=utf-8"
        )
    except Exception:
        # 如果資料庫連不上，回傳 500，這樣 Docker 就會標記為 unhealthy
        raise HTTPException(status_code=500, detail="Database connection failed")
