from datetime import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base_class import Base
from backend.app.models.project_user import ProjectUser


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

    projects: Mapped[List["ProjectUser"]] = relationship(
        "ProjectUser", back_populates="user"
    )
