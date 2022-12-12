import motor as motor
from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from models.link3 import GetLinkinfo

linkinfo_route = APIRouter()

@linkinfo_route.get("/")
async def get_link(link: str):
    try:
        mongo_client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://172.30.1.26:27017')
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
    db = mongo_client['linkl']
    collection = db['link']
    try:
        redirect_link = await collection.find_one({"link": link})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
    if redirect_link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    return JSONResponse(status_code=200, content={"link": link, "redirect_link": redirect_link['redirect_link'], "created_at": str(redirect_link['created_at']), "using": redirect_link['using']})