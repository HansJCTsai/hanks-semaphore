from typing import Any, List

# [修正] 移除了 backend.app.api.deps，因為還不存在
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app import crud, schemas
from backend.app.db.session import get_db

router = APIRouter()


# ----------------------------------------------------------------------
# GET /users/ - 取得所有使用者
# ----------------------------------------------------------------------
@router.get("/", response_model=List[schemas.UserResponse])
async def read_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    取得使用者列表 (Retrieve users).
    """
    # 這裡的 crud.user 就是指 crud_user.py 模組
    users = await crud.user.get_users(db, skip=skip, limit=limit)
    return users


# ----------------------------------------------------------------------
# POST /users/ - 建立新使用者
# ----------------------------------------------------------------------
@router.post("/", response_model=schemas.UserResponse)
async def create_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: schemas.UserCreate,
) -> Any:
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
) -> Any:
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
) -> Any:
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
