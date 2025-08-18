from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI()

# MongoDB connection
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.get_database("fastapi")
users_collection = db.get_collection("users")

# Pydantic models
class User(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

class UserResponse(User):
    id: str = Field(default_factory=str, alias="_id")

# Helper to convert MongoDB ObjectId
def user_helper(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "age": user.get("age")
    }

# Routes

@app.post("/users", response_model=UserResponse)
async def create_user(user: User):
    new_user = await users_collection.insert_one(user.dict())
    created_user = await users_collection.find_one({"_id": new_user.inserted_id})
    return user_helper(created_user)


# @app.get("/users", response_model=List[UserResponse])
# async def get_users():
#     users = []
#     async for user in users_collection.find():
#         users.append(user_helper(user))
#     return users


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return user_helper(user)
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, updated_user: User):
    result = await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": updated_user.dict()}
    )
    if result.modified_count == 1:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        return user_helper(user)
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/users" , response_model=List[UserResponse])
async def get_users_old():
    users=[]
    async for user in users_collection.find():
        users.append(user_helper(user))
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_particular_user(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return user_helper(user)
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/user/{id}", response_model=UserResponse)
async def update_particular_user(id: str, user: User):
    result = await users_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": user.dict()}
    )
    if result.modified_count == 1:
        user = await users_collection.find_one({"_id": ObjectId(id)})
        return user_helper(user)
    raise HTTPException(status_code=404, detail="User not found")

@app.patch("/user/{id}" , response_model=UserResponse)
async def update_particular_one_patch(id: str, user: User):
    result = await users_collection.update_one(
        {"_id" : ObjectId(id)},
        {"$set": user.dict()}
    )

    if result.modified_count == 1:
        user = await users_collection.find_one({"_id": ObjectId(id)})
        return user_helper(user)
    raise HTTPException(status_code=404, detail="User not found")