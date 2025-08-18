import motor

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

db = client.get_database('fastapi')

collection = db.get_collection('users')

print("Mongo DB connected")