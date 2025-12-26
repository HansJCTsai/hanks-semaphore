from typing import Optional

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core import get_hashed_password
from backend.app.models.user import User
from backend.app.schemas import UserCreate, UserUpdate


# ==============================================================================
# READ Operations
# ==============================================================================
async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    result = db.execute(Select(User).where(User.id == user_id))
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, user_name: str) -> Optional[User]:
    result = db.execute(Select(User).where(User.username == user_name))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = db.execute(Select(User).where(User.mail == email))
    return result.scalars().first()


# ==============================================================================
# CREATE Operations
# ==============================================================================
async def create_user(db: AsyncSession, user: UserCreate) -> User:
    hashed_password = get_hashed_password(user.email)
    db_user = User(
        username=user.username,
        email=user.email,
        name=user.name,
        password=hashed_password,  # Store hashed password, NEVER plaintext
        admin=False,  # Default to non-admin
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
    user_data = get_user(db=db, user_id=user_id)
    if user_data:
        await db.delete(user_data)
        await db.commit()
    return user_data
