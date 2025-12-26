from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# 修正引用路徑
from backend.app.core.security import get_hashed_password
from backend.app.models.user import User
from backend.app.schemas import UserCreate, UserUpdate


# ==============================================================================
# READ Operations
# ==============================================================================
async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    # [修正] 加上 await
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    # [修正] 參數改為 username，並加上 await
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    # [修正] User.mail 改為 User.email，並加上 await
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


# [新增] 補回 get_users 函式，因為 users.py 有用到
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


# ==============================================================================
# CREATE Operations
# ==============================================================================
async def create_user(db: AsyncSession, user: UserCreate) -> User:
    # [修正] 這裡要把 user.password 拿去雜湊，之前寫成 user.email 了！
    hashed_password = get_hashed_password(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        name=user.name,
        password=hashed_password,
        admin=False,
        alert=False,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


# ==============================================================================
# UPDATE Operations
# ==============================================================================
async def update_user(db: AsyncSession, *, db_user: User, user_in: UserUpdate) -> User:
    update_user_data = user_in.model_dump(exclude_unset=True)

    if "password" in update_user_data and update_user_data["password"]:
        hashed_password = get_hashed_password(update_user_data["password"])
        update_user_data["password"] = hashed_password

    for field, value in update_user_data.items():
        setattr(db_user, field, value)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


# ==============================================================================
# DELETE Operations
# ==============================================================================
async def delete_user(db: AsyncSession, user_id: int) -> Optional[User]:
    # [修正] 加上 await
    user_data = await get_user(db=db, user_id=user_id)
    if user_data:
        await db.delete(user_data)
        await db.commit()
    return user_data
