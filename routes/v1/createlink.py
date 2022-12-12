import motor.motor_asyncio
import datetime
import redis.asyncio as redis
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from starlette import status
from starlette.responses import JSONResponse
from models.link import CrateLink

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def auth_request(token: str = Depends(oauth2_scheme)) -> bool:
    authenticated = token == "test_key"
    return authenticated

create_route = APIRouter()


@create_route.post("/create")
async def create_link(request: Request, link: CrateLink):
    try:
        r = await redis.Redis(host='localhost', port=6379, db=1)
        mongo_client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://172.30.1.26:27017")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
    db = mongo_client["linkl"]
    collection = db["link"]
    if await collection.find_one({"link": link.link}) is not None:
        return JSONResponse(status_code=409, content={"detail": "Link already exists"})
    mongo_payload = {
        "link": link.link,
        "redirect_link": link.redirect_link,
        "created_at": datetime.datetime.now(),
        "using": 0
    }
    try:
        await collection.insert_one(mongo_payload)
        await r.set(link.link, link.redirect_link)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
    return JSONResponse(status_code=201, content={"link": link.link,
                                                  "redirect_link": link.redirect_link,
                                                  "created_at": str(datetime.datetime.now())
                                                  })
