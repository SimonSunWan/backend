from fastapi import APIRouter

from app.api import cache, department, dictionary, menu, role, system, user

api_router = APIRouter()

# 路由配置
ROUTES = [
    (user.router, "/user", ["user"]),
    (dictionary.router, "/dictionary", ["dictionary"]),
    (role.router, "/role", ["role"]),
    (menu.router, "/menu", ["menu"]),
    (department.router, "/department", ["department"]),
    (system.router, "/system", ["system-settings"]),
    (cache.router, "/cache", ["cache"]),
]

for router, prefix, tags in ROUTES:
    api_router.include_router(router, prefix=prefix, tags=tags)
