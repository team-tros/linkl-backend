import motor.motor_asyncio
import datetime
import redis.asyncio as redis
import string
import random
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from starlette.responses import JSONResponse
from models.link import CrateLink

create_route = APIRouter()


@create_route.post("/create")
async def create_link(request: Request, link: CrateLink):
    original_link = link.link
    if link.redirect_link is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "redirect_link is required"})
    if link.redirect_link.startswith("http://") or link.redirect_link.startswith("https://") or link.redirect_link.startswith("ftp://") or link.redirect_link.startswith("ftps://") or link.redirect_link.startswith("sftp://") or link.redirect_link.startswith("smb://") or link.redirect_link.startswith("smb://") or link.redirect_link.startswith("chrome://") or link.redirect_link.startswith("magnet://") or link.redirect_link.startswith("mailto://") or link.redirect_link.startswith("tel://") or link.redirect_link.startswith("telnet://") or link.redirect_link.startswith("webdav://") or link.redirect_link.startswith("webdavs://") or link.redirect_link.startswith("ws://") or link.redirect_link.startswith("wss://") or link.redirect_link.startswith("file://"):
        pass
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Bad Redirect link"})
    special_characters = "!@#$%^&*()-+?_=,<>/"
    if any(c in special_characters for c in original_link):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Bad link name"})
    try:
        r = await redis.Redis(host='localhost', port=6379, db=1)
        mongo_client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://172.30.1.26:27017")
    except Exception:
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
    db = mongo_client["linkl"]
    collection = db["link"]
    if original_link == "" or None:
        while True:
            original_link = "".join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(9))
            if await collection.find_one({"link": original_link}) is None:
                break
    elif await collection.find_one({"link": original_link}) is not None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Link already exists","link": original_link})
    mongo_payload = {
        "link": original_link,
        "redirect_link": link.redirect_link,
        "created_at": datetime.datetime.now(),
        "using": 0
    }
    try:
        await collection.insert_one(mongo_payload)
        await r.set(original_link, link.redirect_link)
    except Exception:
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
    return JSONResponse(status_code=201, content={"link": original_link,
                                                  "redirect_link": link.redirect_link,
                                                  "created_at": str(datetime.datetime.now())
                                                  })
