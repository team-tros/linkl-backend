from fastapi import APIRouter

# from .users import users_router
from .getlink import getlink_route
from .createlink import create_route
from .getlinkinfo import linkinfo_route
v1_router = APIRouter()

# v1_router.include_router(users_router, prefix="/users", tags=["users"])
v1_router.include_router(getlink_route, prefix="/link", tags=["link"])
v1_router.include_router(create_route, prefix="/link", tags=["link"])
v1_router.include_router(linkinfo_route, prefix="/info", tags=["link"])