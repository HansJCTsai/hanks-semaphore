# backend/app/db/base.py

# 1. 導入基礎 Base 類別
from backend.app.db.base_class import Base

# 2. 導入所有的 Model
# 即使這裡沒用到，也必須 import，這樣 Base.metadata 才能收集到它們
from backend.app.models.user import User
from backend.app.models.project import Project
from backend.app.models.project_user import ProjectUser