from fastapi import APIRouter

from backend.app.api.v1.endpoints import health, users

api_router = APIRouter()

# 這裡就是把 users.py 裡的路由掛載進來
# prefix="/users" 代表網址會變成 /api/v1/users/xxx
# tags=["users"] 代表在 Swagger 上面會分類在 "users" 這個標籤下
api_router.include_router(users.router, prefix="/users", tags=["users"])

# 未來如果你寫了 projects.py，就在這裡加一行：
# from backend.app.api.v1.endpoints import projects
# api_router.include_router(projects.router, prefix="/projects", tags=["projects"])

# [新增] 掛載 health 路由
# 這樣存取路徑會是 /api/v1/ping (或是你想完全模仿原版放在 /api/ping 也可以，但在這裡我們先遵循 v1 規範)
api_router.include_router(health.router, tags=["system"])
