import os
from fastapi import FastAPI
from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo import MongoClient
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

client = MongoClient(
    host=os.getenv("MONGO_HOST"),
    port=int(os.getenv("MONGO_PORT")),
    username=os.getenv("MONGO_USERNAME"),
    password=os.getenv("MONGO_PASSWORD"),
)


db = client["ipo"]

collection = db["ipo"]


class IpoIn(BaseModel):
    query: str = Field(..., min_length=1, max_length=200)
    result: str = Field(..., min_length=1, max_length=2000)
    source_documents: list[str] = Field(..., min_items=1, max_items=10)


class IpoOut(BaseModel):
    query: str
    result: str
    source_documents: list[str]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/", response_model=IpoOut)
def create_ipo(ipo: IpoIn):
    ipo = ipo.model_dump()
    ipo_id = collection.insert_one(ipo).inserted_id
    ipo = collection.find_one({"_id": ipo_id})
    return ipo


@app.post("/ipo/{ipo_id}")
def delete_ipo(ipo_id: str):
    result = collection.delete_one({"_id": ObjectId(ipo_id)})
    if result.deleted_count == 1:
        return {"success": True}
    return {"success": False}


@app.get("/ipo", response_model=list[IpoOut])
def read_ipo():
    ipos = list(collection.find())
    return ipos
