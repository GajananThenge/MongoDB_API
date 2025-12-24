from pydantic import BaseModel
# ,HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)

db = client["Customer"]
custdata = db["Customer_coll"]

app = FastAPI()

class cust_data(BaseModel):
    name: str
    phone: int
    city: str
    product: str

# data={"name":"Gajanan",'phone':80800,"city":"Pune","product":"ALL"}

@app.post("/cust/insert")    
async def cust_data_insert_helper(data:cust_data):
    result  = await custdata.insert_one(data.dict())
    return str(result.inserted_id)


def cust_helper(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc


@app.get("/cust/getdata")
async def get_cust_data():
    iterms = []
    cursor = custdata.find({})
    async for document in cursor:
        iterms.append(cust_helper(document))
    return iterms
    
    
@app.get("/cust/showdata")
async def show_cust_data():
    iterms = []
    cursor = custdata.find({})
    async for document in cursor:
        iterms.append(cust_helper(document))
    return iterms
    
