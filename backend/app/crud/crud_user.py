from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# 修正引用路徑
from backend.app.core.security import get_hashed_password
from backend.app.models.user import User
from backend.app.schemas import UserCreate, UserUpdate


class daoUser:
    """
    User CRUD 操作封裝
    """

    # ==============================================================================
    # READ Operations
    # ==============================================================================
    # [修正] 加上 self
    async def get_user(self, db: AsyncSession, user_id: int) -> Optional[User]:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    # [修正] 加上 self
    async def get_user_by_username(
        self, db: AsyncSession, username: str
    ) -> Optional[User]:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalars().first()

    # [修正] 加上 self
    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    # [修正] 加上 self (這就是報錯的地方！)
    async def get_users(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[User]:
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    # ==============================================================================
    # CREATE Operations
    # ==============================================================================
    # [修正] 加上 self，並將參數名稱改為 obj_in 以符合通用習慣 (非強制，但建議)
    async def create(self, db: AsyncSession, obj_in: UserCreate) -> User:
        hashed_password = get_hashed_password(obj_in.password)

        db_user = User(
            username=obj_in.username,
            email=obj_in.email,
            name=obj_in.name,
            password=hashed_password,
            admin=getattr(
                obj_in, "admin", False
            ),  # 防止 UserCreate 沒有 admin 欄位時報錯
            alert=False,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    # ==============================================================================
    # UPDATE Operations
    # ==============================================================================
    # [修正] 加上 self
    async def update(
        self, db: AsyncSession, *, db_user: User, user_in: UserUpdate
    ) -> User:
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
    # [修正] 加上 self
    async def delete(self, db: AsyncSession, user_id: int) -> Optional[User]:
        # 注意這裡要用 self.get_user 呼叫自己的方法
        user_data = await self.get_user(db=db, user_id=user_id)
        if user_data:
            await db.delete(user_data)
            await db.commit()
        return user_data


# 實例化
daoUser_instan = daoUser()
