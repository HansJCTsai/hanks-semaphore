from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base_class import Base
from backend.app.models.project_user import ProjectUser


class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String, nullable=False)

    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # [設定] 是否開啟警報
    alert: Mapped[bool] = mapped_column(Boolean, default=False)

    # 這裡使用 Optional[str] 且 nullable=True，表示它可以是 NULL
    alert_chat: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # [設定] 最大並行任務數 (0 代表無限制)
    max_parallel_tasks: Mapped[int] = mapped_column(Integer, default=0)

    # [反向關聯]
    # 讓 project.users 可以直接拿到所有成員清單
    # cascade="all, delete-orphan" 會連動 SQLAlchemy 的 session 操作
    users: Mapped[List["ProjectUser"]] = relationship(
        "ProjectUser", back_populates="project", cascade="all, delete-orphan"
    )
