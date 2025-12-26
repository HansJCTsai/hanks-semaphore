from fastapi import APIRouter

from backend.app.api.v1.endpoints import users

api_router = APIRouter()

# 這裡就是把 users.py 裡的路由掛載進來
# prefix="/users" 代表網址會變成 /api/v1/users/xxx
# tags=["users"] 代表在 Swagger 上面會分類在 "users" 這個標籤下
api_router.include_router(users.router, prefix="/users", tags=["users"])

# 未來如果你寫了 projects.py，就在這裡加一行：
# from backend.app.api.v1.endpoints import projects
# api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
