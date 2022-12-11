from fastapi import APIRouter

# from .users import users_router
from .getlink import getlink_route
from .createlink import create_route
from .getlinkinfo import getlinkinfo_route
v1_router = APIRouter()

# v1_router.include_router(users_router, prefix="/users", tags=["users"])
v1_router.include_router(getlink_route, prefix="/link", tags=["getlink"])
v1_router.include_router(create_route, prefix="/link", tags=["createlink"])
v1_router.include_router(getlinkinfo_route, prefix="/info", tags=["getlinkinfo"])