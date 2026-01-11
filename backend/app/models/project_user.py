from enum import Enum

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base_class import Base


class ProjectRole(str, Enum):
    OWNER = "owner"
    MANAGER = "manager"
    TASK_RUNNER = "task_runner"
    GUEST = "guest"


class ProjectUser(Base):
    __tablename__ = "project_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # 外鍵關聯
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("project.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    role: Mapped[str] = mapped_column(String, nullable=False, default=ProjectRole.GUEST)

    # [關鍵對應]
    # "User" -> 對應 User class (必須大寫)
    # back_populates="projects" -> 對應 User class 裡面的 projects 變數 (修正1加上的那個)
    user = relationship("User", back_populates="projects")

    # "Project" -> 對應 Project class (必須大寫，修正2改的那個)
    # back_populates="users" -> 對應 Project class 裡面的 users 變數
    project = relationship("Project", back_populates="users")

    __table_args__ = (
        UniqueConstraint("project_id", "user_id", name="unique_project_user_role"),
    )
