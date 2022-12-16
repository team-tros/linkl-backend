import motor as motor
from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from models.link3 import GetLinkinfo

link_used_info_route = APIRouter()

@link_used_info_route.get("/")
async def get_link(link: str):
    try:
        mongo_client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://172.30.1.26:27017')
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
    db = mongo_client['linkl']
    collection = db['logs']
    try:
        """limit query to 50"""
        log = await collection.find({"link": link}).limit(50).to_list(length=50)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
    if log is None:
        raise HTTPException(status_code=404, detail="Link not found")
    """return log list"""
    result = []
    count = 0
    for i in log:
        count = count + 1
        result.append({"index": count, "time": i['time']})
    return JSONResponse(status_code=200, content={"link": link, "log": result})
