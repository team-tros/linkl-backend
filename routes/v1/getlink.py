import motor as motor
from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from models.link1 import GetLink
getlink_route = APIRouter()


@getlink_route.get("/{link}")
async def get_link(link: str):
    mongo_client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://172.30.1.26:27017')
    db = mongo_client['linkl']
    collection = db['link']
    redirect_link = await collection.find_one({"link": link})
    if redirect_link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    await collection.update_one({"link": link}, {"$inc": {"using": 1}})
    return JSONResponse(status_code=200, content={"link": link, "redirect_link": redirect_link['redirect_link']})


