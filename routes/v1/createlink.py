import asyncio
import motor.motor_asyncio
import json
import datetime
from fastapi import APIRouter, Request
from starlette.responses import JSONResponse
from models.link2 import CrateLink
create_route = APIRouter()


@create_route.post("/create")
async def create_link(link: CrateLink,request: Request):
    mongo_client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://172.30.1.26:27017')
    db = mongo_client['linkl']
    collection = db['link']
    original_payload = {
        "link": link.link,
        "redirect_link": link.redirect_link,
        "created_at": datetime.datetime.now(),
        "using": 0,
        "create_by": request.client.host
    }
    if await collection.find_one({"link": link.link}) is not None:
        return JSONResponse(status_code=401, content={"link is already exists": link.link})
    await collection.insert_one(original_payload)
    return JSONResponse(status_code=200, content={"link": link.link, "redirect_link": link.redirect_link})


