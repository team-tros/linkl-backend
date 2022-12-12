import datetime
import motor as motor
import redis.asyncio as redis
from fastapi import APIRouter, HTTPException, Request
from starlette.responses import JSONResponse
getlink_route = APIRouter()


@getlink_route.get("/get")
async def get_link(link: str, request: Request):
    try:
        mongo_client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://172.30.1.26:27017')
        r = await redis.from_url('redis://localhost:6379/1')
    except Exception as e:
       return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
    db = mongo_client['linkl']
    collection = db['link']
    collection2 = db['logs']
    try:
        redirect_link = await r.get(link)
        await collection.update_one({"link": link}, {"$inc": {"using": 1}})
        data = {
            "link": link,
            "time": str(datetime.datetime.now()),
            "ip":  request.client.host
        }
        await collection2.insert_one(data)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
    if redirect_link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    return JSONResponse(status_code=200, content={"link": link, "redirect_link": redirect_link.decode()})


