from typing import List

# [修正] 移除了 backend.app.api.deps，因為還不存在
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app import crud, models, schemas
from backend.app.db.session import get_db

router = APIRouter()


# ----------------------------------------------------------------------
# GET /users/me - 取得當前登入者資料
# ----------------------------------------------------------------------
@router.get("/me", summary="取得當前登入者資料", response_model=schemas.UserResponse)
async def read_user_me(
    # [注意] 這裡通常會依賴一個驗證函式 (get_current_user)
    # 因為我們還沒做登入，這裡先暫時註解掉或寫一個假的
    # current_user: User = Depends(deps.get_current_active_user),
    # [暫時方案] 為了讓你現在能測試，我們先用假的：假設 ID=1 是當前使用者
    db: AsyncSession = Depends(get_db),
) -> models.user:
    """
    取得當前登入使用者的詳細資料 (Get current user).
    注意：在未實作 JWT Auth 前，此端點暫時寫死回傳 ID=1 的使用者以供測試。
    """

    # --- [正式版邏輯] (等下一章做完 Auth 後啟用) ---
    # return current_user

    # --- [臨時版邏輯] (方便你現在測試) ---
    # 假設目前登入的是 ID 為 1 的使用者 (通常是 admin)
    mock_current_user_id = 1
    user_me = await crud.user.get_user(db, mock_current_user_id)
    if not user_me:
        raise HTTPException(
            status_code=404, detail="User not found (Test user ID 1 missing)"
        )
    return user_me


# ----------------------------------------------------------------------
# GET /users/ - 取得所有使用者
# ----------------------------------------------------------------------
@router.get("/", response_model=List[schemas.UserResponse])
async def read_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[models.User]:
    """
    取得使用者列表 (Retrieve users).
    """
    # 這裡的 crud.user 就是指 crud_user.py 模組
    users = await crud.user.get_users(db, skip=skip, limit=limit)
    return users


# ----------------------------------------------------------------------
# GET /users/{user_id} - 取得單一使用者
# ----------------------------------------------------------------------
@router.get("/{user_id}", response_model=schemas.UserResponse)
async def read_user(
    db: AsyncSession = Depends(get_db),
    user_id: int = 0,
) -> models.User:
    """
    根據 ID 取得特定使用者 (Get user by ID).
    """
    user = await crud.user.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    return user


# ----------------------------------------------------------------------
# POST /users/ - 建立新使用者
# ----------------------------------------------------------------------
@router.post("/", response_model=schemas.UserResponse)
async def create_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: schemas.UserCreate,
) -> models.User:
    """
    建立新使用者 (Create new user).
    """
    user = await crud.user.get_user_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    user = await crud.user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user = await crud.user.create_user(db, user=user_in)
    return user


# ----------------------------------------------------------------------
# PUT /users/{user_id} - 更新使用者
# ----------------------------------------------------------------------
@router.put("/{user_id}", response_model=schemas.UserResponse)
async def update_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
) -> models.User:
    """
    更新使用者資料 (Update a user).
    """
    user = await crud.user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )

    user = await crud.user.update_user(db, db_user=user, user_in=user_in)
    return user


# ----------------------------------------------------------------------
# DELETE /users/{user_id} - 刪除使用者
# ----------------------------------------------------------------------
@router.delete("/{user_id}", response_model=schemas.UserResponse)
async def delete_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: int,
) -> models.User:
    """
    刪除使用者 (Delete a user).
    """
    user = await crud.user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )

    await crud.user.delete_user(db, user_id=user_id)
    return user
