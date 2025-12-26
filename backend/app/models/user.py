from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base_class import Base


class User(Base):
    __tablename__ = "user"

    # PK ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Timestamp
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Account Info
    username: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    # Premission Flags
    admin: Mapped[bool] = mapped_column(Boolean, default=False)
    alert: Mapped[bool] = mapped_column(Boolean, default=False)
